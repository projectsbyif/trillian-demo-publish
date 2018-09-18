import datetime
import re
import logging

import requests
import utcdatetime

LOG = logging.getLogger(__name__)


class RequestsWrapper():
    def __init__(self, user_agent, cache_for=None):
        if cache_for is not None:
            import requests_cache
            self._session = requests_cache.core.CachedSession(
                expire_after=cache_for
            )
        else:
            self._session = requests.Session()

        self._user_agent = user_agent

    def get(self, *args, **kwargs):
        headers = requests.structures.CaseInsensitiveDict(
            kwargs.get('headers', {})
        )

        if 'user-agent' not in headers:
            headers['user-agent'] = self._user_agent

        timeout = kwargs.pop('timeout', 10)

        return self._session.get(
            headers=headers, timeout=timeout, *args, **kwargs
        )


class TrafficCounterAPI():
    BASE_URL = 'https://traffic-counter.projectsbyif.com/'

    def __init__(self):
        pass

    def download(self, after, before):
        http = RequestsWrapper(
            'https://github.com/projectsbyif/trillian-demo-publish'
        )
        response = http.get(self.BASE_URL)
        response.raise_for_status()

        def within_time_range(row):
            return after < row['datetime'] < before

        def not_null(row):
            "Return false if any of the dict's values are '', False, None"
            return all(row.values())

        rows_in_time_range = filter(
            within_time_range,
            DataFormatConverter(response.json()).convert()
        )

        rows_without_nulls = filter(not_null, rows_in_time_range)

        return map(self._stringify_row_timestamp, rows_without_nulls)

    @staticmethod
    def _datetime_to_day(dt, round_up):
        assert isinstance(dt, (datetime.datetime, utcdatetime.utcdatetime)), \
            'expected datetime, got {}: `{}`'.format(type(dt), dt)

        if round_up:
            dt += datetime.timedelta(hours=24)

        return dt.date()

    @staticmethod
    def _stringify_row_timestamp(row):
        row['datetime'] = str(row['datetime'])
        return row


class DataFormatConverter():
    """
    Converts a particular format of JSON into CSV rows
    """

    def __init__(self, data):
        self._data = data
        self._columns = {}

        self.parse_columns()

    def convert(self):
        for row in self._data['TrafficData']['RawData']['Data']:
            new_row = {}

            for id_, value in row.items():
                new_row[self._columns[id_.lstrip('@')]] = value

            new_row['datetime'] = self._parse_date(
                new_row.pop('date_and_hour_gmt')
            )

            yield new_row

    def parse_columns(self):
        """
        {
            '@ColumnName': 'Eastbridge Road - Pedestrians',
            '@ColumnId': 'Data1'
        }
        """
        assert len(self._data['TrafficData']['Columns']) == 1

        self._columns['MeasurementDateGMT'] = 'date_and_hour_gmt'

        for column_def in self._data['TrafficData']['Columns']['Column']:
            name = column_def['@ColumnName']
            id_ = column_def['@ColumnId']

            self._columns[id_] = name

        for key, value in self._columns.items():
            LOG.debug(' column {} ==> `{}`'.format(key, value))

    def _parse_date(self, string):
        """
        `2018-07-04 00:00`
        """
        match = re.match('(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2})', string)
        year, month, day, hour, minute = [int(x) for x in match.groups()]
        return utcdatetime.utcdatetime(year, month, day, hour, minute)

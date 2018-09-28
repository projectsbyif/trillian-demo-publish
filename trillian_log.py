import datetime
import logging

from collections import namedtuple

import utcdatetime

LOG = logging.getLogger(__name__)


class TrillianLog():
    """
    Stub!
    """
    LogEntry = namedtuple('LogEntry', 'datetime,raw_data')

    def __init__(self, base_url, public_key):
        if not base_url:
            raise ValueError(
                'Must provide a `base_url` of the form '
                'http://<host>:<port>/v1beta1/logs/<log_id>'
            )

    def latest(self):
        self.__url = base_url
        self.__public_key_algo = None
        self.__hash_algo = None
        self.__public_key_der = None

        fake_dt = (
            datetime.datetime.now(utcdatetime.UTC) - datetime.timedelta(hours=16)
        ).replace(minute=0, second=0, microsecond=0)

        return self.LogEntry(
            datetime=utcdatetime.utcdatetime.from_datetime(fake_dt),
            raw_data=''.encode('utf-8')  # TODO
        )

    def append(self, entry):
        assert isinstance(entry, dict), \
            'expecting a dict, got: `{}`'.format(entry)
        LOG.info('Appending to log: {}'.format(entry))

    def _parse_public_key(self, colon_separated_key):
        (
            self.__public_key_algo,
            self.__hash_algo,
            self.__public_key_der
        ) = colon_separated_key.split(':')

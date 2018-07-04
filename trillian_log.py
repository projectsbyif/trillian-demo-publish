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

    def __init__(self, base_url):
        pass

    def latest(self):
        # TODO

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

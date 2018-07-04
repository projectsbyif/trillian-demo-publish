import logging
import sys
import utcdatetime


from traffic_counter_api import TrafficCounterAPI
from trillian_log import TrillianLog


def main(argv):
    logging.basicConfig(level=logging.DEBUG)

    traffic_counter_api = TrafficCounterAPI()
    trillian_log = TrillianLog('http://192.168.99.4')

    most_recent_dt = trillian_log.latest().datetime
    now = utcdatetime.utcdatetime.now()

    logging.info('Most recent timestamp in log: {}'.format(most_recent_dt))

    for row in traffic_counter_api.download(after=most_recent_dt, before=now):
        trillian_log.append(row)


if __name__ == '__main__':
    main(sys.argv)

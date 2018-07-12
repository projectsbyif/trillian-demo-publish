import datetime
import logging
import sys

import utcdatetime

from trillian import TrillianLog

from traffic_counter_api import TrafficCounterAPI
from print_helper import Print


def main(argv):
    logging.basicConfig(level=logging.INFO)

    traffic_counter_api = TrafficCounterAPI()
    trillian_log = TrillianLog.load_from_environment()

    now = utcdatetime.utcdatetime.now()

    Print.status('Getting most recent log entry')

    latest_log_entry = trillian_log.latest()
    Print.tick('Validated signed log root')

    if latest_log_entry is not None:
        most_recent_dt = utcdatetime.utcdatetime.from_string(
            latest_log_entry.json()['datetime']
        )
        Print.tick('Most recent timestamp in log: {}'.format(most_recent_dt))
    else:
        most_recent_dt = now - datetime.timedelta(hours=12)
        Print.bullet('Log looks empty, getting last 12 hours')

    Print.status('Downloading new traffic counts')

    rows_to_push = list(
        traffic_counter_api.download(after=most_recent_dt, before=now)
    )

    Print.bullet('Got {} new counts'.format(len(rows_to_push)))

    if not rows_to_push:
        Print.tick('Log is up to date with the latest counts')
    else:
        Print.status('Inserting new counts into log')

        for row in rows_to_push:
            trillian_log.append(row)

        Print.tick('Inserted {} new counts'.format(len(rows_to_push)))

    print()


if __name__ == '__main__':
    main(sys.argv)

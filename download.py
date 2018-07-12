import datetime
import logging
import os
import sys

import utcdatetime

from trillian import TrillianLog

from traffic_counter_api import TrafficCounterAPI
from print_helper import Print


def main(argv):
    logging.basicConfig(level=logging.INFO)

    traffic_counter_api = TrafficCounterAPI()
    trillian_log = TrillianLog(**load_log_settings())

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
        logging.info('Log looks empty, getting last 12 hours')

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


def load_log_settings():
    url = os.environ.get('TRILLIAN_LOG_URL', None)
    if not url:
        raise RuntimeError(
            'No TRILLIAN_LOG_URL found in `settings.sh`. It should look like '
            'http://<host>:<post>/v1beta1/logs/<log_id>. On the demo log '
            'server, see http://192.168.99.4:5000/demoapi/logs/ to '
            'and look for the `log_url` field'
        )

    public_key = os.environ.get('TRILLIAN_LOG_PUBLIC_KEY', None)

    if not public_key:
        raise RuntimeError(
            'No TRILLIAN_LOG_PUBLIC_KEY found in `settings.sh`. On the demo log '
            'server, see http://192.168.99.4:5000/demoapi/logs/ to '
            'and look for the `public_key` field'
        )

    return {'base_url': url, 'public_key': public_key}


if __name__ == '__main__':
    main(sys.argv)

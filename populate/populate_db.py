# -*- coding: utf-8 -*-

import argparse
import logging
import json
import sys

import requests

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

log = logging.getLogger(__name__)


def main():
    # Set Up Logger
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(levelname)-8s %(message)s',
        datefmt='%a, %d %b %Y %H:%M:%S'
    )

    args = parse_args()
    config = parse_config(args.configpath)
    uri = create_uri(config['database'])
    session = connect_to_db(uri)

    data_sets = get_json_data(session, config['urls'])

    print data_sets

    sys.exit(0)


def get_json_data(session, urls):
    data_sets = []
    for url in urls:
        r = requests.get(url)

        # Convert result from JSON to python object
        try:
            data = json.loads(r.text)
        except Exception:
            log.exception("Could Not Parse JSON Data")
            continue

        # Save decoded json data set
        data_sets.append(data)

    return data_sets


def connect_to_db(uri):
    try:
        engine = create_engine(uri)
        Session = sessionmaker(bind=engine)
        session = Session()
        session.execute('SELECT 1')
        log.info('Successfully Connected To: %s' % uri)

        return session
    except Exception:
        log.exception('Could Not Connect to DB: %s' % uri)
        sys.exit(1)


def create_uri(db_conf):
    uri = 'postgresql://%(user)s:%(password)s@%(host)s:%(port)s/%(db)s'
    return uri % db_conf


def parse_config(filepath):
    try:
        with open(filepath, 'rb') as f:
            data = json.load(f)
            return data
    except Exception:
        log.exception('Count Not Open JSON Config File: %s' % filepath)
        sys.exit(1)


def parse_args():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description='gather and save historical pogo map data'
    )

    # Positional Arguments
    parser.add_argument(
        'configpath', type=str,
        help='path to json config file'
    )

    args = parser.parse_args()
    return args


if __name__ == '__main__':
    main()

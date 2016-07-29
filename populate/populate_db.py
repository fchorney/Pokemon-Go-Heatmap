# -*- coding: utf-8 -*-

import argparse
import logging
import json
import sys

import requests
import pytz

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from datetime import datetime

from models import Pokemon, Gym

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

    data_sets = get_json_data(config['web'])

    current_time = pytz.utc.localize(datetime.utcnow())
    insert_data(session, data_sets, current_time)

    sys.exit(0)


def insert_data(session, data_sets, time):
    for data_set in data_sets:
        for gym in data_set['gyms']:
            insert_gym(session, gym, time)
        for pokemon in data_set['pokemons']:
            insert_pokemon(session, pokemon, time)

    session.commit()


def insert_gym(session, gym, time):
    gym_obj = Gym(
        gym_id=str(gym['gym_id']),
        gym_points=int(gym['gym_points']),
        enabled=bool(gym['enabled']),
        guard_pokemon_id=int(gym['guard_pokemon_id']),
        team_id=int(gym['team_id']),
        last_modified=dt_from_epoch(int(gym['last_modified'])),
        time=time,
        geom='SRID=4326;POINT(%s %s)' % (
            float(gym['longitude']),
            float(gym['latitude'])
        )
    )
    session.merge(gym_obj)

def insert_pokemon(session, pokemon, time):
    pokemon_obj = Pokemon(
        encounter_id=str(pokemon['encounter_id']),
        spawnpoint_id=str(pokemon['spawnpoint_id']),
        disappear_time=dt_from_epoch(int(pokemon['disappear_time'])),
        pokemon_id=int(pokemon['pokemon_id']),
        pokemon_name=unicode(pokemon['pokemon_name']),
        time=time,
        geom='SRID=4326;POINT(%s %s)' % (
            float(pokemon['longitude']),
            float(pokemon['latitude'])
        )
    )
    session.merge(pokemon_obj)

def dt_from_epoch(epoch):
    # epoch uses ms, so cut those off
    s, ms = divmod(epoch, 1000)

    # Grab the dt as utc timezone
    return datetime.fromtimestamp(s, pytz.utc)


def get_json_data(web_conf):
    data_sets = []
    for url in web_conf['urls']:
        headers = {'User-Agent': web_conf['user_agent']}
        r = requests.get(url, headers=headers)

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

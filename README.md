# Pokemon-Go-Heatmap
![Python 2.7](https://img.shields.io/badge/python-2.7-blue.svg) ![PostgreSQL 9.3](https://img.shields.io/badge/postgresql-9.3-blue.svg) ![PostGIS 2.1](https://img.shields.io/badge/postgis-2.1-blue.svg)

Store Pokemon Go historical data to make heatmaps and whatnot

## How to setup
### Ubuntu 14.04 LTS
First install the OS dependencies

Install Postgres 9.3 and Postgis 2.1

```
sudo apt-get install postgresql-9.3 postgresql-server-dev-9.3 postgresql-contrib-9.3 postgresql-9.3-postgis-2.1
```

Create a user and database
```
createuser -U postgres -DRS pogo
createdb -U postgres -O pogo pogo
```

Enable postgis on your new db
```
psql pogo postgres -c 'CREATE EXTENSION postgis'
```
### Python Setup
Clone the project and setup a virtual env
```
virtualenv env
```

Activate and install required packages
```
. ./env/bin/activate
pip install -r requirements.txt
```

### Database Setup
Create the neccessary tables from the sql files included
```
psql pogo pogo -1 -f ./sql/tables/pokemons.sql
psql pogo pogo -1 -f ./sql/tables/gyms.sql
```

## Running
Create a config.json file with the required info based on the included sample_config.json file
and run the populate script
```
cd populate
python populate_db.py ../config.json
```

You will start seeing output as such
```
Fri, 29 Jul 2016 13:01:23 INFO     Successfully Connected To: postgresql://pogo:@127.0.0.1:5432/pogo
Fri, 29 Jul 2016 13:01:23 INFO     Running Every 5 Seconds
Fri, 29 Jul 2016 13:01:28 INFO     Querying The URLs
Fri, 29 Jul 2016 13:01:28 INFO     Starting new HTTP connection (1): www.example.com
Fri, 29 Jul 2016 13:01:36 INFO     Starting new HTTP connection (1): www.example2.com
Fri, 29 Jul 2016 13:01:37 INFO     Populating The Databases
Fri, 29 Jul 2016 13:01:42 INFO     Inserted New Gym Records
Fri, 29 Jul 2016 13:01:42 INFO     685 New Records: 37919 -> 38604
Fri, 29 Jul 2016 13:01:42 INFO     Inserted New Pokemon Records
Fri, 29 Jul 2016 13:01:42 INFO     50 New Records: 6486 -> 6536
Fri, 29 Jul 2016 13:01:42 INFO     Querying The URLs
Fri, 29 Jul 2016 13:01:42 INFO     Starting new HTTP connection (1): www.example.com
Fri, 29 Jul 2016 13:01:47 INFO     Starting new HTTP connection (1): www.example2.com
Fri, 29 Jul 2016 13:01:48 INFO     Populating The Databases
Fri, 29 Jul 2016 13:01:53 INFO     Inserted New Gym Records
Fri, 29 Jul 2016 13:01:53 INFO     685 New Records: 38604 -> 39289
Fri, 29 Jul 2016 13:01:53 INFO     Inserted New Pokemon Records
Fri, 29 Jul 2016 13:01:53 INFO     32 New Records: 6536 -> 6568
```

## Attribution
This projects data source comes from the output of the [Pokemon Go Map](https://github.com/AHAAAAAAA/PokemonGo-Map) Project

## Closing Statement
p.s. I am trash at writing README files and explaining things. 

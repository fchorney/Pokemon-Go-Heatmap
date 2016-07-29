CREATE TABLE pokemon (
    encounter_id TEXT NOT NULL,
    spawnpoint_id TEXT NOT NULL,
    disappear_time TIMESTAMPTZ NOT NULL,
    pokemon_id INTEGER NOT NULL,
    pokemon_name TEXT NOT NULL,
    time TIMESTAMPTZ NOT NULL,
    geom geometry(POINT, 4326) NOT NULL,

    PRIMARY KEY (encounter_id, time)
);

CREATE INDEX pokemon_geom_gist ON pokemon USING gist (geom);

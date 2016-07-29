CREATE TABLE pokemons (
    encounter_id TEXT NOT NULL,
    spawnpoint_id TEXT NOT NULL,
    disappear_time TIMESTAMPTZ NOT NULL,
    pokemon_id INTEGER NOT NULL,
    pokemon_name TEXT NOT NULL,
    time TIMESTAMPTZ NOT NULL,
    geom geometry(POINT, 4326) NOT NULL,

    PRIMARY KEY (encounter_id)
);

CREATE INDEX pokemons_geom_gist ON pokemons USING gist (geom);

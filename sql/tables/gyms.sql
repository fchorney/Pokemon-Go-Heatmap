CREATE TABLE gyms (
    gym_id TEXT NOT NULL,
    gym_points INTEGER NOT NULL,
    enabled BOOLEAN NOT NULL,
    guard_pokemon_id INTEGER NOT NULL,
    team_id INTEGER NOT NULL,
    last_modified TIMESTAMPTZ NOT NULL,
    time TIMESTAMPTZ NOT NULL,
    geom geometry(POINT, 4326) NOT NULL,

    PRIMARY KEY (gym_id, time)
);

CREATE INDEX gyms_geom_gist ON gyms USING gist (geom);

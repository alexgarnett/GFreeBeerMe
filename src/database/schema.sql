DROP TABLE IF EXISTS information;

CREATE TABLE information (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    manufacturer TEXT,
    city TEXT,
    state TEXT,
    country TEXT,
    availability TEXT,
    gf_or_gr TEXT
);
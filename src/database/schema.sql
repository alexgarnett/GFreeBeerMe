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

INSERT INTO information (
    id, name, manufacturer, city, state, country,
    availability, gf_or_gr
    )
VALUES (
    1, 'Redbridge', 'Anheuser-Busch', 'St. Louis',
    'Missouri', 'United States', 'National', 'GF'
    ),
    (
    2, 'Copperpoint Lager', 'Copperpoint', 'Boynton Beach',
    'Florida', 'United States', 'Local', 'GR'
    );
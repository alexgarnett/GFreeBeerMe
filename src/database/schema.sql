DROP TABLE IF EXISTS information;
DROP TABLE IF EXISTS encounters;

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

CREATE TABLE encounters (
    id INTEGER,
    date_of DATE NOT NULL,
    location POINT NOT NULL,
    address TEXT,
    content TEXT NOT NULL
);

INSERT INTO encounters (
    id, date_of, location, address, content
    )
VALUES (
    2, '2023-11-25', '(26.571146, -80.0887830)',
    '4770 N Congress Ave, Boynton Beach, FL 33426, United States',
    'I found a 6-pack of Copperpoint Lager in the beer cooler at Publix'
    ),
    (
    2, '2023-12-15', '(26.56, -80.09)',
    '', 'Test Encounter Test Encounter Test Encounter Test Encounter Test Encounter Test Encounter Test Encounter Test Encounter Test Encounter Test Encounter'
    ),
    (
    1, '2023-12-15', '(26.56, -80.09)',
    '', 'Test Encounter Test Encounter Test Encounter Test Encounter Test Encounter Test Encounter Test Encounter Test Encounter Test Encounter Test Encounter'
    );
-- DROP TABLE IF EXISTS information;
-- DROP TABLE IF EXISTS encounters;


CREATE TABLE IF NOT EXISTS information (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    manufacturer TEXT,
    city TEXT,
    state TEXT,
    country TEXT,
    availability TEXT,
    gf_or_gr TEXT
);

DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM information) THEN
        INSERT INTO information (
            id, name, manufacturer, city, state, country,
            availability, gf_or_gr
            )
        VALUES (1, 'Redbridge', 'Anheuser-Busch', 'St. Louis', 'Missouri', 'United States', 'National', 'GF'),
            (2, 'Copperpoint Lager', 'Copperpoint', 'Boynton Beach', 'Florida', 'United States', 'Local', 'GR'),
            (3, 'Das Pils', 'Copperpoint', 'Boynton Beach', 'Florida', 'United States', 'Local', 'GR'),
            (4, 'B-20 Bombardier', 'Copperpoint', 'Boynton Beach', 'Florida', 'United States', 'Local', 'GR'),
            (5, 'One Love IPA', 'Copperpoint', 'Boynton Beach', 'Florida', 'United States', 'Local', 'GR'),
            (6, 'Trula Saison', 'Copperpoint', 'Boynton Beach', 'Florida', 'United States', 'Local', 'GR'),
            (7, '"G" (Grapefruit) Saison', 'Copperpoint', 'Boynton Beach', 'Florida', 'United States', 'Local', 'GR'),
            (8, 'A10 Hop-Hog', 'Copperpoint', 'Boynton Beach', 'Florida', 'United States', 'Local', 'GR'),
            (9, 'B. Rabbit Espresso Cream Stout', 'Copperpoint', 'Boynton Beach', 'Florida', 'United States', 'Local', 'GR'),
            (10, 'Copperpoint Witness', 'Copperpoint', 'Boynton Beach', 'Florida', 'United States', 'Local', 'GR'),
            (11, 'Copperpoint Blood Orange Wit', 'Copperpoint', 'Boynton Beach', 'Florida', 'United States', 'Local', 'GR'),
            (12, 'Blonde', 'Glutenberg', 'Montreal', 'Quebec', 'Canada', 'Global', 'GF'),
            (13, 'IPA', 'Glutenberg', 'Montreal', 'Quebec', 'Canada', 'Global', 'GF'),
            (14, 'Pale Ale', 'Glutenberg', 'Montreal', 'Quebec', 'Canada', 'Global', 'GF'),
            (15, 'Red', 'Glutenberg', 'Montreal', 'Quebec', 'Canada', 'Global', 'GF'),
            (16, 'White', 'Glutenberg', 'Montreal', 'Quebec', 'Canada', 'Global', 'GF'),
            (17, 'Stout', 'Glutenberg', 'Montreal', 'Quebec', 'Canada', 'Global', 'GF'),
            (18, 'Session IPA', 'Glutenberg', 'Montreal', 'Quebec', 'Canada', 'Global', 'GF'),
            (19, 'Lager Beer', 'Daura Damm', 'Barcelona', 'Catalonia', 'Spain', 'Global', 'GR'),
            (20, 'IPA', 'Daura Damm', 'Barcelona', 'Catalonia', 'Spain', 'Global', 'GR'),
            (21, 'Delicious IPA', 'Stone Brewing', 'Escondido', 'California', 'United States', 'National', 'GR'),
            (22, 'Hop Cloud', 'Mike Hess', 'San Diego', 'California', 'United States', 'Local', 'GR'),
            (23, 'Grapefruit Solis', 'Mike Hess', 'San Diego', 'California', 'United States', 'Local', 'GR'),
            (24, 'Into the Sunset', 'Mike Hess', 'San Diego', 'California', 'United States', 'Local', 'GR'),
            (25, 'Steel Beach', 'Mike Hess', 'San Diego', 'California', 'United States', 'Local', 'GR'),
            (26, 'Solis', 'Mike Hess', 'San Diego', 'California', 'United States', 'Local', 'GR'),
            (27, 'Mandatory Fun', 'Mike Hess', 'San Diego', 'California', 'United States', 'Local', 'GR'),
            (28, 'Claritas', 'Mike Hess', 'San Diego', 'California', 'United States', 'Local', 'GR'),
            (29, 'Grazias', 'Mike Hess', 'San Diego', 'California', 'United States', 'Local', 'GR');
    END IF;
END$$;

CREATE TABLE IF NOT EXISTS encounters (
    id INTEGER,
    date_of DATE NOT NULL,
    location POINT NOT NULL,
    address TEXT,
    content TEXT NOT NULL
);

DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM encounters) THEN
        INSERT INTO encounters (
            id, date_of, location, address, content
            )
        VALUES (
            2, '2023-11-25', '(26.571146, -80.0887830)',
            '4770 N Congress Ave, Boynton Beach, FL 33426, United States',
            'I found a 6-pack of Copperpoint Lager in the beer cooler at Publix'
            );
    END IF;
END$$;

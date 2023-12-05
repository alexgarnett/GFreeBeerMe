import psycopg2


def run():
    conn = psycopg2.connect("dbname='beer_app' user='postgres' password='password'")

    cursor = conn.cursor()
    cursor.execute(open("schema.sql", "r").read())

    # Moved the following lines into schema.sql
    # cursor.execute("INSERT INTO information (id, name, manufacturer, city, state, country, availability, gf_or_gr) "
    #                "VALUES (1, 'Redbridge', 'Anheuser-Busch', 'St. Louis', 'Missouri', 'United States', 'National', 'GF')")

    conn.commit()
    conn.close()


if __name__ == "__main__":
    run()

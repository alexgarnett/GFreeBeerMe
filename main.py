import psycopg2

def main():
    # Connect to your postgres DB
    conn = psycopg2.connect("dbname='beer_app' user='postgres' password='password'")

    # Open a cursor to perform database operations
    cur = conn.cursor()

    # Execute a query
    cur.execute("SELECT * FROM information")

    # Retrieve query results
    records = cur.fetchall()

    print(records)

if __name__ == '__main__':
    main()


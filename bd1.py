import psycopg2


def creat_table(conn):
    with conn.cursor() as cur:
        cur.execute("""
        DROP TABLE client_phone;
        DROP TABLE client_data;
        """)

        cur.exicute("""
                CREATE TABLE IF NOT EXISTS client_data(
                    client_id SERIAL PRIMARY KEY,
                    first_name VARCHAR(40) NOT NULL,
                    last_name VARCHAR(60) NOT NULL,
                    email VARCHAR(80) UNIQUE NOT NULL
                    );
                    """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS client_phone(
                    id SERIAL PRIMARY KEY,
                    client_id INTEGER REFERENCES client_data(client_id),
                    phone VARCHAR(12) 
                    );
                    """)


def add_client(conn, first_name, last_name, email, phones=None):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO client_data (first_name, last_name, email)
            VALUES (%s,%s,%s,%s)
            RETURNING client_id, first_name, last_name, email;
            """, (first_name, last_name, email))
    return cur.fetchone()


if __name__ == '__main__':
    with psycopg2.connect(database='data_base', user='postgres', password='postgres') as conn:
        print(add_client(conn, 'Tanya', 'Ivanova', 'tanya@mail.ru'))

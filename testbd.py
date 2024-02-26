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
            VALUES (%s,%s,%s)
            RETURNING client_id, first_name, last_name, email;
            """, (first_name, last_name, email))
    return cur.fetchone()
    
    
def add_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO client_phone(client_id, phone)
            VALUES(%s, %s)
            RETURNING client_id, phone;
            """, (client_id, phone))
        return cur.fetchone()
        

def delete_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        cur.execute("""
            DELETE FROM client_phone
            WHERE client_id = %s
            RETURNING client_id;
            """,(client_id,))
    return cur.fetchone()

def delete_client(conn, client_id):
    with conn.cursor() as cur:
        cur.execute("""
        DELETE FROM client_data
        WHERE client_id = %s
        RETURNING client_id;
            """,(client_id,))
    return cur.fetchone()

def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
    with conn.cursor() as cur:
        cur.execute("""
        SELECT * FROM client_data cd
        JOIN client_phone cp ON cd.client_id = cp.client_id
        WHERE (first_name = %(first_name)s OR %(first_name)s IS NULL)
            AND (last_name = %(last_name)s OR %(last_name)s IS NULL)
            AND (email = %(email)s OR %(email)s IS NULL)
            OR (phone = %(phone)s OR %(phone)s IS NULL);
            """, {'first_name': first_name, 'last_name': last_name, 'email': email, 'phone': phone})
        return cur.fetchone()
                    
wiht psycopg2.connect(database = 'clients', user = 'postgres', password = '544202') as conn:
    print(add_client(conn, 'Tanya', 'Spicyna', 'tanya@mail.ru'))
    print(add_phone(conn, '1', '89998887766'))
    print(delete_phone(conn, '1', '89998887766'))
    print(delete_client(conn, 1))
    print(find_client(conn, 'Tanya'))
    create_table(conn)

conn.close()

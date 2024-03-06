import psycopg2
def create_table(conn):
    with conn.cursor() as cur:
        cur.execute("""
        DROP TABLE client_phone;
        DROP TABLE clients;
        """)

        cur.execute("""
        create table IF NOT EXISTS clients(
            client_id SERIAL PRIMARY KEY,
            first_name VARCHAR(40) NOT NULL,
            last_name VARCHAR(60) NOT NULL,
            email VARCHAR(80) UNIQUE NOT NULL
        );
        """)
        

        cur.execute("""
        CREATE TABLE IF NOT EXISTS client_phone(
        id SERIAL PRIMARY KEY,
        client_id INTEGER REFERENCES clients(client_id),
        phone VARCHAR(12) 
        );
        """)
        

def add_client(cur, first_name, last_name, email, phones=None):
        cur.execute("""INSERT INTO clients(first_name, last_name, email) VALUES(%s, %s, %s);"""
        , (first_name, last_name, email))

if __name__ == "__main__":          
    with psycopg2.connect(database="clients_db", user="postgres", password="postgres") as conn:
        with conn.cursor() as cur:  
            create_table(conn)
            print(add_client(cur, 'Tanya', 'Ivanova', 'tanya@mail.ru'))


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

def delete_client(conn, client_id, phone):
    with conn.cursor() as cur:
        cur.execute("""
        SELECT * FROM clients c
        JOIN client_phone cp ON c.client_id = cp.client_id
        DELETE FROM clients
        WHERE client_id = %s
        RETURNING client_id;
            """,(client_id,))
    return cur.fetchone()

def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
    with conn.cursor() as cur:
        cur.execute("""
        SELECT * FROM clients c
        JOIN client_phone cp ON c.client_id = cp.client_id
        WHERE (first_name = %(first_name)s OR %(first_name)s IS NULL)
            AND (last_name = %(last_name)s OR %(last_name)s IS NULL)
            AND (email = %(email)s OR %(email)s IS NULL)
            OR (phone = %(phone)s OR %(phone)s IS NULL);
            """, {'first_name': first_name, 'last_name': last_name, 'email': email, 'phone': phone})
        return cur.fetchone()

def change_client(conn, client_id, first_name=None, last_name=None, email=None):
    arg_list = {'first_name': first_name, "last_name": last_name, 'email': email}
    for key, arg in arg_list.items():
        if arg:
            conn.execute(SQL("UPDATE clients SET {}=%s WHERE client_id=%s").format(Identifier(key)), (arg, client_id))
    conn.execute("""
            SELECT * FROM clients
            WHERE client_id=%s
            """, client_id)
    return cur.fetchall()
                    
with psycopg2.connect(database = 'clients_db', user = 'postgres', password = 'postgres') as conn:
    print(add_client(conn, 'Tanya', 'Ivanova', 'tanya@mail.ru'))
    print(add_phone(conn, '1', '89998887766'))
    print(delete_phone(conn, '1', '89998887766'))
    print(delete_client(conn, '1'))
    print(find_client(conn, 'Tanya'))
    print(change_client(conn, '1', 'Tanya', 'Ivanova', 'tanya@mail.ru'))
   

conn.close()
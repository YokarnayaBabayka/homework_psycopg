import psycopg2


def create_db(conn):
    with conn.cursor() as cur:
        cur.execute(
            """
                    CREATE TABLE IF NOT EXISTS client(
                    id SERIAL PRIMARY KEY,
                    first_name VARCHAR(40) NOT NULL,
                    last_name VARCHAR(40) NOT NULL,
                    email VARCHAR(60) UNIQUE NOT NULL CHECK (email LIKE '%@%.%'),
                    phones VARCHAR(100) NULL
                    );
                    """
        )
        conn.commit()
    print("Table created")


def add_client(conn, first_name, last_name, email, phones=None):
    with conn.cursor() as cur:
        cur.execute(
            """
                INSERT INTO client(first_name, last_name, email, phones) 
                VALUES(%s, %s, %s, %s);
                """,
            (first_name, last_name, email, phones),
        )
        conn.commit()
    print("Client added")


def add_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        cur.execute(
            """
                UPDATE client SET phones=concat(phones, ' ', %s) 
                WHERE id=%s;
                """,
            (phone, client_id),
        )
        conn.commit()
    print("Phone number added")


def change_client(
    conn, client_id, first_name=None, last_name=None, email=None, phones=None
):
    if first_name != None:
        with conn.cursor() as cur:
            cur.execute(
                """
                    UPDATE client SET first_name=%s WHERE id=%s;
                    """,
                (first_name, client_id),
            )
        conn.commit()
    if last_name != None:
        with conn.cursor() as cur:
            cur.execute(
                """
                    UPDATE client SET last_name=%s WHERE id=%s;
                    """,
                (last_name, client_id),
            )
        conn.commit()
    if email != None:
        with conn.cursor() as cur:
            cur.execute(
                """
                    UPDATE client SET email=%s WHERE id=%s;
                    """,
                (email, client_id),
            )
        conn.commit()
    if phones != None:
        with conn.cursor() as cur:
            cur.execute(
                """
                    UPDATE client SET phones=%s WHERE id=%s;
                    """,
                (phones, client_id),
            )
        conn.commit()
    print("Client changed")


def delete_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        cur.execute(
            """
                SELECT phones FROM client WHERE id=%s;
                """,
            (client_id),
        )
        phone_num = cur.fetchone()[0]
        phone_num_list = phone_num.split()
        phone_num_list.remove(phone)
        cur.execute(
            """
                UPDATE client SET phones=%s WHERE id=%s;
                """,
            (" ".join(phone_num_list), client_id),
        )
        conn.commit()
    print("Phone number deleted")


def delete_client(conn, client_id):
    with conn.cursor() as cur:
        cur.execute(
            """
                DELETE FROM client WHERE id=%s;
                """,
            (client_id),
        )
        conn.commit()
    print("Client deleted")


def find_client(conn, first_name=None, last_name=None, email=None, phones=None):
    if first_name != None:
        with conn.cursor() as cur:
            cur.execute(
                """
                    SELECT * FROM client WHERE first_name=%s;
                    """,
                (first_name,),
            )
            return cur.fetchall()
    if last_name != None:
        with conn.cursor() as cur:
            cur.execute(
                """
                    SELECT * FROM client WHERE last_name=%s;
                    """,
                (last_name,),
            )
            return cur.fetchall()
    if email != None:
        with conn.cursor() as cur:
            cur.execute(
                """
                    SELECT * FROM client WHERE email=%s;
                    """,
                (email,),
            )
            return cur.fetchall()
    if phones != None:
        with conn.cursor() as cur:
            cur.execute(
                """
                    SELECT * FROM client WHERE phones=%s;
                    """,
                (phones,),
            )
            return cur.fetchall()


# ------------------------------------------------------------------

with psycopg2.connect(database="clients_db", user="postgres", password="postgres") as conn:
    with conn.cursor() as cur:
        cur.execute("""DROP TABLE client;""")

    create_db(conn)  # вызывайте функции здесь

    add_client(conn, "Tucker", "Karlson", "Tucker@gmail.com", "+1-123-123-1234")

    add_client(conn, "Volodya", "Putin", "whoismrpu@mail.ru", "+7-111-111-1111")

    add_client(conn, "Karl", "Karlson", "life-on-roof@roof.com", "+46-123-111-1111")

    add_phone(conn, "1", "+7-000-000-0001")

    change_client(conn, "2", first_name="Vladimir")

    delete_phone(conn, "1", "+7-000-000-0001")

    delete_client(conn, "1")

    finded_client = find_client(conn, last_name="Karlson")
    print(finded_client)

conn.close()

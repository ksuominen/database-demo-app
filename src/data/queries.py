from config import config
import psycopg2
from psycopg2 import sql


def connect():
    con = None
    try:
        con = psycopg2.connect(**config())
        return con
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def query_data(query, how):
    con = connect()
    if con is not None:
        cursor = con.cursor()
        cursor.execute(query)
        if how == "one":
            row = cursor.fetchone()
        elif how == "all":
            row = cursor.fetchall()
        cursor.close()
        con.close()
        return row


def all_rows_from_table(table):
    query = sql.SQL("SELECT * FROM {table}").format(table=sql.Identifier(table))
    row = query_data(query, "all")
    for r in row:
        print(r)


def column_names_from_table(table):
    query = sql.SQL("SELECT * FROM {table}").format(table=sql.Identifier(table))
    con = connect()
    if con is not None:
        cursor = con.cursor()
        cursor.execute(query)
        col_names = [desc[0] for desc in cursor.description]
        for c in col_names:
            print(c)
        cursor.close()
        con.close()


def rows_and_column_names_from_table(table):
    print(f"Column names of table {table}")
    column_names_from_table(table)
    print(f"Rows of table {table}")
    all_rows_from_table(table)


def get_average_age_from_person():
    query = """SELECT AVG(age) from person"""
    averag_age = round(query_data(query, "one")[0], 2)
    print(f"The average age of persons is {averag_age}")


def get_certificate_holders(certificate):
    query = sql.SQL(
        "SELECT person.name FROM certificates INNER JOIN person ON certificates.person_id = person.id WHERE certificates.name = %s"
    )
    con = connect()
    if con is not None:
        cursor = con.cursor()
        cursor.execute(query, (certificate,))
        row = cursor.fetchall()
        for r in row:
            print(r[0])
        cursor.close()
        con.close()


def add_certificate(name, certificate):
    query = sql.SQL(
        "INSERT INTO certificates (name, person_id) VALUES (%(certificate)s, (SELECT id FROM person WHERE person.name=%(name)s))"
    )
    con = connect()
    if con is not None:
        cursor = con.cursor()
        cursor.execute(query, {"certificate": certificate, "name": name})
        con.commit()
        cursor.close()
        con.close()


def add_person(name, age, student):
    query = sql.SQL(
        "INSERT INTO person (name, age, student) VALUES (%(name)s, %(age)s, %(student)s)"
    )
    con = connect()
    if con is not None:
        cursor = con.cursor()
        cursor.execute(query, {"name": name, "age": age, "student": student})
        con.commit()
        cursor.close()
        con.close()


def update_person(name, age, student):
    query = sql.SQL(
        "UPDATE person SET age = %(age)s, student = %(student)s WHERE name = %(name)s"
    )
    con = connect()
    if con is not None:
        cursor = con.cursor()
        cursor.execute(query, {"name": name, "age": age, "student": student})
        con.commit()
        cursor.close()
        con.close()


def update_certificates(id, certificate, person_id):
    query = sql.SQL(
        "UPDATE certificates SET name = %(certificate)s, person_id = %(person_id)s WHERE id = %(id)s"
    )
    con = connect()
    if con is not None:
        cursor = con.cursor()
        cursor.execute(
            query, {"certificate": certificate, "person_id": person_id, "id": id}
        )
        con.commit()
        cursor.close()
        con.close()


def delete_person(id):
    query1 = sql.SQL("DELETE FROM certificates WHERE person_id = %(person_id)s")
    query2 = sql.SQL("DELETE FROM person WHERE id = %(id)s")
    con = connect()
    if con is not None:
        cursor = con.cursor()
        cursor.execute(query1, {"person_id": id})
        con.commit()
        cursor.execute(query2, {"id": id})
        con.commit()
        cursor.close()
        con.close()


def delete_certificate(id):
    query = sql.SQL("DELETE FROM certificates WHERE id = %(id)s")
    con = connect()
    if con is not None:
        cursor = con.cursor()
        cursor.execute(query, {"id": id})
        con.commit()
        cursor.close()
        con.close()


def create_table(tablename):
    query = sql.SQL(
        "CREATE TABLE {tablename} (id SERIAL PRIMARY KEY, name varchar(255))"
    ).format(tablename=sql.Identifier(tablename))
    con = connect()
    if con is not None:
        cursor = con.cursor()
        cursor.execute(query)
        con.commit()
        cursor.close()
        con.close()

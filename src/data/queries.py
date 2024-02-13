from config import config
import psycopg2


def connect():
    con = None
    try:
        con = psycopg2.connect(**config())
        print("Connected to the PostgreSQL server.")
        return con
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def query_data(sql, how):
    con = connect()
    if con is not None:
        cursor = con.cursor()
        cursor.execute(sql)
        if how == "one":
            row = cursor.fetchone()
        elif how == "all":
            row = cursor.fetchall()
        cursor.close()
        con.close()
        return row


def all_rows_from_person():
    sql = """SELECT * FROM person;"""
    row = query_data(sql, "all")
    for r in row:
        print(r)


def column_names_from_person():
    sql = """SELECT * FROM person;"""
    con = connect()
    if con is not None:
        cursor = con.cursor()
        cursor.execute(sql)
        col_names = [desc[0] for desc in cursor.description]
        for c in col_names:
            print(c)
        cursor.close()
        con.close()

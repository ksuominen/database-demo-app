from config import config
import psycopg2
from psycopg2 import sql


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


column_names_from_table("person")

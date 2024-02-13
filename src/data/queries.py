from config import config
import psycopg2


def connect(sql):
    con = None
    try:
        con = psycopg2.connect(**config())
        cursor = con.cursor()
        SQL = sql
        cursor.execute(SQL)
        row = cursor.fetchone()
        print(row)
        cursor.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if con is not None:
            con.close()

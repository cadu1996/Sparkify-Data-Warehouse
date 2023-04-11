import configparser

import psycopg2

from sql_queries import copy_table_queries, insert_table_queries


def load_staging_tables(cur, conn):
    """
    Loads staging tables with data using the queries in 'copy_table_queries'.

    Args:
        cur (psycopg2.cursor): A psycopg2 cursor to execute database commands.
        conn (psycopg2.connection): A psycopg2 connection to the database.
    """

    for query in copy_table_queries:
        cur.execute(query)
        conn.commit()


def insert_tables(cur, conn):
    """
    Inserts data into the target tables using the queries in 'insert_table_queries'.

    Args:
        cur (psycopg2.cursor): A psycopg2 cursor to execute database commands.
        conn (psycopg2.connection): A psycopg2 connection to the database.
    """

    for query in insert_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """
    Main function to connect to the database, load staging tables, and insert data into target tables.
    """

    config = configparser.ConfigParser()
    config.read("dwh.cfg")

    conn = psycopg2.connect(
        "host={} dbname={} user={} password={} port={}".format(
            *config["CLUSTER"].values()
        )
    )
    cur = conn.cursor()

    load_staging_tables(cur, conn)
    insert_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()

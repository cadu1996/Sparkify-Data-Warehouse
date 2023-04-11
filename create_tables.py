import configparser

import psycopg2

from sql_queries import create_table_queries, drop_table_queries


def drop_tables(cur, conn):
    """
    Drops the tables defined in 'drop_table_queries'.

    Args:
        cur (psycopg2.cursor): A psycopg2 cursor to execute database commands.
        conn (psycopg2.connection): A psycopg2 connection to the database.
    """

    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    """
    Creates the tables defined in 'create_table_queries'.

    Args:
        cur (psycopg2.cursor): A psycopg2 cursor to execute database commands.
        conn (psycopg2.connection): A psycopg2 connection to the database.
    """

    for query in create_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """
    Main function to connect to the database, drop existing tables, and create new ones.
    """

    config = configparser.ConfigParser()
    config.read("dwh.cfg")

    conn = psycopg2.connect(
        "host={} dbname={} user={} password={} port={}".format(
            *config["CLUSTER"].values()
        )
    )
    cur = conn.cursor()

    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()

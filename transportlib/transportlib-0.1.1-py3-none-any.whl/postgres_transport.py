import logging
from typing import Optional, List, Tuple
from pathlib import Path
from psycopg2._psycopg import connection, cursor



def truncate_table(conn: connection,
                   cur: cursor,
                   table_name: str,
                   ):
    logging.info(f"Now truncating {table_name}...")
    truncate_table_sql = f"""
    TRUNCATE {table_name}
    """
    cur.execute(truncate_table_sql)
    conn.commit()


def load_csv_file_to_staging(
        conn,
        cur,
        csv_file_path: Path,
        table_name: str,
):
    logging.info(f"Now loading file {csv_file_path} to staging")
    load_to_staging_sql = f"""
    -- COPY all data from csv into staging table

    COPY {table_name} FROM stdin with CSV HEADER DELIMITER as ',' QUOTE as '"' ;

    """
    logging.info("COPY JOB")
    logging.info(load_to_staging_sql)

    with open(csv_file_path, 'r') as read_file:
        cur.copy_expert(sql=load_to_staging_sql, file=read_file)
        conn.commit()


def load_from_staging_to_l0(
        conn,
        cur,
        sql: str,
        args: Optional[Tuple],

):
    logging.info(f"Now loading data from staging to l0 with the below SQL:")
    logging.info(sql)

    if args is None:
        cur.execute(query=sql)
    else:
        cur.execute(sql, args)

    # Print notice
    notices = conn.notices
    if type(notices) == list:
        for notice in conn.notices:
            logging.info(notice)
    else:
        logging.info("No notice is printed")

    conn.commit()

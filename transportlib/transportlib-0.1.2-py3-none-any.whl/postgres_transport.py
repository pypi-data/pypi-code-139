import logging
from typing import Optional, List, Tuple
from pathlib import Path
from psycopg2._psycopg import connection, cursor
import traceback


class PostgresTransport():
    """
    Truncate Staging Table
    Load CSV to Staging Table.
    Run Custom SQL which loads from Staging to L0 Table(s).
    """

    def __init__(self,
                 conn: connection,
                 staging_table_name: str,
                 csv_file_path:Path,
                 staging_to_l0_sql: str,
                 staging_to_l0_args: Optional[Tuple],
                 ):
        self.conn = conn
        self.cur = self.conn.cursor()
        self.staging_table_name = staging_table_name
        self.csv_file_path = csv_file_path
        self.staging_to_l0_sql = staging_to_l0_sql
        self.staging_l0_args = staging_to_l0_args


    def run(self):
        # Truncate table
        self.truncate_staging_table()

        # Bulk load data to staging
        try:
            self.load_csv_file_to_staging()

        except Exception as e:
            logging.error("Something went wrong with loading csv data to staging!!!")
            logging.error(traceback.format_exc())
            return False

        # LOad from staging to l0
        try:
            self.load_from_staging_to_l0()
            self.cur.close()
        except Exception as e:
            logging.error("Something went wrong with loading from staging to l0!!!")
            logging.error(traceback.format_exc())
            return False
        finally:
            logging.info("Closing connection....")
            if self.conn is not None:
                self.conn.close()

    def truncate_staging_table(self):
        logging.info(f"Now truncating {self.staging_table_name}...")
        truncate_table_sql = f"""
        TRUNCATE {self.staging_table_name}
        """
        self.cur.execute(truncate_table_sql)
        self.conn.commit()

    def load_csv_file_to_staging(
            self,
    ):
        logging.info(f"Now loading file {self.csv_file_path} to staging")
        load_to_staging_sql = f"""
        -- COPY all data from csv into staging table
        
        COPY {self.staging_table_name} FROM stdin with CSV HEADER DELIMITER as ',' QUOTE as '"' ;
        """
        logging.info("COPY JOB")
        logging.info(load_to_staging_sql)

        with open(self.csv_file_path, 'r') as read_file:
            self.cur.copy_expert(sql=load_to_staging_sql, file=read_file)
            self.conn.commit()

    def load_from_staging_to_l0(
            self,
    ):
        logging.info(f"Now loading data from staging to l0 with the below SQL:")
        logging.info(self.staging_to_l0_sql)

        if self.staging_l0_args is None:
            self.cur.execute(query=self.staging_to_l0_sql)
        else:
            self.cur.execute(self.staging_to_l0_sql, self.staging_l0_args)

        # Print notice
        notices = self.conn.notices
        if type(notices) == list:
            for notice in self.conn.notices:
                logging.info(notice)
        else:
            logging.info("No notice is printed")

        self.conn.commit()

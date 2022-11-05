"""
Module for handling files, directories and databases
"""

import contextlib
import os
import sqlite3


@contextlib.contextmanager
def working_directory(path):
    """Change the working directory during process by context manager

    Parameters
    ----------
    path : str: Path for target directory
        

    Returns
    -------
    None
    """
    cwd = os.getcwd()
    os.chdir(path)
    yield None
    os.chdir(cwd)


@contextlib.contextmanager
def sqlite_database(path):
    """Connect to sqlite database from path and disconnect after operation using context manager

    Parameters
    ----------
    path : Path to sqlite database file
        

    Yields
    -------
    conn: sqlite.Connection : Connection object for db operations
    """
    conn = None
    try:
        conn = sqlite3.connect(path)
        yield conn
    finally:
        conn.close()
        print('DB Disconnected')


# if __name__ == '__main__':
    # print(f'Before {os.listdir()}')
    # with working_directory('../'):
    #     print(f'During {os.listdir()}')
    # print(f'After {os.listdir()}')

    # with sqlite_database('trackerdb.db') as conn:
    #     sql = f"SELECT * FROM kpi_data"
    #     cursor = conn.cursor()
    #     cursor.execute(sql)
    #     try:
    #         obj = cursor.fetchall()
    #         print(obj)
    #     except sqlite3.Error as err:
    #         print('Error:', err)

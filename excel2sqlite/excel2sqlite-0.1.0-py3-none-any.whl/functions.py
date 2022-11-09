import pandas
import openpyxl
import pathlib
import sqlite3

def excel2sqlite(excel_filename:pathlib.Path, sqlite_filename:pathlib.Path):
    wb = openpyxl.load_workbook(excel_filename)
    sheet_names = wb.sheetnames
    wb.close()

    connection = sqlite3.connect(sqlite_filename)

    for sheet_name in sheet_names:
        data = pandas.read_excel(excel_filename,sheet_name=sheet_name)
        if len(data) > 0:
            data.to_sql(sheet_name,connection,index=False,if_exists='replace')
    
    connection.commit()
    connection.close()



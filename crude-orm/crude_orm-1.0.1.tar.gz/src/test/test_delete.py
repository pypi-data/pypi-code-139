"""Test delete operations."""

import os
import sqlite3
import unittest

from crude import connect, MissingResource

class TestRead(unittest.TestCase):
    
    def setUp(self):
        
        # Create a test database:
        with open("./src/test/crude_test_db.sql") as fp:
            sql_script = fp.read()
        connection = sqlite3.connect("./test_data/crude_test_sample.db")
        cursor = connection.cursor()
        cursor.executescript(sql_script)
        connection.commit()
        connection.close()
        builder = connect("./test_data/crude_test_sample.db")
        self.TesttextTable = builder.build_table_class("testtext")
        self.TestrealTable = builder.build_table_class("testreal")
        self.TestintTable = builder.build_table_class("testint")
        self.TestblobTable = builder.build_table_class("testblob")
        
    def test_delete_int_record(self):
        self.TestintTable.delete(intPrimaryKey=1)
        raised = False
        try:
            self.TestintTable.load(intPrimaryKey=1)
        except MissingResource as err:
            raised = True
        self.assertTrue(raised)
        
    def test_delete_text_record(self):
        self.TesttextTable.delete(textPrimaryKey="KEY")
        try:
            self.TesttextTable.load(textPrimaryKey="KEY")
        except MissingResource as err:
            raised = True
        self.assertTrue(raised)
        
    def test_delete_real_record(self):
        self.TestrealTable.delete(realPrimaryKey=1.0)
        try:
            self.TestrealTable.load(realPrimaryKey=1.0)
        except MissingResource as err:
            raised = True
        self.assertTrue(raised)
        
    def test_delete_blob_record(self):
        self.TestblobTable.delete(blobPrimaryKey=bytes([0xbe, 0xef]))
        try:
            self.TestblobTable.load(blobPrimaryKey=bytes([0xbe, 0xef]))
        except MissingResource as err:
            raised = True
        self.assertTrue(raised)
        
    def tearDown(self) -> None:
        os.remove("./test_data/crude_test_sample.db")
    
if __name__ == "__main__":
    unittest.main()
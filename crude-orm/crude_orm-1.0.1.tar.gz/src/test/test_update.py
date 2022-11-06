"""Test update operations."""

import os
import sqlite3
import unittest

from crude import connect

class TestUpdate(unittest.TestCase):
    
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
        TesttextTable = builder.build_table_class("testtext")
        TestrealTable = builder.build_table_class("testreal")
        TestintTable = builder.build_table_class("testint")
        TestblobTable = builder.build_table_class("testblob")
        self.test_record_int = TestintTable.load(intPrimaryKey=1)
        self.test_record_text = TesttextTable.load(textPrimaryKey="KEY")
        self.test_record_real = TestrealTable.load(realPrimaryKey=1.0)
        self.test_record_blob = TestblobTable.load(
            blobPrimaryKey=bytes([0xbe, 0xef]))
        
    def test_update_int_field(self):
        self.test_record_int.intNonNull = -80
        expected = -80
        real = self.test_record_int.intNonNull
        self.assertEqual(expected, real)
        
    def test_update_text_field(self):
        self.test_record_text.textNonNull = "TEST"
        expected = "TEST"
        real = self.test_record_text.textNonNull
        self.assertEqual(expected, real)
        
    def test_update_real_field(self):
        self.test_record_real.realNonNull = 182.25
        expected = 182.25
        real = self.test_record_real.realNonNull
        self.assertEqual(expected, real)
        
    def test_update_blob_field(self):
        self.test_record_blob.blobNonNull = bytes([0x5f, 0x2b, 0xaa, 0xf2])
        expected = bytes([0x5f, 0x2b, 0xaa, 0xf2])
        real = self.test_record_blob.blobNonNull
        self.assertEqual(expected, real)
        
    def tearDown(self) -> None:
        os.remove("./test_data/crude_test_sample.db")
        
if __name__ == "__main__":
    unittest.main()
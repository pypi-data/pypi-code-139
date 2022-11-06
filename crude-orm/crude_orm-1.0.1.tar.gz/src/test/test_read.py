"""Test read operations."""

import os
import sqlite3
import unittest

from crude import connect

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
        TesttextTable = builder.build_table_class("testtext")
        TestrealTable = builder.build_table_class("testreal")
        TestintTable = builder.build_table_class("testint")
        TestblobTable = builder.build_table_class("testblob")
        self.test_record_int = TestintTable.load(intPrimaryKey=1)
        self.test_record_text = TesttextTable.load(textPrimaryKey="KEY")
        self.test_record_real = TestrealTable.load(realPrimaryKey=1.0)
        self.test_record_blob = TestblobTable.load(
            blobPrimaryKey=bytes([0xbe, 0xef]))

    def test_read_text_primary_key(self):
        expected = "KEY"
        real = self.test_record_text.textPrimaryKey
        self.assertEqual(expected, real)

    def test_read_text_non_null(self):
        expected = "HELLO"
        real = self.test_record_text.textNonNull
        self.assertEqual(expected, real)

    def test_read_text_null(self):
        expected = None
        real = self.test_record_text.textNull
        self.assertEqual(expected, real)

    def test_read_text_unique(self):
        expected = "WORLD"
        real = self.test_record_text.textUnique
        self.assertEqual(expected, real)

    def test_read_real_primary_key(self):
        expected = 1.0
        real = self.test_record_real.realPrimaryKey
        self.assertEqual(expected, real)
    
    def test_read_real_non_null(self):
        expected = 1.5
        real = self.test_record_real.realNonNull
        self.assertEqual(expected, real)

    def test_read_real_null(self):
        expected = None
        real = self.test_record_real.realNull
        self.assertEqual(expected, real)

    def test_read_real_unique(self):
        expected = -5.0
        real = self.test_record_real.realUnique
        self.assertEqual(expected, real)
        
    def test_read_int_primary_key(self):
        expected = 1
        real = self.test_record_int.intPrimaryKey
        self.assertEqual(expected, real)

    def test_read_int_non_null(self):
        expected = 100
        real = self.test_record_int.intNonNull
        self.assertEqual(expected, real)

    def test_read_int_null(self):
        expected = None
        real = self.test_record_int.intNull
        self.assertEqual(expected, real)

    def test_real_int_unique(self):
        expected = 1000
        real = self.test_record_int.intUnique
        self.assertEqual(expected, real)
        
    def test_read_blob_primary_key(self):
        expected = bytes([0xbe, 0xef])
        real = self.test_record_blob.blobPrimaryKey
        self.assertEqual(expected, real)
        
    def test_read_blob_non_null(self):
        expected = bytes([0xfe, 0xed])
        real = self.test_record_blob.blobNonNull
        self.assertEqual(expected, real)
        
    def test_read_blob_null(self):
        expected = None
        real = self.test_record_blob.blobNull
        self.assertEqual(expected, real)
        
    def test_read_blob_unique(self):
        expected = bytes([0xde, 0xaf])
        real = self.test_record_blob.blobUnique
        self.assertEqual(expected, real)

    def tearDown(self) -> None:
        os.remove("./test_data/crude_test_sample.db")

if __name__ == "__main__":
    unittest.main()
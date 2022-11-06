"""Test create operations."""

import os
import sqlite3
import unittest

from crude import connect

class TestCreate(unittest.TestCase):
    
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
        self.TestintTable = builder.build_table_class("testint")
        self.TestrealTable = builder.build_table_class("testreal")
        self.TestblobTable = builder.build_table_class("testblob")
        
    def test_create_text_data(self):
        
        record = self.TesttextTable.create(
            textPrimaryKey="RECORD_1",
            textNonNull="FOO",
            textNull=None,
            textUnique="BAR")
        self.assertEqual(record.textPrimaryKey, "RECORD_1")
        self.assertEqual(record.textNonNull, "FOO")
        self.assertEqual(record.textNull, None)
        self.assertEqual(record.textUnique, "BAR")
        
    def test_create_int_data(self):
        
        record = self.TestintTable.create(
            intPrimaryKey=2,
            intNonNull=3,
            intNull=None,
            intUnique=4)
        self.assertEqual(record.intPrimaryKey, 2)
        self.assertEqual(record.intNonNull, 3)
        self.assertEqual(record.intNull, None)
        self.assertEqual(record.intUnique, 4)
        
    def test_create_real_data(self):
        
        record = self.TestrealTable.create(
            realPrimaryKey=10.25,
            realNonNull=-50.75,
            realNull=None,
            realUnique=0.333333333)
        self.assertEqual(record.realPrimaryKey, 10.25)
        self.assertEqual(record.realNonNull, -50.75)
        self.assertEqual(record.realNull, None)
        self.assertEqual(record.realUnique, 0.333333333)
        
    def test_create_blob_data(self):
        
        record = self.TestblobTable.create(
            blobPrimaryKey=bytes([0xab, 0xcd, 0xef]),
            blobNonNull=bytes([0xfe, 0xdc, 0xba]),
            blobNull=None,
            blobUnique=bytes([0x00, 0x00, 0x00]))
        self.assertEqual(record.blobPrimaryKey, bytes([0xab, 0xcd, 0xef]))
        self.assertEqual(record.blobNonNull,bytes([0xfe, 0xdc, 0xba]))
        self.assertEqual(record.blobNull, None)
        self.assertEqual(record.blobUnique, bytes([0x00, 0x00, 0x00]))
        
        
    def tearDown(self):
        os.remove("./test_data/crude_test_sample.db")

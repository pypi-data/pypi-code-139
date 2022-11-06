import unittest

from mathcube import Table


class TestTable(unittest.TestCase):

    def test_insert_column(self):

        data = [[1, 2, 3, 4]]
        t = Table(data)

        self.assertEqual((1, 4), t.shape)

        t.insert_column(1)
        self.assertEqual('', t[0, 1])

        self.assertEqual((1, 5), t.shape)

        with self.assertRaises(ValueError):
            t.insert_column(-1)

        t.insert_column()
        self.assertEqual((1, 6), t.shape)
        self.assertEqual('', t[0, 5])

    def test_insert_row(self):

        data = [[1, 2, 3, 4]]
        t = Table(data)

        t.insert_row(0)
        self.assertEqual('', t[0, 1])

        self.assertEqual((2, 4), t.shape)

        with self.assertRaises(ValueError):
            t.insert_row(-1)

        t.insert_row()
        self.assertEqual((3, 4), t.shape)
        self.assertEqual('', t[2, 1])


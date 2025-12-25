import unittest

from generate import extract_title

class TestGenerate(unittest.TestCase):
    def test_extract(self):
        self.assertEqual(extract_title("# Hello"),"Hello")
    def test_extract_not_a_title(self):
        with self.assertRaises(Exception):
            test = extract_title("Hello")

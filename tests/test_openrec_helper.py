import unittest

from openrec_helper import OpenrecHelper


class TestOpenrecHelper(unittest.TestCase):

    def test_separate_integer_and_string_empty_string(self):
        actual_int, actual_str = OpenrecHelper.separate_integer_and_string("")
        self.assertEqual(None, actual_int)
        self.assertEqual("", actual_str)

    def test_separate_integer_and_string_json_string(self):
        actual_int, actual_str = OpenrecHelper.separate_integer_and_string('0{"sid":"ICcoGjtvVnI28E82ABb6","upgrades":[],"pingInterval":25000,"pingTimeout":60000}')
        self.assertEqual(0, actual_int)
        self.assertEqual('{"sid":"ICcoGjtvVnI28E82ABb6","upgrades":[],"pingInterval":25000,"pingTimeout":60000}', actual_str)

    def test_separate_integer_and_string_integer_only(self):
        actual_int, actual_str = OpenrecHelper.separate_integer_and_string("40")
        self.assertEqual(40, actual_int)
        self.assertEqual("", actual_str)

    def test_separate_integer_and_string_message_string(self):
        actual_int, actual_str = OpenrecHelper.separate_integer_and_string('42["message","{"type":1,"room":"3208306","data":{"movie_id":3208306,"viewers":2005,"live_viewers":558}}"]')
        self.assertEqual(42, actual_int)
        self.assertEqual('["message","{"type":1,"room":"3208306","data":{"movie_id":3208306,"viewers":2005,"live_viewers":558}}"]', actual_str)

    def test_separate_integer_and_string_non_numeric_start(self):
        actual_int, actual_str = OpenrecHelper.separate_integer_and_string('abc{"sid":"ICcoGjtvVnI28E82ABb6","upgrades":[],"pingInterval":25000,"pingTimeout":60000}')
        self.assertEqual(None, actual_int)
        self.assertEqual("", actual_str)

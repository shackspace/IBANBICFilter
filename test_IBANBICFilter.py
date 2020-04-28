#!/usr/bin/python3

import unittest

from IBANBICFilter import IBANBICFilter

# python3 -m unittest
class TestIBANBICFilter(unittest.TestCase):
    def get_test_case(self, beginning='', spaces_at=[]):
        test_case = "\"" + beginning + "IBAN: DE87123456781234567890 BIC: COBADEHD055\""

        spaces_at.sort()
        spaces_at.reverse()

        for i in spaces_at:
            test_case = test_case[:i] + ' ' + test_case[i:]

        return test_case

    def test_filter_removes_spaces_in_IBAN(self):
        ibanBICFilter = IBANBICFilter()

        expected_string = self.get_test_case()
        index_of_space = expected_string.index("IBAN: ") + len("IBAN: ") + 1

        actual_string = ibanBICFilter.filter(self.get_test_case(spaces_at=[index_of_space]))
        self.assertEqual(expected_string, actual_string)

    def test_filter_removes_spaces_in_BIC(self):
        ibanBICFilter = IBANBICFilter()

        expected_string = self.get_test_case()
        index_of_space = expected_string.index("BIC: ") + len("BIC: ") + 1
        
        actual_string = ibanBICFilter.filter(self.get_test_case(spaces_at=[index_of_space]))
        self.assertEqual(expected_string, actual_string)

    def test_leaves_glibberish_intact(self):
        ibanBICFilter = IBANBICFilter()
        
        glibberish = 'Any kind of string at the beginning BIC: IBAN: BIC: ' 

        spaces_at = []
        spaces_at.append(self.get_test_case(glibberish).rindex("IBAN: ") + len("IBAN: ") + 1)
        spaces_at.append(self.get_test_case(glibberish).rindex("BIC: ") + len("BIC: ") + 1)

        string = self.get_test_case(glibberish, spaces_at)
        expected_string =  self.get_test_case(glibberish)

        actual_string = ibanBICFilter.filter(string)
        self.assertEqual(expected_string, actual_string)


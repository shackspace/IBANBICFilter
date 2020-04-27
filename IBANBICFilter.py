#!/usr/bin/python3

import unittest

# pip3 install schwifty
import re
import schwifty

# python3 -m unittest IBANBICFilter.TestIBANBICFilter
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


class IBANBICFilter():
    def filter(self, line):
        resulting_line = line

        match = re.search('".*IBAN: (.*) BIC: ((\\w\\s?){11}|(\\w\\s?){8})"', resulting_line)

        if not match is None and len(match.groups()) >= 2:
           # replace bic
            span = match.span(2)
            index = span[0]
            end_index = span[1]

            try:
                # raises exception if BIC can not be parsed
                bic = schwifty.BIC(match.group(2))

                # replace BIC string with compact string from successfully parsed BIC object
                resulting_line = resulting_line[:index] + bic.compact + resulting_line[end_index:]
            except:
                pass

            # replace iban
            index = match.span(1)[0]
            
            # try to parse iban of variable length - can be up to 32 dependening on the country code
            # worst case a space after each character -> check lengths up to 64
            for length in range(2, 64+1):
                try:
                    # raises exception if IBAN can not be parsed
                    iban = schwifty.IBAN(resulting_line[index:index+length])

                    # replace IBAN string with compact string from successfully parsed IBAN object
                    resulting_line = resulting_line[:index] + iban.compact + resulting_line[index+length:]

                    break
                except:
                    pass

        return resulting_line


if __name__ == '__main__':
    ibanBICFilter = IBANBICFilter()

    while True:
        try:
            print(ibanBICFilter.filter(input()))
        except:
            break


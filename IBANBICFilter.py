#!/usr/bin/python3

import unittest

# python3 -m unittest IBANBICFilter.TestIBANBICFilter
class TestIBANBICFilter(unittest.TestCase):
    def get_test_case(self, spaces_at=[]):
        test_case = "IBAN: DE12123456781234567890 BIC: COBADEHD055"

        spaces_at.sort()
        spaces_at.reverse()

        for i in spaces_at:
            test_case = test_case[:i] + ' ' + test_case[i:]

        return test_case

    def test_filter_removes_spaces_in_IBAN(self):
        ibanBICFilter = IBANBICFilter()

        expected_string = self.get_test_case()
        index_of_space = expected_string.index("IBAN: ") + len("IBAN: ") + 1

        actual_string = ibanBICFilter.filter(self.get_test_case([index_of_space]))
        self.assertEqual(expected_string, actual_string)

    def test_filter_removes_spaces_in_BIC(self):
        ibanBICFilter = IBANBICFilter()

        expected_string = self.get_test_case()
        index_of_space = expected_string.index("BIC: ") + len("BIC: ") + 1
        
        actual_string = ibanBICFilter.filter(self.get_test_case([index_of_space]))
        self.assertEqual(expected_string, actual_string)

    def test_leaves_glibberish_intact(self):
        ibanBICFilter = IBANBICFilter()
        
        glibberish = 'Any kind of string at the beginning BIC: IBAN: BIC: ' 

        spaces_at = []
        spaces_at.append(self.get_test_case().index("IBAN: ") + len("IBAN: ") + 1)
        spaces_at.append(self.get_test_case().index("BIC: ") + len("BIC: ") + 1)

        string = glibberish + self.get_test_case(spaces_at)
        expected_string =  glibberish + self.get_test_case()

        actual_string = ibanBICFilter.filter(string)
        self.assertEqual(expected_string, actual_string)


class IBANBICFilter():
    def filter(self, line):
        resulting_line = ''
        tokens = line.split(' ')

        is_first_token = True
        skip_spaces_until_number_of_characters_read = 0
        for token in tokens:
            if not is_first_token and not skip_spaces_until_number_of_characters_read:
                resulting_line += ' '

            if token.find('BIC:') == 0:
                resulting_line += 'BIC: '
                token = token[len('BIC: '):]
                
                # BIC consists of 8 non-space-characters
                skip_spaces_until_number_of_characters_read = 8

            if token.find('IBAN:') == 0:
                resulting_line += 'IBAN: '
                token = token[len('BIC: '):]

                # IBAN consists of 22 non-space-characters
                skip_spaces_until_number_of_characters_read = 22

            if not skip_spaces_until_number_of_characters_read:
                resulting_line += token
            else:
                for character in token:
                    if character != ' ' or not skip_spaces_until_number_of_characters_read:
                        resulting_line += character
                        skip_spaces_until_number_of_characters_read -= 1

            is_first_token = False

        return resulting_line


if __name__ == '__main__':
    ibanBICFilter = IBANBICFilter()

    while True:
        try:
            print(ibanBICFilter.filter(input()))
        except:
            break


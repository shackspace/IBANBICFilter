#!/usr/bin/python3

# pip3 install schwifty
import re
import schwifty

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


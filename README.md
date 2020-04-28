# IBANBICFilter

a command line filter to normalize IBAN / BIC outputted by some bank APIs.

```
Testcase input lines:
;"Some transation information... IBAN: DE8712345678 1234567890 BIC: COBADEHD05 5";
;"Some transation information... IBAN: D E87123456781234567890 BIC: C OBADEHD055";

Goal output:
;"Some transation information... IBAN: DE87123456781234567890 BIC: COBADEHD055";
;"Some transation information... IBAN: DE87123456781234567890 BIC: COBADEHD055";

Testcase input lines:
;"Some transation information... IBAN: DE8712345678 1234567890 BIC: V OBADESS";
;"Some transation information... IBAN: DE8712345678 1234567890 BIC: VOBADES S";

Goal output:
;"Some transation information... IBAN: DE87123456781234567890 BIC: VOBADESS";
;"Some transation information... IBAN: DE87123456781234567890 BIC: VOBADESS";
```

## Installation

This tool requires the schwifty library to be installed

```
$ pip3 install schwifty
```

## Example usage

The bank data can simply be piped into the tool to output the same data with normalized IBAN / BICs

```
$ cat someBankTransactions.csv | ./IBANBICFilter.py
```

or

```
$ PYTHONIOENCODING=iso8859-1 cat someBankTransactions.csv | ./IBANBICFilter.py
```

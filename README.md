# xlltgen

Generate Text Filter Files (XLLT Files) for Nintendo's FontConverter.



# Usage

```
usage: xlltgen.py [-h] -f [FILES [FILES ...]]
                  [-e [EXTENSIONS [EXTENSIONS ...]]] [-o OUTPUT] [-t TITLE]
                  [-x CHARSET]

Nintendo CTR Font Converter Text Filter(xllt) Generator.

optional arguments:
  -h, --help            show this help message and exit
  -f [FILES [FILES ...]], --files [FILES [FILES ...]]
                        Files to scan.
  -e [EXTENSIONS [EXTENSIONS ...]], --extensions [EXTENSIONS [EXTENSIONS ...]]
                        Set extensions.
  -o OUTPUT, --output OUTPUT
                        Set output file path.
  -t TITLE, --title TITLE
                        Set title.
  -x CHARSET, --charset CHARSET
                        Set raw charset path. If not set, the charset will not
                        save.

```

# Requirement

Python 2.7

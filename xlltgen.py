import os,sys,codecs
from fnmatch import fnmatch
import argparse

BLACK_LIST = [u'\u0000', u'\u001e', u'\ufeff', u'\u000a', u'\u000d']

def walk(dirname):
    filelist = []
    for root, dirs, files in os.walk(dirname):
        for filename in files:
            fullname = os.path.join(root, filename)
            filelist.append(fullname)
    return filelist

def getenc(path):
    with open(path,'rb')as inputfile:
        if inputfile.read(2) == '\xff\xfe':
            return 'utf-16le'
        inputfile.seek(0,0)
        if inputfile.read(2) == '\xfe\xff':
            return 'utf-16be'
        inputfile.seek(0,0)
        if inputfile.read(3) == '\xef\xbb\xbf':
            return 'utf-8-sig'
        return 'utf-8'

def scanfile(path):
    print path
    text = codecs.open(path,'r',getenc(path)).read()
    charset = []
    for c in text:
        if not c in charset:
            charset.append(c)
    charset.sort()
    return charset

def scanfiles(paths, exts):
    charset = []
    for path in paths:
        for fext in exts:
            if fnmatch(path, fext):
                charset.extend(scanfile(path))
                break
    result = []
    for c in charset:
        if (not c in result) and (not c in BLACK_LIST):
            result.append(c)
    result.sort()
    return ''.join(result)

def savecharset(path, charset):
    s = u''
    i = 0
    for c in charset:
        s += c
        i += 1
        if i == 16:
            s += '\n'
            i = 0
    codecs.open(path, 'w', 'utf-8-sig').write(s)
    print 'Save:', path

def genxllt(charset, title='Default'):
    xllt = '''<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE letter-list SYSTEM "letter-list.dtd">

<letter-list version="1.0">
	<head>
		<create user="LITTOMA" date="2016-11-03" />
		<title>%s</title>
		<comment></comment>
	</head>

	<body>
		<letter>

        '''%title
    i = 0
    for c in charset:
        xllt += '&#x%04x; '%(ord(c))
        i+=1
        if i == 16:
            xllt += '\n        '
            i = 0
    xllt += '''

		</letter>
	</body>

</letter-list>
'''
    return xllt

def parse_options():
    parser = argparse.ArgumentParser(description="Nintendo CTR Font Converter Text Filter(xllt) Generator.")
    parser.add_argument('-f', '--files', help="Files to scan.", required=True, nargs='*', type=str)
    parser.add_argument('-e', '--extensions', help="Set extensions.", default=["*.txt"], nargs='*', type=str)
    parser.add_argument('-o', '--output', help="Set output file path.")
    parser.add_argument('-t', '--title', help="Set title.", default='Default filter')
    parser.add_argument('-x', '--charset', help="Set raw charset path. If not set, the charset will not save.", default=None)
    return parser.parse_args()

def main():
    options = parse_options()
    if not options:
        return False
    charset = scanfiles(options.files, options.extensions)
    
    if options.output:
        codecs.open(options.output, 'w', 'utf-8-sig').write(genxllt(charset, options.title))
    if options.charset:
        savecharset(options.charset, charset)


if __name__ == '__main__':
    main()

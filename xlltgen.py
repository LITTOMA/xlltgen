import os,sys,codecs
from fnmatch import fnmatch
from optparse import OptionParser

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

def scanfiles(paths, fext):
    charset = []
    for path in paths:
        if fnmatch(path, fext):
            charset.extend(scanfile(path))
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


def vararg_callback(option, opt_str, value, parser):
    assert value is None
    value = []

    def floatable(str):
        try:
            float(str)
            return True
        except ValueError:
            return False

    for arg in parser.rargs:
        # stop on --foo like options
        if arg[:2] == "--" and len(arg) > 2:
            break
        # stop on -a, but not on -3 or -3.0
        if arg[:1] == "-" and len(arg) > 1 and not floatable(arg):
            break
        value.append(arg)

    del parser.rargs[:len(value)]
    setattr(parser.values, option.dest, value)


def parse_options():
    parser = OptionParser()
    parser.add_option("-f", "--files", dest="files", action="callback", callback=vararg_callback)
    parser.add_option('-e', type='string', dest='ext', default='*.txt', help='Set scan file extention.')
    parser.add_option('-o', type='string', dest='output', help='Set output path.')
    parser.add_option('-t', type='string', dest='title', default='Default', help='Set title.')
    parser.add_option('-x', type='string', dest='charset', help='Save charset.')
    (options, args) = parser.parse_args()
    if not options.files:
        parser.print_help()
        return None
    return options

def main():
    options = parse_options()
    if not options:
        return False
    charset = scanfiles(options.files, options.ext)
    
    codecs.open(options.output, 'w', 'utf-8-sig').write(genxllt(charset, options.title))
    if options.charset:
        savecharset(options.charset, charset)


if __name__ == '__main__':
    main()

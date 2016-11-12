import os,sys,codecs
from fnmatch import fnmatch
from optparse import OptionParser

BLACK_LIST = [u'\u0000', u'\u001e']
MODES = ['file', 'dir']

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
    parser = OptionParser()
    parser.add_option('-m', type='string', dest='mode', help='Set scan mode.(file/dir)')
    parser.add_option('-e', type='string', dest='ext', default='*.txt', help='Set scan file extention.')
    parser.add_option('-i', type='string', dest='input', help='Set input path.')
    parser.add_option('-o', type='string', dest='output', help='Set output path.')
    parser.add_option('-t', type='string', dest='title', default='Default', help='Set title.')
    (options, args) = parser.parse_args()
    if((not options.mode) or (not options.input)) or (not (options.mode in MODES)):
        parser.print_help()
        return None
    return options

def main():
    options = parse_options()
    if not options:
        return False
    if options.mode == 'file':
        if os.path.isdir(options.input):
            print 'Input is not a file.'
            return False
        codecs.open(options.output, 'w', 'utf-8-sig').write(genxllt(scanfile(options.input), options.title))
        return True
    if options.mode == 'dir':
        if os.path.isfile(options.input):
            print 'Input is not a directory.'
            return False
        codecs.open(options.output, 'w', 'utf-8-sig').write(genxllt(scanfiles(walk(options.input), options.ext), options.title))
        return True


if __name__ == '__main__':
    main()

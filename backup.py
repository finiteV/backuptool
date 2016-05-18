# -*- coding: utf-8 -*-
import optparse
import sys
from FilesMan import FilesMan
from passwordman import PasswordMan
#from backuptool import BackUpTool
#-------------------------------------
#配合backuptool压缩零散文件,提高压缩速度
# backtool = BackUpTool()
# backtool.start()
# backtool.join()
#---------------------------------"to:k1:k2:pr:a:q:sd:tl:dr"

parser = optparse.OptionParser(
            "usage: backup.py -o <where> -k <key1> -s <key2> -r <dir1;dir2>"
            )

parser.add_option('-o', dest='todir', type='string',help='where')
parser.add_option('-k', dest='key1', type='string',help='key1')
parser.add_option('-s', dest='key2', type='string',help='key2')
parser.add_option('-r', dest='dirs', type='string',help='dirs to backup')
parser.add_option('-n', dest='secondir', type='string',help='second dir related')

parser.add_option('-p', dest='printable', type='string',help='printable')
parser.add_option('-a', dest='a1', type='int',help='parm1 to keygen')
parser.add_option('-q', dest='q', type='int',help='parm2 to keygen')
parser.add_option('-t', dest='tool', type='string',help='compression tool')


(options, args) = parser.parse_args()
if (options.todir == None) or (options.key1 == None)\
     or (options.key2 == None) or (options.dirs == None):
    print parser.usage
    sys.exit(0)


todir = options.todir  
key1 = options.key1
key2 = options.key2
dirs = options.dirs

if options.printable==None:
        printable = '~!!!!!!!!!!!!'\
            ',,,,,,,,,,,,,,,,,,,,,,'
else:
    printable = options.printable
if options.a1==None:
    a1 = 3
else:
    a1 = options.a1
if options.q==None:
    q = 3
else:
    q = options.q

PwdMan = PasswordMan(printable)
key1 = PwdMan.keygen(key1,a1,q)
key2 = PwdMan.keygen(key2,a1,q)

if options.secondir==None:
    secondir = ''
else:
    secondir = options.secondir
if options.tool==None:
    tool = 'rar'
else:
    tool = options.tool

for dr in dirs.split(';'):
    if dr=='':   continue
    
    fileman = FilesMan()
    if fileman.init(dr):
        sys.exit(-1)
        
    fileman.init_cpress(todir,key1,key2,secondir,tool)
    
    fileman.start()
    fileman.join()
    #--------------------------------
    if fileman.Changed:
        fileman.compress.spliterar(10)
    #print("[*] {} is Done.".format(dr))

# -*- coding: utf-8 -*-
from FilesMan import FilesMan
from passwordman import PasswordMan
#from backuptool import BackUpTool
#-------------------------------------
#配合backuptool压缩零散文件,提高压缩速度
# backtool = BackUpTool()
# backtool.start()
# backtool.join()
#---------------------------------
key1 = 'kWbNt8xUPfcP'
key2 = '97O3pRBYPz5d'
printable = '~!QAZ@WSX#EDC$RFV%TGB^YHN&UJM*IK'\
        ',<(OL.>)P;:/?-[=+]}'
a1 =1
q=2        
PwdMan = PasswordMan(printable)
key1 = PwdMan.keygen(key1,a1,q)
key2 = PwdMan.keygen(key2,a1,q)

todir = 'E:\\'
dirs = ['G:\\test']
secondir = 'YUN1\\Zips\\'
tool = 'rar'

for dr in dirs:
    fileman = FilesMan()
    if fileman.init(dr):
        import sys
        sys.exit(-1)
        
    fileman.init_cpress(todir,key1,key2,secondir,tool)
    
    fileman.start()
    fileman.join()
    #--------------------------------
    fileman.compress.spliterar(10)
    print("[*] {} is Done.".format(dr))

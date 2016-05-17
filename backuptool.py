# -*- coding: utf-8 -*-
##this tool is very simple, just zip some important folder
##to back up directory.
import shutil
import os
import os.path
from threading import Thread
import time
import tempfile
import sys
class BackUpTool(Thread):
    """
    Those folders are tools,some software,the html files,
    eclipse workspace,netbean workspace,python programs
    """
    #back folder contains the exception dir of a folder
    def __init__(self):
        Thread.__init__(self)
        ##--------------zip目录-----------------------
        self.folders = [
                   #['folder','exclude1',...],
                   ['F:\\Work\\workspace','.metadata'],
                   ['F:\\Work\\Python'],
                   ['F:\\Work\\PHP'],                   
                   ['F:\\Work\\Cspace'],
                   ['F:\\User','Downloads','Music','Downloads','Documents'],
                   ['D:\\Program Files (x86)\\iDailyDiary\\DATA']
                ]
        #self.testfolder=[['F:\\Temp','aaa']]
        ##-----------------备份路径-------------------------
        self.DESTINATION = 'F:\\Laboratory\\SourceCode\\'
        self.tmpdirname = tempfile.mkdtemp()

    def run(self):
        for folder in self.folders:
            #分为全目录,部分目录.部分目录需借用系统临时目录
            if len(folder) > 1:
                ##move the select file to temp folder
                dirs = os.listdir(folder[0])
                #the root path of an second tmp folder
                print self.tmpdirname
                dst=self.tmpdirname+'\\'+self.get_name(folder[0])
                ###copy sub directory###
                for dir in dirs:
                    if dir not in folder[1:]:
                        #copy exact file to system temp dir with same name
                        src = folder[0]+'\\'+dir  
                        dst1 = dst + '\\'+dir                       
                        print '##Copy dir:',src,dst1,'##\n'
                        self.mycopytree(src,dst1)

                #back up it
                print '#',folder[0],' is compressing','#\n'
                shutil.make_archive(self.DESTINATION+self.get_name(folder[0]),'zip',dst)
                print '#',folder[0],' is compressed~','#\n'
            else:##copy whole directory
                print '#',folder[0],' is compressing...','\n'
                shutil.make_archive(self.DESTINATION+self.get_name(folder[0]),'zip',folder[0])
                print '#',folder[0],' is compressed~','#\n'

            time.sleep(1)
        print '###The back up process has finished sucessfully!###'

    def get_name(self,path):
        """
        return the basename of the path
        """
        return os.path.basename(path)

    def mycopytree(self,src, dst):
        ####first of all, copy a file
        if os.path.isfile(src):
            dst = os.path.dirname(dst)
            if not os.path.exists(dst):
                os.mkdir(dst)
            print '#Copy file:',src,dst,'\n'
            shutil.copy2(src,dst)
            return 0

        ###second condition, copy a directory
        names = os.listdir(src)
        if not os.path.isdir(dst):
            os.makedirs(dst)
        
        errors = []
        #sleep for every directory copying
        #time.sleep(1)
        for name in names:
            srcname = os.path.join(src, name)
            dstname = os.path.join(dst, name)
            try:
                if os.path.isdir(srcname):
                    self.mycopytree(srcname, dstname)
                else:
                    if(not os.path.exists(dstname)):
                        shutil.copy2(srcname, dstname)
                    else:
                        #判断文件是否更新
                        if(os.stat(srcname)[8] > os.stat(dstname)[8]):
                            #移除文件，然后拷贝
                            os.remove(dstname)
                            shutil.copy2(srcname, dstname)
            except:
                print '!!!Error File:',srcname,sys.exc_info()[0],'!!!\n'
####---------使用方法------------------------------------
if __name__ == "__main__":
    #print 'abb'
    backtool = BackUpTool()
    backtool.start()
    #backtool.mycopytree('F:\\Temp\\173.py','c:\\users\\bangle\\appdata\\local\\temp\\tmpvkinho\\Temp\\173.py')

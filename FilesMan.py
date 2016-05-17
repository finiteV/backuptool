# -*- coding: utf-8 -*-
from threading import Thread,Lock
import hashlib
import time
import os.path
import sys
from Compress import Compress
from dbman import DBMan
lock = Lock()
class FilesMan(Thread):
    ''''
    备份一个目录,主要类,不能有重复文件,第一次时间比较长,由rar引起
    '''
    def __init__(self):
        Thread.__init__(self)  
             
    def init(self,dirname):
        self.dir = dirname  #备份目录 
            
        self.dbman = DBMan(os.path.basename(self.dir)+'_metadata')
        self.firstime = self.is_firstime()  
        
        return 0
    
    def init_cpress(self,todir,key1,key2,secondir,tool):
        self.compress = Compress()
    
        self.compress.init(todir,secondir,tool)
        self.compress.init_key(key1,key2) 
            
        return 0
                                
    def run(self):
        ##是否第一次进行备份
        if self.firstime:
            self.compress.addir(self.dir)
            print '[*] Sccessfully for the first time.'
        ##先进入目录，然后递归处理文件,不检查目录
        os.chdir(self.dir)
        ##若第一次则,只更新数据库
        self.walkdir()         
    
 
    ###主要函数,递归处理一个目录,仅处理实体文件###
    def walkdir(self,abssrc=''):
        '''
        相对绝对路径,可以屏蔽处理文件
        '''
        ####如果是文件结束进程####
        if os.path.isfile(abssrc):  
            #self.file_handle(abssrc)
            print '[!] 只处理目录'
            return 0

        ###如果是目录,递归处理目录#####
        if abssrc=='':##顶级主目录
            names = os.listdir('.')
        else:##子目录
            names = os.listdir(abssrc)
        #sleep for every directory handle
        time.sleep(1)
        for name in names:
            srcname = os.path.join(abssrc, name)
            try:
                #self.walkdir(srcname)#错误递归
                ##展开理解##
                if os.path.isdir(srcname):
                    self.walkdir(srcname)
                elif os.path.isfile(srcname) and not os.path.islink(srcname):
                    lock.acquire()
                    self.single_handle(srcname)
                    lock.release()
                    #print srcname
            except:
                print '[!] Error File:',srcname,sys.exc_info()[0],'!!!\n'
                
    def single_handle(self,srcname):
        '''
        处理单个文件非链接,想对于顶级目录下绝对目录
        包括处理压缩文件,数据库
        '''                        
        #1.文件hash值
        sha1str = self.hashfile(srcname)
        
        #2.若文件hash值在数据库中不存在
        res = self.dbman.query(sha1str)
        
        if not res:
            res = self.dbman.query('',srcname)
            if not res:
                #2.1 更新数据库
                self.dbman.insert(srcname, sha1str)  
                #2.2 添加文件,第一次备份时略过
                if not self.firstime: 
                    self.compress.addfile(srcname)
            else:
                #2.0 更新文件
                self.dbman.update(res[0][0],'',sha1str)
                self.compress.delfile(srcname)
                self.compress.addfile(srcname) 
        #3.文件hash值存在,但目录改变
        ##不考虑链接等,多个重复文件将，覆盖只保留同hash值最后一个文件
        elif res[0][1]!=srcname:
            #3.1 更新数据库
            self.dbman.update(res[0][0],srcname)
            print("[+] update {0} with {1} as they are the same.\n".
                  format(res[0][0],srcname))
            #3.2 更新压缩文件,第一次备份时略过
            if not self.firstime: 
                self.compress.delfile(res[0][1])
                self.compress.addfile(srcname)
        #4.无需更新,文件未改变
        else:
            #4.1 更新数据库
            self.dbman.update(res[0][0])
   
        #5.休息一下
        #time.sleep(0.1)
            
    def trashfile(self):
        '''
        收尾工作,对压缩文件和数据库中文件进行同步
        '''
        rubbish = self.dbman.query_rbsh()
        if not rubbish:
            return
        for r in rubbish:
            ##数据库操作
            self.dbman.delete(r[0])
            ##压缩文件操作
            self.compress.delfile(r[1])
            
    def hashfile(self,filename):
        '''
        caculate sha1 of a file
        '''
        #rltv_path = os.path.dirname(filename)
        sha = hashlib.sha1()
        #sha.update(rltv_path)
        with open(filename,'rb') as f:
            while True:
                block = f.read(2**10)
                if not block:
                    break
                sha.update(block)
            return sha.hexdigest()
    
    def is_firstime(self):
        '''
        通过配置文件是否存在判断是否进行第一次进行备份
        '''
        name = os.path.basename(self.dir)+'_config.ini'
        if os.path.exists(name):
            return False
        else:#第一次之后创建配置文件
            f=open(name,'w')
            f.close()
            return True

    def __del__(self):
        '''
        收尾工作,对压缩文件和数据库中文件进行同步
        删除已经不使用文件
        '''
        try:
            self.trashfile()
        except:
            print "[!]Error while trashfile!!!"
        print '[*] #####End of Backup######'
        
if __name__=='__main__':
    dirs = 'G:\\BackUp'
    todir = 'j:\\'
    #workspace = os.getcwd()
    fileman = FilesMan(dirs,todir)
    fileman.start()
    fileman.join()
    #os.chdir(workspace);
    #fileman.single_handle('metadata.db')
    #fileman.trashfile()
    #import os
    #os.chdir(dirs)
    #srcname = 'dirs/1.txt'
    #print fileman.hashfile(srcname)
    #fileman.single_handle(srcname)
    #fileman.walkdir()
    
    

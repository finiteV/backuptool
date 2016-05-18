# -*- coding: utf-8 -*-
import os
import os.path
import subprocess

class RarCompressor:
    '''
    都是绝对路径,当前压缩工具是rar
    '''  
    def init(self,todir,filename,secondir,tool='rar'):
        ##绝对备份目录路径
        filename = self.namegen(filename)
        self.dest = os.path.join(todir, filename+'.rar')
        
        self.sfilename = self.namegen(filename+'_BBK')
        secr_dest = os.path.join(todir, secondir)
        self.secr_dest = os.path.join(secr_dest,self.sfilename+'.rar')
        
        #self.tool = tool
        
        return 0
 
    def init_key(self,key='key1',secrkey='key2',):
        self.key = key
        self.secrkey = secrkey 
        print '\n[*] key: \n',self.key,'\nsecure key: \n',self.secrkey,'\n'  
       
    def addfile(self,filename):
        '''
        添加一个压缩文件,或者压缩一个绝对目录下所有文件
        '''
        #cmd = "rar a -hp%s %s %s" % (self.key,self.dest,filename)
        try:
            cmd = ['rar','a','-hp'+self.key,self.dest,filename]
            child = subprocess.Popen(cmd,stdout=subprocess.PIPE)
            print '[+] adding %s' % filename
            #child.wait()
            out = child.communicate()
#             for k in out:
#                 print k
        except Exception as e:
            print e
        
        #os.system(cmd)
    def addir(self,dirname):
        '''
        压缩一个绝对目录下所有文件
        '''
        src = os.getcwd()
        try:
            os.chdir(dirname)
            cmd = ['rar','a','-r','-hp'+self.key,self.dest]
            child = subprocess.Popen(cmd,stdout=subprocess.PIPE)
            print '[+] first time,compressing dir %s' % dirname
            #child.wait()
            out = child.communicate()
#             for k in out:
#                 print k
        except Exception as e:
            print e
        finally:
            os.chdir(src)

    def delfile(self,filename):
        '''
        删除一个压缩文件
        '''
        #cmd = "rar d -hp%s %s %s" % (self.key,self.dest,filename)
        #os.system(cmd)
        try:
            cmd = ['rar','d','-hp'+self.key,self.dest,filename]
            child = subprocess.Popen(cmd,stdout=subprocess.PIPE)
            print '[-] deleting %s' % filename
            #child.wait()
            out = child.communicate()            
        except Exception as e:
            print e
    
    def spliterar(self,per_len=1):
        '''
        将压缩文件分卷压缩,默认1m分割
        '''
        #cmd = "rar a -hp%s -v%dm %s %s" % (self.secrkey,self.piece_len,self.secr_dest,self.dest)
        #per_len = 1#default 1024m
        src = os.getcwd()
        pt,name = os.path.split(self.secr_dest)
        os.chdir(pt)
        if os.path.exists(name):
            os.remove(name)
        r_str = "{0}.part".format(self.sfilename)
        for fl in os.listdir(pt):
            if r_str in fl:
                os.remove(fl)
        try:
            cmd = ['rar','a','-hp'+self.secrkey,'-v'+str(per_len)+'m',self.secr_dest,self.dest]
            child = subprocess.Popen(cmd,stdout=subprocess.PIPE)
            print '[+] spliting %s ...' % self.dest
#             child.wait() #buggy
            out = child.communicate()
#             for k in out:
#                 print k
        except Exception as e:
            print e
        finally:
            os.chdir(src)
        # remove source rar
        #os.remove(self.dest)
        
    def namegen(self,salt):
        import hashlib
        sha = hashlib.sha1()
        sha.update(salt)
        name = sha.hexdigest()
        return name
    
if __name__=="__main__":
    todir = ''
    os.chdir('e:\\')
    test = RarCompressor(todir);
    #print 'add a file'
    #filename = 'dirs/3.txt'     ##不要代一代目录路径
    #test.addfile(filename);
    #del a file
    #test.delfile(filename)
    test.spliterar()

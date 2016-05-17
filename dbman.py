# -*- coding: utf-8 -*-
import sqlite3
class DBMan():
    
    def __init__(self,dbname):
        '''
        只进行一次
        '''
        self.dbname = dbname+'.db';
        self.conn = sqlite3.connect(self.dbname,check_same_thread = False); 
        self.conn.text_factory = bytes#解决中文出错
        #if not exits, create it
        #if not os.path.exists(self.dbname):
        ##1.新建表
        sqls = ("create table if not exists filehash("
                    "id integer not null primary key autoincrement,"
                    "absname char(100) not null,"
                    "hash char(200) not null,"
                    ##初始0,添加新文件为1,更新文件2,已存在未改变状态3,
                    ##一次备份后删除状态为0文件
                    "status integer default 0"
                    ")");
        self.conn.execute(sqls)
        self.conn.commit()
        ##2.更新状态
        sqls = "update filehash set status=0"
        self.conn.execute(sqls)
        self.conn.commit()
    
    def query(self,sha1str,path=''):
        '''
        查询hash值,若hash值存在,则返回文件对于的绝对路径,以及id;不存在返回False
        '''
        if path=='':
            sqls = 'select id,absname from filehash where hash = "%s"' % sha1str
        else:
            sqls = 'select id from filehash where absname = "%s"' % path
        try:
            cur = self.conn.cursor()
            cur.execute(sqls)
            res = cur.fetchall()
            
            cur.close()
        except Exception as e:
            print e
        if len(res)==1:
            return res
        else:
            return False
         
    def insert(self,abssrc,sha1str):
        #1.路径,文件名
        sqls = 'insert into filehash(absname,hash,status) values ("%s","%s",%d)' % (abssrc,sha1str,1)
        try:
            self.conn.execute(sqls)
            self.conn.commit()
        except Exception as e:
            print e
    
    def update(self,iid,abssrc='',hash_str=''):
        '''
        更新hash值存在的文件的路径值
        '''
        
        if hash_str!='':
            sqls = 'update filehash set hash="%s",status=%d where id=%d' % (hash_str,1,iid)
        elif abssrc=='':##文件已经存在，更新状态
            sqls = 'update filehash set status=%d where id=%d' % (3,iid)
        else:##文件目录改变，内容未变
            sqls = 'update filehash set absname="%s",status=%d where id=%d' % (abssrc,2,iid)
        try:
            self.conn.execute(sqls)
            self.conn.commit()
        except Exception as e:
            print e
        return True
    
    def query_rbsh(self):
        '''
        查询数据库中垃圾文件,不存在返回False，存在返回id,路径数组
        只进行一次
        '''
        sqls = 'select id,absname from filehash where status = 0'
        cur = self.conn.cursor()
        
        cur.execute(sqls)
        res = cur.fetchall()
        cur.close()
        if len(res)>0:
            return res
        else:
            return False
    
    def delete(self,iid):
        '''
        删除数据库中已经不存在的文件
        '''
        sqls = 'delete from filehash where id = %d' % iid
        try:
            self.conn.execute(sqls)
            self.conn.commit()
        except Exception as e:
            print e
        
        return True
    
    def __del__(self):
        self.conn.close()
    
if __name__=='__main__':
    dbman = DBMan()
    #dbman.insert('/test', '11111111')
    #print dbman.query('11111112')
    print dbman.query_rbsh()
    #print dbman.update(2)
    #print dbman.delete(3)
    
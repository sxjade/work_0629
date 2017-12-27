# -*- coding:utf-8 -*-
'''
@author: liuyang
'''
import ConfigParser
import os
import shutil
import datetime
import re
import hashlib  

class Conf:
    def __init__(self,ini_file):
        self.ini_f = ini_file
        self.config=ConfigParser.ConfigParser()
        self.config.readfp(open(ini_file))
        
    
    def get_New_table(self):
        new_str = self.config.get('CodeTable','newtable')
        
        return new_str
        
    def get_server_dir(self):
        return self.config.get('CodeTable','server')
    
    def get_cle_dir(self):
#         print self.config.get('CodeTable','cledir')
        return self.config.get('CodeTable','cledir')


class Codetable:
    def __init__(self,conf):
        self.conf = conf


    def backup(self,bkdir,bkfile):
        to_dir = os.path.join(bkdir,'bak')
#         print to_dir
        yOrn = os.path.isdir(to_dir)
        if yOrn is False:
            print "Make dir %s" % to_dir
            os.mkdir(to_dir)
        
        to_file = os.path.join(to_dir,setver(bkfile))
        from_file = os.path.join(bkdir,bkfile)
        
        if os.path.isfile(from_file):
            cpfile(from_file,to_file)
            pass
        if os.path.isfile(to_file):
            print '%s backup ok!' % to_file
            return True
        else:
            print '%s backup error!' % to_file
            return False
        
    def update_f(self,root,f):
        to_f = os.path.join(root,f)
        new_table = self.conf.get_New_table()
        from_f = False
        if re.search('dataserver',root) is not None:
            from_f = os.path.join(new_table,'CWcodetable.XML')
#             print 'Server'
        elif re.search('lianxu',root)is not None or re.search('sender',root)is not None:
            from_f = os.path.join(new_table,'Scodetable.XML')
#             print 'sender or lianxu'
        elif re.search('UpdateWeb',root):
            from_f = os.path.join(new_table,'Ccodetable.XML')
#             print 'cle'
        else:
            pass
        if from_f:
            torf = cpfile(from_f,to_f)
            if torf:
                return True
            else:
                return False
    
    def traverse(self,f_dir):
        
        if os.path.isdir(f_dir):
            for root,dir,filer in os.walk(f_dir):
                for d in dir:
                    if d == 'data':
                        dir.remove(d)
#                 print root, dir, filer
                for f in filer:
                    if f == 'codetable.XML':
#                         print root,f
                        codefile = os.path.join(root,f)
                        yorn = self.backup(root,f)
                        if yorn:
                            if self.update_f(root,f):
                                print 'update ok \n'
                            else:
                                print 'update false \n'
                        else:
                            print 'backup error,update False. \n'
                        
        else:
            print '%s is not dir.' % f_dir

def cpfile(from_f,to_f):
    if os.path.isfile(from_f):
        shutil.copyfile(from_f,to_f)
        if IsHashEqual(from_f,to_f):
            print 'Copy %s ot %s ok!' % (from_f,to_f)
            return True
        else:
            print 'Copy %s ot %s lose,' % (from_f,to_f)
    else:
        print 'Copy error, %s is not a file.' % from_f
        return False

# 
def setver(f_str):
    today = datetime.datetime.now()
    todaystr = today.strftime("%Y%m%d")
    (filepath,tempfilename) = os.path.splitext(f_str);  
#     print filepath,tempfilename
    ver = filepath + '_' + todaystr  + tempfilename
#     print ver
    return ver


def getHash(f):  
    line=f.readline()  
    hash=hashlib.md5()  
    while(line):  
        hash.update(line)  
        line=f.readline()  
    return hash.hexdigest()  

def IsHashEqual(f1_str,f2_str): 
    f1=open(f1_str,"rb")  
    f2=open(f2_str,"rb")  
    str1=getHash(f1)  
    str2=getHash(f2)  
    return str1==str2  

def main(confile):
    conf = Conf(confile)
    code = Codetable(conf)
    cledir=conf.get_cle_dir()
    serdir =conf.get_server_dir()
    
    code.traverse(serdir)
    code.traverse(cledir)


if __name__ == '__main__':
    confile = './updateConfig.ini'
    main(confile)


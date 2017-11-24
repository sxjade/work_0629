# -*- coding:utf-8 -*-
'''
@author: liuyang
'''
import os
import re
import datetime

class LogDate:
    def __init__(self,serverlogdir):
        self.txtLogName = ''
        self.log4jLogName = ''
        self.logDir = serverlogdir
        
        
    def setTxtName(self):
        today = datetime.date.today()
        self.txtLogName = today.strftime('%Y%m%d')+'.txt'
        print self.txtLogName
        return self.txtLogName
    
    def setLog4jName(self):
        today = datetime.date.today()
        self.log4jLogName = today.strftime('%Y-%m-%d')+'.log4j'
        print self.log4jLogName
        return self.log4jLogName
    
    def handleLog(self):
        print self.logDir
        for path in self.logDir:
            if os.path.isdir(path):
                for root,dirs,files in os.walk(path):
                    for filepath in files:
                        self.delLog(root,filepath)
    
    def delLog(self,dirs,filer):
        print dirs,filer
        log4j = re.findall(r".*log4j$",filer)
        txt = re.findall(r".*txt$",filer)
        if log4j or txt:
            if filer <> self.log4jLogName and filer <> self.txtLogName:
                logFile = os.path.join(dirs,filer)
                print logFile
                os.remove(logFile)
        else:
            print '%s is not log file.' % filer




if __name__ == '__main__':
    logDir = ('D:\\Server\\newserver\\dataserver\\log',\
              'D:\\Server\\newserver\\dataserver2\\log',\
              'D:\\Server\\newserver\\dataserver3\\log',\
              'D:\\Server\\newserver\\dataserver4\\log',\
              'D:\\Server\\sender\\log',\
              'D:\\Server\\sender_3\\log')
    dates = LogDate(logDir)
    dates.setLog4jName()
    dates.setTxtName()
    dates.handleLog()



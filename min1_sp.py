'''
-*- coding:utf-8 -*-

Created on 2017年5月18日

@author: liuyang
'''
import os
import time
import datetime
import csv
from pandas import DataFrame
import ConfigParser
from xml.dom import minidom

class Config:
    def __init__(self,configfile):
        self.conf = ConfigParser.ConfigParser()
        self.conf.read(configfile)

    def getsrcdir(self):
        srcdir = self.conf.get('src','srcdir') 
        return srcdir
    
    def getproduct(self):
        product = self.conf.get('src','product')
        return product
    
    def getcodetable(self):
        codetable = self.conf.get('src','codetable')
        return codetable
    
    def getnight(self):
        night = self.conf.getboolean('src', 'night')
        return night
    
    def getdot(self):
        dot = self.conf.getint('src', 'dot')
        return dot

    def getdst(self):
        dstcsv = self.conf.get('dst', 'dstcsv')
        return dstcsv

def getcodename(outdir,productname,xmlfilename):
    doc = minidom.parse(xmlfilename)
    root = doc.documentElement
    
    code_nodes = root.getElementsByTagName('subproduct')
    
    for node in code_nodes:
        if node.getAttribute('subsymbol') == productname:
            code_id = node.getAttribute('id')
            if code_id == '0':
                code_id = ''
            father = node.parentNode
            grandfather = father.parentNode
            marketId = grandfather.getAttribute('marketId')
            
            sons = node.childNodes
            for son in sons:
                if son.nodeName == 'list':
                    grandsons = son.childNodes
                    for gdson in grandsons:
                        if gdson.nodeName == 'product':
                            dot = gdson.getAttribute('dot')
                            timezone = gdson.getAttribute('timezone')
                            break
            break
    lianxuname = '1min-'+ marketId + '-' + code_id + '9999.csv'    # 1min-1-19999.csv
    lxpath = os.path.join(outdir,lianxuname)
    return lxpath,dot,timezone


class Filepd:
    
    def __init__(self,outfile,dotstr,timezone):
        self.outfile = outfile
        self.dot = int(dotstr)
        self.timezone = abs(int(timezone))
        self.daylist = []    
        self.lianxulist = []


def readcsv(filername):
    # 读取文件，统计出当前文件每日成交额，以备对比日线最大成交量，找出每日连续合约
    # 市场代码,合约代码,时间,开,高,低,收,成交量,成交额,持仓量
    csvfile = file(filername,'rb')
    reader = csv.reader(csvfile)
    today = None
    sum = 0
    for line in reader:
            
        day = line[2]
#             print type(day),day,'\n'
        daystr = day.decode('gb2312')
        code = int(separateSN(line[1]))
        if daystr == u'时间':
            continue
        else:
            day = datetime.datetime.strptime(line[2],'%Y-%m-%d %H:%M:%S').date()
        if today is None:
            today = day
            sum = sum + int(float(line[7])) +int(float(line[9]))
        elif day == today:
            sum = sum + int(float(line[7])) +int(float(line[9]))
                
        else:
            d = (filername,code,today,sum)    
            # 当读到下一日期后，记录内容：（文件绝对路径，合约名，日期，当日成交额总和）    
            # ('D:\\tmp\\cu\\2013\\cu1305.csv', 1305, datetime.date(2013, 4, 2), 3816032)
            da.daylist.append(d)
            today = day
    d = (filername,code,today,sum)
    da.daylist.append(d)

def main(datedir):
    if os.path.isdir(datedir):
        for root,dir,files in os.walk(datedir):
            for fi in files:
                datefile = os.path.join(root,fi)
                if os.path.isfile(datefile):
#                     print datefile
                    
                    readcsv(datefile)
    
    else:
        print 'this is not dir'
    
    da.appendlist()



if __name__ == '__main__':
    configfile = 'D:\\workspace\\work\\1minconfig.ini'
    config = Config(configfile)
    datedir = config.getsrcdir()
    outfile,dotstr,timezone = getcodename(config.getdst(),config.getproduct(),config.getcodetable())
    
    
    pass
# -*- coding:utf-8 -*-
import os
import time
import datetime
import csv
from pandas import DataFrame
import ConfigParser
from xml.dom import minidom

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
    dayline = 'dayline-'+ marketId + '-' + code_id + '9999.csv'
    dayall = 'dayall-'+ marketId + '-' + code_id + '9999.csv'
    
    lxpath = os.path.join(outdir,lianxuname)
    daylinpath = os.path.join(outdir,dayline)
    dayallpath = os.path.join(outdir,dayall)
    
    return lxpath,daylinpath,dayallpath,dot,timezone

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
    
class Filepd:
    
    def __init__(self,outfile,daylinpath,dayallpath,dotstr,timezone):
        self.outfile = outfile
        self.daylinpath = daylinpath
        self.dayallpath = dayallpath
        self.dot = int(dotstr)
        self.timezone = abs(int(timezone))
        self.daylist = []    
        self.lianxulist = []
        

    def appendlist(self):
        # 将daylist内容以日期排列后遍历找出连续合约，添加到lianxulist中
        # (lianxufile,lianxucode,lianxudate,lianxuvol)
        pd = DataFrame(self.daylist,columns=['file','code','date','vol'])
        pds = pd.sort_values(by=['date','code'])
        pds.index = range(len(self.daylist))  # 替换index
        pds.to_csv(self.dayallpath)
#         print pds
        lianxufile = None
        lianxudate = None
        lianxucode = 0
        lianxuvol = 0
        for i in pds.index:
            ifile,icode,idate,ivol = pds.iloc[i]
            if ifile == 'file':
                continue
            if lianxufile == None :  # 初始赋值
                lianxufile,lianxucode,lianxudate,lianxuvol = ifile,icode,idate,ivol
            else:
                if icode < lianxucode:
                    continue
                else:
                    if idate == lianxudate:
                        if ivol > lianxuvol :  #  确保连续不回头
                            lianxufile,lianxucode,lianxudate,lianxuvol = ifile,icode,idate,ivol
                        else:
                            pass
                    else:
                        self.lianxulist.append((lianxufile,lianxucode,lianxudate,lianxuvol))
                        
                        if icode >= lianxucode:
                            lianxufile,lianxucode,lianxudate,lianxuvol = ifile,icode,idate,ivol  # 添加一条记录后，清空lianxufile
                        else:
                            pass
                    
        self.lianxulist.append((lianxufile,lianxucode,lianxudate,lianxuvol))
        csvfile = file(self.daylinpath,'wb')
        writer = csv.writer(csvfile)
        writer.writerows(self.lianxulist)
        self.findlianxu()

    def findlianxu(self):
        # 新建并打开目标文件，从lianxulist中统计各个连续文件内含连续日期的列表。
#         outfile,_ = getcodename(config.getdst(),config.getproduct(),config.getcodetable())
        csvfile = file(self.outfile,'wb')
        writer = csv.writer(csvfile)
        lianxufi = None
        lianxudate = []
        for lianxu in self.lianxulist:
            
#             print type(lianxu[2])
            if lianxufi == None:
                lianxufi = lianxu[0]
                lianxudate.append(lianxu[2])
            else:
                if lianxu[0] == lianxufi:
                    lianxudate.append(lianxu[2])
                else:
                    self.writerfile(lianxufi,lianxudate,writer)
                    lianxufi = lianxu[0]
                    lianxudate = []  # 一个文件写完后清空连续的日期列表
                    lianxudate.append(lianxu[2])
        self.writerfile(lianxufi,lianxudate,writer) # 写入最后一个文件
        csvfile.close()
        
        
    def getdatetime(self,strs,daylin=False):
        # 如果有夜盘，将时间加3小时，无夜盘则加0小时
        t = datetime.datetime.strptime(strs,'%Y-%m-%d %H:%M:%S')
        
        add3h = t + datetime.timedelta(hours = self.timezone)
        
        h = int(datetime.datetime.strftime(add3h,'%H'))
        dayofweek = add3h.weekday()
        if dayofweek == 5: # 如果是周五，则夜盘加两天  （周五夜盘加了3个小时后则为周六的凌晨,weekday是从0-6 周一到周日）
            if 0 <= h <= 5:
                add3h = add3h + datetime.timedelta(days = 2)
        
        if daylin == True:
            return add3h
        
        td = datetime.datetime.strftime(add3h,'%Y.%m.%d')
        tt = datetime.datetime.strftime(add3h,'%H:%M')
#         print td,tt
        return td,tt
    
    def getprice(self,pricestr):
        # 数据库内存的是int型，故而将1为小数的价格乘以10,2位小数的价格乘以100
#         _,dotstr = getcodename(config.getdst(),config.getproduct(),config.getcodetable())
#         dot = int(self.dotstr)
        price = float(pricestr)
        i = 0
        while i < self.dot:
            price = price * 10
            i +=1
        return int(price)

    def writerfile(self,filestr,datelist,writer):
        # 打开连续文件，将日期在日期列表内的记录写入目标文件
        print filestr
        csvfile = file(filestr,'rb')
        reader = csv.reader(csvfile)
        for lin in reader:
            if lin[0].decode('gb2312') == u'市场代码':
                continue
#             print lin[2]
#             day = datetime.datetime.strptime(lin[2],'%Y-%m-%d %H:%M:%S').date()
            day = self.getdatetime(lin[2],daylin=True).date()
            if day in datelist:
                dater,timer = self.getdatetime(lin[2])
                open = self.getprice(lin[3])
                high = self.getprice(lin[4])
                low = self.getprice(lin[5])
                close = self.getprice(lin[6])
                linlist = [dater,timer,open,high,low,close,int(float(lin[7])),int(float(lin[9])),0]
#                 print linlist
                writer.writerow(linlist)
                
            
        csvfile.close()
        print 'lianxu file writered !!!'


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
#             day = datetime.datetime.strptime(line[2],'%Y-%m-%d %H:%M:%S').date()
            day = da.getdatetime(line[2],daylin=True).date()
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
            sum = int(float(line[7])) +int(float(line[9]))
    d = (filername,code,today,sum)
    da.daylist.append(d)
        
        
def separateSN(name):
    # 找出合约数字部分
    proName = ''
    proNum = ''
    names = name.decode('gb2312')
    if names  <> u'合约代码' and names <> '':
        for s in name:
            if s.isalpha() :  
                proName =  proName + s
            else:
                proNum = proNum + s
    else:
        proNum = '0'
    return proNum

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
    outfile,daylinpath,dayallpath,dotstr,timezone = getcodename(config.getdst(),config.getproduct(),config.getcodetable())
    print outfile,dotstr
    da = Filepd(outfile,daylinpath,dayallpath,dotstr,timezone)
    da.getdatetime('2013-07-05 21:15:00')
    main(datedir)
    print 'Complete!!!'




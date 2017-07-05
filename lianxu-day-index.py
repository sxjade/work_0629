# -*- coding:utf-8 -*-
'''
@author: liuyang
'''
import os
import csv
import ConfigParser


class Config:
    
    def __init__(self,configfile):
        self.conf = ConfigParser.ConfigParser()
        self.conf.read(configfile)

    def getsrcdir(self):
        srcdir = self.conf.get('src','srcdir') 
        return srcdir
    
    def getdst(self):
        dstcsv = self.conf.get('dst', 'dstcsv')
        return dstcsv

    def getLX(self):
        product = self.conf.get('src','lianxu')
        return product
    
    def getsse(self):
        ssestr = self.conf.get('src','sse')
        return ssestr

class CodeData:
    
    def __init__(self,lx,sse):
        self.lxFile = lx # 连续文件
        self.sseFile = sse # sse300文件
        self.fileList = [] # 合约文件列表
        self.sseList =[]  # sse300数据列表
        self.codelist = [] # 合约名列表['1607', '1608', '1609', ...]
        self.codedict = {} # 合约名为键，数据列表为内容的字典
        
        self.lxData = [] # 最终写入文件的数据列表
        
    def getsseData(self):
        # 将收盘价存入self。sseList列表
        ssedata = self.readfile(self.sseFile)
        for ss in ssedata:
            if ss[1]=='15:00':
                self.sseList.append(ss)
        
    def codefile(self):
    # 生成合约名列表['1607', '1608', '1609', '1610', '1611', '1612', '1701', '1702', '1703', '1704', '1705', '1706', '1707', '1708', '1709', '1712']
    # 生成合约名为键，数据列表为内容的字典{"1607":[],"1608":[]}
        for fi in self.fileList:
            code = fi[-8:-4]
            self.codelist.append(code)
#             print code
            self.codedict[code] = self.readfile(fi)
        self.codelist.sort()
        print self.codelist
#         print self.codedict

    def readfile(self,filestr):
        # 读取csv文件
        fileli = []
        lxcsv = file(filestr, 'rb')
        data = csv.reader(lxcsv)
        for line in data:
            fileli.append(line)
        return fileli
    
    def getadd2(self,key):
        # 以下标找到隔两个月的合约
        code_index = self.codelist.index(key)
        add2 = self.codelist[code_index+2]
        return add2
    
    def findData(self):
        lianxu = self.readfile(self.lxFile)
        print lianxu
        for l in lianxu:
            # 连续日期，开，高，close
            l_date,l_open,l_high,l_close = l[0], l[2], l[3], l[5]
            for key in self.codedict.keys():
#                 print key
                for c_data in self.codedict[key]:
#                     print c_data
                    if l_date == c_data[0] and l_open==c_data[2] and l_high==c_data[3]:
                        # 找到主力合约隔两个月的合约
                        keyadd2 = self.getadd2(key)
#                         print keyadd2,type(keyadd2)
                        break
            
            # 隔两月close
            if keyadd2:
                for i in self.codedict[keyadd2]:
                    if l_date == i[0]:
                        two_close = c_data[3]
#                     print l_date,l_open,l_high,l_close,two_close
                        break
            
            # sse300close
            for sse in self.sseList:
                
                if l_date == sse[0]:
                    s_close = sse[2]
                    break
                else:
                    s_close = 0
            print l_date,l_open,l_high,l_close,keyadd2,two_close,s_close     
            self.lxData.append((l_date,l_close,two_close,s_close))

    def writerfile(self,outfile):
        # 写入文件
        out = open(outfile, 'wb')
        csv_writer = csv.writer(out)
        csv_writer.writerow(['date','lxclose','lx+2close','sse300close'])
        csv_writer.writerows(self.lxData)
        out.close()
        print 'writer ok'

def main(datadir,lx,sse,outfile):
    data = CodeData(lx,sse)
    if os.path.isdir(datadir):
        for root,dir,files in os.walk(datadir):
            for fi in files:
                datafile = os.path.join(root,fi)
                if os.path.isfile(datafile):
#                     print datafile
                    data.fileList.append(datafile)
#                     readcsv(datefile)
    
    else:
        print 'this is not dir'
    
    data.codefile()
    data.getsseData()
    data.findData()
    data.writerfile(outfile)
    
    
if __name__ == '__main__':
    configfile = 'D:\\workspace\\work\\lianxu_config.ini'
    config = Config(configfile)
    datadir = config.getsrcdir()
    lixFile = config.getLX()
    ssefile = config.getsse()
    outfile = config.getdst()
    
    main(datadir,lixFile,ssefile,outfile)
    print 'Complete!!!'
    
    
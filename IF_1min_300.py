# -*- coding:utf-8 -*-
'''
@author: liuyang
'''
import csv

class IFData:
    def __init__(self):
        self.iflx = []
        self.if1709 = []
        self.sse300 = []
        self.alldata = []
        
    def finddata(self):
        ifdate = ''
        iftime = ''
        lxclose = 0
        if09close = 0
        seeclose = 0
        for lx in self.iflx:
            ifdate, iftime, lxclose = lx[0], lx[1], lx[5]
            for if09 in self.if1709:
                if ifdate == if09[0] and iftime == if09[1]:
                    if09close = if09[5]
                    break
            for sse in self.sse300:
                if ifdate == sse[0] and iftime == sse[1]:
                    seeclose = sse[5]
            all = (ifdate,iftime,lxclose,if09close,seeclose)
            self.alldata.append(all)
        print self.alldata

    def writeFile(self):
        out = open(outfile, 'wb')
        csv_writer = csv.writer(out)
        csv_writer.writerows(self.alldata)
        out.close()
        print 'writer ok'

def main(lxfile,if09file,ssefile):
    data = IFData()
    f = file(lxfile)
    lines = f.readlines()
    data.iflx = strToList(lines)
    
    f2 = file(if09file)
    lines2 = f2.readlines()
    data.if1709 = strToList(lines2)
    
    f3 = file(ssefile)
    lines3 = f3.readlines()
    data.sse300 = strToList(lines3)
    
    data.finddata()
    data.writeFile()
    
def strToList(strsList):
    lists = []
    for strs in strsList:
        li = strs.split(',')
        lists.append(li)
    return lists

if __name__ == '__main__':
    iflx = 'C:\\Users\\liuyang\\Desktop\\ji\\CFFEXIFlx.txt'
    if1709 = 'C:\\Users\\liuyang\\Desktop\\ji\\CFFEXIF1709.txt'
    sse300 = 'C:\\Users\\liuyang\\Desktop\\ji\\SSE300.txt'
    outfile = 'C:\\Users\\liuyang\\Desktop\\ji\\outfile.csv'
    main(iflx,if1709,sse300)
    

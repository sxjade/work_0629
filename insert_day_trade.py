# -*- coding:utf-8 -*-

import csv
import datetime

class DayAndTrade:
    def __init__(self):
        self.day_line_data = None
        self.trade_data = None
        self.out_data = []
        
    
    def readcsv(self,csvfile):
        # 读取csv文件，返回一个列表
        outlist = []
        with open(csvfile,'rb') as csvfiler:
            readfile = csv.reader(csvfiler)
            for lin in readfile:
                outlist.append(lin)
                
        return outlist
    
    def getdatetime(self,strs):
        # 格式时间，返回一个日期
        t_day = datetime.datetime.strptime(strs,'%Y.%m.%d')
        return t_day    
    
    def formatList(self,datelist):
        # 格式化列表，将列表内所有项连接为一个字符串(盈亏单独为一项)，将此字符串为一项生成一个列表
        # "进场Long,Buy,2015/1/28,9:22:00 AM,13240,-2826.21"
        # "出场Long,Sell,2015/1/28,10:10:00 PM,12970,"
        datestr = ''
        yk = datelist[5]
        i = 0
        while i < 5:
            if datestr:
                datestr = datestr + ',' + datelist[i]
            else:
                datestr = datelist[i]
            i += 1
        list2 = [datestr,yk]
        return list2
    
    def appendOutdata(self):
        # 将day_list和trade_list分别添加到新列表内
        insert_day = None
        for lin in self.trade_data:
            type(lin)
            lin_tru = self.getdatetime(lin[2].replace('/','.'))
            if insert_day == lin_tru:  # 成交数据的时间与最后一次记录插入时间相同时，将成交列数据添加到out_data列表内
                lin2 = self.formatList(lin)
                self.out_data.append(lin2)
                continue
            while self.day_line_data:
                
                day_date = self.getdatetime(self.day_line_data[0][0])
                if day_date < lin_tru:  
                # 日线数据的日期小于成交日期时，将日期数据添加到out_data列表内，并且删除原日线列表内该项。同时记录日期，继续循环
                    print self.day_line_data[0]
                    self.out_data.append(self.day_line_data[0])
                    self.day_line_data.pop(0)
                    insert_day = day_date
                    continue
                elif day_date == lin_tru: 
                # 日线数据的日期小于成交日期时，将日期数据和成交列数据都添加到out_data列表内，并且删除原日线列表内该项。同时记录日期，调出循环
                    print self.day_line_data[0]
                    print lin
                    lin2 = self.formatList(lin)
                    
                    self.out_data.append(self.day_line_data[0])
                    self.out_data.append(lin2)
                    self.day_line_data.pop(0)
                    insert_day = day_date
                    break
                else:
                    break
            
            
    
    def writerfile(self,outfile):
        # 写入文件
        with open(outfile,'wb') as wr:
            writ = csv.writer(wr)
            writ.writerows(self.out_data)

    def main(self,dayfile,tradefile,outfile):
        self.day_line_data = self.readcsv(dayfile)
        self.trade_data =self.readcsv(tradefile)
        self.appendOutdata()
        self.writerfile(outfile)
        
    
if __name__ == '__main__':
    day_file = 'D:\\ATS_SXY\\work\\day_trade\\day-1-29999.csv'
    trade_file = 'D:\\ATS_SXY\\work\\day_trade\\trade_day2.csv'
    out_file = 'D:\\ATS_SXY\\work\\day_trade\\out.csv'
    d = DayAndTrade()
    d.main(day_file,trade_file,out_file)
    
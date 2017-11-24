# -*- coding:utf-8 -*-
'''
@author: liuyang
'''
import struct
import sqlite3

def connacc(accdb):
    cx = sqlite3.connect(accdb)
    cu = cx.cursor()
    cu.execute("select * from ACCData where date=%d " % begindate)
    rows = cu.fetchall()
    if rows != []:
        for i in rows:
            print i,len(i[1])
            xx = struct.unpack("2i",i[1])
            print xx 






if __name__ == "__main__":
    acc_file = "D:\\ATS_SXY\\tmp\\acc.db"
    begindate = 20160517
    connacc(acc_file)
    pass
# -*- coding:utf-8 -*-
'''
@author: liuyang
'''
import os
from xml.dom import minidom

class XmlDate:
    def __init__(self):
        self.namedict = {}
        
    def readxml(self,x_file):
        # 读取xml文件
        doc = minidom.parse(x_file)
        root = doc.documentElement
    
        code_nodes = root.getElementsByTagName('product')   # 获取product节点列表
        for node in code_nodes:
            tradeName = node.getAttribute('tradeName')    # tradeName="cu1609"
            
            productId = node.getAttribute('productId')    # productId="001609"
            marketId = self.getMarketId(node)
            fullname = self.getfullname(productId,marketId)  # 返回'1-1609'
            self.namedict[fullname] = tradeName
        print self.namedict
    
    def getfullname(self,productId,marketId):
        int_prod = int(productId)
        str_prod = str(int_prod)
        fullname = marketId + "-" + str_prod
        return fullname 
            
    def getMarketId(self,xml_node):
        one_fa = xml_node.parentNode
        two_fa = one_fa.parentNode
        thr_fa = two_fa.parentNode
        for_fa = thr_fa.parentNode
        marketId = for_fa.getAttribute('marketId')
        print marketId
        return marketId
        

def main(f_path):
    if os.path.isdir(f_path):
        for dir,root,csvfiles in os.walk(f_path):
            for csv_file in csvfiles:
                if os.path.splitext(csv_file)[1] == ".csv":
                    print csv_file
                    newname = formatName(csv_file)
                    if newname:
                        str_csv = os.path.join(dir,csv_file)
                        new_csv = os.path.join(dir,newname)
                        
                        os.rename(str_csv,new_csv)
                        print "%s copy to %s CSV file sucessfull." % (csv_file, new_csv)
                else:
                    print "%s is not a CSV file."%csv_file 

def formatName(filename):
    # 1min-1-99999.csv,  5min-1-99999.csv,  1day-1-99999.csv
    namelist = filename.split('.')
    k_name = namelist[0][:5]
    c_name = namelist[0][5:]
    try:    
        codename = codedic[c_name]
        newname = k_name+codename+'.csv'
        print newname
        return newname
    except:
        print "%s is too old! "
        return 
    

if __name__ == "__main__":
    filePath = "D:\\ATS_SXY\\codetable\\date\\20170629\\kline\\"
    xmlfile = "D:\ATS_SXY\codetable\Ccodetable.XML"
    x = XmlDate()
    x.readxml(xmlfile)
    codedic = x.namedict

    main(filePath)


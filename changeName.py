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
    
        code_nodes = root.getElementsByTagName('subproduct')   # 获取subproduct节点列表
        for node in code_nodes:
            tradeName = node.getAttribute('subsymbol')    # subsymbol="cu"
            
            productId = node.getAttribute('id')    # id="0"
            marketId = self.getMarketId(node)
            mid_name = self.getfullname(productId,marketId)  # 返回'1-x
            self.namedict[mid_name] = tradeName
        print self.namedict
    
    def getfullname(self,productId,marketId):
        int_prod = int(productId)
        str_prod = str(int_prod)
        if str_prod == "0":
            mid_name = marketId + "-" 
        else:
            mid_name = marketId + "-" + str_prod
        print mid_name
        return mid_name 
            
    def getMarketId(self,xml_node):
        products_node = xml_node.parentNode  #  获取父节点
        market_node = products_node.parentNode  # 获取 market 节点
        
        marketId = market_node.getAttribute('marketId')
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
    c_name = namelist[0][5:-4]
    e_name = namelist[0][-4:]
    try:    
        codename = codedic[c_name]
        newname = k_name + codename + e_name + '.csv'
        print newname
        return newname
    except:
        print "%s is too old! " % filename
        return 
    

if __name__ == "__main__":
    filePath = "D:\\ATS_SXY\\codetable\\date\\20170807\\"
    xmlfile = "D:\ATS_SXY\codetable\Ccodetable.XML"
    x = XmlDate()
    x.readxml(xmlfile)
    codedic = x.namedict

    main(filePath)
    print "The End!"


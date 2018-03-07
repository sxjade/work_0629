# -*- coding:utf-8 -*-
'''
@author: liuyang
'''
import ConfigParser
import os
import re
import time

class Myconf(ConfigParser.ConfigParser):  
    def __init__(self,defaults=None):  
        ConfigParser.ConfigParser.__init__(self,defaults=None)  
    def optionxform(self, optionstr):  
        return optionstr  

class Conf:
    def __init__(self,ini_file):
        self.ini_f = open(ini_file)
        self.config=Myconf()
        self.config.readfp(self.ini_f)
        
    def get_str_para(self,section,parameter):
        str_para = self.config.get(section,parameter)
        return str_para
    
    def get_int_para(self,section,parameter):
        int_para = self.config.getint(section,parameter)
        return int_para
        
    def get_float_para(self,section,parameter):
        float_para = self.config.getint(section,parameter)
        return float_para
    
    def get_sections(self):
        sec_list = self.config.sections()
        sec = sec_list[0]
#         print sec
        return sec
    
    def close_file(self):
        self.ini_f.close()
        



class Product_Hold:
    def __init__(self,realfile,product,strategy):
        self.filer = realfile
        self.strategy = strategy
        self.product = product
        self.conf = Conf(realfile)
        
        self.buy_hold = 0
        self.sell_hold = 0
        
    
       
    def get_hold(self):
        if self.strategy == "JUNIC1" or self.strategy == "JUNIC2":
            self.get_JUNIC1_2()
        elif self.strategy == "JUNIC5" or self.strategy == "JUNIC6":
            self.get_JUNIC5_6()
        elif self.strategy == "UNICORE2":
            self.get_UNICODE2()
        else:
            self.get_UNICODE1_3to6()
        
        
    
    def get_JUNIC1_2(self):
        sec = self.conf.get_sections()
#         print "open file"
        direct = self.conf.get_int_para(sec, "direct")
#         time.sleep(60)
        now_lots = self.conf.get_int_para(sec, "now_lots")
        
        hold = direct*now_lots
        
        self.set_hold(hold)
        
        
    
    def get_JUNIC5_6(self):
        sec = self.conf.get_sections()
        
        direct = self.conf.get_int_para(sec, "direct")
        addnum = self.conf.get_int_para(sec, "addnum")
        day_lots = self.conf.get_int_para(sec, "DAY_LOTS")
        
        hold = addnum*day_lots*direct
        
        self.set_hold(hold)
            
        
    
    def get_UNICODE1_3to6(self):
        sec = self.conf.get_sections()
        
        actual_lots = self.conf.get_int_para(sec, "ACTUAL_LOTS")
        day_lots = self.conf.get_int_para(sec, "DAY_LOTS")
        
        hold = actual_lots*day_lots
        
        self.set_hold(hold)
        
        
    
    def get_UNICODE2(self):
        sec = self.conf.get_sections()
        
        direct = self.conf.get_int_para(sec, "TPB_DIRECT")
        lots = self.conf.get_int_para(sec, "TPB_LOTS")
        
        if direct == 0:
            hold = lots
        elif direct == 1:
            hold = lots*(-1)
        else:
            hold = 0
        
        self.set_hold(hold)
        
        
    
    def get_buy(self):
        return self.buy_hold
    
    def get_sell(self):
        return self.sell_hold
    
    def set_hold(self,holdnum):
        if holdnum > 0:
            self.buy_hold = holdnum
#             print "buyhold \n"
        elif holdnum < 0:
            self.sell_hold = holdnum
#             print "sellhold \n"
        

    
    def close_file(self):
        self.conf.close_file()
        
    
    def __unicode__(self):
        return self.filer


def read_dir(dirs):
    real_list = []
    real_dict = {}
    
    if os.path.isdir(dirs):
        for (root, dirs, files) in os.walk(dirs):
            for f in files:
                if f.startswith("Real"):
                    codefile = os.path.join(root,f)
                    real_list.append(codefile)
#     print real_list
    for i in real_list:
        filename_list = i.split("_")
        (prod,stra) = filename_list[-3],filename_list[-1]
        
#         print prod,stra
        product = Product_Hold(i,prod,stra)
        product.get_hold()
        product.close_file()
        if real_dict.has_key(prod):
            real_dict[prod].append(product)
        else:
            real_dict[prod] = []
            real_dict[prod].append(product)
#     print real_dict
    return real_dict


                

def statistics(st_dir):
    dicts = read_dir(st_dir)
    sum_dict = {}
    for key in dicts:
#         print key
        if len(dicts[key]) > 0:
#             print len(dicts[key])
            for i in dicts[key]:
                buy = i.get_buy()
                sell = i.get_sell()
                
                if key in sum_dict:
#                     print sum_dict
                    buy2 = sum_dict[key]["buy"] + buy
                    sell2 = sum_dict[key]["sell"] + sell
                    sum_dict[key].update({"buy":buy2})
                    sum_dict[key].update({"sell":sell2})
                    
                else:
#                     print sum_dict
                    sum_dict.update({key:{"buy":buy,"sell":sell}})
    print " %s hold is :\n" % st_dir               
    print sum_dict
    
def main(dir1,dir2):
    statistics(dir1)
    statistics(dir2)


if __name__ == "__main__":
    dir_60 = "C:\\Users\\admin\\Desktop\\BI_UNICORE_15208260\\users\\ATSJY\\"
    dir_79 = "C:\\Users\\admin\\Desktop\\BI_UNICORE_15208279\\users\\ATSJY\\"
    main(dir_60,dir_79)
    


# -*- coding:utf-8 -*-
'''
@author: liuyang
'''
import sys
import ConfigParser
import os
import re
import time
import logging

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='checkhold.log',
                filemode='a+')


class Myconf(ConfigParser.ConfigParser):  
    def __init__(self,defaults=None):  
        ConfigParser.ConfigParser.__init__(self,defaults=None)  
    def optionxform(self, optionstr):  
        return optionstr  

class Conf:
    def __init__(self,ini_file):
        self.inier = ini_file
        self.config=Myconf()
        try:
            self.ini_f = open(ini_file)
            self.config.readfp(self.ini_f)
        except:
            sys.exit(1)
        
    def get_str_para(self,section,parameter):
        str_para = self.config.get(section,parameter)
        return str_para
    
    def get_int_para(self,section,parameter):
        
        int_para = self.config.getint(section,parameter)
        if parameter == "DAY_LOTS" and int_para <> 1:
            print "warning: %s : DAY_LOTS is : %d" % (self.inier,int_para)
            logging.warning("%s : DAY_LOTS is : %d" % (self.inier,int_para))
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
    
    def get_product(self):
        return self.product
        
    def get_file(self):
        (filepath,filename) = os.path.split(self.filer)
        return filename
        pass
       
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
        if filename_list[-2] == "BAK":
            pd_str = filename_list[1]
            (prod,stra) = pd_str[-2:]+"_BAK",filename_list[-1]
            (prod,stra) = filename_list[0],filename_list[-1]
        else:
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

def holdOrNo(prod_list):
    hold_list = []
    nohold_list = []
    prod = ""
    hold_str = ''
    
    if len(prod_list) > 0:
        for i in prod_list:
            file_str = i.get_file()
            prod = i.get_product()
            buy = i.get_buy()
            sell = i.get_sell()
             
            if buy == 0 and sell == 0:
                nohold_list.append(file_str)
            else:
                hold_list.append(file_str)
                hold_str = hold_str + "\n" + file_str + ": " + " buy= " + str(buy) + " sell= " + str(sell)
    
    
    logging.info("%s no hold is %s " % (prod,nohold_list))
    logging.info("%s hold is :  %s \n" % (prod,hold_str))
                

def statistics(st_dir):
    dicts = read_dir(st_dir)
    sum_dict = {}
    
    for key in dicts:
#         print key
        if len(dicts[key]) > 0:
            holdOrNo(dicts[key])
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
    print "\n %s hold is : " % st_dir     
    for v,k in sum_dict.items():
        print('{v}:{k}'.format(v = v, k = k))
        logging.info('{v}:{k}'.format(v = v, k = k))          
#     print sum_dict
    
def main(hold_dirs):
    if len(hold_dirs) > 0:
        for i in hold_dirs:
            statistics(i)
    
    


if __name__ == "__main__":
    
    dirs_test = ["d:\\workspace\\work\\ATSJY\\"]
    dirs = ["C:\\Users\\admin\\Desktop\\BI_UNICORE_15208279\\users\\ATSJY\\",
            "C:\\Users\\admin\\Desktop\\5208260-ag-al-hc-i-ni\\users\\ATSJY\\",
            "C:\\Users\\admin\\Desktop\\5208260-rb-ru-v-zn\\users\\ATSJY\\"]
    main(dirs_test)
    


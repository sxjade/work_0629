# -*- coding:utf-8 -*-
'''
@author: liuyang
'''
import random

'''
猜数字游戏，程序随机生成一个0-9组成的非重复四位数字，用户有10次机会。
每猜一次程序给出猜正确率，A为数字正确且位置正确，B为数字正确位置错误。
例如：2A1B  表示：
所猜数字有两个是数字正确位置正确，1个为数字正确位置错误，还有一个数字为错误
'''

class GuessNumber:
    
    MAX_TIMES = 10
    WIN_GUESS = '4A0B'
    
    def __init__(self):
        self.numberList = ['1','2','3','4','5','6','7','8','9','0']
        self.randomNumber = []
        self.times = 0
        self.guessNumList = []
        self.guessA = 0
        self.guessB = 0
        
        
    def setrandomNumber(self):
    	  # 随机生成4为数字列表，无返回值
        self.randomNumber = random.sample(self.numberList, 4)
        #print self.randomNumber,type(self.randomNumber)

    def getResult(self):
    	  # 获取猜测结果，返回字符串
        guess_str = str(self.guessA) + 'A' + str(self.guessB) + 'B'
        return guess_str

    def guess(self):
        while self.times < self.MAX_TIMES :
            if self.getResult() <> self.WIN_GUESS:
                if self.times <> 0:
                    print self.getResult()
            else:
                print 'Congratulations! you are Win.'
                break
            
            input_N = raw_input("raw_input: ")
            if input_N.isdigit() and len(input_N) == 4:
                self.guessNumList = list(input_N)
                self.matchNum()
                self.times += 1
            else:
                print 'input error! please again.'
        
        if self.getResult() <> self.WIN_GUESS:
            
            print 'Lose, times out! \n'
            print 'The number is %s' % self.randomNumber
            
        

    def matchNum(self):
        guessA = 0
        guessB = 0
        for i in range(len(self.randomNumber)):
            for j in range(len(self.guessNumList)):
                if self.randomNumber[i] == self.guessNumList[j] :
                    if i == j:
                        guessA += 1
                    else:
                        guessB += 1
                    
                    
        self.guessA = guessA
        self.guessB = guessB
                    
    def againOrNot(self):
        print 'Are you want again? ( y  or n) \n'
        input_Again = raw_input("raw_input: ")
        if input_Again == 'y':
            self.setrandomNumber()
            self.times = 0
            return True
        else :
            print 'bye!!!'
            return False




def main():
    num = GuessNumber()
    num.setrandomNumber()
    num.guess()
    if num.againOrNot():
        num.guess()

if __name__ == '__main__':
    main()
    

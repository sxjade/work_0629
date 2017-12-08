# -*- coding:utf-8 -*-
'''
@author: liuyang
'''
import random

'''
��������Ϸ�������������һ��0-9��ɵķ��ظ���λ���֣��û���10�λ��ᡣ
ÿ��һ�γ����������ȷ�ʣ�AΪ������ȷ��λ����ȷ��BΪ������ȷλ�ô���
���磺2A1B  ��ʾ��
����������������������ȷλ����ȷ��1��Ϊ������ȷλ�ô��󣬻���һ������Ϊ����
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
    	  # �������4Ϊ�����б��޷���ֵ
        self.randomNumber = random.sample(self.numberList, 4)
        #print self.randomNumber,type(self.randomNumber)

    def getResult(self):
    	  # ��ȡ�²����������ַ���
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
    

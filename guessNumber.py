# -*- coding:utf-8 -*-
'''
@author: liuyang
'''
import random


class GuessNumber:
    
    Max_times = 5
    Win_guess = '4A0B'
    
    def __init__(self):
        self.numberList = ['1','2','3','4','5','6','7','8','9','0']
        self.randomNumber = []
        self.times = 0
        self.guessNumList = []
        self.guessA = 0
        self.guessB = 0
        
        
    def setrandomNumber(self):
        self.randomNumber = random.sample(self.numberList, 4)
        print self.randomNumber,type(self.randomNumber)

    def guess(self):
        while self.times < self.Max_times :
            if self.getResult() <> self.Win_guess:
                if self.times <> 0:
                    print self.getResult()
            else:
                print 'Congratulations! you are Win.'
                return True
            
            input_N = raw_input("raw_input: ")
            if input_N.isdigit() and len(input_N) == 4:
                self.guessNumList = list(input_N)
                self.matchNum()
                self.times += 1
            else:
                print 'input error! please again.'
        
        if self.getResult() <> self.Win_guess:
            
            print 'Lose, times out! '
            print 'The number is %s' % self.randomNumber
            return False
        

    def matchNum(self):
        self.guessA = 0
        self.guessB = 0
        for i in range(len(self.randomNumber)):
            for j in range(len(self.guessNumList)):
                if self.randomNumber[i] == self.guessNumList[j] and i == j:
                    self.guessA += 1
                elif self.randomNumber[i] == self.guessNumList[j] and i <> j:
                    self.guessB += 1
                    
                    
    def getResult(self):
        guess_str = str(self.guessA) + 'A' + str(self.guessB) + 'B'
        return guess_str




def main():
    num = GuessNumber()
    num.setrandomNumber()
    num.guess()

if __name__ == '__main__':
    main()
    

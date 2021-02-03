##imports##
from random import *
from time import *

###classes###

#board#
class Board(): #class for board
    def __init__(self, number):
        self.array = [] #attributes as chosen on UML diagram
        self.current_row = 0
        self.current_col = 0
        self.two_player = False
        self.ID = number
        for i in range(0,4):
            self.array.append(['x']*4) #create array in instantiation

    def get_array(self):
        return self.array

    def get_row(self):
        row = self.current_row
        return row

    def get_col(self):
        return self.current_col

    def set_current_space(self, x, y):
        self.current_row = x
        self.current_col = y

    def set_array(self, right):
        if right == True:
            self.array[self.current_row][self.current_col] = 'O'
        elif right == False:
            self.array[self.current_row][self.current_col] = 'N'

    def check_free(self):
        available = True
        if self.array[self.current_row][self.current_col] == 'N' or self.array[self.current_row][self.current_col] == 'O':
            available = False
        return available

    def check_winnable(self):
        Ns = 0
        winnable = True
        #for extensibility, this can be modified to check if each row has both an N and and O in it, which will indicate that neither of the two players can win
        if self.array[0][0] == 'N' or self.array[1][1] == 'N' or self.array[2][2] == 'N' or self.array[3][3] == 'N':
            Ns +=1
        if self.array[0][3] == 'N' or self.array[1][2] == 'N' or self.array[2][1] == 'N' or self.array[3][0] == 'N':
            Ns +=1
        for i in range(0,4):
            if self.array[i][0] == 'N' or self.array[i][1] == 'N' or self.array[i][2] == 'N' or self.array[i][3] == 'N':
                Ns +=1
            if self.array[0][i] == 'N' or self.array[1][i] == 'N' or self.array[2][i] == 'N' or self.array[3][i] == 'N':
                Ns +=1
        if Ns >=10:
            winnable = False
        return winnable
            
    def check_won(self):
        won = False
        symbol = 'O'
        winner = ""
        for k in range (0,2):
            if (self.array[0][0] == symbol and self.array[1][1] == symbol and self.array[2][2] == symbol and self.array[3][3] == symbol) or (
                self.array[0][3] == symbol and self.array[1][2] == symbol and self.array[2][1] == symbol and self.array[3][0] == symbol):
                won = True
                if k == 0:
                    winner = 'player'
                else:
                    winner = 'opponent'
            for i in range(0,4):
                if self.array[i][0] == symbol and self.array[i][1] ==symbol and self.array[i][2] == symbol and self.array[i][3] == symbol:
                     won = True
                     if k == 0:
                         winner = 'player'
                     else:
                         winner = 'opponent'
                elif self.array[0][i] == symbol and self.array[1][i] == symbol and self.array[2][i] == symbol and self.array[3][i] == symbol:
                    won = True
                    if k == 0:
                        winner = 'player'
                    else:
                        winner = 'opponent'
            symbol = 'N'
        return won, winner

    def reset_board(self):
        self.array = []
        for i in range(0,4):
            self.array.append(['x']*4)

#player#
class Player():
    def __init__(self,name):
        self.name = name
        self.points = 0
        self.level = 0
        self.correct = False

    def get_name(self):
        return self.name

    def set_points(self, points_earned):
        self.points += points_earned

    def get_points(self):
        return self.points

    def set_correct(self, correct):
        self.correct = correct

    def get_correct(self):
        return self.correct

    def get_level(self):
        return self.level

    def set_level(self, increment):
        self.level = self.level + increment

#question#
class Question():
    def __init__(self, operator, level):
        self.operator = operator
        self.question = ""
        self.level = level
        self.x = 0
        self.y = 0

    def set_question(self, level):
        if self.operator == "÷":
            divisible = False
            while not divisible:
                if level <= 1:
                    self.x = randint(1,50) #good part to talk about
                    self.y = randint(1,12)
                elif level == 2 or level == 3:
                    self.x = randint(1,130)
                    self.y = randint(5,20)
                elif level == 4 or level == 5:
                    self.x = randint(75,250)
                    self.y = randint(10,75)
                elif level>= 6:
                    self.x = randint(100,500)
                    self.y = randint(15,100)
                if self.x%self.y == 0:
                        divisible = True
        else:
            if level <= 1:
                self.x = randint(1,12)
                self.y = randint(1,12)
            elif level == 2 or level == 3:
                self.x = randint(20,50)
                self.y = randint(20,50)
            elif level == 4 or level == 5:
                self.x = randint(50,100)
                self.y = randint(50,100)
            elif level >= 6:
                self.x = randint(100,500)
                self.y = randint(100,500)
        self.question = "What is {} {} {}?: ".format(self.x, self.operator, self.y)

    def get_question(self):
        return self.question

    def check_question(self, value):
        correct = False
        if self.operator == "+":
            if value == self.x + self.y:
                correct = True
        elif self.operator == "-":
            if value == self.x - self.y:
                correct = True
        elif self.operator == "x":
            if value == self.x * self.y:
                correct = True
        elif self.operator == "÷":
            if value == self.x / self.y:
                correct=True
        return correct
        
        

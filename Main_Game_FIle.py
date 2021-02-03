#-> link up database
#CHECK NOTES ON PAPER

##imports##
from random import *
from time import *
from math import *
from Class_Structure import Board, Player, Question
from guizero import App, Text, Waffle, TextBox, PushButton, Window
global player, board, add, minus, times, mod
global correct,button_clicked
    
##Functions##
def show_instructions():
    Rules.show()

def hide_instructions():
    Rules.hide()

def set_up():
    Login.hide()
    global player,board,add,minus,times,mod
    player=Player(LoginTextBox.value)
    board = Board(1)
    add = Question('+',0)
    minus = Question('-',1)
    times = Question('x',2)
    mod = Question('÷',3)

def choose_space(x,y):
    global button_clicked
    button_clicked = 0
    board.set_current_space(x,y)
    available = board.check_free()
    if available:
        question()
    else:
        rejection()

def rejection():
    Rejection.show()

def hide_rejection():
    Rejection.hide()

def question():
    if board.get_row() == 0:
        add.set_question(player.get_level())
        question = add.get_question()
    elif board.get_row() == 1:
        minus.set_question(player.get_level())
        question = minus.get_question()   
    elif board.get_row() == 2: 
        times.set_question(player.get_level())
        question = times.get_question()
    else:
        mod.set_question(player.get_level())
        question = mod.get_question()
    QuestionText.value = question
    QuestionTextBox.value = "" #clears textbox
    AskQuestion.show()

def check_answer():
    global button_clicked
    button_clicked = button_clicked+1 #incremenets button_clicked to count how many times this subprogram has been called
    number = QuestionTextBox.value 
    if number.isdigit() or (number[0] == "-" and number[1:].isdigit()): #validates input
        correct = False
        AskQuestion.hide() #hides window
        if board.get_row() == 0: #checks which object needs to be used to check the answer
            correct = add.check_question(int(number)) #must convert to integer as input is a string
        elif board.get_row() == 1:
            correct = minus.check_question(int(number))
        elif board.get_row() == 2:
            correct = times.check_question(int(number))
        else:
            correct = mod.check_question(int(number))
        player.set_correct(correct) #changes whether the player's most recent answer was correct
        if correct:
            Correct.show() #shows congratulatory window
            player.set_level(1) #changes player's level to be higher
        else:
            Incorrect.show() 
            player.set_level(-1)
    else:
        if button_clicked == 1: #checks how many times the button has been clicked
            update = ("Please ensure that you enter a number in response! \n"+QuestionText.value) #adds message but keeps question
            QuestionText.value = update
        elif button_clicked == 2:
            update = ("Let's try that again!\n"+QuestionText.value)
            QuestionText.value = update
            
def correct_hide():
    Correct.hide()
    update()              #both of these close the window and then call update()

def incorrect_hide():
    Incorrect.hide()
    update()

def update():
    board.set_array(player.get_correct()) #changes the array to reflect whether the player or opponent now has that space
    if player.get_correct():
        Waffle[board.get_row(),board.get_col()].color = "white" #pixel in waffle is changed to be white if player is correct
        if player.get_level == 0 or player.get_level == 1: #checks what level the player is working at
            player.set_points(1) #at only 0 or 1, they earn only one point
        elif player.get_level()%2 == 0: #has a rule for if the level is even
            points = (player.get_level()-log2(player.get_level())) 
            player.set_points(points)
        elif player.get_level()%2 == 1: #has a rule for if the level is odd
            points = (player.get_level()-((player.get_level()-1)/2)) 
            player.set_points(points)
    else:
        Waffle[board.get_row(),board.get_col()].color = "pink" #pixel in waffle is changed to be pink is player is incorrect
    ScoreText.value = str(int(player.get_points())) #updates the score in corner
    check_winning() #calls check_winning subprogram

def check_winning():
    won = False
    won, winner = board.check_won()
    if won and winner == 'player':
        end_game()
    elif won and winner == 'opponent':
       end_game_lost()
    if not board.check_winnable() and not won:
        end_game_draw()

def end_game():
    WonText.value = ("Well Done "+player.get_name()+"! You won the game!")
    WonScore.value = ("You got "+str(int(player.get_points()))+" points!")
    Won.show()

def end_game_lost():
    WonText.value = ("Sorry "+player.get_name()+", you were beaten by the computer!")
    WonScore.value = ("Don't be discouraged though! You got "+str(int(player.get_points()))+" points!")
    Won.show()

def end_game_draw():
    WonText.value = ("Sorry "+player.get_name()+" you are no longer able to win this game!")
    WonScore.value = ("We'll call that a draw! You got "+str(int(player.get_points()))+" points still!")
    Won.show()
    
def end_app():
    app.destroy()

def restart_game():
    board.reset_board()
    Won.hide()
    for i in range(0,4):
        for j in range(0,4):
            Waffle[i,j].color="light blue"
    player.set_points(0-player.get_points())
    ScoreText.value = str(int(player.get_points()))
    player.set_level(0-player.get_level())

#APP#

#main app#
app = App(title='Main Game', bg='light pink', height='1000', width='2000', layout="grid")
AppTitle = Text(app, text="GAME",grid=[1,0])
ScoreText = Text(app, text="0",grid=[2,0])
LeftImage = Text(app,text="an image should go here",grid=[0,1])
RightImage = Text(app,text="an image should go here",grid=[2,1])
Waffle = Waffle(app, color="light blue",height=4, width=4, dim=150, command=choose_space, grid=[1,1])
InstructionsButton = PushButton(app,grid=[1,2],text="Instructions",command=show_instructions)

#login#
Login = Window(app, bg = 'light pink', height = '200', visible = True)
LoginTitle = Text(Login, text="LOGIN!")
LoginQuestion = Text(Login, text="What is your name?")
LoginTextBox = TextBox(Login)
LoginButton = PushButton(Login, text="Go!",command=set_up)

#instructions#
Rules = Window(app, bg='light pink', height = '400', visible = False)
RulesTitle = Text(Rules, text='RULES')
RulesText = Text(Rules,text='This is essentially a game of connect four!')
RulesButton = PushButton(Rules, text="CLOSE",command=hide_instructions)

#rejection#
Rejection = Window(app, height = "200", bg='light pink', visible = False)
RejectionText = Text(Rejection, text="You've already chosen this space! Please choose a different one!")
RejectionButton = PushButton(Rejection, text="Go Back to Game",command=hide_rejection)

#question#
AskQuestion = Window(app, height = "200", bg='light pink', visible = False)
QuestionText = Text(AskQuestion, text="")
QuestionTextBox = TextBox(AskQuestion)
QuestionButton = PushButton(AskQuestion, text="Enter",command=check_answer)

#correct#
Correct = Window(app, bg = "light pink", height = "200", visible = False)
CorrectText = Text(Correct, text = "Well Done! That's right!")
CorrectButton = PushButton(Correct, text="Continue",command=correct_hide)

#incorrect#
Incorrect = Window(app, bg = "light pink", height = "200", visible = False)
IncorrectText = Text(Incorrect, text = "Sorry, that wasn't right!") #i'd like to be able to add the correct answer here
IncorrectButton = PushButton(Incorrect, text="Continue",command=incorrect_hide)

#won#
Won = Window(app, bg="light pink", height = "150", visible = False)
WonText = Text(Won, text = "")
WonScore = Text(Won, text = "")
WonButton = PushButton(Won, text="Finish!", command=end_app)
WonButtonAgain = PushButton(Won, text="Start Again!",command=restart_game)


# import modules for pygame and random 
from fileinput import close
from multiprocessing.sharedctypes import Value
from operator import truediv
import time
import pygame
import random
from tkinter import *
from tkinter import messagebox
from tkinter import *
from tkinter import messagebox

#creates the window for the game; sets up the environment
root = Tk()
#titles the window and sets up the size of the window
root.title("Snake Game Instructions")
root.geometry("755x200")

#prints out the pop-up for the instructions; uses tkinter
myLabel = Label(text= "Instructions", font='Stencil 18 bold' )
myLabel.grid(row= 0, column= 0)
#prints out the instructions onto different lines
line_1 = Label(root, text= "Welcome to the snake game!", font=28)
line_2 = Label(root, text= "The goal of the game is for the snake(the yellow square), to eat as many apples as possible(the red squares),", font=28)
line_3 = Label(root, text= "without touching itself or the sides of the screen!", font=28)
line_4 = Label(root, text= "To move the snake use the arrows keys, the arrows correspond to the direction the snake will move", font=28)
line_1.grid(row= 1, column= 0)
line_2.grid(row= 3, column= 0)
line_3.grid(row= 4, column= 0)
line_4.grid(row=4, column=0)
#creates a button that when clicked, closes the instructions and goes to the game
exit_button = Button(root, text="Play", font='Times 25', command=root.destroy)
exit_button.grid(row=6, column=0)

#loops the program
root.mainloop()


# initate the font and display module 
pygame.init()
 
# #assigns correct values to the colors
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (0, 0, 128)

#sets default height and width for game screen; assigns values to display width & height
width = 800
height = 600

#sets-up display for the game
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game: by The Preston Snakes")
 
#keeps track on in-game time; important for snake speed
clock = pygame.time.Clock()

#snake char is the size of the each individual block of the snake
snake_char = 10
# how fast the snake moves
movement = 15

# assign a font to the score 
score_font = pygame.font.SysFont("comicsansms", 20)
message_font = pygame.font.SysFont("comicsansms", 20)


# define the score function and parameters
def game_score(score):
#display the score font
    value = score_font.render("Your Score: " + str(score), True, white)
# blits the display to the screen
    win.blit(value, [0, 0])

#creates a function to keep track of the users high score, even when the game is closed
def high_score(score):
  #stores the users highscore in a .txt file
  file = open("HighScore.txt", "w")
  file.write(str(score))
  #renders and prints out the high score to the screen
  high_value = score_font.render("High Score: " + str(score), True, white)
  win.blit(high_value, [650, 0] )


# define the function for the snake and its paramaeters 
def our_snake(snake_char, snake_body):
    for x in snake_body:
# draws the rectangle, which will be used as our snake
        pygame.draw.rect(win, yellow, [x[0], x[1], snake_char, snake_char])

#creates function to define popup text
def popup(message, color):
  #renders the message and sets the location of the text on the screen
  text = message_font.render(message, True, color)
  win.blit(text, [width / 8 , height / 3])


#functions for when there is not a high score
def is_highscore_empty():
  #opens and reads the file where the score should be stored
  file = open("HighScore.txt", "r+")
  check = file.read()
  #checks to see if there are no integer values in the file
  try:
    int(check)
    pass
  #if none, writes in a 0
  except:
    file.write("0")

#calls on functions to check if high score exists
is_highscore_empty()

#functions for the game
def game():
  #sets run to true
  run = True 
  close_screen = False
  #assigns value to variables x1 and y1
  x1 = width / 2
  y1 = height / 2
 
  x1_change = 0
  y1_change = 0
 
  snake_body = [] # initlialize a list
  snake_size = 1 # inital length of the snake 

  # causes the food to generate in random places across the video game screen
  food1 = round(random.randrange(0, width - snake_char) / 10.0) * 10.0
  food2 = round(random.randrange(0, height - snake_char) / 10.0) * 10.0
  pygame.mixer.music.load('music.wav')
  pygame.mixer.music.play(-1)
  # if the user presses the exit button on the top left; run becomes false and game ends
  while run == True:
    #when the user loses in the game, redirects them to a gameover screen
    while close_screen == True:
      win.fill(white)
      popup("You Lost! Press Space to Play Again, or Press Backspace to Quit", red)
      pygame.display.update()
      for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
          #if user presses the backspace, the game closes
          if event.key == pygame.K_BACKSPACE:
            run = False
            close_screen = False
          #if user presses spacebar, the game starts again
          if event.key == pygame.K_SPACE:
            game()
        #if user presses the quit icon, the game closes
        elif event.type == pygame.QUIT:
          run = False
          close_screen = False
    #if the user clicks the quit icon, even when not in the gameover screen, the game closes
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        run = False
  #if the player presses down on the left key, the snake will move left
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
          x1_change = -snake_char
          y1_change = 0
      # if the player presses down on the right arrow key, the snake will move right
        elif event.key == pygame.K_RIGHT:
          x1_change = snake_char
          y1_change = 0
      # if the player presses down on the upper arrow key, the snake will move up
        elif event.key == pygame.K_UP:
          y1_change = -snake_char
          x1_change = 0
      # if the player presses down on the down arrow key, the snake will move down
        elif event.key == pygame.K_DOWN:
          y1_change = snake_char
          x1_change = 0
    
    # if the value of y exceeds the height of the window (goes down too far); or if it goes lower than 0 (goes up too high), then the boundaries will activate and the game is over 
    if x1 >= width or x1 < 0 or y1 >= height or y1 < 0:
      close_screen = True
        
    x1 += x1_change
    y1 += y1_change

    #sets the window colour to black
    win.fill(black)
    pygame.draw.rect(win, red, [food1, food2, snake_char, snake_char])
    # initiialzes a list for the rectangle (which is the snake's head)
    snake_top = []

    # if the snake eats the food, it appends the block to the end of its body  
    snake_top.append(x1)
    snake_top.append(y1)
    snake_body.append(snake_top)

    if len(snake_body) > snake_size:
      del snake_body[0]

  #if the snake touches itself, the game ends
    for x in snake_body[:-1]:
      if x == snake_top:
        close_screen = True

  # calls and tests the function
    our_snake(snake_char, snake_body)
  # it will display the length of the snake subtracted by 1 because 1 block it is the initial size of the snake
    score = (snake_size - 1)
    #sets the value of the game score displays, to the score of how many times the snake ate food
    game_score(score)
    high_score(is_highscore(score))
  # updates the display of the game 
    pygame.display.update()
  
  # check for a collision with the food. if the snake collides with the food, it moves it to a random spot on the game screen
    if x1 == food1 and y1 == food2:
      food1 = round(random.randrange(0, width - snake_char) / 10.0) * 10.0
      food2 = round(random.randrange(0, height - snake_char) / 10.0) * 10.0
  # increases the score 
      snake_size += 1 

    clock.tick(movement)

#creates a function to overwrite the high score when the player sets a new high score
def is_highscore(score):
  #opens the .txt file where the score is stored
  file = open("HighScore.txt", "r+")
  filescore = file.read()
  #if the current score is higher than the saved high score, the score will be overwritten for the new score
  if int(score) > int(filescore):
    file.truncate(0)
    file.write(str(score))
    return score
  else:
    return filescore

#function to call on and start the game
game()
# ---------------------------- #
#       Fleet Battle AI        #
# Written by Mohammad Tomaraei #
# ---------------------------- #

from PIL import Image, ImageDraw, ImageGrab
from os import system, name 
from time import sleep
import win32gui, win32api, win32con, random

# Define the rectangular screen region corresponding to the phone screen
phone_x_1, phone_y_1, phone_x_2, phone_y_2 = 479,24,823,768

# Define the main square coordinates and its length
square_x, square_y, square_length = 15, 397, 313

# Alphabet array
alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']

# Perform a click at a given screen position
def click(x,y, board):
  x_coordinate = board[(x,y)][1]
  y_coordinate = board[(x,y)][2]
  for _ in range(2):
    win32api.SetCursorPos((x_coordinate,y_coordinate))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x_coordinate,y_coordinate,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x_coordinate,y_coordinate,0,0)
    sleep(1)

# Clear the terminal
def clear(): 
  _ = system('cls')

# Check for user's turn
def checkturn(img):
  # It's our turn when enemy_fleet_color = [>100, >100, >100]
  # The word "fleet" happens to be at the position 132,274 only when it's the player's turn
  enemy_fleet_color = img.getpixel((132,274))
  if enemy_fleet_color[0] > 100 and enemy_fleet_color[1] > 100 and enemy_fleet_color[2] > 100:
    return True
  else:
    return False

# Scan the board into an array
# 0 = empty, 1 = missed, 2 = hit
def getboard(img):
  board = {}
  squareimg = img.crop((square_x, square_y, (square_x+square_length), (square_y+square_length-1)))
  for y in range(0, 10):
    for x in range(0, 10):
      x_pix = 15+x+(30*x)
      y_pix = 15+y+(30*y)
      x_coordinate = 479+square_x+x_pix
      y_coordinate = 24+square_y+y_pix
      rgb_im = squareimg.convert('RGB')
      coordinate_color = rgb_im.getpixel((x_pix,y_pix)) # 0 = r, 1 = g, 2 = b
      square_status = 0 # By default, a square is considered empty
      if coordinate_color[2] < 50:
        square_status = 2 # If the color is red, it's been hit
      elif coordinate_color[0] > 70 and coordinate_color[1] > 70 and coordinate_color[2] > 70:
        square_status = 1 # If the color is white / gray, it's a missed square
      board[x+1, y+1] = [square_status, x_coordinate, y_coordinate]
      #draw = ImageDraw.Draw(squareimg)
      #draw.rectangle([(x_pix,y_pix),(x_pix+1,y_pix+1)])
  #squareimg.show()
  return board

# Draw a 2D representation of the board
def drawboard(board):
  drawn_board = ""
  for square in board:
    drawn_board += str(board[square][0]).replace("0", "-").replace("1", "X").replace("2","*") + " "
    if square[0] == 10:
      drawn_board += "\n"
  return drawn_board

# Check if an array contains an index
def checkifindexexists(index, array):
  try:
    array[index]
  except (KeyError, IndexError):
      return False
  return True
# Find the last hit square and hit the squares around it, otherwise return False
def findlasthit(board):
  success = 0
  for square in board:
    if board[square][0] == 2:
      # We have found a hit square, now check and hit the square above, below, left, and right of it
      #print("Last hit:", alphabet[square[0]-1], square[1])
      square_above = (square[0], square[1]-1)
      square_below = (square[0], square[1]+1)
      square_left = (square[0]-1, square[1])
      square_right = (square[0]+1, square[1])
      if checkifindexexists(square_above, board) and board[square_above][0] == 0:
        success = 1
        print("[FLH] Clicking on:", alphabet[square_above[0]-1], square_above[1])
        click(square_above[0], square_above[1], board)
        break
      elif checkifindexexists(square_below, board) and board[square_below][0] == 0:
        success = 1
        print("[FLH] Clicking on:", alphabet[square_below[0]-1], square_below[1])
        click(square_below[0], square_below[1], board)
        break
      elif checkifindexexists(square_left, board) and board[square_left][0] == 0:
        success = 1
        print("[FLH] Clicking on:", alphabet[square_left[0]-1], square_left[1])
        click(square_left[0], square_left[1], board)
        break
      elif checkifindexexists(square_right, board) and board[square_right][0] == 0:
        success = 1
        print("[FLH] Clicking on:", alphabet[square_right[0]-1], square_right[1])
        click(square_right[0], square_right[1], board)
        break
  if success == 0:
    hitrandom(board)
  
# Hit a random empty square
def hitrandom(board):
  while True:
    random_x = random.randint(1,10)
    random_y = random.randint(1,10)
    if board[(random_x, random_y)][0] == 0:
      print("[RH] Clicking on:", alphabet[random_x-1], random_y)
      click(random_x, random_y, board)
      break

def AI():
  # Capture the phone screen
  phone_img = ImageGrab.grab(bbox=(phone_x_1,phone_y_1,phone_x_2,phone_y_2))
  
  # Wait for user's turn
  if checkturn(phone_img):
    #print(getboard(phone_img))
    clear()
    board_array = getboard(phone_img)
    #hitrandom(board_array)
    if findlasthit(board_array) == False:
      hitrandom(board_array)
    print(drawboard(board_array))
  
# Run the program
while 1:
    AI()
    sleep(3)

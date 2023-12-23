import sys

import pygame

from Board import Board

import math

import random

# from Sudoku_Generatorudoku_generator import SudokuGenerator
# from Cell import Cell

SIZE = HEIGHT, WIDTH = 600, 600
TITLE_FONT = 70
CROSS_COLOR = (0, 0, 0)
BG_COLOR = (255, 255, 245)

pygame.init()
pygame.display.set_caption('Sudoku')
screen = pygame.display.set_mode((SIZE))

title_font = pygame.font.SysFont("times new roman", 70, (255, 255, 245))
label_font = pygame.font.SysFont("times new roman", 32, (255, 255, 245))

"""
This was adapted from a GeeksforGeeks article "Program for Sudoku Generator" by Aarti_Rathi and Ankur Trisal
https://www.geeksforgeeks.org/program-sudoku-generator/

"""

########################
#
#   Sudoku Generator
#
########################

class SudokuGenerator:
    '''
  create a sudoku board - initialize class variables and set up the 2D board
  This should initialize:
  self.row_length		- the length of each row
  self.removed_cells	- the total number of cells to be removed
  self.board			- a 2D list of ints to represent the board
  self.box_length		- the square root of row_length

  Parameters:
    row_length is the number of rows/columns of the board (always 9 for this project)
    removed_cells is an integer value - the number of cells to be removed

  Return:
  None
    '''

    def __init__(self, row_length, removed_cells):
        self.row_length = row_length
        self.removed_cells = removed_cells
        self.board = [[0 for i in range(row_length)] for j in range(row_length)]
        self.box_length = int(math.sqrt(row_length))
        return

    '''
  Returns a 2D python list of numbers which represents the board

  Parameters: None
  Return: list[list]
    '''

    def get_board(self):
        return self.board

    '''
  Displays the board to the console
    This is not strictly required, but it may be useful for debugging purposes

  Parameters: None
  Return: None
    '''

    def print_board(self):
        print(self.board)

    '''
  Determines if num is contained in the specified row (horizontal) of the board
    If num is already in the specified row, return False. Otherwise, return True

  Parameters:
  row is the index of the row we are checking
  num is the value we are looking for in the row

  Return: boolean
    '''

    def valid_in_row(self, row, num):
        if num in self.board[row]:
            return False
        else:
            return True

    '''
  Determines if num is contained in the specified column (vertical) of the board
    If num is already in the specified col, return False. Otherwise, return True

  Parameters:
  col is the index of the column we are checking
  num is the value we are looking for in the column

  Return: boolean
    '''

    def valid_in_col(self, col, num):
        for row in range(self.row_length):
            if self.board[row][col] == num:
                return False
        return True

        ''' Determines if num is contained in the 3x3 box specified on the board
      If num is in the specified box starting at (row_start, col_start), return False.
      Otherwise, return True

    Parameters:
    row_start and col_start are the starting indices of the box to check
    i.e. the box is from (row_start, col_start) to (row_start+2, col_start+2)
    num is the value we are looking for in the box

    Return: boolean

    '''

    def valid_in_box(self, row_start, col_start, num):
        for i in range(row_start, row_start + 3):
            for j in range(col_start, col_start + 3):
                if self.board[i][j] == num:
                    return False
        return True

    '''
    Determines if it is valid to enter num at (row, col) in the board
    This is done by checking that num is unused in the appropriate, row, column, and box

  Parameters:
  row and col are the row index and col index of the cell to check in the board
  num is the value to test if it is safe to enter in this cell

  Return: boolean
    '''

    def is_valid(self, row, col, num):
        if self.valid_in_col(col, num) and self.valid_in_row(row, num) and self.valid_in_box(row - row % 3,
                                                                                             col - col % 3, num):
            return True
        else:
            return False

    '''
    Fills the specified 3x3 box with values
    For each position, generates a random digit which has not yet been used in the box

  Parameters:
  row_start and col_start are the starting indices of the box to check
  i.e. the box is from (row_start, col_start) to (row_start+2, col_start+2)

  Return: None
    '''

    def fill_box(self, row_start, col_start):
        box_values = list(range(1, self.row_length + 1))

        for i in range(3):
            for j in range(3):
                choice = random.randint(0, len(box_values) - 1)
                num = box_values[choice]
                box_values.remove(num)
                self.board[row_start + i][col_start + j] = num

    '''
    Fills the three boxes along the main diagonal of the board
    These are the boxes which start at (0,0), (3,3), and (6,6)

  Parameters: None
  Return: None
    '''

    def fill_diagonal(self):
        for i in range(0, self.row_length, 3):
            self.fill_box(i, i)

    '''
    DO NOT CHANGE
    Provided for students
    Fills the remaining cells of the board
    Should be called after the diagonal boxes have been filled

  Parameters:
  row, col specify the coordinates of the first empty (0) cell

  Return:
  boolean (whether or not we could solve the board)
    '''

    def fill_remaining(self, row, col):
        if (col >= self.row_length and row < self.row_length - 1):
            row += 1
            col = 0
        if row >= self.row_length and col >= self.row_length:
            return True
        if row < self.box_length:
            if col < self.box_length:
                col = self.box_length
        elif row < self.row_length - self.box_length:
            if col == int(row // self.box_length * self.box_length):
                col += self.box_length
        else:
            if col == self.row_length - self.box_length:
                row += 1
                col = 0
                if row >= self.row_length:
                    return True

        for num in range(1, self.row_length + 1):
            if self.is_valid(row, col, num):
                self.board[row][col] = num
                if self.fill_remaining(row, col + 1):
                    return True
                self.board[row][col] = 0
        return False

    '''
    DO NOT CHANGE
    Provided for students
    Constructs a solution by calling fill_diagonal and fill_remaining

  Parameters: None
  Return: None
    '''

    def fill_values(self):
        self.fill_diagonal()  # This one works
        self.fill_remaining(0, self.box_length)  # This one keeps getting stuck

    def remove_cells(self):  # Check This One Works
        for i in range(self.removed_cells):
            row = random.randint(0, 9 - 1)
            col = random.randint(0, 9 - 1)
            while self.board[row][col] == 0:
                row = random.randint(0, 9 - 1)
                col = random.randint(0, 9 - 1)
            self.board[row][col] = 0


def generate_sudoku(size, removed):
    sudoku = SudokuGenerator(size, removed)
    sudoku.fill_values()
    board = sudoku.get_board()
    sudoku.remove_cells()
    board = sudoku.get_board()
    return board


'''DO NOT CHANGE
Provided for students
Given a number of rows and number of cells to remove, this function:
1. creates a SudokuGenerator
2. fills its values and saves this as the solved state
3. removes the appropriate number of cells
4. returns the representative 2D Python Lists of the board and solution

Parameters:
size is the number of rows/columns of the board (9 for this project)
removed is the number of cells to clear (set to 0)

Return: list[list] (a 2D Python list to represent the board)'''


########################
#
#   Cell
#
########################

class Cell:

    def __init__(self, value, row, col, screen):
        '''Constructor for the Cell class'''
        self.value = value
        self.row = row
        self.col = col
        self.screen = screen
        self.sketched_value = 0
        font_size = 50
        self.font = pygame.font.Font(None, font_size)
        self.is_selected = False
        self.was_blank = False

    def set_cell_value(self, value):
        '''Setter for this cell’s value'''
        self.value = value

    def set_sketched_value(self, value):
        '''Setter for this cell’s sketched value'''
        self.sketched_value = value

    def draw(self):
        '''Draws this cell, along with the value inside it.
If this cell has a nonzero value, that value is displayed.
Otherwise, no value is displayed in the cell.
The cell is outlined red if it is currently selected.'''

        w = self.screen.get_width()
        h = self.screen.get_height()
        cell_width = (w - 2 * w // 10 - w // 20) // 9
        cell_height = (h - 2 * h // 10 - h // 20) // 9

        #makes inputted numbers comeout as gray instead of black so players can see which numbers the input
        if self.sketched_value != 0:
            if self.was_blank == True:
                text = self.font.render(str(self.sketched_value), True, (128, 128, 128))
            else:
                text = self.font.render(str(self.sketched_value), True, (0, 0, 0))
            cell_rect = pygame.Rect((w - cell_width * 9) // 2 + self.col * cell_width, h // 20 + self.row * cell_height, cell_width, cell_height)
            cell_rect = text.get_rect(center=cell_rect.center)
            self.screen.blit(text, cell_rect)
        else:
            text = self.font.render('', True, (0, 0, 0))
            cell_rect = pygame.Rect((w - cell_width * 9) // 2 + self.col * cell_width, h // 20 + self.row * cell_height, cell_width, cell_height)
            cell_rect = text.get_rect(center=cell_rect.center)
            self.screen.blit(text, cell_rect)
        #makes a red outline when the boxs are clicked on
        if self.is_selected:
            pygame.draw.line(self.screen, (255, 0, 0),
                             ((w - cell_width * 9) // 2 + self.col * cell_width, h // 20 + self.row * cell_height),
                             ((w - cell_width * 9) // 2 + self.col * cell_width + cell_width, h // 20 + self.row * cell_height), 2)
            pygame.draw.line(self.screen, (255, 0, 0),
                             ((w - cell_width * 9) // 2 + self.col * cell_width, h // 20 + self.row * cell_height),
                             ((w - cell_width * 9) // 2 + self.col * cell_width, h // 20 + self.row * cell_height + cell_height), 2)
            pygame.draw.line(self.screen, (255, 0, 0),
                             ((w - cell_width * 9) // 2 + self.col * cell_width, h // 20 + self.row * cell_height + cell_height),
                             ((w - cell_width * 9) // 2 + self.col * cell_width + cell_width, h // 20 + self.row * cell_height + cell_height), 2)
            pygame.draw.line(self.screen, (255, 0, 0),
                             ((w - cell_width * 9) // 2 + self.col * cell_width + cell_width, h // 20 + self.row * cell_height),
                             ((w - cell_width * 9) // 2 + self.col * cell_width + cell_width, h // 20 + self.row * cell_height + cell_height), 2)





########################
#
#   Board
#
########################



class Board:

    def __init__(self, width, height, screen, difficulty):
        self.width = width #good
        self.height = height #good
        self.screen = screen #good
        self.difficulty = difficulty #good
        #print("Test 1") #good
        self.board = generate_sudoku(9, self.difficulty)
        #print("Test 2")
        self.original_board = [[cell for cell in row] for row in self.board]
        #print("Test 3")
        self.cells = [[Cell(self.board[row][col],row,col,self.screen) for col in range(9)] for row in range(9)]
        for cell_row in self.cells:
            for cell in cell_row:
                if cell.value == 0:
                    cell.was_blank = True
        self.selected_cell = self.find_empty()
        return

    def draw(self): #All works
        '''Draws an outline of the Sudoku grid, with bold lines to delineate the 3x3 boxes.
Draws every cell on this board.'''
        # box size
        w = self.screen.get_width()
        h = self.screen.get_height()
        box_width = (w - 2 * w // 10 - w // 20) // 9 #(self.screen.get_width() - 100) // 9
        box_height = (h - 2 * h // 10 - h // 20) // 9

        for i in range(0, 10):
            line_width = 5 if i % 3 == 0 else 2 #Great

            # vertical lines
            pygame.draw.line(self.screen, (0, 0, 0), (i * box_width + (w - box_width * 9)//2, h // 20),
                             (i * box_width + (w - box_width * 9)//2, h - 2 * h // 10), line_width)

            # horizontal lines
            pygame.draw.line(self.screen, (0, 0, 0), ((w - box_width * 9)//2, i * box_height + h // 20),
                             (w-(w - box_width * 9)//2, i * box_height + h // 20), line_width)

    def select(self, row, col):
        '''Marks the cell at (row, col) in the board as the current selected cell.
Once a cell has been selected, the user can edit its value or sketched value'''
        if self.original_board[row][col] == 0:
            self.cells[self.selected_cell[0]][self.selected_cell[1]].is_selected = False
            self.cells[row][col].is_selected = True
            self.selected_cell = (row,col)

    def click(self, screen, x, y):
        #Dimensions of each box for when clicked on, will return the correct tuple for the row and column
        '''If a tuple of (x, y) coordinates is within the displayed board, this function returns a tuple of the (row, col)
of the cell which was clicked. Otherwise, this function returns None.'''
        w = self.screen.get_width()
        h = self.screen.get_height()
        cell_width = (w - 2 * w // 10 - w // 20) // 9
        cell_height = (h - 2 * h // 10 - h // 20) // 9

        if ((w - cell_width * 9)//2) <= x <= w - ((w - cell_width * 9)//2) and (h // 20) <= y <= (cell_height * 9) + (h // 20):
            x -= (w - cell_width * 9)//2
            y -= (h // 20)
            col = x // cell_width
            row = y // cell_height
            return row, col
        else:
            return None

    def clear(self):

        '''Clears the value cell. Note that the user can only remove the cell values and sketched value that are
filled by themselves'''
        row, col = self.selected_cell
        if self.original_board[row][col] == 0:
            self.board[row][col] = 0

    def sketch(self, value):
        '''Sets the sketched value of the current selected cell equal to user entered value.
It will be displayed at the top left corner of the cell using the draw() function'''
        row, col = self.selected_cell
        cell = Cell(value, row, col, self.screen).set_sketched_value(value)
        cell.draw()

    def place_number(self, value):
        '''Sets the value of the current selected cell equal to user entered value.
Called when the user presses the Enter key.'''
        if self.selected_cell:
            row, col = self.selected_cell
            cell = Cell(value, row, col, self.screen).set_cell_value(value)
            cell.draw()

    def reset_to_original(self): #This one is all good
        '''Reset all cells in the board to their original values (0 if cleared, otherwise the corresponding digit).'''
        self.board = [[cell for cell in row] for row in self.original_board]
        #self.board = [row[:] for row in self.original_board]

    def is_full(self):
        '''Returns a Boolean value indicating whether the board is full or not.'''
        for row in self.board:
            for cell in row:
                if cell == 0:
                    return False
        return True

    def update_board(self):
        '''Updates the underlying 2D board with the values in all cells.'''
        for row in self.board:
            for cell in row:
                self.create_board.board[row][cell] = cell

    def find_empty(self):
        '''Finds an empty cell and returns its row and col as a tuple (x, y).'''
        for row in self.board:
            for cell in row:
                if cell == 0:
                    return (self.board.index(row), row.index(cell))

        return None

    def check_board(self): #This one works
        '''Check whether the Sudoku board is solved correctly.'''
        for row in self.board:
            row_sum = 0
            for cell in row:
                row_sum += cell
            if row_sum != 45:
                return False
        for column_index in range(len(self.board[0])):
            column_sum = 0
            for row_index in range(len(self.board)):
                column_sum += self.board[row_index][column_index]
            if column_sum != 45:
                return False
        return True

########################
#
#   Main
#
########################

def set_sketched_values_cells(board):
    for cell_row in board.cells:
        for cell in cell_row:
            cell.set_sketched_value(cell.value)

    #function for the title screen

def draw_title_screen():
    global easy_button_rect
    global medium_button_rect
    global hard_button_rect
    global easy_number
    global medium_number
    global hard_number
    screen.fill(BG_COLOR)

    # Title Screen
    title = title_font.render("Sudoku", True, CROSS_COLOR)
    title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 4))
    screen.blit(title, title_rect)

    # Easy Button
    easy_button_rect = pygame.Rect(WIDTH // 4, HEIGHT // 2, WIDTH // 2, 50)
    pygame.draw.rect(screen, CROSS_COLOR, easy_button_rect)
    easy_button = label_font.render("Easy", True, BG_COLOR)
    easy_text_rect = easy_button.get_rect(center=easy_button_rect.center)
    screen.blit(easy_button, easy_text_rect)
    easy_number = 30

    # Medium Button
    medium_button_rect = pygame.Rect(WIDTH // 4, HEIGHT // 2 + 100, WIDTH // 2, 50)
    pygame.draw.rect(screen, CROSS_COLOR, medium_button_rect)
    medium_button = label_font.render("Medium", True, BG_COLOR)
    medium_text_rect = medium_button.get_rect(center=medium_button_rect.center)
    screen.blit(medium_button, medium_text_rect)
    medium_number = 40

    # Hard Button
    hard_button_rect = pygame.Rect(WIDTH // 4, HEIGHT // 2 + 200, WIDTH // 2, 50)
    pygame.draw.rect(screen, CROSS_COLOR, hard_button_rect)
    hard_button = label_font.render("Hard", True, BG_COLOR)
    hard_text_rect = hard_button.get_rect(center=hard_button_rect.center)
    screen.blit(hard_button, hard_text_rect)
    hard_number = 50

def draw_game_buttons(screen,screen_width,screen_height):
    global exit_button_rect
    global reset_button_rect
    global restart_button_rect
    button_width = (screen.get_width() - 4 * screen.get_width() // 20) // 3
    button_height = (screen.get_height() // 10)

    #exit button
    exit_button_rect = pygame.Rect(screen.get_width() // 20, screen.get_height() - 2 * screen.get_height() // 10 + screen.get_height() // 20, button_width, button_height)
    pygame.draw.rect(screen, (0, 0, 0), exit_button_rect)
    exit_button_font = label_font.render("Exit", True, BG_COLOR)
    exit_text_rect = exit_button_font.get_rect(center=exit_button_rect.center)
    screen.blit(exit_button_font, exit_text_rect)

    # Reset button
    reset_button_rect = pygame.Rect(2 * screen.get_width() // 20 + button_width,screen.get_height() - 2 * screen.get_height() // 10 + screen.get_height() // 20,button_width, button_height)
    pygame.draw.rect(screen, (0, 0, 0), reset_button_rect)
    reset_button_font = label_font.render('Reset', True, BG_COLOR)
    reset_button_rect = reset_button_font.get_rect(center = reset_button_rect.center)
    screen.blit(reset_button_font, reset_button_rect)

    # Restart button
    restart_button_rect = pygame.Rect(3 * screen.get_width() // 20 + 2 * button_width,screen.get_height() - 2 * screen.get_height() // 10 + screen.get_height() // 20,button_width, button_height)
    pygame.draw.rect(screen, (0, 0, 0), restart_button_rect)
    restart_button_font = label_font.render('Restart', True, BG_COLOR)
    restart_button_rect = restart_button_font.get_rect(center=restart_button_rect.center)
    screen.blit(restart_button_font, restart_button_rect)
    return

def main():
    global screen
    draw_title_screen()
    easy_screen = pygame.display.set_mode((SIZE))
    clock = pygame.time.Clock()
    display_board = False
    game_bool = False
    game_win = False
    game_lose = False

    title_font = pygame.font.SysFont("times new roman", 70, (255, 255, 245))
    label_font = pygame.font.SysFont("times new roman", 32, (255, 255, 245))

    button_width = (screen.get_width() - 4 * screen.get_width() // 20) // 3
    button_height = (screen.get_height() // 10)
    exit_button_rect = pygame.Rect(screen.get_width() // 20,screen.get_height() - 2 * screen.get_height() // 10 + screen.get_height() // 20,button_width, button_height)
    restart_button_rect = pygame.Rect(3 * screen.get_width() // 20 + 2 * button_width,screen.get_height() - 2 * screen.get_height() // 10 + screen.get_height() // 20,button_width, button_height)

    while True: #Menu loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if not(game_win or game_lose):
                        if easy_button_rect.collidepoint(event.pos):
                            #print('Easy clicked')
                            #display_board = True
                            game_bool = True
                            #difficulty_mode = 30
                            board = Board(screen.get_width(), screen.get_height(), screen, 30)
                            set_sketched_values_cells(board)
                        elif medium_button_rect.collidepoint(event.pos):
                            #print("medium clicked")
                            #display_board = True
                            game_bool = True
                            #difficulty_mode = 40
                            board = Board(screen.get_width(), screen.get_height(), screen, 40)
                            set_sketched_values_cells(board)
                        elif hard_button_rect.collidepoint(event.pos):
                            #print('hard button clicked')
                            #display_board = True
                            game_bool = True
                            #difficulty_mode = 50
                            board = Board(screen.get_width(), screen.get_height(), screen, 50)
                            set_sketched_values_cells(board)
                    elif game_win or game_lose:
                        if game_win:
                            #Game win exit button collide check
                            if exit_button_rect.collidepoint(event.pos):
                                print("Thank you for playing!")
                                pygame.quit()
                                sys.exit()

                        elif game_lose:
                            #Game lose restart button collide check
                            if restart_button_rect.collidepoint(event.pos):
                                game_win = False
                                game_lose = False
                                break

        while game_bool:#Gameplay loop

            screen.fill(BG_COLOR)  # good
            board.draw()
            button_width = (screen.get_width() - 4 * screen.get_width() // 20) // 3
            button_height = (screen.get_height() // 10)
            draw_game_buttons(screen, screen.get_width(), screen.get_height())

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    #Allowing the buttons to register clicks and performing operations
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if exit_button_rect.collidepoint(event.pos): #Exit button clickable and ends game
                            #print('Exit clicked')
                            print("Thank you for playing!")
                            pygame.quit()
                            sys.exit()

                        elif reset_button_rect.collidepoint(event.pos): #Reset button clickable and resets the board to the original
                            #print("Reset clicked")
                            board.reset_to_original()

                        elif restart_button_rect.collidepoint(event.pos): #Restart button clickable and restarts to menu
                            #print('Restart button clicked')
                            game_bool = False
                            break

                        elif board.click(screen, event.pos[0],event.pos[1]) != None:
                            board.select(board.click(screen, event.pos[0],event.pos[1])[0],board.click(screen, event.pos[0],event.pos[1])[1])

               #Implementing the numbers as buttons when clicked, 1-9
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        board.board[board.selected_cell[0]][board.selected_cell[1]] = 1
                    elif event.key == pygame.K_2:
                        board.board[board.selected_cell[0]][board.selected_cell[1]] = 2
                    elif event.key == pygame.K_3:
                        board.board[board.selected_cell[0]][board.selected_cell[1]] = 3
                    elif event.key == pygame.K_4:
                        board.board[board.selected_cell[0]][board.selected_cell[1]] = 4
                    elif event.key == pygame.K_5:
                        board.board[board.selected_cell[0]][board.selected_cell[1]] = 5
                    elif event.key == pygame.K_6:
                        board.board[board.selected_cell[0]][board.selected_cell[1]] = 6
                    elif event.key == pygame.K_7:
                        board.board[board.selected_cell[0]][board.selected_cell[1]] = 7
                    elif event.key == pygame.K_8:
                        board.board[board.selected_cell[0]][board.selected_cell[1]] = 8
                    elif event.key == pygame.K_9:
                        board.board[board.selected_cell[0]][board.selected_cell[1]] = 9

            #sets row and cell values
            for cell_row_index in range(len(board.cells)):
                for cell_index in range(len(board.cells[cell_row_index])):
                    board.cells[cell_row_index][cell_index].set_cell_value(board.board[cell_row_index][cell_index])
                    board.cells[cell_row_index][cell_index].set_sketched_value(board.board[cell_row_index][cell_index])
                    board.cells[cell_row_index][cell_index].draw()

            #for row in board.board:
            #    for cell in row:
            #        print(cell,end=" ")
            #    print()
            #print("-----------------------")

            #for row in board.original_board:
            #    for cell in row:
            #        print(cell,end=" ")
            #    print()
            #print()

            if board.is_full():
                if board.check_board():
                    game_win = True
                else:
                    game_lose = True
                game_bool = False
                break

            #pygame.time.wait(1000)

            pygame.display.flip()

        draw_title_screen()

        if game_win or game_lose:
            screen.fill(BG_COLOR)  # good
            if game_win:
                #Draw exit button
                pygame.draw.rect(screen, (0, 0, 0), exit_button_rect)
                exit_button_font = label_font.render("Exit", True, BG_COLOR)
                exit_text_rect = exit_button_font.get_rect(center=exit_button_rect.center)
                screen.blit(exit_button_font, exit_text_rect)
                win_text = title_font.render("Game Won!", True, CROSS_COLOR)
                win_rect = win_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
                screen.blit(win_text, win_rect)
            if game_lose:
                # Restart button
                pygame.draw.rect(screen, (0, 0, 0), restart_button_rect)
                restart_button_font = label_font.render('Restart', True, BG_COLOR)
                restart_text_rect = restart_button_font.get_rect(center=restart_button_rect.center)
                screen.blit(restart_button_font, restart_text_rect)
                lose_text = title_font.render("You Lose!", True, CROSS_COLOR)
                lose_rect = lose_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
                screen.blit(lose_text, lose_rect)

        pygame.display.flip() #updates screen

if __name__ == "__main__":
    main()



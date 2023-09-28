from os import killpg
import random
import numpy as np
import pdb
import copy
import time

# Set these flags to True or False to enable/disable constraints
USE_NORMAL_SUDOKU = True
USE_DIAGONALS = False
USE_ANTIKNIGHTS_CONSTRAINT = False
USE_KINGS_CONSTRAINT = False
USE_NONCONSECUTIVE_CONSTRAINT = False
USE_KYLE = False
USE_CHESS = False
GRID_SIZE = 2

# Check if grid is full
def is_grid_full(board):
    for row in board:
        if 0 in row:
            return False
    return True

# Normal Sudoku Function
def regular_rules(board,row,col,num):
    # Check row and column
    for i in range(GRID_SIZE**2):
        if board[row][i] == num or board[i][col] == num:
            return False
    # Check 3x3 subgrid
    start_row, start_col = GRID_SIZE * (row // GRID_SIZE), GRID_SIZE * (col // GRID_SIZE)
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if board[start_row + i][start_col + j] == num:
                return False
    return True

# All rows and sums equal the same number
def check_sums(board):
    x = sum(board[0])


    print("sum ", x)
    for i in range(4):
        y = sum(board[i]) #row 

        #col = [board[j][i] for j in range(4)]
        col = board[0:GRID_SIZE**2,i]
        z = sum(col) #col



        if y != x or z != x:
            return False
    return True

#########################################

# MAIN DEFINITION: CHECKS IF THE SUDOKU FOLLOWS THE GIVEN RULES
def is_valid(board, row, col, num):
    if USE_NORMAL_SUDOKU: #Normal Rules
        if not regular_rules(board,row,col,num):
            return False
    
    #check rows
    prev_sum = 0
    for row in board:
        if 0 in row:
            if sum(row) > prev_sum and prev_sum != 0:
                return False
        else:
            if prev_sum == 0:
                prev_sum = sum(row)
            else:
                if prev_sum != sum(row):
                    return False
    
    #check columns
    for i in range(4):
        col = [board[j][i] for j in range(4)]
        if 0 in col:
            if sum(col) > prev_sum and prev_sum != 0:
                return False
        else:
            if prev_sum == 0:
                prev_sum = sum(col)
            else:
                if prev_sum != sum(col):
                    return False
    return True
    
# SOLVE CURRENT BOARD
def solve_sudoku(board):
    for row in range(GRID_SIZE**2):
        for col in range(GRID_SIZE**2):
            if board[row][col] == 0:
                for num in random.sample(range(1, 10), 9):
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        if is_grid_full(board):
                            if check_sums(board):
                                return True
                            else:
                                board[row][col] = 0
                                return False
                        if solve_sudoku(board):
                            return True
                        board[row][col] = 0
                return False
    return True

def generate_sudoku():
    board = np.zeros((GRID_SIZE**2,GRID_SIZE**2))
    #board2[0:4,0] = np.transpose(np.array([1,1,1,1]))

    solve_sudoku(board)
    return board

def print_sudoku(board):
    print("printing")
    for row in board:
        print(" ".join(map(str, row)))

if __name__ == "__main__":
    sudoku_puzzle = generate_sudoku()
    print("Generated Sudoku Puzzle:")
    print_sudoku(sudoku_puzzle)

from os import killpg
import random
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

# Check if grid is full
def is_grid_full(board):
    for row in board:
        if 0 in row:
            return False
    return True

# Knights Definition
def is_knights_move_away(r1, c1, r2, c2):
    return abs(r1 - r2) == 2 and abs(c1 - c2) == 1 or abs(r1 - r2) == 1 and abs(c1 - c2) == 2

# Bishop Functions
def is_diagonal(r1, c1, r2, c2):
    if r1 == r2 and c1 == c2:
       return False 
    return abs(r1 - r2) == abs(c1 - c2)

# Normal Sudoku Function
def regular_rules(board,row,col,num):
    # Check row and column
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False
    # Check 3x3 subgrid
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False
    return True

# Checks if diagonals are unique 
def is_valid_diagonals(board,row,col,num):
    d1 = [(i,i) for i in range(9)]
    diagonal1 = [board[i][i] for i in range(9)]
    d2 = [(i,8-i) for i in range(9)]
    diagonal2 = [board[i][8 - i] for i in range(9)]
    if (row,col) in d1 and num in diagonal1:
        return False
    if (row,col) in d2 and num in diagonal2:
        return False
    return True

#########################################

# MAIN DEFINITION: CHECKS IF THE SUDOKU FOLLOWS THE GIVEN RULES
def is_valid(board, row, col, num):
    if USE_NORMAL_SUDOKU: #Normal Rules
        if not regular_rules(board,row,col,num):
            return False
        
    if USE_DIAGONALS: # Anti diagonals
        if not is_valid_diagonals(board,row,col,num):
            return False
    
    if USE_ANTIKNIGHTS_CONSTRAINT: #KNIGHTS
        for i in range(9):
            for j in range(9):
                if board[i][j] != 0 and is_knights_move_away(row, col, i, j) and board[i][j] == num:
                    return False

    if USE_KINGS_CONSTRAINT: # KINGS
        for dr, dc in [(1, 1), (-1, -1), (1, -1), (-1, 1)]:
            r, c = row + dr, col + dc
            if 0 <= r < 9 and 0 <= c < 9 and board[r][c] == num:
                return False

    # ORTHOGONAL NONCONSECUTIVE
    if USE_NONCONSECUTIVE_CONSTRAINT:
        consecutive_digits = [(num - 1) % 9, (num + 1) % 9]
        #print("cons ", consecutive_digits)
        consecutive_digits = [digit for digit in consecutive_digits if digit != 0]
        #print("cons ", consecutive_digits)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            r, c = row + dr, col + dc
            if 0 <= r < 9 and 0 <= c < 9 and board[r][c] in consecutive_digits:
                return False
            
    if USE_KYLE:
        if board[2][0] != 0: #if the number isn't zero
            if sum([board[3][0],board[4][0],board[5][0]]) > board[2][0] or sum([board[3][0],board[3][1],board[2][2]]) > board[2][0] or \
            sum([board[3][0],board[4][1],board[5][2]]) > board[2][0]: #If the sums are already bigger
                return False
            numbers = [board[3][0],board[4][0],board[5][0],board[3][1],board[2][2],board[4][1],board[5][2]]
            if not any(num == 0 for num in numbers): #if no tail has zero
                if sum([board[3][0],board[4][0],board[5][0]]) != board[2][0] or sum([board[3][0],board[3][1],board[2][2]]) != board[2][0] or \
                sum([board[3][0],board[4][1],board[5][2]]) != board[2][0]: #If the sums don't add up
                    return False
        # if board[3][3] != 0: #if the number isn't zero
        #     if sum([board[4][4],board[3][5]]) > board[3][3] or \
        #     sum([board[4][4],board[5][3],board[6][2]]) > board[3][3]: #If the sums are already bigger
        #         return False
        #     numbers = [board[4][4],board[3][5],board[5][3],board[6][2]]
        #     if not any(num == 0 for num in numbers): #if no tail has zero
        #         if sum([board[4][4],board[3][5]]) != board[3][3] or \
        #         sum([board[4][4],board[5][3],board[6][2]]) != board[3][3]: #If the sums don't add up
        #             return False
        

        # knights and bishop
        for i in range(9):
            for j in range(9):
                #print("i ", i, " j ", j)
                if board[i][j] == num or board[i][j] == 0:
                    if is_knights_move_away(row, col, i, j) or is_diagonal(row, col, i, j):
                        return True
        return False

    # For debuggin later
    #pdb.set_trace()
    #vals = [board,num,row,col]
    return True

# SOLVE CURRENT BOARD
def solve_sudoku(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                for num in random.sample(range(1, 10), 9):
                    #for num in range(1,10):  # Shuffle numbers for randomness
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        if is_grid_full(board):
                            return True
                        if solve_sudoku(board):
                            return True
                        board[row][col] = 0
                return False
    return True

def generate_sudoku():

    board = [[0 for _ in range(9)] for _ in range(9)]
    solve_sudoku(board)

    
    return board

def print_sudoku(board):
    print(" ")
    for row in board:
        print(" ".join(map(str, row)))

if __name__ == "__main__":
    sudoku_puzzle = generate_sudoku()
    print("Generated Sudoku Puzzle:")
    print_sudoku(sudoku_puzzle)



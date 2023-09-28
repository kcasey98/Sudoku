#include <iostream>
#include <vector>
#include <algorithm>
#include <random>

using namespace std;

// Set these flags to true or false to enable/disable constraints
bool USE_NORMAL_SUDOKU = true;
bool USE_ANTIKNIGHTS_CONSTRAINT = false;
bool USE_KINGS_CONSTRAINT = false;
bool USE_NONCONSECUTIVE_CONSTRAINT = false;

// Check if grid is full
bool is_grid_full(vector< vector<int> >& board) {
    for (const vector<int>& row : board) {
        if (find(row.begin(), row.end(), 0) != row.end()) {
            return false;
        }
    }
    return true;
}

// Knights Definition
bool is_knights_move_away(int r1, int c1, int r2, int c2) {
    return (abs(r1 - r2) == 2 && abs(c1 - c2) == 1) || (abs(r1 - r2) == 1 && abs(c1 - c2) == 2);
}

// Bishop Functions
bool is_diagonal(int r1, int c1, int r2, int c2) {
    if (r1 == r2 && c1 == c2) {
        return false;
    }
    return abs(r1 - r2) == abs(c1 - c2);
}

// Normal Sudoku Function
bool regular_rules(vector< vector<int> >& board, int row, int col, int num) {
    // Check row and column
    for (int i = 0; i < 9; ++i) {
        if (board[row][i] == num || board[i][col] == num) {
            return false;
        }
    }
    // Check 3x3 subgrid
    int start_row = 3 * (row / 3);
    int start_col = 3 * (col / 3);
    for (int i = 0; i < 3; ++i) {
        for (int j = 0; j < 3; ++j) {
            if (board[start_row + i][start_col + j] == num) {
                return false;
            }
        }
    }
    return true;
}

// MAIN DEFINITION: CHECKS IF THE SUDOKU FOLLOWS THE GIVEN RULES
bool is_valid(vector< vector<int> >& board, int row, int col, int num) {
    if (USE_NORMAL_SUDOKU) { // Normal Rules
        if (!regular_rules(board, row, col, num)) {
            return false;
        }
    }

    if (USE_ANTIKNIGHTS_CONSTRAINT) { // KNIGHTS
        for (int i = 0; i < 9; ++i) {
            for (int j = 0; j < 9; ++j) {
                if (board[i][j] != 0 && is_knights_move_away(row, col, i, j) && board[i][j] == num) {
                    return false;
                }
            }
        }
    }

    if (USE_KINGS_CONSTRAINT) { // KINGS
        int dr[4] = {1, -1, 1, -1};
        int dc[4] = {1, -1, -1, 1};
        for (int k = 0; k < 4; ++k) {
            int r = row + dr[k];
            int c = col + dc[k];
            if (r >= 0 && r < 9 && c >= 0 && c < 9 && board[r][c] == num) {
                return false;
            }
        }
    }

    // ORTHOGONAL NONCONSECUTIVE
    if (USE_NONCONSECUTIVE_CONSTRAINT) {
        int consecutive_digits[] = {((num - 1) % 9), ((num + 1) % 9)};
        vector<int> consecutive_digits_vec;
        for (int i = 0; i < 2; ++i) {
            if (consecutive_digits[i] != 0) {
                consecutive_digits_vec.push_back(consecutive_digits[i]);
            }
        }
        for (int dr = -1; dr <= 1; dr += 2) {
            for (int dc = -1; dc <= 1; dc += 2) {
                int r = row + dr;
                int c = col + dc;
                if (r >= 0 && r < 9 && c >= 0 && c < 9 &&
                    find(consecutive_digits_vec.begin(), consecutive_digits_vec.end(), board[r][c]) != consecutive_digits_vec.end()) {
                    return false;
                }
            }
        }
    }

    return true;
}

// SOLVE CURRENT BOARD
bool solve_sudoku(vector< vector<int> >& board) {
    for (int row = 0; row < 9; ++row) {
        for (int col = 0; col < 9; ++col) {
            if (board[row][col] == 0) {
                //vector<int> num_list = {1, 2, 3, 4, 5, 6, 7, 8, 9};
                vector<int> num_list;
                for (int i = 1; i <= 9; ++i) {
                    num_list.push_back(i);
                }
                shuffle(num_list.begin(), num_list.end(), mt19937(random_device()()));
                for (int num : num_list) {
                    if (is_valid(board, row, col, num)) {
                        board[row][col] = num;
                        if (is_grid_full(board)) {
                            return true;
                        }
                        if (solve_sudoku(board)) {
                            return true;
                        }
                        board[row][col] = 0;
                    }
                }
                return false;
            }
        }
    }
    return true;
}

// Generate Sudoku
vector< vector<int> > generate_sudoku() {
    vector< vector<int> > board(9, vector<int>(9, 0));
    solve_sudoku(board);
    return board;
}

// Print Sudoku
void print_sudoku(const vector< vector<int> >& board) {
    cout << endl;
    for (const vector<int>& row : board) {
        for (int num : row) {
            cout << num << " ";
        }
        cout << endl;
    }
}

int main() {
    vector< vector<int> > sudoku_puzzle = generate_sudoku();
    cout << "Generated Sudoku Puzzle:" << endl;
    print_sudoku(sudoku_puzzle);
    return 0;
}

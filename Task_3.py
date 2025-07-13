import tkinter as tk
from tkinter import messagebox

class SudokuSolverGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Solver")

        self.entries = []
        for i in range(9):
            row_entries = []
            for j in range(9):
                e = tk.Entry(root, width=3, justify="center", font=("Arial", 16))
                e.grid(row=i, column=j, padx=2, pady=2)
                row_entries.append(e)
            self.entries.append(row_entries)

        solve_button = tk.Button(root, text="Solve", command=self.solve)
        solve_button.grid(row=9, column=0, columnspan=9, pady=10)

    def get_board(self):
        board = []
        for i in range(9):
            row = []
            for j in range(9):
                val = self.entries[i][j].get()
                if val == '':
                    row.append(0)
                else:
                    try:
                        num = int(val)
                        if num < 0 or num > 9:
                            raise ValueError
                        row.append(num)
                    except ValueError:
                        messagebox.showerror("Invalid Input", f"Invalid value at row {i+1}, column {j+1}")
                        return None
            board.append(row)
        return board

    def set_board(self, board):
        for i in range(9):
            for j in range(9):
                self.entries[i][j].delete(0, tk.END)
                if board[i][j] != 0:
                    self.entries[i][j].insert(0, str(board[i][j]))

    def solve(self):
        board = self.get_board()
        if board and self.solve_board(board):
            self.set_board(board)
            messagebox.showinfo("Success", "Sudoku solved successfully!")
        elif board:
            messagebox.showerror("No Solution", "No solution exists for this puzzle.")

    def find_empty(self, board):
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    return (i, j)
        return None

    def valid(self, board, num, pos):
        row, col = pos

        for j in range(9):
            if board[row][j] == num and j != col:
                return False

        for i in range(9):
            if board[i][col] == num and i != row:
                return False

        box_x = col // 3
        box_y = row // 3

        for i in range(box_y*3, box_y*3 + 3):
            for j in range(box_x*3, box_x*3 + 3):
                if board[i][j] == num and (i, j) != pos:
                    return False

        return True

    def solve_board(self, board):
        find = self.find_empty(board)
        if not find:
            return True
        else:
            row, col = find

        for num in range(1, 10):
            if self.valid(board, num, (row, col)):
                board[row][col] = num

                if self.solve_board(board):
                    return True

                board[row][col] = 0

        return False

# Run the GUI
root = tk.Tk()
app = SudokuSolverGUI(root)
root.mainloop()

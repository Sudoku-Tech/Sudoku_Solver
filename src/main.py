import tkinter as tk
from gui.main_app import SudokuApp

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Sudoku Solver")
    root.geometry("724x768")  

    app = SudokuApp(root)
    root.mainloop()

import tkinter as tk
from gui.main_view import MainView
from gui.input_view import InputView
from gui.solving_view import SolvingView
from gui.results_view import ResultsView
from gui.algorithms_info_view import AlgorithmsInfoView

class SudokuApp:
    def __init__(self, root):
        self.root = root
        self.root.resizable(False, False)

        self.container = tk.Frame(self.root)
        self.container.pack(fill="both", expand=True)

        self.views = {}
        self.init_views()

        self.show_view("MainView")

    def init_views(self):
        self.views["MainView"] = MainView(self.container, self)
        self.views["InputView"] = InputView(self.container, self)
        self.views["SolvingView"] = SolvingView(self.container, self)
        self.views["ResultsView"] = ResultsView(self.container, self)
        self.views["AlgorithmsInfoView"] = AlgorithmsInfoView(self.container, self)

        for view in self.views.values():
            view.place(x=0, y=0, relwidth=1, relheight=1)

    def show_view(self, view_name):
        view = self.views[view_name]
        view.tkraise()

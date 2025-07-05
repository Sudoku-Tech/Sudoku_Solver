import tkinter as tk
from PIL import Image, ImageTk

class MainView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.bg_image = Image.open("src/assets/fondo.png")
        self.bg_photo = ImageTk.PhotoImage(self.bg_image.resize((724, 768)))

        self.canvas = tk.Canvas(self, width=724, height=768)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, anchor="nw", image=self.bg_photo)

        self.canvas.create_text(362, 100, text="Sudoku Solver", font=("Helvetica", 36, "bold"), fill="white")
        self.canvas.create_text(362, 200, text="Compara la eficiencia de algoritmos de Sudoku.", font=("Helvetica", 18), fill="white")

        btn_resolver = tk.Button(self, text="Resolver sudoku", width=32, font=("Helvetica", 14, "bold"), command=lambda: controller.show_view("InputView"))
        btn_algo = tk.Button(self, text="Algoritmos de comparación", width=32, font=("Helvetica", 14, "bold"), command=lambda: controller.show_view("AlgorithmsInfoView"))
        btn_salir = tk.Button(self, text="Salir", width=32, font=("Helvetica", 14, "bold"), command=controller.root.quit)

        self.canvas.create_window(362, 350, window=btn_resolver)
        self.canvas.create_window(362, 410, window=btn_algo)
        self.canvas.create_window(362, 470, window=btn_salir)

        self.canvas.create_text(362, 740, text="v1.0 © 2025 Complejidad algorítmica - UPC", fill="white", font=("Helvetica", 14))

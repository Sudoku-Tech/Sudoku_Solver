import tkinter as tk
from PIL import Image, ImageTk

class InputView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.bg_image = Image.open("src/assets/fondo2.png")
        self.bg_photo = ImageTk.PhotoImage(self.bg_image.resize((724, 768)))

        self.canvas = tk.Canvas(self, width=724, height=768)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, anchor="nw", image=self.bg_photo)

        self.canvas.create_text(362, 24, text="Pantalla de entrada", font=("Helvetica", 18, "bold"), fill="black")
        self.btn_atras = tk.Button(self, text="← Atrás", command=lambda: controller.show_view("MainView"))
        self.canvas.create_window(60, 24, window=self.btn_atras)

        # Tablero vacío (grid visual)
        self.grid_frame = tk.Frame(self.canvas, bg="white")
        large_cell_font = ("Helvetica", 24)
        for i in range(9):
            for j in range(9):
                tk.Entry(self.grid_frame, width=2, justify='center', font=large_cell_font,).grid(row=i, column=j, padx=1, pady=1)
        self.canvas.create_window(362, 260, window=self.grid_frame)

        # Botones de acción
        self.btn_gen = tk.Button(self, width=22, font=("Helvetica", 14, "bold"), text="GENERAR ALEATORIO")
        self.btn_cargar = tk.Button(self, width=22,  font=("Helvetica", 14, "bold"), text="CARGAR TABLERO")
        self.btn_borrar = tk.Button(self, width=22, font=("Helvetica", 14, "bold"), text="BORRAR TABLERO")
        self.btn_resolver = tk.Button(self, width=22, font=("Helvetica", 14, "bold"), text="RESOLVER", command=lambda: controller.show_view("SolvingView"))

        self.canvas.create_window(210, 550, window=self.btn_gen)
        self.canvas.create_window(510, 550, window=self.btn_cargar)
        self.canvas.create_window(210, 600, window=self.btn_borrar)
        self.canvas.create_window(510, 600, window=self.btn_resolver)

        self.canvas.create_text(362, 650, text="[Mensaje de Feedback: 'Tablero listo!']", fill="white", font=("Helvetica", 10))

import tkinter as tk
from PIL import Image, ImageTk

class ResultsView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.bg_image = Image.open("src/assets/fondo4.png")
        self.bg_photo = ImageTk.PhotoImage(self.bg_image.resize((724, 768)))

        self.canvas = tk.Canvas(self, width=724, height=768)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, anchor="nw", image=self.bg_photo)

        self.canvas.create_text(362, 24, text="Resultados y comparativa", font=("Helvetica", 18, "bold"), fill="black")
        self.btn_atras = tk.Button(self, text="← Atrás", command=lambda: controller.show_view("SolvingView"))
        self.canvas.create_window(60, 24, window=self.btn_atras)

        # Cuadros de rendimiento
        self.canvas.create_text(190, 150, text="BACKTRACKING", font=("Helvetica", 12, "bold"), fill="white")
        self.canvas.create_text(170, 200, text="Tiempo: [1.2 ms]\nPasos: [45]\nPrecisión: [100%]",
                                font=("Helvetica", 10), fill="white", justify="center")
        
        self.canvas.create_text(540, 150, text="FUERZA BRUTA", font=("Helvetica", 12, "bold"), fill="white")
        self.canvas.create_text(500, 200, text="Tiempo: [5.8 ms]\nPasos: [120]\nPrecisión: [100%]",
                                font=("Helvetica", 10), fill="white", justify="center")

        # Barras de tiempo 
        self.canvas.create_text(362, 330, text="Tiempo de Ejecución: BT vs FB", font=("Helvetica", 12, "bold"), fill="white")

        # Barras de tiempo 
        self.canvas.create_text(362, 480, text="Numero de pasos: BT vs FB", font=("Helvetica", 12, "bold"), fill="white")
        
        # Resultados
        self.canvas.create_text(362, 640, text='Conclusión: "Backtracking fue más rápido y eficiente..."',
                                fill="white", font=("Helvetica", 12))

        # Botones
        self.btn_otro = tk.Button(self, width=22, font=("Helvetica", 14, "bold"), text="RESOLVER OTRO SUDOKU", command=lambda: controller.show_view("InputView"))
        self.btn_inicio = tk.Button(self, width=22, font=("Helvetica", 14, "bold"), text="VOLVER AL INICIO", command=lambda: controller.show_view("MainView"))
        self.canvas.create_window(210, 700, window=self.btn_otro)
        self.canvas.create_window(510, 700, window=self.btn_inicio)

    def set_resultado(self, tablero, algoritmo, pasos, backtracks):
        resultado = f"Algoritmo: {algoritmo}\nPasos: {pasos}\nBacktracks: {backtracks}\n\nTablero resuelto:\n"
        for fila in tablero:
            resultado += " ".join(fila) + "\n"
    
        self.text_widget.delete("1.0", tk.END)
        self.text_widget.insert(tk.END, resultado)


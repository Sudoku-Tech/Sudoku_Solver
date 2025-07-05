import tkinter as tk
from PIL import Image, ImageTk

class AlgorithmsInfoView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.bg_image = Image.open("src/assets/fondo.png")
        self.bg_photo = ImageTk.PhotoImage(self.bg_image.resize((724, 768)))

        self.canvas = tk.Canvas(self, width=724, height=768)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, anchor="nw", image=self.bg_photo)

        self.canvas.create_text(362, 40, text="Información sobre Algoritmos", font=("Helvetica", 16, "bold"), fill="white")
        btn_atras = tk.Button(self, text="← Atrás", command=lambda: controller.show_view("MainView"))
        self.canvas.create_window(60, 30, window=btn_atras)

        info_text = (
            "🔁 Backtracking:\n"
            "- Explora todas las soluciones posibles.\n"
            "- Se devuelve (backtrack) si el camino actual no es válido.\n"
            "- Eficiente en muchos casos, pero aún puede tardar en tableros difíciles.\n\n"
            "🔢 Fuerza Bruta:\n"
            "- Intenta todas las combinaciones posibles.\n"
            "- Mucho más costoso computacionalmente.\n"
            "- Útil para comparación teórica pero no recomendado para producción."
        )

        self.canvas.create_text(362, 180, text=info_text, font=("Helvetica", 12), fill="white", justify="center", width=600)

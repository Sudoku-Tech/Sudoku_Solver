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

        # Títulos
        self.canvas.create_text(190, 155, text="BACKTRACKING", font=("Helvetica", 12, "bold"), fill="white")
        self.canvas.create_text(540, 155, text="FUERZA BRUTA", font=("Helvetica", 12, "bold"), fill="white")

        # Datos comparativos
        self.label_bt = self.canvas.create_text(190, 215, text="", font=("Helvetica", 10), fill="white", justify="center")
        self.label_fb = self.canvas.create_text(540, 215, text="", font=("Helvetica", 10), fill="white", justify="center")

        # Barras comparativas
        self.canvas.create_text(362, 335, text="Comparativa de Tiempo de Ejecución (ms)", font=("Helvetica", 12, "bold"), fill="white")
        self.time_bar_bt = self.canvas.create_rectangle(100, 390, 100, 420, fill="green")  # antes 330–360
        self.time_bar_fb = self.canvas.create_rectangle(100, 430, 100, 460, fill="blue")   # antes 370–400
        self.label_time_bt = self.canvas.create_text(560, 380, text="", fill="white", anchor="w", font=("Helvetica", 10))
        self.label_time_fb = self.canvas.create_text(560, 420, text="", fill="white", anchor="w", font=("Helvetica", 10))

        self.canvas.create_text(362, 475, text="Comparativa de Cantidad de Pasos", font=("Helvetica", 12, "bold"), fill="white")
        self.step_bar_bt = self.canvas.create_rectangle(100, 530, 100, 560, fill="green")  # antes 470–500
        self.step_bar_fb = self.canvas.create_rectangle(100, 570, 100, 600, fill="blue")   # antes 510–540
        self.label_step_bt = self.canvas.create_text(560, 520, text="", fill="white", anchor="w", font=("Helvetica", 10))
        self.label_step_fb = self.canvas.create_text(560, 560, text="", fill="white", anchor="w", font=("Helvetica", 10))

        # Conclusión
        self.conclusion_text = self.canvas.create_text(362, 635, text="", fill="white", font=("Helvetica", 12), width=600)

        

        # Botones
        self.btn_otro = tk.Button(self, width=22, font=("Helvetica", 14, "bold"),
                                  text="RESOLVER OTRO SUDOKU", command=lambda: controller.show_view("InputView"))
        self.btn_inicio = tk.Button(self, width=22, font=("Helvetica", 14, "bold"),
                                    text="VOLVER AL INICIO", command=lambda: controller.show_view("MainView"))
        self.canvas.create_window(210, 700, window=self.btn_otro)
        self.canvas.create_window(510, 700, window=self.btn_inicio)

        # Estructura para métricas
        self.resultados = {
            "Backtracking": {"tiempo": 0, "pasos": 0, "backtracks": 0},
            "Fuerza Bruta": {"tiempo": 0, "pasos": 0, "backtracks": 0}
        }

    def set_resultado(self, tablero, algoritmo_usado, bt_metrics, fb_metrics):
        # Guardar métricas
        self.resultados["Backtracking"] = bt_metrics
        self.resultados["Fuerza Bruta"] = fb_metrics

        # Mostrar datos comparativos
        self.canvas.itemconfigure(self.label_bt, text=self._format_metrics("Backtracking"))
        self.canvas.itemconfigure(self.label_fb, text=self._format_metrics("Fuerza Bruta"))

        # Actualizar gráficas
        self._update_bars()

        # Generar conclusión
        conclusion = self._generate_conclusion()
        self.canvas.itemconfigure(self.conclusion_text, text=conclusion)

    def _format_metrics(self, algoritmo):
        r = self.resultados[algoritmo]
        return f"Tiempo: {r['tiempo']:.2f} ms\nPasos: {r['pasos']}\nBacktracks: {r['backtracks']}\nPrecisión: 100%"

    def _update_bars(self):
        bt = self.resultados["Backtracking"]
        fb = self.resultados["Fuerza Bruta"]
        max_time = max(bt["tiempo"], fb["tiempo"], 1)
        max_steps = max(bt["pasos"], fb["pasos"], 1)

        # Barras tiempo
        bt_len = int((bt["tiempo"] / max_time) * 400)
        fb_len = int((fb["tiempo"] / max_time) * 400)
        self.canvas.coords(self.time_bar_bt, 100, 365, 100 + bt_len, 395)
        self.canvas.coords(self.time_bar_fb, 100, 405, 100 + fb_len, 435)
        self.canvas.itemconfigure(self.label_time_bt, text=f"{bt['tiempo']:.2f} ms")
        self.canvas.itemconfigure(self.label_time_fb, text=f"{fb['tiempo']:.2f} ms")

        # Barras pasos
        bt_step_len = int((bt["pasos"] / max_steps) * 400)
        fb_step_len = int((fb["pasos"] / max_steps) * 400)
        self.canvas.coords(self.step_bar_bt, 100, 505, 100 + bt_step_len, 535)
        self.canvas.coords(self.step_bar_fb, 100, 545, 100 + fb_step_len, 575)
        self.canvas.itemconfigure(self.label_step_bt, text=f"{bt['pasos']} pasos")
        self.canvas.itemconfigure(self.label_step_fb, text=f"{fb['pasos']} pasos")

    def _generate_conclusion(self):
        bt = self.resultados["Backtracking"]
        fb = self.resultados["Fuerza Bruta"]
        if bt["tiempo"] < fb["tiempo"]:
            return "Conclusión: Backtracking fue más rápido y eficiente que Fuerza Bruta."
        elif fb["tiempo"] < bt["tiempo"]:
            return "Conclusión: Fuerza Bruta fue más rápida, aunque puede no escalar bien con tableros grandes."
        else:
            return "Conclusión: Ambos algoritmos tuvieron un desempeño similar."

import tkinter as tk
from PIL import Image, ImageTk
from algorithms.backtracking_solver import BacktrackingSolver
from algorithms.brute_force_solver import BruteForceSolver
import time

class SolvingView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.bg_image = Image.open("src/assets/fondo3.png")
        self.bg_photo = ImageTk.PhotoImage(self.bg_image.resize((724, 768)))

        self.canvas = tk.Canvas(self, width=724, height=768)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, anchor="nw", image=self.bg_photo)

        # Header
        self.canvas.create_text(362, 24, text="Resolviendo sudoku", font=("Helvetica", 18, "bold"), fill="black")
        self.btn_atras = tk.Button(self, text="← Atrás", command=lambda: controller.show_view("InputView"))
        self.canvas.create_window(60, 24, window=self.btn_atras)

        # Tablero
        self.grid_frame = tk.Frame(self.canvas, bg="white")
        self.entries = [[tk.Entry(self.grid_frame, width=2, justify='center') for _ in range(9)] for _ in range(9)]
        for i in range(9):
            for j in range(9):
                self.entries[i][j].grid(row=i, column=j, padx=1, pady=1)
        self.canvas.create_window(270, 200, window=self.grid_frame)

        # Selector de algoritmo
        self.algo_var = tk.StringVar(value="Backtracking")
        self.canvas.create_text(560, 120, text="SELECTOR DE ALGORITMO", font=("Helvetica", 12, "bold"), fill="white")
        btn_backtracking = tk.Radiobutton(self, font=("Helvetica", 10, "bold"), text="Backtracking", variable=self.algo_var, value="Backtracking")
        btn_fuerza_bruta = tk.Radiobutton(self, font=("Helvetica", 10, "bold"), text="Fuerza Bruta", variable=self.algo_var, value="Fuerza Bruta")
        btn_resolver = tk.Button(self, font=("Helvetica", 10, "bold"), text="RESOLVER", command=self.start_solving)
        self.canvas.create_window(500, 160, window=btn_backtracking)
        self.canvas.create_window(500, 190, window=btn_fuerza_bruta)
        self.canvas.create_window(560, 230, window=btn_resolver)

        # Controles
        self.canvas.create_text(560, 290, text="CONTROLES", font=("Helvetica", 12, "bold"), fill="white")
        
        btn_play_pausa = tk.Button(self, font=("Helvetica", 10, "bold"), text="Play/Pausa", command=self.play_animation)
        btn_pasos = tk.Button(self, font=("Helvetica", 10, "bold"), text="Paso a Paso", command=self.step_once)
        btn_reiniciar = tk.Button(self, font=("Helvetica", 10, "bold"), text="Reiniciar", command=self.reset_view)
        self.canvas.create_window(487, 330, window=btn_play_pausa)
        self.canvas.create_window(610, 330, window=btn_pasos)
        self.canvas.create_window(480, 360, window=btn_reiniciar)

        # Métricas
        self.canvas.create_text(170, 450, text="MÉTRICAS EN TIEMPO REAL", font=("Helvetica", 12, "bold"), fill="white")

        self.metrics_text = self.canvas.create_text(
            120, 520,
            text="Algoritmo Actual: [Nombre]\nTiempo Transcurrido: [0.00 ms]\nNúmero de Pasos: [0]\nBacktracks: [0]\nEstado: Buscando...",
            fill="white",
            font=("Helvetica", 10),
            justify="center"
        )

        # Botón para ir a resultados
        self.result_button = tk.Button(self, text="Ir a resultados", width=32, font=("Helvetica", 14, "bold"), command=self.ir_a_resultados)
        self.canvas.create_window(362, 700, window=self.result_button)
        self.result_button.config(state='disabled')  # Inicialmente deshabilitado



    def set_tablero(self, board):
        self.board = board
        for i in range(9):
            for j in range(9):
                self.entries[i][j].delete(0, tk.END)
                if board[i][j] != 0:
                    self.entries[i][j].insert(0, str(board[i][j]))

    def fake_solve(self):
        # Simulación 
        self.canvas.itemconfigure(self.metrics_text, text=(
            "Métricas en Tiempo Real\n"
            "Algoritmo Actual: Backtracking\n"
            "Tiempo: [1.23 ms]\n"
            "Pasos: [45]\n"
            "Backtracks: [3]\n"
            "Estado: ¡Sudoku Resuelto!"
        ))

        # Estado interno
        self.steps = []
        self.current_step_index = 0
        self.board = [[0] * 9 for _ in range(9)]
        self.solver = None
        self.timer_running = False 

    def read_board(self):
        for i in range(9):
            for j in range(9):
                val = self.entries[i][j].get()
                self.board[i][j] = int(val) if val.isdigit() else 0

    def start_solving(self):
        self.read_board()
        algo = self.algo_var.get()
        self.estado_actual = "Buscando..."

        # Guardar el tablero original antes de resolver
        self.original_board = [[self.entries[i][j].get() for j in range(9)] for i in range(9)]

        if algo == "Backtracking":
            self.solver = BacktrackingSolver(self.board)
        else:
            self.solver = BruteForceSolver(self.board)

        start_time = time.time()
        self.solver.solve()
        end_time = time.time()

        self.solving_time = (end_time - start_time) * 1000
        self.steps = self.solver.steps
        self.current_step_index = 0
        self.result_button.config(state='disabled')

        self.update_metrics(self.estado_actual)

    def step_once(self):
        if self.current_step_index < len(self.steps):
            i, j, val = self.steps[self.current_step_index]
            self.entries[i][j].delete(0, tk.END)
            if val == 0:
                self.entries[i][j].config(bg="red")
                self.estado_actual = "Backtracking"
            else:
                self.entries[i][j].insert(0, str(val))
                self.entries[i][j].config(bg="turquoise")
                self.estado_actual = "Buscando..."

            self.update_metrics(self.estado_actual)
            self.current_step_index += 1
        else:
            # Verifica si el tablero está completamente lleno
            if all(all(cell.get().isdigit() and cell.get() != "0" for cell in row) for row in self.entries):
                self.estado_actual = "¡Solución Encontrada!"
            else:
                self.estado_actual = "No hay solución"
            self.update_metrics(self.estado_actual)
            self.result_button.config(state='normal')

    def play_animation(self):
        if self.current_step_index < len(self.steps):
            self.step_once()
            self.after(100, self.play_animation)  # 100ms delay
        else:
            self.update_metrics("¡Sudoku resuelto!")

    def update_metrics(self, state):
        text = (
            f"Algoritmo Actual: {self.algo_var.get()}\n"
            f"Tiempo Transcurrido: {self.solving_time:.2f} ms\n"
            f"Número de Pasos: {self.current_step_index}/{len(self.steps)}\n"
            f"Backtracks: {getattr(self.solver, 'backtracks', 0)}\n"
            f"Estado Actual: {state}"
        )
        self.canvas.itemconfigure(self.metrics_text, text=text)

    def reset_view(self):
        for i in range(9):
            for j in range(9):
                valor_original = self.original_board[i][j] if hasattr(self, 'original_board') else ""
                self.entries[i][j].delete(0, tk.END)
                if valor_original.isdigit() and valor_original != "0":
                    self.entries[i][j].insert(0, valor_original)
                self.entries[i][j].config(bg="white")
        self.steps = []
        self.current_step_index = 0
        self.result_button.config(state='disabled')
        self.update_metrics("Reiniciado.")      
    
    def ir_a_resultados(self):
        resultado_final = [[self.entries[i][j].get() or "0" for j in range(9)] for i in range(9)]
        self.controller.views["ResultsView"].set_resultado(
            resultado_final,
            self.algo_var.get(),
            len(self.steps),
            getattr(self.solver, 'backtracks', 0),
            self.solving_time
        )
        self.controller.show_view("ResultsView")


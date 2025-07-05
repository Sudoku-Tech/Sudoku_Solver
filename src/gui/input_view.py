import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import random

# Función para generar tablero Sudoku
def generar_tablero(dificultad='medio'):
    def es_valido(tablero, fila, col, num):
        for i in range(9):
            if tablero[fila][i] == num or tablero[i][col] == num:
                return False
        start_row, start_col = 3 * (fila // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if tablero[i][j] == num:
                    return False
        return True

    def resolver(tablero):
        for i in range(9):
            for j in range(9):
                if tablero[i][j] == 0:
                    nums = list(range(1, 10))
                    random.shuffle(nums)
                    for num in nums:
                        if es_valido(tablero, i, j, num):
                            tablero[i][j] = num
                            if resolver(tablero):
                                return True
                            tablero[i][j] = 0
                    return False
        return True

    tablero = [[0 for _ in range(9)] for _ in range(9)]
    resolver(tablero)

    if dificultad == 'fácil':
        vacías = 30
    elif dificultad == 'medio':
        vacías = 45
    else:  # difícil
        vacías = 60

    count = 0
    while count < vacías:
        i, j = random.randint(0, 8), random.randint(0, 8)
        if tablero[i][j] != 0:
            tablero[i][j] = 0
            count += 1

    return tablero

# Clase de la vista
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

        # Tablero editable
        self.grid_frame = tk.Frame(self.canvas, bg="white")
        large_cell_font = ("Helvetica", 24)
        self.entries = [[tk.Entry(self.grid_frame, width=2, justify='center', font=large_cell_font) for _ in range(9)] for _ in range(9)]
        for i in range(9):
            for j in range(9):
                self.entries[i][j].grid(row=i, column=j, padx=1, pady=1)
        self.canvas.create_window(362, 260, window=self.grid_frame)

        # Selector de dificultad
        self.dificultad_var = tk.StringVar(value="Medio")
        opciones = ["Fácil", "Medio", "Difícil"]
        self.selector_dificultad = tk.OptionMenu(self, self.dificultad_var, *opciones)
        self.canvas.create_window(362, 500, window=self.selector_dificultad)

        # Botones de acción
        self.btn_gen = tk.Button(self, width=22, font=("Helvetica", 14, "bold"), text="GENERAR ALEATORIO", command=self.generar_tablero_en_vista)
        self.btn_cargar = tk.Button(self, width=22, font=("Helvetica", 14, "bold"), text="CARGAR TABLERO", command=self.cargar_tablero_desde_txt)
        self.btn_borrar = tk.Button(self, width=22, font=("Helvetica", 14, "bold"), text="BORRAR TABLERO", command=self.borrar_tablero)
        self.btn_resolver = tk.Button(self, width=22, font=("Helvetica", 14, "bold"), text="RESOLVER", command=self.enviar_a_solving)

        self.canvas.create_window(210, 550, window=self.btn_gen)
        self.canvas.create_window(510, 550, window=self.btn_cargar)
        self.canvas.create_window(210, 600, window=self.btn_borrar)
        self.canvas.create_window(510, 600, window=self.btn_resolver)

        self.canvas.create_text(362, 650, text="¡TU TABLERO ESTÁ LISTO!", fill="white", font=("Helvetica", 10))

    def generar_tablero_en_vista(self):
        dificultad = self.dificultad_var.get().lower()
        tablero = generar_tablero(dificultad)
        for i in range(9):
            for j in range(9):
                self.entries[i][j].delete(0, tk.END)
                if tablero[i][j] != 0:
                    self.entries[i][j].insert(0, str(tablero[i][j]))

    def borrar_tablero(self):
        for i in range(9):
            for j in range(9):
                self.entries[i][j].delete(0, tk.END)

    def cargar_tablero_desde_txt(self):
        ruta = filedialog.askopenfilename(
            filetypes=[("Archivos de texto", "*.txt")],
            title="Selecciona un archivo de tablero"
        )

        if not ruta:
            return  # Cancelado

        try:
            with open(ruta, "r") as archivo:
                lineas = archivo.readlines()

            if len(lineas) != 9:
                raise ValueError("El archivo debe tener exactamente 9 líneas.")

            for i in range(9):
                fila = lineas[i].strip()
                if len(fila) != 9 or not fila.isdigit():
                    raise ValueError(f"La línea {i+1} debe tener 9 dígitos (sin espacios).")

                for j in range(9):
                    self.entries[i][j].delete(0, tk.END)
                    if fila[j] != "0":
                        self.entries[i][j].insert(0, fila[j])

            messagebox.showinfo("Cargado", "¡Tablero cargado con éxito!")

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el tablero:\n{str(e)}")
    
    def enviar_a_solving(self):
        board = [[0 for _ in range(9)] for _ in range(9)]
        for i in range(9):
            for j in range(9):
                val = self.entries[i][j].get()
                board[i][j] = int(val) if val.isdigit() else 0
    
        self.controller.views["SolvingView"].set_tablero(board)
        self.controller.show_view("SolvingView")
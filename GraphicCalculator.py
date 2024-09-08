import tkinter as tk
from tkinter import ttk

class VonNeumannSimulatorWithGraphics:
    def __init__(self, master):
        self.master = master
        master.title("Simulador de Máquina de Von Neumann")
        
        self.memory = ['00000100', '01010101', '01100111', '01110000', '01001011', '01010101', '00000000', '00000000']
        self.program_counter = 0
        self.instruction_register = ''
        self.accumulator = '00000000'
        self.alu_result = '00000000'
        self.current_step = 0
        self.operation_complete = False

        self.create_widgets()
        self.apply_styles()

    def create_widgets(self):
        # Frame para el diagrama
        self.diagram_frame = ttk.LabelFrame(self.master, text="Diagrama del Sistema")
        self.diagram_frame.grid(row=0, column=0, padx=10, pady=10)

        self.canvas = tk.Canvas(self.diagram_frame, width=500, height=400, bg="white")
        self.canvas.pack()

        # Dibujar los componentes principales de la arquitectura
        self.draw_diagram()

        # CPU y controles
        self.cpu_frame = ttk.LabelFrame(self.master, text="CPU")
        self.cpu_frame.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(self.cpu_frame, text="Contador de Programa:").grid(row=0, column=0, sticky="w")
        self.pc_label = ttk.Label(self.cpu_frame, text="0")
        self.pc_label.grid(row=0, column=1, sticky="w")

        ttk.Label(self.cpu_frame, text="Registro de Instrucción:").grid(row=1, column=0, sticky="w")
        self.ir_label = ttk.Label(self.cpu_frame, text="")
        self.ir_label.grid(row=1, column=1, sticky="w")

        ttk.Label(self.cpu_frame, text="Acumulador:").grid(row=2, column=0, sticky="w")
        self.acc_label = ttk.Label(self.cpu_frame, text=self.accumulator)
        self.acc_label.grid(row=2, column=1, sticky="w")

        ttk.Label(self.cpu_frame, text="ALU:").grid(row=3, column=0, sticky="w")
        self.alu_label = ttk.Label(self.cpu_frame, text=self.alu_result)
        self.alu_label.grid(row=3, column=1, sticky="w")

        # Controles
        self.next_button = ttk.Button(self.master, text="Siguiente Paso", command=self.next_step)
        self.next_button.grid(row=1, column=0, padx=10, pady=10)
        
        self.reset_button = ttk.Button(self.master, text="Reiniciar Simulación", command=self.reset_simulation)
        self.reset_button.grid(row=1, column=1, padx=10, pady=10)

        self.status_label = ttk.Label(self.master, text="")
        self.status_label.grid(row=2, column=0, columnspan=2)

    def apply_styles(self):
        # Aplicar estilos personalizados
        style = ttk.Style()
        style.configure('TButton',
                        font=('Helvetica', 12, 'bold'),
                        padding=10,
                        relief='raised',
                        background='#4CAF50',
                        foreground='black')
        style.configure('TButton:hover',
                        background='#45a049')
        style.configure('TLabel',
                        font=('Helvetica', 10),
                        padding=5)
        style.configure('TLabelFrame',
                        font=('Helvetica', 12, 'bold'),
                        padding=10)

        # Ajustar colores y bordes de los botones
        self.next_button.configure(style='TButton')
        self.reset_button.configure(style='TButton')
        self.status_label.configure(style='TLabel')

    def draw_diagram(self):
        # Dibujar la representación gráfica de la CPU, memoria, etc.
        self.memory_rect = self.canvas.create_rectangle(50, 50, 150, 100, fill="lightgray", outline="black")
        self.canvas.create_text(100, 75, text="Memoria")

        self.cpu_rect = self.canvas.create_rectangle(200, 50, 300, 100, fill="lightblue", outline="black")
        self.canvas.create_text(250, 75, text="CPU")

        self.canvas.create_line(150, 75, 200, 75, arrow=tk.LAST)

        # Dibujar las celdas de la memoria para hacerlas dinámicas
        self.memory_cells = []
        for i in range(len(self.memory)):
            rect = self.canvas.create_rectangle(50, 120 + i*30, 150, 150 + i*30, fill="white", outline="black")
            text = self.canvas.create_text(100, 135 + i*30, text=self.memory[i])
            self.memory_cells.append((rect, text))

        # Celda para la operación OR (ALU)
        self.alu_rect = self.canvas.create_rectangle(200, 120, 300, 170, fill="lightgreen", outline="black")
        self.canvas.create_text(250, 145, text="ALU (OR)")

    def update_memory_diagram(self):
        # Actualizar el contenido de la memoria en el canvas
        for i, (rect, text) in enumerate(self.memory_cells):
            self.canvas.itemconfig(text, text=self.memory[i])
            if i == self.program_counter:
                self.canvas.itemconfig(rect, fill="yellow")  # Resaltar la celda que se está utilizando
            else:
                self.canvas.itemconfig(rect, fill="white")  # Restaurar el color de las demás celdas

    def highlight_memory(self):
        # Cambiar color cuando la memoria se actualiza
        self.canvas.itemconfig(self.memory_rect, fill="yellow")

    def highlight_cpu(self):
        # Cambiar color cuando la CPU se actualiza
        self.canvas.itemconfig(self.cpu_rect, fill="green")

    def highlight_alu(self):
        # Cambiar color cuando la ALU realiza la operación OR
        self.canvas.itemconfig(self.alu_rect, fill="orange")

    def reset_colors(self):
        # Resetear los colores originales
        self.canvas.itemconfig(self.memory_rect, fill="lightgray")
        self.canvas.itemconfig(self.cpu_rect, fill="lightblue")
        self.canvas.itemconfig(self.alu_rect, fill="lightgreen")

    def next_step(self):
        # Cambiar los colores según el paso
        if self.operation_complete:
            self.status_label.config(text="La operación ya ha finalizado.")
            return
        
        if self.current_step == 0:
            self.fetch()
        elif self.current_step == 1:
            self.decode()
        elif self.current_step == 2:
            self.execute()
        elif self.current_step == 3:
            self.store()
            self.operation_complete = True
            self.status_label.config(text="La operación ha finalizado.")
        
        self.current_step = (self.current_step + 1) % 4
        self.update_display()

    def reset_simulation(self):
        # Reiniciar la simulación
        self.memory = ['00000100', '01010101', '01100111', '01110000', '01001011', '01010101', '00000000', '00000000']
        self.program_counter = 0
        self.accumulator = '00000000'
        self.alu_result = '00000000'
        self.current_step = 0
        self.operation_complete = False
        self.reset_colors()
        self.status_label.config(text="Simulación reiniciada.")
        self.update_display()

    def fetch(self):
        self.instruction_register = self.memory[self.program_counter]
        self.program_counter += 1
        self.status_label.config(text="Fetch: Instrucción cargada en el registro de instrucción.")
        self.highlight_memory()  # Cambiar color al cargar la instrucción

    def decode(self):
        self.status_label.config(text="Decode: Operación OR identificada.")
        self.highlight_alu()  # Cambiar color al identificar la operación OR

    def execute(self):
        operand1 = int(self.memory[4], 2)
        operand2 = int(self.memory[5], 2)
        result = operand1 | operand2
        self.alu_result = format(result, '08b')
        self.status_label.config(text="Execute: Operación OR realizada en la ALU.")
        self.highlight_cpu()  # Cambiar color al realizar la operación en la ALU

    def store(self):
        self.accumulator = self.alu_result
        self.memory[6] = self.accumulator
        self.status_label.config(text="Store: Resultado almacenado en el acumulador y la memoria.")
        self.highlight_memory()  # Cambiar color al almacenar el resultado

    def update_display(self):
        self.pc_label.config(text=str(self.program_counter))
        self.ir_label.config(text=self.instruction_register)
        self.acc_label.config(text=self.accumulator)
        self.alu_label.config(text=self.alu_result)
        self.update_memory_diagram()  # Actualizar la memoria en el canvas

root = tk.Tk()
simulator = VonNeumannSimulatorWithGraphics(root)
root.mainloop()

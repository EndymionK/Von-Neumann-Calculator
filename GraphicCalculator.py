import tkinter as tk
from tkinter import ttk
import time

class VonNeumannSimulator:
    def __init__(self, master):
        self.master = master
        master.title("Simulador de Máquina de von Neumann")
        
        self.memory = ['00000100', '01010101', '01100111', '01110000', '01001011', '01010101', '00000000', '00000000']
        self.program_counter = 0
        self.instruction_register = ''
        self.accumulator = '00000000'
        self.alu_result = '00000000'
        self.current_step = 0
        self.operation_complete = False
        
        self.create_widgets()
        
    def create_widgets(self):
        # Componentes principales
        self.memory_frame = ttk.LabelFrame(self.master, text="Memoria")
        self.memory_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        self.cpu_frame = ttk.LabelFrame(self.master, text="CPU")
        self.cpu_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        self.control_frame = ttk.Frame(self.master)
        self.control_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        
        # Memoria
        self.memory_labels = []
        for i in range(8):
            label = ttk.Label(self.memory_frame, text=f"{i}: {self.memory[i]}")
            label.grid(row=i, column=0, padx=5, pady=2)
            self.memory_labels.append(label)
        
        # CPU
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
        self.next_button = ttk.Button(self.control_frame, text="Siguiente Paso", command=self.next_step)
        self.next_button.grid(row=0, column=0, padx=5, pady=5)
        
        self.close_button = ttk.Button(self.control_frame, text="Cerrar", command=self.master.quit)
        self.close_button.grid(row=0, column=1, padx=5, pady=5)
        
        self.status_label = ttk.Label(self.control_frame, text="")
        self.status_label.grid(row=1, column=0, columnspan=2, pady=5)
        
    def next_step(self):
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
        
    def fetch(self):
        self.instruction_register = self.memory[self.program_counter]
        self.program_counter += 1
        self.status_label.config(text="Fetch: Instrucción cargada en el registro de instrucción.")
        
    def decode(self):
        # En este caso, sabemos que es una operación OR
        self.status_label.config(text="Decode: Operación OR identificada.")
        
    def execute(self):
        operand1 = int(self.memory[4], 2)
        operand2 = int(self.memory[5], 2)
        result = operand1 | operand2
        self.alu_result = format(result, '08b')
        self.status_label.config(text="Execute: Operación OR realizada en la ALU.")
        
    def store(self):
        self.accumulator = self.alu_result
        self.memory[6] = self.accumulator
        self.status_label.config(text="Store: Resultado almacenado en el acumulador y la memoria.")
        
    def update_display(self):
        for i, label in enumerate(self.memory_labels):
            label.config(text=f"{i}: {self.memory[i]}")
        self.pc_label.config(text=str(self.program_counter))
        self.ir_label.config(text=self.instruction_register)
        self.acc_label.config(text=self.accumulator)
        self.alu_label.config(text=self.alu_result)

root = tk.Tk()
simulator = VonNeumannSimulator(root)
root.mainloop()
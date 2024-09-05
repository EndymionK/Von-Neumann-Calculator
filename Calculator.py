class Memory:
    def __init__(self):
        # Simulamos la memoria con las instrucciones y datos
        self.memory = [0] * 256  # Memoria de 256 espacios
    
    def load_instruction(self, address):
        # Fetch: Obtener la instrucción desde la memoria
        return self.memory[address]
    
    def store_result(self, address, value):
        # Store: Guardar el resultado de la operación en memoria
        self.memory[address] = value

class Register:
    def __init__(self):
        self.accumulator = 0  # Registro acumulador
        self.program_counter = 0  # Contador de programa

class ALU:
    def or_operation(self, value1, value2):
        # Simula la operación OR en la ALU
        return value1 | value2

class ControlUnit:
    def __init__(self, memory, alu, registers):
        self.memory = memory
        self.alu = alu
        self.registers = registers
    
    def fetch(self):
        # Fetch: Obtener la instrucción actual
        instruction = self.memory.load_instruction(self.registers.program_counter)
        self.registers.program_counter += 1
        return instruction
    
    def decode(self, instruction):
        # Decode: Decodificar la instrucción (en este caso, OR)
        if instruction == "OR":
            return "OR"
        return None
    
    def execute(self, operation, operand1, operand2):
        # Execute: Ejecutar la operación decodificada en la ALU
        if operation == "OR":
            return self.alu.or_operation(operand1, operand2)

def user_interaction(is_completed):
    print("\nOpciones:")
    if not is_completed:
        print("1. Avanzar al siguiente paso")
    print("2. Reiniciar simulación")
    print("3. Salir")

    choice = input("\nElige una opción (1/2/3): ")
    return choice

def simulate():
    operand1 = 0b01001011  # Primer operando (01001011)
    operand2 = 0b01010101  # Segundo operando (01010101)

    while True:
        memory = Memory()
        registers = Register()
        alu = ALU()
        control_unit = ControlUnit(memory, alu, registers)

        # Cargar la instrucción OR en la memoria
        memory.memory[0] = "OR"

        steps = ["fetch", "decode", "execute", "store"]
        current_step = 0
        simulation_completed = False

        while True:
            choice = user_interaction(simulation_completed)

            if choice == "1" and not simulation_completed:
                if current_step < len(steps):
                    if steps[current_step] == "fetch":
                        # Fetch
                        instruction = control_unit.fetch()
                        print(f"Fetch: Instrucción obtenida: {instruction}")

                    elif steps[current_step] == "decode":
                        # Decode
                        operation = control_unit.decode(instruction)
                        print(f"Decode: Operación decodificada: {operation}")

                    elif steps[current_step] == "execute":
                        # Execute
                        result = control_unit.execute(operation, operand1, operand2)
                        print(f"Execute: Resultado de {bin(operand1)} OR {bin(operand2)} = {bin(result)}")

                    elif steps[current_step] == "store":
                        # Store
                        control_unit.memory.store_result(1, result)
                        print(f"Store: Resultado almacenado en la memoria en la dirección 1: {bin(memory.memory[1])}")

                    current_step += 1
                if current_step == len(steps):
                    simulation_completed = True
                    print("\nSimulación completada. Ya no puedes avanzar más pasos.")

            elif choice == "2":
                # Reiniciar la simulación
                print("Reiniciando la simulación...\n")
                break

            elif choice == "3":
                # Salir del programa
                print("Saliendo de la simulación.")
                return

            elif choice == "1" and simulation_completed:
                print("Simulación ya completada. Reinicia o sal del programa.")

            else:
                print("Opción inválida. Intenta de nuevo.")

# Ejecutar la simulación
simulate()

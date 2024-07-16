import argparse
import threading
import time
import random
import msvcrt

# Argument parser setup
parser = argparse.ArgumentParser(description="Simulación de filósofos y tenedores.")
parser.add_argument('--num_filosofos', type=int, default=5, help='Número de filósofos(por defecto 5)')
args = parser.parse_args()

# Variables iniciales
num_filosofos = args.num_filosofos
num_tenedores = num_filosofos
tenedores_sem = [threading.Semaphore(1) for _ in range(num_tenedores)]
mutex = threading.Semaphore(1)

# Variables para la traza
stop_program = False
max_thinking_time = [0] * num_filosofos
max_eating_time = [0] * num_filosofos
thinking_counts = [0] * num_filosofos
eating_counts = [0] * num_filosofos
trace_lock = threading.Lock()

# Función del filósofo
def filosofo(indice):
    """
    Simulates the behavior of a philosopher.

    Args:
        indice (int): The index of the philosopher.

    Returns:
        None

    Raises:
        None
    """
    global max_thinking_time, max_eating_time, thinking_counts, eating_counts
    while not stop_program:
        thinking_time = random.randint(1, 5)
        print(f"El filósofo {indice} está pensando...")
        time.sleep(thinking_time)
        with trace_lock:
            thinking_counts[indice] += 1
            if thinking_time > max_thinking_time[indice]:
                max_thinking_time[indice] = thinking_time

        mutex.acquire()
        tenedores_sem[indice].acquire()
        tenedores_sem[(indice + 1) % num_tenedores].acquire()
        mutex.release()

        eating_time = random.randint(1, 5)
        print(f"El filósofo {indice} está comiendo...")
        time.sleep(eating_time)
        with trace_lock:
            eating_counts[indice] += 1
            if eating_time > max_eating_time[indice]:
                max_eating_time[indice] = eating_time

        tenedores_sem[indice].release()
        tenedores_sem[(indice + 1) % num_tenedores].release()

# Función para monitorear la tecla 'ESC'
def monitor_stop():
    """
    Monitors keyboard input to check if the 'ESC' key is pressed.
    If the 'ESC' key is pressed, sets the global variable 'stop_program' to True and exits the program.
    """
    global stop_program
    while True:
        if msvcrt.kbhit():
            key = msvcrt.getch()
            if key == b'\x1b':  # La tecla 'ESC' está representada por '\x1b'
                stop_program = True
                print("Se presionó 'ESC'. Saliendo del programa...")
                break

# Registrar el tiempo de inicio del programa
start_time = time.time()

# Crear y empezar hilos de filósofos
hilos_filosofos = []
for i in range(num_filosofos):
    hilo = threading.Thread(target=filosofo, args=(i,))
    hilos_filosofos.append(hilo)
    hilo.start()

# Crear y empezar el hilo para monitorear la tecla 'ESC'
hilo_monitor = threading.Thread(target=monitor_stop)
hilo_monitor.start()

# Esperar a que se detengan todos los hilos
for hilo in hilos_filosofos:
    hilo.join()
hilo_monitor.join()

# Registrar el tiempo de fin del programa
end_time = time.time()
total_execution_time = end_time - start_time

# Guardar la traza en un archivo
with trace_lock:
    try:
        with open("trace.txt", "r") as file:
            existing_content = file.read()
    except FileNotFoundError:
        existing_content = ""


    with open("trace.txt", "w") as file:
        new_trace = '*'*50 + "\n"
        new_trace += "Algoritmo Filósofos-Comensales\n\n" 
        new_trace += f"Cantidad de filósofos: {num_filosofos}\n"
        for i in range(num_filosofos):
            new_trace += f"    Filósofo {i} pensó {thinking_counts[i]} veces\n"
            new_trace += f"    Filósofo {i} comió {eating_counts[i]} veces\n"
        new_trace += f"\nTiempo máximo comiendo: {max(max_eating_time):.2f} segundos\n"
        new_trace += f"Tiempo máximo pensando: {max(max_thinking_time):.2f} segundos\n"
        new_trace += f"Tiempo total de ejecución del algoritmo: {total_execution_time:.2f} segundos\n"
        new_trace += '*'*50 + "\n"
        file.write(new_trace + existing_content)
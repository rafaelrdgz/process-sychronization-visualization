import threading
import queue
import time
import random
import sys
import msvcrt

# Variable global para controlar la finalización del programa
stop_program = False

# Variables globales para la traza
num_producers = 0
num_consumers = 0
max_production_time = 0
max_consumption_time = 0
items_produced = []
items_consumed = []
total_execution_time = 0

# Bloqueo para proteger el acceso a las variables globales
trace_lock = threading.Lock()

def producer(q, empty_semaphore, full_semaphore, producer_id):
    """
    Producer function that adds items to a queue.

    Args:
        q (Queue): The queue to add items to.
        empty_semaphore (Semaphore): Semaphore indicating the availability of empty slots in the queue.
        full_semaphore (Semaphore): Semaphore indicating the availability of items in the queue.
        producer_id (int): The ID of the producer.

    Returns:
        None
    """
    global max_production_time
    items_produced[producer_id] = 0
    while not stop_program:
        empty_semaphore.acquire()  # Wait until there is space in the queue
        item = random.randint(1, 10)
        t = random.random()
        time.sleep(t)
        with trace_lock:
            items_produced[producer_id] += 1
            if t > max_production_time:
                max_production_time = t
        print(f"Productor {producer_id} produjo {item} en {t:.2f} segundos")
        q.put(item)
        print(f"Productor {producer_id}: Elemento añadido a la cola.")
        full_semaphore.release()  # Indicate that a new item is available

def consumer(q, empty_semaphore, full_semaphore, consumer_id):
    """
    Consumer function that consumes items from a queue.

    Args:
        q (Queue): The queue from which items are consumed.
        empty_semaphore (Semaphore): Semaphore indicating the availability of empty spaces in the queue.
        full_semaphore (Semaphore): Semaphore indicating the availability of items in the queue.
        consumer_id (int): The ID of the consumer.

    Returns:
        None
    """
    global max_consumption_time
    items_consumed[consumer_id] = 0
    while not stop_program:
        full_semaphore.acquire()  # Wait until there are items in the queue
        item = q.get()
        t = random.random()
        print(f"Consumidor {consumer_id} consumió {item} en {t:.2f} segundos")
        print(f"Consumidor {consumer_id}: Elemento retirado de la cola.")
        time.sleep(t)
        with trace_lock:
            items_consumed[consumer_id] += 1
            if t > max_consumption_time:
                max_consumption_time = t
        empty_semaphore.release()  # Indicates that a new space is available
        q.task_done()

import msvcrt

def monitor_stop():
    """
    Monitors keyboard input for the Esc key and sets the stop_program flag to True if it is pressed.

    This function continuously checks for keyboard input using the msvcrt module. If the Esc key is pressed,
    it sets the global variable stop_program to True and prints a message indicating that the program is
    exiting. The function then breaks out of the loop.

    Note: This function assumes that the global variable stop_program has been defined elsewhere in the code.

    """
    global stop_program
    while True:
        if msvcrt.kbhit():
            key = msvcrt.getch()
            if key == b'\x1b':  # Esc key is represented by '\x1b'
                stop_program = True
                print("Se presionó 'Esc'. Saliendo del programa...")
                break

def main():
    """
    Entry point of the program.
    
    Parses command line arguments to determine the number of producers and consumers.
    Initializes the lists for production and consumption.
    Creates and starts producer and consumer threads.
    Monitors the 'Esc' key.
    Waits for all threads to finish.
    Calculates the total execution time.
    Writes the trace information to a file.
    """
    global num_producers, num_consumers, total_execution_time
    if len(sys.argv) > 1 and sys.argv[1] in ("-h", "--help"):
        print("Uso: python producer-consumer.py [num_productores] [num_consumidores]")
        print("  num_productores: Número de productores (opcional) (por defecto 1)")
        print("  num_consumidores: Número de consumidores (opcional) (por defecto 1)")
        sys.exit(0)

    num_producers = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    num_consumers = int(sys.argv[2]) if len(sys.argv) > 2 else 1

    # Inicializar listas de producción y consumo
    global items_produced, items_consumed
    items_produced = [0] * (num_producers + 1)
    items_consumed = [0] * (num_consumers + 1)

    q = queue.Queue(10)
    empty_semaphore = threading.Semaphore(q.maxsize)
    full_semaphore = threading.Semaphore(0)

    start_time = time.time()

    producer_threads = []
    for i in range(num_producers):
        thread = threading.Thread(target=producer, args=(q, empty_semaphore, full_semaphore, i + 1))
        thread.start()
        producer_threads.append(thread)

    consumer_threads = []
    for i in range(num_consumers):
        thread = threading.Thread(target=consumer, args=(q, empty_semaphore, full_semaphore, i + 1))
        thread.start()
        consumer_threads.append(thread)

    # Hilo para monitorear la tecla 'Esc'
    threading.Thread(target=monitor_stop).start()

    q.join()

    # Esperar a que todos los hilos terminen
    for thread in producer_threads:
        thread.join()

    for thread in consumer_threads:
        thread.join()

    end_time = time.time()
    total_execution_time = end_time - start_time

    try:
        with open("trace.txt", "r") as file:
            existing_content = file.read()
    except FileNotFoundError:
        existing_content = ""
 
 
    with open("trace.txt", "w") as file:
        new_trace = '*'*50 + "\n"
        new_trace += "Algoritmo Productor-Consumidor\n" 
        
        new_trace += f"\nCantidad de productores: {num_producers}\n"
        for i in range(1, num_producers + 1):
            new_trace += f"    Productor {i} produjo {items_produced[i]} items\n"
        new_trace += f"Tiempo máximo de producción: {max_production_time:.2f} segundos\n"
        
        new_trace += f"\nCantidad de consumidores: {num_consumers}\n"
        for i in range(1, num_consumers + 1):
            new_trace += f"    Consumidor {i} consumió {items_consumed[i]} items\n"
        new_trace += f"Tiempo máximo de consumición: {max_consumption_time:.2f} segundos\n"

        new_trace += f"\nTiempo total de ejecución del algoritmo: {total_execution_time:.2f} segundos\n{'*'*50}\n"
        file.write(new_trace + existing_content)
   

if __name__ == "__main__":
    main()

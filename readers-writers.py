import argparse
import threading
import time
import random
import msvcrt

# Variable global para controlar la finalización del programa
stop_program = False

class ReadersWriters:
    """
    A class that implements the Readers-Writers problem using semaphores and locks.

    Attributes:
        read_count (int): The number of active readers.
        resource (threading.Semaphore): A semaphore to control access to the shared resource.
        read_count_lock (threading.Lock): A lock to synchronize access to the read_count variable.
        blocked_count (int): The number of writers blocked waiting for the resource.
        max_read_time (float): The maximum time spent by a reader reading.
        max_write_time (float): The maximum time spent by a writer writing.
        read_counts (list): A list to store the number of reads performed by each reader.
        write_counts (list): A list to store the number of writes performed by each writer.
    """

    def __init__(self):
        self.read_count = 0
        self.resource = threading.Semaphore(1)
        self.read_count_lock = threading.Lock()
        self.blocked_count = 0

        # Variables for tracing
        self.max_read_time = 0
        self.max_write_time = 0
        self.read_counts = []
        self.write_counts = []

    def reader(self, id, max_read_time):
        """
        Simulates a reader accessing the shared resource.

        Args:
            id (int): The ID of the reader.
            max_read_time (float): The maximum time a reader can spend reading.

        Returns:
            None
        """
        global stop_program
        self.read_counts[id] = 0
        while not stop_program:
            start_time = time.time()

            with self.read_count_lock:
                self.read_count += 1
                if self.read_count == 1:
                    self.resource.acquire()

            print(f"Reader {id} is reading")
            reading_time = random.uniform(0, max_read_time)
            time.sleep(reading_time)
            self.max_read_time = max(self.max_read_time, reading_time)
            self.read_counts[id] += 1

            with self.read_count_lock:
                self.read_count -= 1
                if self.read_count == 0:
                    self.resource.release()

            print(f"Reader {id} finished reading")
            time.sleep(random.uniform(0, max_read_time))

    def writer(self, id, max_write_time):
        """
        Simulates a writer accessing the shared resource.

        Args:
            id (int): The ID of the writer.
            max_write_time (float): The maximum time a writer can spend writing.

        Returns:
            None
        """
        global stop_program
        self.write_counts[id] = 0
        while not stop_program:
            start_time = time.time()

            acquired = self.resource.acquire(blocking=False)
            if not acquired:
                self.blocked_count += 1
                self.resource.acquire()

            print(f"Writer {id} is writing")
            writing_time = random.uniform(0, max_write_time)
            time.sleep(writing_time)
            self.max_write_time = max(self.max_write_time, writing_time)
            self.write_counts[id] += 1

            self.resource.release()
            print(f"Writer {id} finished writing")
            time.sleep(random.uniform(0, max_write_time))

def monitor_stop():
    """
    Monitors the keyboard for the 'ESC' key press to stop the program.

    This function continuously checks for keyboard input using the `msvcrt.kbhit()` function.
    If the 'ESC' key is pressed, it sets the global variable `stop_program` to True and prints a message.
    The function then breaks out of the loop, stopping the program.

    Note: This function requires the `msvcrt` module to be imported.

    Returns:
        None
    """
    global stop_program
    while True:
        if msvcrt.kbhit():
            key = msvcrt.getch()
            if key == b'\x1b':
                stop_program = True
                print("Se presionó 'ESC'. Saliendo del programa...")
                break

def main():
    """
    Simulate the Readers-Writers problem with semaphores.

    This function takes command line arguments to configure the simulation parameters,
    creates reader and writer threads, and monitors the execution of the simulation.

    Args:
        --readers (int): Number of reader processes. Default is 5.
        --writers (int): Number of writer processes. Default is 2.
        --max_read_time (int): Maximum time a reader spends reading. Default is 3.
        --max_write_time (int): Maximum time a writer spends writing. Default is 3.
    """

    parser = argparse.ArgumentParser(description="Simulate the Readers-Writers problem with semaphores.")
    parser.add_argument('--readers', type=int, default=5, help='Number of reader processes.')
    parser.add_argument('--writers', type=int, default=2, help='Number of writer processes.')
    parser.add_argument('--max_read_time', type=int, default=3, help='Maximum time a reader spends reading.')
    parser.add_argument('--max_write_time', type=int, default=3, help='Maximum time a writer spends writing.')
    args = parser.parse_args()

    rw = ReadersWriters()
    rw.read_counts = [0] * args.readers
    rw.write_counts = [0] * args.writers

    threads = []
    for i in range(args.readers):
        t = threading.Thread(target=rw.reader, args=(i, args.max_read_time))
        t.start()
        threads.append(t)

    for i in range(args.writers):
        t = threading.Thread(target=rw.writer, args=(i, args.max_write_time))
        t.start()
        threads.append(t)

    # Hilo para monitorear la tecla 'ESC'
    monitor_thread = threading.Thread(target=monitor_stop)
    monitor_thread.start()

    for t in threads:
        t.join()

    monitor_thread.join()

    total_execution_time = time.time() - start_time

    # Leer el contenido existente del archivo
    try:
        with open("trace.txt", "r") as file:
            existing_content = file.read()
    except FileNotFoundError:
        existing_content = ""

    # Guardar la nueva traza al inicio del archivo
    with open("trace.txt", "w") as file:
        file.write("*"*50 + "\n")
        file.write("Algoritmo de Lector-Escritor\n\n")
        file.write(f"Cantidad de lectores: {args.readers}\n")
        for i in range(args.readers):
            file.write(f"    Lector {i} leyó {rw.read_counts[i]} veces\n")
        file.write(f"Tiempo máximo de lectura: {rw.max_read_time:.2f} segundos\n\n")
        file.write(f"Cantidad de escritores: {args.writers}\n")
        for i in range(args.writers):
            file.write(f"    Escritor {i} escribió {rw.write_counts[i]} veces\n")
        file.write(f"Tiempo máximo de escritura: {rw.max_write_time:.2f} segundos\n\n")
        file.write(f"Tiempo total de ejecución del algoritmo: {total_execution_time:.2f} segundos\n")
        file.write("*"*50 + "\n")
        file.write(existing_content)

if __name__ == "__main__":
    start_time = time.time()  # Registrar el tiempo de inicio del programa
    main()

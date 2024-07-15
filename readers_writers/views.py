import json
import threading
import time
import random
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

# Variables globales para controlar la simulación
running = False
threads = []
event_log = []

class ReadersWriters:
    """
    A class that implements the Readers-Writers problem solution.

    This class provides methods for readers and writers to access a shared resource
    while ensuring mutual exclusion between writers and allowing multiple readers
    to access the resource simultaneously.

    Attributes:
        read_count (int): The number of active readers.
        resource (threading.Semaphore): A semaphore to control access to the resource.
        read_count_lock (threading.Lock): A lock to synchronize access to the read_count variable.
        blocked_count (int): The number of blocked readers or writers.

    Methods:
        reader(id, max_read_time): Simulates a reader accessing the shared resource.
        writer(id, max_write_time): Simulates a writer accessing the shared resource.
    """

    def __init__(self):
        self.read_count = 0
        self.resource = threading.Semaphore(1)
        self.read_count_lock = threading.Lock()
        self.blocked_count = 0

    def reader(self, id, max_read_time):
        """
        Simulates a reader accessing the shared resource.

        Args:
            id (int): The ID of the reader.
            max_read_time (float): The maximum time in seconds that the reader can spend reading.

        Returns:
            None
        """
        global running, event_log
        while running:
            with self.read_count_lock:
                self.read_count += 1
                if self.read_count == 1:
                    self.resource.acquire()  # Primer lector adquiere el recurso

            read_time = random.uniform(0, max_read_time)
            print(f"Reader {id} is reading for {read_time} seconds")
            time.sleep(read_time)

            with self.read_count_lock:
                self.read_count -= 1
                if self.read_count == 0:
                    self.resource.release()  # Último lector libera el recurso

            print(f"Reader {id} finished reading")
            event_log.append({"reader": True, "id": id, "time": read_time})
            time.sleep(random.uniform(0, max_read_time))

    def writer(self, id, max_write_time):
        """
        Simulates a writer accessing the shared resource.

        Args:
            id (int): The ID of the writer.
            max_write_time (float): The maximum time in seconds that the writer can spend writing.

        Returns:
            None
        """
        global running, event_log
        while running:
            self.resource.acquire()  # Escritor adquiere el recurso
            write_time = random.uniform(0, max_write_time)
            print(f"Writer {id} is writing for {write_time} seconds")
            time.sleep(write_time)
            self.resource.release()  # Escritor libera el recurso
            print(f"Writer {id} finished writing")
            event_log.append({"reader": False, "id": id, "time": write_time})
            time.sleep(random.uniform(0, max_write_time))

# Función para iniciar la simulación
@csrf_exempt
def start_simulation(request):
    """
    Starts the simulation of the readers-writers problem.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        JsonResponse: A JSON response indicating the status of the simulation.
            - If the simulation is started successfully, the response will have a "status" key with the value "Simulation started".
            - If the simulation is already running, the response will have a "status" key with the value "Simulation already running".
    """
    global running, threads

    if not running:
        running = True
        args =  json.loads(request.body)
        num_readers = int(args.get('readers', 5))
        num_writers = int(args.get('writers', 2))
        max_read_time = int(args.get('maxReadTime', 3))
        max_write_time = int(args.get('maxWriteTime', 3))
        
        rw = ReadersWriters()
        threads = []

        for i in range(num_readers):
            t = threading.Thread(target=rw.reader, args=(i, max_read_time))
            t.start()
            threads.append(t)

        for i in range(num_writers):
            t = threading.Thread(target=rw.writer, args=(i, max_write_time))
            t.start()
            threads.append(t)

        return JsonResponse({"status": "Simulation started"})
    else:
        return JsonResponse({"status": "Simulation already running"})

# Función para detener la simulación
@csrf_exempt
def stop_simulation(request):
    """
    Stops the simulation if it is currently running.

    Returns:
        JsonResponse: A JSON response indicating the status of the simulation.
            - If the simulation was running and is now stopped, the response will be {"status": "Simulation stopped"}.
            - If there was no simulation running, the response will be {"status": "No simulation running"}.
    """
    global running, threads, event_log

    if running:
        running = False
        for t in threads:
            t.join()

        threads = []
        event_log = []

        return JsonResponse({"status": "Simulation stopped"})
    else:
        return JsonResponse({"status": "No simulation running"})

# Función para obtener y limpiar el registro de eventos
@csrf_exempt
def get_event_log(request):
    """
    Retrieves the event log and clears it.

    Args:
        request: The HTTP request object.

    Returns:
        A JsonResponse containing the event log.

    """
    global event_log
    log = event_log.copy()
    event_log = []
    return JsonResponse(log, safe=False)

# Vista para cargar la página de simulación
def readers_writers(request):
    """
    This function handles the readers_writers view.

    Parameters:
    - request: The HTTP request object.

    Returns:
    - A rendered HTML response.

    """
    return render(request, 'index.html')

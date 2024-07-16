import threading
import time
import random
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json

# Variables globales para controlar la simulación
num_filosofos = 5
num_tenedores = num_filosofos
tenedores_sem = [threading.Semaphore(1) for _ in range(num_tenedores)]
mutex = threading.Semaphore(1)
running = False
hilos_filosofos = []
filosofos = []  # Lista para almacenar instancias de Filosofo
event_log = []  # Lista para almacenar los eventos

# Clase para representar a un filósofo
class Filosofo(threading.Thread):
    """
    Represents a philosopher thread.

    Args:
        indice (int): The index of the philosopher.
        action_time (int): The maximum time for each action (thinking or eating).

    Attributes:
        indice (int): The index of the philosopher.
        daemon (bool): Indicates whether the thread is a daemon thread.
        stopped (threading.Event): Event to signal the thread to stop.
        action_time (int): The maximum time for each action (thinking or eating).

    """

    def __init__(self, indice, action_time):
        super().__init__()
        self.indice = indice
        self.daemon = True  # Los hilos se marcan como "daemon" para que se detengan cuando se cierre el programa
        self.stopped = threading.Event()
        self.action_time = action_time

    def run(self):
        """
        Executes the main logic of the philosopher's thread.
        The philosopher alternates between thinking and eating.
        """
        global event_log
        while not self.stopped.wait(0.1):  # Espera corta para verificar si se debe detener
            if running:
                print(f"El filósofo {self.indice} está pensando...")
                t = random.randint(1, self.action_time)
                event_log.append({"id": self.indice, "action": "pensando", "time": t})
                time.sleep(t)

                mutex.acquire()
                tenedores_sem[self.indice].acquire()
                tenedores_sem[(self.indice + 1) % num_tenedores].acquire()
                mutex.release()

                print(f"El filósofo {self.indice} está comiendo...")
                t = random.randint(1, self.action_time)
                event_log.append({"id": self.indice, "action": "comiendo", "time": t})
                time.sleep(t)

                tenedores_sem[self.indice].release()
                tenedores_sem[(self.indice + 1) % num_tenedores].release()
            else:
                break

# Función para iniciar la simulación
@csrf_exempt
def start_simulation(request):
    """
    Starts the simulation of the dining philosophers problem.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        JsonResponse: A JSON response indicating the status of the simulation.

    Raises:
        None
    """
    global running, hilos_filosofos, filosofos, num_filosofos, num_tenedores, tenedores_sem, mutex
    global event_log

    if request.method == "POST":
        event_log.clear()
        data = json.loads(request.body)
        num_filosofos = data.get('philosophers', 5)
        action_time = data.get('actionTime', 5)

        # Reiniciar las variables según los nuevos valores
        num_tenedores = num_filosofos
        tenedores_sem = [threading.Semaphore(1) for _ in range(num_tenedores)]
        mutex = threading.Semaphore(1)
        hilos_filosofos = []
        filosofos = []

        if not hilos_filosofos:
            running = True
            for i in range(num_filosofos):
                filosofo = Filosofo(i, action_time)
                filosofos.append(filosofo)  # Agregar el filósofo a la lista
                filosofo.start()
                hilos_filosofos.append(filosofo)

        return JsonResponse({"status": "La simulación comenzará en pocos segundos."})
    else:
        return JsonResponse({"status": "Invalid request method"}, status=405)

# Función para detener la simulación
@csrf_exempt
def stop_simulation(request):
    """
    Stops the simulation of philosophers.

    This function stops the simulation by setting the 'running' flag to False,
    and signaling each philosopher thread to stop by setting the 'stopped' event.
    It also clears the lists of philosopher threads and philosophers.

    Args:
        request: The HTTP request object.

    Returns:
        A JSON response indicating that the simulation has been stopped.

    """
    global running, hilos_filosofos, filosofos

    running = False
    for filosofo in hilos_filosofos:
        filosofo.stopped.set()  # Marcar el evento para detener el hilo

    hilos_filosofos = []
    filosofos = []  # Limpiar la lista de filósofos

    return JsonResponse({"status": "Filósofos-Comensales se ha detenido, por favor, espere a que culmine el procesamiento de datos."})

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
def dining_philosophers(request):
    """
    Renders the 'index.html' template for the dining philosophers page.

    Args:
        request: The HTTP request object.

    Returns:
        A rendered HTML response.
    """
    return render(request, 'index.html')

def animated_version(request):
    """
    Renders the 'philosophers_animated.html' template.

    Args:
        request: The HTTP request object.

    Returns:
        The rendered HTML response.
    """
    return render(request, "philosophers_animated.html")

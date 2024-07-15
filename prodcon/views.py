import threading
import queue
import time
import random
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json

# Lista compartida para almacenar los objetos producidos y consumidos
shared_list = []
# Bloqueo para proteger el acceso a la lista compartida
list_lock = threading.Lock()
# Variable global para controlar los hilos de productor-consumidor
running = False

def producer(q, empty_semaphore, full_semaphore, producer_id):
    """
    Producer function that adds items to a shared queue and a shared list.

    Args:
        q (Queue): The shared queue to add items to.
        empty_semaphore (Semaphore): The semaphore to control the number of empty slots in the queue.
        full_semaphore (Semaphore): The semaphore to control the number of full slots in the queue.
        producer_id (int): The ID of the producer.

    Returns:
        None
    """
    global running
    while running:
        empty_semaphore.acquire()
        item = random.randint(1, 10)
        t = random.random()
        time.sleep(t)
        with list_lock:
            obj = {"producer": True, "id": producer_id, "item": item, "time": t}
            shared_list.append(obj)
        q.put(item)
        full_semaphore.release()

def consumer(q, empty_semaphore, full_semaphore, consumer_id):
    """
    Consume items from the queue and add them to the shared list.

    Args:
        q (Queue): The queue from which items are consumed.
        empty_semaphore (Semaphore): Semaphore to control the number of empty slots in the queue.
        full_semaphore (Semaphore): Semaphore to control the number of filled slots in the queue.
        consumer_id (int): The ID of the consumer.

    Returns:
        None
    """
    global running
    while running:
        full_semaphore.acquire()
        item = q.get()
        t = random.random()
        q.task_done()
        with list_lock:
            obj = {"producer": False, "id": consumer_id, "item": item, "time": t}
            shared_list.append(obj)
        time.sleep(t)
        empty_semaphore.release()

@csrf_exempt
def start_prodcon(request):
    """
    Starts the producer-consumer threads.

    This function initializes and starts the producer-consumer threads based on the provided parameters.
    It creates a shared queue, semaphores, and starts the specified number of producers and consumers.
    The function expects a JSON payload in the request body containing the number of producers and consumers.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        JsonResponse: A JSON response indicating that the producer-consumer threads have been started.

    """
    global running
    global shared_list
    if not running:
        shared_list.clear()
        running = True
        q = queue.Queue(10)
        empty_semaphore = threading.Semaphore(q.maxsize)
        full_semaphore = threading.Semaphore(0)

        data = json.loads(request.body)
        num_producers = data.get('producers', 2)
        num_consumers = data.get('consumers', 2)

        for i in range(num_producers):
            threading.Thread(target=producer, args=(q, empty_semaphore, full_semaphore, i + 1)).start()

        for i in range(num_consumers):
            threading.Thread(target=consumer, args=(q, empty_semaphore, full_semaphore, i + 1)).start()

    return JsonResponse({"status": "Producer-Consumer threads started"})

def stop_prodcon(request):
    """
    Stops the Producer-Consumer threads.

    This function sets the global variable `running` to False, which stops the execution
    of the Producer-Consumer threads.

    Returns:
        A JsonResponse with the status message indicating that the Producer-Consumer threads
        have been stopped.
    """
    global running
    running = False
    return JsonResponse({"status": "Producer-Consumer threads stopped"})

def get_and_clear_list(request):
    """
    Retrieves and clears the shared_list.

    This function retrieves the contents of the shared_list, creates a copy of it,
    clears the shared_list, and returns the copied list as a JSON response.

    Args:
        request: The HTTP request object.

    Returns:
        A JSON response containing the copied contents of the shared_list.

    """
    global shared_list
    with list_lock:
        response_list = shared_list.copy()
        shared_list.clear()
    return JsonResponse(response_list, safe=False)

def prodcon(request):
    """
    This function handles the request for the 'prodcon' view.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object containing the rendered 'index.html' template.
    """
    return render(request, 'index.html')

def animated_version(request):
    """
    Renders the 'prodcon_animated.html' template.

    Args:
        request: The HTTP request object.

    Returns:
        The rendered HTML response.
    """
    return render(request, "prodcon_animated.html")

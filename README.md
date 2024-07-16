# Visualización de Problemas de Sincronización de Procesos

Explora la sincronización de procesos con este programa que te muestra gráficamente cómo funcionan los problemas clásicos.

## ¿Cómo utilizar la aplicación web?

Debes tener instalado Django para usar la aplicación. A continuación el comando para su instalación en caso de no tenerlo:

### `py -m pip install Django`

Luego procede con este comando:

### `python manage.py runserver`

Luego de ejecutar el comando la aplicación será ejecutada en [http://localhost:8000](http://localhost:8000).

## Simular productor-consumidor desde la consola

Para ejecutar el programa del productor-consumidor se debe ejecutar el siguiente comando:

### `python producer-consumer.py 5 3`

En este ejemplo [5] [3] indican la cantidad de productores y consumidores respectivamente.

## Simular filósofos-comensales desde la consola

Para ejecutar el programa de los filósofos-comensales se debe ejecutar el siguiente comando:

### `python philosophers.py --num_filosofos 10`

En este ejemplo [10] indica la cantidad de filósofos.

## Simular lectores-escritores desde la consola

Para ejecutar el programa de los lectores-escritores se debe ejecutar el siguiente comando:

### `python readers-writers.py --readers 3 --writers 3 --max_read_time 1 --max_write_time 1`

En este ejemplo [3] [3] [1] [1] indican la cantidad de lectores, cantidad de escritores, tiempo máximo en segundos que dura el proceso de lectura y tiempo maximo en segundos que dura el proceso de escritura respectivamente.

### Todos los comandos citados deben ejecutarse desde el directorio principal del proyecto. 

### En el fichero 'trace.txt' se almacena un resúmen estadístico de las ejecuciones de las aplicaciones por consola. 

# Visualización de Problemas de Sincronización de Procesos

Explora la sincronización de procesos con este programa que te muestra gráficamente cómo funcionan los problemas clásicos.

## ¿Cómo utilizar la aplicación web?

Debes tener instalado Django para usar la aplicación. A continuación el comando para su instalación en caso de no tenerlo:

### `py -m pip install Django`

Luego procede con este comando desde el directorio principal del proyecto:

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

## ¿Cómo realizar cambios en la interfaz web?

El backend de la aplicación se ejecuta sobre los ficheros guardados en '/frontend/build', por tanto los cambios efectuados en '/frontend/src' no serán visibles hasta que se haga build del proyecto utilizando el siguiente comando desde '/frontend':

### `npm run build`

En caso de no tener instaladas las dependencias del frontend, se debe ejecutar el siguiente comando desde '/frontend' antes de efectuar build del proyecto:

### `npm install`
 
#### Todos los comandos citados deben ejecutarse  usando la terminal con permisos de administrador. 

#### En el fichero 'trace.txt' se almacena un resúmen estadístico de las ejecuciones de las aplicaciones por consola. 

El modelo animado de la ejecución del problema productor-consumidor fue extraído de https://iximiuz.com/node-writable-streams/visual/?utm_medium=github&utm_source=gh-producer-consumer-vis

El modelo animado de la ejecución del problema filósofos-comensales fue extraído de https://www.netlogoweb.org/launch#https://www.netlogoweb.org/assets/modelslib/Sample%20Models/Computer%20Science/Dining%20Philosophers.nlogo
# EpicIO_Tracker

Este repositorio contiene una implementación de un sistema de tracking para un video de entrada dado. 

Desarrollado por: Diego Hernández.

https://user-images.githubusercontent.com/41651997/174445944-3ef40b5e-2da1-4f50-94ae-5587d74342fa.mp4

### Introducción

Un algoritmo de tracking consiste en predecir la posición de un objeto en un frame dado sabiendo la posición de dicho objeto en el frame anterior.
Para conseguir este objetivo, se aceptan como parámetros de entrada un video que contiene los objetos a seguir y un archivo en formato Json donde se define el ground truth de los objetos:
![diagramaES](https://user-images.githubusercontent.com/41651997/174447669-3a588691-ff85-4b01-9edb-325d30e5310a.PNG)

La salida del algoritmo es un video donde se muestra en cada frame los objetos seguidos. Para mostrar dicho seguimiento se dibujará un rectángulo contenedor sobre cada objeto seguido como se observa en el video inicial de este repositorio. 

### Solucion propuesta

Para implementar un sistema como el descrito en la sección anterior se desarrollan los siguientes pasos:

- Leer las entradas: Video + archivo json. Para este challenge se seguirán 3 jugadores de fútbol en 10 segundos de video. El archivo(.json) contiene la información asociada a cada jugador,por ejemplo, las coordenas iniciales donde empiezan los jugadores a desplazarse.
- Escoger un método para hacer tracking. Para esta solución se usa la librería OpenCV(en su última versión) como herramienta que provee módulos especiales para hacer seguimiento de objetos. Específicamente, el usuario puede escoger entre 2 métodos implementados en la libreria mencionada: KCF(Kernelized Correlation filters) y CSRT(Channel and Spatial Reliability Tracking). El primer método es más rapido pero menos preciso (mayor FPS). El segundo es más preciso pero también mas lento.
- Crear un objeto que se encargará del tracking para los 3 jugadores(multitracking) según el método escogido en el apartado anterior. 
- Inicializar el objeto creado en el punto anterior a partir de las coordenadas iniciales de los jugadores.
-  Dibujar las bboxes de los jugadores(ground truth) sobre el primer frame de video.
-  Actualizar la posición de cada jugador con el resultado del tracker escogido en cada frame de video.
-  Se calculan los FPS(Frames per second) asociado al proceso de tracking una vez terminado el video. Entre más alto sea este valor más rápido es el agoritmo de tracking.
-   Se crea el video de salida para mostrar los resultados de todo el proceso

### Forma de uso

La solución propuesta se ejecuta dentro de un container de docker llamado "EpicIO_tracker". 

Build image:
```sh
$ cd .devcontainer
$ docker build --tag EpicIO_tracker .
```
run
```sh
$ cd /workspaces/EpicIO_Tracker
$ python3 main.py --input_video Inputs\input.mkv --json_file Inputs/initial_conditions.json --tracker KCF 
```
or
```sh
$ python3 main.py --input_video Inputs\input.mkv --json_file Inputs/initial_conditions.json  --tracker CSRT
```




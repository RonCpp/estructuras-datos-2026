Simulación logística integral para una empresa de transporte y almacenamiento
==========================================================================

Este proyecto implementa un sistema de simulación logística donde se integran
múltiples estructuras de datos clásicas para modelar el flujo de cajas a
través de bodegas, contenedores y camiones. Se han implementado las
siguientes estructuras desde cero o utilizando módulos de la biblioteca
estándar de Python:

* **Pilas (LIFO)**: representan las cajas apiladas dentro de cada contenedor.
* **Colas (FIFO)**: gestionan la recepción de cajas y los contenedores listos
  para despacho.
* **Listas enlazadas simples**: almacenan los contenedores presentes en cada
  bodega.
* **Listas enlazadas dobles**: administran la flota de camiones con
  recorrido hacia adelante y hacia atrás.
* **Listas circulares simples**: modelan una cinta transportadora circular
  que distribuye cajas entre bodegas según su destino.
* **Listas circulares dobles**: implementan una programación cíclica de
  camiones para que los viajes se asignen de forma rotativa.
* **Árbol binario de búsqueda (ABB)**: organiza los contenedores activos por
  código, permitiendo búsquedas rápidas y una representación jerárquica de
  los contenedores.
* **Diccionarios y tuplas**: se usan para parámetros globales, registros de
  eventos y representación de cada caja como una tupla con sus atributos.

El simulador guía al usuario a través de un menú interactivo que permite
simular días de recepción y despacho, visualizar el estado de las bodegas,
consultar detalles de contenedores, reconfigurar parámetros, e incluso
resolver la Torre de Hanói. Tras cada acción relevante se muestran
representaciones ASCII/textuales de las estructuras de datos, de forma que
pueda observarse el estado interno del sistema en tiempo real. La
implementación no requiere bibliotecas externas y puede ejecutarse
directamente con Python 3.

Para iniciar la simulación, ejecute este archivo. El menú principal
permite avanzar día a día en la operación logística y revisar el estado
detallado de cada estructura. Las operaciones clave incluyen:

* **Simular recepción**: genera cajas aleatorias, las coloca en la cola de
  recepción y las distribuye a contenedores a través de la cinta
  transportadora circular.
* **Simular despacho**: identifica contenedores con 75 % o más de
  ocupación y los despacha asignándoles un camión según la lista circular
  doble. Los contenedores despachados se sustituyen por contenedores
  vacíos de igual tipo.
* **Visualizar estructuras**: muestra el estado de bodegas, colas,
  contenedores, camiones y del árbol binario de búsqueda de contenedores
  activos, utilizando representaciones textuales.

El código está abundantemente comentado para facilitar su comprensión y
posible extensión. Cada estructura de datos posee métodos de utilidad y
representaciones `__str__` que contribuyen a la visualización del estado
interno del sistema.

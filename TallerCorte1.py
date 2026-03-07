"""
Taller Primer Corte - Estructuras de Datos
Autor: Ronaldo Cortes & David Santiago Walteros Corzo
Objetivo: Visualizar y practicar el uso de Pilas, Colas, Diccionarios, Tuplas,
Listas enlazadas (simple, doble, circular simple, circular doble) y Torre de Hanói.

Cómo usar:
- Ejecuta el archivo: python TallerCorte1.py
- Usa el menú para interactuar con cada estructura.
"""


from collections import deque


# PILA: estructura LIFO. El último en entrar es el primero en salir.
class Pila:
    def __init__(self):
        self.datos = []

    def apilar(self, valor):
        self.datos.append(valor)

    def desapilar(self):
        if self.esta_vacia():
            return None
        return self.datos.pop()

    def tope(self):
        if self.esta_vacia():
            return None
        return self.datos[-1]

    def esta_vacia(self):
        return len(self.datos) == 0

    def __str__(self):
        return "Pila (base -> tope): " + str(self.datos)


# COLA: estructura FIFO. El primero en entrar es el primero en salir.
class Cola:
    def __init__(self):
        self.datos = deque()

    def encolar(self, valor):
        self.datos.append(valor)

    def desencolar(self):
        if self.esta_vacia():
            return None
        return self.datos.popleft()

    def frente(self):
        if self.esta_vacia():
            return None
        return self.datos[0]

    def esta_vacia(self):
        return len(self.datos) == 0

    def __str__(self):
        return "Cola (frente -> final): " + str(list(self.datos))


# Nodo para listas simples y circulares simples.
class NodoSimple:
    def __init__(self, valor):
        self.valor = valor
        self.siguiente = None


# Lista enlazada simple: cada nodo apunta solo al siguiente.
class ListaEnlazadaSimple:
    def __init__(self):
        self.cabeza = None

    def insertar_al_final(self, valor):
        nuevo = NodoSimple(valor)
        if self.cabeza is None:
            self.cabeza = nuevo
            return

        actual = self.cabeza
        while actual.siguiente is not None:
            actual = actual.siguiente
        actual.siguiente = nuevo

    def eliminar_valor(self, valor):
        if self.cabeza is None:
            return False

        if self.cabeza.valor == valor:
            self.cabeza = self.cabeza.siguiente
            return True

        anterior = self.cabeza
        actual = self.cabeza.siguiente

        while actual is not None:
            if actual.valor == valor:
                anterior.siguiente = actual.siguiente
                return True
            anterior = actual
            actual = actual.siguiente

        return False

    def __str__(self):
        if self.cabeza is None:
            return "Lista Simple: (vacía)"

        valores = []
        actual = self.cabeza
        while actual is not None:
            valores.append(str(actual.valor))
            actual = actual.siguiente

        return "Lista Simple: " + " -> ".join(valores) + " -> None"


# Nodo para listas dobles y circulares dobles.
class NodoDoble:
    def __init__(self, valor):
        self.valor = valor
        self.anterior = None
        self.siguiente = None


# Lista enlazada doble: cada nodo conoce el anterior y el siguiente.
class ListaEnlazadaDoble:
    def __init__(self):
        self.cabeza = None
        self.cola = None

    def insertar_al_final(self, valor):
        nuevo = NodoDoble(valor)
        if self.cabeza is None:
            self.cabeza = nuevo
            self.cola = nuevo
            return

        nuevo.anterior = self.cola
        self.cola.siguiente = nuevo
        self.cola = nuevo

    def eliminar_valor(self, valor):
        actual = self.cabeza

        while actual is not None:
            if actual.valor == valor:
                if actual.anterior is not None:
                    actual.anterior.siguiente = actual.siguiente
                else:
                    self.cabeza = actual.siguiente

                if actual.siguiente is not None:
                    actual.siguiente.anterior = actual.anterior
                else:
                    self.cola = actual.anterior

                return True
            actual = actual.siguiente

        return False

    def __str__(self):
        if self.cabeza is None:
            return "Lista Doble: (vacía)"

        valores = []
        actual = self.cabeza
        while actual is not None:
            valores.append(str(actual.valor))
            actual = actual.siguiente

        return "Lista Doble: " + " <-> ".join(valores)


# Lista circular simple: el último nodo vuelve a la cabeza.
class ListaCircularSimple:
    def __init__(self):
        self.cabeza = None

    def insertar_al_final(self, valor):
        nuevo = NodoSimple(valor)
        if self.cabeza is None:
            self.cabeza = nuevo
            nuevo.siguiente = nuevo
            return

        actual = self.cabeza
        while actual.siguiente != self.cabeza:
            actual = actual.siguiente

        actual.siguiente = nuevo
        nuevo.siguiente = self.cabeza

    def eliminar_valor(self, valor):
        if self.cabeza is None:
            return False

        if self.cabeza.valor == valor:
            if self.cabeza.siguiente == self.cabeza:
                self.cabeza = None
                return True

            ultimo = self.cabeza
            while ultimo.siguiente != self.cabeza:
                ultimo = ultimo.siguiente

            self.cabeza = self.cabeza.siguiente
            ultimo.siguiente = self.cabeza
            return True

        anterior = self.cabeza
        actual = self.cabeza.siguiente

        while actual != self.cabeza:
            if actual.valor == valor:
                anterior.siguiente = actual.siguiente
                return True
            anterior = actual
            actual = actual.siguiente

        return False

    def __str__(self):
        if self.cabeza is None:
            return "Lista Circular Simple: (vacía)"

        valores = []
        actual = self.cabeza
        while True:
            valores.append(str(actual.valor))
            actual = actual.siguiente
            if actual == self.cabeza:
                break

        return "Lista Circular Simple: " + " -> ".join(valores) + " -> (regresa al inicio)"


# Lista circular doble: enlaces en ambos sentidos y forma circular.
class ListaCircularDoble:
    def __init__(self):
        self.cabeza = None

    def insertar_al_final(self, valor):
        nuevo = NodoDoble(valor)

        if self.cabeza is None:
            self.cabeza = nuevo
            nuevo.siguiente = nuevo
            nuevo.anterior = nuevo
            return

        cola = self.cabeza.anterior
        cola.siguiente = nuevo
        nuevo.anterior = cola
        nuevo.siguiente = self.cabeza
        self.cabeza.anterior = nuevo

    def eliminar_valor(self, valor):
        if self.cabeza is None:
            return False

        actual = self.cabeza
        while True:
            if actual.valor == valor:
                if actual.siguiente == actual:
                    self.cabeza = None
                else:
                    actual.anterior.siguiente = actual.siguiente
                    actual.siguiente.anterior = actual.anterior
                    if actual == self.cabeza:
                        self.cabeza = actual.siguiente
                return True

            actual = actual.siguiente
            if actual == self.cabeza:
                break

        return False

    def __str__(self):
        if self.cabeza is None:
            return "Lista Circular Doble: (vacía)"

        valores = []
        actual = self.cabeza
        while True:
            valores.append(str(actual.valor))
            actual = actual.siguiente
            if actual == self.cabeza:
                break

        return "Lista Circular Doble: " + " <-> ".join(valores) + " <-> (regresa al inicio)"


# Torre de Hanói usando recursividad.
def hanoi(n, origen, auxiliar, destino, movimientos):
    if n == 1:
        movimientos.append((1, origen, destino))
        return

    hanoi(n - 1, origen, destino, auxiliar, movimientos)
    movimientos.append((n, origen, destino))
    hanoi(n - 1, auxiliar, origen, destino, movimientos)


def mostrar_hanoi(num_discos):
    movimientos = []
    hanoi(num_discos, "A", "B", "C", movimientos)

    print("\nTORRE DE HANÓI")
    print(f"Número de discos: {num_discos}")
    print(f"Movimientos mínimos: {len(movimientos)}")
    print("-" * 35)

    for i, movimiento in enumerate(movimientos, start=1):
        disco, origen, destino = movimiento
        print(f"Paso {i}: mover disco {disco} de {origen} a {destino}")


# Diccionario: pares clave-valor. Tupla: colección ordenada e inmutable.
def demo_diccionario_tupla():
    agenda = {
        "Ronaldo": "3001234567",
        "David": "3019876543",
        "Ana": "3025551111"
    }

    ubicacion = ("Bogotá", "Colombia")

    while True:
        print("\n--- DICCIONARIOS Y TUPLAS ---")
        print("1) Ver diccionario")
        print("2) Buscar contacto")
        print("3) Agregar/actualizar contacto")
        print("4) Eliminar contacto")
        print("5) Ver tupla")
        print("0) Volver")

        op = input("Opción: ").strip()

        if op == "1":
            print("Agenda:", agenda)

        elif op == "2":
            nombre = input("Nombre a buscar: ").strip()
            print("Resultado:", agenda.get(nombre, "No encontrado"))

        elif op == "3":
            nombre = input("Nombre: ").strip()
            numero = input("Número: ").strip()
            agenda[nombre] = numero
            print("Agenda actualizada:", agenda)

        elif op == "4":
            nombre = input("Nombre a eliminar: ").strip()
            eliminado = agenda.pop(nombre, None)
            if eliminado is None:
                print("No existe ese contacto.")
            else:
                print("Contacto eliminado.")
                print("Agenda actual:", agenda)

        elif op == "5":
            print("Tupla:", ubicacion)
            print("Ciudad:", ubicacion[0])
            print("País:", ubicacion[1])

        elif op == "0":
            break

        else:
            print("Opción inválida.")


def menu_pila():
    pila = Pila()

    while True:
        print("\n--- PILA ---")
        print(pila)
        print("1) Apilar")
        print("2) Desapilar")
        print("3) Ver tope")
        print("0) Volver")

        op = input("Opción: ").strip()

        if op == "1":
            valor = input("Valor a apilar: ")
            pila.apilar(valor)
            print("Elemento apilado correctamente.")

        elif op == "2":
            eliminado = pila.desapilar()
            if eliminado is None:
                print("La pila está vacía.")
            else:
                print("Elemento desapilado:", eliminado)

        elif op == "3":
            print("Tope:", pila.tope())

        elif op == "0":
            break

        else:
            print("Opción inválida.")


def menu_cola():
    cola = Cola()

    while True:
        print("\n--- COLA ---")
        print(cola)
        print("1) Encolar")
        print("2) Desencolar")
        print("3) Ver frente")
        print("0) Volver")

        op = input("Opción: ").strip()

        if op == "1":
            valor = input("Valor a encolar: ")
            cola.encolar(valor)
            print("Elemento encolado correctamente.")

        elif op == "2":
            eliminado = cola.desencolar()
            if eliminado is None:
                print("La cola está vacía.")
            else:
                print("Elemento desencolado:", eliminado)

        elif op == "3":
            print("Frente:", cola.frente())

        elif op == "0":
            break

        else:
            print("Opción inválida.")


def menu_lista_simple(lista):
    while True:
        print("\n" + str(lista))
        print("1) Insertar al final")
        print("2) Eliminar valor")
        print("0) Volver")

        op = input("Opción: ").strip()

        if op == "1":
            valor = input("Valor: ")
            lista.insertar_al_final(valor)
            print("Insertado correctamente.")

        elif op == "2":
            valor = input("Valor a eliminar: ")
            if lista.eliminar_valor(valor):
                print("Elemento eliminado.")
            else:
                print("No se encontró el valor.")

        elif op == "0":
            break

        else:
            print("Opción inválida.")


def menu_lista_doble(lista):
    while True:
        print("\n" + str(lista))
        print("1) Insertar al final")
        print("2) Eliminar valor")
        print("0) Volver")

        op = input("Opción: ").strip()

        if op == "1":
            valor = input("Valor: ")
            lista.insertar_al_final(valor)
            print("Insertado correctamente.")

        elif op == "2":
            valor = input("Valor a eliminar: ")
            if lista.eliminar_valor(valor):
                print("Elemento eliminado.")
            else:
                print("No se encontró el valor.")

        elif op == "0":
            break

        else:
            print("Opción inválida.")


def menu_circular_simple(lista):
    while True:
        print("\n" + str(lista))
        print("1) Insertar al final")
        print("2) Eliminar valor")
        print("0) Volver")

        op = input("Opción: ").strip()

        if op == "1":
            valor = input("Valor: ")
            lista.insertar_al_final(valor)
            print("Insertado correctamente.")

        elif op == "2":
            valor = input("Valor a eliminar: ")
            if lista.eliminar_valor(valor):
                print("Elemento eliminado.")
            else:
                print("No se encontró el valor.")

        elif op == "0":
            break

        else:
            print("Opción inválida.")


def menu_circular_doble(lista):
    while True:
        print("\n" + str(lista))
        print("1) Insertar al final")
        print("2) Eliminar valor")
        print("0) Volver")

        op = input("Opción: ").strip()

        if op == "1":
            valor = input("Valor: ")
            lista.insertar_al_final(valor)
            print("Insertado correctamente.")

        elif op == "2":
            valor = input("Valor a eliminar: ")
            if lista.eliminar_valor(valor):
                print("Elemento eliminado.")
            else:
                print("No se encontró el valor.")

        elif op == "0":
            break

        else:
            print("Opción inválida.")


def menu_listas():
    lista_simple = ListaEnlazadaSimple()
    lista_doble = ListaEnlazadaDoble()
    lista_circular_simple = ListaCircularSimple()
    lista_circular_doble = ListaCircularDoble()

    while True:
        print("\n--- LISTAS ENLAZADAS ---")
        print("1) Lista enlazada simple")
        print("2) Lista enlazada doble")
        print("3) Lista circular simple")
        print("4) Lista circular doble")
        print("0) Volver")

        op = input("Opción: ").strip()

        if op == "1":
            menu_lista_simple(lista_simple)
        elif op == "2":
            menu_lista_doble(lista_doble)
        elif op == "3":
            menu_circular_simple(lista_circular_simple)
        elif op == "4":
            menu_circular_doble(lista_circular_doble)
        elif op == "0":
            break
        else:
            print("Opción inválida.")


def menu_hanoi():
    while True:
        print("\n--- TORRE DE HANÓI ---")
        print("0) Volver")
        dato = input("Ingrese número de discos: ").strip()

        if dato == "0":
            break

        if not dato.isdigit():
            print("Debe ingresar un número válido.")
            continue

        num_discos = int(dato)

        if num_discos < 1 or num_discos > 8:
            print("Use un número entre 1 y 8 para visualizar mejor en consola.")
            continue

        mostrar_hanoi(num_discos)


# Menú principal para probar todas las estructuras.
def main():
    while True:
        print("\n" + "=" * 40)
        print("TALLER DE ESTRUCTURAS DE DATOS")
        print("=" * 40)
        print("1) Pilas")
        print("2) Colas")
        print("3) Diccionarios y tuplas")
        print("4) Listas enlazadas")
        print("5) Torre de Hanói")
        print("0) Salir")

        op = input("Seleccione una opción: ").strip()

        if op == "1":
            menu_pila()
        elif op == "2":
            menu_cola()
        elif op == "3":
            demo_diccionario_tupla()
        elif op == "4":
            menu_listas()
        elif op == "5":
            menu_hanoi()
        elif op == "0":
            print("Programa finalizado.")
            break
        else:
            print("Opción inválida.")


if __name__ == "__main__":
    main()

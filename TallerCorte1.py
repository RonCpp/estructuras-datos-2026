"""
Simulación logística integral para una empresa de transporte y almacenamiento
==========================================================================

Este proyecto implementa un sistema de simulación logística donde se integran
múltiples estructuras de datos clásicas para modelar el flujo de cajas a
través de bodegas, contenedores y camiones. Se han implementado las
siguientes estructuras desde cero o utilizando módulos de la biblioteca
estándar de Python:

El código está abundantemente comentado para facilitar su comprensión y
posible extensión. Cada estructura de datos posee métodos de utilidad y
representaciones `__str__` que contribuyen a la visualización del estado
interno del sistema.
"""

from collections import deque
import random


# =========================================================
# ESTRUCTURAS BASE
# =========================================================

class Pila:
    """Estructura LIFO para las cajas dentro de un contenedor."""
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

    def tamano(self):
        return len(self.datos)

    def elementos(self):
        return list(self.datos)

    def __str__(self):
        return f"Pila(base->tope): {self.datos}"


class Cola:
    """Estructura FIFO para recepción y despacho."""
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

    def tamano(self):
        return len(self.datos)

    def elementos(self):
        return list(self.datos)

    def limpiar(self):
        self.datos.clear()

    def __str__(self):
        return f"Cola(frente->final): {list(self.datos)}"


class NodoSimple:
    def __init__(self, valor):
        self.valor = valor
        self.siguiente = None


class ListaEnlazadaSimple:
    """Lista enlazada simple para contenedores dentro de una bodega."""
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

    def eliminar_por_codigo(self, codigo):
        if self.cabeza is None:
            return False

        if getattr(self.cabeza.valor, "codigo", None) == codigo:
            self.cabeza = self.cabeza.siguiente
            return True

        anterior = self.cabeza
        actual = self.cabeza.siguiente

        while actual is not None:
            if getattr(actual.valor, "codigo", None) == codigo:
                anterior.siguiente = actual.siguiente
                return True
            anterior = actual
            actual = actual.siguiente

        return False

    def buscar_por_codigo(self, codigo):
        actual = self.cabeza
        while actual is not None:
            if getattr(actual.valor, "codigo", None) == codigo:
                return actual.valor
            actual = actual.siguiente
        return None

    def recorrer(self):
        actual = self.cabeza
        while actual is not None:
            yield actual.valor
            actual = actual.siguiente

    def __str__(self):
        if self.cabeza is None:
            return "Lista Simple: (vacía)"
        valores = []
        actual = self.cabeza
        while actual is not None:
            valores.append(str(actual.valor))
            actual = actual.siguiente
        return " -> ".join(valores)


class NodoDoble:
    def __init__(self, valor):
        self.valor = valor
        self.anterior = None
        self.siguiente = None


class ListaEnlazadaDoble:
    """Lista enlazada doble para la flota de camiones."""
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

    def recorrer_adelante(self):
        actual = self.cabeza
        while actual is not None:
            yield actual.valor
            actual = actual.siguiente

    def recorrer_atras(self):
        actual = self.cola
        while actual is not None:
            yield actual.valor
            actual = actual.anterior

    def __str__(self):
        if self.cabeza is None:
            return "Lista Doble: (vacía)"
        return " <-> ".join(str(x) for x in self.recorrer_adelante())


class ListaCircularSimple:
    """Cinta transportadora circular de distribución entre bodegas."""
    def __init__(self):
        self.cabeza = None
        self.actual = None

    def insertar_al_final(self, valor):
        nuevo = NodoSimple(valor)
        if self.cabeza is None:
            self.cabeza = nuevo
            nuevo.siguiente = nuevo
            self.actual = nuevo
            return

        temp = self.cabeza
        while temp.siguiente != self.cabeza:
            temp = temp.siguiente

        temp.siguiente = nuevo
        nuevo.siguiente = self.cabeza

    def mover_hasta(self, valor):
        """
        Avanza sobre la cinta hasta llegar a la estación deseada.
        Retorna el número de movimientos realizados.
        """
        if self.cabeza is None or self.actual is None:
            return 0

        movimientos = 0
        while self.actual.valor != valor:
            self.actual = self.actual.siguiente
            movimientos += 1
        return movimientos

    def obtener_actual(self):
        if self.actual is None:
            return None
        return self.actual.valor

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
        return " -> ".join(valores) + " -> (regresa al inicio)"


class ListaCircularDoble:
    """Programación circular de camiones para despacho diario."""
    def __init__(self):
        self.cabeza = None
        self.actual = None

    def insertar_al_final(self, valor):
        nuevo = NodoDoble(valor)
        if self.cabeza is None:
            self.cabeza = nuevo
            nuevo.siguiente = nuevo
            nuevo.anterior = nuevo
            self.actual = nuevo
            return

        cola = self.cabeza.anterior
        cola.siguiente = nuevo
        nuevo.anterior = cola
        nuevo.siguiente = self.cabeza
        self.cabeza.anterior = nuevo

    def siguiente(self):
        if self.actual is None:
            return None
        valor = self.actual.valor
        self.actual = self.actual.siguiente
        return valor

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
        return " <-> ".join(valores) + " <-> (regresa al inicio)"


# =========================================================
# ÁRBOL BINARIO DE BÚSQUEDA
# =========================================================

class NodoArbol:
    """
    Nodo para un árbol binario de búsqueda. Cada nodo almacena una clave y un
    valor asociado, así como punteros a sus hijos izquierdo y derecho.
    """
    def __init__(self, clave, valor):
        self.clave = clave
        self.valor = valor
        self.izquierda = None
        self.derecha = None


class ArbolBinarioBusqueda:
    """
    Implementación básica de un árbol binario de búsqueda (ABB). Este ABB se
    utiliza en la simulación para organizar contenedores por su código,
    permitiendo búsquedas rápidas y una representación jerárquica de los
    contenedores activos en el sistema. Se incluyen métodos para insertar,
    buscar y eliminar nodos, así como una representación textual del árbol.
    """
    def __init__(self):
        self.raiz = None

    def insertar(self, clave, valor):
        """Inserta un par clave-valor en el árbol."""
        def _insertar(nodo, clave, valor):
            if nodo is None:
                return NodoArbol(clave, valor)
            if clave < nodo.clave:
                nodo.izquierda = _insertar(nodo.izquierda, clave, valor)
            elif clave > nodo.clave:
                nodo.derecha = _insertar(nodo.derecha, clave, valor)
            else:
                # Si la clave ya existe, actualiza el valor asociado.
                nodo.valor = valor
            return nodo
        self.raiz = _insertar(self.raiz, clave, valor)

    def buscar(self, clave):
        """Busca un valor por su clave. Retorna None si no existe."""
        actual = self.raiz
        while actual is not None:
            if clave == actual.clave:
                return actual.valor
            elif clave < actual.clave:
                actual = actual.izquierda
            else:
                actual = actual.derecha
        return None

    def eliminar(self, clave):
        """Elimina el nodo con la clave dada del árbol."""
        def _eliminar(nodo, clave):
            if nodo is None:
                return None
            if clave < nodo.clave:
                nodo.izquierda = _eliminar(nodo.izquierda, clave)
            elif clave > nodo.clave:
                nodo.derecha = _eliminar(nodo.derecha, clave)
            else:
                # Caso 1: el nodo no tiene hijos
                if nodo.izquierda is None and nodo.derecha is None:
                    return None
                # Caso 2: el nodo tiene un solo hijo
                if nodo.izquierda is None:
                    return nodo.derecha
                if nodo.derecha is None:
                    return nodo.izquierda
                # Caso 3: el nodo tiene dos hijos. Se busca el sucesor
                # in-order (el mínimo en el subárbol derecho).
                sucesor_padre = nodo
                sucesor = nodo.derecha
                while sucesor.izquierda is not None:
                    sucesor_padre = sucesor
                    sucesor = sucesor.izquierda
                # Sustituye los valores
                nodo.clave, nodo.valor = sucesor.clave, sucesor.valor
                # Elimina el sucesor
                if sucesor_padre.izquierda == sucesor:
                    sucesor_padre.izquierda = sucesor.derecha
                else:
                    sucesor_padre.derecha = sucesor.derecha
            return nodo
        self.raiz = _eliminar(self.raiz, clave)

    def _imprimir(self, nodo, prefijo, es_izquierda):
        """
        Función auxiliar para generar una representación en ASCII del árbol.
        """
        if nodo is None:
            return ""
        resultado = ""
        resultado += prefijo
        resultado += "├── " if es_izquierda else "└── "
        resultado += f"{nodo.clave}\n"
        # Construye representación de subárbol izquierdo
        resultado += self._imprimir(
            nodo.izquierda, prefijo + ("│   " if es_izquierda else "    "), True
        )
        # Construye representación de subárbol derecho
        resultado += self._imprimir(
            nodo.derecha, prefijo + ("│   " if es_izquierda else "    "), False
        )
        return resultado

    def __str__(self):
        if self.raiz is None:
            return "Árbol: (vacío)"
        return self._imprimir(self.raiz, "", False)


# =========================================================
# MODELO LOGÍSTICO
# =========================================================

class Contenedor:
    """
    Usa Pila para almacenar cajas.
    Cada caja es una tupla: (id_caja, tamaño, destino, volumen)
    """
    def __init__(self, codigo, tipo, bodega, capacidad_volumen):
        self.codigo = codigo
        self.tipo = tipo
        self.bodega = bodega
        self.capacidad_volumen = capacidad_volumen
        self.cajas = Pila()
        self.volumen_actual = 0
        self.despachado = False

    def puede_recibir(self, caja):
        volumen = caja[3]
        return (not self.despachado) and (self.volumen_actual + volumen <= self.capacidad_volumen)

    def agregar_caja(self, caja):
        if self.puede_recibir(caja):
            self.cajas.apilar(caja)
            self.volumen_actual += caja[3]
            return True
        return False

    def ocupacion_porcentaje(self):
        if self.capacidad_volumen == 0:
            return 0
        return (self.volumen_actual / self.capacidad_volumen) * 100

    def listo_para_despacho(self):
        return self.ocupacion_porcentaje() >= 75

    def cantidad_cajas(self):
        return self.cajas.tamano()

    def resumen_corto(self):
        return (f"{self.codigo} | tipo={self.tipo} | "
                f"{self.volumen_actual}/{self.capacidad_volumen} vol | "
                f"{self.ocupacion_porcentaje():.1f}% | cajas={self.cantidad_cajas()}")

    def detalle(self):
        lineas = []
        lineas.append(f"Código: {self.codigo}")
        lineas.append(f"Tipo: {self.tipo}")
        lineas.append(f"Bodega: {self.bodega}")
        lineas.append(f"Capacidad: {self.capacidad_volumen}")
        lineas.append(f"Volumen actual: {self.volumen_actual}")
        lineas.append(f"Ocupación: {self.ocupacion_porcentaje():.1f}%")
        lineas.append(f"Cantidad de cajas: {self.cantidad_cajas()}")
        lineas.append(f"Estado: {'LISTO PARA DESPACHO' if self.listo_para_despacho() else 'En proceso'}")
        lineas.append("Cajas apiladas (base -> tope):")
        if self.cajas.esta_vacia():
            lineas.append("  (sin cajas)")
        else:
            for caja in self.cajas.elementos():
                lineas.append(f"  {caja}")
        return "\n".join(lineas)

    def snapshot(self):
        return {
            "codigo": self.codigo,
            "tipo": self.tipo,
            "bodega": self.bodega,
            "capacidad_volumen": self.capacidad_volumen,
            "volumen_actual": self.volumen_actual,
            "ocupacion": round(self.ocupacion_porcentaje(), 2),
            "cantidad_cajas": self.cantidad_cajas(),
            "cajas": self.cajas.elementos(),
            "despachado": self.despachado,
        }

    def __str__(self):
        return self.resumen_corto()


class Camion:
    def __init__(self, codigo, ruta_base):
        self.codigo = codigo
        self.ruta_base = ruta_base
        self.disponible = True
        self.viajes_realizados = 0

    def asignar_viaje(self):
        if self.disponible:
            self.disponible = False
            self.viajes_realizados += 1
            return True
        return False

    def liberar(self):
        self.disponible = True

    def __str__(self):
        estado = "Disponible" if self.disponible else "En ruta"
        return f"{self.codigo} ({self.ruta_base}) - {estado} - viajes={self.viajes_realizados}"


class Bodega:
    """Cada bodega contiene una lista enlazada simple de contenedores."""
    def __init__(self, nombre):
        self.nombre = nombre
        self.contenedores = ListaEnlazadaSimple()

    def agregar_contenedor(self, contenedor):
        self.contenedores.insertar_al_final(contenedor)

    def eliminar_contenedor(self, codigo):
        return self.contenedores.eliminar_por_codigo(codigo)

    def buscar_contenedor(self, codigo):
        return self.contenedores.buscar_por_codigo(codigo)

    def obtener_contenedores(self):
        return list(self.contenedores.recorrer())

    def __str__(self):
        return f"Bodega {self.nombre}"


# =========================================================
# TORRE DE HANÓI (SIN MODIFICAR)
# =========================================================

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
    print("-" * 40)

    for i, movimiento in enumerate(movimientos, start=1):
        disco, origen, destino = movimiento
        print(f"Paso {i}: mover disco {disco} de {origen} a {destino}")


# =========================================================
# SIMULADOR PRINCIPAL
# =========================================================

class EmpresaLogistica:
    def __init__(self):
        # Diccionarios de configuración
        self.volumenes_caja = {
            1: 1,
            2: 2,
            3: 3,
            4: 4,
            5: 5,
            6: 6
        }

        self.capacidades_contenedor = {
            "normal": 40,
            "largo": 60,
            "extra_largo": 80
        }

        self.contenedores_por_bodega_y_tipo = {
            "normal": 3,
            "largo": 2,
            "extra_largo": 2
        }

        self.bodegas = {
            "Sur": Bodega("Sur"),
            "Norte": Bodega("Norte"),
            "Oriente": Bodega("Oriente"),
            "Occidente": Bodega("Occidente")
        }

        self.cola_recepcion = Cola()
        self.cola_listos_despacho = Cola()
        self.cajas_en_espera = Cola()

        self.cinta_transportadora = ListaCircularSimple()
        for nombre in self.bodegas.keys():
            self.cinta_transportadora.insertar_al_final(nombre)

        self.flota = ListaEnlazadaDoble()
        self.programacion_camiones = ListaCircularDoble()
        self.num_camiones = 5
        self._crear_camiones()

        self.registro_contenedores = {}
        self.historico_despachados = {}

        self.contador_cajas = 1
        self.contador_contenedores = 1

        self.dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"]
        self.indice_dia = 0

        self.total_cajas_recibidas = 0
        self.total_cajas_asignadas = 0
        self.total_cajas_en_espera = 0
        self.total_contenedores_despachados = 0

        # CREAR EL ÁRBOL ANTES DE INICIALIZAR CONTENEDORES
        self.arbol_contenedores = ArbolBinarioBusqueda()

        # AHORA SÍ inicializar contenedores
        self._inicializar_contenedores()

    def _crear_camiones(self):
        rutas = ["Ruta Sur", "Ruta Norte", "Ruta Oriente", "Ruta Occidente", "Ruta Mixta"]
        for i in range(1, self.num_camiones + 1):
            camion = Camion(f"CAM-{i:02d}", rutas[(i - 1) % len(rutas)])
            self.flota.insertar_al_final(camion)
            self.programacion_camiones.insertar_al_final(camion)

    def _nuevo_codigo_contenedor(self, tipo, bodega):
        prefijo = {"normal": "N", "largo": "L", "extra_largo": "XL"}[tipo]
        codigo = f"{prefijo}-{bodega[:3].upper()}-{self.contador_contenedores:03d}"
        self.contador_contenedores += 1
        return codigo

    def _inicializar_contenedores(self):
        # Inicialización temporal del contador
        self.contador_contenedores = 1

        for nombre_bodega, bodega in self.bodegas.items():
            for tipo, cantidad in self.contenedores_por_bodega_y_tipo.items():
                for _ in range(cantidad):
                    codigo = self._nuevo_codigo_contenedor(tipo, nombre_bodega)
                    cont = Contenedor(codigo, tipo, nombre_bodega, self.capacidades_contenedor[tipo])
                    bodega.agregar_contenedor(cont)
                    self.registro_contenedores[codigo] = cont
                    # Insertar el nuevo contenedor en el árbol binario de búsqueda.
                    self.arbol_contenedores.insertar(codigo, cont)

    def dia_actual(self):
        return self.dias_semana[self.indice_dia]

    def avanzar_dia(self):
        self.indice_dia = (self.indice_dia + 1) % len(self.dias_semana)
        for camion in self.flota.recorrer_adelante():
            camion.liberar()
        print(f"\nSe avanzó al siguiente día. Día actual: {self.dia_actual()}")
        print("Todos los camiones quedaron disponibles nuevamente.")

    def tipo_contenedor_para_tamano(self, tamano):
        if tamano in (1, 2):
            return "normal"
        elif tamano in (3, 4):
            return "largo"
        return "extra_largo"

    def crear_caja_aleatoria(self):
        tamano = random.randint(1, 6)
        destinos = list(self.bodegas.keys())
        destino = random.choice(destinos)
        volumen = self.volumenes_caja[tamano]
        caja = (f"CAJA-{self.contador_cajas:05d}", tamano, destino, volumen)
        self.contador_cajas += 1
        return caja

    def generar_cajas_del_dia(self, cantidad):
        for _ in range(cantidad):
            caja = self.crear_caja_aleatoria()
            self.cola_recepcion.encolar(caja)

    def buscar_contenedor_disponible(self, bodega_nombre, tipo, caja):
        bodega = self.bodegas[bodega_nombre]
        for contenedor in bodega.obtener_contenedores():
            if contenedor.tipo == tipo and contenedor.puede_recibir(caja):
                return contenedor
        return None

    def reemplazar_contenedor_despachado(self, contenedor):
        bodega = self.bodegas[contenedor.bodega]
        # Elimina el contenedor saliente de la lista de la bodega y del árbol.
        eliminado = bodega.eliminar_contenedor(contenedor.codigo)
        if eliminado:
            # Quitar del registro general y del árbol
            self.registro_contenedores.pop(contenedor.codigo, None)
            self.arbol_contenedores.eliminar(contenedor.codigo)

            # Crear un nuevo contenedor vacío que reemplace al despachado
            nuevo_codigo = self._nuevo_codigo_contenedor(contenedor.tipo, contenedor.bodega)
            nuevo_contenedor = Contenedor(
                nuevo_codigo,
                contenedor.tipo,
                contenedor.bodega,
                self.capacidades_contenedor[contenedor.tipo]
            )
            bodega.agregar_contenedor(nuevo_contenedor)
            # Registrar el nuevo contenedor
            self.registro_contenedores[nuevo_codigo] = nuevo_contenedor
            # Insertar en el árbol
            self.arbol_contenedores.insertar(nuevo_codigo, nuevo_contenedor)

    def distribuir_cajas_desde_recepcion(self):
        asignadas = 0
        en_espera = 0
        movimientos_cinta = 0

        while not self.cola_recepcion.esta_vacia():
            caja = self.cola_recepcion.desencolar()
            destino = caja[2]
            tamano = caja[1]
            tipo = self.tipo_contenedor_para_tamano(tamano)

            movimientos_cinta += self.cinta_transportadora.mover_hasta(destino)

            contenedor = self.buscar_contenedor_disponible(destino, tipo, caja)
            if contenedor is not None:
                contenedor.agregar_caja(caja)
                asignadas += 1
            else:
                self.cajas_en_espera.encolar(caja)
                en_espera += 1

        self.total_cajas_asignadas += asignadas
        self.total_cajas_en_espera += en_espera

        print(f"Cajas asignadas a contenedores: {asignadas}")
        print(f"Cajas enviadas a cola de espera: {en_espera}")
        print(f"Movimientos de la cinta transportadora: {movimientos_cinta}")

    def reintentar_cajas_en_espera(self):
        if self.cajas_en_espera.esta_vacia():
            return

        temp = Cola()
        recuperadas = 0

        while not self.cajas_en_espera.esta_vacia():
            caja = self.cajas_en_espera.desencolar()
            destino = caja[2]
            tamano = caja[1]
            tipo = self.tipo_contenedor_para_tamano(tamano)

            self.cinta_transportadora.mover_hasta(destino)
            contenedor = self.buscar_contenedor_disponible(destino, tipo, caja)

            if contenedor is not None:
                contenedor.agregar_caja(caja)
                recuperadas += 1
            else:
                temp.encolar(caja)

        self.cajas_en_espera = temp

        if recuperadas > 0:
            print(f"Se lograron ubicar {recuperadas} cajas que estaban en espera.")

    def actualizar_cola_despacho(self):
        self.cola_listos_despacho.limpiar()
        for bodega in self.bodegas.values():
            for contenedor in bodega.obtener_contenedores():
                if contenedor.listo_para_despacho() and not contenedor.despachado:
                    self.cola_listos_despacho.encolar(contenedor)

    def simular_dia_recepcion(self):
        dia = self.dia_actual()
        if dia == "Sábado":
            print("\nHoy es Sábado. No se reciben cajas. Solo se realizan despachos.")
            return

        cantidad = random.randint(80, 200)
        print(f"\n--- RECEPCIÓN DEL DÍA: {dia} ---")
        print(f"Cantidad de cajas generadas aleatoriamente: {cantidad}")

        self.generar_cajas_del_dia(cantidad)
        self.total_cajas_recibidas += cantidad

        print(f"Cajas en cola de recepción: {self.cola_recepcion.tamano()}")
        self.distribuir_cajas_desde_recepcion()
        self.actualizar_cola_despacho()

        print("Recepción y almacenamiento completados.")

    def simular_dia_despacho(self):
        dia = self.dia_actual()
        print(f"\n--- DESPACHO DEL DÍA: {dia} ---")

        # Intentar primero ubicar cajas que hubieran quedado esperando
        self.reintentar_cajas_en_espera()

        self.actualizar_cola_despacho()

        if self.cola_listos_despacho.esta_vacia():
            print("No hay contenedores con 75% o más de ocupación.")
            return

        despachados_hoy = 0
        maximo = self.num_camiones

        while (not self.cola_listos_despacho.esta_vacia()) and despachados_hoy < maximo:
            contenedor = self.cola_listos_despacho.desencolar()
            camion = self.programacion_camiones.siguiente()

            if camion is None:
                print("No hay programación circular de camiones.")
                break

            if not camion.disponible:
                # Si por alguna razón el camión no está disponible, se busca el siguiente.
                intentos = 0
                while not camion.disponible and intentos < self.num_camiones:
                    camion = self.programacion_camiones.siguiente()
                    intentos += 1
                if not camion.disponible:
                    print("No hay camiones disponibles en este momento.")
                    break

            camion.asignar_viaje()
            contenedor.despachado = True

            self.historico_despachados[contenedor.codigo] = {
                "camion": camion.codigo,
                "dia": dia,
                "detalle": contenedor.snapshot()
            }

            print(f"Despachado {contenedor.codigo} desde {contenedor.bodega} "
                  f"en {camion.codigo} | ocupación={contenedor.ocupacion_porcentaje():.1f}%")

            self.reemplazar_contenedor_despachado(contenedor)
            despachados_hoy += 1
            self.total_contenedores_despachados += 1

        self.actualizar_cola_despacho()
        print(f"Contenedores despachados hoy: {despachados_hoy}")

    def mostrar_estado_bodegas(self):
        print("\n" + "=" * 70)
        print(f"ESTADO ACTUAL DE BODEGAS - Día: {self.dia_actual()}")
        print("=" * 70)

        for nombre, bodega in self.bodegas.items():
            print(f"\nBODEGA {nombre.upper()}")
            print("-" * 70)
            contenedores = bodega.obtener_contenedores()
            if not contenedores:
                print("Sin contenedores.")
                continue

            for contenedor in contenedores:
                print(contenedor.resumen_corto())

        # Mostrar la cinta transportadora circular y las estructuras de cola
        print("\nESTADO DE ESTRUCTURAS INTERNAS:")
        print("Cinta transportadora circular:")
        print(self.cinta_transportadora)

        print("\nCola de recepción (cajas esperando asignación):")
        print(self.cola_recepcion)

        print("\nCola de contenedores listos para despacho:")
        print(self.cola_listos_despacho)

        print("\nLista de camiones (doblemente enlazada):")
        print(self.flota)

        print("\nProgramación de camiones (circular doble):")
        print(self.programacion_camiones)

        print("\nÁrbol de contenedores (ABB):")
        print(str(self.arbol_contenedores))

        print("\n" + "-" * 70)
        print(f"Total cajas recibidas: {self.total_cajas_recibidas}")
        print(f"Total cajas asignadas: {self.total_cajas_asignadas}")
        print(f"Cajas en espera: {self.cajas_en_espera.tamano()}")
        print(f"Total contenedores despachados: {self.total_contenedores_despachados}")

    def mostrar_cola_despacho(self):
        self.actualizar_cola_despacho()
        print("\n--- COLA DE CONTENEDORES LISTOS PARA DESPACHAR ---")
        if self.cola_listos_despacho.esta_vacia():
            print("No hay contenedores listos.")
            return

        for i, contenedor in enumerate(self.cola_listos_despacho.elementos(), start=1):
            print(f"{i}. {contenedor.resumen_corto()}")

    def ver_detalle_contenedor(self, codigo):
        contenedor = self.registro_contenedores.get(codigo)
        if contenedor is not None:
            print("\n--- DETALLE DE CONTENEDOR ACTIVO ---")
            print(contenedor.detalle())
            return

        historico = self.historico_despachados.get(codigo)
        if historico is not None:
            print("\n--- DETALLE DE CONTENEDOR DESPACHADO ---")
            print(f"Código: {historico['detalle']['codigo']}")
            print(f"Tipo: {historico['detalle']['tipo']}")
            print(f"Bodega origen: {historico['detalle']['bodega']}")
            print(f"Despachado el día: {historico['dia']}")
            print(f"Camión asignado: {historico['camion']}")
            print(f"Ocupación al despacho: {historico['detalle']['ocupacion']}%")
            print(f"Cantidad de cajas: {historico['detalle']['cantidad_cajas']}")
            print("Cajas:")
            for caja in historico["detalle"]["cajas"]:
                print(f"  {caja}")
            return

        print("No existe un contenedor con ese código.")

    def mostrar_flota_y_programacion(self):
        print("\n--- FLOTA DE CAMIONES (LISTA ENLAZADA DOBLE) ---")
        print(self.flota)

        print("\nRecorrido inverso de la flota:")
        print(" <-> ".join(str(camion) for camion in self.flota.recorrer_atras()))

        print("\n--- PROGRAMACIÓN CIRCULAR DE CAMIONES (LISTA CIRCULAR DOBLE) ---")
        print(self.programacion_camiones)

    def mostrar_arbol_contenedores(self):
        """
        Muestra en consola la estructura del árbol binario de búsqueda que
        organiza los contenedores activos por su código. Esta representación
        permite visualizar de forma jerárquica cómo se distribuyen los
        contenedores dentro del ABB. Si el árbol está vacío, se indicará
        explícitamente.
        """
        print("\n--- ÁRBOL DE CONTENEDORES (BÚSQUEDA POR CÓDIGO) ---")
        print(str(self.arbol_contenedores))

    def mostrar_parametros(self):
        print("\n--- PARÁMETROS DEL SISTEMA ---")
        print("Volumen por tamaño de caja:", self.volumenes_caja)
        print("Capacidad por tipo de contenedor:", self.capacidades_contenedor)
        print("Contenedores por bodega y tipo:", self.contenedores_por_bodega_y_tipo)
        print("Número de camiones:", self.num_camiones)
        print("Cantidad de cajas recibidas por día: aleatorio entre 80 y 200")
        print("Regla de despacho: contenedor con 75% o más de ocupación")

    def reconfigurar_parametros(self):
        print("\n--- RECONFIGURACIÓN DE PARÁMETROS ---")
        try:
            print("Capacidades actuales:", self.capacidades_contenedor)
            normal = int(input("Nueva capacidad contenedor normal: ").strip())
            largo = int(input("Nueva capacidad contenedor largo: ").strip())
            extra = int(input("Nueva capacidad contenedor extra largo: ").strip())

            print("Volúmenes actuales por tamaño:", self.volumenes_caja)
            nuevos_volumenes = {}
            for tam in range(1, 7):
                nuevos_volumenes[tam] = int(input(f"Nuevo volumen para tamaño {tam}: ").strip())

            print("Contenedores actuales por bodega y tipo:", self.contenedores_por_bodega_y_tipo)
            cant_normal = int(input("Cantidad de contenedores normales por bodega: ").strip())
            cant_largo = int(input("Cantidad de contenedores largos por bodega: ").strip())
            cant_extra = int(input("Cantidad de contenedores extra largos por bodega: ").strip())

            num_camiones = int(input("Número de camiones: ").strip())
            if num_camiones < 1:
                print("Debe haber al menos 1 camión. No se realizaron cambios.")
                return

            self.capacidades_contenedor = {
                "normal": normal,
                "largo": largo,
                "extra_largo": extra
            }
            self.volumenes_caja = nuevos_volumenes
            self.contenedores_por_bodega_y_tipo = {
                "normal": cant_normal,
                "largo": cant_largo,
                "extra_largo": cant_extra
            }
            self.num_camiones = num_camiones

            # Reinicio de estructuras dependientes
            self.bodegas = {
                "Sur": Bodega("Sur"),
                "Norte": Bodega("Norte"),
                "Oriente": Bodega("Oriente"),
                "Occidente": Bodega("Occidente")
            }
            self.registro_contenedores = {}
            self.historico_despachados = {}
            self.cola_recepcion = Cola()
            self.cola_listos_despacho = Cola()
            self.cajas_en_espera = Cola()

            self.flota = ListaEnlazadaDoble()
            self.programacion_camiones = ListaCircularDoble()
            self._crear_camiones()

            self.contador_contenedores = 1
            self._inicializar_contenedores()

            print("Parámetros actualizados correctamente.")
            print("Se reinició el estado operativo para aplicar la nueva configuración.")

        except ValueError:
            print("Entrada inválida. No se realizaron cambios.")

    def resumen_operativo(self):
        print("\n--- RESUMEN OPERATIVO ---")
        print(f"Día actual: {self.dia_actual()}")
        print(f"Cajas recibidas acumuladas: {self.total_cajas_recibidas}")
        print(f"Cajas asignadas acumuladas: {self.total_cajas_asignadas}")
        print(f"Cajas en espera: {self.cajas_en_espera.tamano()}")
        print(f"Contenedores listos para despacho: {self.cola_listos_despacho.tamano()}")
        print(f"Contenedores despachados acumulados: {self.total_contenedores_despachados}")


# =========================================================
# MENÚ
# =========================================================

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


def main():
    empresa = EmpresaLogistica()

    while True:
        print("\n" + "=" * 75)
        print("SIMULADOR LOGÍSTICO - EMPRESA DE CAJAS, CONTENEDORES Y BODEGAS")
        print("=" * 75)
        print(f"Día actual: {empresa.dia_actual()}")
        print("1) Simular un día de recepción")
        print("2) Simular un día de despacho")
        print("3) Mostrar estado actual de todas las bodegas")
        print("4) Mostrar cola de contenedores listos para despacho")
        print("5) Ver detalles de un contenedor específico")
        print("6) Mostrar flota y programación de camiones")
        print("7) Mostrar parámetros del sistema")
        print("8) Reconfigurar parámetros")
        print("9) Avanzar al siguiente día")
        print("10) Resumen operativo")
        print("11) Torre de Hanói")
        print("12) Mostrar árbol de contenedores (ABB)")
        print("0) Salir")

        op = input("Seleccione una opción: ").strip()

        if op == "1":
            empresa.simular_dia_recepcion()

        elif op == "2":
            empresa.simular_dia_despacho()

        elif op == "3":
            empresa.mostrar_estado_bodegas()

        elif op == "4":
            empresa.mostrar_cola_despacho()

        elif op == "5":
            codigo = input("Ingrese el código del contenedor: ").strip()
            empresa.ver_detalle_contenedor(codigo)

        elif op == "6":
            empresa.mostrar_flota_y_programacion()

        elif op == "7":
            empresa.mostrar_parametros()

        elif op == "8":
            empresa.reconfigurar_parametros()

        elif op == "9":
            empresa.avanzar_dia()

        elif op == "10":
            empresa.resumen_operativo()

        elif op == "11":
            menu_hanoi()

        elif op == "12":
            empresa.mostrar_arbol_contenedores()

        elif op == "0":
            print("Programa finalizado.")
            break

        else:
            print("Opción inválida.")


if __name__ == "__main__":
    main()

from collections import deque
from dataclasses import dataclass, field
import random


class Pila:
    def __init__(self):
        self._datos = []

    def apilar(self, valor):
        self._datos.append(valor)

    def esta_vacia(self):
        return not self._datos

    def tamano(self):
        return len(self._datos)

    def elementos(self):
        return self._datos[:]


class Cola:
    def __init__(self):
        self._datos = deque()

    def encolar(self, valor):
        self._datos.append(valor)

    def desencolar(self):
        return self._datos.popleft() if self._datos else None

    def esta_vacia(self):
        return not self._datos

    def tamano(self):
        return len(self._datos)

    def limpiar(self):
        self._datos.clear()

    def elementos(self):
        return list(self._datos)


@dataclass
class Caja:
    codigo: str
    tamano: int
    destino: str
    volumen: int


@dataclass
class Contenedor:
    codigo: str
    tipo: str
    bodega: str
    capacidad: int
    cajas: Pila = field(default_factory=Pila)
    volumen_actual: int = 0
    despachado: bool = False

    def puede_recibir(self, caja: Caja) -> bool:
        return not self.despachado and self.volumen_actual + caja.volumen <= self.capacidad

    def agregar_caja(self, caja: Caja) -> bool:
        if not self.puede_recibir(caja):
            return False
        self.cajas.apilar(caja)
        self.volumen_actual += caja.volumen
        return True

    def ocupacion(self) -> float:
        return 0 if self.capacidad == 0 else self.volumen_actual * 100 / self.capacidad

    def listo(self) -> bool:
        return self.ocupacion() >= 75

    def resumen(self) -> str:
        return (
            f"{self.codigo} | {self.tipo} | {self.bodega} | "
            f"{self.volumen_actual}/{self.capacidad} | {self.ocupacion():.1f}% | "
            f"cajas={self.cajas.tamano()}"
        )


@dataclass
class Camion:
    codigo: str
    ruta: str
    disponible: bool = True
    viajes: int = 0

    def asignar(self) -> bool:
        if not self.disponible:
            return False
        self.disponible = False
        self.viajes += 1
        return True

    def liberar(self):
        self.disponible = True


class EmpresaLogistica:
    def __init__(self):
        self.volumenes = {1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6}
        self.capacidades = {"normal": 40, "largo": 60, "extra_largo": 80}
        self.config_contenedores = {"normal": 3, "largo": 2, "extra_largo": 2}
        self.bodegas = {nombre: [] for nombre in ("Sur", "Norte", "Oriente", "Occidente")}
        self.recepcion = Cola()
        self.listos = Cola()
        self.espera = Cola()
        self.ruta_bodegas = list(self.bodegas)
        self.pos_cinta = 0
        self.camiones = []
        self.turno_camion = 0
        self.registro = {}
        self.historico = {}
        self.cont_cajas = 1
        self.cont_contenedores = 1
        self.dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"]
        self.idx_dia = 0
        self.stats = {
            "cajas_recibidas": 0,
            "cajas_asignadas": 0,
            "cajas_espera": 0,
            "contenedores_despachados": 0,
        }
        self._crear_camiones(5)
        self._inicializar_contenedores()

    def _crear_camiones(self, cantidad):
        rutas = ["Ruta Sur", "Ruta Norte", "Ruta Oriente", "Ruta Occidente", "Ruta Mixta"]
        self.camiones = [Camion(f"CAM-{i:02d}", rutas[(i - 1) % len(rutas)]) for i in range(1, cantidad + 1)]
        self.turno_camion = 0

    def _codigo_contenedor(self, tipo, bodega):
        pref = {"normal": "N", "largo": "L", "extra_largo": "XL"}[tipo]
        codigo = f"{pref}-{bodega[:3].upper()}-{self.cont_contenedores:03d}"
        self.cont_contenedores += 1
        return codigo

    def _inicializar_contenedores(self):
        self.registro.clear()
        self.cont_contenedores = 1
        for nombre_bodega, lista in self.bodegas.items():
            lista.clear()
            for tipo, cantidad in self.config_contenedores.items():
                for _ in range(cantidad):
                    cont = Contenedor(
                        self._codigo_contenedor(tipo, nombre_bodega),
                        tipo,
                        nombre_bodega,
                        self.capacidades[tipo],
                    )
                    lista.append(cont)
                    self.registro[cont.codigo] = cont

    def dia_actual(self):
        return self.dias[self.idx_dia]

    def avanzar_dia(self):
        self.idx_dia = (self.idx_dia + 1) % len(self.dias)
        for camion in self.camiones:
            camion.liberar()
        print(f"\nDía actual: {self.dia_actual()}. Todos los camiones quedaron disponibles.")

    def tipo_para_tamano(self, tamano):
        if tamano <= 2:
            return "normal"
        if tamano <= 4:
            return "largo"
        return "extra_largo"

    def crear_caja(self):
        tamano = random.randint(1, 6)
        destino = random.choice(self.ruta_bodegas)
        caja = Caja(f"CAJA-{self.cont_cajas:05d}", tamano, destino, self.volumenes[tamano])
        self.cont_cajas += 1
        return caja

    def mover_cinta(self, destino):
        nueva_pos = self.ruta_bodegas.index(destino)
        movimientos = (nueva_pos - self.pos_cinta) % len(self.ruta_bodegas)
        self.pos_cinta = nueva_pos
        return movimientos

    def buscar_contenedor(self, destino, tipo, caja):
        for cont in self.bodegas[destino]:
            if cont.tipo == tipo and cont.puede_recibir(caja):
                return cont
        return None

    def generar_recepcion(self, cantidad):
        for _ in range(cantidad):
            self.recepcion.encolar(self.crear_caja())
        self.stats["cajas_recibidas"] += cantidad

    def distribuir_recepcion(self):
        asignadas = en_espera = movimientos = 0
        while not self.recepcion.esta_vacia():
            caja = self.recepcion.desencolar()
            tipo = self.tipo_para_tamano(caja.tamano)
            movimientos += self.mover_cinta(caja.destino)
            cont = self.buscar_contenedor(caja.destino, tipo, caja)
            if cont:
                cont.agregar_caja(caja)
                asignadas += 1
            else:
                self.espera.encolar(caja)
                en_espera += 1
        self.stats["cajas_asignadas"] += asignadas
        self.stats["cajas_espera"] = self.espera.tamano()
        print(f"Asignadas: {asignadas} | En espera: {en_espera} | Movimientos cinta: {movimientos}")

    def reintentar_espera(self):
        pendientes = Cola()
        recuperadas = 0
        while not self.espera.esta_vacia():
            caja = self.espera.desencolar()
            tipo = self.tipo_para_tamano(caja.tamano)
            self.mover_cinta(caja.destino)
            cont = self.buscar_contenedor(caja.destino, tipo, caja)
            if cont:
                cont.agregar_caja(caja)
                recuperadas += 1
            else:
                pendientes.encolar(caja)
        self.espera = pendientes
        self.stats["cajas_espera"] = self.espera.tamano()
        if recuperadas:
            print(f"Cajas recuperadas desde espera: {recuperadas}")

    def actualizar_listos(self):
        self.listos.limpiar()
        for contenedores in self.bodegas.values():
            for cont in contenedores:
                if cont.listo() and not cont.despachado:
                    self.listos.encolar(cont)

    def siguiente_camion_disponible(self):
        if not self.camiones:
            return None
        for _ in range(len(self.camiones)):
            camion = self.camiones[self.turno_camion]
            self.turno_camion = (self.turno_camion + 1) % len(self.camiones)
            if camion.disponible:
                return camion
        return None

    def reemplazar_contenedor(self, contenedor):
        lista = self.bodegas[contenedor.bodega]
        lista[:] = [c for c in lista if c.codigo != contenedor.codigo]
        self.registro.pop(contenedor.codigo, None)
        nuevo = Contenedor(
            self._codigo_contenedor(contenedor.tipo, contenedor.bodega),
            contenedor.tipo,
            contenedor.bodega,
            self.capacidades[contenedor.tipo],
        )
        lista.append(nuevo)
        self.registro[nuevo.codigo] = nuevo

    def simular_recepcion(self):
        if self.dia_actual() == "Sábado":
            print("\nHoy es Sábado. No se reciben cajas.")
            return
        cantidad = random.randint(80, 200)
        print(f"\nRecepción de {self.dia_actual()}: {cantidad} cajas")
        self.generar_recepcion(cantidad)
        self.distribuir_recepcion()
        self.actualizar_listos()

    def simular_despacho(self):
        print(f"\nDespacho de {self.dia_actual()}")
        self.reintentar_espera()
        self.actualizar_listos()
        if self.listos.esta_vacia():
            print("No hay contenedores listos para despacho.")
            return

        despachados = 0
        while not self.listos.esta_vacia() and despachados < len(self.camiones):
            cont = self.listos.desencolar()
            camion = self.siguiente_camion_disponible()
            if not camion:
                break
            camion.asignar()
            cont.despachado = True
            self.historico[cont.codigo] = {
                "dia": self.dia_actual(),
                "camion": camion.codigo,
                "ocupacion": round(cont.ocupacion(), 2),
                "cajas": cont.cajas.tamano(),
            }
            print(f"{cont.codigo} -> {camion.codigo} | {cont.ocupacion():.1f}%")
            self.reemplazar_contenedor(cont)
            despachados += 1
            self.stats["contenedores_despachados"] += 1
        self.actualizar_listos()
        print(f"Contenedores despachados hoy: {despachados}")

    def ver_contenedor(self, codigo):
        cont = self.registro.get(codigo)
        if cont:
            print(cont.resumen())
            for caja in cont.cajas.elementos():
                print(f"  - {caja.codigo} | t={caja.tamano} | {caja.destino} | v={caja.volumen}")
            return
        hist = self.historico.get(codigo)
        if hist:
            print(f"{codigo} | despachado {hist['dia']} | {hist['camion']} | {hist['ocupacion']}% | cajas={hist['cajas']}")
            return
        print("No existe ese contenedor.")

    def mostrar_bodegas(self):
        print(f"\nEstado general - {self.dia_actual()}")
        for nombre, contenedores in self.bodegas.items():
            print(f"\nBodega {nombre}")
            for cont in contenedores:
                print(" ", cont.resumen())
        self.resumen()

    def mostrar_listos(self):
        self.actualizar_listos()
        print("\nCola de despacho")
        if self.listos.esta_vacia():
            print("Sin contenedores listos.")
            return
        for i, cont in enumerate(self.listos.elementos(), start=1):
            print(f"{i}. {cont.resumen()}")

    def mostrar_camiones(self):
        print("\nFlota")
        for camion in self.camiones:
            estado = "Disponible" if camion.disponible else "En ruta"
            print(f"{camion.codigo} | {camion.ruta} | {estado} | viajes={camion.viajes}")

    def resumen(self):
        print(
            f"\nResumen -> recibidas={self.stats['cajas_recibidas']}, "
            f"asignadas={self.stats['cajas_asignadas']}, "
            f"espera={self.espera.tamano()}, "
            f"despachados={self.stats['contenedores_despachados']}"
        )

    def reconfigurar(self):
        try:
            normal = int(input("Capacidad normal: "))
            largo = int(input("Capacidad largo: "))
            extra = int(input("Capacidad extra_largo: "))
            camiones = int(input("Número de camiones: "))
            if min(normal, largo, extra, camiones) <= 0:
                print("Todos los valores deben ser mayores que 0.")
                return
            self.capacidades = {"normal": normal, "largo": largo, "extra_largo": extra}
            self._crear_camiones(camiones)
            self.recepcion = Cola()
            self.listos = Cola()
            self.espera = Cola()
            self.historico.clear()
            self.stats = {k: 0 for k in self.stats}
            self._inicializar_contenedores()
            print("Configuración actualizada correctamente.")
        except ValueError:
            print("Entrada inválida.")


def menu():
    empresa = EmpresaLogistica()
    opciones = {
        "1": empresa.simular_recepcion,
        "2": empresa.simular_despacho,
        "3": empresa.mostrar_bodegas,
        "4": empresa.mostrar_listos,
        "6": empresa.mostrar_camiones,
        "8": empresa.reconfigurar,
        "9": empresa.avanzar_dia,
        "10": empresa.resumen,
    }

    while True:
        print("\n" + "=" * 60)
        print("SIMULADOR LOGÍSTICO OPTIMIZADO")
        print("=" * 60)
        print(f"Día actual: {empresa.dia_actual()}")
        print("1) Simular recepción")
        print("2) Simular despacho")
        print("3) Mostrar bodegas")
        print("4) Mostrar cola de despacho")
        print("5) Ver contenedor")
        print("6) Mostrar camiones")
        print("8) Reconfigurar")
        print("9) Avanzar día")
        print("10) Resumen")
        print("0) Salir")
        op = input("Seleccione una opción: ").strip()

        if op == "0":
            print("Programa finalizado.")
            break
        if op == "5":
            empresa.ver_contenedor(input("Código del contenedor: ").strip())
            continue
        accion = opciones.get(op)
        if accion:
            accion()
        else:
            print("Opción inválida.")


if __name__ == "__main__":
    menu()

"""Gestor de estaciones con altas y bajas consistentes en hash, ABB y AVL."""
import re
from Modelos.estacion import estacion
from config.localidades import LOCALIDADES

TIPOS = ("PLUVIOMETRICA", "METEOROLOGICA", "HIDROMETRICA")


def validar_estacion(e):
    # El numero 10000 se utiliza en el experimento, no en el registro operativo
    # de formato CBA-NNNN. Se admite 0000..9999 para altas manuales.
    if not isinstance(e.codigo, str) or not re.fullmatch(r"CBA-\d{4}", e.codigo):
        raise ValueError("Codigo invalido: debe tener formato CBA-NNNN.")
    if not isinstance(e.numero, int) or isinstance(e.numero, bool) or not (0 <= e.numero <= 9999):
        raise ValueError("Numero fuera de rango (0 a 9999).")
    if e.codigo != f"CBA-{e.numero:04d}":
        raise ValueError("El codigo y el numero deben corresponder a la misma estacion.")
    if not isinstance(e.nombre, str) or not e.nombre.strip():
        raise ValueError("El nombre no puede estar vacio.")
    if e.localidad not in LOCALIDADES:
        raise ValueError("Localidad invalida.")
    if e.tipo not in TIPOS:
        raise ValueError("Tipo invalido. Opciones: " + ", ".join(TIPOS))
    if not isinstance(e.bateria, int) or isinstance(e.bateria, bool) or not 0 <= e.bateria <= 100:
        raise ValueError("La bateria debe estar entre 0 y 100.")
    if not isinstance(e.diasSinVisita, int) or isinstance(e.diasSinVisita, bool) or e.diasSinVisita < 0:
        raise ValueError("Los dias sin visita deben ser un entero no negativo.")


def registrar_en_sistema(sistema, nueva, validar=True):
    """Devuelve (ok, mensaje). Revierte inserciones si una estructura falla."""
    if validar:
        try:
            validar_estacion(nueva)
        except ValueError as exc:
            return False, str(exc)

    if sistema.tabla_hash.buscar(nueva.codigo) is not None:
        return False, "Ya existe una estacion con ese codigo."
    if sistema.abb.buscar(nueva.numero) is not None or sistema.avl.buscar(nueva.numero) is not None:
        return False, "Ya existe una estacion con ese numero."

    hechos = []
    try:
        for estructura, clave in ((sistema.tabla_hash, nueva.codigo),
                                  (sistema.abb, nueva.numero),
                                  (sistema.avl, nueva.numero)):
            if estructura.insertar(nueva) is not True:
                raise RuntimeError(f"Fallo al insertar en {type(estructura).__name__}.")
            hechos.append((estructura, clave))
    except Exception as exc:
        errores = []
        for estructura, clave in reversed(hechos):
            try:
                if estructura.eliminar(clave) is not True:
                    errores.append(type(estructura).__name__)
            except Exception:
                errores.append(type(estructura).__name__)
        if errores:
            raise RuntimeError("Error grave: fallo la insercion y el rollback en " + ", ".join(errores)) from exc
        return False, f"Registro cancelado; se revirtieron los cambios: {exc}"
    return True, "Estacion registrada correctamente."


def eliminar_del_sistema(sistema, codigo):
    """Borra en las tres estructuras y revierte ante fallos."""
    actual = sistema.tabla_hash.buscar(codigo)
    if actual is None:
        return False, "Estacion no encontrada."
    numero = actual.numero
    # Comprobacion previa para no borrar parcialmente datos inconsistentes.
    en_abb = sistema.abb.buscar(numero)
    en_avl = sistema.avl.buscar(numero)
    if en_abb is None or en_avl is None or en_abb.codigo != codigo or en_avl.codigo != codigo:
        return False, "Inconsistencia detectada: estacion ausente o diferente en ABB/AVL. No se elimino nada."

    hechos = []
    try:
        for estructura, clave in ((sistema.tabla_hash, codigo),
                                  (sistema.abb, numero),
                                  (sistema.avl, numero)):
            if estructura.eliminar(clave) is not True:
                raise RuntimeError(f"Fallo al eliminar de {type(estructura).__name__}.")
            hechos.append(estructura)
    except Exception as exc:
        errores = []
        for estructura in reversed(hechos):
            try:
                if estructura.insertar(actual) is not True:
                    errores.append(type(estructura).__name__)
            except Exception:
                errores.append(type(estructura).__name__)
        if errores:
            raise RuntimeError("Error grave: fallo la eliminacion y el rollback en " + ", ".join(errores)) from exc
        return False, f"Eliminacion cancelada; se revirtieron los cambios: {exc}"
    return True, "Estacion eliminada correctamente."


class GestorEstaciones:
    def __init__(self, sistema):
        self.sistema = sistema

    def registrar_estacion(self):
        try:
            codigo = input("Codigo (CBA-NNNN): ").strip().upper()
            numero = int(input("Numero: "))
            # Rechazar antes de solicitar el resto de los campos.
            if self.sistema.tabla_hash.buscar(codigo) is not None:
                print("Error: ya existe una estacion con ese codigo.")
                return
            if self.sistema.abb.buscar(numero) is not None or self.sistema.avl.buscar(numero) is not None:
                print("Error: ya existe una estacion con ese numero.")
                return
            nombre = input("Nombre de la estacion: ").strip()
            print("\nLocalidades disponibles:")
            for i, localidad in enumerate(LOCALIDADES, start=1):
                print(f"{i}. {localidad}")
            opcion = int(input("Seleccione localidad: "))
            if not 1 <= opcion <= len(LOCALIDADES):
                print("Error: localidad invalida.")
                return
            print("Tipos disponibles: " + ", ".join(TIPOS))
            tipo = input("Tipo de estacion: ").strip().upper()
            bateria = int(input("Bateria (0-100): "))
            dias = int(input("Dias sin visita: "))
            nueva = estacion(codigo, numero, nombre, LOCALIDADES[opcion - 1], tipo, bateria, dias)
            ok, mensaje = registrar_en_sistema(self.sistema, nueva)
            print(("\n" if ok else "\nError: ") + mensaje)
        except ValueError as exc:
            print(f"Error de entrada: {exc}")
        except RuntimeError as exc:
            print(f"ERROR DE INTEGRIDAD: {exc}")

    def buscar_estacion(self):
        codigo = input("Codigo: ").strip().upper()
        encontrada = self.sistema.tabla_hash.buscar(codigo)
        if encontrada is None:
            print("Estacion no encontrada")
            return
        print("\nEstacion encontrada:")
        for titulo, valor in (("Codigo", encontrada.codigo), ("Numero", encontrada.numero),
                              ("Nombre", encontrada.nombre), ("Localidad", encontrada.localidad),
                              ("Tipo", encontrada.tipo), ("Bateria", encontrada.bateria),
                              ("Dias sin visita", encontrada.diasSinVisita)):
            print(f"{titulo}: {valor}")

    def eliminar_estacion(self):
        codigo = input("Codigo: ").strip().upper()
        try:
            ok, mensaje = eliminar_del_sistema(self.sistema, codigo)
            print(("\n" if ok else "\nError: ") + mensaje)
        except RuntimeError as exc:
            print(f"ERROR DE INTEGRIDAD: {exc}")

    def mostrar_tabla(self):
        self.sistema.tabla_hash.mostrar()

    def mostrar_estadisticas(self):
        self.sistema.tabla_hash.mostrar_estadisticas()

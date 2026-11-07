import heapq
from collections import Counter
import random

# 1. GENERACIÓN DE ARCHIVO (M6)
def generar_archivo_mediciones(nombre_archivo, cantidad_lineas, semilla=1026):
    rnd = random.Random(semilla)
    with open(nombre_archivo, 'w', encoding='utf-8') as f:
        for _ in range(cantidad_lineas):
            numero = rnd.randint(1, 9999)
            codigo = f"CBA-{numero:04d}"
            # Formato: CBA-0347;2026-10-13;08:00;T=18.4;H=62;P=0.0;BAT=18
            fecha = f"2026-{rnd.randint(1,12):02d}-{rnd.randint(1,28):02d}"
            hora = f"{rnd.randint(0,23):02d}:{rnd.randint(0,59):02d}"
            temp = round(rnd.uniform(-5.0, 45.0), 1)
            hum = rnd.randint(10, 100)
            prec = round(rnd.uniform(0.0, 150.0), 1)
            bat = rnd.randint(0, 100)
            
            linea = f"{codigo};{fecha};{hora};T={temp};H={hum};P={prec};BAT={bat}\n"
            f.write(linea)

# 2. IMPLEMENTACIÓN DE HUFFMAN
class Nodo:
    def __init__(self, caracter, frecuencia):
        self.caracter = caracter
        self.frecuencia = frecuencia
        self.izq = None
        self.der = None

    def __lt__(self, otro):
        return self.frecuencia < otro.frecuencia

def construirArbolHuffman(texto):
    if not texto:
        return None

    frecuencias = Counter(texto)
    cola = [Nodo(char, freq) for char, freq in frecuencias.items()]
    heapq.heapify(cola)
    
    if len(cola) == 1:
        nodo_unico = heapq.heappop(cola)
        raiz = Nodo(None, nodo_unico.frecuencia)
        raiz.izq = nodo_unico
        return raiz

    while len(cola) > 1:
        izq = heapq.heappop(cola)
        der = heapq.heappop(cola)
        
        nuevo = Nodo(None, izq.frecuencia + der.frecuencia)
        nuevo.izq = izq
        nuevo.der = der
        
        heapq.heappush(cola, nuevo)
        
    return heapq.heappop(cola)

def generar_tabla_codigos(nodo, codigo_actual="", tabla=None):
    if tabla is None:
        tabla = {}
        
    if nodo is not None:
        if nodo.caracter is not None:
            tabla[nodo.caracter] = codigo_actual
        generar_tabla_codigos(nodo.izq, codigo_actual + "0", tabla)
        generar_tabla_codigos(nodo.der, codigo_actual + "1", tabla)
        
    return tabla

def codificar(texto, tabla_codigos):
    return "".join([tabla_codigos[char] for char in texto])

def decodificar(texto_comprimido, raiz):
    if not texto_comprimido or raiz is None:
        return ""
        
    resultado = []
    actual = raiz
    
    for bit in texto_comprimido:
        if bit == '0':
            actual = actual.izq
        else:
            actual = actual.der
            
        if actual.caracter is not None:
            resultado.append(actual.caracter)
            actual = raiz
            
    return "".join(resultado)

# 3. y 4. VALIDACIONES Y MÉTRICAS
def verificar_prefijos(tabla):
    codigos = list(tabla.values())
    for i in range(len(codigos)):
        for j in range(len(codigos)):
            if i != j and codigos[i].startswith(codigos[j]):
                return False, f"Error: {codigos[j]} es prefijo de {codigos[i]}"
    return True, "Validación OK: Ningún código es prefijo de otro."

def reporte_compresion(texto_original, texto_comprimido, tabla):
    frecuencias = Counter(texto_original)
    print("\n--- Tabla de Frecuencias y Códigos ---")
    print(f"{'Char':<6} | {'Frecuencia':<12} | {'Código Huffman'}")
    print("-" * 45)
    for char, freq in frecuencias.most_common():
        print(f"{repr(char):<6} | {freq:<12} | {tabla[char]}")
        
    _, msj_prefijos = verificar_prefijos(tabla)
    print(f"\n{msj_prefijos}")

    bits_original = len(texto_original) * 8
    bits_comprimido = len(texto_comprimido)
    tasa = (bits_original - bits_comprimido) / bits_original * 100
    
    print("\n--- Métricas de Compresión ---")
    print(f"Tamaño Original (8 bits/char): {bits_original} bits")
    print(f"Tamaño Comprimido:             {bits_comprimido} bits")
    print(f"Tasa de compresión:            {tasa:.2f}%")

# EJECUCIÓN PRINCIPAL
def ejecutar_modulo():
    print(" PRUEBA DE VERIFICACIÓN (Punto 5) ")
    texto_prueba = "WWXWYZWX"
    raiz_prueba = construirArbolHuffman(texto_prueba)
    tabla_prueba = generar_tabla_codigos(raiz_prueba)
    comprimido_prueba = codificar(texto_prueba, tabla_prueba)
    
    reporte_compresion(texto_prueba, comprimido_prueba, tabla_prueba)
    
    print(f"\nBits resultantes de WWXWYZWX: {len(comprimido_prueba)}")
    if len(comprimido_prueba) == 14:
        print("VERIFICACIÓN LECTURA EXITOSA: 64 bits comprimidos a 14 bits.")

    print("\n\n COMPRESIÓN DE ARCHIVO DE MEDICIONES (Puntos 1 a 5) ")
    archivo = "mediciones.txt"
    generar_archivo_mediciones(archivo, 5000)
    
    with open(archivo, 'r', encoding='utf-8') as f:
        texto = f.read()
    
    raiz = construirArbolHuffman(texto)
    tabla = generar_tabla_codigos(raiz)
    comprimido = codificar(texto, tabla)
    
    reporte_compresion(texto, comprimido, tabla)
    
    print("\nDecodificando archivo...")
    decodificado = decodificar(comprimido, raiz)
    
    if decodificado == texto:
        print("ÉXITO: El texto decodificado es EXACTAMENTE igual al original.")
    else:
        print("ERROR en la decodificación.")

if __name__ == "__main__":
    ejecutar_modulo()
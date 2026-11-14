from pathlib import Path

from M4_huffman.huffman import (
    generar_archivo_mediciones,
    construirArbolHuffman,
    generar_tabla_codigos,
    codificar,
    decodificar,
    reporte_compresion,
    verificar_prefijos
)


class GestorCompresion:

    def __init__(self, sistema):
        self.sistema = sistema

        # El archivo se guardará dentro de la carpeta m4
        self.archivo = (
            Path(__file__).resolve().parent.parent
            / "m4"
            / "mediciones.txt"
        )

        # Estado de la compresión actual
        self.texto_original = None
        self.raiz_huffman = None
        self.tabla_codigos = None
        self.texto_comprimido = None

    def verificar_ejemplo_huffman(self):
        """
        Ejecuta el ejemplo obligatorio WWXWYZWX sin modificar
        el estado de la compresión del archivo de mediciones.
        """

        texto = "WWXWYZWX"

        raiz = construirArbolHuffman(texto)
        tabla = generar_tabla_codigos(raiz)
        comprimido = codificar(texto, tabla)
        decodificado = decodificar(comprimido, raiz)

        print("\n====================================")
        print(" EJEMPLO HUFFMAN")
        print("====================================")
        print("Texto original:", texto)
        print("Texto comprimido:", comprimido)
        print("Cantidad de bits:", len(comprimido))

        print("\nCódigos generados:")

        for caracter, codigo in tabla.items():
            print(f"{repr(caracter)} -> {codigo}")

        valido, mensaje = verificar_prefijos(tabla)

        print("\nValidación de prefijos:")
        print(mensaje)

        print("\nTexto decodificado:", decodificado)

        if decodificado == texto:
            print("Verificación correcta: el texto recuperado coincide.")
        else:
            print("Error: el texto recuperado no coincide.")

        if len(comprimido) == 14:
            print("El ejemplo se comprimió correctamente a 14 bits.")
        else:
            print(
                "La cantidad de bits puede variar si existen empates "
                "entre frecuencias."
            )

    def generar_mediciones(self):
        """
        Genera el archivo de mediciones simuladas utilizando
        la función correspondiente del módulo Huffman.
        """

        try:
            cantidad = int(
                input("Cantidad de mediciones a generar: ")
            )

            if cantidad <= 0:
                print("La cantidad debe ser mayor que cero.")
                return

        except ValueError:
            print("Debe ingresar un número entero.")
            return

        try:
            semilla_texto = input(
                "Semilla aleatoria [1026]: "
            ).strip()

            if semilla_texto == "":
                semilla = 1026
            else:
                semilla = int(semilla_texto)

        except ValueError:
            print("La semilla debe ser un número entero.")
            return

        generar_archivo_mediciones(
            self.archivo,
            cantidad,
            semilla
        )

        # Se limpia cualquier compresión anterior
        self.texto_original = None
        self.raiz_huffman = None
        self.tabla_codigos = None
        self.texto_comprimido = None

        print("\nArchivo generado correctamente.")
        print("Ruta:", self.archivo)
        print("Mediciones generadas:", cantidad)
        print("Semilla utilizada:", semilla)

    def comprimir_archivo(self):
        """
        Lee mediciones.txt, construye el árbol Huffman,
        genera los códigos y comprime el contenido.
        """

        if not self.archivo.exists():
            print("\nTodavía no existe el archivo de mediciones.")
            print("Primero seleccione la opción 2 para generarlo.")
            return

        try:
            with self.archivo.open(
                "r",
                encoding="utf-8"
            ) as archivo:
                self.texto_original = archivo.read()

        except OSError as error:
            print("No se pudo leer el archivo:", error)
            return

        if not self.texto_original:
            print("El archivo de mediciones está vacío.")
            return

        self.raiz_huffman = construirArbolHuffman(
            self.texto_original
        )

        self.tabla_codigos = generar_tabla_codigos(
            self.raiz_huffman
        )

        self.texto_comprimido = codificar(
            self.texto_original,
            self.tabla_codigos
        )

        print("\nArchivo comprimido correctamente.")
        print(
            "Caracteres originales:",
            len(self.texto_original)
        )
        print(
            "Símbolos diferentes:",
            len(self.tabla_codigos)
        )
        print(
            "Bits comprimidos:",
            len(self.texto_comprimido)
        )

    def mostrar_metricas(self):
        """
        Muestra la tabla de frecuencias, códigos Huffman,
        tamaños y porcentaje de compresión.
        """

        if not self._hay_compresion():
            return

        reporte_compresion(
            self.texto_original,
            self.texto_comprimido,
            self.tabla_codigos
        )

    def validar_descompresion(self):
        """
        Decodifica la secuencia comprimida y verifica que el
        resultado coincida exactamente con el archivo original.
        """

        if not self._hay_compresion():
            return

        texto_decodificado = decodificar(
            self.texto_comprimido,
            self.raiz_huffman
        )

        print("\n====================================")
        print(" VALIDACIÓN DE INTEGRIDAD")
        print("====================================")

        if texto_decodificado == self.texto_original:
            print(
                "Validación correcta: el texto decodificado "
                "coincide exactamente con el original."
            )
        else:
            print(
                "Error: el texto decodificado no coincide "
                "con el original."
            )

        print(
            "Caracteres originales:",
            len(self.texto_original)
        )

        print(
            "Caracteres recuperados:",
            len(texto_decodificado)
        )

    def mostrar_estado(self):
        """
        Muestra el estado actual del proceso.
        """

        print("\n====================================")
        print(" ESTADO DE LA COMPRESIÓN")
        print("====================================")
        print("Archivo:", self.archivo)
        print(
            "Archivo generado:",
            "Sí" if self.archivo.exists() else "No"
        )
        print(
            "Archivo cargado:",
            "Sí" if self.texto_original is not None else "No"
        )
        print(
            "Árbol Huffman construido:",
            "Sí" if self.raiz_huffman is not None else "No"
        )
        print(
            "Tabla de códigos generada:",
            "Sí" if self.tabla_codigos is not None else "No"
        )
        print(
            "Compresión realizada:",
            "Sí" if self.texto_comprimido is not None else "No"
        )

    def _hay_compresion(self):
        """
        Verifica que exista una compresión antes de mostrar
        métricas o validar la descompresión.
        """

        if (
            self.texto_original is None
            or self.raiz_huffman is None
            or self.tabla_codigos is None
            or self.texto_comprimido is None
        ):
            print("\nTodavía no se realizó ninguna compresión.")
            print("Primero seleccione la opción 3.")
            return False

        return True
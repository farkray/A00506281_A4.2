#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Módulo para analizar la frecuencia de palabras en archivos de texto.

Este módulo implementa un contador de frecuencia de palabras que lee un archivo
de texto, identifica palabras únicas y cuenta sus ocurrencias. El análisis se
realiza utilizando algoritmos básicos sin depender de bibliotecas especializadas.
"""

import sys
import time
from datetime import datetime
from typing import Dict, List


class AnalizadorTextoError(Exception):
    """Clase base para excepciones específicas del analizador de texto."""


class ArchivoError(AnalizadorTextoError):
    """Excepción para errores relacionados con el manejo de archivos."""


class ProcesadorTexto:
    """
    Clase para procesar y analizar texto.
    
    Esta clase contiene métodos para limpiar texto, separar palabras y
    realizar análisis de frecuencia de palabras.
    """

    @staticmethod
    def limpiar_palabra(palabra: str) -> str:
        """
        Limpia una palabra de caracteres no deseados.

        Elimina signos de puntuación y convierte a minúsculas para
        asegurar un conteo consistente.

        Args:
            palabra: La palabra a limpiar.

        Returns:
            La palabra limpia en minúsculas.
        """
        # Eliminamos puntuación común al inicio y final de la palabra
        signos_puntuacion = '.,;:!?"\'()[]{}¿¡'
        palabra_limpia = palabra.strip(signos_puntuacion).lower()
        return palabra_limpia

    def dividir_en_palabras(self, texto: str) -> List[str]:
        """
        Divide un texto en palabras individuales.

        Args:
            texto: El texto a dividir.

        Returns:
            Lista de palabras limpias y no vacías.
        """
        # Dividimos por espacios y filtramos palabras vacías
        palabras_sucias = texto.split()
        return [
            palabra for palabra in (
                self.limpiar_palabra(p) for p in palabras_sucias
            ) if palabra
        ]

    def contar_frecuencias(self, palabras: List[str]) -> Dict[str, int]:
        """
        Cuenta la frecuencia de cada palabra en la lista.

        Args:
            palabras: Lista de palabras a analizar.

        Returns:
            Diccionario con las frecuencias de cada palabra.
        """
        frecuencias = {}
        for palabra in palabras:
            frecuencias[palabra] = frecuencias.get(palabra, 0) + 1
        return frecuencias


class GestorArchivos:
    """
    Clase para manejar operaciones de archivo.
    
    Proporciona métodos para leer archivos de texto y guardar resultados.
    """

    def leer_archivo(self, ruta_archivo: str) -> str:
        """
        Lee el contenido completo de un archivo de texto.

        Args:
            ruta_archivo: Ruta al archivo a leer.

        Returns:
            Contenido del archivo como texto.

        Raises:
            ArchivoError: Si hay problemas al leer el archivo.
        """
        try:
            with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
                return archivo.read()
        except FileNotFoundError as error:
            raise ArchivoError(
                f"No se encontró el archivo: {ruta_archivo}"
            ) from error
        except Exception as error:
            raise ArchivoError(
                f"Error al leer el archivo: {str(error)}"
            ) from error

    def guardar_resultados(
        self,
        resultados: str,
        nombre_archivo: str = 'WordCountResults.txt'
    ) -> None:
        """
        Guarda los resultados en un archivo.

        Args:
            resultados: Texto a guardar.
            nombre_archivo: Nombre del archivo de salida.
        """
        try:
            with open(nombre_archivo, 'a', encoding='utf-8') as archivo:
                archivo.write(resultados)
        except IOError as error:
            print(f"Error al guardar los resultados: {str(error)}")


class FormateadorResultados:
    """
    Clase para formatear los resultados del análisis.
    
    Proporciona métodos para crear representaciones legibles de los resultados.
    """

    def formatear_frecuencias(
        self,
        frecuencias: Dict[str, int],
        tiempo: float
    ) -> str:
        """
        Formatea los resultados del análisis para su presentación.

        Args:
            frecuencias: Diccionario de frecuencias de palabras.
            tiempo: Tiempo de ejecución del análisis.

        Returns:
            Texto formateado con los resultados.
        """
        # Ordenamos las palabras por frecuencia (mayor a menor)
        palabras_ordenadas = sorted(
            frecuencias.items(),
            key=lambda x: (-x[1], x[0])
        )

        # Creamos el encabezado con la fecha y hora
        encabezado = (
            f"\n{'='*60}\n"
            f"Análisis realizado el: {datetime.now()}\n"
            f"{'='*60}\n"
            f"{'Palabra':<30} | {'Frecuencia':>10}\n"
            f"{'-'*60}\n"
        )

        # Formateamos cada línea de resultados
        cuerpo = "".join(
            f"{palabra:<30} | {frecuencia:>10}\n"
            for palabra, frecuencia in palabras_ordenadas
        )

        # Añadimos el resumen y el tiempo de ejecución
        resumen = (
            f"{'-'*60}\n"
            f"Total de palabras únicas: {len(frecuencias):>10}\n"
            f"Total de palabras procesadas: "
            f"{sum(frecuencias.values()):>10}\n"
            f"Tiempo de ejecución: {tiempo:.4f} segundos\n"
            f"{'='*60}\n\n"
        )

        return encabezado + cuerpo + resumen


def main():
    """
    Función principal del programa.

    Coordina la lectura del archivo, el análisis de palabras y la
    presentación de resultados.
    """
    if len(sys.argv) != 2:
        print("Uso: python word_count.py archivo_texto.txt")
        sys.exit(1)

    tiempo_inicio = time.time()

    try:
        # Inicializamos los componentes necesarios
        gestor_archivos = GestorArchivos()
        procesador = ProcesadorTexto()
        formateador = FormateadorResultados()

        # Leemos y procesamos el archivo
        texto = gestor_archivos.leer_archivo(sys.argv[1])
        palabras = procesador.dividir_en_palabras(texto)
        frecuencias = procesador.contar_frecuencias(palabras)

        # Calculamos el tiempo y formateamos resultados
        tiempo_total = time.time() - tiempo_inicio
        resultados = formateador.formatear_frecuencias(
            frecuencias,
            tiempo_total
        )

        # Mostramos y guardamos los resultados
        print(resultados)
        gestor_archivos.guardar_resultados(resultados)
        print("Resultados guardados en 'WordCountResults.txt'")

    except AnalizadorTextoError as error:
        print(f"Error: {str(error)}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nOperación cancelada por el usuario")
        sys.exit(1)
    except Exception as error:  # pylint: disable=broad-except
        print(f"Error inesperado: {str(error)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
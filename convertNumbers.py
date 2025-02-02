#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# pylint: disable=C0103  # Permitimos el nombre del archivo según los requisitos

"""
Módulo para la conversión de números decimales a binario y hexadecimal.

Este módulo implementa algoritmos de conversión desde cero, sin utilizar
funciones incorporadas de Python. Lee números desde un archivo, realiza
las conversiones y guarda los resultados tanto en pantalla como en archivo.
"""

import sys
import time
from datetime import datetime
from typing import List, Tuple


class ConversionError(Exception):
    """Clase base para excepciones específicas del módulo de conversión."""


class ArchivoError(ConversionError):
    """Excepción para errores relacionados con el manejo de archivos."""


class GestorArchivos:
    """Clase para manejar operaciones de archivo."""

    @staticmethod
    def leer_numeros(ruta_archivo: str) -> List[int]:
        """
        Lee números desde un archivo de texto, manejando posibles errores.

        Args:
            ruta_archivo: Ruta al archivo que contiene los números.

        Returns:
            Lista de números enteros válidos encontrados en el archivo.

        Raises:
            ArchivoError: Si hay problemas con el archivo o su contenido.
        """
        numeros = []
        try:
            with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
                for num_linea, linea in enumerate(archivo, 1):
                    try:
                        numero = int(float(linea.strip()))
                        numeros.append(numero)
                    except ValueError:
                        print(f"Error en línea {num_linea}: '{linea.strip()}' "
                              "no es un número válido")
        except FileNotFoundError as error:
            raise ArchivoError(f"No se encontró el archivo: {ruta_archivo}") from error
        except Exception as error:
            raise ArchivoError(f"Error al leer el archivo: {str(error)}") from error

        if not numeros:
            raise ArchivoError("No se encontraron números válidos en el archivo")

        return numeros

    @staticmethod
    def guardar_resultados(resultados: str, 
                          nombre_archivo: str = 'ConvertionResults.txt') -> None:
        """
        Añade los resultados al archivo de salida.

        Args:
            resultados: Texto con los resultados a guardar.
            nombre_archivo: Nombre del archivo donde guardar los resultados.
        """
        try:
            with open(nombre_archivo, 'a', encoding='utf-8') as archivo:
                archivo.write(resultados)
        except IOError as error:
            print(f"Error al guardar los resultados: {str(error)}")


class Convertidor:
    """Clase para realizar conversiones numéricas a diferentes bases."""

    def __init__(self):
        """Inicializa el convertidor con los dígitos hexadecimales."""
        self.digitos_hex = "0123456789ABCDEF"

    def decimal_a_binario(self, numero: int) -> str:
        """
        Convierte un número decimal a binario usando división sucesiva.

        Args:
            numero: Número decimal entero a convertir.

        Returns:
            Representación binaria del número como cadena.
        """
        if numero == 0:
            return "0"

        es_negativo = numero < 0
        numero = abs(numero)

        binario = []
        while numero > 0:
            binario.append(str(numero % 2))
            numero //= 2

        return f"-{''.join(binario[::-1])}" if es_negativo else ''.join(binario[::-1])

    def decimal_a_hexadecimal(self, numero: int) -> str:
        """
        Convierte un número decimal a hexadecimal usando división sucesiva.

        Args:
            numero: Número decimal entero a convertir.

        Returns:
            Representación hexadecimal del número como cadena.
        """
        if numero == 0:
            return "0"

        es_negativo = numero < 0
        numero = abs(numero)

        hexadecimal = []
        while numero > 0:
            hexadecimal.append(self.digitos_hex[numero % 16])
            numero //= 16

        return f"-{''.join(hexadecimal[::-1])}" if es_negativo else ''.join(hexadecimal[::-1])


def formatear_resultados(numeros: List[int], 
                        conversiones: List[Tuple[str, str]], 
                        tiempo: float) -> str:
    """
    Formatea los resultados de las conversiones para su presentación.

    Args:
        numeros: Lista de números originales.
        conversiones: Lista de tuplas (binario, hexadecimal).
        tiempo: Tiempo de ejecución del programa.

    Returns:
        Cadena formateada con los resultados.
    """
    encabezado = (
        f"\n{'='*60}\n"
        f"Conversiones realizadas el: {datetime.now()}\n"
        f"{'='*60}\n"
        f"{'Decimal':>12} | {'Binario':>16} | {'Hexadecimal':>12}\n"
        f"{'-'*50}\n"
    )

    cuerpo = "".join(
        f"{numero:>12} | {binario:>16} | {hexa:>12}\n"
        for numero, (binario, hexa) in zip(numeros, conversiones)
    )

    pie = (
        f"{'-'*50}\n"
        f"Tiempo de ejecución: {tiempo:.4f} segundos\n"
        f"{'='*60}\n\n"
    )

    return encabezado + cuerpo + pie


def main():
    """
    Función principal del programa.

    Lee números desde un archivo, realiza las conversiones y guarda los resultados.
    """
    if len(sys.argv) != 2:
        print("Uso: python convertNumbers.py archivo_numeros.txt")
        sys.exit(1)

    tiempo_inicio = time.time()

    try:
        gestor = GestorArchivos()
        numeros = gestor.leer_numeros(sys.argv[1])
        convertidor = Convertidor()

        conversiones = [
            (convertidor.decimal_a_binario(n),
             convertidor.decimal_a_hexadecimal(n))
            for n in numeros
        ]

        tiempo_total = time.time() - tiempo_inicio
        resultados = formatear_resultados(numeros, conversiones, tiempo_total)
        print(resultados)

        gestor.guardar_resultados(resultados)
        print("Resultados guardados en 'ConvertionResults.txt'")

    except (ConversionError, IOError) as error:
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
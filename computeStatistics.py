#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Módulo para análisis estadístico de datos numéricos.

Este módulo proporciona funcionalidad para leer números desde un archivo,
calcular estadísticas descriptivas básicas (media, mediana, moda,
desviación estándar y varianza) y guardar los resultados.

Todas las operaciones estadísticas se implementan usando algoritmos básicos,
sin depender de bibliotecas estadísticas externas.
"""

import sys
import time
from typing import List, Union
from datetime import datetime


class EstadisticasError(Exception):
    """Clase base para excepciones específicas del módulo."""


class ArchivoError(EstadisticasError):
    """Excepción lanzada cuando hay problemas con el archivo de entrada."""


def leer_archivo(ruta_archivo: str) -> List[float]:
    """
    Lee y valida números desde un archivo de texto.

    Args:
        ruta_archivo: Ruta al archivo que contiene los números, uno por línea.

    Returns:
        Lista de números válidos encontrados en el archivo.

    Raises:
        ArchivoError: Si hay problemas al leer el archivo o no hay números válidos.
    """
    numeros = []
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            for num_linea, linea in enumerate(archivo, 1):
                try:
                    numero = float(linea.strip())
                    numeros.append(numero)
                except ValueError:
                    print(f"Error en línea {num_linea}: '{linea.strip()}' no es número")
    except FileNotFoundError as error:
        raise ArchivoError(f"No se encontró el archivo: {ruta_archivo}") from error
    except Exception as error:
        raise ArchivoError(f"Error al leer el archivo: {str(error)}") from error

    if not numeros:
        raise ArchivoError("No se encontraron números válidos en el archivo")

    return numeros


class CalculadoraEstadistica:
    """Clase para realizar cálculos estadísticos básicos."""

    def __init__(self, datos: List[float]):
        """
        Inicializa la calculadora con un conjunto de datos.

        Args:
            datos: Lista de números sobre los que se realizarán los cálculos.
        """
        self.datos = datos
        self.n_elementos = len(datos)

    def calcular_media(self) -> float:
        """
        Calcula la media aritmética de los datos.

        Returns:
            Media aritmética de los datos.
        """
        return sum(self.datos) / self.n_elementos

    def calcular_mediana(self) -> float:
        """
        Calcula la mediana de los datos.

        Returns:
            Mediana de los datos.
        """
        ordenados = sorted(self.datos)
        mitad = self.n_elementos // 2

        if self.n_elementos % 2 == 0:
            return (ordenados[mitad - 1] + ordenados[mitad]) / 2
        return ordenados[mitad]

    def calcular_moda(self) -> Union[float, str]:
        """
        Calcula la moda de los datos.

        Returns:
            Moda de los datos o mensaje descriptivo si no hay moda única.
        """
        frecuencias = {}
        for numero in self.datos:
            frecuencias[numero] = frecuencias.get(numero, 0) + 1

        max_frecuencia = max(frecuencias.values())
        modas = [
            num for num, freq in frecuencias.items()
            if freq == max_frecuencia
        ]

        if len(modas) == self.n_elementos:
            return "No hay moda (todos los valores aparecen una vez)"
        if len(modas) > 1:
            return f"Múltiples modas: {modas}"
        return modas[0]

    def calcular_varianza(self, media: float) -> float:
        """
        Calcula la varianza de los datos.

        Args:
            media: Media aritmética de los datos.

        Returns:
            Varianza de los datos.
        """
        suma_cuadrados = sum((x - media) ** 2 for x in self.datos)
        return suma_cuadrados / self.n_elementos

    @staticmethod
    def calcular_desviacion_estandar(varianza: float) -> float:
        """
        Calcula la desviación estándar a partir de la varianza.

        Args:
            varianza: Varianza de los datos.

        Returns:
            Desviación estándar de los datos.
        """
        return varianza ** 0.5


def guardar_resultados(contenido: str, nombre_archivo: str = 'StatisticsResults.txt'):
    """
    Guarda los resultados en un archivo de texto, añadiendo al final del archivo
    en lugar de sobrescribir. Incluye marca de tiempo para cada ejecución.

    Args:
        contenido: Texto a guardar en el archivo.
        nombre_archivo: Nombre del archivo de salida.

    Raises:
        IOError: Si hay problemas al escribir el archivo.
    """
    try:
        # Creamos una marca de tiempo para esta ejecución
        marca_tiempo = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Preparamos el contenido con un separador claro entre ejecuciones
        contenido_con_tiempo = (
            f"\n{'='*60}\n"
            f"Ejecución realizada el: {marca_tiempo}\n"
            f"{'='*60}\n"
            f"{contenido}\n"
        )
        
        # Abrimos el archivo en modo append ('a') en lugar de write ('w')
        with open(nombre_archivo, 'a', encoding='utf-8') as archivo:
            archivo.write(contenido_con_tiempo)
            
    except IOError as error:
        print(f"Error al guardar resultados: {str(error)}")
        raise


def main():
    """
    Función principal del programa.

    Lee los datos, calcula estadísticas y guarda los resultados.
    """
    if len(sys.argv) != 2:
        print("Uso: python computeStatistics.py archivo_datos.txt")
        sys.exit(1)

    tiempo_inicio = time.time()

    try:
        numeros = leer_archivo(sys.argv[1])
        calculadora = CalculadoraEstadistica(numeros)

        media = calculadora.calcular_media()
        mediana = calculadora.calcular_mediana()
        moda = calculadora.calcular_moda()
        varianza = calculadora.calcular_varianza(media)
        desviacion = calculadora.calcular_desviacion_estandar(varianza)

        tiempo_total = time.time() - tiempo_inicio

        resultados = (
            "\nResultados del análisis estadístico:\n"
            f"{'='*40}\n"
            f"Cantidad de números analizados: {len(numeros)}\n"
            f"Media: {media:.4f}\n"
            f"Mediana: {mediana:.4f}\n"
            f"Moda: {moda}\n"
            f"Varianza: {varianza:.4f}\n"
            f"Desviación estándar: {desviacion:.4f}\n"
            f"{'='*40}\n"
            f"Tiempo de ejecución: {tiempo_total:.4f} segundos\n"
        )

        print(resultados)
        guardar_resultados(resultados)
        print("Resultados guardados en 'StatisticsResults.txt'")

    except EstadisticasError as error:
        print(f"Error: {str(error)}")
        sys.exit(1)
    except Exception as error:
        print(f"Error inesperado: {str(error)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
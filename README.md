# Programas de Análisis y Procesamiento de Datos
## Autor: Dr. Farid Krayem Pineda
### Matricula: A00506281
### Curso: Pruebas de software y aseguramiento de la calidad
### Tec de Monterrey
Este repositorio contiene tres programas Python diseñados para realizar diferentes tipos de análisis y procesamiento de datos. Cada programa está optimizado para manejar archivos desde cientos hasta miles de elementos y cumple con las convenciones de estilo PEP8.

## 1. Análisis Estadístico (computeStatistics.py)

### Descripción
Programa que calcula estadísticas descriptivas básicas de un conjunto de números. Implementa los cálculos desde cero, sin utilizar bibliotecas estadísticas.

### Funcionalidades
- Cálculo de media
- Cálculo de mediana
- Cálculo de moda
- Cálculo de desviación estándar
- Cálculo de varianza

### Uso
```bash
python computeStatistics.py fileWithData.txt
```

### Archivo de Salida: StatisticsResults.txt
El archivo guarda los resultados de cada ejecución, incluyendo:
- Fecha y hora de la ejecución
- Estadísticas calculadas
- Tiempo de ejecución
- Los resultados se añaden al final del archivo, manteniendo un historial de todas las ejecuciones

## 2. Conversor de Bases Numéricas (convertNumbers.py)

### Descripción
Programa que convierte números decimales a sus representaciones binarias y hexadecimales. Implementa los algoritmos de conversión desde cero.

### Funcionalidades
- Conversión a binario (base 2)
- Conversión a hexadecimal (base 16)
- Manejo de números positivos y negativos

### Uso
```bash
python convertNumbers.py fileWithData.txt
```

### Archivo de Salida: ConvertionResults.txt
El archivo almacena:
- Fecha y hora de la ejecución
- Tabla con números originales y sus conversiones
- Tiempo de ejecución
- Los resultados se añaden secuencialmente, preservando el historial

## 3. Contador de Palabras (wordCount.py)

### Descripción
Programa que analiza la frecuencia de palabras en archivos de texto. Implementa el procesamiento de texto y conteo desde cero.

### Funcionalidades
- Identificación de palabras únicas
- Conteo de frecuencia de cada palabra
- Normalización de texto (conversión a minúsculas)
- Limpieza de signos de puntuación

### Uso
```bash
python wordCount.py fileWithData.txt
```

### Archivo de Salida: WordCountResults.txt
El archivo guarda:
- Fecha y hora del análisis
- Lista de palabras y sus frecuencias
- Estadísticas totales (palabras únicas, total de palabras)
- Tiempo de ejecución
- Los resultados se añaden cronológicamente al archivo

## Características Comunes

Todos los programas comparten las siguientes características:
- Manejo robusto de errores
- Medición del tiempo de ejecución
- Formato claro y legible en los archivos de salida
- Capacidad para procesar grandes volúmenes de datos
- Cumplimiento con PEP8
- Documentación detallada del código

## Requisitos
- Python 3.x
- No se requieren bibliotecas externas

## Notas Importantes
- Los archivos de entrada deben tener el formato correcto según el programa
- Los archivos de salida se crean automáticamente si no existen
- Cada ejecución añade sus resultados al final del archivo correspondiente
- Se muestran mensajes de error claros en caso de problemas

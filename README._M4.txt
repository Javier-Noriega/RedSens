¿Por qué el archivo de mediciones se comprime bastante pero no al nivel de un texto con muchos caracteres repetidos?

Huffman comprime mejor cuanto más se repite un pequeño grupo de caracteres (baja entropía), ya que les asigna códigos ultra cortos de 1 o 2 bits, logrando una compresión extrema. 

En nuestro archivo de mediciones pasa algo distinto: aunque ciertos símbolos frecuentes (como guiones, puntos y coma o números) bajan de 8 a 3 o 4 bits, la gran variedad de datos dinámicos (fechas y valores aleatorios) hace que ningún carácter domine por completo. Al estar las frecuencias más repartidas, el árbol de Huffman queda equilibrado; por lo tanto, la compresión es buena y reduce el peso original, pero se queda en una tasa moderada en comparación con un texto altamente repetitivo.
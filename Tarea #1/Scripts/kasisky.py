import re
import sys
from functools import reduce
from math import gcd, sqrt


def leerArchivo(nombre):
    """
    Lee un archivo de texto y regresa su contenido como cadena.
    leerArchivo("mensaje.txt") = "HOLA MUNDO..."
    """
    f = open(nombre)
    contenido = f.read()
    f.close()
    return contenido


def distanciaAFrecuenciasNormales(aeosFrecuencias):
    """
    Regresa la distancia euclidiana entre la frecuencia de las letras AEOS y la frecuencia
    de estas letras en el español. Mientras más cercana a 0, más se parece al español.
    distanciaAFrecuenciasNormales([0.13, 0.13, 0.09, 0.08]) ≈ 0.014
    distanciaAFrecuenciasNormales([0.0, 0.0, 0.0, 0.0])     ≈ 0.207
    """
    frecuenciasNormales = [0.1314, 0.1314, 0.0916, 0.0782]
    suma = 0
    for i in range(0, 4):
        suma += (frecuenciasNormales[i] - aeosFrecuencias[i]) ** 2
    return sqrt(suma)


def generarClave(claveBase, longitud):
    # generarClave("perro", 4) = ["p", "e", "r", "r"]
    longitudClaveBase = len(claveBase)
    clave = [claveBase[i % longitudClaveBase] for i in range(0, longitud)]
    return clave


def descifrar(mensaje, clave):
    """
    Descifra un mensaje usando el Algoritmo de Vigenere: M[i] = (C[i] - K[i] + 26) % 26
    descifrar("FCGURWQOVDG", "DOS") = "COORDENADAS"
    """
    longitudMensaje = len(mensaje)
    mensajeDescifrado = ""
    arregloClave = generarClave(clave, longitudMensaje)
    for i in range(0, longitudMensaje):
        numeroDescifrado = (ord(mensaje[i]) - ord(arregloClave[i]) + 26) % 26
        mensajeDescifrado += chr(numeroDescifrado + 65)
    return mensajeDescifrado


def sumarALetra(letra, n):
    """
    Regresa la letra que resulta de sumar n a la letra de entrada
    sumarALetra("A", 4) = 'E'. Debe ser una letra mayuscula de
    antemano.
    """
    posicionEnAlfabeto = ord(letra) - 65
    nuevaLetra = (posicionEnAlfabeto + n) % 26
    return chr(nuevaLetra + 65)


def obtenerNGramas(texto, n):
    """
    Regresa una lista ordenada de tuplas [(nGrama, repeticiones)] que representa,
    de mayor a menor, todos los nGramas encontrados en el texto y su número de repeticiones
    obtenerNGramas("ABCDEFABC", 3) = [("ABC", 2), ("DEF", 1)]
    """
    regex = f".\x7b{n}\x7d"
    coincidencias = re.findall(regex, texto)
    nGramas = dict({})
    for coincidencia in coincidencias:
        if coincidencia in nGramas:
            nGramas[coincidencia] = nGramas[coincidencia] + 1
        else:
            nGramas[coincidencia] = 1
    return sorted(nGramas.items(), key=lambda x: x[1], reverse=True)


def obtenerPosicionesNGrama(nGrama, texto):
    """
    Regresa todos los índices donde termina cierto nGrama en un texto dado.
    obtenerPosicionesNGrama("ABC", "XABCYABC") = [4, 8]
    """
    coincidencias = re.finditer(nGrama, texto)
    posiciones = []
    for coincidencia in coincidencias:
        posiciones.append(coincidencia.end(0))
    return posiciones


def estimarLongitudClave(textoCifrado):
    """
    Estima la longitud de la clave dado un texto. Para ello, obtiene los X nGramas más
    comunes y calcula el MCD de sus separaciones.
    Comienza intentando obtener los 5 tetragramas más comunes que se repitan más de dos
    veces; si hay menos de cinco, obtendrá X - 5 trigramas, siendo X el número de
    tetragramas obtenidos.
    En caso de que el MCD de los 5 nGramas más comunes sea 1, la función repetirá el
    procedimiento anterior obteniendo los 4, 3, 2 y/o 1 nGramas más comunes, hasta que
    el MCD sea distinto de 1 o se llegue a 1 nGrama.
    Si "XYZXYZ" aparece en posiciones 0 y 6, y "ABCABC" en posiciones 0 y 6 también,
    las diferencias son [6, 6] y el MCD es 6, por lo que la clave tiene longitud 6.
    estimarLongitudClave("FCGURWQOVDGFCGURWQOVDG") = 11
    """

    def estimarLongitudClave(textoCifrado, maxMuestras):
        tetragramas = obtenerNGramas(textoCifrado, 4)
        trigramas = obtenerNGramas(textoCifrado, 3)
        posiciones = []
        i = 0
        j = 0
        while len(posiciones) < maxMuestras:
            if tetragramas[i][1] >= 2:
                posiciones.append(
                    obtenerPosicionesNGrama(tetragramas[i][0], textoCifrado)
                )
                i += 1
            elif trigramas[j][1] >= 2:
                posiciones.append(
                    obtenerPosicionesNGrama(trigramas[j][0], textoCifrado)
                )
                j += 1
            else:
                break
        diferencias = []
        for pos in posiciones:
            diferencias += [y - x for x, y in zip(pos, pos[1:])]
        return reduce(gcd, diferencias)

    longitudClave = 1
    maxMuestras = 6
    while longitudClave == 1 and maxMuestras > 1:
        maxMuestras -= 1
        longitudClave = estimarLongitudClave(textoCifrado, maxMuestras)
    return longitudClave


def obtenerSubcriptogramas(longitudClave, texto):
    """
    Divide una cadena en subcadenas tomando cada longitudClave-ésimo caracter.
    Cada subcadena fue cifrada con la misma letra de la clave.
    obtenerSubcriptogramas(3, "ABCDEFGHI") = ["ADG", "BEH", "CFI"]
    """
    longitudTexto = len(texto)
    return [texto[i:longitudTexto:longitudClave] for i in range(0, longitudClave)]


def obtenerFrecuenciaLetras(letras, texto):
    """
    Regresa las frecuencias relativas de las letras indicadas dentro del texto.
    obtenerFrecuenciaLetras(["A", "B", "C"], "AAABBC") = [0.5, 0.333, 0.166]
    """
    longitudCriptograma = len(texto)
    diccionarioLetras = dict(
        obtenerNGramas(texto, 1)
    )  # Diccionario [letra:repeticiones]
    frecuencias = []
    for letra in letras:
        if letra not in diccionarioLetras:
            frecuencias.append(0)
        else:
            frecuencias.append(diccionarioLetras[letra] / longitudCriptograma)
    return frecuencias


def obtenerClave(longitudClave, textoCifrado):
    """
    Obtiene la clave basándose en la longitud de la clave, dividiendo el texto en
    longitud-de-clave subcadenas y aplicando a cada una el procedimiento AEOS.
    Por cada subcriptograma, se asume que la letra más frecuente corresponde a una
    de las letras A, E, O o S del español, y se elige la hipótesis cuya distribución
    AEOS resultante sea más cercana a la del español.
    obtenerClave(3, "FCGURWQOVDG") = ["F", "C", "G"]
    """
    criptogramas = obtenerSubcriptogramas(longitudClave, textoCifrado)
    print(longitudClave)
    posibleClave = []
    for criptograma in criptogramas:
        # Regla AEOS
        letras = obtenerNGramas(
            criptograma, 1
        )  # Lista ordenada de letras y sus repeticiones
        distancias = []
        for i in range(0, 6):  # Se asume que AEOS estará entre las 6 letras más comunes
            posibleA = letras[i][0]
            posibleE = sumarALetra(posibleA, 4)
            posibleO = sumarALetra(posibleE, 10)
            posibleS = sumarALetra(posibleO, 4)
            posibleAEOS = [posibleA, posibleE, posibleO, posibleS]
            frecuencias = obtenerFrecuenciaLetras(posibleAEOS, criptograma)
            distancias.append((posibleA, distanciaAFrecuenciasNormales(frecuencias)))
        distanciasOrdenadas = sorted(distancias, key=lambda x: x[1])
        posibleClave.append(distanciasOrdenadas[0][0])
    return posibleClave


def imprimirResultados(longitudClave, clave, mensaje):
    print(f"Longitud de la clave: {longitudClave}")
    print(f"Clave más probable: {clave}")
    print("--------")
    print("MENSAJE")
    print("--------")
    print(mensaje)


def main():
    if len(sys.argv) != 2:
        return print("""
	Uso:
	vigenere.py <archivoDeTexto>
	""")
    else:
        textoCifrado = leerArchivo(sys.argv[1]).upper()
        longitudClave = estimarLongitudClave(textoCifrado)
        letrasClave = obtenerClave(longitudClave, textoCifrado)
        if letrasClave == []:
            print("No fue posible descifrar el mensaje")
            exit(1)
        clave = reduce(lambda x, y: x + y, letrasClave)  # ["C", "A", "T"] -> "CAT"
        mensaje = descifrar(textoCifrado, clave)
    imprimirResultados(longitudClave, clave, mensaje)


main()

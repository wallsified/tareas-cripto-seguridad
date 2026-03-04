import sys
import argparse
from math import gcd
from functools import reduce
from collections import Counter
from colorama import Fore, init

# Inicializar colorama
init(autoreset=True)

# ─── Constantes ──────────────────────────────────────────────────────────────

ALFABETO = "abcdefghijklmnopqrstuvwxyz"
TAM_ALFABETO = len(ALFABETO)

# Frecuencias relativas de letras en español (fuente: corpus RAE, orden a-z)
FRECUENCIAS_ES = {
    "a": 12.53,
    "b": 1.42,
    "c": 4.68,
    "d": 5.86,
    "e": 13.68,
    "f": 0.69,
    "g": 1.01,
    "h": 0.70,
    "i": 6.25,
    "j": 0.44,
    "k": 0.02,
    "l": 4.97,
    "m": 3.15,
    "n": 6.71,
    "o": 8.68,
    "p": 2.51,
    "q": 0.88,
    "r": 6.87,
    "s": 7.98,
    "t": 4.63,
    "u": 3.93,
    "v": 0.90,
    "w": 0.01,
    "x": 0.22,
    "y": 0.90,
    "z": 0.52,
}

# Frecuencias relativas de letras en inglés (fuente: Lewand, 2000)
FRECUENCIAS_EN = {
    "a": 8.17,
    "b": 1.49,
    "c": 2.78,
    "d": 4.25,
    "e": 12.70,
    "f": 2.23,
    "g": 2.02,
    "h": 6.09,
    "i": 6.97,
    "j": 0.15,
    "k": 0.77,
    "l": 4.03,
    "m": 2.41,
    "n": 6.75,
    "o": 7.51,
    "p": 1.93,
    "q": 0.10,
    "r": 5.99,
    "s": 6.33,
    "t": 9.06,
    "u": 2.76,
    "v": 0.98,
    "w": 2.36,
    "x": 0.15,
    "y": 1.97,
    "z": 0.07,
}

IDIOMAS = {
    "es": FRECUENCIAS_ES,
    "en": FRECUENCIAS_EN,
}


def limpiar_texto(texto: str) -> str:
    """Convierte el texto a minúsculas y elimina caracteres fuera del alfabeto latino básico."""
    return "".join(c for c in texto.lower() if c in ALFABETO)


def buscar_repeticiones(texto: str, tam_min: int = 3) -> dict[str, list[int]]:
    """
    Busca todas las subcadenas de longitud >= `tam_min` que aparecen más de una vez
    en `texto` y devuelve un diccionario {secuencia: [posición1, posición2, ...]}.
    """
    repeticiones: dict[str, list[int]] = {}

    for longitud in range(tam_min, len(texto) // 2 + 1):
        for inicio in range(len(texto) - longitud + 1):
            seq = texto[inicio : inicio + longitud]
            # Solo registrar la primera vez que se detecta la secuencia como repetida
            if seq in repeticiones:
                if inicio not in repeticiones[seq]:
                    repeticiones[seq].append(inicio)
            else:
                # Buscar si aparece en otra posición posterior
                if texto.find(seq, inicio + 1) != -1:
                    repeticiones[seq] = [inicio]

    # Completar todas las posiciones para cada secuencia ya marcada como repetida
    for seq in list(repeticiones.keys()):
        posiciones = []
        inicio = 0
        while True:
            pos = texto.find(seq, inicio)
            if pos == -1:
                break
            posiciones.append(pos)
            inicio = pos + 1
        repeticiones[seq] = posiciones

    return repeticiones


def calcular_distancias(repeticiones: dict[str, list[int]]) -> list[int]:
    """
    A partir del diccionario de repeticiones, devuelve la lista de todas las
    distancias entre pares consecutivos de posiciones de cada secuencia.
    """
    distancias: list[int] = []
    for posiciones in repeticiones.values():
        for i in range(1, len(posiciones)):
            distancias.append(posiciones[i] - posiciones[i - 1])
    return distancias


def mcd_lista(numeros: list[int]) -> int:
    """Calcula el MCD de una lista de enteros."""
    return reduce(gcd, numeros)


def factores(n: int) -> list[int]:
    """Devuelve todos los divisores de `n` mayores que 1."""
    divs = []
    for i in range(2, n + 1):
        if n % i == 0:
            divs.append(i)
    return divs


def estimar_longitud_clave(
    distancias: list[int], max_longitud: int = 20
) -> list[tuple[int, int]]:
    """
    Cuenta la frecuencia de cada factor común entre todas las distancias.
    Devuelve una lista de (longitud_candidata, frecuencia) ordenada de mayor a menor frecuencia,
    filtrada a candidatos <= `max_longitud`.
    """
    conteo: Counter = Counter()
    for d in distancias:
        for f in factores(d):
            if 2 <= f <= max_longitud:
                conteo[f] += 1

    return conteo.most_common()


def indice_coincidencia(texto: str) -> float:
    """
    Calcula el índice de coincidencia de un texto.
    IC ≈ 0.065 para español, ≈ 0.065 para inglés, ≈ 0.038 para texto aleatorio.
    """
    n = len(texto)
    if n < 2:
        return 0.0
    frec = Counter(texto)
    suma = sum(f * (f - 1) for f in frec.values())
    return suma / (n * (n - 1))


def mejor_desplazamiento(
    grupo: str, frecuencias_ref: dict[str, float]
) -> tuple[int, float]:
    """
    Para un grupo de caracteres (columna del texto cifrado), prueba los 26 desplazamientos
    posibles y devuelve el que mejor correlaciona con las frecuencias de referencia del idioma.

    Devuelve (desplazamiento, puntuación_máxima).
    """
    mejor_desp = 0
    mejor_puntuacion = -1.0
    n = len(grupo)

    if n == 0:
        return 0, 0.0

    for desp in range(TAM_ALFABETO):
        puntuacion = 0.0
        for i, letra in enumerate(ALFABETO):
            # Letra cifrada que correspondería a `letra` con este desplazamiento
            letra_cifrada = ALFABETO[(i + desp) % TAM_ALFABETO]
            conteo = grupo.count(letra_cifrada)
            puntuacion += (conteo / n) * frecuencias_ref.get(letra, 0)

        if puntuacion > mejor_puntuacion:
            mejor_puntuacion = puntuacion
            mejor_desp = desp

    return mejor_desp, mejor_puntuacion


def recuperar_clave(
    texto: str, longitud_clave: int, frecuencias_ref: dict[str, float]
) -> str:
    """
    Divide el texto cifrado en `longitud_clave` grupos y determina el mejor
    desplazamiento para cada grupo mediante análisis de frecuencias.

    Devuelve la clave como cadena de texto.
    """
    clave = ""
    for i in range(longitud_clave):
        grupo = texto[i::longitud_clave]
        desp, _ = mejor_desplazamiento(grupo, frecuencias_ref)
        clave += ALFABETO[desp]
    return clave


# ─── Paso 6: Descifrado Vigenère ─────────────────────────────────────────────


def descifrar_vigenere(texto_cifrado: str, clave: str) -> str:
    """
    Descifra un texto cifrado con Vigenère dado el texto cifrado (solo letras minúsculas)
    y la clave en texto plano.
    """
    texto_descifrado = []
    clave = clave.lower()
    tam_clave = len(clave)
    j = 0  # índice dentro de la clave

    for c in texto_cifrado:
        if c in ALFABETO:
            desp = ALFABETO.index(clave[j % tam_clave])
            letra = ALFABETO[(ALFABETO.index(c) - desp) % TAM_ALFABETO]
            texto_descifrado.append(letra)
            j += 1
        else:
            texto_descifrado.append(c)

    return "".join(texto_descifrado)


def encabezado(msg: str) -> None:
    """Imprime un encabezado de sección."""
    print(f"\n{Fore.CYAN}{'─' * 60}")
    print(f"{Fore.CYAN} {msg}")
    print(f"{Fore.CYAN}{'─' * 60}")


def info(msg: str) -> None:
    """Imprime un mensaje informativo."""
    print(f"{Fore.WHITE}{msg}")


def resaltar(etiqueta: str, valor: str) -> None:
    """Imprime una etiqueta con su valor resaltado."""
    print(f"{Fore.YELLOW}{etiqueta}: {Fore.GREEN}{valor}")


def advertencia(msg: str) -> None:
    """Imprime una advertencia."""
    print(f"{Fore.YELLOW}[!] {msg}")


def error(msg: str) -> None:
    """Imprime un error y termina el programa."""
    print(f"{Fore.RED}[-] {msg}")
    sys.exit(1)


def analizar(
    texto_original: str,
    idioma: str,
    tam_seq: int,
    max_long_clave: int,
    longitud_forzada: int | None,
    verbose: bool,
) -> None:
    """
    Ejecuta el análisis de Kasiski completo sobre el texto proporcionado.

    Parámetros
    ----------
    texto_original   : Texto cifrado tal como fue introducido.
    idioma           : 'es' o 'en', determina la tabla de frecuencias de referencia.
    tam_seq          : Longitud mínima de las secuencias buscadas.
    max_long_clave   : Límite superior para los candidatos de longitud de clave.
    longitud_forzada : Si se proporciona, omite la estimación y usa este valor directamente.
    verbose          : Muestra detalles adicionales del análisis.
    """
    frecuencias_ref = IDIOMAS[idioma]
    texto = limpiar_texto(texto_original)

    if len(texto) < 20:
        error(
            "El texto cifrado es demasiado corto para el análisis de Kasiski (mínimo 20 letras)."
        )

    # ── 1. Secuencias repetidas ──
    encabezado("Paso 1 · Búsqueda de secuencias repetidas")
    repeticiones = buscar_repeticiones(texto, tam_seq)

    if not repeticiones:
        advertencia(f"No se encontraron secuencias repetidas de longitud >= {tam_seq}.")
        advertencia("Intenta reducir el parámetro --tam-seq o usa un texto más largo.")
    else:
        info(f"Secuencias únicas encontradas: {Fore.GREEN}{len(repeticiones)}")
        if verbose:
            # Mostrar las 10 secuencias más largas
            top = sorted(repeticiones.items(), key=lambda x: len(x[0]), reverse=True)[
                :10
            ]
            for seq, pos in top:
                info(f"  '{Fore.GREEN}{seq}{Fore.WHITE}' → posiciones {pos}")

    # ── 2. Distancias ──
    encabezado("Paso 2 · Distancias entre repeticiones")
    distancias = calcular_distancias(repeticiones)

    if not distancias:
        error("No se pudieron calcular distancias. El texto puede ser demasiado corto.")

    info(f"Distancias calculadas: {Fore.GREEN}{len(distancias)}")
    if verbose and distancias:
        info(f"  Muestra: {distancias[:15]}{'...' if len(distancias) > 15 else ''}")

    # ── 3. Longitud de la clave ──
    encabezado("Paso 3 · Estimación de la longitud de la clave")

    if longitud_forzada:
        longitud_clave = longitud_forzada
        advertencia(f"Longitud de clave forzada por el usuario: {longitud_clave}")
    else:
        candidatos = estimar_longitud_clave(distancias, max_long_clave)

        if not candidatos:
            error("No se encontraron factores comunes. Prueba con un texto más largo.")

        info("Longitudes de clave candidatas (por frecuencia de factores comunes):\n")
        for longitud, frec in candidatos[:8]:
            barra = "█" * frec
            print(
                f"  {Fore.YELLOW}Longitud {longitud:>2}{Fore.WHITE}: {Fore.GREEN}{barra}{Fore.WHITE} ({frec})"
            )

        longitud_clave = candidatos[0][0]
        print()
        resaltar("Longitud de clave estimada", str(longitud_clave))

        # Verificar con índice de coincidencia
        ic_promedio = (
            sum(
                indice_coincidencia(texto[i::longitud_clave])
                for i in range(longitud_clave)
            )
            / longitud_clave
        )

        info(
            f"Índice de coincidencia promedio para longitud {longitud_clave}: "
            f"{Fore.GREEN}{ic_promedio:.4f}"
        )
        info("  (Referencia: ~0.065 texto natural, ~0.038 texto aleatorio)")

    encabezado("Paso 4 & 5 · Análisis de frecuencias y recuperación de la clave")
    clave = recuperar_clave(texto, longitud_clave, frecuencias_ref)

    if verbose:
        info("Desplazamiento encontrado por columna:")
        for i, letra in enumerate(clave):
            grupo = texto[i::longitud_clave]
            desp = ALFABETO.index(letra)
            ic = indice_coincidencia(grupo)
            info(
                f"  Columna {i + 1:>2}: '{Fore.GREEN}{letra}{Fore.WHITE}' "
                f"(desp={desp:>2}, IC={ic:.4f}, n={len(grupo)})"
            )

    print()
    resaltar("Clave recuperada", clave.upper())
    encabezado("Paso 6 · Descifrado con la clave encontrada")
    texto_descifrado = descifrar_vigenere(texto, clave)

    print()
    resaltar("Texto cifrado   ", texto[:80] + ("..." if len(texto) > 80 else ""))
    resaltar("Clave           ", clave.upper())
    resaltar(
        "Texto descifrado",
        texto_descifrado[:80] + ("..." if len(texto_descifrado) > 80 else ""),
    )

    if verbose and len(texto_descifrado) > 80:
        encabezado("Texto descifrado completo")
        print(f"{Fore.WHITE}{texto_descifrado}")

    print()


def construir_parser() -> argparse.ArgumentParser:
    """Construye y devuelve el analizador de argumentos."""
    parser = argparse.ArgumentParser(
        prog="kasiski",
        description="Rompe el cifrado Vigenère mediante el método de Kasiski.",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    grupo = parser.add_mutually_exclusive_group(required=True)
    grupo.add_argument(
        "-t",
        "--texto",
        metavar="TEXTO",
        help="Texto cifrado a analizar (entre comillas).",
    )
    grupo.add_argument(
        "-a",
        "--archivo",
        metavar="ARCHIVO",
        help="Ruta al archivo de texto que contiene el texto cifrado.",
    )

    parser.add_argument(
        "-i",
        "--idioma",
        choices=["es", "en"],
        default="es",
        help="Idioma del texto original para el análisis de frecuencias.\n"
        "  es → español (predeterminado)\n"
        "  en → inglés",
    )
    parser.add_argument(
        "-s",
        "--tam-seq",
        type=int,
        default=3,
        metavar="N",
        help="Longitud mínima de las secuencias repetidas buscadas (predeterminado: 3).",
    )
    parser.add_argument(
        "-m",
        "--max-longitud",
        type=int,
        default=20,
        metavar="N",
        help="Longitud máxima de clave a considerar (predeterminado: 20).",
    )
    parser.add_argument(
        "-l",
        "--longitud-clave",
        type=int,
        default=None,
        metavar="N",
        help="Fuerza una longitud de clave concreta, omitiendo la estimación automática.",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Muestra detalles adicionales del análisis.",
    )

    return parser


def main() -> None:
    parser = construir_parser()
    args = parser.parse_args()

    if args.texto:
        texto_cifrado = args.texto
    else:
        try:
            with open(args.archivo, "r", encoding="utf-8") as f:
                texto_cifrado = f.read()
        except FileNotFoundError:
            error(f"No se encontró el archivo '{args.archivo}'.")
        except OSError as e:
            error(f"No se pudo leer el archivo: {e}")

    # Validar parámetros
    if args.tam_seq < 2:
        error("La longitud mínima de secuencia debe ser al menos 2.")
    if args.max_longitud < 2:
        error("La longitud máxima de clave debe ser al menos 2.")
    if args.longitud_clave is not None and args.longitud_clave < 1:
        error("La longitud de clave forzada debe ser un entero positivo.")

    print(f"{Fore.CYAN}Método de Kasiski · Ruptura del cifrado Vigenère")
    print(
        f"{Fore.WHITE}Idioma: {Fore.GREEN}{args.idioma.upper()}{Fore.WHITE}  "
        f"| Tam. secuencia mínimo: {Fore.GREEN}{args.tam_seq}{Fore.WHITE}  "
        f"| Longitud máx. de clave: {Fore.GREEN}{args.max_longitud}"
    )

    analizar(
        texto_original=texto_cifrado,
        idioma=args.idioma,
        tam_seq=args.tam_seq,
        max_long_clave=args.max_longitud,
        longitud_forzada=args.longitud_clave,
        verbose=args.verbose,
    )


if __name__ == "__main__":
    main()

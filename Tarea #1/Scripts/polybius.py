import argparse

from colorama import Fore, Style, init

init(autoreset=True)

ALFABETO = "ABCDEFGHIJKLMNOPQRSTUVWXY"

NORMALIZACION: dict[str, str] = {
    "á": "a",
    "Á": "A",
    "é": "e",
    "É": "E",
    "í": "i",
    "Í": "I",
    "ó": "o",
    "Ó": "O",
    "ú": "u",
    "Ú": "U",
    "ü": "u",
    "Ü": "U",
    "ñ": "n",
    "Ñ": "N",
}


def construir_cuadrado() -> tuple[dict[str, str], dict[str, str]]:
    """
    Construye los mapas de codificación y decodificación del cuadrado de Polibio.
    mapa_cifrado   : letra  → código de 2 dígitos  ej. 'A' → '11'
    mapa_descifrado: código → letra                ej. '11' → 'A'
    """
    mapa_cifrado: dict[str, str] = {}
    mapa_descifrado: dict[str, str] = {}
    for i, letra in enumerate(ALFABETO):
        # i // 5 da la fila: cada grupo de 5 letras ocupa una fila.
        # i % 5 da la columna: posición cíclica dentro de la fila.
        fila = i // 5 + 1
        columna = i % 5 + 1
        codigo = f"{fila}{columna}"
        mapa_cifrado[letra] = codigo
        mapa_descifrado[codigo] = letra
    return mapa_cifrado, mapa_descifrado


def normalizar(caracter: str) -> str:
    return NORMALIZACION.get(caracter, caracter).upper()


def cifrar(texto: str, mapa_cifrado: dict[str, str]) -> str:
    """
    Cifra un texto con el cuadrado de Polibio.
    Retorna la cadena cifrada y la lista de caracteres omitidos (ej. Z).
    """
    codigos: list[str] = []

    for caracter in texto:
        normalizado = normalizar(caracter)
        if normalizado in mapa_cifrado:
            codigos.append(mapa_cifrado[normalizado])
    return " ".join(codigos)


def descifrar(texto: str, mapa_descifrado: dict[str, str]) -> str:
    """
    Descifra una cadena de códigos separados por espacios.
    Retorna el texto plano y la lista de códigos inválidos.
    """
    fichas = texto.split()
    letras: list[str] = []

    for ficha in fichas:
        if ficha in mapa_descifrado:
            letras.append(mapa_descifrado[ficha])

    return "".join(letras)


def construir_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="polybius",
        epilog=(
            "Ejemplos:\n"
            '  Cifrar:    python (uv run) polybius.py -c -m "Hola mundo"\n'
            '  Descifrar: python (uv run) polybius.py -d -m "23 35 32 11"'
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    modo = parser.add_mutually_exclusive_group(required=True)
    modo.add_argument("-c", "--cifrar", action="store_true", help="Cifrar un texto")
    modo.add_argument(
        "-d", "--descifrar", action="store_true", help="Descifrar códigos numéricos"
    )

    parser.add_argument(
        "-m",
        "--mensaje",
        required=True,
        metavar="TEXTO",
        help="Texto a cifrar o serie de códigos a descifrar",
    )
    return parser


def main() -> None:
    parser = construir_parser()
    args = parser.parse_args()

    mapa_cifrado, mapa_descifrado = construir_cuadrado()

    if args.cifrar:
        resultado = cifrar(args.mensaje, mapa_cifrado)
        print(f"{Fore.WHITE}Texto:   {args.mensaje}")
        print(f"{Fore.GREEN}{Style.BRIGHT}Cifrado: {resultado}")

    elif args.descifrar:
        resultado = descifrar(args.mensaje, mapa_descifrado)
        print(f"{Fore.WHITE}Códigos:    {args.mensaje}")
        print(f"{Fore.CYAN}{Style.BRIGHT}Descifrado: {resultado}")


if __name__ == "__main__":
    main()

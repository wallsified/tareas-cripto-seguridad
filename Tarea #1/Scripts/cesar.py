from colorama import Fore, init

init()

ALFABETO_MIN = "abcdefghijklmnñopqrstuvwxyz"
ALFABETO_MAY = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
TAM_ALFABETO = len(ALFABETO_MIN)


def cifrado_cesar(texto, clave, descifrar=False):
    """Cifra o descifra un texto usando el cifrado César con el alfabeto español."""
    resultado = ""
    desplazamiento = -clave if descifrar else clave

    for char in texto:
        if char in ALFABETO_MIN:
            idx = (ALFABETO_MIN.index(char) + desplazamiento) % TAM_ALFABETO
            resultado += ALFABETO_MIN[idx]
        elif char in ALFABETO_MAY:
            idx = (ALFABETO_MAY.index(char) + desplazamiento) % TAM_ALFABETO
            resultado += ALFABETO_MAY[idx]
        else:
            # Conservar caracteres que no son del alfabeto: números, puntuación, etc.
            resultado += char

    return resultado


def romper_cifrado_cesar(texto_cifrado):
    """Prueba todas las claves posibles (0-27) por fuerza bruta e imprime los resultados."""
    print(
        f"{Fore.YELLOW}\n[*] Iniciando ataque por fuerza bruta ({TAM_ALFABETO} desplazamientos posibles)...\n"
    )
    for clave in range(TAM_ALFABETO):
        texto_descifrado = cifrado_cesar(texto_cifrado, clave, descifrar=True)
        print(
            f"{Fore.CYAN}[Desplazamiento {clave:>2}/26]{Fore.RESET} → {texto_descifrado}"
        )
    print(f"{Fore.YELLOW}\n[*] Búsqueda completada.\n")


# Bucle principal
while True:
    texto = input(f"{Fore.GREEN}[?] Ingresa el texto/mensaje a descifrar: ")
    if not texto:
        print(f"{Fore.RED}[-] Por favor ingresa un texto.")
    else:
        romper_cifrado_cesar(texto)

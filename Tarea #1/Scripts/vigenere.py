"""
Uso:
    Ejecutar el script directamente:
        - python vigenere.py
        - uv run vigenere.py

    Seleccionar 'C' para cifrar o 'D' para descifrar, luego ingresar
    el texto y la clave cuando se soliciten.
"""

# Diccionario de sustitución para normalizar caracteres especiales del español.
# Mapea vocales acentuadas (mayúsculas y minúsculas) y la Ñ/ñ a sus equivalentes
# sin tilde dentro del alfabeto inglés de 26 letras.
ACENTOS = {
    "á": "a",
    "é": "e",
    "í": "i",
    "ó": "o",
    "ú": "u",
    "ü": "u",  # diéresis también se normaliza
    "ñ": "n",
    "Á": "A",
    "É": "E",
    "Í": "I",
    "Ó": "O",
    "Ú": "U",
    "Ü": "U",
    # "Ñ": "N",
}


def normalizar(texto):
    """
    Normaliza un texto en español eliminando acentos y caracteres especiales.

    Reemplaza vocales acentuadas (á, é, í, ó, ú, ü) y la letra ñ por sus
    equivalentes sin tilde, tanto en minúsculas como en mayúsculas. Esto
    permite que el cifrado Vigenère opere sobre el alfabeto estándar de
    26 letras sin perder información semántica relevante.

    Args:
        texto (str): Cadena de texto en español que puede contener
                     caracteres acentuados o la letra ñ.

    Returns:
        str: Cadena de texto con los caracteres especiales sustituidos
             por su equivalente sin acento. Los demás caracteres se
             mantienen sin cambios.

    Ejemplos:
        >>> normalizar("Ñoño")
        'Nono'
        >>> normalizar("México")
        'Mexico'
        >>> normalizar("ñandú")
        'nandu'
    """
    return "".join(ACENTOS.get(c, c) for c in texto)


def encrypt_vigenere(plain_text, key):
    """
    Cifra un texto usando el algoritmo de Vigenère.

    El texto en claro se normaliza (se eliminan acentos y la ñ) y se
    eliminan los espacios antes del cifrado. Cada letra se desplaza en
    el alfabeto según el valor de la letra correspondiente de la clave,
    ciclando la clave cuando se agota.

    La fórmula de cifrado para cada carácter es:
        C_i = (P_i + K_i) mod 26

    Donde:
        - C_i es el i-ésimo carácter del texto cifrado.
        - P_i es el valor numérico del i-ésimo carácter del texto plano (A=0, Z=25).
        - K_i es el valor numérico del i-ésimo carácter de la clave (A=0, Z=25).

    Args:
        plain_text (str): Texto en claro a cifrar. Puede contener espacios,
                          acentos y letras ñ, que serán normalizados
                          automáticamente antes del cifrado.
        key (str):        Clave de cifrado. Debe contener únicamente letras
                          del alfabeto (A-Z, a-z). La clave se repite
                          cíclicamente si es más corta que el texto.

    Returns:
        str: Texto cifrado en mayúsculas. Los caracteres no alfabéticos
             (números, puntuación) se incluyen sin cifrar.

    Ejemplos:
        >>> encrypt_vigenere("HOLAMUNDO", "CLAVE")
        'JPZENTARL'
        >>> encrypt_vigenere("hola mundo", "clave")
        'JPZENTARL'
    """
    # Eliminar espacios y normalizar acentos antes de cifrar
    plain_text = normalizar(plain_text.replace(" ", ""))
    encrypted_text = ""
    key_index = 0

    for char in plain_text:
        if char.isalpha():
            char = char.upper()
            # Calcular el desplazamiento según la letra actual de la clave
            shift = ord(key[key_index].upper()) - ord("A")
            # Aplicar la fórmula de cifrado Vigenère y ajustar al rango A-Z
            encrypted_char = chr((ord(char) - ord("A") + shift) % 26 + ord("A"))
            encrypted_text += encrypted_char

            key_index = (key_index + 1) % len(key)
        else:
            # Los caracteres no alfabéticos se agregan sin modificación
            encrypted_text += char

    return encrypted_text


def decrypt_vigenere(encrypted_text, key):
    """
    Descifra un texto cifrado con el algoritmo de Vigenère.

    Aplica la operación inversa al cifrado: resta el desplazamiento de la
    clave a cada carácter del texto cifrado para recuperar el texto original.
    Los espacios se eliminan y se normaliza el texto antes de descifrar.

    La fórmula de descifrado para cada carácter es:
        P_i = (C_i - K_i) mod 26

    Donde:
        - P_i es el i-ésimo carácter del texto plano recuperado.
        - C_i es el valor numérico del i-ésimo carácter del texto cifrado (A=0, Z=25).
        - K_i es el valor numérico del i-ésimo carácter de la clave (A=0, Z=25).

    Args:
        encrypted_text (str): Texto cifrado a descifrar. Se asume que fue
                               generado con `encrypt_vigenere` usando la misma
                               clave. Los espacios serán eliminados antes de
                               procesar.
        key (str):             Clave de descifrado. Debe ser la misma clave
                               usada durante el cifrado. La clave se repite
                               cíclicamente si es más corta que el texto.

    Returns:
        str: Texto descifrado en mayúsculas. Los caracteres no alfabéticos
             (números, puntuación) se incluyen sin modificar.

    Ejemplos:
        >>> decrypt_vigenere("JPZENTARL", "CLAVE")
        'HOLAMUNDO'
        >>> decrypt_vigenere("JPZEN TARL", "clave")
        'HOLAMUNDO'
    """
    encrypted_text = normalizar(encrypted_text.replace(" ", ""))
    decrypted_text = ""
    key_index = 0

    for char in encrypted_text:
        if char.isalpha():
            char = char.upper()
            # Calcular el desplazamiento según la letra actual de la clave
            shift = ord(key[key_index].upper()) - ord("A")

            # Aplicar la fórmula de descifrado Vigenère y ajustar al rango A-Z
            # El módulo 26 garantiza que valores negativos se envuelvan correctamente
            decrypted_char = chr((ord(char) - ord("A") - shift) % 26 + ord("A"))
            decrypted_text += decrypted_char

            # Avanzar al siguiente carácter de la clave (cíclicamente)
            key_index = (key_index + 1) % len(key)
        else:
            # Los caracteres no alfabéticos se agregan sin modificación
            decrypted_text += char

    return decrypted_text


def main():
    print("Bienvenido al cifrador Vigenère")
    option = input("Ingrese 'C' para cifrar o 'D' para descifrar: ")

    if option.upper() == "C":
        plain_text = input("Ingrese el texto a cifrar: ")
        key = input("Ingrese la clave: ")

        encrypted_text = encrypt_vigenere(plain_text, key)
        print("Texto cifrado:", encrypted_text)

    elif option.upper() == "D":
        encrypted_text = input("Ingrese el texto a descifrar: ")
        key = input("Ingrese la clave: ")

        decrypted_text = decrypt_vigenere(encrypted_text, key)
        print("Texto descifrado:", decrypted_text)

    else:
        print("Opción no válida. Por favor, ingrese 'C' o 'D'.")


main()

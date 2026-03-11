# Cifrado César

```bash
uv run cesar.py
# o sin uv, usando python directamente
python cesar.py
```

Dentro de la ejecución, se te pedirá que ingreses el mensaje a descifrar. Por ejemplo:

```python
[?] Ingresa el texto/mensaje a descifrar: Nc xkfc gu dgnnc

[*] Iniciando ataque por fuerza bruta (27 desplazamientos posibles)...

[Desplazamiento  0/26] → Nc xkfc gu dgnnc
[Desplazamiento  1/26] → Mb wjeb ft cfmmb
[Desplazamiento  2/26] → La vida es bella
[Desplazamiento  3/26] → Kz uhcz dr adkkz
[Desplazamiento  4/26] → Jy tgby cq zcjjy
[Desplazamiento  5/26] → Ix sfax bp ybiix
[Desplazamiento  6/26] → Hw rezw ao xahhw
[Desplazamiento  7/26] → Gv qdyv zñ wzggv
[Desplazamiento  8/26] → Fu pcxu yn vyffu
[Desplazamiento  9/26] → Et obwt xm uxeet
[Desplazamiento 10/26] → Ds ñavs wl twdds
[Desplazamiento 11/26] → Cr nzur vk svccr
[Desplazamiento 12/26] → Bq mytq uj rubbq
[Desplazamiento 13/26] → Ap lxsp ti qtaap
[Desplazamiento 14/26] → Zo kwro sh pszzo
[Desplazamiento 15/26] → Yñ jvqñ rg oryyñ
[Desplazamiento 16/26] → Xn iupn qf ñqxxn
[Desplazamiento 17/26] → Wm htom pe npwwm
[Desplazamiento 18/26] → Vl gsñl od movvl
[Desplazamiento 19/26] → Uk frnk ñc lñuuk
[Desplazamiento 20/26] → Tj eqmj nb knttj
[Desplazamiento 21/26] → Si dpli ma jmssi
[Desplazamiento 22/26] → Rh cokh lz ilrrh
[Desplazamiento 23/26] → Qg bñjg ky hkqqg
[Desplazamiento 24/26] → Pf anif jx gjppf
[Desplazamiento 25/26] → Oe zmhe iw fiooe
[Desplazamiento 26/26] → Ñd ylgd hv ehññd

[*] Búsqueda completada.
```

Se usa `Ctrl+D` para salir del programa.

# Cifrado Polybius

```bash
# Para descifrar.
uv run polybius.py -d -m "00 00 00 00 00 00 00 00 00 00"

# Para cifrar
uv run polybius.py -c -m "Mensaje"

# o sin uv, usando python directamente
python polybius.py -d -m "00 00 00 00 00"
python polybius.py -c -m "Mensaje"
```

Ejemplo de Uso:

```python
uv run polybius.py -d -m "15 32 45 24 15 33 41 35 34 35 15 44 41 15 43 11 11 34 11 14 24 15"

Códigos:    15 32 45 24 15 33 41 35 34 35 15 44 41 15 43 11 11 34 11 14 24 15
Descifrado: ELTIEMPONOESPERAANADIE

uv run polybius.py -c -m "Si la felicidad tuviera una forma, tendria forma de cristal, porque puede estar a tu alrededor sin que la notes. Pero si cambias de perspectiva, puede reflejar una luz capaz de iluminarlo todo."

Texto:   Si la felicidad tuviera una forma, tendria forma de cristal, porque puede estar a tu alrededor sin que la notes. Pero si cambias de perspectiva, puede reflejar una luz capaz de iluminarlo todo.
Cifrado: 44 24 32 11 21 15 32 24 13 24 14 11 14 45 51 52 24 15 43 11 51 34 11 21 35 43 33 11 45 15 34 14 43 24 11 21 35 43 33 11 14 15 13 43 24 44 45 11 32 41 35 43 42 51 15 41 51 15 14 15 15 44 45 11 43 11 45 51 11 32 43 15 14 15 14 35 43 44 24 34 42 51 15 32 11 34 35 45 15 44 41 15 43 35 44 24 13 11 33 12 24 11 44 14 15 41 15 43 44 41 15 13 45 24 52 11 41 51 15 14 15 43 15 21 32 15 25 11 43 51 34 11 32 51 13 11 41 11 14 15 24 32 51 33 24 34 11 43 32 35 45 35 14 35
```

# Método de Kasiski

```bash
uv run kasiski.py mensaje.txt
# o sin uv, usando python directamente
python kasiski.py mensaje.txt
```

Ejemplo de Uso:

```python
uv run kasiski.py mensaje.txt

Longitud de la clave: 15
Clave más probable: RVEHZNKOSHABKIB
--------
MENSAJE
--------
NHELDELEEOLFTVVDJBAGAWQAQUUJABXPMHUNXVXAWZAXAWFANPAEVNAOMSHGAEJLDBAQEESTVHENJQPPZXBYYADUVNUIXJSBARHENPRKWERBSAACCYLABUKCMAIHOURDWNEAWENLAELMMQAFWGSZVZZAVEEEJADTKCTONTOPYFWRNNGHAWDBAONETXLQDNDANGOEIRSBQRSAECOECTFXOCDEGIKHLEECTL
```

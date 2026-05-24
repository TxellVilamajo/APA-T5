# Sonido estéreo y ficheros WAVE

## Nom i cognoms

> [!Important]
> Introduzca a continuación su nombre y apellidos:
>
> Txell Vilamajó i Puixeu

## Aviso Importante

> [!Caution]
> 
> El objetivo de esta tarea es manejar la lectura y escritura de ficheros binarios. Para ello, sólo se
> permite el uso de las funciones de la biblioteca `struct`. Aunque existen distintas bibliotecas que
> permiten manejar los ficheros WAVE de una manera más eficiente y sencilla, su uso está prohibido.
>
> ¿Quiere saber más?, consulte con el profesorado.

## Fecha de entrega: 24 de mayo a medianoche

## El formato WAVE

El formato WAVE es uno de los más extendidos para el almacenamiento y transmisión
de señales de audio. En el fondo, se trata de un tipo particular de fichero
[RIFF](https://en.wikipedia.org/wiki/Resource_Interchange_File_Format) (*Resource
Interchange File Format*), utilizado no sólo para señales de audio sino también para señales de
otros tipos, como las imágenes estáticas o en movimiento, o secuencias MIDI (aunque, en el caso
del MIDI, con pequeñas diferencias que los hacen incompatibles).

La base de los ficheros RIFF es el uso de *cachos* (*chunks*, en inglés). Cada cacho,
o subcacho, está encabezado por una cadena de cuatro caracteres ASCII, que indica el tipo del cacho,
seguido por un entero sin signo de cuatro bytes, que indica el tamaño en bytes de lo que queda de
cacho sin contar la cadena inicial y el propio tamaño. A continuación, y en función del tipo de
cacho, se colocan los datos que lo forman.

Todo fichero RIFF incluye un primer cacho que lo identifica como tal y que empieza por la cadena
`'RIFF'`. A continuación, después del tamaño del cacho y en otra cadena de cuatro caracteres,
se indica el tipo concreto de información que contiene el fichero. En el caso concreto de los
ficheros de audio WAVE, esta cadena es igual a `'WAVE'`, y el cacho debe contener dos
*subcachos*: el primero, de nombre `'fmt '`, proporciona la información de cómo está
codificada la señal. Por ejemplo, si es PCM lineal, ADPCM, etc., o si es monofónica o estéreo. El
segundo subcacho, de nombre `'data'`, incluye las muestras de la señal.

Dispone de una descripción detallada del formato WAVE en la página
[WAVE PCM soundfile format](http://soundfile.sapp.org/doc/WaveFormat/) de Soundfile.

## Audio estéreo

La mayor parte de los animales, incluidos los del género *homo sapiens sapiens* sanos y completos,
están dotados de dos órganos que actúan como transductores acústico-sensoriales (es decir, tienen dos
*oídos*). Esta duplicidad orgánica permite al bicho, entre otras cosas, determinar la dirección de
origen del sonido. En el caso de la señal de música, además, la duplicidad proporciona una sensación
de *amplitud espacial*, de realismo y de confort acústico.

En un principio, los equipos de reproducción de audio no tenían en cuenta estos efectos y sólo permitían
almacenar y reproducir una única señal para los dos oídos. Es el llamado *sonido monofónico* o
*monoaural*. Una alternativa al sonido monofónico es el *estereofónico* o, simplemente, *estéreo*. En
él, se usan dos señales independientes, destinadas a ser reproducidas a ambos lados del oyente: los
llamados *canal izquierdo* (**L**) y *derecho* (**R**).

Aunque los primeros experimentos con sonido estereofónico datan de finales del siglo XIX, los primeros
equipos y grabaciones de este tipo no se popularizaron hasta los años 1950 y 1960. En aquel tiempo, la
gestión de los dos canales era muy rudimentaria. Por ejemplo, los instrumentos se repartían entre los
dos canales, con unos sonando exclusivamente a la izquierda y el resto a la derecha. Es el caso de las
primeras grabaciones en estéreo de los Beatles: las versiones en alemán de los singles *She loves you*
y *I want to hold your hand*. Así, en esta última (de la que dispone de un fichero en Atenea con sus
primeros treinta segundos, [Komm, gib mir deine Hand](wav/komm.wav)), la mayor parte de los instrumentos
suenan por el canal derecho, mientras que las voces y las características palmas lo hacen por el izquierdo.

Un problema habitual en los primeros años del sonido estereofónico, y aún vigente hoy en día, es que no
todos los equipos son capaces de reproducir los dos canales por separado. La solución comúnmente
adoptada consiste en no almacenar cada canal por separado, sino en la forma semisuma, $(L+R)/2$, y
semidiferencia, $(L-R)/2$, y de tal modo que los equipos monofónicos sólo accedan a la primera de ellas.
De este modo, estos equipos pueden reproducir una señal completa, formada por la suma de los dos
canales, y los estereofónicos pueden reconstruir los dos canales estéreo.

Por ejemplo, en la radio FM estéreo, la señal, de ancho de banda 15 kHz, se transmite del modo siguiente:

- En banda base, $0\le f\le 15$ kHz, se transmite la suma de los dos canales, $L+R$. Esta es la señal
  que son capaces de reproducir los equipos monofónicos.

- La señal diferencia, $L-R$, se transmite modulada en amplitud con una frecuencia de portadora
  $f_m = 38$ kHz.

  - Por tanto, ocupa la banda $23 \mathrm{kHz}\le f\le 53 \mathrm{kHz}$, que sólo es accedida por los
    equipos estéreo, y, en el caso de colarse en un reproductor monofónico, ocupa la banda no audible.

- También se emite una sinusoide de $19 \mathrm{kHz}$, denominada *señal piloto*, que se usa para
  demodular síncronamente la señal diferencia.

- Finalmente, la señal de audio estéreo puede acompañarse de otras señales de señalización y servicio en
  frecuencias entre $55.35 \mathrm{kHz}$ y $94 \mathrm{kHz}$.

En los discos fonográficos, la semisuma de las señales está grabada del mismo modo que se haría en una
grabación monofónica, es decir, en la profundidad del surco; mientras que la semidiferencia se graba en el
desplazamiento a izquierda y derecha de la aguja. El resultado es que un reproductor mono, que sólo atiende
a la profundidad del surco, reproduce casi correctamente la señal monofónica, mientras que un reproductor
estéreo es capaz de separar los dos canales. Es posible que algo de la información de la semisuma se cuele
en el reproductor mono, pero, como su amplitud es muy pequeña, se manifestará como un ruido muy débil,
apenas perceptible.

En general, todos estos sistemas se basan en garantizar que el reproductor mono recibe correctamente la
semisuma de canales y que, si algo de la semidiferencia se cuela en la reproducción, sea en forma de un
ruido inaudible.

## Tareas a realizar

Escriba el fichero `estereo.py` que incluirá las funciones que permitirán el manejo de los canales de una
señal estéreo y su codificación/decodificación para compatibilizar ésta con sistemas monofónicos.


### Manejo de los canales de una señal estéreo

En un fichero WAVE estéreo con señales de 16 bits, cada muestra de cada canal se codifica con un entero de
dos bytes. La señal se almacena en el *cacho* `'data'` alternando, para cada muestra de $x[n]$, el valor
del canal izquierdo y el derecho:

<img src="img/est%C3%A9reo.png" width="380px">

#### Función `estereo2mono(ficEste, ficMono, canal=2)`

La función lee el fichero `ficEste`, que debe contener una señal estéreo, y escribe el fichero `ficMono`,
con una señal monofónica. El tipo concreto de señal que se almacenará en `ficMono` depende del argumento
`canal`:

- `canal=0`: Se almacena el canal izquierdo $L$.
- `canal=1`: Se almacena el canal derecho $R$.
- `canal=2`: Se almacena la semisuma $(L+R)/2$. Ha de ser la opción por defecto.
- `canal=3`: Se almacena la semidiferencia $(L-R)/2$.

#### Función `mono2estereo(ficIzq, ficDer, ficEste)`

Lee los ficheros `ficIzq` y `ficDer`, que contienen las señales monofónicas correspondientes a los canales
izquierdo y derecho, respectivamente, y construye con ellas una señal estéreo que almacena en el fichero
`ficEste`.

### Codificación estéreo usando los bits menos significativos

En la línea de los sistemas usados para codificar la información estéreo en señales de radio FM o en los
surcos de los discos fonográficos, podemos usar enteros de 32 bits para almacenar los dos canales de 16 bits:

- En los 16 bits más significativos se almacena la semisuma de los dos canales.

- En los 16 bits menos significativos se almacena la semidiferencia.

Los sistemas monofónicos sólo son capaces de manejar la señal de 32 bits. Esta señal es prácticamente
idéntica a la señal semisuma, ya que la semisuma ocupa los 16 bits más significativos. La señal
semidiferencia aparece como un ruido añadido a la señal, pero, como su amplitud es $2^{16}$ veces más
pequeña, será prácticamente inaudible (la relación señal a ruido es del orden de 90 dB).

Los sistemas estéreo son capaces de aislar las dos partes de la señal y, con ellas, reconstruir los dos
canales izquierdo y derecho.

<img src="img/est%C3%A9reo_cod.png" width="510px">

#### Función `codEstereo(ficEste, ficCod)`

Lee el fichero `ficEste`, que contiene una señal estéreo codificada con PCM lineal de 16 bits, y
construye con ellas una señal codificada con 32 bits que permita su reproducción tanto por sistemas
monofónicos como por sistemas estéreo preparados para ello.

#### Función `decEstereo(ficCod, ficEste)`

Lee el fichero `ficCod` con una señal monofónica de 32 bits en la que los 16 bits más significativos
contienen la semisuma de los dos canales de una señal estéreo y los 16 bits menos significativos la
semidiferencia, y escribe el fichero `ficEste` con los dos canales por separado en el formato de los
ficheros WAVE estéreo.

### Entrega

#### Fichero `estereo.py`

- El fichero debe incluir una cadena de documentación que incluirá el nombre del alumno y una descripción
  del contenido del fichero.

- Es muy recomendable escribir, además, sendas funciones que *empaqueten* y *desempaqueten* las cabeceras
  de los ficheros WAVE a partir de los datos contenidos en ellas.

- Aparte de `struct`, no se puede importar o usar ningún módulo externo.

- Se deben evitar los bucles. Se valorará el uso, cuando sea necesario, de *comprensiones*.

- Los ficheros se deben abrir y cerrar usando gestores de contexto.

- Las funciones deberán comprobar que los ficheros de entrada tienen el formato correcto y, en caso
  contrario, elevar la excepción correspondiente.

- Los ficheros resultantes deben ser reproducibles correctamente usando cualquier reproductor estándar;
  por ejemplo, el Windows Media Player o similar. Es probable, muy probable, que tenga que modificar los
  datos de las cabeceras de los ficheros para conseguirlo.

- Se valorará lo pythónico de la solución; en concreto, su claridad y sencillez, y el uso de los estándares
  marcados por PEP-ocho.

#### Comprobación del funcionamiento

Es responsabilidad del alumno comprobar que las distintas funciones realizan su cometido de manera correcta.
Para ello, se recomienda usar la canción [Komm, gib mir deine Hand](wav/komm.wav), suminstrada al efecto.
De todos modos, recuerde que, aunque sea en alemán, se trata de los Beatles, así que procure no destrozar
innecesariamente la canción.

#### Código desarrollado

Inserte a continuación el código de los métodos desarrollados en esta tarea, usando los comandos necesarios
para que se realice el realce sintáctico en Python del mismo (no vale insertar una imagen o una captura de
pantalla, debe hacerse en formato *markdown*).

##### Código de `estereo2mono()`

```Python
def estereo2mono(fileEstereo, fileMono, canal=2):
    """
    Aquesta funció llegeix un fitxer estereo de 16 bits i genera un fitxer monosegons el calan solicitat:.
        0. L
        1. R
        2. Semisuma  (Si no s'indica es realitza aquest)
        3. Semidiferència
    """

    # Primer de tot obtim el fitxer estereo en mode LECTURA BINÀRIA ('rb')
    with open(fileEstereo, 'rb') as f_in:
        # llegim la capçalera per obtenir les dades tèciques
        meta = llegir_capcalera(f_in)
        # Validem que sigui realment un fitxer estéreo (2 canals) i de 16 bits
        if meta["num_channels"] != 2 or meta["bits_per_sample"] != 16:
            raise ValueError("L'arxiu d'entrada ha dde ser estereo de 16 bits")

        # Calculem el nombre de mostres totals 
        num_samples = meta["data_size"] // 2  # 16 bits = 2 bytes
        # Llegim el bloc sencer on hi ha la música
        buffer = f_in.read(meta["data_size"])
        # Desempaquetem totes les mostres
        samples = st.unpack(f'<{num_samples}h', buffer)
                                            # h --> enters amb signe de 16 bits

    # Separem els canals barrejats utilitzant salts de llista (slicing) sense fer bucles
    # Comença a la posició 0 i agafa una mostra de cada dues (obté totes les esquerres)
    left = samples[::2]
    # Comença a la posició 1 i agafa una mostra de cada dues (obté totes les dretes)
    right = samples[1::2]

    # Decidim què desar segons el canal que hagi demanat l'usuari
    if canal == 0:
        mono_samples = left  # Guardem només el canal esquerre
    elif canal == 1:
        mono_samples = right  # Guardem només el canal dret
    elif canal == 2:
        # Semisuma: sumem esquerra i dreta mostra per mostra i dividim entre 2 per fer la barreja mono neta
        mono_samples = [int((l + r) / 2) for l, r in zip(left, right)]
    elif canal == 3:
        # Semidiferencia: restem esquerra i dreta mostra per mostra i dividim entre 2 (informació espacial)
        mono_samples = [int((l - r) / 2) for l, r in zip(left, right)]
    else:
        # Si ens demanen un canal inventat (que no sigui 0, 1, 2 o 3) donem un error
        raise ValueError("Canal no vàlid. Ha de ser 0, 1, 2 o 3.")

    # Calculem el tamany de les noves dades en bytes (cada mostra mono ocupa 2 bytes)
    nou_data_size = len(mono_samples) * 2
    # Obrim el nou fitxer monofònic en mode escriptura binària ('wb')
    with open(fileMono, 'wb') as f_out:
        # Escrivim la capçalera configurant-la com a MONO (1 canal) i 16 bits
        escriure_capcalera(f_out, 1, meta["sample_rate"], 16, nou_data_size)
        # Convertim la llista de números a bytes i la injectem al fitxer d'un sol cop
        f_out.write(st.pack(f'<{len(mono_samples)}h', *mono_samples))
```

##### Código de `mono2estereo()`
```Python
def mono2estereo(fileEsquerre, fileDret, fileEstereo):
    """
    Llegeix dos fitxers mono de 16 bits (canal dret i canal esquerre) i els combina per generar un fitxer estereo.
    """
    # Obrim simultàniament el fitxer de l'esquerra i el de la dreta en mode lectura binària
    with open(fileEsquerre, 'rb') as f_l, open(fileDret, 'rb') as f_r:
        # Llegim les capçaleres de tots dos fitxers mono
        meta_l = llegir_capcalera(f_l)
        meta_r = llegir_capcalera(f_r)

        # Comprovem que tots dos fitxers siguin mono (1 canal)
        if meta_l["num_channels"] != 1 or meta_r["num_channels"] != 1:
            raise ValueError("Els dos arxius d'entrada han de ser mono")
        # Comprovem que els dos fitxers tinguin la mateixa freqüència de mostratge per tal que el so no vagi descompensat
        if meta_l["sample_rate"] != meta_r["sample_rate"]:
            raise ValueError("Els arxius mono han de tenir la mateixa taxa de mostreig.")

        # Desempaquetem les mostres de so dels dos fitxers independents
        samples_l = st.unpack(f"<{meta_l['data_size'] // 2}h", f_l.read())
        samples_r = st.unpack(f"<{meta_r['data_size'] // 2}h", f_r.read())
                    # h --> enters de 16 bits

    # Mirem quin fitxer és més curt (per si de cas un tingués unes mostres més que l'altre)
    min_len = min(len(samples_l), len(samples_r))
    
    # Intercalem les mostres fent servir una llista de comprensió sense bucles tradicionals
    # zip() les ajunta en parelles (L0, R0), i el doble bucle les aplana a: [L0, R0, L1, R1...]
    estereo_samples = [sample for pair in zip(samples_l[:min_len], samples_r[:min_len]) for sample in pair]

    # El tamany de les dades estéreo serà el doble, ja que ara tenim dos canals junts
    nou_data_size = len(estereo_samples) * 2
    # Obrim el fitxer de sortida estéreo per escriure-hi els bytes
    with open(fileEstereo, 'wb') as f_out:
        # Creem la capçalera configurant-la com a ESTÉREO (2 canals) i 16 bits
        escriure_capcalera(f_out, 2, meta_l["sample_rate"], 16, nou_data_size)
        # Convertim la llista intercalada a bytes i la gravem al disc dur
        f_out.write(st.pack(f'<{len(estereo_samples)}h', *estereo_samples))
```

##### Código de `codEstereo()`
```Python
def codEstereo(fileEstereo, fileCod):
    """
    Codifiac un estereo de 16 bits en un arxiu mono de 32 bits
        MSB --> 16 bits més significatius --> Semisuma
        LSB --> 16 bits menys significatius --> Semidiferència
    """
    # Obrim el fitxer estéreo original
    with open(fileEstereo, 'rb') as f_in:
        meta = llegir_capcalera(f_in)
        # Comprovem que sigui estéreo de 16 bits
        if meta["num_channels"] != 2 or meta["bits_per_sample"] != 16:
            raise ValueError("Ha de ser un arxiu estéreo de 16 bits.")

        # Desempaquetem la llista de mostres de 16 bits
        num_samples = meta["data_size"] // 2
        samples = st.unpack(f'<{num_samples}h', f_in.read())

    # Separem el canal esquerre i el dret utilitzaznt tall de llistes (slicing)
    left = samples[::2]
    right = samples[1::2]

    # Ajuntem la semisuma i la semidiferència dins d'un únic bloc de 32 bits per mostra
        # & 0xFFFF: Màscara binària per fixar el número a 16 bits nets i netejar el signe negatiu de Python
        # << 16: Desplaça els bits de la semisuma cap a l'esquerra (part alta de la capsa de 32 bits)
        # | : L'operador lògic OR fusiona la part alta i la part baixa en un sol enter de 32 bits
    cod_samples = [
        ((int((l + r) / 2) & 0xFFFF) << 16) | (int((l - r) / 2) & 0xFFFF)
        for l, r in zip(left, right)
    ]

    # Convertim els valors a format de 32 bits amb signe real ('i' de 4 bytes)
    buffer_bytes = st.pack(f'<{len(cod_samples)}I', *cod_samples)
                                                                            # Si el valor és superior al límit permès, li restem el desbordament per corregir el signe negatiu en binari

    # Obrim el fitxer codificat final per escriure-hi
    with open(fileCod, 'wb') as f_out:
        # El desem com a MONO (1 canal), però atenció: de 32 BITS per mostra
        escriure_capcalera(f_out, 1, meta["sample_rate"], 32, len(buffer_bytes))
        # Escrivim la cadena de bytes generada
        f_out.write(buffer_bytes)

```

##### Código de `decEstereo()`
```Python
def decEstereo(fileCod, fileEstereo):
    """
    Decodifica un arxiu mono de 32 bits recuperant els canals L i R originals de 16 bits.
    """
    # Obrim el fitxer codificat de 32 bits
    with open(fileCod, 'rb') as f_in:
        meta = llegir_capcalera(f_in)
        # Validem que sigui realment un fitxer de 32 bits mono (el format on hem amagat l'estéreo)
        if meta["num_channels"] != 1 or meta["bits_per_sample"] != 32:
            raise ValueError("Es necessita un arxiu monofonic de 32 bits.")

        # Cada mostra de 32 bits ocupa 4 bytes, per tant dividim la mida total entre 4
        num_samples = meta["data_size"] // 4
        # Desempaquetem com a enters sense signe de 32 bits per poder extreure els bits fàcilment
        samples_32 = st.unpack(f'<{num_samples}I', f_in.read())
                    # I --> enters sense signe de 32 bits

    # Petita funció interna per restablir el signe negatiu dels enters de 16 bits extrets
    # Si el valor és igual o superior a 0x8000, significa que en veritat és un nombre negatiu (complement a dos)
    def to_int16(val):
        return val if val < 0x8000 else val - 0x10000

    # Recuperem la semisuma agafant el número de 32 bits i desplaçant-lo 16 posicions a la dreta (val >> 16)
    semisuma = [to_int16(val >> 16) for val in samples_32]
    # Recuperem la semidiferència esborrant la part alta gràcies a la màscara binària (val & 0xFFFF)
    semidiferencia = [to_int16(val & 0xFFFF) for val in samples_32]

    # Reconstrucció matemàtica dels canals originals barrejant la semisuma i la semidiferència
    # Esquerra (L) = Semisuma + Semidiferència
    left = [s + d for s, d in zip(semisuma, semidiferencia)]
    # Dreta (R) = Semisuma - Semidiferència
    right = [s - d for s, d in zip(semisuma, semidiferencia)]

    # Tornem a intercalar les mostres separades per reconstruir la llista única d'estéreo: [L0, R0, L1, R1...]
    estereo_samples = [sample for pair in zip(left, right) for sample in pair]

    # Calculem el tamany final de la música en bytes (mostres d'estéreo de 16 bits = 2 bytes per mostra)
    nou_data_size = len(estereo_samples) * 2
    # Obrim el fitxer estéreo de sortida per guardar-hi el resultat final decodificat
    with open(fileEstereo, 'wb') as f_out:
        # Li creem una capçalera estéreo estàndard neta de 2 canals i 16 bits
        escriure_capcalera(f_out, 2, meta["sample_rate"], 16, nou_data_size)
        # Convertim la llista de música recuperada a bytes i la desem al disc
        f_out.write(st.pack(f'<{len(estereo_samples)}h', *estereo_samples))
```

#### Subida del resultado al repositorio GitHub y *pull-request*

La entrega se formalizará mediante *pull request* al repositorio de la tarea.

El fichero `README.md` deberá respetar las reglas de los ficheros Markdown y visualizarse correctamente en
el repositorio, incluyendo el realce sintáctico del código fuente insertado.

"""
Txell Vilamajó i Puixeu
    Fitxer binari --> Un fitxer d'àudio no conté text, si no una serie de numeros (bytes). Per llegir-los doncs, s'ha d'indicar quants bytes agafar i com traduir-los a números naturals. 
    Format WAVE --> Conté la capçalera, que és on s'indica el nombre de canals, la freqüència de mostratge ... i les dades (mostres del so)

"""

import struct as st

# ---------------------------------------------------------------------------------------------------------------------- 
#  FUNCIONS QUE EMPAQUETEN I DESEMPAQUETEN LES CAPÇALERES DELS FITXERS WAVES A PARTIR DE LES DADES QUE CONTINGUIN 
# ----------------------------------------------------------------------------------------------------------------------

def llegir_capcalera(file):
    """
    Funció que llegeix i desempaqueta la capçalera d'un arxiu WAVE PCM de 16 o 32 bits. 
        Aquesta funció retorna un diccionari amb les metadades i la posició d'on començen les dades del fitxer (file).
    """
    # 1. LLEGIR EL BLOC PRINCIPAL (RIFF Chunk - 12 bytes fixos de la capçalera)
    # S'ha de comprovar que el fitxer sigui realment un fitxer vàlid, tipus WAVE i no una imatge o document de text:
    buffer = file.read(12) # read(12) permet llegir els primers 12 bytes
    if len(buffer) < 12: 
        # Si el buffer té una mida inferior a 12 vol dir que no s'han llegit els 12 bytes necessaris i per tant el ftxer està buit o malmès (elevem un error)+
        raise ValueError("L'arxiu WAVE està incomplet o és corrupte!")

    # Desempaquetem els bytes llegits: 4 caràcters de text (4s), 1 enter de 4 bytes (I) i 4 caràcterms de text més (4s)
    chunk_id, chunk_size, chunk_format = st.unpack('4sI4s', buffer) 
        # Amb unpack() fem el desempaquetament extreient tres dades:
            # 1. Si el fitxer comença amb la paraula RIFF
            # 2. El temany del fitxer
            # 3. Si posa WAVE (Format amb el qual estem treballant)
    
    if chunk_id != b'RIFF' or chunk_format != b'WAVE':
        # Si el fitxer no coté la paraula RIFF o WAVE no està en el format correcte i elevem un error. 
        raise ValueError("L'arxiu no està en un format WAVE vàlid")

    # 2. LLEGIR EL BLOC DE FORMAT (Subchunk1 'fmt ')
    # Llegim els següents 4 bytes per veure el nom del següent bloc
    subchunk1_id = file.read(4)  # Llegeix el primers 4 bytes
    # Busquem el bloc de text anomenat 'fmt'
        # Si hi ha altres blocs pel mig, es llegeixen, es mira quant ocupen i es salten
    while subchunk1_id != b'fmt ':
        # Si s'acaba el fitxer abans de trobar el format, elevem un error
        if len(subchunk1_id) < 4:
            raise ValueError("No s'ha trobat el camp 'fmt'")
        # Llegim la mida d'aquest bloc desconegut per saber quants bytes saltar
        size = st.unpack('<I', file.read(4))[0]
        file.seek(size, 1)  # Amb la funció seek() Ens saltem aquest bloc desconegut
        # Tornem a llegir 4 bytes per comprovar el nom del següent bloc
        subchunk1_id = file.read(4)

    # Llegim la mida del bloc 'fmt '
    subchunk1_size = st.unpack('<I', file.read(4))[0]
    # Llegim exactament els bytes que ocupa aquest bloc de format
    fmt_buffer = file.read(subchunk1_size)

    # Desempaquetem (unpack()) les dades tècniques de l'àudio (H = enter de 2 bytes, I = enter de 4 bytes)
    audio_format, num_channels, sample_rate, byte_rate, block_align, bits_per_sample = st.unpack('<HHIIHH', fmt_buffer[:16])
        # Extreiem: format d'àudio, canals (1 o 2), velocitat, bytes per segon, alineació i bits per mostra

    # 3. LLEGIR EL BLOC DE MÚSICA (Subchunk2 'data')
    # Llegim el subchunk2 (data) --> Fem el mateix procés de cerca fins a trobar la paraula 'data'

    # Llegim 4 bytes per buscar l'inici de les dades de so reals
    subchunk2_id = file.read(4)
    # Iniciem un altre bucle per buscar la paraula 'data' esquivant qualsevol bloc extra de metadades
    while subchunk2_id != b'data':
        if len(subchunk2_id) < 4:
            raise ValueError("No s'ha trobat la paraula 'data'.")
        size = st.unpack('<I', file.read(4))[0]
        file.seek(size, 1)
        subchunk2_id = file.read(4)

    # Llegim la mida total que ocupen les mostres de música reals (en bytes)
    subchunk2_size = st.unpack('<I', file.read(4))[0]
    
    # Retornem un diccionari ordenat amb totes les dades vitals que hem extret del fitxer
    return {
        "chunk_size": chunk_size,
        "num_channels": num_channels,
        "sample_rate": sample_rate,
        "byte_rate": byte_rate,
        "block_align": block_align,
        "bits_per_sample": bits_per_sample,
        "data_size": subchunk2_size
    }

    
def escriure_capcalera(file, num_channels, sample_rate, bits_per_sample, data_size):
    """
    Genera i escriu una capçalera WAVE PCM vàlida a l'arxiu.ç
        Rep les propietats del so (canals, velocitat, etc.) i les converteix en bytes utilitzant st.pack
    """
  # CÀLCULEM PARÀMETRES:
    # Mida fixa interna del bloc 'fmt ' per a fitxers d'àudio PCM estàndard (16 bytes)
    subchunk1_size = 16
    # Calculem l'alineació de bloc: quants bytes ocupa una mostra combinant tots els canals
    block_align = (num_channels * bits_per_sample) // 8
    # Calculem el byterate --> bytes per segon que tindrà aquest fitxer
    byte_rate = sample_rate * block_align
    # Calculem la mida de la capçalera general (36 bytes fixos de control + el tamany de la música)
    chunk_size = 36 + data_size

  # ESCRIVIM AL FITXER
    # Escribim el bloc principal 'RIFF' transformant les dades a bytes binaris ('<4sI4s')
    file.write(st.pack('<4sI4s', b'RIFF', chunk_size, b'WAVE'))
    # Escribim l'etiqueta 'fmt ' i la seva mida
    file.write(st.pack('<4sI', b'fmt ', subchunk1_size))
    # Escribim els detalls tècnics (Format=1 (PCM), canals, velocitat, bytes/segon, alineació, bits)
    file.write(st.pack('<HHIIHH', 1, num_channels, sample_rate, byte_rate, block_align, bits_per_sample))
    # Escribim l'etiqueta 'data' i la mida exacta de les dades de música que aniran a continuació
    file.write(st.pack('<4sI', b'data', data_size))


# ---------------------------------------------------------------------------------------------------------------------- 
#  FUNCIONS DEMANADES A LA TASCA
# ----------------------------------------------------------------------------------------------------------------------

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
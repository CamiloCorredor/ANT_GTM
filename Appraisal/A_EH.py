import string
import time
print('Iniciando avalúo ...')
BP = time.time()

from num2words import num2words

# import datetime
from datetime import datetime
import locale
locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
# Obtener la fecha actual
fecha_actual = datetime.now()

# Obtener el día, mes y año
dia = fecha_actual.day
mes = fecha_actual.strftime("%B") # %B muestra el nombre del mes en letras
anio = fecha_actual.year

from docx import Document
from docx.shared import Inches

document = Document()

# document.add_heading('Document Title', 0)

document.add_paragraph(f"""Bogotá, D. C. {dia} de {mes} de {anio} \n """)

p = document.add_paragraph(f"""Señores\n""")
p.add_run('ELECTROHUILA\n').bold = True
p.add_run('Neiva, Huila\n')
#Variables a capturar
Propietarios = ['JUAN PEDRO']
Cedulas = ['123456']
add_text1 = ''
N_Predio = 'GUAYACANES' ##Nombre del predio
TPredio = 'RURAL' ##Predio en zona rural
Mun = 'Rivera'
TDR = 'PROPIETARIO' ##Calidad del propietario
DAP = 'E.P. N° 1009 del 08 de abril de 2014 de la Notaría Tercera del municipio de Rivera, departamento de Huila, debidamente registrada en la anotación N° 1 del CTL 200-235397.' ##Documetos que acredita propiedad

V_N = 'Los Medios.'      ##Norte
V_S = 'Bajo Pedregal.'##Sur 
V_O = 'Los Medios.'##Oriente
V_OR = 'El Guadual.'## Occidente

POT = 'PBOT'  ##Tipo Ordenamiento Territorial
Ac_POT = 'Acuerdo 004 de 2022'
Nom_POT = 'POR MEDIO DEL CUAL SE APRUEBA EL PLAN BÁSICO DE ORDENAMIENTO TERRITORIAL PBOT DEL MUNICIPIO DE RIVERA (HUILA)'
Art_POT = '23'


i_d = 'd' ##Margen izquierda o derecha

track = 5                                       ## Duraciń trayecto
w_track = num2words(track, lang = 'es')  ## Trayecto en letras

VP = 'Neiva – Rivera' ##Vía Principal al predio
OR_VIA = 'segundo' ##Orden de la via
V_CP = 'Arenoso' #3Via a centro poblado
OV_CP = 'Tercer' ##Orden vía a centro poblado

##1.9.1
lat = 2.79394
lon = -75.25974
alt = 705 

date = '17/07/2023'
# Convertimos la fecha a un objeto datetime
date = datetime.strptime(date, '%d/%m/%Y')
# Formateamos la fecha como un string en el formato deseado
date = date.strftime('%d de %B de %Y')

P = 'Y'
CTL = 'Y'
CUS = 'Y'
EP = 'N'

CC_Num = '416150000000000060079000000000'
CTL_Num = '200-34357'
Date_CTL = '30/05/2021'
Date_CTL = datetime.strptime(Date_CTL, '%d/%m/%Y')
Date_CTL_str = Date_CTL.strftime('%d de %B de %Y')
Date_CUS = '30/04/2021'
Date_CUS = datetime.strptime(Date_CUS, '%d/%m/%Y')
Date_CUS_str = Date_CUS.strftime('%d de %B de %Y')


# lp = len(Propietarios)
if len(Propietarios) > 1:
    add_text = 'de los señores'
    for _ in range(0,len(Propietarios)):
        add_text1 = add_text1 + ',' +Propietarios[_]
else:
    add_text = 'del señor'


# print(Propietarios[1])
# print(add_text1)

p = document.add_paragraph(f"""Atendiendo su amable solicitud, adjunto a la presente le estamos enviando el avalúo comercial practicado al bien inmueble de propiedad {add_text}""")
p.add_run({add_text1}).bold = True
p.add_run(f""";predio ubicado en la vereda Los Vereda""")
p.add_run(f"""VEREDA""").bold = True
p.add_run(f""",jurisdicción del municipio de""")
p.add_run(f"""MUNICIPIO""").blod = True
p.add_run('en el departamento del Huila')

document.add_paragraph(f"""El valor comercial del inmueble ha sido elaborado según los parámetros y criterios de la Resolución No. 620 del 23 de septiembre de 2.008, por medio de la cual se establecieron los procedimientos para la elaboración de los avalúos ordenados dentro del marco de la Ley 388 de 1.997. \n \n Informo expresa y motivadamente que los precios nominales del mercado al que pertenece el inmueble avaluado no han experimentado caídas significativas y duraderas en los últimos cinco (5) años. \n \n Cordialmente""")

p = document.add_paragraph('')
p.add_run(f'CAMILO ANDRÉS LÓPEZ VELASCO \n')
p.add_run(f'Ingeniero Catastral y Geodesta \n').bold = True
p.add_run(f'CAMILO ANDRÉS LÓPEZ VELASCO\n').bold = True
p.add_run(f'M.P 25222-339415 CND\n').bold = True
p.add_run(f'RAA: AVAL – 1015433632 de acuerdo con el autorregulador nacional de Avaluadores ANA.').bold = True

p = document.add_paragraph('')
p.add_run(f'AVALÚO COMERICAL INMUEBLE RURAL\n').bold = True
p.add_run(f'PROPÓSITO DEL AVALUÓ:\n').bold = True
p.add_run(f'Estimar el valor comercial o de mercado del bien inmueble identificado en el Capítulo 1, numeral 1.7 del informe valuatorio, teniendo en cuenta las condiciones económicas reinantes al momento del avalúo y los factores de comercialización que puedan incidir positiva o negativamente en el resultado final.\n \n')
p.add_run(f'DEFINICIÓN DE VALOR COMERCIAL O DE MERCADO:\n').bold = True
p.add_run(f'El valor comercial o de mercado como se utiliza en este informe se define como: la cuantía estimada por la que un bien podría intercambiarse en la fecha de valuación, entre un comprador dispuesto a comprar y un vendedor dispuesto a vender, en una transacción libre tras una comercialización adecuada, en la que las partes hayan actuado con la información suficiente, de manera prudente y sin coacción. \n \n')
p.add_run(f'DERECHO DE PROPIEDAD:\n').bold = True
p.add_run(f'Se considera que el propietario tiene derecho de propiedad completo y absoluto pudiendo disponer y transferir el inmueble con entera libertad.\n \n') 
p.add_run(f'MAYOR Y MEJOR USO:\n').bold = True
p.add_run(f'Se define como: El uso más probable de un bien, físicamente posible, justificado adecuadamente, permitido jurídicamente, financieramente viable y que da como resultado el mayor valor del bien valorado.\n \n')
p.add_run(f'VIGENCIA DEL AVALUÓ:\n').bold = True
p.add_run(f'El presente avalúo tiene vigencia de un año a partir de la fecha de su emisión, siempre y cuando no se presenten circunstancias o cambios inesperados de índole jurídica, técnica, económica o normativa que afecten o modifiquen los criterios analizados. \n \n')

document.add_page_break()


p = document.add_paragraph('')
p.add_run(f'1.1.- CLASE DE AVALÚO:\n').bold = True
p.add_run(f'Comercial.\n')
p.add_run(f'1.2.- TIPO DE INMUEBLE:\n').bold = True	
p.add_run(f'El inmueble objeto de avalúo consiste en un lote de terreno denominado')
p.add_run(f'{N_Predio}').bold = True
p.add_run(f', tipo de predio ')
p.add_run(f'{TPredio}').bold = True
p.add_run(f'segun certificado de tradición y libertad')
 
p.add_run(f'1.3. DESTINACIÓN ECONÓMICA ACTUAL DEL INMUEBLE:\n')
p.add_run(f'Actualmente el inmueble está siendo explotado en el área de franja de servidumbre, sin embargo, el sector en el que se encuentra es de zona agropecuaria, donde se identifican varios lotes con actividad económica de tipo pecuaria y explotación turística.\n')
p.add_run(f'1.4. SOLICITANTE DEL AVALUÓ:\n').bold = True	
p.add_run(f'Electrohuila.\n')
p.add_run(f'1.5. PROPIETARIO DEL INMUEBLE:\n').bold = True	
resultado = ''
add_text3 = []

##Pendiente para varios propietarios
if len(Propietarios) == 1:
    p.add_run(f'{Propietarios[0]} identificado con cédula de ciudadanía N° {Cedulas[0]}')
else: 
    pass

# for _ in range(0, len(Propietarios)):
    
#     # print(Cedulas[0])
#     # print(Cedulas[1])
#     add_text3.append(f'{Propietarios[_]} identificado con cédula de ciudadanía N° {Cedulas[_]} y ')
    # print(f'{Propietarios[_]} identificado con cédula de ciudadanía N° {Cedulas[_]} y')
# add_text31 = ''.join(add_text3)
# p.add_run(f"""{add_text31}""")

p.add_run(f'en calidad de {TDR} de conformidad, con la {DAP}.\n \n')

p.add_run(f'1.6. NOMBRE DEL INMUEBLE:\n').bold = True
p.add_run(f'Predio denominado ')
p.add_run(f'{N_Predio} \n').bold = True

p.add_run(f'1.7. DIRECCIÓN DEL INMUEBLE:\n').bold = True
p.add_run(f'{N_Predio} \n')
p.add_run(f'1.7.1 PARAJE O VEREDA:\n').bold = True

##Falta realizar intersección de la vereda
p.add_run(f'VEREDA (De acuerdo con información geográfica del DANE y Certificado de Uso del Suelo) \n')
p.add_run(f'1.7.2 MUNICIPIO:\n').bold = True
p.add_run(f' {Mun}\n')

p.add_run(f'1.7.3 MUNICIPIO:\n').bold = True
p.add_run(f' Huila \n')

p.add_run(f'1.8 DELIMITACIÓN DEL SECTOR:\n').bold = True
p.add_run(f'Norte: Vereda {V_N}\n')
p.add_run(f'Sur: Vereda {V_S}\n')
p.add_run(f'Occidente: Vereda {V_O}\n')
p.add_run(f'Oriente: Vereda {V_OR}\n')

p.add_run(f'1.9 LOCALIZACIÓN GEOGRÁFICA DEL INMUEBLE: :\n').bold = True

p.add_run(f'El inmueble denominado {N_Predio}, materia de este avalúo, es un predio rural cuyos usos se establecen en el articulo {Art_POT} del {POT} del municipio de {Mun}.')
p.add_run(f'Predio que se encuentra ubicado al costado {i_d} de la vía veredal.')
dist = '10'

track = 5
w_track = num2words(track, lang = 'es')
 
p.add_run(f'El inmueble sujeto a avalúo se encuentra ubicado a {dist} km aproximadamente de la cabecera municipal de Rivera por las vías secundarias y terciarias del municipio; el trayecto puede ser de {w_track} ({track}) minutos \n')
p.add_run(f'El sector de influencia en de zona agroturistica donde se identifican varios lotes con actividad económica de tipo agropecuario, pecuario y explotación turística.\n')
p.add_run(f'La infraestructura vial y de servicios públicos, funcionan satisfactoriamente; la vía principal de la zona de influencia e inmediatamente circundante corresponde a la {VP}, esta se encuentra en pavimento, vía de segundo orden de acuerdo con el {POT} del municipio de {Mun}, en buen estado de conservación, adicionalmente cuenta con la vía al centro poblado de la vereda {V_CP}, vía de tercer nivel según el {POT} de {Mun}. El sector cuenta con redes de acueducto veredal y de riego, pozo séptico y energía Eléctrica.')

p.add_run(f'1.9.1. COORDENADAS GEOGRÁFICAS DEL ACCESO PRINCIPAL DEL INMUEBLE:\n')
lat = 2.79394
lon = -75.25974
alt = 705 
p.add_run(f'latitud:').bold = True
p.add_run(f'{lat}°N \n')
p.add_run(f'Longitud:').bold = True
p.add_run(f'{lon}°O \n')
p.add_run(f'Altura:').bold = True
p.add_run(f'{alt}msnm \n')

p.add_run(f'1.10. VECINDARIO INMEDIATO: \n').bold = True
p.add_run(f'El sector de influencia se halla conformado por pequeños y medianos lotes explotados para actividad económica agroturística y lotes sin explotación en la zona agropecuaria del municipio de {Mun}.')

p.add_run(f'1.11. INFRAESTRUCTURA VIAL: \n').bold = True
p.add_run(f'La vía más importante de la zona es la que conduce al Centro Poblado {V_CP}, la cual es vía de {OV_CP} según {POT} de {Mun} y se encuentra en buen estado de conservación.\n')

p.add_run(f'1.12. INFRAESTRUCTURA DE SERVICIOS PÚBLICOS: \n').bold = True
p.add_run(f'El sector cuenta con las redes instaladas de los servicios públicos de acueducto, alcantarillado y energía eléctrica (Rurales).\n')

p.add_run(f'1.13. TRANSPORTE PÚBLICO: \n').bold = True
p.add_run(f'El sector cuenta con transporte intermunicipal por la vía descrita anteriormente y rutas rurales (camperos y motos).\n')

p.add_run(f'1.14. ESTRATIFICACIÓN SOCIOECONÓMICA DE LA ZONA: \n').bold = True
p.add_run(f'No aplica para el presente caso, teniendo en cuenta que, el estrato aplica a los inmuebles de uso residencial.\n')

p.add_run(f'1.15 FECHA DE LA VISITA: \n').bold = True
p.add_run(f'{date} \n')

p.add_run(f'2. DOCUMENTOS SUMINISTRADOS PARA EL AVALÚO: \n').bold = True
P = 'Y'
CTL = 'Y'
CUS = 'Y'
EP = 'N'

CTL_Num = '200-34357'
Date_CTL = '30/04/2021'
Date_CUS = '30/04/2021'


if P == 'Y':
    p.add_run(f'        Plano de servidumbre aportado por ElectroHuila \n')
else: 
    pass
if CTL == 'Y':
    p.add_run(f'        Certificado de tradición y libertad No {CTL_Num} de fecha {Date_CTL_str} \n')
else: 
    pass
if CUS == 'Y':
    p.add_run(f'        Certificado de uso del suelo de fecha {Date_CUS_str} \n')
else:
    pass
p.add_run(f'        {DAP}\n')


p.add_run(f'3. INFORMACIÓN JURÍDICA \n').bold = True
p.add_run(f'3.1. PROPIETARIO DEL INMUEBLE:	 \n').bold = True

resultado = ''
add_text3 = []

##Pendiente para varios propietarios
if len(Propietarios) == 1:
    p.add_run(f'{Propietarios[0]} identificado con cédula de ciudadanía N° {Cedulas[0]}')
else: 
    pass

# for _ in range(0, len(Propietarios)):
    
#     # print(Cedulas[0])
#     # print(Cedulas[1])
#     add_text3.append(f'{Propietarios[_]} identificado con cédula de ciudadanía N° {Cedulas[_]} y ')
    # print(f'{Propietarios[_]} identificado con cédula de ciudadanía N° {Cedulas[_]} y')
# add_text31 = ''.join(add_text3)
# p.add_run(f"""{add_text31}""")

p.add_run(f'en calidad de {TDR} de conformidad, con la {DAP}.\n \n')
p.add_run(f'3.2. TITULO DE PROPIEDAD Y/O ESCRITURA PÚBLICA: \n').bold = True
p.add_run(f'{DAP} \n')

p.add_run(f'3.3. MATRICULA INMOBILIARIA: \n').bold = True
p.add_run(f'{CTL_Num} \n')

p.add_run(f'3.4. CEDULA CATASTRAL: \n').bold = True
p.add_run(f'{CC_Num} \n')

p.add_run(f'4. NORMATIVIDAD VIGENTE: \n').bold = True
p.add_run(f'La Reglamentación de Usos del Suelo en el Municipio de {Mun}, está contenida en el {Ac_POT} {Nom_POT} que determina el sector como suelo rural y cuyos usos están especificados en el Ártículo {Art_POT} del {POT} del municipio de {Mun}.  \n')














# document.add_heading('Heading, level 1', level=1)
# document.add_paragraph('Intense quote', style='Intense Quote')

# document.add_paragraph(
#     'first item in unordered list', style='List Bullet'
# )
# document.add_paragraph(
#     'first item in ordered list', style='List Number'
# )

# document.add_picture('monty-truth.png', width=Inches(1.25))

# records = (
#     (3, '101', 'Spam'),
#     (7, '422', 'Eggs'),
#     (4, '631', 'Spam, spam, eggs, and spam')
# )

# table = document.add_table(rows=1, cols=3)
# hdr_cells = table.rows[0].cells
# hdr_cells[0].text = 'Qty'
# hdr_cells[1].text = 'Id'
# hdr_cells[2].text = 'Desc'
# for qty, id, desc in records:
#     row_cells = table.add_row().cells
#     row_cells[0].text = str(qty)
#     row_cells[1].text = id
#     row_cells[2].text = desc

# document.add_page_break()

document.save('demo.docx')




# import docx
# doc.add_paragraph(f'Bogotá, D. C. {dia} de {mes} de {anio}')
# doc.add_paragraph(f"""Señores:
# ELECTROHUILA
# NeivaHuila""")
# doc.save('/home/camilocorredor/DS_P/ETL/Appraisal/Document10.docx')

# import time
# print('Iniciando ITJP ...')
# BP = time.time()
# from ctypes import c_char_p
# from osgeo import ogr, osr

# import shapely.wkb
# from shapely.geometry import Polygon

# import openpyxl
# import os
# os.environ['USE_PYGEOS'] = '0'
# import geopandas as gpd

# import psycopg2

# from shapely.wkb import loads
# from shapely import wkb
# import os

# import binascii
# import matplotlib.pyplot as plt


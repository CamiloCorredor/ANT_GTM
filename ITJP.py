
from ctypes import c_char_p
import time
start_time = time.time()

import openpyxl
import os
os.environ['USE_PYGEOS'] = '0'
import geopandas as gpd


import psycopg2
import time
from shapely.wkb import loads
import os

import binascii
import matplotlib.pyplot as plt


import time

connection = psycopg2.connect(
    host="localhost",
    database="ladm_ttsp",
    user="postgres",
    password="1234"
)

cursor = connection.cursor()
sql = f"""select P.id_operacion as QR, (st_area(T.geometria))/10000, I.nombre, I.documento_identidad, P.nombre, T.geometria as geom, P.matricula_inmobiliaria as fmi
from rev_08.lc_predio as P
inner join rev_08.lc_terreno as T on P.id_operacion = T.etiqueta 
inner join rev_08.lc_derecho as D on P.t_id = D.unidad
inner join rev_08.lc_derechotipo as DT on D.tipo = DT.t_id 
left join rev_08.lc_interesado as I on D.interesado_lc_interesado = I.t_id
left join rev_08.lc_agrupacioninteresados as AGI on D.interesado_lc_agrupacioninteresados = AGI.t_id 
left join rev_08.col_grupointeresadotipo as GIT on AGI.tipo = GIT.t_id 
left join rev_08.lc_interesadodocumentotipo as IDT on I.tipo_documento = IDT.t_id
left join rev_08.lc_sexotipo as SX on I.sexo = SX.t_id
left join rev_08.lc_grupoetnicotipo as GE on I.grupo_etnico = GE.t_id 
left join rev_08.lc_prediotipo as PT on P.tipo = PT.t_id
where P.id_operacion = '1875303137'"""
cursor.execute(sql)
schema = cursor.fetchall()

archivo_excel = openpyxl.load_workbook('/home/camilocorredor/DS_P/ETL/ACCTI- F110 - ITJ EJ.xlsx')
sheet = archivo_excel['Hoja1']

#Nombre solicitante
# sheet['B9'] = f"""Nombre solicitante: {schema[0][2]}
# Documento de identificación: {schema[0][3]}"""
# #Nombre del Predio
# sheet['B19'] = f"""Nombre: {schema[0][4]}"""
# #Area predio
# sheet['F21'] = int(schema[0][1])
# sheet['I21'] = round((float(schema[0][1]) - int(schema[0][1]))*10000,3)
#Cedula catastral 
#Cargar capa predial y realizar intersect AC21

hex_wkb = schema[0][5]
wkb = binascii.unhexlify(hex_wkb)
geometry = loads(wkb)


#Cargar información
# R_Terreno = gpd.read_file("/home/camilocorredor/DS_P/ETL/Layers/R_Terreno.shp")
# R_Terreno.to_crs('EPSG:9377', inplace=True)

# ZRC = gpd.read_file("/home/camilocorredor/DS_P/ETL/Layers/ZRC_PatoBalsillas.gpkg")
# ZRC.to_crs('EPSG:9377', inplace=True)

# Pnn = gpd.read_file('/home/camilocorredor/DS_P/ETL/Layers/PNN.shp')
# Pnn.to_crs('EPSG:9377', inplace=True)

# Ley_2 = gpd.read_file("/home/camilocorredor/DS_P/ETL/Layers/Ley2.shp")
# Ley_2.to_crs('EPSG:9377', inplace=True)

# Paramos = gpd.read_file("/home/camilocorredor/DS_P/ETL/Layers/Paramos.shp")
# Paramos.to_crs('EPSG:9377', inplace=True)

# Bosques = gpd.read_file("/home/camilocorredor/DS_P/ETL/Layers/Bosques.shp")
# Bosques.to_crs('EPSG:9377', inplace=True)

Z_Degradacion = gpd.read_file("/home/camilocorredor/DS_P/ETL/Layers/Zona1_degradacion_suelo.shp")
Z_Degradacion.to_crs('EPSG:9377', inplace=True)



# # # ##Cédula catastral FMI
# CC_pol = gpd.overlay(R_Terreno, gpd.GeoDataFrame(geometry = [geometry]), how = 'intersection')
# sheet['AC21'] = CC_pol.iloc[0,0]

# if schema[0][6] is None:
#     sheet['V21'] = 'X'
#     sheet['X21'] = 'No registra'
# else:
#     sheet['T21'] = 'SI X'
#     sheet['X21'] = schema[0][6]
  
# ##Zona de reserva campesina
# ZRC_pol = gpd.overlay(ZRC, gpd.GeoDataFrame(geometry=[geometry]), how='intersection')
# a_ZRC_pol = (ZRC_pol.geometry.area)/10000

# print(a_ZRC_pol)
# if float(a_ZRC_pol) > 0:
#     sheet['H36'] = 'SI X'
#     sheet['J36'] = '¿Cuál? Zona de reserva campesina del Pato Balsillas'
# else:
#     sheet['H36'] = 'SI'
#     sheet['J36'] = '¿Cuál?'

# PNN_pol = gpd.overlay(Pnn, gpd.GeoDataFrame(geometry=[geometry]), how='intersection')
# A_PNN_pol = PNN_pol.geometry.area

# if PNN_pol.empty:
#     sheet['L39'] = 'NO X'
# else:
#     sheet['K39'] = 'SI X' 
#     sheet['M39'] = f"""¿Cuál? {PNN_pol.iloc[0,4]} {PNN_pol.iloc[0,2]}"""


#Para celda M34
# Ley2 = gpd.overlay(Ley_2, gpd.GeoDataFrame(geometry=[geometry]), how='intersection')
# Paramos = gpd.overlay(Paramos, gpd.GeoDataFrame(geometry=[geometry]), how='intersection')
Degradacion = gpd.overlay(Z_Degradacion, gpd.GeoDataFrame(geometry=[geometry]), how='intersection')

if Degradacion.empty:
    print('Vacio')
else:
    print('No vacio')


cd = time.time()
print(f'Tiempo de ejecucion: {cd-start_time}')




#Plot graph
# print(hex_wkb)
# wkb = binascii.unhexlify(hex_wkb)
# geometry = loads(wkb)
# gdf = gpd.GeoDataFrame(geometry=[geometry])
# gdf.plot()
# plt.show()

archivo_excel.save('/home/camilocorredor/DS_P/ETL/Ejemplo1.xlsx')
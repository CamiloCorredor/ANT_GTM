import time
start_time = time.time()

import openpyxl
import geopandas as gpd
from osgeo import gdal

import psycopg2
import time
from shapely.geometry import shape
from shapely.wkb import loads
import os
os.environ['USE_PYGEOS'] = '0'

import binascii
import matplotlib.pyplot as plt


connection = psycopg2.connect(
    host="localhost",
    database="ladm_ttsp",
    user="postgres",
    password="1234"
)

cursor = connection.cursor()
sql = f"""select P.id_operacion as QR, (st_area(T.geometria))/10000, I.nombre, I.documento_identidad, P.nombre, T.geometria as geom
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
where P.id_operacion = '1875300405'"""
cursor.execute(sql)
schema = cursor.fetchall()

archivo_excel = openpyxl.load_workbook('/home/camilocorredor/DS_P/ETL/ACCTI- F110 - ITJ EJ.xlsx')
sheet = archivo_excel['Hoja1']

#Nombre solicitante
sheet['B9'] = f"""Nombre solicitante: {schema[0][2]}
Documento de identificación: {schema[0][3]}"""
#Nombre del Predio
sheet['B19'] = f"""Nombre: {schema[0][4]}"""
#Area predio
sheet['F21'] = int(schema[0][1])
sheet['I21'] = round((float(schema[0][1]) - int(schema[0][1]))*10000,3)
#Cedula catastral 
#Cargar capa predial y realizar intersect AC21

hex_wkb = schema[0][5]
wkb = binascii.unhexlify(hex_wkb)
geometry = loads(wkb)

R_Terreno = gpd.read_file("/home/camilocorredor/DS_P/ETL/Layers/R_Terreno.gpkg", use_threads=True, chunksize=1000)
cd = time.time()
print(cd-start_time)
ZRC = gpd.read_file("/home/camilocorredor/DS_P/ETL/Layers/ZRC_PatoBalsillas.gpkg")

##Cédula catastral
CC_pol = gpd.overlay(R_Terreno, gpd.GeoDataFrame(geometry = [geometry]), how = 'intersection')
print(CC_pol.head())

#CC_pol.plot()
# plt.show()




##Zona de reserva campesina
ZRC_pol = gpd.overlay(ZRC, gpd.GeoDataFrame(geometry=[geometry]), how='intersection')
a_ZRC_pol = (ZRC_pol.geometry.area)/10000
# print(a_ZRC_pol)
# if float(a_ZRC_pol) > 0:
#     sheet['H36'] = 'SI X'
#     sheet['J36'] = '¿Cuál? Zona de reserva campesina del Pato Balsillas'
# else:
#     sheet['H36'] = 'SI'
#     sheet['J36'] = '¿Cuál?'

print('ok')




#Plot graph
# print(hex_wkb)
# wkb = binascii.unhexlify(hex_wkb)
# geometry = loads(wkb)
# gdf = gpd.GeoDataFrame(geometry=[geometry])
# gdf.plot()
# plt.show()

archivo_excel.save('/home/camilocorredor/DS_P/ETL/Ejemplo1.xlsx')
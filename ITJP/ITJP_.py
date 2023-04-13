
import time
from ctypes import c_char_p
from osgeo import ogr, osr
print('Iniciando ITJP ...')
BP = time.time()

import shapely.wkb
from shapely.geometry import Polygon


import openpyxl
import os
os.environ['USE_PYGEOS'] = '0'
import geopandas as gpd

import psycopg2

from shapely.wkb import loads
from shapely import wkb
import os

import binascii
import matplotlib.pyplot as plt

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
where P.id_operacion = '1875301941'"""
cursor.execute(sql)
schema = cursor.fetchall()

archivo_excel = openpyxl.load_workbook('/home/camilocorredor/DS_P/ETL/ACCTI- F110 - ITJ EJ.xlsx')
sheet = archivo_excel['Hoja1']

hex_wkb = schema[0][5]
#wkb = binascii.unhexlify(hex_wkb)
spatial_reference = osr.SpatialReference()
spatial_reference.ImportFromEPSG(9377)

# Leer el objeto WKB desde un archivo o una base de datos
#wkb = hex_wkb

# Convertir el objeto WKB a un objeto shapely
shapely_obj = shapely.wkb.loads(schema[0][5])
predio = ogr.CreateGeometryFromWkt(shapely_obj.wkt)
predio.AssignSpatialReference(spatial_reference)
#geometry = loads(wkb)

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
driver = ogr.GetDriverByName('ESRI Shapefile')
spatial_reference = osr.SpatialReference()
spatial_reference.ImportFromEPSG(9377) # 

# driver = ogr.GetDriverByName('ESRI Shapefile')
lyr = driver.Open('/home/camilocorredor/DS_P/ETL/Layers/R_Terreno.shp') ##OK Capa
layer = lyr.GetLayer() 
    
for feature in layer:     
    geometry = feature.GetGeometryRef()
    intersect = geometry.Intersection(predio)
    inter_tf = geometry.Intersect(predio)
    if inter_tf == True:
        sheet['AC21'] = feature.GetField('codigo')
        codigo = feature.GetField('codigo')
    else: 
        a = 1 

#En el área solicitada se evidencian zonas de bosques
lyr = driver.Open('/home/camilocorredor/DS_P/ETL/Layers/Bosques_.shp') ##OK Capa
layer = lyr.GetLayer() 
    
for feature in layer:     
    geometry = feature.GetGeometryRef()
    intersect = geometry.Intersection(predio)
    inter_tf = geometry.Intersect(predio)
    if inter_tf == True:
        sheet['K34'] = "SI X"
        sheet['M34'] = f"""El predio presenta traslape con un área de {round(intersect.Area()/10000,3)}Ha, que equivale a un {round((intersect.Area()/10000)/(schema[0][1])*100,3)}%, con la capa cartográfica Bosques-2010 del IDEAM"""
        area_bos = round((intersect.Area()/10000)/(schema[0][1])*100,3)
        ab = round(intersect.Area()/10000,3)
    else: 
        sheet['L34'] = f'NO X'

#Determinantes ambientales
lyr = driver.Open('/home/camilocorredor/DS_P/ETL/Layers/Drenaje_Sencillo_(30m)_.shp') ## OK
layer = lyr.GetLayer() 

for feature in layer:     
    geometry = feature.GetGeometryRef()
    intersect = geometry.Intersection(predio)
    inter_tf1 = geometry.Intersect(predio)
    if inter_tf1 == True:
        sheet['K34'] = "SI X"
        sheet['M34'] = f"""El predio presenta traslape con un área de {round(intersect.Area()/10000,3)}Ha, que equivale a un {round((intersect.Area()/10000)/(schema[0][1])*100,3)}%, con la capa cartográfica Bosques-2010 del IDEAM"""
        ds = round((intersect.Area()/10000)/(schema[0][1])*100,3)
        area_ds = round(intersect.Area()/10000,3)
    else: 
        sheet['L35'] = 'NO X'

lyr = driver.Open('/home/camilocorredor/DS_P/ETL/Layers/Cuenca_Rios.shp') ##OK Capa
layer = lyr.GetLayer() 
C_R_A = []
for feature in layer:     
    geometry = feature.GetGeometryRef()
    intersect = geometry.Intersection(predio)
    inter_tf = geometry.Intersect(predio)
    if inter_tf == True:
        # C_R_A.append(feature.GetField('NOM_ZH'))
        CR = feature.GetField('NOM_SZH')
        CR_A = intersect.Area()
        
    else: 
        pass

# ZRC 
lyr = driver.Open('/home/camilocorredor/DS_P/ETL/Layers/ZRC_PB.shp') ##OK Capa
layer = lyr.GetLayer() 
    
for feature in layer:     
    geometry = feature.GetGeometryRef()
    intersect = geometry.Intersection(predio)
    inter_tf = geometry.Intersect(predio)
    if inter_tf == True and round(intersect.Area()/10000,3) == round(schema[0][1],3):
        p_zrc = round((intersect.Area()/10000)/(schema[0][1])*100,3)
        sheet['H36'] = "SI X"
        sheet['J36'] = f"""Zona de reserva campesina del Pato Balsillas"""
    else: 
        sheet['L34'] = f'NO X'

##Cruce vias Buffer 
lyr = driver.Open('/home/camilocorredor/DS_P/ETL/Layers/Buffer_Vial.shp') ## Ok Capa
layer = lyr.GetLayer() 
area_bf = 0
for feature in layer:     
    geometry = feature.GetGeometryRef()
    intersect = geometry.Intersection(predio)
    inter_tf = geometry.Intersect(predio)
    if inter_tf == True:
        sheet['K40'] = "SI X"
        sheet['M34'] = f"""El predio presenta traslape con un área de {round(intersect.Area()/10000,3)}Ha, que equivale a un {round((intersect.Area()/10000)/(schema[0][1])*100,3)}%, con faja de retiro de la vía de primer orden Transversal Neiva - San Vicente"""
        bv = round((intersect.Area()/10000)/(schema[0][1])*100,3)
        area_bf = round(intersect.Area()/10000,3)
        
    else: 
        sheet['L40'] = f'NO X'

## URT 

lyr = driver.Open('/home/camilocorredor/DS_P/ETL/Layers/URT_Pol.shp') ## OK Capa
layer = lyr.GetLayer() 
    
for feature in layer:     
    geometry = feature.GetGeometryRef()
    intersect = geometry.Intersection(predio)
    inter_tf1 = geometry.Intersect(predio)

lyr = driver.Open('/home/camilocorredor/DS_P/ETL/Layers/URT_Pto.shp') ## OK Capa
layer = lyr.GetLayer() 
    
for feature in layer:     
    geometry = feature.GetGeometryRef()
    intersect = geometry.Intersection(predio)
    inter_tf2 = geometry.Intersect(predio)

if inter_tf1 == True and inter_tf2 == True or inter_tf1 == True and inter_tf2 == False or inter_tf1 == False and inter_tf2 == True:
    c_urt = f'presenta traslape'
else: 
    pass
if inter_tf1 == False and inter_tf2 == False:
    c_urt = f'NO presenta traslape'
else:
    pass

lyr = driver.Open('/home/camilocorredor/DS_P/ETL/Layers/Degradacion_suelo.shp') 
layer = lyr.GetLayer() 
    
for feature in layer:     
    geometry = feature.GetGeometryRef()
    intersect = geometry.Intersection(predio)
    inter_tf = geometry.Intersect(predio)
    if inter_tf == True:
        dse_p = round((intersect.Area()/10000)/(schema[0][1])*100,3)
        dse_a = round(intersect.Area()/10000,3)
    else: 
        pass

concepto = f"""Motivación del Concepto Técnico relacionado con continuar con el trámite de adjudicación o proceder a la negación de la solicitud: 
Concepto Topográfico: El área objeto de intervención se encuentra dentro del área del código predial {codigo} a nombre de la Nación denominado Baldío 
sin folio de matrícula inscrito en la base del IGAC, """
##Concepto cruce --all
if area_ds > 0:
    concepto = concepto + f'presenta cruce con drenaje sencillo en un área de {area_ds}m2 equivalentes al {ds}% del área de intervención'
else:
    concepto = concepto + f'NO presenta cruce con drenaje sencillo '
if p_zrc == 100:
    concepto = concepto + f'La zona en intervención se encuentra contenida 100% en la zona de reserva campesina del PATO BALSILLAS constituida bajo RESOLUCION 055 DE 18-12-1997,'
else:
    pass
if p_zrc < 100 and p_zrc > 0:
    concepto = concepto + f'La zona en intervención se encuentra parcialmente en la zona de reserva campesina del PATO BALSILLAS'
elif p_zrc == 0:
    concepto = concepto + f'La zona en intervención NO encuentra parcialmente en la zona de reserva campesina del PATO BALSILLAS'
    
if area_bf > 0:
    concepto = concepto + f' El predio objeto de estudio presenta traslape con faja de retiro de primer orden Transversal Neiva - San Vicente del Caguán en un área de {area_bf}m2, que equivale al {bv}% del área de intervención.'
else: 
    concepto = concepto + f' El predio objeto de estudio NO presenta traslape con faja de retiro de vías nacionales.'
if c_urt == 'presenta traslape':
    concepto = concepto + f' Se evidencia traslape frente a la capas geográficas de la Unidad de Restitución de Tierras'
else:
    concepto = concepto + f' NO se evidencia traslape frente a la capas geográficas de la Unidad de Restitución de Tierras'
if area_bos > 0:
    concepto = concepto + f' El área objeto de intervención presenta traslape con la capa cartográfica Bosques-2010 del IDEAM en un área de {area_bos}, que equivale al {ab}% del área de intervención'
else:
    concepto = concepto + f' El área objeto de intervención NO presenta traslape con la capa cartográfica Bosques-2010 del IDEAM'
if CR_A > 0: 
    concepto = concepto + f' el predio se encuentra ubicado la cuenca del {CR}, esto no afecta el trámite de formalización'
else:
    pass
if dse_a > 0:
    concepto = concepto + f' Dentro del área a formalizar se encuentra afectado por zonificación de degradación del suelo por erosión de tipo hídrico moderado en un {dse_p}% del área del predio, esto no afecta el tramite'

sheet['B53'] = concepto
archivo_excel.save('/home/camilocorredor/DS_P/ETL/Ejemplo1.xlsx')

FP = time.time()
print('Finaliza ITJP')
print(f'Tiempo de ejecución {round((FP-BP)/60,2)} minutos')
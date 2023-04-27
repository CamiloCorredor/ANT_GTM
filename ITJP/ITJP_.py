import time
from unicodedata import name
BP = time.time()
print('Iniciando ITJP ...')
from ctypes import c_char_p
from osgeo import ogr, osr

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

import pandas as pd

from num2words import num2words

from datetime import datetime

def intersect_layers_FA(path_layer, object_XTF,Field,Field_R): ##Return features y areas
    total_area = []
    layer = path_layer.GetLayer()
    for feature in layer:     
        geometry = feature.GetGeometryRef()
        intersect = geometry.Intersection(object_XTF)
        inter_tf = geometry.Intersect(object_XTF)
        if inter_tf == True and feature.GetField(Field) == Field_R:
            total_area.append(intersect.Area())
        else:              
            pass
        
    return sum(total_area)

def intersect_layers_FA_dif(path_layer, object_XTF,Field,Field_R): ##Return features y areas
    total_area = []
    layer = path_layer.GetLayer()
    for feature in layer:     
        geometry = feature.GetGeometryRef()
        intersect = geometry.Intersection(object_XTF)
        inter_tf = geometry.Intersect(object_XTF)
        if inter_tf == True and feature.GetField(Field) != Field_R:
            total_area.append(intersect.Area())
        else:              
            pass
        
    return sum(total_area)

    

def intersect_layers_F(path_layer, object_XTF,Field): ##Return features
    feature_intersects = []
    layer = path_layer.GetLayer()
    for feature in layer:     
        geometry = feature.GetGeometryRef()
        inter_tf = geometry.Intersect(object_XTF)
        if inter_tf == True:                
            feature_intersects.append(feature.GetField(Field))       
    else: 
        pass
    return feature_intersects

def intersect_layers_A(path_layer, object_XTF): ##Return Areas
    total_area = []
    layer = path_layer.GetLayer()
    for feature in layer:     
        geometry = feature.GetGeometryRef()
        intersect = geometry.Intersection(object_XTF)
        inter_tf = geometry.Intersect(object_XTF)
        if inter_tf == True:
            total_area.append(intersect.Area())     
       
    else: 
        pass
    return sum(total_area)

def sex_interesado(squema):
    sex_interesado = ''
    if squema == 'Femenino':
        sex_interesado = 'la interesada' 
    elif squema == 'Masculino':
        sex_interesado = 'el interesado' 
    elif squema == None:
        sex_interesado = 'los interesados'
    else:
        pass
    return sex_interesado

def cultivos(lis_t1, lis_t2):
    
    strg = ''
    cultivos = lis_t1 
    cultivos_ = cultivos.split(", ")
    cultivos_porc = lis_t2
    cultivos_porc_ = cultivos_porc.split(",")
    a = len(cultivos_)
    b = len(cultivos_porc_)

    for cultivos_, cultivos_porc_ in zip(cultivos_, cultivos_porc_):
        strg += f"{cultivos_} - {cultivos_porc_}%, "
    return strg
    
            
def def_uaf(object_XTF):
    range_UAF = [7.8383,10.639,15.3069,19.6939,33.8393,42.6454,66.1033,92.4583,103.2257,129.6417,264.8417,330.3617]
    range = []
    
    if object_XTF < range_UAF[0] and object_XTF < range_UAF[1]:
        
        range.append(range_UAF[0])
        range.append(range_UAF[1])
        range.append('café y frijol')
        if object_XTF <= range_UAF[1] and object_XTF >= range_UAF[0]:
            range.append('en el')
        elif object_XTF <= range_UAF[0]:
            range.append('por debajo del')
    
        var_dif = [abs(range_UAF[0]-object_XTF),abs(range_UAF[1]-object_XTF)]
        if var_dif[1] < var_dif[0]:
            range.append(round((object_XTF*2.5)/range_UAF[1],2))
        else:
            range.append(round((object_XTF*2.5)/range_UAF[0],2))      
    ##Café frijol

    elif object_XTF >= range_UAF[1] and object_XTF <= range_UAF[3]:
        
        range.append(range_UAF[2])
        range.append(range_UAF[3])
        range.append('frijol y maíz')
        if object_XTF <= range_UAF[3] and object_XTF >= range_UAF[2]:
            range.append('en el')
        elif object_XTF <= range_UAF[2] and object_XTF >= range_UAF[1]:
            range.append('por debajo del')
        
        var_dif = [abs(range_UAF[2]-object_XTF),abs(range_UAF[3]-object_XTF)]
        if var_dif[1] < var_dif[0]:
            range.append(round((object_XTF*2.5)/range_UAF[3],2))
        else:
            range.append(round((object_XTF*2.5)/range_UAF[2],2))
               ##FRijol - Maíz

    elif object_XTF >= range_UAF[3] and object_XTF <= range_UAF[5]:        
        range.append(range_UAF[4])
        range.append(range_UAF[5])
        range.append('caña y plátano')
        if object_XTF <= range_UAF[5] and object_XTF >= range_UAF[4]:
            range.append('en el')
        elif object_XTF <= range_UAF[4] and object_XTF >= range_UAF[3]:
            range.append('por debajo del')

        var_dif = [abs(range_UAF[4]-object_XTF),abs(range_UAF[5]-object_XTF)]
        if var_dif[1] < var_dif[0]:
            range.append(round((object_XTF*2.5)/range_UAF[5],2))
        else:
            range.append(round((object_XTF*2.5)/range_UAF[4],2))
        ##Caña - Plátano

    elif object_XTF >= range_UAF[5] and object_XTF <= range_UAF[7]:
        range.append(range_UAF[6])
        range.append(range_UAF[7])
        range.append('ganadería y maíz')
        if object_XTF <= range_UAF[7] and object_XTF >= range_UAF[6]:
            range.append('en el')
        elif object_XTF <= range_UAF[6] and object_XTF >= range_UAF[5]:
            range.append('por debajo del')
        var_dif = [abs(range_UAF[6]-object_XTF),abs(range_UAF[7]-object_XTF)]
        if var_dif[1] < var_dif[0]:
            range.append(round((object_XTF*2.5)/range_UAF[7],2))
        else:
            range.append(round((object_XTF*2.5)/range_UAF[6],2))
        ##Maiz Ganaderia
        
    elif object_XTF >= range_UAF[7] and object_XTF <= range_UAF[9]:
        range.append(range_UAF[8])
        range.append(range_UAF[9])
        range.append('ganadería de leche y ceba')
        if object_XTF <= range_UAF[9] and object_XTF >= range_UAF[8]:
            range.append('en el')
        elif object_XTF <= range_UAF[8] and object_XTF >= range_UAF[7]:
            range.append('por debajo del')

        var_dif = [abs(range_UAF[8]-object_XTF),abs(range_UAF[9]-object_XTF)]
        if var_dif[1] < var_dif[0]:
            range.append(round((object_XTF*2.5)/range_UAF[9],2))
        else:
            range.append(round((object_XTF*2.5)/range_UAF[8],2))
        ##Ganadería lechec y ganadería ceba

    elif object_XTF >= range_UAF[9] and object_XTF <= range_UAF[11] :
        range.append(range_UAF[10])
        range.append(range_UAF[11])
        range.append('ganadería extensiva')
        if object_XTF <= range_UAF[11] and object_XTF > range_UAF[10]:
            range.append('en el')
        elif object_XTF <= range_UAF[10] and object_XTF >= range_UAF[9]:
            range.append('por debajo del')
        var_dif = [abs(range_UAF[8]-object_XTF),abs(range_UAF[9]-object_XTF)]
        if var_dif[1] < var_dif[0]:
            range.append(round((object_XTF*2.5)/range_UAF[11],2))
        else:
            range.append(round((object_XTF*2.5)/range_UAF[10],2))
            ##GAnaderia extensiva
    else: 
        print('Sin clasificación')

    return range

def A_restricciones(list_lyrs, object_XTF):
    lyr_restricciones = []
    Sum_area = []
    
    for i in list_lyrs:
        if os.path.splitext(os.path.basename(i.GetName()))[0] == 'SOLICITUD_INGRESO_RTDAF':
            if intersect_layers_FA(i, predio,'estado_tra', 'Sentencia') > 0:
                lyr_restricciones.append(os.path.splitext(os.path.basename(i.GetName()))[0])
                Sum_area.append(intersect_layers_FA(i, predio,'estado_tra', 'Sentencia'))
            else:
                pass

        elif os.path.splitext(os.path.basename(i.GetName()))[0] == 'Drenaje_Sencillo_(30m)_':
            if intersect_layers_FA_dif(i,predio,'NOMBRE_GEO',None):
                lyr_restricciones.append(os.path.splitext(os.path.basename(i.GetName()))[0])
                Sum_area.append(intersect_layers_FA_dif(i,predio,'NOMBRE_GEO',None))
            else:
                pass
        elif intersect_layers_A(i,object_XTF) > 0:
            lyr_restricciones.append(os.path.splitext(os.path.basename(i.GetName()))[0])
            Sum_area.append(intersect_layers_A(i,object_XTF))

    Suma_area = sum(Sum_area)/10000

    if len(lyr_restricciones) > 0:
        AU = schema[0][1] - Suma_area
        strg = f"""cuenta con las siguientes restricciones ambientales o de Ley: {', '.join(lyr_restricciones[:-1]) + ' y ' + lyr_restricciones[-1]} \n \nAsí las cosas, se tiene que el área que se superpone con estas prohibiciones o restricciones legales corresponde a {(num2words(round((int(Suma_area))), lang = 'es')).upper()} HECTÁREAS {(num2words(round((float(Suma_area) - int(Suma_area))*10000,2), lang = 'es')).upper()} METROS CUADRADOS ({round((int(Suma_area)))}Ha + {round((float(Suma_area) - int(Suma_area))*10000,2)}m2). """
        strg = strg + f"""En virtud de estos traslapes no es posible la titulación del 100% del área solicitada, razón por la cual se descontaron las áreas antes descritas y se define un área útil de adjudicación correspondiente a {(num2words(round((int(AU))), lang = 'es')).upper()} HECTÁREAS {(num2words(round((float(AU) - int(AU))*10000,2), lang = 'es')).upper()} METROS CUADRADOS ({round((int(AU)))}Ha + {round((float(AU) - int(AU))*10000,2)}m2)."""
    else: 
        strg = 'NO cuenta con traslapes o restricciones ambientales de Ley'

    return Suma_area, strg

def names_interesados(schema):

    if schema[0][7] == None:
        str_name = f"solicitado por {sex_interesado(schemax[0][1])} {schema[0][2]}"
        str_all = str_name + f" con cédula de ciudadania No {schema[0][3]}"
    elif schema[0][7] == 'Grupo civil':
        str_name = f"solicitado por {sex_interesado(schemax[0][1])} {schemaxint[0][7]} y {schemaxint[1][7]}"
        str_all = str_name + f"identificados con cédula de ciudadania {schemaxint[0][6]} y {schemaxint[1][6]}, respectivamente"
    else: 
        print('Warning: Predio con > 2 solicitantes')
    
    return str_name, str_all

def condiciones(list):
    name_lyrs = []
    for i in list:
        name_lyrs.append(os.path.splitext(os.path.basename(i.GetName()))[0])
    
    if len(name_lyrs) > 1:
        string = ', '.join(name_lyrs[:-1]) + ' y ' + name_lyrs[-1]
    else:
        string = name_lyrs[0]
    return string 

ID = '5035000236'

juridico_pd = pd.read_excel('Source_Concepts/Juridico.xlsx')
ID_pred_ = juridico_pd.loc[juridico_pd['ID'] == int(ID)]
agronomia_pd = pd.read_excel('Source_Concepts/UAF.xlsx')
ID_pred = agronomia_pd.loc[agronomia_pd['ID'] == int(ID)]

date_ = datetime.strptime(str(ID_pred.iloc[0,7]), '%Y-%m-%d %H:%M:%S')
date = date_.strftime('%d/%m/%Y')

date_LV = datetime.strptime(str(ID_pred_.iloc[0,2]), '%Y-%m-%d %H:%M:%S')
date_LV = date_.strftime('%d/%m/%Y')

date_FA = datetime.strptime(str(ID_pred_.iloc[0,3]), '%Y-%m-%d %H:%M:%S')
date_FA = date_.strftime('%d/%m/%Y')

list_lyr = []
# ID_pred_ = np.array(ID_pred)
# print(ID_pred_.shape)
# print(type(ID_pred.iloc[0,3]))
# print(ID_pred.iloc[0,4])

connection = psycopg2.connect(
    host="localhost",
    database="ladm_ttsp",
    user="postgres",
    password="1234"
)

cursor = connection.cursor()
##                  0                                     1                              2                   3                 4                5                             6                       7
sql = f"""select P.id_operacion as QR, (st_area(T.geometria))/10000 as AREA_PRED, upper(I.nombre), I.documento_identidad, upper(P.nombre), T.geometria as geom, P.matricula_inmobiliaria as fmi, GIT.dispname as grupo_perso
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
left join rev_08.lc_datosadicionaleslevantamientocatastral as DA on P.t_id = DA.lc_predio 
left join rev_08.lc_categoriasuelotipo as CS on DA.categoria_suelo = CS.t_id 
left join rev_08.lc_destinacioneconomicatipo as DE on DA.destinacion_economica = DE.t_id
left join rev_08.lc_procedimientocatastralregistraltipo as PC on DA.procedimiento_catastral_registral = PC.t_id 
left join rev_08.lc_condicionprediotipo as CP on P.condicion_predio = CP.t_id 
left join rev_08.lc_prediotipo as PT on P.tipo = PT.t_id
where P.id_operacion = '{ID}'"""
cursor.execute(sql)
schema = cursor.fetchall()


sql_sex = f"""select P.id_operacion as QR, SX.dispname as sexo 
from rev_08.lc_predio as P
inner join rev_08.lc_terreno as T on P.id_operacion = T.etiqueta 
inner join rev_08.lc_derecho as D on P.t_id = D.unidad
inner join rev_08.lc_derechotipo as DT on D.tipo = DT.t_id 
left join rev_08.lc_interesado as I on D.interesado_lc_interesado = I.t_id
left join rev_08.lc_agrupacioninteresados as AGI on D.interesado_lc_agrupacioninteresados = AGI.t_id 
left join rev_08.col_grupointeresadotipo as GIT on AGI.tipo = GIT.t_id 
left join rev_08.lc_interesadodocumentotipo as IDT on I.tipo_documento = IDT.t_id
left join rev_08.lc_sexotipo as SX on I.sexo = SX.t_id 
where P.id_operacion = '{ID}' """
cursor.execute(sql_sex)
schemax = cursor.fetchall()

sql_int = f"""select P.id_operacion as QR, P.numero_predial, DT.dispname as derecho, P.codigo_orip ,
P.matricula_inmobiliaria as FMI, DIT.dispname ,I.documento_identidad , I.nombre 
from rev_08.lc_terreno as T
left join rev_08.lc_predio as P on T.etiqueta = P.local_id
left join rev_08.lc_derecho as D on P.t_id = D.unidad
left join rev_08.lc_derechotipo as DT on D.tipo = DT.t_id
left join rev_08.lc_agrupacioninteresados as AI on D.interesado_lc_agrupacioninteresados = AI.t_id
left join rev_08.col_miembros as CM on AI.t_id = CM.agrupacion 
left join rev_08.fraccion as F on CM.t_id = F.col_miembros_participacion 
left join rev_08.lc_interesado as I on CM.interesado_lc_interesado = I.t_id
left join rev_08.lc_interesadodocumentotipo as DIT on I.tipo_documento = DIT.t_id
where P.id_operacion = '{ID}'"""
cursor.execute(sql_int)
schemaxint = cursor.fetchall()

ITJP = openpyxl.load_workbook('ACCTI- F110 - ITJ EJ.xlsx')
sheet = ITJP['Hoja1']

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

# Nombre solicitante

if len(schemaxint) == 2:  
    sheet['B9'] = f"""Nombre solicitante: {schemaxint[0][7]}
Documento de identifcación: {schemaxint[0][6]}"""
    sheet['R9'] = f"""Nombre solicitante: {schemaxint[1][7]}
Documento de identifcación: {schemaxint[1][6]}"""
elif len(schema) == 1:
    sheet['B9'] = f"""Nombre solicitante: {schema[0][2]}
Documento de identificación: {schema[0][3]}"""
else:
    print('Warning: Predio con mas de dos interesados')
# Nombre del Predio
sheet['B19'] = f"""Nombre: {schema[0][4]}"""
# Area predio
sheet['F21'] = int(schema[0][1])
sheet['I21'] = round((float(schema[0][1]) - int(schema[0][1]))*10000,3)
# Cedula catastral 
# Cargar capa predial y realizar intersect AC21
driver = ogr.GetDriverByName('ESRI Shapefile')
lyr_condiciones = []
lyr_restricciones = []

lyr_dep = driver.Open('Layers/Departamentos.shp')
lyr_mun = driver.Open('Layers/Municipios.shp')

sheet['X19'] = f"""Municipio: {intersect_layers_F(lyr_dep, predio,'NOMBRE_DEP')[0]}"""
sheet['P19']= f"""Departamento: {intersect_layers_F(lyr_mun, predio,'NOMBRE_MUN')[0]}"""
sheet['B20'] = f"""Vereda o Fracción: {ID_pred.iloc[0,1].upper()}"""


lyr_Terreno = driver.Open('Layers/R_Terreno.shp') ##OK Capa
data = intersect_layers_F(lyr_Terreno, predio, 'codigo')
if len(data) > 1:        
    sheet['AC21'] = '\n'.join(data)
elif len(data) == 1:
    sheet['AC21'] = data[0]

#En el área solicitada se evidencian zonas de bosques

##Cuenca Rios
# lyr_CR = driver.Open('Layers/Cuenca_Rios.shp') ##OK Capa
# area_CR = intersect_layers_FA(lyr_CR, predio,'NOM_ZH')

# ZRC 
lyr_ZRC = driver.Open('Layers/ZRC_PB.shp') ##OK Capa
area_ZRC = intersect_layers_A(lyr_ZRC, predio)
if round(area_ZRC/10000,3) == round(schema[0][1],3):
    # p_zrc = round((intersect.Area()/10000)/(schema[0][1])*100,3)
    sheet['H36'] = "SI X"
    sheet['J36'] = f"""Zona de reserva campesina del Pato Balsillas"""
else: 
    sheet['I36'] = f'NO X'



#sheet['M34']
lyr_bosque = driver.Open('Layers/Bosques_.shp') ##OK Capa
lyr_condiciones.append(lyr_bosque)
area_bosques = intersect_layers_A(lyr_bosque, predio)
if area_bosques > 0:
    sheet['K34'] = "SI X"
    sheet['M34'] = f"""El predio presenta traslape con un área de {round(area_bosques/10000,3)}Ha, que equivale a un {round((area_bosques/10000)/(schema[0][1])*100,3)}%, con la capa cartográfica Bosques-2010 del IDEAM"""
   
else:
    sheet['L34'] = f'NO X'

# #Determinantes ambientales M35
lyr_ds = driver.Open('Layers/Drenaje_Sencillo_(30m)_.shp') ## ##Se debe agregar todas las capas (Excel). Por ahora solo cruza con DS
lyr_dd = driver.Open('Layers/DRENAJE_DOBLE.shp')
lyr_M35 = []
lyr_M35.append(lyr_ds)
# lyr_M35.append(lyr_dd)
for i in lyr_M35:

    a_0 = intersect_layers_FA(i, predio, 'NOMBRE_GEO', None) ##Iguales
    a_1 = intersect_layers_FA_dif(i, predio, 'NOMBRE_GEO', None) ##Diferentes
    if a_0 > 0 and a_1 > 0:
        ##and intersect_layers_FA(lyr_ds, predio, 'NOMBRE_GEO', None)[0] > 0:
        lyr_restricciones.append(i)
        lyr_condiciones.append(i)
        sheet['K35'] = "SI X"
        sheet['M35'] = f"""El predio presenta restricciones en un área de {round(a_1/10000,2)}Ha, que equivale a un {round((a_1/10000)/(schema[0][1])*100,2)}%. Adicionalmente, presenta condicionantes en un área de {round(a_0/10000,2)}Ha, que equivade a un {round((a_0/10000)/(schema[0][1])*100,2)}%, lo anterior en relación con la capa cartográfica {os.path.splitext(os.path.basename(i.GetName()))[0]}"""
        print(f"""El predio presenta restricciones en un área de {round(a_1/10000,2)}Ha, que equivale a un {round((a_1/10000)/(schema[0][1])*100,2)}%. Adicionalmente, presenta condicionantes en un área de {round(a_0/10000,2)}Ha, que equivade a un {round((a_0/10000)/(schema[0][1])*100,2)}%, lo anterior en relación con la capa cartográfica {os.path.splitext(os.path.basename(i.GetName()))[0]}""")
    elif a_1 > 0 and a_0 <= 0:
        lyr_restricciones.append(i)
        sheet['K35'] = "SI X"
        sheet['M35'] = f"""El predio presenta restricciones en un área de {round(a_1/10000,2)}Ha, que equivale a un {round((a_1/10000)/(schema[0][1])*100,2)}% en relación con la capa cartográfica {os.path.splitext(os.path.basename(i.GetName()))[0]}"""
        print('2')
    elif a_1 <= 0 and a_0 > 0:
        lyr_condiciones.append(i)
        sheet['K35'] = "SI X"
        sheet['M35'] = f"""El predio presenta condicionantes en un área de {round(a_0/10000,2)}Ha, que equivale a un {round((a_0/10000)/(schema[0][1])*100,2)}% en relación con la capa cartográfica {os.path.splitext(os.path.basename(i.GetName()))[0]}"""
        print('3')
        # ds = round((intersect.Area()/10000)/(schema[0][1])*100,3)
        # area_ds = round(intersect.Area()/10000,3)
    elif a_0 <= 0 and a_1 <= 0:
        sheet['L35'] = 'NO X'
        
    else: 
        pass       


#sheet['K37']
lyr_RTDAF = driver.Open('Layers/SOLICITUD_INGRESO_RTDAF.shp')

lyr_M37 = [] ##Se debe agregar todas las capas (Excel). Por ahora solo cruza con RTDAF
lyr_M37.append(lyr_RTDAF)
for i in lyr_M37:
    a = intersect_layers_FA(i, predio,'estado_tra', 'Sentencia')
    b = intersect_layers_FA_dif(i, predio,'estado_tra', 'Sentencia')
    if a > 0 and b > 0:
        lyr_restricciones.append(i)
        lyr_condiciones.append(i)
        sheet['K37'] = 'SI X'
        sheet['M37'] = f"""El predio presenta restricciones en un área de {round(a/10000,2)}Ha, que equivale a un {round((a/10000)/(schema[0][1])*100,2)}%. Adicionalmente, presenta condicionantes en un área de {round(b/10000,2)}Ha, que equivade a un {round((b/10000)/(schema[0][1])*100,2)}%, lo anterior en relación con la capa cartográfica {os.path.splitext(os.path.basename(i.GetName()))[0]}"""
        
    elif a > 0 and b <= 0:
        lyr_restricciones.append(i)
        sheet['K35'] = "SI X"
        sheet['M35'] = f"""El predio presenta restricciones en un área de {round(a/10000,2)}Ha, que equivale a un {round((a/10000)/(schema[0][1])*100,2)}% en relación con la capa cartográfica {os.path.splitext(os.path.basename(i.GetName()))[0]}"""
        
    elif a <= 0 and b > 0:
        lyr_condiciones.append(i)
        sheet['K35'] = "SI X"
        sheet['M35'] = f"""El predio presenta condicionantes en un área de {round(b/10000,2)}Ha, que equivale a un {round((b/10000)/(schema[0][1])*100,2)}% en relación con la capa cartográfica {os.path.splitext(os.path.basename(i.GetName()))[0]}"""
        
        # ds = round((intersect.Area()/10000)/(schema[0][1])*100,3)
        # area_ds = round(intersect.Area()/10000,3)
    elif a_0 <= 0 and a_1 <= 0:
        sheet['L35'] = 'NO X'
     
    else:
        sheet['L37'] = 'NO X'

print(A_restricciones(lyr_restricciones, predio))
    
# ##El predio se encuentra dentro del radio de inadjudicabilidad de zonas donde se adelanten explotaciones de recursos naturales no renovables        
sheet['M38'] ##Se debe agregar todas las capas (Excel). Por ahora solo cruza con 
sheet['L38'] = 'NO X'


lyr_PNN = driver.Open('Layers/Parque Nacional Natural.shp') ##Por ahora solo cruza con PNN
lyr_M39 = []
lyr_M39.append(lyr_PNN)
for i in lyr_M39:
    if intersect_layers_A(i,predio) > 0:
        lyr_restricciones.append(lyr_PNN)
        sheet['K39'] = 'SI X'
        sheet['M39'] = f"El predio objeto de estudio presenta restricciones en un área de {round(intersect_layers_A(i,predio),2)}m2 equivalente al {round((intersect_layers_A(i,predio)/10000)/schema[0][1]*100,2)}% del predio, con la capa cartográfica {os.path.splitext(os.path.basename(i.GetName()))[0]}"
    else:
        sheet['L39'] = 'NO X'

# ##Sheet40

# Cruce vias Buffer 
lyr_bv = driver.Open('Layers/Buffer_Vial.shp') ## Ok Capa
lyr_restricciones.append(lyr_bv)
area_bv = intersect_layers_A(lyr_bv, predio)

if area_bv > 0:
    sheet['K40'] = "SI X"
    sheet['M40'] = f"""El predio presenta traslape con un área de {round(area_bv/10000,2)}Ha, que equivale a un {round((area_bv/10000)/(schema[0][1])*100,2)}%, con faja de retiro de la vía de primer orden Transversal Neiva - San Vicente"""
    # bv = round((area_bv/10000)/(schema[0][1])*100,3)
    # area_bf = round(area_bv/10000,3)
  
else: 
    sheet['L40'] = f'NO X'

##Condicionante
lyr_ZM = driver.Open('Layers/ZONIFICACION_MANEJO.shp') ##Zonificación Manejo
lyr_condiciones.append(lyr_ZM) if intersect_layers_A(lyr_ZM, predio) > 0 else None

lyr_deg_s = driver.Open('Layers/Degradacion_suelo.shp') ##Degradación suelo
lyr_condiciones.append(lyr_deg_s) if intersect_layers_A(lyr_deg_s, predio) > 0 else None

lyr_ZSI = driver.Open('Layers/ZONAS_SUSCEPTIBLES_INUNDACION.shp') ##Zonas Susceptibles Inundación
lyr_condiciones.append(lyr_ZSI) if intersect_layers_A(lyr_ZSI, predio) > 0 else None

lyr_AFPC = driver.Open('Layers/UNIDAD_AGRICOLA_FAMILIAR_PROCESO_CONSTITUCION.shp')
lyr_condiciones.append(lyr_AFPC) if intersect_layers_A(lyr_AFPC, predio) > 0 else None

lyr_SMV = driver.Open('Layers/SOLICITU_MINERA_VIGENTE.shp')
lyr_condiciones.append(lyr_SMV) if intersect_layers_A(lyr_SMV, predio) > 0 else None

# lyr_l2 = driver.Open('Layers/Ley2.shp')
# lyr_condiciones.append(lyr_l2)

lyr_PSM = driver.Open('Layers/PREDIO_SIN_MATRICULA.shp')
lyr_condiciones.append(lyr_PSM) if intersect_layers_A(lyr_PSM, predio) > 0 else None

lyr_MTH = driver.Open('Layers/MAPA_TIERRAS_HIDROCARBUROS.shp')
lyr_condiciones.append(lyr_MTH) if intersect_layers_A(lyr_MTH, predio) > 0 else None

lyr_H = driver.Open('Layers/HUMEDAL.shp')
lyr_condiciones.append(lyr_H) if intersect_layers_A(lyr_H, predio) > 0 else None

lyr_HTMMP = driver.Open('Layers/HISTORICO_TITULO_MINERO_MUNICIPIO_PRIORIZADO.shp')
lyr_condiciones.append(lyr_HTMMP) if intersect_layers_A(lyr_HTMMP, predio) > 0 else None

lyr_HSMMP = driver.Open('Layers/HISTORICO_SOLICITUD_MINERA_MUNICIPIO_PRIORIZADO.shp')
lyr_condiciones.append(lyr_HSMMP) if intersect_layers_A(lyr_HSMMP, predio) > 0 else None

lyr_FA = driver.Open('Layers/FRONTERA_AGRICOLA.shp')
lyr_condiciones.append(lyr_FA) if intersect_layers_A(lyr_FA, predio) > 0 else None

lyr_ELTA = driver.Open('Layers/ESTADO_LEGAL_TERRITORIO_AMAZONICO.shp')
lyr_condiciones.append(lyr_ELTA) if intersect_layers_A(lyr_ELTA, predio) > 0 else None

lyr_CS = driver.Open('Layers/CORRELACION_SUELO.shp')
lyr_condiciones.append(lyr_CS) if intersect_layers_A(lyr_CS, predio) > 0 else None

lyr_CP = driver.Open('Layers/Centro_poblado.shp')
lyr_condiciones.append(lyr_CP) if intersect_layers_A(lyr_CP, predio) > 0 else None

lyr_BVMA = driver.Open('Layers/BUFFER_VICTIMA_MINA_ANTIPERSONA.shp')
lyr_condiciones.append(lyr_BVMA) if intersect_layers_A(lyr_BVMA, predio) > 0 else None

lyr_BEMA = driver.Open('Layers/BUFFER_EVENTO_MINA_ANTIPERSONA.shp')
lyr_condiciones.append(lyr_BEMA) if intersect_layers_A(lyr_BEMA, predio) > 0 else None

lyr_RM = driver.Open('Layers/remocion_en_masa.shp')
lyr_restricciones.append(lyr_RM)



con_catastral = f"""De acuerdo con la información recaudada a través del método indirecto de mesas colaborativas se determinó que el predio denominado {schema[0][4]}, ubicado en el departamento de {intersect_layers_F(lyr_dep, predio,'NOMBRE_DEP')[0]}, municipio de {intersect_layers_F(lyr_mun, predio,'NOMBRE_MUN')[0]}, vereda{ID_pred.iloc[0,1].upper()}, cuenta con un área según el plano topográfico de {(num2words(round((int(schema[0][1]))), lang = 'es')).upper()} HECTÁREAS {(num2words(round((float(schema[0][1]) - int(schema[0][1]))*10000,2), lang = 'es')).upper()} METROS CUADRADOS ({round((int(schema[0][1])))}Ha + {round((float(schema[0][1]) - int(schema[0][1]))*10000,2)}m2). Que el (dia) de mes de 2023, el grupo de topografía de la ANT, elaboró el cruce de información geográfica (F-007), y/o análisis espacial y cuya conclusión respecto del predio objeto de solicitud es que {A_restricciones(lyr_restricciones, predio)[1]} \n \nIgualmente, se informa que el predio denominado {schema[0][4]}, se traslapa con los siguientes componentes condicionantes:{condiciones(lyr_condiciones)}. Sin embargo, estas no afectan el área potencial y/o útil de titulación del predio."""
# print(con_catastral)

con_juridico = f"""Con fundamento en el marco normativo establecido en la Resolución No. 20230010000036 del 12 de abril de 2023 suscrita por la Dirección General de la Agencia Nacional de Tierras y mediante la cual se expidió el Reglamento Operativo de esta entidad, se procedió a la revisión jurídica del proceso de adjudicación de predio denominado {schema[0][4]} {names_interesados(schema)[1]}. 

Para todos los fines de este documento se comprende que los documentos, planos, soportes técnicos y /o oficios del caso que se relacionan a continuación fueron identificados y ubicados en el expediente No. {ID_pred_.iloc[0,1]} de los sistemas de información SIT y ORFEO de la Agencia Nacional de Tierras.

Evaluación de la naturaleza jurídica del predio (articulo 28, numeral 1 de Resolución 20230010000036 del 12 de abril de 2023)

Se ha verificado la siguiente información técnica indispensable para establecer la viabilidad de la adjudicación del predio {schema[0][4]} de acuerdo con lo ordenado en Resolución No. 20230010000036 del 12 de abril de 2023, articulo 13 que se integra por los componentes topográficos y agronómicos expresados así:

Respecto del levantamiento topográfico elaborado por el grupo de topografía del cooperante OEI del {date_LV}, realizado al predio denominado"{schema[0][4]}”, (numeral 5 del presente informe), 
se identificaron los siguientes elementos:

* Que tiene un área de {(num2words(round((int(schema[0][1]))), lang = 'es')).upper()} HECTÁREAS {(num2words(round((float(schema[0][1]) - int(schema[0][1]))*10000,2), lang = 'es')).upper()} METROS CUADRADOS ({round((int(schema[0][1])))}Ha + {round((float(schema[0][1]) - int(schema[0][1]))*10000,2)}m2),
* Que se encuentra ubicado en el municipio de {intersect_layers_F(lyr_mun, predio,'NOMBRE_MUN')[0]}, departamento de {intersect_layers_F(lyr_dep, predio,'NOMBRE_DEP')[0]}; 
* Que se identificaron cada uno de los linderos y colindancias del predio, contenidos en la Redacción Técnica de Linderos (F-009) de fecha (FALTA FECHA) 
* Que de acuerdo con el Cruce de Información Geográfica (F-007), el predio {A_restricciones(lyr_restricciones, predio)[1]}
* Igualmente, se evidenció que el predio denominado {schema[0][4]}, traslapa con los siguientes componentes condicionantes: {condiciones(lyr_condiciones)}. Sin embargo, estas no afectan el área de potencial y/o útil de titulación del predio.

Respecto del componente agronómico, mediante estudio de fecha {date_FA} realizado por grupo de agronomía de la SATDD, se estableció un rango de área para obtener entre 2 a 2.5 smmlv de {int(def_uaf(schema[0][1])[0])}Ha + {round((float(def_uaf(schema[0][1])[0]) - int(def_uaf(schema[0][1])[0]))*10000,3)}m2 a {int(def_uaf(schema[0][1])[1])}Ha + {round((float(def_uaf(schema[0][1])[1]) - int(def_uaf(schema[0][1])[1]))*10000,3)}, con la capacidad de producir {def_uaf(schema[0][1])[4]} smmlv, en la actualidad.

* Además, que el predio denominado {schema[0][4]}está siendo ocupado hace {num2words(ID_pred.iloc[0,2], lang = 'es')} ({ID_pred.iloc[0,2]}) años, por {sex_interesado(schemax[0][1])} de manera directa, que a su vez realiza una explotación con {cultivos(ID_pred.iloc[0,3], ID_pred.iloc[0,4])}. 
* Que el predio denominado “{schema[0][4]}” no presenta ninguna situación o condiciones que puedan poner en riesgo la integridad de {sex_interesado(schema[0][1])}, ni limitantes que afecten los recursos naturales, el medio ambiente, ni la zona productiva del predio; por tal razón, el grupo agronómico de la SATDD emitió concepto técnico (numeral 5 del presente informe) recomendando continuar con el proceso de adjudicación del predio. 

Revisión de requisitos subjetivos:

De conformidad con lo ordenado en el artículo 28, numeral 1º del Reglamento Operativo, se ha determinado la condición de poseedor y ocupante, estableciendo en este caso que {sex_interesado(schemax[0][1])} ocupa(n) el predio desde hace {num2words(ID_pred.iloc[0,2], lang = 'es')} {ID_pred.iloc[0,2]} años y ejerce(n) una explotación de {cultivos(ID_pred.iloc[0,3], ID_pred.iloc[0,4])}

Respecto de la información de cruces con bases de datos de los solicitantes, la Subdirección de Acceso a Tierras por Demanda y Descongestión – SATDD, solicitó a la Subdirección de Sistemas de Información de Tierras – SSIT mediante memorandos 20234200091813 del 31 de marzo de 2023 y 20234200106273 del 15 de abril de 2023, la valoración e inclusión en el RESO de {sex_interesado(schemax[0][1])}.

En consecuencia, la definición de inclusión ó no de los potenciales beneficiarios al RESO será confirmada con fundamento en estas valoraciones, es decir, si es procedente ó no la adjudicación del predio {schema[0][4]} a {sex_interesado(schemax[0][1])} en el informe técnico jurídico definitivo. Esta situación se establece con fundamento en el artículo 38 del Reglamento Operativo.

Se concluye entonces que la solicitud cumple con los requisitos objetivos para adjudicación del predio denominado {schema[0][4]} y en consecuencia, se comunica que es viable continuar con la etapa de apertura del trámite administrativo del Procedimiento Único de Reconocimiento de Derecho del predio {schema[0][4]}, ubicado en el municipio {intersect_layers_F(lyr_mun, predio,'NOMBRE_MUN')[0]}, departamento {intersect_layers_F(lyr_dep, predio,'NOMBRE_DEP')[0]} {names_interesados(schema)[0]} de conformidad con el artículo 32 de la Resolución 20230010000036 del 12 de abril de 2023.""" 
#print(con_juridico)

ITJP.save('/home/camilocorredor/DS_P/ETL/ITJP/Ejemplo1.xlsx')

FP = time.time()
print('Finaliza ITJP')
print(f'Tiempo de ejecución {round((FP-BP)/60,2)} minutos')
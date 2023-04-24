from pickle import OBJ
import time
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

def intersect_layers_FA(path_layer, object_XTF,Field): ##Return features y areas
    total_area = []
    feature_intersects = []
    layer = path_layer.GetLayer()
    for feature in layer:     
        geometry = feature.GetGeometryRef()
        intersect = geometry.Intersection(object_XTF)
        inter_tf = geometry.Intersect(object_XTF)
        if inter_tf == True:
        
            total_area.append(intersect.Area())
            feature_intersects.append(feature.GetField(Field))       
    else: 
        pass
    return sum(total_area), feature_intersects

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
        sex_interesado = 'la' 
    elif squema == 'Masculino':
        sex_interesado = 'el' 
    elif squema == None:
        sex_interesado = 'los'
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
        if intersect_layers_A(i,object_XTF) > 0:
            Sum_area.append(intersect_layers_A(i,predio))
            lyr_restricciones.append(os.path.splitext(os.path.basename(i.GetName()))[0])

    Suma_area = sum(Sum_area)/10000

    if len(lyr_restricciones) > 0:
        AU = schema[0][1] - Suma_area

        strg = f"""cuenta con los siguientes traslapes con restricciones ambientales o de Ley: {', '.join(lyr_restricciones[:-1]) + ' y ' + lyr_restricciones[-1]} \n \n 
        Así las cosas, se tiene que el área que se superpone con estas prohibiciones o restricciones legales corresponde a 
        {(num2words(round((int(Suma_area))), lang = 'es')).upper()} HECTÁREAS 
        {(num2words(round((float(Suma_area) - int(Suma_area))*10000,2), lang = 'es')).upper()} METROS CUADRADOS ({round((int(Suma_area)))}Ha + 
        {round((float(Suma_area) - int(Suma_area))*10000,2)}m2)"""

        strg =  strg + f"""En virtud de estos traslapes no es posible la titulación del 100% del área solicitada, razón por la cual se descontaron las áreas antes descritas 
        y se define un área útil de adjudicación correspondiente a {(num2words(round((int(AU))), lang = 'es')).upper()} HECTÁREAS 
        {(num2words(round((float(AU) - int(AU))*10000,2), lang = 'es')).upper()} METROS CUADRADOS ({round((int(AU)))}Ha + 
        {round((float(AU) - int(AU))*10000,2)}m2) """

    else: 
        strg = 'NO cuenta con traslapes o restricciones ambientales de Ley'

    return Suma_area, strg

ID = '1875300610'
agronomia_pd = pd.read_excel('Source_Concepts/UAF.xlsx')
ID_pred = agronomia_pd.loc[agronomia_pd['ID'] == int(ID)]

date_ = datetime.strptime(str(ID_pred.iloc[0,7]), '%Y-%m-%d %H:%M:%S')
date = date_.strftime('%d/%m/%Y')

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
##                  0                                     1                              2                   3                 4                5 
sql = f"""select P.id_operacion as QR, (st_area(T.geometria))/10000 as AREA_PRED, upper(I.nombre), I.documento_identidad, upper(P.nombre), T.geometria as geom, 
P.matricula_inmobiliaria as fmi 
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
print(len(schema))
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
#Nombre del Predio
# sheet['B19'] = f"""Nombre: {schema[0][4]}"""
#Area predio
# sheet['F21'] = int(schema[0][1])
# sheet['I21'] = round((float(schema[0][1]) - int(schema[0][1]))*10000,3)
#Cedula catastral 
#Cargar capa predial y realizar intersect AC21
driver = ogr.GetDriverByName('ESRI Shapefile')

lyr_dep = driver.Open('Layers/Departamentos.shp')
lyr_mun = driver.Open('Layers/Municipios.shp')

sheet['X19'] = f"""Municipio: {intersect_layers_F(lyr_dep, predio,'NOMBRE_DEP')[0]}"""
sheet['P19']= f"""Departamento: {intersect_layers_F(lyr_mun, predio,'NOMBRE_MUN')[0]}"""
sheet['B20'] = f"""Vereda o Fracción: {ID_pred.iloc[0,1].upper()}"""


# lyr_Terreno = driver.Open('Layers/R_Terreno.shp') ##OK Capa
# data = intersect_layers_F(lyr_Terreno, predio, 'codigo')
# if len(data) > 1:        
#     sheet['AC21'] = '\n'.join(data)
# elif len(data) == 1:
#     sheet['AC21'] = data[0]

#En el área solicitada se evidencian zonas de bosques
# lyr_bosque = driver.Open('Layers/Bosques_.shp') ##OK Capa
# area_bosques = intersect_layers_A(lyr_bosque, predio)
# if area_bosques > 0:
#     sheet['K34'] = "SI X"
#     sheet['M34'] = f"""El predio presenta traslape con un área de {round(area_bosques/10000,3)}Ha, que equivale a un {round((area_bosques/10000)/(schema[0][1])*100,3)}%, con la capa cartográfica Bosques-2010 del IDEAM"""
#     porc_bos = round((area_bosques/10000)/(schema[0][1])*100,3)
    
# else:
#     sheet['L34'] = f'NO X'


#Determinantes ambientales
# lyr_ds = driver.Open('Layers/Drenaje_Sencillo_(30m)_.shp') ## OK
# area_ds = intersect_layers_A(lyr_ds, predio)
# if area_ds > 0:
#     sheet['K35'] = "SI X"
#     sheet['M35'] = f"""El predio presenta traslape con un área de {round(area_ds/10000,3)}Ha, que equivade a un {round((area_ds/10000)/(schema[0][1])*100,3)}%, con la capa de drenaje simple y franjas de retiro de 30 metros de acuerdo con la normatividad vigente"""
#         # ds = round((intersect.Area()/10000)/(schema[0][1])*100,3)
#         # area_ds = round(intersect.Area()/10000,3)
# else:
#     sheet['L35'] = 'NO X'

##Cuenca Rios
# lyr_CR = driver.Open('Layers/Cuenca_Rios.shp') ##OK Capa
# area_CR = intersect_layers_FA(lyr_CR, predio,'NOM_ZH')

# ZRC 
# lyr_ZRC = driver.Open('Layers/ZRC_PB.shp') ##OK Capa
# area_ZRC = intersect_layers_A(lyr_ZRC, predio)
# if round(area_ZRC/10000,3) == round(schema[0][1],3):
#     # p_zrc = round((intersect.Area()/10000)/(schema[0][1])*100,3)
#     sheet['H36'] = "SI X"
#     sheet['J36'] = f"""Zona de reserva campesina del Pato Balsillas"""
# else: 
#     sheet['I36'] = f'NO X'



# URT 

# lyr_URT_Pol = driver.Open('Layers/URT_Pol.shp') ## OK Capa
# features_URT_Pol = intersect_layers_F(lyr_URT_Pol, predio, 'estado_tra')

# lyr_URT_Pto = driver.Open('Layers/URT_Pto.shp') ## OK Capa
# features_URT_Pto = intersect_layers_F(lyr_URT_Pto, predio, 'estado_tra')

# if len(features_URT_Pol) > 0 and len(features_URT_Pto) > 0 or len(features_URT_Pol) > 0 and len(features_URT_Pto) == 0 or len(features_URT_Pol) == 0 and len(features_URT_Pto) > 0:
#     c_urt = f'presenta traslape'
# else: 
#     pass
# if len(features_URT_Pto) == 0 and len(features_URT_Pol) == 0:
#     c_urt = f'NO presenta traslape'
# else:
#     pass

# print(c_urt)

# lyr_deg_s = driver.Open('Layers/Degradacion_suelo.shp') 
# area_deg_s = intersect_layers_A(lyr_deg_s, predio)

# if area_deg_s == True:
#     dse_p = round((area_deg_s/10000)/(schema[0][1])*100,3)
#     dse_a = round(area_deg_s/10000,3)
# else: 
#     pass

list_lyr = []
#sheet['K37']
lyr_RTDAF = driver.Open('Layers/SOLICITUD_INGRESO_RTDAF.shp')
list_lyr.append(lyr_RTDAF)
lyr_M37 = []
lyr_M37.append(lyr_RTDAF)
for i in lyr_M37:
    if intersect_layers_A(i,predio) > 0:
        sheet['K37'] = 'SI X'
        sheet['M37'] = f"El predio objeto de estudio se ve afectado en un área de {round(intersect_layers_A(i,predio),2)}m2 equivalente al {round((intersect_layers_A(i,predio)/10000)/schema[0][1]*100,2)}% con la capa cartográfica {os.path.splitext(os.path.basename(i.GetName()))[0]}"
    else:
        sheet['L37'] = 'NO X'


#Sheet['M38']
sheet['L38'] = 'NO X'

##El predio se encuentra dentro del radio de inadjudicabilidad de zonas donde se adelanten explotaciones de recursos naturales no renovables

lyr_PNN = driver.Open('Layers/Parque Nacional Natural.shp')
list_lyr.append(lyr_PNN)
lyr_M39 = []
lyr_M39.append(lyr_PNN)
for i in lyr_M39:
    if intersect_layers_A(i,predio) > 0:
        sheet['K39'] = 'SI X'
        sheet['M39'] = f"El predio objeto de estudio se ve afectado en un área de {round(intersect_layers_A(i,predio),2)}m2 equivalente al {round((intersect_layers_A(i,predio)/10000)/schema[0][1]*100,2)}% con la capa cartográfica {os.path.splitext(os.path.basename(i.GetName()))[0]}"
    else:
        sheet['L39'] = 'NO X'

##Sheet40

#Cruce vias Buffer 
lyr_bv = driver.Open('Layers/Buffer_Vial.shp') ## Ok Capa
list_lyr.append(lyr_bv)
area_bv = intersect_layers_A(lyr_bv, predio)

if area_bv > 0:
    sheet['K40'] = "SI X"
    sheet['M40'] = f"""El predio presenta traslape con un área de {round(area_bv/10000,3)}Ha, que equivale a un {round((area_bv/10000)/(schema[0][1])*100,3)}%, con faja de retiro de la vía de primer orden Transversal Neiva - San Vicente"""
    # bv = round((area_bv/10000)/(schema[0][1])*100,3)
    # area_bf = round(area_bv/10000,3)
  
else: 
    sheet['L40'] = f'NO X'




# lyr_RTDAF = driver.Open('Layers/SOLICITUD_INGRESO_RTDAF.shp')
# list_lyr.append(lyr_RTDAF)


con_catastral = f"""De acuerdo con la información recaudada a través del método indirecto de mesas colaborativas se determinó que el predio denominado {schema[0][4]}, 
ubicado en el departamento de {intersect_layers_F(lyr_dep, predio,'NOMBRE_DEP')[0]}, municipio de {intersect_layers_F(lyr_mun, predio,'NOMBRE_MUN')[0]}, vereda {ID_pred.iloc[0,1].upper()},
cuenta con un área según el plano topográfico de {(num2words(round((int(schema[0][1]))), lang = 'es')).upper()} HECTÁREAS 
 {(num2words(round((float(schema[0][1]) - int(schema[0][1]))*10000,2), lang = 'es')).upper()} METROS CUADRADOS ({round((int(schema[0][1])))}Ha + 
 {round((float(schema[0][1]) - int(schema[0][1]))*10000,2)}m2). Que el (dia) de mes de 2023, 
el grupo de topografía de la ANT, elaboró el cruce de información geográfica (F-007), y/o análisis espacial y cuya conclusión respecto del predio objeto de solicitud
es que {A_restricciones(list_lyr, predio)[1]}

Igualmente, se informa que el predio denominado {schema[0][4]}, se traslapa con los siguientes componente condicionantes:
 *Condicionante1, Condicionante2, … , Condicionante.*. Sin embargo, estas no afectan el área de potencial y/o útil de titulación del predio.   """

print(con_catastral)


# con_agronomia = f"""De acuerdo a la información recaudada a través del método indirecto de mesas colaborativas, se determinó que para la zona donde está ubicado el predio, se presenta un régimen de lluvias monomodal y condiciones de suelos con textura mayormente arcillosa y ph  fuertemente ácidos, bajos contenidos de materia orgánica y condiciones productivas aptas para determinados cultivos y ganadería bovina y bufalina. \n \nAdemás, se tiene que el predio denominado {schema[0][4]}, ubicado en el departamento de {intersect_layers_F(lyr_dep, predio,'NOMBRE_DEP')[0]}, municipio de {intersect_layers_F(lyr_mun, predio,'NOMBRE_MUN')[0]}, vereda {ID_pred.iloc[0,1].upper()},cuenta con un área según el plano topográfico de {(num2words(round((int(schema[0][1]))), lang = 'es')).upper()} HECTÁREAS {(num2words(round((float(schema[0][1]) - int(schema[0][1]))*10000,2), lang = 'es')).upper()} METROS CUADRADOS ({round((int(schema[0][1])))}Ha + {round((float(schema[0][1]) - int(schema[0][1]))*10000,2)}m2), el cual está siendo ocupado hace {ID_pred.iloc[0,2]} años, por {sex_interesado(schemax[0][1])} solicitante de manera directa, que a su vez realiza una explotación de {cultivos(ID_pred.iloc[0,3], ID_pred.iloc[0,4])}. \n \nSegún la inspección ocular realizada (Formato ANT - ACCTI-F-116), realizada el {date}, en el predio no se evidencia ningún tipo de situaciones de riesgo o condiciones tales como remociones en masa de tierra, crecientes súbitas o pendientes mayores a 45° que representen peligro para la integridad de {sex_interesado(schemax[0][1])} ocupantes. \n \nDesde el componente ambiental no se observan limitantes que afecten los recursos naturales, el medio ambiente ni la zona productiva del predio. \n \nBajo estas condiciones, el grupo de Agronomía a cargo de esta evaluación determinó el cálculo de UAF con propuesta de producción de {def_uaf(schema[0][1])[2]}. Resultado de esta propuesta se estableció un rango de área para obtener entre 2 a 2.5 smmlv de {int(def_uaf(schema[0][1])[0])}Ha + {round((float(def_uaf(schema[0][1])[0]) - int(def_uaf(schema[0][1])[0]))*10000,3)}m2 a {int(def_uaf(schema[0][1])[1])}Ha + {round((float(def_uaf(schema[0][1])[1]) - int(def_uaf(schema[0][1])[1]))*10000,3)}. Con lo anterior, se establece que el predio está {def_uaf(schema[0][1])[3]} rango de la UAF mencionada, con la capacidad de producir {def_uaf(schema[0][1])[4]} smmlv, en la actualidad. \n \nEn consecuencia, de lo explicado anteriormente, desde el componente agronómico de la Subdirección de Acceso a Tierras por Demanda y Descongestión se recomienda continuar con el proceso de adjudicación del predio. """
# sheet['L51'] = con_agronomia

# concepto = f"""Motivación del Concepto Técnico relacionado con continuar con el trámite de adjudicación o proceder a la negación de la solicitud: 
# Concepto Topográfico: El área objeto de intervención se encuentra dentro del área del código predial {codigo} a nombre de la Nación denominado Baldío 
# sin folio de matrícula inscrito en la base del IGAC, """
# ##Concepto cruce --all
# if area_ds > 0:
#     concepto = concepto + f'presenta cruce con drenaje sencillo en un área de {area_ds}m2 equivalentes al {ds}% del área de intervención'
# else:
#     concepto = concepto + f'NO presenta cruce con drenaje sencillo '
# if p_zrc == 100:
#     concepto = concepto + f'La zona en intervención se encuentra contenida 100% en la zona de reserva campesina del PATO BALSILLAS constituida bajo RESOLUCION 055 DE 18-12-1997,'
# else:
#     pass
# if p_zrc < 100 and p_zrc > 0:
#     concepto = concepto + f'La zona en intervención se encuentra parcialmente en la zona de reserva campesina del PATO BALSILLAS'
# elif p_zrc == 0:
#     concepto = concepto + f'La zona en intervención NO encuentra parcialmente en la zona de reserva campesina del PATO BALSILLAS'
    
# if area_bf > 0:
#     concepto = concepto + f' El predio objeto de estudio presenta traslape con faja de retiro de primer orden Transversal Neiva - San Vicente del Caguán en un área de {area_bf}m2, que equivale al {bv}% del área de intervención.'
# else: 
#     concepto = concepto + f' El predio objeto de estudio NO presenta traslape con faja de retiro de vías nacionales.'
# if c_urt == 'presenta traslape':
#     concepto = concepto + f' Se evidencia traslape frente a la capas geográficas de la Unidad de Restitución de Tierras'
# else:
#     concepto = concepto + f' NO se evidencia traslape frente a la capas geográficas de la Unidad de Restitución de Tierras'
# if area_bos > 0:
#     concepto = concepto + f' El área objeto de intervención presenta traslape con la capa cartográfica Bosques-2010 del IDEAM en un área de {area_bos}, que equivale al {ab}% del área de intervención'
# else:
#     concepto = concepto + f' El área objeto de intervención NO presenta traslape con la capa cartográfica Bosques-2010 del IDEAM'
# if CR_A > 0: 
#     concepto = concepto + f' el predio se encuentra ubicado la cuenca del {CR}, esto no afecta el trámite de formalización'
# else:
#     pass
# if dse_a > 0:
#     concepto = concepto + f' Dentro del área a formalizar se encuentra afectado por zonificación de degradación del suelo por erosión de tipo hídrico moderado en un {dse_p}% del área del predio, esto no afecta el tramite'

# sheet['B53'] = concepto
ITJP.save('/home/camilocorredor/DS_P/ETL/ITJP/Ejemplo1.xlsx')

FP = time.time()
print('Finaliza ITJP')
print(f'Tiempo de ejecución {round((FP-BP)/60,2)} minutos')
import time
BP = time.time()
print('Iniciando ITJP ...')
from ctypes import c_char_p
from osgeo import ogr, osr
import osgeo.ogr
import shapely.wkb
from shapely.geometry import Polygon

import openpyxl
import os
os.environ['USE_PYGEOS'] = '0'
import geopandas as gpd



from shapely.wkb import loads
from shapely import wkb
import os

import binascii
import matplotlib.pyplot as plt

import pandas as pd
import json

with open('paths.json') as file:
    # Load the JSON data
    data = json.load(file)

from datetime import datetime

from OP_geographic import OP_geographic

from interesado import interesado

from SQL_LADM import SQL_LADM

from Agricola import agricola

from BIP import BIP



# vector_ID =['5035000202', '5035000322', '5035010566']



vector_ID = ['5035010005']

for ID in vector_ID:

    object_agronomia = BIP(data[1]["UAF"], ID)
    object_juridico = BIP(data[1]["agronomia"], ID)
    
    
    print(f'Informe Técnico Jurídico Preliminar {ID}')
    # ID = input('Ingrese ID del predio: ')
    ITJP = openpyxl.load_workbook(data[1]["path_xlsx"])
    

    juridico = pd.read_excel(data[1]["juridico"])
    ID_pred_ = juridico.loc[juridico['ID'] == int(ID)]
    agronomia_pd = pd.read_excel('Source_Concepts/UAF.xlsx')
    ID_pred = agronomia_pd.loc[agronomia_pd['ID'] == int(ID)]


    date_ = datetime.strptime(str(ID_pred.iloc[0,7]), '%Y-%m-%d %H:%M:%S')
    date = date_.strftime('%d/%m/%Y')

    from datetime import datetime, timedelta
    excel_start_date = datetime(1900, 1, 1)
    date_ = int(ID_pred_.iloc[0,2])
    delta = timedelta(days = date_)
    date_ = excel_start_date + delta 
    date_LV = date_.strftime('%d/%m/%Y')

    date_ = datetime.strptime(str(ID_pred_.iloc[0,3]), '%Y-%m-%d %H:%M:%S')
    date_FA = date_.strftime('%d/%m/%Y')

    date_ = datetime.strptime(str(ID_pred_.iloc[0,6]), '%Y-%m-%d %H:%M:%S')
    date_F007 = date_.strftime('%d/%m/%Y')


    list_lyr = []
    # ID_pred_ = np.array(ID_pred)
    # print(ID_pred_.shape)
    # print(type(ID_pred.iloc[0,3]))
    # print(ID_pred.iloc[0,4])
    SQL = SQL_LADM("localhost", "ladm_ttsp", "postgres", "1234","5035010016")
    # resultado = SQL.exe_sql()
    # print(resultado)
    # resultado = SQL.exe_sql_1()
    # print(resultado)
    # resultado = SQL.exe_sql_2()
    # print(resultado)
    
    sheet = ITJP['Hoja1']

    spatial_reference = osr.SpatialReference()
    spatial_reference.ImportFromEPSG(9377)

    shapely_obj = shapely.wkb.loads(SQL.exe_sql()[0][5])
    predio = ogr.CreateGeometryFromWkt(shapely_obj.wkt)
    predio.AssignSpatialReference(spatial_reference)
    #geometry = loads(wkb)
    
    # Nombre solicitante

    # resultado = SQL.exe_sql_2()
    # print(len(resultado))
    # if len(resultado) == 2:  
    #     sheet['B9'] = f"""Nombre solicitante: {SQL.exe_sql_2()[0][7]}
    # Documento de identifcación: {SQL.exe_sql_2()[0][6]}"""
    #     sheet['R9'] = f"""Nombre solicitante: {SQL.exe_sql_2()[1][7]}
    # Documento de identifcación: {SQL.exe_sql_2()[1][6]}"""
    # elif len(SQL.exe_sql_2()) == 1:
    #     sheet['B9'] = f"""Nombre solicitante: {SQL.exe_sql_2()[0][2]}
    # Documento de identificación: {SQL.exe_sql_2()[0][3]}"""
    # else:
    #     print('Warning: Predio > 2 interesados')
    # # Nombre del Predio
    # sheet['B19'] = f"""Nombre: {schema[0][4]}"""
    # # Area predio
    # sheet['F21'] = int(schema[0][1])
    # sheet['I21'] = round((float(schema[0][1]) - int(schema[0][1]))*10000,3)
    # # Cedula catastral 
    # # Cargar capa predial y realizar intersect AC21
    # driver = ogr.GetDriverByName('ESRI Shapefile')
    # lyr_condiciones = []
    # lyr_restricciones = []

    # lyr_dep = driver.Open('Layers/Departamentos.shp')
    # driver = ogr.GetDriverByName('ESRI Shapefile')
    # lyr_mun = driver.Open('Layers/Municipios.shp')

    # sheet['X19'] = f"""Municipio: {intersect_layers_F(lyr_dep, predio,'NOMBRE_DEP')[0]}"""
    # sheet['P19']= f"""Departamento: {intersect_layers_F(lyr_mun, predio,'NOMBRE_MUN')[0]}"""
    # sheet['B20'] = f"""Vereda o Fracción: {ID_pred.iloc[0,1].upper()}"""


    # lyr_Terreno = driver.Open('Layers/R_Terreno.shp') ##OK Capa
    # data = intersect_layers_F(lyr_Terreno, predio, 'codigo')
    # if len(data) > 1:        
    #     sheet['AC21'] = '\n'.join(data)
    # elif len(data) == 1:
    #     sheet['AC21'] = data[0]

    # #En el área solicitada se evidencian zonas de bosques

    # ##Cuenca Rios
    # # lyr_CR = driver.Open('Layers/Cuenca_Rios.shp') ##OK Capa
    # # area_CR = intersect_layers_FA(lyr_CR, predio,'NOM_ZH')

    # # ZRC 
    # lyr_ZRC = driver.Open('Layers/ZRC_PB.shp') ##OK Capa
    # area_ZRC = intersect_layers_A(lyr_ZRC, predio)[0]
    # if round(area_ZRC/10000,3) == round(schema[0][1],3):
    #     # p_zrc = round((intersect.Area()/10000)/(schema[0][1])*100,3)
    #     lyr_condiciones.append(lyr_ZRC)
    #     sheet['H36'] = "SI X"
    #     sheet['J36'] = f"""Zona de reserva campesina del Pato Balsillas"""
    # else: 
    #     sheet['I36'] = f'NO X'



    # #sheet['M34']
    # lyr_bosque = driver.Open('Layers/bosques.shp') ##OK Capa
    # lyr_condiciones.append(lyr_bosque)
    # area_bosques = intersect_layers_A(lyr_bosque, predio)[0]
    # if area_bosques > 0:
    #     sheet['K34'] = "SI X"
    #     sheet['M34'] = f"""El predio presenta traslape con un área de {round(area_bosques/10000,3)}Ha, que equivale a un {round((area_bosques/10000)/(schema[0][1])*100,3)}%, con la capa cartográfica Bosques-2010 del IDEAM"""
    
    # else:
    #     sheet['L34'] = f'NO X'

    # # #Determinantes ambientales M35
    # lyr_ds = driver.Open('Layers/Drenaje_Sencillo_(30m)_.shp') ## ##Se debe agregar todas las capas (Excel). Por ahora solo cruza con DS
    # lyr_dd = driver.Open('Layers/DRENAJE_DOBLE.shp')
    # lyr_M35 = []
    # lyr_M35.append(lyr_ds)
    # lyr_M35.append(lyr_dd)
    # strng = ''
    # for i in lyr_M35:



    #     a_0 = intersect_layers_FA(i, predio, 'NOMBRE_GEO', None)[0] ##Iguales
    #     a_1 = intersect_layers_FA_dif(i, predio, 'NOMBRE_GEO', None)[0] ##Diferentes
    #     if a_0 > 0 and a_1 > 0:
    #         ##and intersect_layers_FA(lyr_ds, predio, 'NOMBRE_GEO', None)[0] > 0:
    #         lyr_restricciones.append(i)
    #         lyr_condiciones.append(i)
    #         sheet['K35'] = "SI X"
    #         sheet['M35'] = f""""""
    #         strng = strng + f'El predio presenta restricciones en un área de {round(a_1/10000,2)}Ha, que equivale a un {round((a_1/10000)/(schema[0][1])*100,2)}%. Adicionalmente, presenta condicionantes en un área de {round(a_0/10000,2)}Ha, que equivade a un {round((a_0/10000)/(schema[0][1])*100,2)}%, lo anterior en relación con la capa cartográfica {os.path.splitext(os.path.basename(i.GetName()))[0]}'
    #         sheet['M35'] = strng
    #         # print(f"""El predio presenta restricciones en un área de {round(a_1/10000,2)}Ha, que equivale a un {round((a_1/10000)/(schema[0][1])*100,2)}%. Adicionalmente, presenta condicionantes en un área de {round(a_0/10000,2)}Ha, que equivade a un {round((a_0/10000)/(schema[0][1])*100,2)}%, lo anterior en relación con la capa cartográfica {os.path.splitext(os.path.basename(i.GetName()))[0]}""")
    #     elif a_1 > 0 and a_0 <= 0:
    #         lyr_restricciones.append(i)
    #         sheet['K35'] = "SI X"
    #         strng = strng + f"""El predio presenta restricciones en un área de {round(a_1/10000,2)}Ha, que equivale a un {round((a_1/10000)/(schema[0][1])*100,2)}% en relación con la capa cartográfica {os.path.splitext(os.path.basename(i.GetName()))[0]}"""
    #         sheet['M35'] = strng

    #     elif a_1 <= 0 and a_0 > 0:
    #         lyr_condiciones.append(i)
    #         sheet['K35'] = "SI X"
    #         strng = strng + f"""El predio presenta condicionantes en un área de {round(a_0/10000,2)}Ha, que equivale a un {round((a_0/10000)/(schema[0][1])*100,2)}% en relación con la capa cartográfica {os.path.splitext(os.path.basename(i.GetName()))[0]}"""
    #         sheet['M35'] = strng


    #         # ds = round((intersect.Area()/10000)/(schema[0][1])*100,3)
    #         # area_ds = round(intersect.Area()/10000,3)
    #     elif a_0 <= 0 and a_1 <= 0:
    #         sheet['L35'] = 'NO X'
    #         sheet['M35'] = ' '

    #     else: 
    #         pass       


    # #sheet['K37']
    # lyr_RTDAF = driver.Open('Layers/SOLICITUD_INGRESO_RTDAF.shp')

    # lyr_M37 = [] ##Se debe agregar todas las capas (Excel). Por ahora solo cruza con RTDAF
    # lyr_M37.append(lyr_RTDAF)
    # for i in lyr_M37:
    #     a = intersect_layers_FA(i, predio,'estado_tra', 'Sentencia')[0]
    #     b = intersect_layers_FA_dif(i, predio,'estado_tra', 'Sentencia')[0]
    #     if a > 0 and b > 0:
    #         lyr_restricciones.append(i)
    #         lyr_condiciones.append(i)
    #         sheet['K37'] = 'SI X'
    #         sheet['M37'] = f"""El predio presenta restricciones en un área de {round(a/10000,2)}Ha, que equivale a un {round((a/10000)/(schema[0][1])*100,2)}%. Adicionalmente, presenta condicionantes en un área de {round(b/10000,2)}Ha, que equivade a un {round((b/10000)/(schema[0][1])*100,2)}%, lo anterior en relación con la capa cartográfica {os.path.splitext(os.path.basename(i.GetName()))[0]}"""

    #     elif a > 0 and b <= 0:
    #         lyr_restricciones.append(i)
    #         sheet['K37'] = "SI X"
    #         sheet['M37'] = f"""El predio presenta restricciones en un área de {round(a/10000,2)}Ha, que equivale a un {round((a/10000)/(schema[0][1])*100,2)}% en relación con la capa cartográfica {os.path.splitext(os.path.basename(i.GetName()))[0]}"""

    #     elif a <= 0 and b > 0:
    #         lyr_condiciones.append(i)
    #         sheet['K37'] = "SI X"
    #         sheet['M37'] = f"""El predio presenta condicionantes en un área de {round(b/10000,2)}Ha, que equivale a un {round((b/10000)/(schema[0][1])*100,2)}% en relación con la capa cartográfica {os.path.splitext(os.path.basename(i.GetName()))[0]}"""

    #         # ds = round((intersect.Area()/10000)/(schema[0][1])*100,3)
    #         # area_ds = round(intersect.Area()/10000,3)
    #     elif a_0 <= 0 and a_1 <= 0:
    #         sheet['L37'] = 'NO X'

    #     else:
    #         sheet['L37'] = 'NO X'

    # # ##El predio se encuentra dentro del radio de inadjudicabilidad de zonas donde se adelanten explotaciones de recursos naturales no renovables        
    # sheet['M38'] ##Se debe agregar todas las capas (Excel). Por ahora solo cruza con 
    # sheet['L38'] = 'NO X'

    # lyr_PNN = driver.Open('Layers/Parque Nacional Natural.shp') ##Por ahora solo cruza con PNN
    # lyr_M39 = []
    # lyr_M39.append(lyr_PNN)
    # for i in lyr_M39:
    #     if intersect_layers_A(i,predio)[0] > 0:
    #         lyr_restricciones.append(lyr_PNN)
    #         sheet['K39'] = 'SI X'
    #         sheet['M39'] = f"El predio objeto de estudio presenta restricciones en un área de {round(intersect_layers_A(i,predio),2)}m2 equivalente al {round((intersect_layers_A(i,predio)/10000)/schema[0][1]*100,2)}% del predio, con la capa cartográfica {os.path.splitext(os.path.basename(i.GetName()))[0]}"
    #     else:
    #         sheet['L39'] = 'NO X'

    # # ##Sheet40

    # # Cruce vias Buffer 
    # lyr_bv = driver.Open('Layers/Buffer_Vial.shp') ## Ok Capa
    # lyr_restricciones.append(lyr_bv)
    # area_bv = intersect_layers_A(lyr_bv, predio)[0]



    # if area_bv > 0:
    #     sheet['K40'] = "SI X"
    #     sheet['M40'] = f"""El predio presenta traslape con un área de {round(area_bv/10000,2)}Ha, que equivale a un {round((area_bv/10000)/(schema[0][1])*100,2)}%, con faja de retiro de la vía de primer orden Transversal Neiva - San Vicente"""
    #     lyr_restricciones.append(lyr_bv)
    #     # bv = round((area_bv/10000)/(schema[0][1])*100,3)
    #     # area_bf = round(area_bv/10000,3)
    
    # else: 
    #     sheet['L40'] = f'NO X'
    
    # sheet['L50'] = f"""La UAF predial del predio corresponde a: {int(def_uaf(schema[0][1])[0])}Ha + {round((float(def_uaf(schema[0][1])[0]) - int(def_uaf(schema[0][1])[0]))*10000,3)}m2 a {int(def_uaf(schema[0][1])[1])}Ha + {round((float(def_uaf(schema[0][1])[1]) - int(def_uaf(schema[0][1])[1]))*10000,3)}"""

    # ##Condicionante
    # lyr_ZM = driver.Open('Layers/ZONIFICACION_MANEJO.shp') ##Zonificación Manejo
    # lyr_condiciones.append(lyr_ZM) if intersect_layers_A(lyr_ZM, predio)[0] > 0 else None

    # lyr_deg_s = driver.Open('Layers/Degradacion_suelo.shp') ##Degradación suelo
    # lyr_condiciones.append(lyr_deg_s) if intersect_layers_A(lyr_deg_s, predio)[0] > 0 else None

    # lyr_ZSI = driver.Open('Layers/ZONAS_SUSCEPTIBLES_INUNDACION.shp') ##Zonas Susceptibles Inundación
    # lyr_condiciones.append(lyr_ZSI) if intersect_layers_A(lyr_ZSI, predio)[0] > 0 else None

    # lyr_AFPC = driver.Open('Layers/UNIDAD_AGRICOLA_FAMILIAR_PROCESO_CONSTITUCION.shp')
    # lyr_condiciones.append(lyr_AFPC) if intersect_layers_A(lyr_AFPC, predio)[0] > 0 else None

    # lyr_SMV = driver.Open('Layers/SOLICITU_MINERA_VIGENTE.shp')
    # lyr_condiciones.append(lyr_SMV) if intersect_layers_A(lyr_SMV, predio)[0] > 0 else None

    # # lyr_l2 = driver.Open('Layers/Ley2.shp')
    # # lyr_condiciones.append(lyr_l2)

    # lyr_EMA = driver.Open('Layers/EVENTO_MINA_ANTIPERSONA.shp')
    # lyr_condiciones.append(lyr_EMA) if intersect_layers_A(lyr_EMA, predio)[0] > 0 else None
    

    # lyr_CR = driver.Open('Layers/Cuenca_Rios.shp') ##OK Capa
    # lyr_condiciones.append(lyr_CR) if intersect_layers_A(lyr_CR, predio)[0] > 0 else None

    # lyr_PSM = driver.Open('Layers/PREDIO_SIN_MATRICULA.shp')
    # lyr_condiciones.append(lyr_PSM) if intersect_layers_A(lyr_PSM, predio)[0] > 0 else None

    # lyr_MTH = driver.Open('Layers/MAPA_TIERRAS_HIDROCARBUROS.shp')
    # lyr_condiciones.append(lyr_MTH) if intersect_layers_A(lyr_MTH, predio)[0] > 0 else None

    # lyr_H = driver.Open('Layers/HUMEDAL.shp')
    # lyr_condiciones.append(lyr_H) if intersect_layers_A(lyr_H, predio)[0] > 0 else None

    # lyr_HTMMP = driver.Open('Layers/HISTORICO_TITULO_MINERO_MUNICIPIO_PRIORIZADO.shp')
    # lyr_condiciones.append(lyr_HTMMP) if intersect_layers_A(lyr_HTMMP, predio)[0] > 0 else None

    # lyr_HSMMP = driver.Open('Layers/HISTORICO_SOLICITUD_MINERA_MUNICIPIO_PRIORIZADO.shp')
    # lyr_condiciones.append(lyr_HSMMP) if intersect_layers_A(lyr_HSMMP, predio)[0] > 0 else None

    # lyr_FA = driver.Open('Layers/FRONTERA_AGRICOLA.shp')
    # lyr_condiciones.append(lyr_FA) if intersect_layers_A(lyr_FA, predio)[0] > 0 else None

    # lyr_ELTA = driver.Open('Layers/ESTADO_LEGAL_TERRITORIO_AMAZONICO.shp')
    # lyr_condiciones.append(lyr_ELTA) if intersect_layers_A(lyr_ELTA, predio)[0] > 0 else None

    # lyr_CS = driver.Open('Layers/CORRELACION_SUELO.shp')
    # lyr_condiciones.append(lyr_CS) if intersect_layers_A(lyr_CS, predio)[0] > 0 else None

    # lyr_CP = driver.Open('Layers/Centro_poblado.shp')
    # lyr_condiciones.append(lyr_CP) if intersect_layers_A(lyr_CP, predio)[0] > 0 else None

    # Lyr_ZRC_PC = driver.Open('Layers/ZRC_PROCESO_CONSTITUCION.shp')
    # lyr_condiciones.append(Lyr_ZRC_PC) if intersect_layers_A(Lyr_ZRC_PC, predio)[0] > 0 else None

    # lyr_BVMA = driver.Open('Layers/BUFFER_VICTIMA_MINA_ANTIPERSONA.shp')
    # lyr_condiciones.append(lyr_BVMA) if intersect_layers_A(lyr_BVMA, predio)[0] > 0 else None

    # lyr_BEMA = driver.Open('Layers/BUFFER_EVENTO_MINA_ANTIPERSONA.shp')
    # lyr_condiciones.append(lyr_BEMA) if intersect_layers_A(lyr_BEMA, predio)[0] > 0 else None

    # lyr_RM = driver.Open('Layers/remocion_en_masa.shp')
    # lyr_restricciones.append(lyr_RM)
    
    # if intersect_layers_FA(lyr_RM,predio,'CATAME','Media')[0] > 0 or intersect_layers_FA(lyr_RM,predio,'CATAME','Baja')[0] > 0:
    #     lyr_condiciones.append(lyr_RM)

    # lyr_SL2 = driver.Open('Layers/RESERVA FORESTAL LEY SEGUNDA SUSTRACCIONES.shp')
    # lyr_condiciones.append(lyr_SL2) if intersect_layers_A(lyr_SL2, predio)[0] > 0 else None

    # con_catastral = f"""De acuerdo con la información recaudada a través del método indirecto de mesas colaborativas se determinó que el predio denominado {schema[0][4]}, ubicado en el departamento de {intersect_layers_F(lyr_dep, predio,'NOMBRE_DEP')[0]}, municipio de {intersect_layers_F(lyr_mun, predio,'NOMBRE_MUN')[0]}, vereda {ID_pred.iloc[0,1].upper()}, cuenta con un área según el plano topográfico de {(num2words(round((int(schema[0][1]))), lang = 'es')).upper()} HECTÁREAS {(num2words(round((float(schema[0][1]) - int(schema[0][1]))*10000,2), lang = 'es')).upper()} METROS CUADRADOS ({round((int(schema[0][1])))}Ha + {round((float(schema[0][1]) - int(schema[0][1]))*10000,2)}m2). Que el {date_F007}, el grupo de topografía de la ANT, elaboró el cruce de información geográfica (F-007), y/o análisis espacial y cuya conclusión respecto del predio objeto de solicitud es que {A_restricciones(lyr_restricciones, predio)[1]} \n \nIgualmente, se informa que el predio denominado {schema[0][4]}, se traslapa con los siguientes componentes condicionantes:{condiciones(lyr_condiciones)}. Sin embargo, estas no afectan el área potencial y/o útil de titulación del predio."""
    # sheet['B53'] = con_catastral
    

    # con_agronomia = f"""De acuerdo a la información recaudada a través del método indirecto de mesas colaborativas, se determinó que para la zona donde está ubicado el predio, se presenta un régimen de lluvias monomodal y condiciones de suelos con textura mayormente arcillosa y ph  fuertemente ácidos, bajos contenidos de materia orgánica y condiciones productivas aptas para determinados cultivos y ganadería bovina y bufalina. \n \nAdemás, se tiene que el predio denominado {schema[0][4]}, ubicado en el departamento de {intersect_layers_F(lyr_dep, predio,'NOMBRE_DEP')[0]}, municipio de {intersect_layers_F(lyr_mun, predio,'NOMBRE_MUN')[0]}, vereda {ID_pred.iloc[0,1].upper()},cuenta con un área según el plano topográfico de {(num2words(round((int(schema[0][1]))), lang = 'es')).upper()} HECTÁREAS {(num2words(round((float(schema[0][1]) - int(schema[0][1]))*10000,2), lang = 'es')).upper()} METROS CUADRADOS ({round((int(schema[0][1])))}Ha + {round((float(schema[0][1]) - int(schema[0][1]))*10000,2)}m2), el cual está siendo ocupado hace {ID_pred.iloc[0,2]} años, por {sex_interesado(schemax[0][1])} solicitante de manera directa, que a su vez realiza una explotación de {cultivos(ID_pred.iloc[0,3], ID_pred.iloc[0,4])}. \n \nSegún la inspección ocular realizada (Formato ANT - ACCTI-F-116), realizada el {date}, en el predio no se evidencia ningún tipo de situaciones de riesgo o condiciones tales como remociones en masa de tierra, crecientes súbitas o pendientes mayores a 45° que representen peligro para la integridad de {sex_interesado(schemax[0][1])} ocupantes. \n \nDesde el componente ambiental no se observan limitantes que afecten los recursos naturales, el medio ambiente ni la zona productiva del predio. \n \nBajo estas condiciones, el grupo de Agronomía a cargo de esta evaluación determinó el cálculo de UAF con propuesta de producción de {def_uaf(schema[0][1])[2]}. Resultado de esta propuesta se estableció un rango de área para obtener entre 2 a 2.5 smmlv de {int(def_uaf(schema[0][1])[0])}Ha + {round((float(def_uaf(schema[0][1])[0]) - int(def_uaf(schema[0][1])[0]))*10000,3)}m2 a {int(def_uaf(schema[0][1])[1])}Ha + {round((float(def_uaf(schema[0][1])[1]) - int(def_uaf(schema[0][1])[1]))*10000,3)}. Con lo anterior, se establece que el predio está {def_uaf(schema[0][1])[3]} rango de la UAF mencionada, con la capacidad de producir {def_uaf(schema[0][1])[4]} smmlv, en la actualidad. \n \nEn consecuencia, de lo explicado anteriormente, desde el componente agronómico de la Subdirección de Acceso a Tierras por Demanda y Descongestión se recomienda continuar con el proceso de adjudicación del predio. """
    # print(cultivos(ID_pred.iloc[0,3], ID_pred.iloc[0,4]))
    # area = SQL.exe_sql()[0][1]
    UAF = agricola(SQL.exe_sql()[0][1])
    
    
        # print(result)
    # sheet['L51'] = con_agronomia
    # sheet['Q26'] = f"""Porción Cultivada o explotada:{cultivos(ID_pred.iloc[0,3], ID_pred.iloc[0,4])}"""
    
    # con_juridico = f"""Con fundamento en el marco normativo establecido en la Resolución No. 20230010000036 del 12 de abril de 2023 suscrita por la Dirección General de la Agencia Nacional de Tierras y mediante la cual se expidió el Reglamento Operativo de esta entidad, se procedió a la revisión jurídica del proceso de adjudicación de predio denominado {schema[0][4]} {names_interesados(schema)[1]}. 

    # Para todos los fines de este documento se comprende que los documentos, planos, soportes técnicos y /o oficios del caso que se relacionan a continuación fueron identificados y ubicados en el expediente No. {ID_pred_.iloc[0,1]} de los sistemas de información SIT y ORFEO de la Agencia Nacional de Tierras.

    # Evaluación de la naturaleza jurídica del predio (articulo 28, numeral 1 de Resolución 20230010000036 del 12 de abril de 2023)

    # Se ha verificado la siguiente información técnica indispensable para establecer la viabilidad de la adjudicación del predio {schema[0][4]} de acuerdo con lo ordenado en Resolución No. 20230010000036 del 12 de abril de 2023, articulo 13 que se integra por los componentes topográficos y agronómicos expresados así:

    # Respecto del levantamiento topográfico elaborado por el grupo de topografía del cooperante OEI del {date_LV}, realizado al predio denominado"{schema[0][4]}”, (numeral 5 del presente informe), 
    # se identificaron los siguientes elementos:

    # * Que tiene un área de {(num2words(round((int(schema[0][1]))), lang = 'es')).upper()} HECTÁREAS {(num2words(round((float(schema[0][1]) - int(schema[0][1]))*10000,2), lang = 'es')).upper()} METROS CUADRADOS ({round((int(schema[0][1])))}Ha + {round((float(schema[0][1]) - int(schema[0][1]))*10000,2)}m2),
    # * Que se encuentra ubicado en el municipio de {intersect_layers_F(lyr_mun, predio,'NOMBRE_MUN')[0]}, departamento de {intersect_layers_F(lyr_dep, predio,'NOMBRE_DEP')[0]}; 
    # * Que se identificaron cada uno de los linderos y colindancias del predio, contenidos en la Redacción Técnica de Linderos (F-009).
    # * Que de acuerdo con el Cruce de Información Geográfica (F-007), el predio {A_restricciones(lyr_restricciones, predio)[1]}
    # * Igualmente, se evidenció que el predio denominado {schema[0][4]}, traslapa con los siguientes componentes condicionantes: {condiciones(lyr_condiciones)}. Sin embargo, estas no afectan el área de potencial y/o útil de titulación del predio.

    # Respecto del componente agronómico, mediante estudio de fecha {date_FA} realizado por grupo de agronomía de la SATDD, se estableció un rango de área para obtener entre 2 a 2.5 smmlv de {int(def_uaf(schema[0][1])[0])}Ha + {round((float(def_uaf(schema[0][1])[0]) - int(def_uaf(schema[0][1])[0]))*10000,3)}m2 a {int(def_uaf(schema[0][1])[1])}Ha + {round((float(def_uaf(schema[0][1])[1]) - int(def_uaf(schema[0][1])[1]))*10000,3)}, con la capacidad de producir {def_uaf(schema[0][1])[4]} smmlv, en la actualidad.

    # * Además, que el predio denominado {schema[0][4]}está siendo ocupado hace {num2words(ID_pred.iloc[0,2], lang = 'es')} ({ID_pred.iloc[0,2]}) años, por {sex_interesado(schemax[0][1])} de manera directa, que a su vez realiza una explotación con {cultivos(ID_pred.iloc[0,3], ID_pred.iloc[0,4])}. 
    # * Que el predio denominado “{schema[0][4]}” no presenta ninguna situación o condiciones que puedan poner en riesgo la integridad de {sex_interesado(schema[0][1])}, ni limitantes que afecten los recursos naturales, el medio ambiente, ni la zona productiva del predio; por tal razón, el grupo agronómico de la SATDD emitió concepto técnico (numeral 5 del presente informe) recomendando continuar con el proceso de adjudicación del predio. 

    # Revisión de requisitos subjetivos:

    # De conformidad con lo ordenado en el artículo 28, numeral 1º del Reglamento Operativo, se ha determinado la condición de poseedor y ocupante, estableciendo en este caso que {sex_interesado(schemax[0][1])} ocupa(n) el predio desde hace {num2words(ID_pred.iloc[0,2], lang = 'es')} {ID_pred.iloc[0,2]} años y ejerce(n) una explotación de {cultivos(ID_pred.iloc[0,3], ID_pred.iloc[0,4])}

    # Respecto de la información de cruces con bases de datos de los solicitantes, la Subdirección de Acceso a Tierras por Demanda y Descongestión – SATDD, solicitó a la Subdirección de Sistemas de Información de Tierras – SSIT mediante memorandos 20234200091813 del 31 de marzo de 2023 y 20234200106273 del 15 de abril de 2023, la valoración e inclusión en el RESO de {sex_interesado(schemax[0][1])}.

    # En consecuencia, la definición de inclusión ó no de los potenciales beneficiarios al RESO será confirmada con fundamento en estas valoraciones, es decir, si es procedente ó no la adjudicación del predio {schema[0][4]} a {sex_interesado(schemax[0][1])} en el informe técnico jurídico definitivo. Esta situación se establece con fundamento en el artículo 38 del Reglamento Operativo.

    # Se concluye entonces que la solicitud cumple con los requisitos objetivos para adjudicación del predio denominado {schema[0][4]} y en consecuencia, se comunica que es viable continuar con la etapa de apertura del trámite administrativo del Procedimiento Único de Reconocimiento de Derecho del predio {schema[0][4]}, ubicado en el municipio {intersect_layers_F(lyr_mun, predio,'NOMBRE_MUN')[0]}, departamento {intersect_layers_F(lyr_dep, predio,'NOMBRE_DEP')[0]} {names_interesados(schema)[0]} de conformidad con el artículo 32 de la Resolución 20230010000036 del 12 de abril de 2023.""" 
    # #print(con_juridico)
    # sheet['B62'] = con_juridico
    # path_out = f'Tec/{ID}.xlsx'
    # ITJP.save(path_out)

    # FP = time.time()
    # print('Finaliza ITJP')
    # print(f'Tiempo de ejecución {round((FP-BP)/60,2)} minutos')

# driver = ogr.GetDriverByName('ESRI Shapefile')
# lyr_ds = driver.Open('Layers/Drenaje_Sencillo_(30m)_.shp')

# # Crear una instancia de la clase LayerIntersection
# layer_intersection_A = OP_geographic(predio,lyr_ds)
# layer_intersection_F = OP_geographic(predio,lyr_ds)
# # Llamar al método intersect_layers_FA()
# result = layer_intersection_A.intersect_layers_A()
# print(result)
# result2 = layer_intersection_F.intersect_layers_F('NOMBRE_GEO')
# print(result2)

# intersect_layers_FA = OP_geographic(predio,lyr_ds)
# result3 = intersect_layers_FA.intersect_layers_FA('NOMBRE_GEO', None)
# print(result3)
# Realizar operaciones con los resultados obtenidos
# ...

# interesado = interesado(SQL.exe_sql())
# result = interesado.names_interesados()
# print(result)





FP_= time.time()
print(f'Tiempo final de ejecución {round((FP_-BP)/60,2)} minutos')
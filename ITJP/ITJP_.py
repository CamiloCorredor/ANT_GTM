class ITJP: 

    def __init__(self, vector_ID):
        self.vector_ID = vector_ID
        

    def ITJP(vector_ID):
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
        from datetime import datetime, timedelta
        
        
        from shapely.wkb import loads
        from shapely import wkb
        import os

        import binascii
        import matplotlib.pyplot as plt
        
        import pandas as pd
        import json
        
        from num2words import num2words
        
        with open('paths.json') as file:
            # Load the JSON data
            data = json.load(file)
        
        
        
        from datetime import datetime
        
        from OP_geographic import OP_geographic
        
        from interesado import interesado
        
        from SQL_LADM import SQL_LADM
        
        from Agricola import agricola
        
        from Restric_conditions import Restricciones_condiciones
        
        from BIP import BIP      
                
        # vector_ID =['5035000202', '5035000322', '5035010566']
               
        #vector_ID = ['5035010005']
        
        for ID in vector_ID:     
                    
            object_agro = BIP(data[1]["agronomia"], ID)
            object_juri = BIP(data[1]["juridico"], ID)    
            
            print(f'Informe Técnico Jurídico Preliminar {ID}')
            ITJP = openpyxl.load_workbook(data[1]["path_xlsx"])
            
            date_ = str(object_agro.info("FECHA_INSPECCION_OCULAR"))
            truncated_time_string = date_[:26]  
            date_ = datetime.strptime(truncated_time_string, '%Y-%m-%dT%H:%M:%S.%f') 
            date = date_.strftime('%d/%m/%Y')
            
            excel_start_date = datetime(1900, 1, 1)
            date_ = int(object_juri.info("FECHA_LEVANTAMIENTO_TOPOGRAFICO"))
            delta = timedelta(days = date_)
            date_ = excel_start_date + delta 
            date_LV = date_.strftime('%d/%m/%Y')
        
            date_ = datetime.strptime(str(object_juri.info("FECHA_FORMATO AGRONOMIA")), '%Y-%m-%d %H:%M:%S')
            date_FA = date_.strftime('%d/%m/%Y')
        
            date_ = str(object_juri.info("F-007"))
            truncated_time_string = date_[:26]  
            date_ = datetime.strptime(truncated_time_string, '%Y-%m-%dT%H:%M:%S.%f') 
            date_F007 = date_.strftime('%d/%m/%Y')
        
            SQL = SQL_LADM("localhost", "ladm_ttsp", "postgres", "1234", ID)
            
            sheet = ITJP['Hoja1']
        
            spatial_reference = osr.SpatialReference()
            spatial_reference.ImportFromEPSG(9377)
        
            shapely_obj = shapely.wkb.loads(SQL.exe_sql()[0][5])
            predio = ogr.CreateGeometryFromWkt(shapely_obj.wkt)
            predio.AssignSpatialReference(spatial_reference)
            #geometry = loads(wkb)
            
            # Nombre solicitante
            if len(SQL.exe_sql_2()) == 2:  
                sheet['B9'] = f"""Nombre solicitante: {SQL.exe_sql_2()[0][7]}
            Documento de identifcación: {SQL.exe_sql_2()[0][6]}"""
                sheet['R9'] = f"""Nombre solicitante: {SQL.exe_sql_2()[1][7]}
            Documento de identifcación: {SQL.exe_sql_2()[1][6]}"""
            elif len(SQL.exe_sql_2()) == 1:
                sheet['B9'] = f"""Nombre solicitante: {SQL.exe_sql_2()[0][2]}
            Documento de identificación: {SQL.exe_sql_2()[0][3]}"""
            else:
                print('Warning: Predio > 2 interesados')
            # # Nombre del Predio
            sheet['B19'] = f"""Nombre: {SQL.exe_sql()[0][4]}"""
            # # Area predio
            sheet['F21'] = int(SQL.exe_sql()[0][1])
            sheet['I21'] = round((float(SQL.exe_sql()[0][1]) - int(SQL.exe_sql()[0][1]))*10000,3)
            # # Cedula catastral 
            # # Cargar capa predial y realizar intersect AC21
            driver = ogr.GetDriverByName('ESRI Shapefile')
        
              
            lyr_condiciones = []
            lyr_restricciones = []      
                    
            OP_GEO = OP_geographic(predio)
        
            lyr_dep = driver.Open(data[0]["lyr_dep"])
            lyr_mun = driver.Open(data[0]["lyr_mun"])
        
            sheet['X19'] = f"""Municipio: { OP_GEO.intersect_layers_F(lyr_mun, "NOMBRE_MUN")}"""
            sheet['P19']= f"""Departamento: {OP_GEO.intersect_layers_F(lyr_dep, "NOMBRE_DEP")}"""
            sheet['B20'] = f"""Vereda o Fracción: {object_agro.info("VEREDA").upper()}"""
            
            lyr_CR = driver.Open(data[0]["lyr_CR"])
        
            lyr_Terreno = driver.Open(data[0]["lyr_Terreno"]) ##OK Capa
            intersection = OP_GEO.intersect_layers_F(lyr_Terreno, "codigo")
            if len(intersection) > 1:        
                sheet['AC21'] = '\n'.join(intersection)
            elif len(data) == 1:
                sheet['AC21'] = intersection[0]
        
            #Cuenca Rios
            lyr_CR = driver.Open(data[0]["lyr_CR"])
            area_CR = OP_GEO.intersect_layers_F(lyr_CR, "NOM_ZH")
        
            # # ZRC 
            lyr_ZRC = driver.Open(data[0]["lyr_ZRC"]) ##OK Capa
            area_ZRC = OP_GEO.intersect_layers_A(lyr_ZRC)[0]
            if round(area_ZRC/10000,3) == round(SQL.exe_sql()[0][1],3):
                
                lyr_condiciones.append(lyr_ZRC)
                sheet['H36'] = "SI X"
                sheet['J36'] = f"""Zona de reserva campesina del Pato Balsillas"""
            else: 
                sheet['I36'] = f'NO X'
                # p_zrc = round((intersect.Area()/10000)/(schema[0][1])*100,3)
                #Implementación aquí 
        
        
        
            # #sheet['M34']
            lyr_bosque = driver.Open(data[0]["lyr_bosque"]) ##OK Capa
            lyr_condiciones.append(lyr_bosque)
            area_bosques = OP_GEO.intersect_layers_A(lyr_bosque)[0]
            if area_bosques > 0:
                sheet['K34'] = "SI X"
                sheet['M34'] = f"""El predio presenta traslape con un área de {round(area_bosques/10000,3)}Ha, que equivale a un {round((area_bosques/10000)/(SQL.exe_sql()[0][1])*100,3)}%, con la capa cartográfica Bosques-2010 del IDEAM"""
            else:
                sheet['L34'] = f'NO X'
        
            # # #Determinantes ambientales M35
            lyr_ds = driver.Open(data[0]["lyr_ds"]) ## ##Se debe agregar todas las capas (Excel). Por ahora solo cruza con DS
            lyr_dd = driver.Open(data[0]["lyr_dd"])
            lyr_M35 = []
            lyr_M35.append(lyr_ds)
            lyr_M35.append(lyr_dd)
            strng = ''
            for i in lyr_M35:
            
                a_0 = OP_GEO.intersect_layers_FA(i,'NOMBRE_GEO', None)[0] ##Iguales
                a_1 = OP_GEO.intersect_layers_DIFFFA(i, 'NOMBRE_GEO', None)[0] ##Diferentes
                if a_0 > 0 and a_1 > 0:
                    lyr_restricciones.append(i)
                    lyr_condiciones.append(i)
                    sheet['K35'] = "SI X"
                    strng = strng + f'El predio presenta restricciones en un área de {round(a_1/10000,2)}Ha, que equivale a un {round((a_1/10000)/(SQL.exe_sql()[0][1])*100,2)}%. Adicionalmente, presenta condicionantes en un área de {round(a_0/10000,2)}Ha, que equivade a un {round((a_0/10000)/(SQL.exe_sql()[0][1])*100,2)}%, lo anterior en relación con la capa cartográfica {os.path.splitext(os.path.basename(i.GetName()))[0]}'
                    sheet['M35'] = strng
                    # print(f"""El predio presenta restricciones en un área de {round(a_1/10000,2)}Ha, que equivale a un {round((a_1/10000)/(schema[0][1])*100,2)}%. Adicionalmente, presenta condicionantes en un área de {round(a_0/10000,2)}Ha, que equivade a un {round((a_0/10000)/(schema[0][1])*100,2)}%, lo anterior en relación con la capa cartográfica {os.path.splitext(os.path.basename(i.GetName()))[0]}""")
                elif a_1 > 0 and a_0 <= 0:
                    lyr_restricciones.append(i)
                    sheet['K35'] = "SI X"
                    strng = strng + f"""El predio presenta restricciones en un área de {round(a_1/10000,2)}Ha, que equivale a un {round((a_1/10000)/(SQL.exe_sql()[0][1])*100,2)}% en relación con la capa cartográfica {os.path.splitext(os.path.basename(i.GetName()))[0]}"""
                    sheet['M35'] = strng
        
                elif a_1 <= 0 and a_0 > 0:
                    lyr_condiciones.append(i)
                    sheet['K35'] = "SI X"
                    strng = strng + f"""El predio presenta condicionantes en un área de {round(a_0/10000,2)}Ha, que equivale a un {round((a_0/10000)/(SQL.exe_sql()[0][1])*100,2)}% en relación con la capa cartográfica {os.path.splitext(os.path.basename(i.GetName()))[0]}"""
                    sheet['M35'] = strng
                   
                elif a_0 <= 0 and a_1 <= 0:
                    sheet['L35'] = 'NO X'
                    sheet['M35'] = ' '
                else: 
                    pass       
                
                
            # #sheet['K37']
            lyr_RTDAF = driver.Open(data[0]["lyr_RTDAF"])
        
            lyr_M37 = [] ##Se debe agregar todas las capas (Excel). Por ahora solo cruza con RTDAF
            lyr_M37.append(lyr_RTDAF)
            for i in lyr_M37:
                a = OP_GEO.intersect_layers_FA(i, 'estado_tra', 'Sentencia')[0]
                b = OP_GEO.intersect_layers_DIFFFA(i,'estado_tra', 'Sentencia')[0]
                if a > 0 and b > 0:
                    lyr_restricciones.append(i)
                    lyr_condiciones.append(i)
                    sheet['K37'] = 'SI X'
                    sheet['M37'] = f"""El predio presenta restricciones en un área de {round(a/10000,2)}Ha, que equivale a un {round((a/10000)/(SQL.exe_sql()[0][1])*100,2)}%. Adicionalmente, presenta condicionantes en un área de {round(b/10000,2)}Ha, que equivade a un {round((b/10000)/(SQL.exe_sql()[0][1])*100,2)}%, lo anterior en relación con la capa cartográfica {os.path.splitext(os.path.basename(i.GetName()))[0]}"""
                elif a > 0 and b <= 0:
                    lyr_restricciones.append(i)
                    sheet['K37'] = "SI X"
                    sheet['M37'] = f"""El predio presenta restricciones en un área de {round(a/10000,2)}Ha, que equivale a un {round((a/10000)/(SQL.exe_sql()[0][1])*100,2)}% en relación con la capa cartográfica {os.path.splitext(os.path.basename(i.GetName()))[0]}"""
                elif a <= 0 and b > 0:
                    lyr_condiciones.append(i)
                    sheet['K37'] = "SI X"
                    sheet['M37'] = f"""El predio presenta condicionantes en un área de {round(b/10000,2)}Ha, que equivale a un {round((b/10000)/(SQL.exe_sql()[0][1])*100,2)}% en relación con la capa cartográfica {os.path.splitext(os.path.basename(i.GetName()))[0]}"""
                    # ds = round((intersect.Area()/10000)/(schema[0][1])*100,3)
                    # area_ds = round(intersect.Area()/10000,3)
                elif a_0 <= 0 and a_1 <= 0:
                    sheet['L37'] = 'NO X'
                else:
                     sheet['L37'] = 'NO X'
             # ##El predio se encuentra dentro del radio de inadjudicabilidad de zonas donde se adelanten explotaciones de recursos naturales no renovables        
            sheet['M38'] ##Se debe agregar todas las capas (Excel). Por ahora solo cruza con 
            sheet['L38'] = 'NO X'
        
            lyr_PNN = driver.Open(data[0]["lyr_PNN"]) ##Por ahora solo cruza con PNN
            lyr_M39 = []
            lyr_M39.append(lyr_PNN)
            for i in lyr_M39:
                area_i = OP_GEO.intersect_layers_A(i)[0]
                if area_i > 0:
                    lyr_restricciones.append(lyr_PNN)
                    sheet['K39'] = 'SI X'
                    sheet['M39'] = f"El predio objeto de estudio presenta restricciones en un área de {round(area_i,2)}m2 equivalente al {round((area_i/10000)/SQL.exe_sql()[0][1]*100,2)}% del predio, con la capa cartográfica {os.path.splitext(os.path.basename(i.GetName()))[0]}"
                else:
                    sheet['L39'] = 'NO X'
        
            # # ##Sheet40
        
            # Cruce vias Buffer 
            lyr_bv = driver.Open(data[0]["lyr_bv"]) ## Ok Capa
            lyr_restricciones.append(lyr_bv)
            area_bv = OP_GEO.intersect_layers_A(lyr_bv)[0]
        
            if area_bv > 0:
                sheet['K40'] = "SI X"
                sheet['M40'] = f"""El predio presenta traslape con un área de {round(area_bv/10000,2)}Ha, que equivale a un {round((area_bv/10000)/(SQL.exe_sql()[0][1])*100,2)}%, con faja de retiro de la vía de primer orden Transversal Neiva - San Vicente"""
                lyr_restricciones.append(lyr_bv)
                ##Implementación para las demás vías del país
            else: 
                sheet['L40'] = f'NO X'
            
            UAF = agricola(SQL.exe_sql()[0][1])
        
            sheet['L50'] = f"""La UAF predial del predio corresponde a: {int(UAF.def_uaf()[0])}Ha + {round((float(UAF.def_uaf()[0]) - int(UAF.def_uaf()[0]))*10000,3)}m2 a {int(UAF.def_uaf()[1])}Ha + {round((float(UAF.def_uaf()[1]) - int(UAF.def_uaf()[1]))*10000,3)}"""
        
            # Condicionante
            lyr_ZM = driver.Open(data[0]["lyr_ZM"]) ##Zonificación Manejo
            lyr_condiciones.append(lyr_ZM) if OP_GEO.intersect_layers_A(lyr_ZM)[0] > 0 else None
        
            lyr_deg_s = driver.Open(data[0]["lyr_deg_s"]) ##Degradación suelo
            lyr_condiciones.append(lyr_deg_s) if OP_GEO.intersect_layers_A(lyr_deg_s)[0] > 0 else None
        
            lyr_ZSI = driver.Open(data[0]["lyr_ZSI"]) ##Zonas Susceptibles Inundación
            lyr_condiciones.append(lyr_ZSI) if OP_GEO.intersect_layers_A(lyr_ZSI)[0] > 0 else None
        
            lyr_AFPC = driver.Open(data[0]["lyr_AFPC"])
            lyr_condiciones.append(lyr_AFPC) if OP_GEO.intersect_layers_A(lyr_AFPC)[0] > 0 else None
        
            lyr_SMV = driver.Open(data[0]["lyr_SMV"])
            lyr_condiciones.append(lyr_SMV) if OP_GEO.intersect_layers_A(lyr_SMV)[0] > 0 else None
        
            # lyr_l2 = driver.Open('Layers/Ley2.shp')
            # lyr_condiciones.append(lyr_l2)
        
            lyr_EMA = driver.Open(data[0]["lyr_EMA"])
            lyr_condiciones.append(lyr_EMA) if OP_GEO.intersect_layers_A(lyr_EMA)[0] > 0 else None
            
            lyr_CR = driver.Open(data[0]["lyr_CR"]) ##OK Capa
            lyr_condiciones.append(lyr_CR) if OP_GEO.intersect_layers_A(lyr_CR)[0] > 0 else None
        
            lyr_PSM = driver.Open(data[0]["lyr_PSM"])
            lyr_condiciones.append(lyr_PSM) if OP_GEO.intersect_layers_A(lyr_PSM)[0] > 0 else None
        
            lyr_MTH = driver.Open(data[0]["lyr_MTH"])
            lyr_condiciones.append(lyr_MTH) if OP_GEO.intersect_layers_A(lyr_MTH)[0] > 0 else None
        
            lyr_H = driver.Open(data[0]["lyr_H"])
            lyr_condiciones.append(lyr_H) if OP_GEO.intersect_layers_A(lyr_H)[0] > 0 else None
        
            lyr_HTMMP = driver.Open(data[0]["lyr_HTMMP"])
            lyr_condiciones.append(lyr_HTMMP) if OP_GEO.intersect_layers_A(lyr_HTMMP)[0] > 0 else None
        
            lyr_HSMMP = driver.Open(data[0]["lyr_HSMMP"])
            lyr_condiciones.append(lyr_HSMMP) if OP_GEO.intersect_layers_A(lyr_HSMMP)[0] > 0 else None
        
            lyr_FA = driver.Open(data[0]["lyr_FA"])
            lyr_condiciones.append(lyr_FA) if OP_GEO.intersect_layers_A(lyr_FA)[0] > 0 else None
        
            lyr_ELTA = driver.Open(data[0]["lyr_ELTA"])
            lyr_condiciones.append(lyr_ELTA) if OP_GEO.intersect_layers_A(lyr_ELTA)[0] > 0 else None
        
            lyr_CS = driver.Open(data[0]["lyr_CS"])
            lyr_condiciones.append(lyr_CS) if OP_GEO.intersect_layers_A(lyr_CS)[0] > 0 else None
        
            lyr_CP = driver.Open(data[0]["lyr_CP"])
            lyr_condiciones.append(lyr_CP) if OP_GEO.intersect_layers_A(lyr_CP)[0] > 0 else None
        
            Lyr_ZRC_PC = driver.Open(data[0]["Lyr_ZRC_PC"])
            lyr_condiciones.append(Lyr_ZRC_PC) if OP_GEO.intersect_layers_A(Lyr_ZRC_PC)[0] > 0 else None
        
            lyr_BVMA = driver.Open(data[0]["lyr_BVMA"])
            lyr_condiciones.append(lyr_BVMA) if OP_GEO.intersect_layers_A(lyr_BVMA)[0] > 0 else None
        
            lyr_BEMA = driver.Open(data[0]["lyr_BEMA"])
            lyr_condiciones.append(lyr_BEMA) if OP_GEO.intersect_layers_A(lyr_BEMA)[0] > 0 else None
        
            lyr_RM = driver.Open(data[0]["lyr_RM"])
            lyr_restricciones.append(lyr_RM)
            
            if OP_GEO.intersect_layers_FA(lyr_RM,'CATAME','Media')[0] > 0 or OP_GEO.intersect_layers_FA(lyr_RM,'CATAME','Baja')[0] > 0:
                lyr_condiciones.append(lyr_RM)
        
            lyr_SL2 = driver.Open('Layers/RESERVA FORESTAL LEY SEGUNDA SUSTRACCIONES.shp')
            lyr_condiciones.append(lyr_SL2) if OP_GEO.intersect_layers_A(lyr_SL2)[0] > 0 else None
        
            RECO = Restricciones_condiciones(predio)
        
            con_catastral = f"""De acuerdo con la información recaudada a través del método indirecto de mesas colaborativas se determinó que el predio denominado {SQL.exe_sql()[0][4]}, ubicado en el departamento de {OP_GEO.intersect_layers_F(lyr_dep, 'NOMBRE_DEP')[0]}, municipio de {OP_GEO.intersect_layers_F(lyr_mun, 'NOMBRE_MUN')[0]}, vereda {object_agro.info("VEREDA").upper()}, cuenta con un área según el plano topográfico de {(num2words(round((int(SQL.exe_sql()[0][1]))), lang = 'es')).upper()} HECTÁREAS {(num2words(round((float(SQL.exe_sql()[0][1]) - int(SQL.exe_sql()[0][1]))*10000,2), lang = 'es')).upper()} METROS CUADRADOS ({round((int(SQL.exe_sql()[0][1])))}Ha + {round((float(SQL.exe_sql()[0][1]) - int(SQL.exe_sql()[0][1]))*10000,2)}m2). Que el {date_F007}, el grupo de topografía de la ANT, elaboró el cruce de información geográfica (F-007), y/o análisis espacial y cuya conclusión respecto del predio objeto de solicitud es que {RECO.A_restricciones(lyr_restricciones)[1]} \n \nIgualmente, se informa que el predio denominado {SQL.exe_sql()[0][4]}, se traslapa con los siguientes componentes condicionantes:{RECO.condiciones(lyr_condiciones)}. Sin embargo, estas no afectan el área potencial y/o útil de titulación del predio."""
            sheet['B53'] = con_catastral
            
        
            
            con_agronomia = f"""De acuerdo a la información recaudada a través del método indirecto de mesas colaborativas, se determinó que para la zona donde está ubicado el predio, se presenta un régimen de lluvias monomodal y condiciones de suelos con textura mayormente arcillosa y ph  fuertemente ácidos, bajos contenidos de materia orgánica y condiciones productivas aptas para determinados cultivos y ganadería bovina y bufalina. \n \nAdemás, se tiene que el predio denominado {SQL.exe_sql()[0][4]}, ubicado en el departamento de {OP_GEO.intersect_layers_F(lyr_dep, 'NOMBRE_DEP')[0]}, municipio de {OP_GEO.intersect_layers_F(lyr_mun, 'NOMBRE_MUN')[0]}, vereda {object_agro.info("VEREDA").upper()},cuenta con un área según el plano topográfico de {(num2words(round((int(SQL.exe_sql()[0][1]))), lang = 'es')).upper()} HECTÁREAS {(num2words(round((float(SQL.exe_sql()[0][1]) - int(SQL.exe_sql()[0][1]))*10000,2), lang = 'es')).upper()} METROS CUADRADOS ({round((int(SQL.exe_sql()[0][1])))}Ha + {round((float(SQL.exe_sql()[0][1]) - int(SQL.exe_sql()[0][1]))*10000,2)}m2), el cual está siendo ocupado hace {object_agro.info("TIEMPO_OCUPACION")} años, por {SQL.exe_sql_1()[0][1]} solicitante de manera directa, que a su vez realiza una explotación de {UAF.cultivos(object_agro.info("CULTIVOS"), object_agro.info("CULTIVOS_%"))}. \n \nSegún la inspección ocular realizada (Formato ANT - ACCTI-F-116), realizada el {date}, en el predio no se evidencia ningún tipo de situaciones de riesgo o condiciones tales como remociones en masa de tierra, crecientes súbitas o pendientes mayores a 45° que representen peligro para la integridad de {SQL.exe_sql_1()[0][1]} ocupantes. \n \nDesde el componente ambiental no se observan limitantes que afecten los recursos naturales, el medio ambiente ni la zona productiva del predio. \n \nBajo estas condiciones, el grupo de Agronomía a cargo de esta evaluación determinó el cálculo de UAF con propuesta de producción de {UAF.def_uaf()[2]}. Resultado de esta propuesta se estableció un rango de área para obtener entre 2 a 2.5 smmlv de {int(UAF.def_uaf()[0])}Ha + {round((float(UAF.def_uaf()[0]) - int(UAF.def_uaf()[0]))*10000,3)}m2 a {int(UAF.def_uaf()[1])}Ha + {round((float(UAF.def_uaf()[1]) - int(UAF.def_uaf()[1]))*10000,3)}. Con lo anterior, se establece que el predio está {UAF.def_uaf()[3]} rango de la UAF mencionada, con la capacidad de producir {UAF.def_uaf()[4]} smmlv, en la actualidad. \n \nEn consecuencia, de lo explicado anteriormente, desde el componente agronómico de la Subdirección de Acceso a Tierras por Demanda y Descongestión se recomienda continuar con el proceso de adjudicación del predio. """
            sheet['L51'] = con_agronomia
            
            sheet['Q26'] = f"""Porción Cultivada o explotada:{UAF.cultivos(object_agro.info("CULTIVOS"), object_agro.info("CULTIVOS_%"))}"""
            
            persona = interesado(SQL.exe_sql())
            print(UAF.def_uaf()[1])
            con_juridico = f"""Con fundamento en el marco normativo establecido en la Resolución No. 20230010000036 del 12 de abril de 2023 suscrita por la Dirección General de la Agencia Nacional de Tierras y mediante la cual se expidió el Reglamento Operativo de esta entidad, se procedió a la revisión jurídica del proceso de adjudicación de predio denominado {SQL.exe_sql()[0][4]}. 
            Para todos los fines de este documento se comprende que los documentos, planos, soportes técnicos y /o oficios del caso que se relacionan a continuación fueron identificados y ubicados en el expediente No. {object_juri.info("EXPEDIENTE")} de los sistemas de información SIT y ORFEO de la Agencia Nacional de Tierras.
            Evaluación de la naturaleza jurídica del predio (articulo 28, numeral 1 de Resolución 20230010000036 del 12 de abril de 2023)
            Se ha verificado la siguiente información técnica indispensable para establecer la viabilidad de la adjudicación del predio {SQL.exe_sql()[0][4]} de acuerdo con lo ordenado en Resolución No. 20230010000036 del 12 de abril de 2023, articulo 13 que se integra por los componentes topográficos y agronómicos expresados así:
            Respecto del levantamiento topográfico elaborado por el grupo de topografía del cooperante OEI del {date_LV}, realizado al predio denominado"{SQL.exe_sql()[0][4]}”, (numeral 5 del presente informe), 
            se identificaron los siguientes elementos:
             * Que tiene un área de {(num2words(round((int(SQL.exe_sql()[0][1]))), lang = 'es')).upper()} HECTÁREAS {(num2words(round((float(SQL.exe_sql()[0][1]) - int(SQL.exe_sql()[0][1]))*10000,2), lang = 'es')).upper()} METROS CUADRADOS ({round((int(SQL.exe_sql()[0][1])))}Ha + {round((float(SQL.exe_sql()[0][1]) - int(SQL.exe_sql()[0][1]))*10000,2)}m2),
             * Que se encuentra ubicado en el municipio de {OP_GEO.intersect_layers_F(lyr_mun, 'NOMBRE_MUN')[0]}, departamento de {OP_GEO.intersect_layers_F(lyr_dep, 'NOMBRE_DEP')[0]}; 
             * Que se identificaron cada uno de los linderos y colindancias del predio, contenidos en la Redacción Técnica de Linderos (F-009).
             * Que de acuerdo con el Cruce de Información Geográfica (F-007), el predio {RECO.A_restricciones(lyr_restricciones)[1]}
             * Igualmente, se evidenció que el predio denominado {SQL.exe_sql()[0][4]}, traslapa con los siguientes componentes condicionantes: {RECO.condiciones(lyr_condiciones)}. Sin embargo, estas no afectan el área de potencial y/o útil de titulación del predio.
            Respecto del componente agronómico, mediante estudio de fecha {date_FA} realizado por grupo de agronomía de la SATDD, se estableció un rango de área para obtener entre 2 a 2.5 smmlv de {int(UAF.def_uaf()[0])}Ha + {round((float(UAF.def_uaf()[0]) - int(UAF.def_uaf()[0]))*10000,3)}m2 a {int(UAF.def_uaf()[1])}Ha + {round((float(UAF.def_uaf()[1]) - int(UAF.def_uaf()[1]))*10000,3)}, con la capacidad de producir {UAF.def_uaf()[4]} smmlv, en la actualidad.
             * Además, que el predio denominado {SQL.exe_sql()[0][4]} está siendo ocupado hace {num2words(object_agro.info("TIEMPO_OCUPACION"), lang = 'es')} ({object_agro.info("TIEMPO_OCUPACION")}) años, por {SQL.exe_sql_1()} de manera directa, que a su vez realiza una explotación con {UAF.cultivos(object_agro.info("CULTIVOS"), object_agro.info("CULTIVOS_%"))}. 
             * Que el predio denominado “{SQL.exe_sql()[0][4]}” no presenta ninguna situación o condiciones que puedan poner en riesgo la integridad de {SQL.exe_sql_1()}, ni limitantes que afecten los recursos naturales, el medio ambiente, ni la zona productiva del predio; por tal razón, el grupo agronómico de la SATDD emitió concepto técnico (numeral 5 del presente informe) recomendando continuar con el proceso de adjudicación del predio. 
            Revisión de requisitos subjetivos:
            De conformidad con lo ordenado en el artículo 28, numeral 1º del Reglamento Operativo, se ha determinado la condición de poseedor y ocupante, estableciendo en este caso que {SQL.exe_sql_1()[0][1]} ocupa(n) el predio desde hace {num2words(object_agro.info("TIEMPO_OCUPACION"), lang = 'es')} {object_agro.info("TIEMPO_OCUPACION")} años y ejerce(n) una explotación de {UAF.cultivos(object_agro.info("CULTIVOS"), object_agro.info("CULTIVOS_%"))}
            Respecto de la información de cruces con bases de datos de los solicitantes, la Subdirección de Acceso a Tierras por Demanda y Descongestión – SATDD, solicitó a la Subdirección de Sistemas de Información de Tierras – SSIT mediante memorandos 20234200091813 del 31 de marzo de 2023 y 20234200106273 del 15 de abril de 2023, la valoración e inclusión en el RESO de {SQL.exe_sql_1()[0][1]}.
            En consecuencia, la definición de inclusión ó no de los potenciales beneficiarios al RESO será confirmada con fundamento en estas valoraciones, es decir, si es procedente ó no la adjudicación del predio {SQL.exe_sql()[0][4]} a {persona.sex_interesado()} en el informe técnico jurídico definitivo. Esta situación se establece con fundamento en el artículo 38 del Reglamento Operativo.
            Se concluye entonces que la solicitud cumple con los requisitos objetivos para adjudicación del predio denominado {SQL.exe_sql()[0][4]} y en consecuencia, se comunica que es viable continuar con la etapa de apertura del trámite administrativo del Procedimiento Único de Reconocimiento de Derecho del predio {SQL.exe_sql()[0][4]}, ubicado en el municipio {OP_GEO.intersect_layers_F(lyr_mun, 'NOMBRE_MUN')[0]}, departamento {OP_GEO.intersect_layers_F(lyr_dep, 'NOMBRE_DEP')[0]} {persona.names_interesados()} de conformidad con el artículo 32 de la Resolución 20230010000036 del 12 de abril de 2023.""" 
            #print(con_juridico)
            sheet['B62'] = con_juridico
            path_out = f'Tec/{ID}.xlsx'
            ITJP.save(path_out)
        
        FP_= time.time()
        print(f'Tiempo final de ejecución {round((FP_-BP)/60,2)} minutos')
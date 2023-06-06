import os
import osgeo.ogr
import json
from OP_geographic import OP_geographic
from num2words import num2words
from osgeo import ogr, osr
import osgeo.ogr
import shapely.wkb
from SQL_LADM import SQL_LADM 
from datetime import datetime, timedelta
from BIP import BIP 
from Agricola import agricola


with open('paths.json') as file:
            # Load the JSON data
            data = json.load(file)

class Restricciones_condiciones:

    def __init__(self, objetct_XTF):
        
        self.name_lyrs = []
        self.object_XTF = objetct_XTF
        self.string = ''
        self.union_geom = osgeo.ogr.Geometry(osgeo.ogr.wkbGeometryCollection)
        self.final_geom = osgeo.ogr.Geometry(osgeo.ogr.wkbGeometryCollection)
        self.lyr_restricciones = []
        self.poly_intersect = []
        self.intersection = 0
        self.Suma_area = 0  
        self.strg = ''            

    def condiciones(self, list_lyrs):
    
        for i in list_lyrs:
            self.name_lyrs.append(os.path.splitext(os.path.basename(i.GetName()))[0])
  
        if len(list_lyrs) > 1:
            self.string = ', '.join(self.name_lyrs[:-1]) + ' y ' + self.name_lyrs[-1]
        else:
            self.string = self.name_lyrs[0]

        return self.string 

    def A_restricciones(self,list_lyrs):
      
        for i in list_lyrs:
            object_geographic = OP_geographic(self.object_XTF)
            if os.path.splitext(os.path.basename(i.GetName()))[0] == 'SOLICITUD_INGRESO_RTDAF':
                self.intersection = object_geographic.intersect_layers_FA(i, 'estado_tra', 'Sentencia')[0]
                if self.intersection > 0:
                    self.lyr_restricciones.append(os.path.splitext(os.path.basename(i.GetName()))[0])
                    if isinstance(self.intersection[1],osgeo.ogr.Geometry):
                        self.poly_intersect.append(self.intersection[1])
                    else:
                        print(f"Invalid type {type(poly)} for layer {os.path.splitext(os.path.basename(i.GetName()))[0]}. Skipping...")
                # print(intersect_layers_FA(i, predio,'estado_tra', 'Sentencia')[1])
                else:
                    pass

            elif os.path.splitext(os.path.basename(i.GetName()))[0] == 'Drenaje_Sencillo_(30m)_':
                self.intersection = object_geographic.intersect_layers_DIFFFA(i, 'NOMBRE_GEO', None)
                if self.intersection[0] > 0:
                    self.lyr_restricciones.append(os.path.splitext(os.path.basename(i.GetName()))[0])
                    if isinstance(self.intersection[1], osgeo.ogr.Geometry):
                        self.poly_intersect.append(self.intersection[1])
                    else:
                        print(f"Invalid type {type(self.intersection[1])} for layer {os.path.splitext(os.path.basename(i.GetName()))[0]}. Skipping...")
                # print(type(intersect_layers_FA_dif(i,predio,'NOMBRE_GEO',None)[1]))
                else:
                    pass
        
            elif os.path.splitext(os.path.basename(i.GetName()))[0] == 'DRENAJE_DOBLE':
                self.intersection = object_geographic.intersect_layers_DIFFFA(i, 'NOMBRE_GEO',None)
                if self.intersection[0] > 0:
                    self.lyr_restricciones.append(os.path.splitext(os.path.basename(i.GetName()))[0])
                    if isinstance(self.intersection[1], osgeo.ogr.Geometry):
                        self.poly_intersect.append(self.intersection[1])
                    else:
                        print(f"Invalid type {type(self.intersection[1])} for layer {os.path.splitext(os.path.basename(i.GetName()))[0]}. Skipping...")
                # print(type(intersect_layers_FA_dif(i,predio,'NOMBRE_GEO',None)[1]))
                else:
                    pass

            elif os.path.splitext(os.path.basename(i.GetName()))[0] == 'remocion_en_masa':
                self.intersection = object_geographic.intersect_layers_FA(i,'CATAME','Alta')
                if self.intersection[0] > 0:
                    self.lyr_restricciones.append(os.path.splitext(os.path.basename(i.GetName()))[0])
                    if isinstance(self.intersection,osgeo.ogr.Geometry):
                        self.poly_intersect.append(self.intersection[1])
                    else:
                        print(f"Invalid type {type(self.intersection[1])} for layer {os.path.splitext(os.path.basename(i.GetName()))[0]}. Skipping...")
                # print(type(intersect_layers_FA(i,predio,'CATAME','Alta')[1]))
                else:
                    pass
            elif os.path.splitext(os.path.basename(i.GetName()))[0] == 'remocion_en_masa':
                self.intersection = object_geographic.intersect_layers_FA('CATAME','Muy Alta')
                if self.intersection[0] > 0:
                    self.lyr_restricciones.append(os.path.splitext(os.path.basename(i.GetName()))[0])
                    if isinstance(self.lyr_restricciones,osgeo.ogr.Geometry):
                        self.poly_intersect.append(self.intersection[1])
                    else:
                        print(f"Invalid type {type(poly)} for layer {os.path.splitext(os.path.basename(i.GetName()))[0]}. Skipping...")
                    
                    # print(type(intersect_layers_FA(i,predio,'CATAME','Muy Alta')[1]))
                else:
                    pass
            elif os.path.splitext(os.path.basename(i.GetName()))[0] != 'remocion_en_masa' and os.path.splitext(os.path.basename(i.GetName()))[0] != 'Drenaje_Sencillo_(30m)_' and  os.path.splitext(os.path.basename(i.GetName()))[0] != 'SOLICITUD_INGRESO_RTDAF' and object_geographic.intersect_layers_A(i)[0] > 0:
                self.lyr_restricciones.append(os.path.splitext(os.path.basename(i.GetName()))[0])
                poly = object_geographic.intersect_layers_A(i)[1]
                if isinstance(poly,osgeo.ogr.Geometry):
                    self.poly_intersect.append(poly)
                else:
                    print(f"Invalid type {type(poly)} for layer {os.path.splitext(os.path.basename(i.GetName()))[0]}. Skipping...")
                # print(type(intersect_layers_A(i,object_XTF)[1]))
            else:
                pass
            
            
            self.lyr_restricciones = list(set(self.lyr_restricciones))
            for geom in self.poly_intersect:
                self.union_geom = self.union_geom.Union(geom)

            self.Suma_area = self.union_geom.Area()/10000

            if len(self.lyr_restricciones) > 0:
                #AU = self.object_XTF - self.Suma_area
                strg = f"""cuenta con las siguientes restricciones ambientales o de Ley: {', '.join(self.lyr_restricciones[:-1]) + ' y ' + self.lyr_restricciones[-1]} \n \nAsí las cosas, se tiene que el área que se superpone con estas prohibiciones o restricciones legales corresponde a {(num2words(round((int(self.Suma_area))), lang = 'es')).upper()} HECTÁREAS {(num2words(round((float(self.Suma_area) - int(self.Suma_area))*10000,2), lang = 'es')).upper()} METROS CUADRADOS ({round((int(self.Suma_area)))}Ha + {round((float(self.Suma_area) - int(self.Suma_area))*10000,2)}m2). """
                strg = strg + f"""En virtud de estos traslapes, la titulación del 100% del área solicitada queda supeditada a la respuesta que emita la entidad correspondiente."""
        ##El área del predio afectada por estas restricciones corresponde a {(num2words(round((int(Suma_area))), lang = 'es')).upper()} HECTÁREAS {(num2words(round((float(AU) - int(Suma_area))*10000,2), lang = 'es')).upper()} METROS CUADRADOS ({round((int(Suma_area)))}Ha + {round((float(Suma_area) - int(Suma_area))*10000,2)}m2)
            else: 
                strg = 'NO cuenta con traslapes o restricciones ambientales de Ley'

        return self.Suma_area, self.strg


class conceptos:

    def __init__(self, ID):
        self.ID = ID 
    
    def concepto_juridico():
        
        
        pass


    def concepto_catastral(self):
        SQL = SQL_LADM("localhost", "ladm_ttsp", "postgres", "1234", self.ID)
        
        spatial_reference = osr.SpatialReference()
        spatial_reference.ImportFromEPSG(9377)
        shapely_obj = shapely.wkb.loads(SQL.exe_sql()[0][5])
        predio = ogr.CreateGeometryFromWkt(shapely_obj.wkt)
        predio.AssignSpatialReference(spatial_reference)
         
        RECO = Restricciones_condiciones(predio)
        OP_GEO = OP_geographic(predio)
        driver = ogr.GetDriverByName('ESRI Shapefile')
        lyr_dep = driver.Open(data[0]["lyr_dep"])
        lyr_mun = driver.Open(data[0]["lyr_mun"])
        object_agro = BIP(data[1]["agronomia"], self.ID)
        object_juri = BIP(data[1]["juridico"], self.ID)          
                    
        date_ = str(object_agro.info("FECHA_INSPECCION_OCULAR"))
        truncated_time_string = date_[:26]  
        date_ = datetime.strptime(truncated_time_string, '%Y-%m-%dT%H:%M:%S.%f') 
        date = date_.strftime('%d/%m/%Y')
         
        excel_start_date = datetime(1900, 1, 1)
        date_ = int(object_juri.info("FECHA_LEVANTAMIENTO_TOPOGRAFICO"))
        delta = timedelta(days = date_)
        date_ = excel_start_date + delta 
        date_LV = date_.strftime('%d/%m/%Y')
        date_ = datetime.strptime(str(object_juri.info("FECHA_FORMATO AGRONOMIA")), '%d/%m/%Y')
        date_FA = date_.strftime('%d/%m/%Y')
        date_ = str(object_juri.info("F-007"))
        truncated_time_string = date_[:26]  
        date_ = datetime.strptime(truncated_time_string, '%d/%m/%Y') 
        date_F007 = date_.strftime('%d/%m/%Y')
        lyr_condiciones = []
        lyr_restricciones = [] 
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
        
        lyr_l2 = driver.Open('Layers/Ley2.shp')
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
        con_catastral = f"""De acuerdo con la información recaudada a través del método indirecto de mesas colaborativas se determinó que el predio denominado {SQL.exe_sql()[0][4]}, ubicado en el departamento de {OP_GEO.intersect_layers_F(lyr_dep, 'NOMBRE_DEP')[0]}, municipio de {OP_GEO.intersect_layers_F(lyr_mun, 'NOMBRE_MUN')[0]}, vereda {object_agro.info("VEREDA").upper()}, cuenta con un área según el plano topográfico de {(num2words(round((int(SQL.exe_sql()[0][1]))), lang = 'es')).upper()} HECTÁREAS {(num2words(round((float(SQL.exe_sql()[0][1]) - int(SQL.exe_sql()[0][1]))*10000,2), lang = 'es')).upper()} METROS CUADRADOS ({round((int(SQL.exe_sql()[0][1])))}Ha + {round((float(SQL.exe_sql()[0][1]) - int(SQL.exe_sql()[0][1]))*10000,2)}m2). Que el {date_F007}, el grupo de topografía de la ANT, elaboró el cruce de información geográfica (F-007), y/o análisis espacial y cuya conclusión respecto del predio objeto de solicitud es que {RECO.A_restricciones(lyr_restricciones)[1]} \n \nIgualmente, se informa que el predio denominado {SQL.exe_sql()[0][4]}, se traslapa con los siguientes componentes condicionantes:{RECO.condiciones(lyr_condiciones)}. Sin embargo, estas no afectan el área potencial y/o útil de titulación del predio."""
            
        return con_catastral
    
    
    def concepto_agronomico(self):
        
        SQL = SQL_LADM("localhost", "ladm_ttsp", "postgres", "1234", self.ID)
        object_agro = BIP(data[1]["agronomia"], self.ID)
        date_ = str(object_agro.info("FECHA_INSPECCION_OCULAR"))
        truncated_time_string = date_[:26]  
        date_ = datetime.strptime(truncated_time_string, '%Y-%m-%dT%H:%M:%S.%f') 
        date = date_.strftime('%d/%m/%Y')

        UAF = agricola(SQL.exe_sql()[0][1])

        spatial_reference = osr.SpatialReference()
        spatial_reference.ImportFromEPSG(9377)
        shapely_obj = shapely.wkb.loads(SQL.exe_sql()[0][5])
        predio = ogr.CreateGeometryFromWkt(shapely_obj.wkt)
        predio.AssignSpatialReference(spatial_reference)
         
        RECO = Restricciones_condiciones(predio)
        OP_GEO = OP_geographic(predio)

        

        driver = ogr.GetDriverByName('ESRI Shapefile')
        lyr_dep = driver.Open(data[0]["lyr_dep"])
        lyr_mun = driver.Open(data[0]["lyr_mun"])
        con_agronomia = f"""De acuerdo a la información recaudada a través del método indirecto de mesas colaborativas, se determinó que para la zona donde está ubicado el predio, se presenta un régimen de lluvias monomodal y condiciones de suelos con textura mayormente arcillosa y ph  fuertemente ácidos, bajos contenidos de materia orgánica y condiciones productivas aptas para determinados cultivos y ganadería bovina y bufalina. \n \nAdemás, se tiene que el predio denominado {SQL.exe_sql()[0][4]}, ubicado en el departamento de {OP_GEO.intersect_layers_F(lyr_dep, 'NOMBRE_DEP')[0]}, municipio de {OP_GEO.intersect_layers_F(lyr_mun, 'NOMBRE_MUN')[0]}, vereda {object_agro.info("VEREDA").upper()},cuenta con un área según el plano topográfico de {(num2words(round((int(SQL.exe_sql()[0][1]))), lang = 'es')).upper()} HECTÁREAS {(num2words(round((float(SQL.exe_sql()[0][1]) - int(SQL.exe_sql()[0][1]))*10000,2), lang = 'es')).upper()} METROS CUADRADOS ({round((int(SQL.exe_sql()[0][1])))}Ha + {round((float(SQL.exe_sql()[0][1]) - int(SQL.exe_sql()[0][1]))*10000,2)}m2), el cual está siendo ocupado hace {object_agro.info("TIEMPO_OCUPACION")} años, por {SQL.exe_sql_1()[0][1]} solicitante de manera directa, que a su vez realiza una explotación de {UAF.cultivos(object_agro.info("CULTIVOS"), object_agro.info("CULTIVOS_%"))}. \n \nSegún la inspección ocular realizada (Formato ANT - ACCTI-F-116), realizada el {date}, en el predio no se evidencia ningún tipo de situaciones de riesgo o condiciones tales como remociones en masa de tierra, crecientes súbitas o pendientes mayores a 45° que representen peligro para la integridad de {SQL.exe_sql_1()[0][1]} ocupantes. \n \nDesde el componente ambiental no se observan limitantes que afecten los recursos naturales, el medio ambiente ni la zona productiva del predio. \n \nBajo estas condiciones, el grupo de Agronomía a cargo de esta evaluación determinó el cálculo de UAF con propuesta de producción de {UAF.def_uaf()[2]}. Resultado de esta propuesta se estableció un rango de área para obtener entre 2 a 2.5 smmlv de {int(UAF.def_uaf()[0])}Ha + {round((float(UAF.def_uaf()[0]) - int(UAF.def_uaf()[0]))*10000,3)}m2 a {int(UAF.def_uaf()[1])}Ha + {round((float(UAF.def_uaf()[1]) - int(UAF.def_uaf()[1]))*10000,3)}. Con lo anterior, se establece que el predio está {UAF.def_uaf()[3]} rango de la UAF mencionada, con la capacidad de producir {UAF.def_uaf()[4]} smmlv, en la actualidad. \n \nEn consecuencia, de lo explicado anteriormente, desde el componente agronómico de la Subdirección de Acceso a Tierras por Demanda y Descongestión se recomienda continuar con el proceso de adjudicación del predio. """
        pass


# vector_ID =['5035000247']

# objecto = conceptos(vector_ID)

# v = objecto.concepto_agronomico()



from docxtpl import DocxTemplate
import json
from BIP import BIP
from SQL_LADM import SQL_LADM
from dates import dates
from num2words import num2words
from OP_geographic import OP_geographic
import shapely.wkb
from osgeo import ogr, osr
from Agricola import agricola
from Restric_conditions import Restricciones_condiciones
from ITJP_ import ITJP
from interesado import interesado

class Resolucion:

    def __init__(self, vector_ID):
        self.context = {}
        self.vector_ID = vector_ID
        pass


    def fill_out_Resolucion(self):

        # Object_ITJP = ITJP(self.vector_ID)
        # ITJP.ITJP(self.vector_ID)

        

        with open('paths.json') as file:
            # Load the JSON data
            data = json.load(file)
        
        for ID in self.vector_ID:

            SQL = SQL_LADM("localhost", "ladm_ttsp", "postgres", "1234", ID) 
            spatial_reference = osr.SpatialReference()
            spatial_reference.ImportFromEPSG(9377)
            shapely_obj = shapely.wkb.loads(SQL.exe_sql()[0][5])
            predio = ogr.CreateGeometryFromWkt(shapely_obj.wkt)
            predio.AssignSpatialReference(spatial_reference)
            area_predio = SQL.exe_sql()[0][1]

            UAF = agricola(area_predio)

            persona = interesado(SQL.exe_sql_1())
            
            driver = ogr.GetDriverByName('ESRI Shapefile')
            lyr_dep = driver.Open(data[0]["lyr_dep"])
            lyr_mun = driver.Open(data[0]["lyr_mun"])
            lyr_Terreno = driver.Open(data[0]["lyr_Terreno"])

            fechas = dates()

            # RECO = Restricciones_condiciones(predio)
            
            object_juri = BIP(data[1]["juridico"], ID)
            object_agro = BIP(data[1]["agronomia"], ID)
            OP_GEO = OP_geographic(predio)

            print(f'Resolución {ID}')
            doc = DocxTemplate(data[1]["template_Resolucion"])
                    
            if len(SQL.exe_sql_2()) == 2:  
                names_sol = f"""{SQL.exe_sql_2()[0][7]} y {SQL.exe_sql_2()[1][7]}"""
                cedula_sol = f"""{SQL.exe_sql_2()[0][6]} y No. {SQL.exe_sql_2()[1][6]}, respectivamente"""
                self.context.update({"Nombre_Solicitante": names_sol})
                self.context.update({"Cedula_solicitante" : cedula_sol})
            
            elif len(SQL.exe_sql_2()) == 1:
                names_sol = SQL.exe_sql()[0][2]
                cedula_sol = SQL.exe_sql()[0][3]
                self.context.update({"Nombre_Solicitante": names_sol})               
                self.context.update({"Cedula_solicitante" : cedula_sol}) ##separar miles
            
            else:
                print('Warning: Predio > 2 interesados')

            pass  

            

            intersection = OP_GEO.intersect_layers_F(lyr_Terreno, "codigo")
            if len(intersection) > 1:        
                Terreno = ' y '.join(intersection)
            else:
                Terreno = intersection[0]           
            
            date = object_agro.info("FECHA_INSPECCION_OCULAR")
            date_F007 = fechas.date2text(object_juri.info("F-007"))            
            
            self.context.update({"ID_BARRIDO": SQL.exe_sql()[0][0]})
            self.context.update({"No_Auto": int(object_juri.info("No_AUTO"))})
            self.context.update({"Expediente": object_juri.info("EXPEDIENTE")})
            self.context.update({"FECHA_AUTO": fechas.date2text(object_juri.info("FECHA_AUTO"))})
            self.context.update({"Nombre_Predio": SQL.exe_sql()[0][4]})
            self.context.update({"Departamento": OP_GEO.intersect_layers_F(lyr_dep, 'NOMBRE_DEP')[0].capitalize()})
            
            self.context.update({"Municipio": fechas.convert_Cap(OP_GEO.intersect_layers_F(lyr_mun, 'NOMBRE_MUN')[0])}) ##Dos palabras dos mayusculas
            self.context.update({"Vereda": fechas.convert_Cap(object_agro.info("VEREDA"))}) ##Dos palabras dos mayusculas
            self.context.update({"No_FOLIOS_AA": int(object_juri.info("No_FOLIOS_AA"))})
            self.context.update({"No_Resolutiva": object_juri.info("No_Resolutiva")})
            self.context.update({"Nombre_proyecta": object_juri.info("PROYECTÓ")})
            self.context.update({"Nombre_revisa": object_juri.info("REVISÓ")})
            self.context.update({"Nombre_aprobo": object_juri.info("APROBÓ")})
            self.context.update({"email_not": object_juri.info("EMAIL_NOT")})
            self.context.update({"No_FISO": int(object_juri.info("No_FISO"))})
            self.context.update({"FECHA_FISO": fechas.date2text(object_juri.info("FECHA_FISO"))})
            self.context.update({"Email_Notificacion": object_juri.info("Email_Notificacion")})
            self.context.update({"Definicion_UAF": f"{num2words(int(UAF.def_uaf()[0]), lang='es').upper()} HECTAREAS CON {num2words(round((float(UAF.def_uaf()[0]) - int(UAF.def_uaf()[0]))*10000,3), lang = 'es').upper()} METROS CUADRADOS ({int(UAF.def_uaf()[0])}Ha + {round((float(UAF.def_uaf()[0]) - int(UAF.def_uaf()[0]))*10000,3)}m2) a {num2words(int(UAF.def_uaf()[1]), lang='es').upper()} HECTAREAS CON {num2words(round((float(UAF.def_uaf()[1]) - int(UAF.def_uaf()[1]))*10000,3), lang = 'es').upper()} METROS CUADRADOS ({int(UAF.def_uaf()[1])}Ha + {round((float(UAF.def_uaf()[1]) - int(UAF.def_uaf()[1]))*10000,3)}m2)"})
            self.context.update({"Definicion_UAF_NUM": f"{int(UAF.def_uaf()[0])}Ha + {round((float(UAF.def_uaf()[0]) - int(UAF.def_uaf()[0]))*10000,3)}m2 a {int(UAF.def_uaf()[1])}Ha + {round((float(UAF.def_uaf()[1]) - int(UAF.def_uaf()[1]))*10000,3)}"})
            self.context.update({"Rango_UAF": UAF.def_uaf()[4]})
            self.context.update({"Producto_UAF": UAF.def_uaf()[2]})
            self.context.update({"UAF_IN_OUT": UAF.def_uaf()[3]})
            self.context.update({"AREA_PREDIO": f"{num2words(int(area_predio), lang='es').upper()} HECTAREAS CON {num2words(round((float(area_predio) - int(area_predio))*10000,3), lang = 'es').upper()} METROS CUADRADOS ({int(area_predio)}Ha + {round((float(area_predio) - int(area_predio))*10000,3)}m2)"})
            self.context.update({"AREA_PREDIO_NUM": f"{int(area_predio)} Has, {round((float(area_predio) - int(area_predio))*10000,3)} m2"})
            self.context.update({"FECHA_F007": date_F007})
            self.context.update({"FECHA_ITJP": fechas.date2text(object_juri.info("F_ITJP"))})
            self.context.update({"CCatastral": Terreno})
            self.context.update({"Oficio_ORIP": int(object_juri.info("Oficio_ORIP"))})
            self.context.update({"Fecha_Oficio_ORIP": object_juri.info("FECHA_Oficio_ORIP")})
            self.context.update({"Oficio_SI": int(object_juri.info("Oficio_SI"))})
            self.context.update({"Fecha_Oficio_SI": fechas.date2text(object_juri.info("Fecha_Oficio_SI"))})
            self.context.update({"Oficio_URT": int(object_juri.info("Oficio_URT"))})
            self.context.update({"Fecha_Oficio_URT": fechas.date2text(object_juri.info("Fecha_Oficio_URT"))})
            self.context.update({"Oficio_Web": int(object_juri.info("Oficio_Web"))})
            self.context.update({"Fecha_Oficio_Web": fechas.date2text(object_juri.info("Fecha_Oficio_Web"))})
            self.context.update({"Minsiterio_Publico": object_juri.info("Minsiterio_Publico")})
            self.context.update({"Fecha_Minsiterio_Publico": fechas.date2text(object_juri.info("Fecha_Ministerio_público"))})
            self.context.update({"Concepto_agronomico": f"""De acuerdo a la información recaudada a través del método indirecto de mesas colaborativas, se determinó que para la zona donde está ubicado el predio, se presenta un régimen de lluvias monomodal y condiciones de suelos con textura mayormente arcillosa y ph  fuertemente ácidos, bajos contenidos de materia orgánica y condiciones productivas aptas para determinados cultivos y ganadería bovina y bufalina. \n \nAdemás, se tiene que el predio denominado {SQL.exe_sql()[0][4]}, ubicado en el departamento de {OP_GEO.intersect_layers_F(lyr_dep, 'NOMBRE_DEP')[0]}, municipio de {OP_GEO.intersect_layers_F(lyr_mun, 'NOMBRE_MUN')[0]}, vereda {object_agro.info("VEREDA").upper()},cuenta con un área según el plano topográfico de {(num2words(round((int(SQL.exe_sql()[0][1]))), lang = 'es')).upper()} HECTÁREAS {(num2words(round((float(SQL.exe_sql()[0][1]) - int(SQL.exe_sql()[0][1]))*10000,2), lang = 'es')).upper()} METROS CUADRADOS ({round((int(SQL.exe_sql()[0][1])))}Ha + {round((float(SQL.exe_sql()[0][1]) - int(SQL.exe_sql()[0][1]))*10000,2)}m2), el cual está siendo ocupado hace {object_agro.info("TIEMPO_OCUPACION")} años, por {persona.sex_interesado()} solicitante de manera directa, que a su vez realiza una explotación de {UAF.cultivos(object_agro.info("CULTIVOS"), object_agro.info("CULTIVOS_%"))}. \n \nSegún la inspección ocular realizada (Formato ANT - ACCTI-F-116), realizada el {date}, en el predio no se evidencia ningún tipo de situaciones de riesgo o condiciones tales como remociones en masa de tierra, crecientes súbitas o pendientes mayores a 45° que representen peligro para la integridad de {SQL.exe_sql_1()[0][1]} ocupantes. \n \nDesde el componente ambiental no se observan limitantes que afecten los recursos naturales, el medio ambiente ni la zona productiva del predio. \n \nBajo estas condiciones, el grupo de Agronomía a cargo de esta evaluación determinó el cálculo de UAF con propuesta de producción de {UAF.def_uaf()[2]}. Resultado de esta propuesta se estableció un rango de área para obtener entre 2 a 2.5 smmlv de {int(UAF.def_uaf()[0])}Ha + {round((float(UAF.def_uaf()[0]) - int(UAF.def_uaf()[0]))*10000,3)}m2 a {int(UAF.def_uaf()[1])}Ha + {round((float(UAF.def_uaf()[1]) - int(UAF.def_uaf()[1]))*10000,3)}. Con lo anterior, se establece que el predio está {UAF.def_uaf()[3]} rango de la UAF mencionada, con la capacidad de producir {UAF.def_uaf()[4]} smmlv, en la actualidad. \n \nEn consecuencia, de lo explicado anteriormente, desde el componente agronómico de la Subdirección de Acceso a Tierras por Demanda y Descongestión se recomienda continuar con el proceso de adjudicación del predio. """})
            # self.context.update({"Concepto_catastral": f"""De acuerdo con la información recaudada a través del método indirecto de mesas colaborativas se determinó que el predio denominado {SQL.exe_sql()[0][4]}, ubicado en el departamento de {OP_GEO.intersect_layers_F(lyr_dep, 'NOMBRE_DEP')[0]}, municipio de {OP_GEO.intersect_layers_F(lyr_mun, 'NOMBRE_MUN')[0]}, vereda {object_agro.info("VEREDA").upper()}, cuenta con un área según el plano topográfico de {(num2words(round((int(SQL.exe_sql()[0][1]))), lang = 'es')).upper()} HECTÁREAS {(num2words(round((float(SQL.exe_sql()[0][1]) - int(SQL.exe_sql()[0][1]))*10000,2), lang = 'es')).upper()} METROS CUADRADOS ({round((int(SQL.exe_sql()[0][1])))}Ha + {round((float(SQL.exe_sql()[0][1]) - int(SQL.exe_sql()[0][1]))*10000,2)}m2). Que el {date_F007}, el grupo de topografía de la ANT, elaboró el cruce de información geográfica (F-007), y/o análisis espacial y cuya conclusión respecto del predio objeto de solicitud es que {RECO.A_restricciones(ITJP.ITJP(self.vector_ID)[0])[1]} \n \nIgualmente, se informa que el predio denominado {SQL.exe_sql()[0][4]}, se traslapa con los siguientes componentes condicionantes:{RECO.condiciones(ITJP.ITJP(self.vector_ID)[0])}. Sin embargo, estas no afectan el área potencial y/o útil de titulación del predio."""})

      

        doc.render(self.context)
        doc.save('Source_Concepts/generated.docx')
        
        pass


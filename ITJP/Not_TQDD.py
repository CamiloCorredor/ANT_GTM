from docxtpl import DocxTemplate
import json
from BIP import BIP
from SQL_LADM import SQL_LADM
from dates import dates
from OP_geographic import OP_geographic
import shapely.wkb
from osgeo import ogr, osr

class Not_TQDD:

    def __init__(self, vector_ID):
        self.context = {}
        self.vector_ID = vector_ID
        pass


    def fill_out_Publish(self):

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

            driver = ogr.GetDriverByName('ESRI Shapefile')
            lyr_dep = driver.Open(data[0]["lyr_dep"])
            lyr_mun = driver.Open(data[0]["lyr_mun"])

            fechas = dates()
            
            object_juri = BIP(data[1]["juridico"], ID)
            object_agro = BIP(data[1]["agronomia"], ID)
            OP_GEO = OP_geographic(predio)

            print(f'Publicación o Notificación a Terceros de Quienes se desconoce su domicilio {ID}')
            doc = DocxTemplate(data[1]["template_Not_TQDD"])
                    
            if len(SQL.exe_sql_2()) == 2:  
                names_sol = f"""{SQL.exe_sql_2()[0][7]} y {SQL.exe_sql_2()[1][7]}"""
                cedula_sol = f"""{SQL.exe_sql_2()[0][6]} y No. {SQL.exe_sql_2()[1][6]}, respectivamente"""
                self.context.update({"Nombre_Solicitante": names_sol})
                self.context.update({"Cedula_solicitante" : cedula_sol})
            
            elif len(SQL.exe_sql_2()) == 1:
                names_sol = SQL.exe_sql()[0][2]
                cedula_sol = SQL.exe_sql()[0][3]
                self.context.update({"Nombre_Solicitante": names_sol})               
                self.context.update({"Cedula_solicitante" : cedula_sol})
            
            else:
                print('Warning: Predio > 2 interesados')

            pass
            
            self.context.update({"No_Auto": int(object_juri.info("No_AUTO"))})
            self.context.update({"Expediente": object_juri.info("EXPEDIENTE")})
            self.context.update({"FECHA_AUTO": fechas.date2text(object_juri.info("FECHA_AUTO"))})
            self.context.update({"Nombre_Predio": SQL.exe_sql()[0][4]})
            self.context.update({"Departamento": OP_GEO.intersect_layers_F(lyr_dep, 'NOMBRE_DEP')[0]})
            self.context.update({"Municipio": OP_GEO.intersect_layers_F(lyr_mun, 'NOMBRE_MUN')[1]})
            self.context.update({"Vereda": object_agro.info("VEREDA")})
            self.context.update({"No_FOLIOS_AA": int(object_juri.info("No_FOLIOS_AA"))})
            self.context.update({"No_Resolutiva": object_juri.info("No_Resolutiva")})
            self.context.update({"Nombre_proyecta": object_juri.info("PROYECTÓ")})
            self.context.update({"Nombre_revisa": object_juri.info("REVISÓ")})
            self.context.update({"Nombre_aprobo": object_juri.info("APROBÓ")})
            self.context.update({"email_not": object_juri.info("EMAIL_NOT")})
            self.context.update({"No_FISO": int(object_juri.info("No_FISO"))})
            self.context.update({"FECHA_FISO": fechas.date2text(object_juri.info("FECHA_FISO"))})
            self.context.update({"Email_Notificacion": object_juri.info("Email_Notificacion")})

        doc.render(self.context)
        doc.save('Source_Concepts/generated.docx')
        
        pass


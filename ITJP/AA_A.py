from docxtpl import DocxTemplate
import json
from BIP import BIP
from SQL_LADM import SQL_LADM
from dates import dates
from OP_geographic import OP_geographic
import shapely.wkb
from osgeo import ogr, osr

class A3:

    def __init__(self, vector_ID):
        self.context = {}
        self.vector_ID = vector_ID
        pass


    def fill_out_Not_A2(self):

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

            print(f'Informe Técnico Jurídico Preliminar {ID}')
            doc = DocxTemplate(data[1]["template_AA_A"])
                    
            if len(SQL.exe_sql_2()) == 2:  
                names_sol = f"""{SQL.exe_sql_2()[0][7]} y {SQL.exe_sql_2()[1][7]}"""
                self.context.update({"Nombre_Solicitante": names_sol})
                print(self.context)
            
            elif len(SQL.exe_sql_2()) == 1:
                names_sol = SQL.exe_sql()[0][2]
                self.context.update({"Nombre_Solicitante": names_sol})
                
            
            else:
                print('Warning: Predio > 2 interesados')

            pass

            self.context.update({"No_Auto": int(object_juri.info("No_AUTO"))})
            self.context.update({"Expediente": object_juri.info("EXPEDIENTE")})
            self.context.update({"FECHA_AUTO": fechas.date2text(object_juri.info("FECHA_AUTO"))})
            self.context.update({"Nombre_Predio": SQL.exe_sql()[0][4]})
            self.context.update({"Departamento": OP_GEO.intersect_layers_F(lyr_dep, 'NOMBRE_DEP')[0]})
            self.context.update({"Municipio": OP_GEO.intersect_layers_F(lyr_mun, 'NOMBRE_MUN')[0]})
            self.context.update({"Vereda": object_agro.info("VEREDA")})
            self.context.update({"No_FOLIOS_AA": int(object_juri.info("No_FOLIOS_AA"))})
            self.context.update({"No_Resolutiva": object_juri.info("No_Resolutiva")})
            self.context.update({"Nombre_proyecta": object_juri.info("PROYECTÓ")})
            self.context.update({"Nombre_revisa": object_juri.info("REVISÓ")})
            self.context.update({"Nombre_aprobo": object_juri.info("APROBÓ")})
            self.context.update({"email_not": object_juri.info("EMAIL_NOT")})

        doc.render(self.context)
        doc.save('Source_Concepts/generated.docx')
        
        pass


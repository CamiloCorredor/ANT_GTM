import os
import osgeo.ogr
from OP_geographic import OP_geographic
from num2words import num2words 

class Restricciones_condiciones:

    def __init__(self, list_lyrs, objetct_XTF):
        self.list_lyrs = list_lyrs
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

    def condiciones(self):
    
        for i in self.list_lyrs:
            self.name_lyrs.append(os.path.splitext(os.path.basename(i.GetName()))[0])
  
        if len(self.list_lyrs) > 1:
            self.string = ', '.join(self.name_lyrs[:-1]) + ' y ' + self.name_lyrs[-1]
        else:
            self.string = self.name_lyrs[0]

        return self.string 

    def A_restricciones(self):
      
        for i in self.list_lyrs:
            object_geographic = OP_geographic(self.object_XTF,i)
            if os.path.splitext(os.path.basename(i.GetName()))[0] == 'SOLICITUD_INGRESO_RTDAF':
                self.intersection = object_geographic.intersect_layers_FA('estado_tra', 'Sentencia')[0]
                if self.intersection[0] > 0:
                    self.lyr_restricciones.append(os.path.splitext(os.path.basename(i.GetName()))[0])
                    if isinstance(self.intersection[1],osgeo.ogr.Geometry):
                        self.poly_intersect.append(self.intersection[1])
                    else:
                        print(f"Invalid type {type(poly)} for layer {os.path.splitext(os.path.basename(i.GetName()))[0]}. Skipping...")
                # print(intersect_layers_FA(i, predio,'estado_tra', 'Sentencia')[1])
                else:
                    pass

            elif os.path.splitext(os.path.basename(i.GetName()))[0] == 'Drenaje_Sencillo_(30m)_':
                self.intersection = object_geographic.intersect_layers_DIFFFA('NOMBRE_GEO', 'None')
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
                self.intersection = object_geographic.intersect_layers_DIFFA('NOMBRE_GEO',None)
                if self.intersection[0] > 0:
                    self.lyr_restricciones.append(os.path.splitext(os.path.basename(i.GetName()))[0])
                    if isinstance(self.intersection[1], osgeo.ogr.Geometry):
                        self.poly_intersect.append(self.intersection[1])
                    else:
                        print(f"Invalid type {type(poly)} for layer {os.path.splitext(os.path.basename(i.GetName()))[0]}. Skipping...")
                # print(type(intersect_layers_FA_dif(i,predio,'NOMBRE_GEO',None)[1]))
                else:
                    pass

            elif os.path.splitext(os.path.basename(i.GetName()))[0] == 'remocion_en_masa':
                self.intersection = object_geographic.intersect_layers_FA('CATAME','Alta')
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
            elif os.path.splitext(os.path.basename(i.GetName()))[0] != 'remocion_en_masa' and os.path.splitext(os.path.basename(i.GetName()))[0] != 'Drenaje_Sencillo_(30m)_' and  os.path.splitext(os.path.basename(i.GetName()))[0] != 'SOLICITUD_INGRESO_RTDAF' and intersect_layers_A(i,object_XTF)[0] > 0:
                self.lyr_restricciones.append(os.path.splitext(os.path.basename(i.GetName()))[0])
                poly = object_geographic.intersect_layers_A()[1]
                if isinstance(poly,osgeo.ogr.Geometry):
                    self.poly_intersect.append(poly)
                else:
                    print(f"Invalid type {type(poly)} for layer {os.path.splitext(os.path.basename(i.GetName()))[0]}. Skipping...")
                # print(type(intersect_layers_A(i,object_XTF)[1]))
            else:
                pass
            
            
            self.lyr_restricciones = list(set(self.lyr_restricciones))
            for geom in self.poly_intersect:
                union_geom = union_geom.Union(geom)

            self.Suma_area = union_geom.Area()/10000

            if len(self.lyr_restricciones) > 0:
                AU = self.object_XTF - self.Suma_area
                strg = f"""cuenta con las siguientes restricciones ambientales o de Ley: {', '.join(self.lyr_restricciones[:-1]) + ' y ' + self.lyr_restricciones[-1]} \n \nAsí las cosas, se tiene que el área que se superpone con estas prohibiciones o restricciones legales corresponde a {(num2words(round((int(self.Suma_area))), lang = 'es')).upper()} HECTÁREAS {(num2words(round((float(self.Suma_area) - int(self.Suma_area))*10000,2), lang = 'es')).upper()} METROS CUADRADOS ({round((int(self.Suma_area)))}Ha + {round((float(self.Suma_area) - int(self.Suma_area))*10000,2)}m2). """
                strg = strg + f"""En virtud de estos traslapes, la titulación del 100% del área solicitada queda supeditada a la respuesta que emita la entidad correspondiente."""
        ##El área del predio afectada por estas restricciones corresponde a {(num2words(round((int(Suma_area))), lang = 'es')).upper()} HECTÁREAS {(num2words(round((float(AU) - int(Suma_area))*10000,2), lang = 'es')).upper()} METROS CUADRADOS ({round((int(Suma_area)))}Ha + {round((float(Suma_area) - int(Suma_area))*10000,2)}m2)
            else: 
                strg = 'NO cuenta con traslapes o restricciones ambientales de Ley'

        return self.Suma_area, self.strg
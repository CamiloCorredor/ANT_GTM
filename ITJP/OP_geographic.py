import osgeo.ogr

class OP_geographic:
    
    def __init__(self,object_XTF):
        
        self.object_XTF = object_XTF
        self.total_area = []
        self.intersection = []
        self.union_geom = osgeo.ogr.Geometry(osgeo.ogr.wkbGeometryCollection)
        self.final_geom = osgeo.ogr.Geometry(osgeo.ogr.wkbGeometryCollection)
        self.feature_intersects = []
        self.intersection = []

    def intersect_layers_A(self, path_layer):
        layer = path_layer.GetLayer()
        for feature in layer:
            geometry = feature.GetGeometryRef()
            intersect = geometry.Intersection(self.object_XTF)
            
            inter_tf = geometry.Intersect(self.object_XTF)
            if inter_tf == True:
                intersect_geometry = intersect.Clone()
                self.total_area.append(intersect.Area())
                self.intersection.append(intersect_geometry)
            else:
                pass

        for geom in self.intersection:
            self.union_geom = self.union_geom.Union(geom)

        return sum(self.total_area), self.union_geom.Area()


    def intersect_layers_F(self, path_layer, Field): ##Return features
        self.feature_intersects = []
        layer = path_layer.GetLayer()
        for feature in layer:     
            geometry = feature.GetGeometryRef()
            inter_tf = geometry.Intersect(self.object_XTF)
            if inter_tf:                
                self.feature_intersects.append(feature.GetField(Field))       
        else: 
            pass
        return self.feature_intersects

    def intersect_layers_FA(self,path_layer ,Field,Field_R): ##Return features y areas
        
        layer = path_layer.GetLayer()
        for feature in layer:     
            geometry = feature.GetGeometryRef()
            intersect = geometry.Intersection(self.object_XTF)

            inter_tf = geometry.Intersect(self.object_XTF)
            if inter_tf == True and feature.GetField(Field) == Field_R:
                intersect_geometry = intersect.Clone()
                self.total_area.append(intersect.Area())
                self.intersection.append(intersect_geometry)
            else:              
                pass
        for geom in self.intersection:
            self.union_geom = self.union_geom.Union(geom)

        return sum(self.total_area), self.union_geom.Area()

    def intersect_layers_DIFFFA(self,path_layer, Field,Field_R): ##Return features y areas
        
        layer = path_layer.GetLayer()
        for feature in layer:     
            geometry = feature.GetGeometryRef()
            intersect = geometry.Intersection(self.object_XTF)

            inter_tf = geometry.Intersect(self.object_XTF)
            if inter_tf == True and feature.GetField(Field) != Field_R:
                intersect_geometry = intersect.Clone()
                self.total_area.append(intersect.Area())
                self.intersection.append(intersect_geometry)
            else:              
                pass
        for geom in self.intersection:
            self.union_geom = self.union_geom.Union(geom)

        return sum(self.total_area), self.union_geom.Area()

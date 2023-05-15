import geopandas as gpd
import os

path = 'LayersDXF/'
files = os.listdir(path)

# Create an empty GeoDataFrame to store all layers
all_layers = gpd.GeoDataFrame()

for file in files:
    if file.endswith('.dxf'):
        print(file)
        layers = gpd.read_file(path + file, driver='DXF')
        for layer in layers['Layer'].unique():
            layer_df = layers[layers['Layer'] == layer]
            layer_df = layer_df.set_crs("EPSG:3115")
            
            all_layers = all_layers.append(layer_df)


all_layers.to_file('all_layers.gpkg', driver='GPKG')

print('Ejecución Finalizada')
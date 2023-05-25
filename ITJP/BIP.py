import pandas as pd

class BIP:
    
    def __init__(self, path_file, ID):
        self.path_file = path_file
        self.ID = ID
        self.valor = ''
        

    def info(self, categoria):
        path = pd.read_excel(self.path_file)
        row = path.loc[path['ID'] == int(self.ID)]
        if not row.empty:  # Verificar si se encontró alguna fila
            self.valor = row[categoria].values[0]
        else:
            self.valor = None  
    
        return self.valor
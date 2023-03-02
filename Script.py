import pandas as pd
from unidecode import unidecode

df = pd.read_excel('Name_File.xlsx')

for row in df.index:
    for column in df.columns:
        # Acceder al valor en la fila y columna actual
        if pd.isna(df.loc[row, column]):
            df.loc[row, column] = ''
        else:
            valor = df.loc[row, column]
            if isinstance(valor, str):
                valor = unidecode(valor)
            else:
                valor = str(valor)
            df.loc[row, column] = valor

df.to_excel('Modified_file.xlsx', index=False)




from ITJP_ import ITJP
from AA_A import A3
from Not_TQDD import Not_TQDD
from Resolucion import Resolucion


vector_ID =[1875302627] 

print(f"""
1. Informe Técnico Jurídico Preliminar
2. Notificación para auto administrativo de apertura
3. Publicación o Notificación a Terceros de Quienes se desconoce su domicilio
4. Resolución
""")

# user_input = input("Ingrese los documentos que requiere generar:")
user_input = int(4)
if int(user_input) == 1:
    Object_ITJP = ITJP(vector_ID)
    Object_ITJP.ITJP()

elif int(user_input) == 2:
    Object_A3 = A3(vector_ID)
    Object_A3.fill_out_Not_A2()

elif int(user_input) == 3:
    Object_Not = Not_TQDD(vector_ID)
    Object_Not.fill_out_Publish()

elif int(user_input) == 4:
    Object_Reso = Resolucion(vector_ID)
    Object_Reso.fill_out_Resolucion()


    


class agricola: 

    def __init__(self, objetc_XTF):
        self.object_XTF = objetc_XTF
        self.range = []
        

    def def_uaf(self):
        range_UAF = [7.8383,10.639,15.3069,19.6939,33.8393,42.6454,66.1033,92.4583,103.2257,129.6417,264.8417,330.3617]
        range = []

        if self.object_XTF < range_UAF[0] or self.object_XTF < range_UAF[1]:

            range.append(range_UAF[0])
            range.append(range_UAF[1])
            range.append('café y frijol')
            if self.object_XTF <= range_UAF[1] and self.object_XTF >= range_UAF[0]:
                range.append('en el')
            elif self.object_XTF <= range_UAF[0]:
                range.append('por debajo del')

            var_dif = [abs(range_UAF[0]-self.object_XTF),abs(range_UAF[1]-self.object_XTF)]
            if var_dif[1] < var_dif[0]:
                range.append(round((self.object_XTF*2.5)/range_UAF[1],2))
            else:
                range.append(round((self.object_XTF*2.5)/range_UAF[0],2))      
        ##Café frijol

        elif self.object_XTF >= range_UAF[1] and self.object_XTF <= range_UAF[3]:

            range.append(range_UAF[2])
            range.append(range_UAF[3])
            range.append('frijol y maíz')
            if self.object_XTF <= range_UAF[3] and self.object_XTF >= range_UAF[2]:
                range.append('en el')
            elif self.object_XTF <= range_UAF[2] and self.object_XTF >= range_UAF[1]:
                range.append('por debajo del')

            var_dif = [abs(range_UAF[2]-self.object_XTF),abs(range_UAF[3]-self.object_XTF)]
            if var_dif[1] < var_dif[0]:
                range.append(round((self.object_XTF*2.5)/range_UAF[3],2))
            else:
                range.append(round((self.object_XTF*2.5)/range_UAF[2],2))
                   ##FRijol - Maíz

        elif self.object_XTF >= range_UAF[3] and self.self.object_XTF <= range_UAF[5]:        
            range.append(range_UAF[4])
            range.append(range_UAF[5])
            range.append('caña y plátano')
            if self.object_XTF <= range_UAF[5] and self.object_XTF >= range_UAF[4]:
                range.append('en el')
            elif self.object_XTF <= range_UAF[4] and self.object_XTF >= range_UAF[3]:
                range.append('por debajo del')

            var_dif = [abs(range_UAF[4]-self.object_XTF),abs(range_UAF[5]-self.object_XTF)]
            if var_dif[1] < var_dif[0]:
                range.append(round((self.object_XTF*2.5)/range_UAF[5],2))
            else:
                range.append(round((self.object_XTF*2.5)/range_UAF[4],2))
            ##Caña - Plátano

        elif self.object_XTF >= range_UAF[5] and self.object_XTF <= range_UAF[7]:
            range.append(range_UAF[6])
            range.append(range_UAF[7])
            range.append('ganadería y maíz')
            if self.object_XTF <= range_UAF[7] and self.object_XTF >= range_UAF[6]:
                range.append('en el')
            elif self.object_XTF <= range_UAF[6] and self.object_XTF >= range_UAF[5]:
                range.append('por debajo del')
            var_dif = [abs(range_UAF[6]-self.object_XTF),abs(range_UAF[7]-self.object_XTF)]
            if var_dif[1] < var_dif[0]:
                range.append(round((self.object_XTF*2.5)/range_UAF[7],2))
            else:
                range.append(round((self.object_XTF*2.5)/range_UAF[6],2))
            ##Maiz Ganaderia

        elif self.object_XTF >= range_UAF[7] and self.object_XTF <= range_UAF[9]:
            range.append(range_UAF[8])
            range.append(range_UAF[9])
            range.append('ganadería de leche y ceba')
            if self.object_XTF <= range_UAF[9] and self.object_XTF >= range_UAF[8]:
                range.append('en el')
            elif self.object_XTF <= range_UAF[8] and self.object_XTF >= range_UAF[7]:
                range.append('por debajo del')

            var_dif = [abs(range_UAF[8]-self.object_XTF),abs(range_UAF[9]-self.object_XTF)]
            if var_dif[1] < var_dif[0]:
                range.append(round((self.object_XTF*2.5)/range_UAF[9],2))
            else:
                range.append(round((self.object_XTF*2.5)/range_UAF[8],2))
            ##Ganadería lechec y ganadería ceba

        elif self.object_XTF >= range_UAF[9] and self.object_XTF <= range_UAF[11] :
            range.append(range_UAF[10])
            range.append(range_UAF[11])
            range.append('ganadería extensiva')
            if self.object_XTF <= range_UAF[11] and self.object_XTF > range_UAF[10]:
                range.append('en el')
            elif self.object_XTF <= range_UAF[10] and self.object_XTF >= range_UAF[9]:
                range.append('por debajo del')
            var_dif = [abs(range_UAF[8]-self.object_XTF),abs(range_UAF[9]-self.object_XTF)]
            if var_dif[1] < var_dif[0]:
                range.append(round((self.object_XTF*2.5)/range_UAF[11],2))
            else:
                range.append(round((self.object_XTF*2.5)/range_UAF[10],2))
                ##GAnaderia extensiva
        else: 
            print('Sin clasificación')

        return range


    def cultivos(lis_t1, lis_t2):
        strg = ''              
        cultivos = lis_t1 
        cultivos_ = cultivos.split(", ")

        if len(cultivos_) >= 2:
            cultivos_porc = lis_t2
            cultivos_porc_ = cultivos_porc.split(",")
            for cultivos_, cultivos_porc_ in zip(cultivos_, cultivos_porc_):
                strg += f"{cultivos_} - {cultivos_porc_}%, "
        else:
            strg = f'{cultivos_[0]} - {lis_t2}%'
        return strg
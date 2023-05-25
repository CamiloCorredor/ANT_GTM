class interesado:
    pass

    def __init__(self,squema):
        self.squema = squema
        self.str_name = ''
        self.str_all = ''

    def sex_interesado(self):
        sex_interesado = ''
        if self.squema[0][1] == 'Femenino':
            sex_interesado = 'la interesada' 
        elif self.squema[0][1] == 'Masculino':
            sex_interesado = 'el interesado' 
        elif self.squema[0][1] == None:
            sex_interesado = 'los interesados'
        else:
            pass
        return sex_interesado

    def names_interesados(self):
        if self.squema[0][7] is None:
            self.str_name = f"solicitado por {self.sex_interesado()} {self.squema[0][2]}"
            self.str_all = self.str_name + f" con cédula de ciudadanía No {self.squema[0][3]}"
        elif self.squema[0][7] == 'Grupo civil':
            self.str_name = f"solicitado por {self.sex_interesado()} {self.squema[0][7]} y {self.squema[1][7]}"
            self.str_all = self.str_name + f" identificados con cédula de ciudadanía {self.squema[0][6]} y {self.squema[1][6]}, respectivamente"
        else: 
            print('Warning: Predio con > 2 solicitantes')
        
        return self.str_name, self.str_all

class interesado:
    pass

    def __init__(self,squema):
        self.squema = squema

    def sex_interesado(self):
        sex_interesado = ''
        if self.squema == 'Femenino':
            sex_interesado = 'la interesada' 
        elif self.squema == 'Masculino':
            sex_interesado = 'el interesado' 
        elif self.squema == None:
            sex_interesado = 'los interesados'
        else:
            pass
        return sex_interesado

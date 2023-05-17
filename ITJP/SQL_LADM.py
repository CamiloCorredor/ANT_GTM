import psycopg2

class SQL_LADM:    

    def __init__(self, host, database, user, psw, ID):
        self.host = host
        self.database = database
        self.user = user
        self.psw = psw
        self.ID = ID
        self.connection = self.connect()
        self.cursor = self.connection.cursor()
        self.schema = None
        self.__sql = f"""select P.id_operacion as QR, (st_area(T.geometria))/10000 as AREA_PRED, upper(I.nombre), I.documento_identidad, upper(P.nombre), T.geometria as geom, P.matricula_inmobiliaria as fmi, GIT.dispname as grupo_perso
        from rev_08.lc_predio as P
        inner join rev_08.lc_terreno as T on P.id_operacion = T.etiqueta 
        inner join rev_08.lc_derecho as D on P.t_id = D.unidad
        inner join rev_08.lc_derechotipo as DT on D.tipo = DT.t_id 
        left join rev_08.lc_interesado as I on D.interesado_lc_interesado = I.t_id
        left join rev_08.lc_agrupacioninteresados as AGI on D.interesado_lc_agrupacioninteresados = AGI.t_id 
        left join rev_08.col_grupointeresadotipo as GIT on AGI.tipo = GIT.t_id 
        left join rev_08.lc_interesadodocumentotipo as IDT on I.tipo_documento = IDT.t_id
        left join rev_08.lc_sexotipo as SX on I.sexo = SX.t_id
        left join rev_08.lc_grupoetnicotipo as GE on I.grupo_etnico = GE.t_id 
        left join rev_08.lc_datosadicionaleslevantamientocatastral as DA on P.t_id = DA.lc_predio 
        left join rev_08.lc_categoriasuelotipo as CS on DA.categoria_suelo = CS.t_id 
        left join rev_08.lc_destinacioneconomicatipo as DE on DA.destinacion_economica = DE.t_id
        left join rev_08.lc_procedimientocatastralregistraltipo as PC on DA.procedimiento_catastral_registral = PC.t_id 
        left join rev_08.lc_condicionprediotipo as CP on P.condicion_predio = CP.t_id 
        left join rev_08.lc_prediotipo as PT on P.tipo = PT.t_id
        where P.id_operacion = '{self.ID}'"""
        self.__sql_sex = f"""select P.id_operacion as QR, SX.dispname as sexo 
        from rev_08.lc_predio as P
        inner join rev_08.lc_terreno as T on P.id_operacion = T.etiqueta 
        inner join rev_08.lc_derecho as D on P.t_id = D.unidad
        inner join rev_08.lc_derechotipo as DT on D.tipo = DT.t_id 
        left join rev_08.lc_interesado as I on D.interesado_lc_interesado = I.t_id
        left join rev_08.lc_agrupacioninteresados as AGI on D.interesado_lc_agrupacioninteresados = AGI.t_id 
        left join rev_08.col_grupointeresadotipo as GIT on AGI.tipo = GIT.t_id 
        left join rev_08.lc_interesadodocumentotipo as IDT on I.tipo_documento = IDT.t_id
        left join rev_08.lc_sexotipo as SX on I.sexo = SX.t_id 
        where P.id_operacion = '{self.ID}' """
        self.__sql_int = f"""select P.id_operacion as QR, P.numero_predial, DT.dispname as derecho, P.codigo_orip ,
        P.matricula_inmobiliaria as FMI, DIT.dispname ,I.documento_identidad , I.nombre 
        from rev_08.lc_terreno as T
        left join rev_08.lc_predio as P on T.etiqueta = P.local_id
        left join rev_08.lc_derecho as D on P.t_id = D.unidad
        left join rev_08.lc_derechotipo as DT on D.tipo = DT.t_id
        left join rev_08.lc_agrupacioninteresados as AI on D.interesado_lc_agrupacioninteresados = AI.t_id
        left join rev_08.col_miembros as CM on AI.t_id = CM.agrupacion 
        left join rev_08.fraccion as F on CM.t_id = F.col_miembros_participacion 
        left join rev_08.lc_interesado as I on CM.interesado_lc_interesado = I.t_id
        left join rev_08.lc_interesadodocumentotipo as DIT on I.tipo_documento = DIT.t_id
        where P.id_operacion = '{self.ID}'"""
        # cursor.execute(sql_sex)
    # schemax = cursor.fetchall()

    def connect(self):
        connection = psycopg2.connect(
            host=self.host,
            database=self.database,
            user=self.user,
            password=self.psw
        )
        return connection

    def exe_sql(self):
        self.cursor.execute(self.__sql)
        self.schema = self.cursor.fetchall()
        return self.schema

    def exe_sql_1(self):
        self.cursor.execute(self.__sql_sex)
        self.schema = self.cursor.fetchall()
        return self.schema

    def exe_sql_2(self):
        self.cursor.execute(self.__sql_int)
        self.schema = self.cursor.fetchall()
        return self.schema
#Datos de la base de datos
DB_NAME = 'ChacaoActivo'
DB_HOST = 'localhost'
DB_PORT = 27017


#Cuentas a seguir para informar sobre sus tweets
seguir = [
              "@chacaodigital",\
              "@culturachacao",\
              "@deportechacao",\
              "@OAC_CHACAO"   ,\
              "@policiachacao",\
              "@ramonmuchacho",\
              "@concejochacao"
         ]


#Parametro que define cuantos tweets se tomaran
#en get_tweets de db.py por query
tweets_por_query = 25

import pymongo
import queries
from time import sleep



#Funcion que buscan los cant tweets mas recientes dado un patron
#en la base de datos
def query_recientes_tweets_id(db,patron,cant=100):
  return db.tweets.find({'mensaje': {'$regex':patron}}).sort("tweet_id",pymongo.DESCENDING).limit(cant)


#Funcion que dado una lista de tweets (que son diccionarios en python)
#los agrega a la db
def add_tweets(db,tweets):
  for tweet in tweets:
    if(db.tweets.find_one({'tweet_id':tweet['tweet_id']})==None):
      db.tweets.insert([{
              'tweet_id'        : tweet['tweet_id'],
              'usuario_twitteo' : tweet['usuario'],
              'user_id'         : tweet['user_id'],
              'mensaje'         : tweet['contenido'],
              'RTs'             : tweet['retweets'],
              'favs'            : tweet['fav'],
              'responde_a_id'   : tweet['responde_a_id'],
              'responda_a'      : tweet['responde_a'],
              'image_url'       : tweet['image_url'],
              'fecha'           : tweet['fecha'],
              'responde_msj'    : tweet['responde_msj']
                     }])

#Funcion que busca los tweets mas recientes de las cuentas
#que estan en el arreglo de seguir
def stalk_infinito(db):
  seguir = [
            "@chacaodigital",\
            "@culturachacao",\
            "@deportechacao",\
            "@OAC_CHACAO"   ,\
            "@policiachacao",\
            "@ramonmuchacho",\
            "@concejochacao"
          ]
  twitter = queries.conectar()
 
  while(1): 
    for patron in seguir:
      sleep(0.1)
      try:
        ultimo_id = db.tweets.find({'mensaje':{'$regex':patron}}).sort("tweet_id",pymongo.ASCENDING).limit(1)[0]['tweet_id']
      except:
        ultimo_id = 0
      ultimo_id=str(int(ultimo_id)-1)
      agregar_t = queries.get_tweets(twitter,patron,10,ultimo_id)
      add_tweets(db,agregar_t)


#db.tweets.insert([{'mensaje': "Hoa gente",
#                   'uid'    : "12",
#                   'user'   : "wilmer"}])
#print(db.tweets.find_one({'user': "wilmer",'mensaje':"Hola gente"})==None)

#for i in db.tweets.find({}).sort("uid",pymongo.DESCENDING).limit(1):
#  print(i['uid'])
#db.tweets.remove({'user':"wilmer"})
#for i in db.tweets.find({'mensaje': {'$regex':'Hoa'}}):
#  print(i) 
client = pymongo.MongoClient('localhost',27017) 
db = client['ChacaoActivo']
#for i in query_recientes_tweets_id(db,"Chacao",cant=10):
#  print(i)
#  print()
stalk_infinito(db)

import pymongo
import queries
from constantes_db import DB_HOST,DB_NAME,DB_PORT,seguir
from time import sleep



#Funcion que buscan los cant tweets mas recientes dado un patron
#en la base de datos
def query_recientes_tweets_id(db,patron,cant=100):
  return db.tweets.find({'mensaje': {'$regex':patron}}).sort("tweet_id",pymongo.DESCENDING).limit(cant)


#Funcion que dado una lista de tweets (que son diccionarios en python)
#los agrega a la db
def add_tweets(db,tweets):
  for tweet in tweets:
    #print(tweet['es_rt'])
    if(db.tweets.find_one({'tweet_id':tweet['tweet_id']})==None):
        agregar = [{
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
              'responde_msj'    : tweet['responde_msj'],
              'es_rt'           : tweet['es_rt']       
                  }]
        
        if('rt_status' in tweet):
          agregar[0]['rt_status']=tweet['rt_status']
        db.tweets.insert(agregar)


#Funcion que busca los tweets mas viejos a los que ya se tienen
#de las cuentas
#que estan en el arreglo de seguir
def stalk_infinito(db):
  twitter = queries.conectar()
 
  while(1): 
    for patron in seguir:
      sleep(0.1)
      try:
        ultimo_id = db.tweets.find({'mensaje':{'$regex':patron}}).sort("tweet_id",pymongo.ASCENDING).limit(1)[0]['tweet_id']
      except:
        ultimo_id = -1
      ultimo_id=str(int(ultimo_id))
      agregar_t = queries.get_tweets(twitter,patron,50,ultimo_id)
      add_tweets(db,agregar_t)


#Igual que la funcion anterior pero busca los tweets mas nuevos
def stalk_infinito_nuevos(db):
  twitter = queries.conectar()
 
  while(1): 
    for patron in seguir:
#      print(patron)
      sleep(0.1)
      try:
        ultimo_id = db.tweets.find({'mensaje':{'$regex':patron}}).sort("tweet_id",pymongo.DESCENDING).limit(1)[0]['tweet_id']
      except:
        ultimo_id = -1
      ultimo_id=str(int(ultimo_id))
      agregar_t = queries.get_tweets_from_since(twitter,patron,50,ultimo_id)
      #print(len(agregar_t))
      add_tweets(db,agregar_t)



def conectar_db():
 client = pymongo.MongoClient(DB_HOST,DB_PORT) 
 return client[DB_NAME]
 

#db.tweets.insert([{'mensaje': "Hoa gente",
#                   'uid'    : "12",
#                   'user'   : "wilmer"}])
#print(db.tweets.find_one({'user': "wilmer",'mensaje':"Hola gente"})==None)

#for i in db.tweets.find({}).sort("uid",pymongo.DESCENDING).limit(1):
#  print(i['uid'])
#db.tweets.remove({'user':"wilmer"})
#for i in db.tweets.find({'mensaje': {'$regex':'Hoa'}}):
#  print(i) 
db = conectar_db()
#for i in query_recientes_tweets_id(db,"Chacao",cant=10):
#  print(i)
#  print()
#stalk_infinito_nuevos(db)
print(db.tweets.find({}).sort("tweet_id",pymongo.DESCENDING).limit(1)[0]['mensaje'])


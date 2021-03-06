from twython import Twython,TwythonError
from time import localtime,sleep
import sys

# We'll use .tm_hour .tm_min
timeTweet = localtime()
number = 0;

#Funcion que dado un archivo co nlas claves de la APP,
# y OAUTH se conecta con twitter para luego
# empezar a hacer queries
def conectar(dataUser="andres.txt"):
  authFile = open(dataUser).read().splitlines()
  # Setting the variables for verificate credentials
  APP_KEY             = authFile[0]
  APP_SECRET          = authFile[1]
  OAUTH_TOKEN         = authFile[2]
  OAUTH_TOKEN_SECRET  = authFile[3]

  #Conectandose a twitter
  twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
  
  #Verificando credenciales
  twitter.verify_credentials()

  return twitter
 

#Funcion que dado un string y un id de algun tweet
#Obtiene todos los usuarios que han twitteado o retweeteado
#un mensaje msj
def get_retweeters(twitter, msj, since=-1,cant=100):
  usuarios = set()
  x = 0  
  c = 0
  while(1):
    if(x>50):
      return list(usuarios)
    if(c>=cant):
      return list(usuarios)
    c+=100
    x+=1
    try:
      results = twitter.search(q=msj,max_id=since,count=100)
    except:
      print("Muchos queries")
      return list(usuarios)
    cnt = 0
    for tweet in results['statuses']:
      usuarios.add((tweet['user']['screen_name'],\
                    str(tweet['user']['id'])))
      cnt+=1
    if(cnt==0 or len(usuarios)>100000):
      return list(usuarios)
    since = results['statuses'][-1]['id']


#Funcion que retorna los ultimos tweets de un usuario de
#nombre name
def get_tweets_of_user(twitter, name, cant=300):
    ret = list()
    try:
      results = twitter.get_user_timeline(screen_name=name, count=cant)
    except:
      print("Error al buscar tweets de un usuario")
      return ret
    for tweet in results:
      agregar = [
                  ('tweet_id'      , tweet['id_str']),\
                  ('usuario'       , tweet['user']['screen_name']),\
                  ('user_id'       , tweet['user']['id']),
                  ('contenido'     , tweet['text']), \
                  ('retweets'      , tweet['retweet_count']),\
                  ('fav'           , tweet['favorite_count']),\
                  ('responde_a_id' , tweet['in_reply_to_user_id_str']),\
                  ('responde_a'    , tweet['in_reply_to_screen_name']),\
                  ('image_url'     , tweet['user']['profile_image_url']),\
                  ('fecha'         , tweet['created_at']),\
                  ('responde_msj'  , tweet['in_reply_to_status_id_str']),\
                  ('es_rt'         , tweet['retweeted'])
                ]
      if('retweeted_status' in tweet):
        agregar.append(('rt_status',tweet['retweeted_status']))
      ret.append(dict(agregar))

    return ret


#Funcion que obtiene los id's de usuarios de los followers 
#de un usuario
def get_followers(twitter, name, cant=300):
    try:
      results = twitter.get_followers_ids(screen_name=name,count=cant)
    except:
      print("Error al recuperar followers")
      return ()
    return results['ids']

#Funcion que obtiene los id's de usuarios de los que sigue 
#un usuario
def get_following(twitter, name, cant=300):
    try:
      results = twitter.get_friends_ids(screen_name=name,count=cant)
    except:
      print("Error al recuperar followings")
      return ()
    return results['ids']

def get_users_tweets_location(twitter,msj,latitud,longitud,radio,cant=10):
  usuarios = list()
  x=cant
  while(1):
    if(x<0):
      return usuarios
    try:
      results = twitter.search(q       = msj,\
                               geocode = latitud+","+longitud+","+radio,\
                               count   = min(cant,100))
    except:
      print("Problema al buscar por geoloc")
      return usuarios
    x-=100
    cant = 0
    #print(len(results['statuses']))
    for tweet in results['statuses']:
      usuarios.append(dict([('id'       ,tweet['user']['id_str']),\
                            ('ususario' ,tweet['user']['screen_name'])])) 
      print(tweet['text'])
      cant+=1
    if(cant==0):
      return usuarios



#Funcion que obtiene los tweets que cumplen con un mensaje
#busca de 100 en 100 (debigo al API de twitter)
#y busca hasta cant tweets
#ademas trunca la busqueda a 100000 tweets 
#y busca los tweets mas nuevos a diferencia de la siguiente
#funcion
def get_tweets_from_since(twitter,msj,cant=100,since=-1):
    cant = min(cant,100000)
    ret = list()
    #print(twitter.search(q=msj,count=100))
    while(cant>0):
      try:
        if(int(since)<0):
          results = twitter.search(q=msj, count=min(100,cant))
        else:
          results = twitter.search(q=msj, count=min(100,cant), since_id=since)
      except Exception as e:
        print("Error al buscar tweets por patron "+str(e))
        return ret
      cant-=100
      tmp = 0
      for tweet in results['statuses']:
        agregar = list(
                 [\
                  ('tweet_id'      , tweet['id_str']),\
                  ('usuario'       , tweet['user']['screen_name']),\
                  ('user_id'       , tweet['user']['id']),
                  ('contenido'     , tweet['text']), \
                  ('retweets'      , tweet['retweet_count']),\
                  ('fav'           , tweet['favorite_count']),\
                  ('responde_a_id' , tweet['in_reply_to_user_id_str']),\
                  ('responde_a'    , tweet['in_reply_to_screen_name']),\
                  ('image_url'     , tweet['user']['profile_image_url']),\
                  ('fecha'         , tweet['created_at']),\
                  ('responde_msj'  , tweet['in_reply_to_status_id_str']),\
                  ('es_rt'         , tweet['retweeted'])
                 ])

        if('retweeted_status' in tweet):
          agregar.append(('rt_status',tweet['retweeted_status']))
 
        ret.append(dict(agregar))
        tmp+=1
      if(tmp==0):
        break
      since = results['statuses'][0]['id']
    return ret


    
#Funcion que obtiene los tweets que cumplen con un mensaje
#busca de 100 en 100 (debigo al API de twitter)
#y busca hasta cant tweets
#ademas trunca la busqueda a 100000 tweets
def get_tweets(twitter,msj,cant=100,since=-1):
    cant = min(cant,100000)
    ret = list()
    #print(twitter.search(q=msj,count=100))
    while(cant>0):
      try:
        if(int(since)<0):
          results = twitter.search(q=msj, count=min(100,cant))
        else:
          results = twitter.search(q=msj, count=min(100,cant), max_id=since)
      except Exception as e:
        print("Error al buscar tweets por patron, "+str(e)+", sleep de 15 minutos")
        sleep(16*60)
        print("Conectando. . .")
        return (conectar(),ret)
      cant-=100
      tmp = 0
      for tweet in results['statuses']:
        agregar = list(
                 [\
                  ('tweet_id'      , tweet['id_str']),\
                  ('usuario'       , tweet['user']['screen_name']),\
                  ('user_id'       , tweet['user']['id']),
                  ('contenido'     , tweet['text']), \
                  ('retweets'      , tweet['retweet_count']),\
                  ('fav'           , tweet['favorite_count']),\
                  ('responde_a_id' , tweet['in_reply_to_user_id_str']),\
                  ('responde_a'    , tweet['in_reply_to_screen_name']),\
                  ('image_url'     , tweet['user']['profile_image_url']),\
                  ('fecha'         , tweet['created_at']),\
                  ('responde_msj'  , tweet['in_reply_to_status_id_str']),\
                  ('es_rt'         , tweet['retweeted'])
                 ])

        if('retweeted_status' in tweet):
          agregar.append(('rt_status',tweet['retweeted_status']))
 
        ret.append(dict(agregar))
        tmp+=1
      if(tmp==0):
        break
      since = results['statuses'][-1]['id']
    return (twitter,ret)


def f(twitter):
 
    while 1:
     print("patron:")
     pat = input()
 
     search_results = twitter.search(q=pat, count=10)
     for tweet in search_results['statuses']:
        print("Usuario:\n")
        print(tweet['user']['screen_name'])
        print("\nContenido\n")
        print("\n==============================================\n")
# Read the name of the file for authentication (which account)


#print(get_following(twitter,"wilmerBandres",10))
#print(get_followers(twitter,"wilmerBandres",10))
#print(get_tweets_of_user(conectar(),"wilmerBandres",1))
#print(len(get_retweeters(twitter,"mas bella")))
#print(conectar().search(q="RT",count=1))
#print(get_tweets(conectar(),"RT",1))
#print(get_users_tweets_location(twitter,"mas bella","10.40833","-66.88333","1km"))
#f(twitter)


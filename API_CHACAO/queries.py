from twython import Twython,TwythonError
from time import localtime
import sys

# We'll use .tm_hour .tm_min
timeTweet = localtime()
number = 0;


#Funcion que dado un string y un id de algun tweet
#Obtiene todos los usuarios que han twitteado o retweeteado
#un mensaje msj
def get_retweeters(twitter, msj, since=-1):
  usuarios = set()
  x =0
  while(1):
    try:
      results = twitter.search(q=msj,max_id=since,count=100)
    except:
      print("Mucho queries")
      return list(usuarios)
 
      cnt = 0
      for tweet in results['statuses']:
        usuarios.add(tweet['user']['screen_name'])
        cnt+=1
      if(cnt==0 or len(usuarios)>100000):
        return list(usuarios)
      since = results['statuses'][-1]['id']

def get_tweets_of_user(twitter, name, cant=300):
    ret = list()
    try:
      results = twitter.get_user_timeline(screen_name=name, count=cant)
    except:
      print("Error al buscar tweets de un usuario")
    for tweet in results:
      ret.append(dict(\
                 [('id'       ,tweet['id_str']),\
                  ('usuario'   ,name),\
                  ('contenido', tweet['text']), \
                  ('fecha'    , tweet['created_at'])]))
    return ret

def f(twitter):
 
    while 1:
     print("patron:")
     pat = input()
 
     search_results = twitter.search(q=pat, count=10)
     for tweet in search_results['statuses']:
        print("Usuario:\n")
        print(tweet['user']['screen_name'])
        print("\nContenido\n")
        print(tweet['text'])
        print("\n==============================================\n")
# Read the name of the file for authentication (which account)

print("Enter the name of the authentication file >> ")
dataUser = input()

authFile = open(dataUser).read().splitlines()
#tweets = open("tweets.txt").read().splitlines()

# Setting the variables for verificate credentials
APP_KEY             = authFile[0]
APP_SECRET          = authFile[1]
OAUTH_TOKEN         = authFile[2]
OAUTH_TOKEN_SECRET  = authFile[3]

twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
twitter.verify_credentials()

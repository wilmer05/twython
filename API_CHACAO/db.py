import pymongo
import queries


client = pymongo.MongoClient('localhost',27017) 
db = client['ChacaoActivo']

#db.tweets.insert([{'mensaje': "Hola gente",
#                   'uid'    : "123",
#                   'user'   : "wilmer"}])
#print(db.tweets.find_one({'user': "wilmer",'mensaje':"Hola gente"})==None)

#for i in db.tweets.find({}).sort("uid",pymongo.DESCENDING).limit(1):
#  print(i['uid'])
#db.tweets.remove({'user':"wilmer"})



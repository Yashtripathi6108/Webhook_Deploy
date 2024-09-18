from pymongo import MongoClient

mongo_uri = 'mongodb://yashansh24:yash1234@cluster0-shard-00-00.u4rqi.mongodb.net:27017,cluster0-shard-00-01.u4rqi.mongodb.net:27017,cluster0-shard-00-02.u4rqi.mongodb.net:27017/?ssl=true&replicaSet=atlas-qn2nv7-shard-0&authSource=admin&retryWrites=true&w=majority&appName=Cluster0'
client = MongoClient(mongo_uri)
db = client['github_events']
collection = db['events']

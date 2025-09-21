from pymongo import MongoClient
import certifi
# put your db creds here like this mongodb+srv://swaraj:swaraj@cluster0.j8mepg9.mongodb.net/ in MONGO_URI
MONGO_URI = ""
client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())

db = client["chat_app"]
users_col = db["users"]
messages_col = db["messages"]

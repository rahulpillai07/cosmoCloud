from pymongo import MongoClient

MONGO_URI = "mongodb+srv://rahulrajeshpillai:rahulpillai07@cluster0.4hcvdvu.mongodb.net/students"

connection = MongoClient(MONGO_URI)

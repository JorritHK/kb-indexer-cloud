from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['kb_indexer_db']

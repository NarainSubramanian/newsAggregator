from pymongo import MongoClient

# Replace with your MongoDB connection string
client = MongoClient("mongodb+srv://narainsubramanium007:p90TQltQSjSA2jkj@cluster0.i2e1h.mongodb.net/ANT?retryWrites=true&w=majority&appName=Cluster0")

# Access your database
db = client['ANT']

collection=db["test"]

document={
    "id":"4"
}

collection.insert_one(document)


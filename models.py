import motor.motor_asyncio
from bson import ObjectId

# Conectar ao MongoDB
MONGO_URI = "mongodb://localhost:27017"
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
db = client["mydatabase"]
collection = db["users"]

def serialize_user(user):
    return {
        "id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"]
    }
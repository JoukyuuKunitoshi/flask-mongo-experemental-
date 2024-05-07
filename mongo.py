from pymongo import *
import hashlib
from bson.objectid import ObjectId
import datetime
def hash_password(password):
    hash_object = hashlib.sha256()
    password_bytes = password.encode("utf-8")
    hash_object.update(password_bytes)
    return hash_object.hexdigest()

class DataBase:
    def __init__(self):
        cluster = MongoClient("mongodb://admin:AdminTop1166060088_SilverDenis05%40gmail.com_aue228_DeTrAdAl2005@217.25.94.249:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.2.5")
        self.db = cluster["HatsuneMiku"]
        self.users = self.db["users"]
        self.tickets = self.db["tickets"]
        print("запустилас")

    def register(self, username, password):
        print(password)
        password = hash_password(password)
        if (self.users.find_one({"username":username})):
                  return "Данное имя пользователя уже используется!"
        
        user = {"username":username, 
                "password":password,
                "permissions":["user"]}



        self.users.insert_one(user)

    def login(self, username, password):
        print("ну вроде запустилас функция логин")
        password = hash_password(password)
        user = self.users.find_one({"username":username, "password":password})
        return user
    
    def violations(self, username, number, description):
        ticket = {"username":username,
                  "number":number,
                  "description":description,
                  "status":"new",
                  "date":datetime.datetime.now()
                  }
        return self.tickets.insert_one(ticket)
    
  
    def getTickets(self, username):
        return self.tickets.find({"username":username})
    
    def getAllTickets(self):
        return self.tickets.find({})
    def editTickets(self, _id, todo):
        if todo == "delete":
            self.tickets.delete_one({"_id":ObjectId(_id)})
            return todo
        self.tickets.find_one_and_update({ "_id":ObjectId(_id) },{"$set":{"status":todo}})
        return todo
    
    def admin(self, username):
        user = self.users.find_one({"username":username})
        if "admin" in user["permissions"]:
            return True
        
             
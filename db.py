from pymongo import MongoClient
from werkzeug.security import generate_password_hash

#sudo  docker exec -it mongodb mongo  
#to run the mongodb in docker


#sudo docker exec -it mongodb mongo --username root --password pass12345
#for root access 


# client = MongoClient("mongodb://localhost:27017",username='root',password='pass12345')
client = MongoClient("mongodb://{}:{}@localhost:27017".format('root','pass12345'))


chat_db = client.get_database("ChatDB")

users_collection = chat_db.get_collection("users")

print(users_collection)

def save_user(username, email, password):
    password_hash = generate_password_hash(password)
    users_collection.insert_one({'_id':username,
    "email":email,"password":password_hash})      



save_user("oykamal", "oyekamalkhan@gmail.com", "pass")
import os
import pickle
from tkinter import EXCEPTION
from flask import Flask
from flask_socketio import SocketIO, send, emit


app = Flask(__name__)
socketio = SocketIO(app)

@app.route("/")
def hello_world():
    return "<h1>Hello, World!</h1>\n<h3>This is the Bip-Bar website running locally!</h3>"

@socketio.on('PublicData') 
def SendDataPublic(data):
    print("I HAVE RECIEVED THE 'PublicData' REQUEST")
    dbfile = pickle.load(open( "dbbb", "rb"))
    try:    
        user = (dbfile[data[0]])
        
        user.pop("name")
        user.pop("email")
        user.pop("adress")
        
        print(user)
        
        with open(f'ServerPhotos/{data[0]}.jpg', 'rb') as f:
            image = f.read()
        
        if user["chipID"] == data[1]:
            emit("recieveData", [user, image])  
        else: emit("serverDenied", "FALSE CHIP-ID\n Public")                
    
    except: emit("serverDenied", "FALSE USER-ID\n Public")
    

@socketio.on("PrivateData")
def SendDataPrivate(data):
    print("I HAVE RECIEVED THE 'PrivateData' REQUEST")
    dbfile = pickle.load(open( "dbbb", "rb"))
    try:
        user = (dbfile[data[0]])
        print(user)
        
        with open(f'ServerPhotos/{data[0]}.jpg', 'rb') as f:
            image = f.read()
        
        if user["chipID"] == data[1]:
            emit("recieveData", [user, image])
        else: emit("serverDenied", "FALSE CHIP-ID\n Private")
        
    except: emit("serverDenied", "FALSE USER-ID\n Private")

@socketio.on("NewUser")
def NewUser(data):
    # database
    print("New user is being created...")
    
    db = pickle.load(open("dbbb", "rb")) #Load database   
    dbUser = data #userData
    
    if list(dbUser.keys())[0] in db: userEdit = True #Check if user is already in database
    else: userEdit = False
    try:
        db.update(dbUser) #update userData in database
        

        #Write to database and save
        dbfile = open('dbbb', 'wb')
        pickle.dump(db, dbfile)                     
        dbfile.close()
        
        if userEdit == False: emit("serverConfirmation", "New user created!")
        elif userEdit == True: emit("serverConfirmation", "User Updated!")
        
    except:
        if userEdit == False: emit("serverConfirmation", "New user failed!")
        elif userEdit == True: emit("serverConfirmation", "User update failed!")

@socketio.on("Billede")
def Billede(data):
    with open(f"ServerPhotos/{data[0]}.jpg", "wb") as binary_file:
        binary_file.write(data[1]) # Write bytes to file
    
    
    
@socketio.on("Trans")
def CreateTransaction(data):
    try:    
        db = pickle.load(open("dbbb", "rb")) #Load database   
        dbUser = data[0] #userData
        transaction = data[1]
        newBalance = data[2]
        db[dbUser]["transactions"].update(transaction) #update userData in database
        db[dbUser]["balance"] = newBalance
        print(db[dbUser])
        
        #Check sum of transactions against newBalance
        if sum(db[dbUser]["transactions"].values()) == newBalance:
            transAuthentication = True
        else: transAuthentication = False
        
        #Write to database and save
        dbfile = open('dbbb', 'wb')
        pickle.dump(db, dbfile)                     
        dbfile.close()
        
        if transAuthentication: emit("serverConfirmation", "Transaction recieved!")
        else: emit("serverConfirmation", "Transaction recieved,\n but balance does\n not match list\n of transactions!")
    except Exception as e:
        print(e)
        emit("serverDenied", "Transaction failed\n for unknown reasons!")


if __name__ == '__main__':    
    app.run()
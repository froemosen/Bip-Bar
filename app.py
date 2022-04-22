import os
import pickle
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
    user = (dbfile[data[0]])
    
    user.pop("name")
    user.pop("email")
    user.pop("adress")
    
    print(user)
    
    with open(f'ServerPhotos/{data[0]}.jpg', 'rb') as f:
        image = f.read()
    
    if user["chipID"] == data[1]:
        emit("recieveData", [user, image])  
    else: emit("recieveData", [{'name':'FALSE CHIP-ID', 'email': 'FALSE CHIP-ID', 'adress': 'FALSE CHIP-ID', 'birthday': '0-0-0', 'chipID': '00000000000', 'balance': 0, 'transactions': {}}, None])                
    
    

@socketio.on("PrivateData")
def SendDataPrivate(data):
    print("I HAVE RECIEVED THE 'PrivateData' REQUEST")
    dbfile = pickle.load(open( "dbbb", "rb"))
    user = (dbfile[data[0]])
    print(user)
    
    with open(f'ServerPhotos/{data[0]}.jpg', 'rb') as f:
        image = f.read()
    
    if user["chipID"] == data[1]:
        emit("recieveData", [user, image])  
    else: emit("recieveData", [{'name':'FALSE CHIP-ID', 'email': 'FALSE CHIP-ID', 'adress': 'FALSE CHIP-ID', 'birthday': '0-0-0', 'chipID': '00000000000', 'balance': 0, 'transactions': {}}, None])


@socketio.on("NewUser")
def NewUser(data):
    # database
    print("New user is being created...")
    
    db = pickle.load(open("dbbb", "rb")) #Load database   
    dbUser = data #userData
    db.update(dbUser) #update userData in database
    

    #Write to database and save
    dbfile = open('dbbb', 'wb')
    pickle.dump(db, dbfile)                     
    dbfile.close()

@socketio.on("Billede")
def Billede(data):
    with open(f"ServerPhotos/{data[0]}.jpg", "wb") as binary_file:
        binary_file.write(data[1]) # Write bytes to file
        
@socketio.on("GetBillede")
def Billede(data):
    pass 
    """with open(f"ServerPhotos/{data}.jpg", "rb") as binary_file:
        # Write bytes to file
        pass"""
    
    




@socketio.on("Trans")
def CreateTransaction(data):
    incom = data
    incom.split(",", 3)
    
    dbfile = open('dbbb', 'ab')
    userid = incom([0])
    
    dbfile.update(userid(Transid(incom([1])),value(incom([2])),desc(incom([3]))))
    
    
    pickle.dump(db, dbfile)                     
    dbfile.close()
    
    #sio.emit("TransOK", "Transaction revieved")
    
    """
    except:
        sio.emit("TransOK", "Transaction Failed!")
    """


if __name__ == '__main__':    
    app.run()
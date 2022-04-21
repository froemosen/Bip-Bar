import os
import pickle
from flask import Flask
from flask_socketio import SocketIO, send, emit


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@socketio.on('PublicData') 
def SendDataPublic(data):
    print("I HAVE RECIEVED THE 'PublicData' REQUEST")
    dbfile = pickle.load(open( "dbbb", "rb"))
    user = (dbfile[data[0]])
    
    emit(user)                
    
    

socketio.on("PrivateData")
def SendDataPrivate(data):
    print("I HAVE RECIEVED THE 'PrivateData' REQUEST")
    dbfile = pickle.load(open( "dbbb", "rb"))
    user = (dbfile[data[0]])
    print(user)
    if user["chipID"] == data[1]:
        emit("recievePrivateData", user)  


@socketio.on("NewUser")
def NewUser(data):
    # database
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
    with open(f"ServerPhotos/{data}.jpg", "rb") as binary_file:
        # Write bytes to file
    




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
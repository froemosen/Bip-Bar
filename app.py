import os
import pickle
from flask import Flask
from flask_socketio import SocketIO, send, emit


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

db = {}

@socketio.on('PublicData') 
def SendDataPublic():
    print("I HAVE RECIEVED THE 'PublicData' REQUEST")
    dbfile = open('dbbb', 'ab')
    user = (dbfile[0])
    emit(user)
    pickle.dump(db, dbfile)                     
    dbfile.close()
    

socketio.on("PrivateData")
def SendDataPrivite():
    dbfile = open('dbbb', 'ab')
    user = (dbfile[0])
    pickle.dump(db, dbfile)                     
    dbfile.close()
    emit(user)


@socketio.on("NewUser")
def NewUser(data):
    # database
    dbfile = open('dbbb', 'ab')   
    dbUser = data
    db.update(dbUser)
      
    # Its important to use binary mode

    # source, destination
    pickle.dump(db, dbfile)                     
    dbfile.close()

@socketio.on("Billede")
def Billede(data):
    with open(f"ServerPhotos/{data[0]}.jpg", "wb") as binary_file:
        binary_file.write(data[1]) # Write bytes to file
    




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
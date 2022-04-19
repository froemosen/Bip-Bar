import os
import pickle
from flask import Flask
from flask_socketio import SocketIO, send, emit


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

db = {}

@socketio.on('Data') 
def SendData():
    dbfile = open('dbbb', 'ab')
    user = {dbfile[0]}
    pickle.dump(db, dbfile)                     
    dbfile.close()
    emit(user)

@socketio.on("NewUser")
def NewUser(data):
    # database
    dbfile = open('dbbb', 'ab')
    
    incomming = data
    incomming.split(",",7)
        

    dbu = {incomming([0]) : {name : incomming([1]) , emailaddres : incomming([2]), adress : incomming([3]), birthday : incomming([4]), 
    bal : incomming([5]), Chip : incomming([6]), Trans : {incomming([7])} } }
    dbfile.update(dbu)
      
    # Its important to use binary mode

    # source, destination
    pickle.dump(db, dbfile)                     
    dbfile.close()

@socketio.on("Billede")
def Billede(data):
    directory = "IDPhotos"
    data.save(directory)



@socketio.on("Trans")
def CreateTransaction(data):
    incom = data
    incom.split(",", 3)
    
    dbfile = open('dbbb', 'ab')
    userid = incum([0])
    
    dbfile.update(userid(Transid(incom([1])),value(incom([2])),desc(incom([3]))))
    
    
    pickle.dump(db, dbfile)                     
    dbfile.close()


if __name__ == '__main__':
    NewUser()
    CreateTransaction()
    SendData()
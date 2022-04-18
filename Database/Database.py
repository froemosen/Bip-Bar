from msilib.schema import IniFile
import pickle
from unittest import skip

#navn = incomiing fra terminal(bruger id)
db = {}
sk = "" #data fra terminal

def storeData():
    # database
    dbu = {userid : {name : navn, emailaddres : email, adress : adresse, birthday : fødselsdag, bal : total, Chip : id, Trans : {} } }
    db.update(dbu)
      
    # Its important to use binary mode
    dbfile = open('dbbb', 'ab')
      
    # source, destination
    pickle.dump(db, dbfile)                     
    dbfile.close()


def loadData():
    input = str(input( ))
    dbfile = open('dbbb', 'rb')     
    db = pickle.load(dbfile)
    print(db[input])
    dbfile.close()

def createTransaction():
    key = sk+pk
    


if __name__ == '__main__':
    storeData()
    loadData()
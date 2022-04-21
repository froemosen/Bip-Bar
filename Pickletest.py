import pickle

"""favcolor = pickle.load(open( "dbbb", "rb"))
print(favcolor)"""


"""def SendDataPrivate(data):
    print("I HAVE RECIEVED THE 'PrivateData' REQUEST")
    dbfile = pickle.load(open( "dbbb", "rb"))
    user = (dbfile[data[0]])
    if user["chipID"] == data[1]:
        print(user)
        
SendDataPrivate(["14928e73-c141-11ec-8b23-2c6dc190bfef", "04910401244003"])  """

def SendDataPublic(data):
    print("I HAVE RECIEVED THE 'PublicData' REQUEST")
    dbfile = pickle.load(open( "dbbb", "rb"))
    user = (dbfile[data[0]])
    
    user.pop("name")
    user.pop("email")
    user.pop("adress")
    
    print(user)
    
    """with open(f'ServerPhotos/{data[0]}.jpg', 'rb') as f:
        image = f.read()"""
    
    if user["chipID"] == data[1]:
        print(user)
    
SendDataPublic(["14928e73-c141-11ec-8b23-2c6dc190bfef", "04910401244003"]) 
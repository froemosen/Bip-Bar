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

"""def SendDataPublic(data):
    print("I HAVE RECIEVED THE 'PublicData' REQUEST")
    dbfile = pickle.load(open( "dbbb", "rb"))
    user = (dbfile[data[0]])
    
    user.pop("name")
    user.pop("email")
    user.pop("adress")
    
    print(user)
    
    """"""with open(f'ServerPhotos/{data[0]}.jpg', 'rb') as f:
        image = f.read()""""""
    
    if user["chipID"] == data[1]:
        print(user)
    
SendDataPublic(["14928e73-c141-11ec-8b23-2c6dc190bfef", "04910401244003"]) """

#Import all the necessary libraries
from tkinter import *

#Define the tkinter instance
win= Toplevel()
win.title("Rounded Button")

#Define the size of the tkinter frame
win.geometry("700x300")

#Define the working of the button

def my_command():
   text.config(text= "You have clicked Me...")

#Import the image using PhotoImage function
click_btn= PhotoImage(file='MenuPhotos/minusBtn.png')

#Let us create a label for button event
img_label= Label(image=click_btn)

#Let us create a dummy button and pass the image
button= Button(win, image=click_btn,command= my_command,
borderwidth=0)
button.pack(pady=30)

text= Label(win, text= "")
text.pack(pady=30)

win.mainloop()
import tkinter as tk # (pip install tkinter)
import sys
import os
from app import NewUser
import entryWithPlaceholder #entryWithPlaceholder.py (local file)
import cv2 #Camera stuff (pip install opencv)
import PIL.Image, PIL.ImageTk #tkinter stuff with PIL (pip install Pillow)
import uuid #Random uuid-generation
import ndef # (pip install ndefpy)? - might be included in (pip install nfc)?
import socketio # (pip install "python-socketio[client]")
import time
from datetime import date

class MainFrame(tk.Frame): 
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs, bg = '#bcc8e8')

        Bip_Bar_Window = Bip_Bar(self)
        Edit_User_Window = Edit_User(self)
        New_User_Window = New_User(self)

        #Først laver vi kasser til selve knapperne.
        ButtonFrame = tk.Frame(self, bg = '#bcc8e8', borderwidth = 3, relief = 'raised')
        Box = tk.Frame(self)
        ButtonFrame.pack(side = "left", fill = "both", expand= False)
        Box.pack(side = "left", fill = "both", expand= True)

        #Placering for kasserne
        Bip_Bar_Window.place(in_= Box, x = 0, y = 0, relwidth = 1, relheight = 1)
        Edit_User_Window.place(in_= Box, x = 0, y = 0, relwidth = 1, relheight = 1)
        New_User_Window.place(in_= Box, x = 0, y = 0, relwidth = 1, relheight = 1)

        mainMenu = tk.Label(ButtonFrame, text = "Main Menu", bg = '#bcc8e8')
        mainMenu.config(font=("Courier", 24), bg = '#bcc8e8')
        
        #Selve knapperne bliver lavet
        Bip_Bar_Button = tk.Button(ButtonFrame, text = "Bip Bar", height = 10, width = 20, command = Bip_Bar_Window.show)
        Edit_User_Button = tk.Button(ButtonFrame, text = "Edit User", height = 10, width = 20, command = Edit_User_Window.show)
        New_User_Button = tk.Button(ButtonFrame, text = "New User", height = 10, width = 20, command = New_User_Window.show)
        Reset_Button = tk.Button(ButtonFrame, text = "reset", height = 3, width = 20, command = self.reset)
        

        #Knapper formatteres i tabel
        mainMenu.grid(row = 0, column = 0, padx = 0, pady = 15)
        Bip_Bar_Button.grid(row = 1, column = 0, padx = 0, pady = 0)
        Edit_User_Button.grid(row = 2, column = 0, padx = 0, pady = 0)
        New_User_Button.grid(row = 3, column = 0, padx = 0, pady = 0)
        Reset_Button.grid(row = 4, column = 0, padx = 0, pady = 15)
        
        #Hvilken side programmet skal starte i
        Bip_Bar_Window.show()
    
    def reset(self):
        os.execl(sys.executable, sys.executable, *sys.argv)      

class page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        
    def show(self):
        self.lift()
        
    def userInfo(self, placeholder):
        navnText = tk.Label(self, text = "Fuldt navn")
        self.navnInput = tk.Entry(self)

        emailText = tk.Label(self, text = "E-mail adresse")
        self.emailInput = tk.Entry(self)
        
        adresseText = tk.Label(self, text = "Adresse")
        self.adresseInput = tk.Entry(self)

        birthdayText = tk.Label(self, text = "Fødselsdato")     
        if placeholder == True:   
            self.date = entryWithPlaceholder.EntryWithPlaceholder(self, "dag")
            self.month = entryWithPlaceholder.EntryWithPlaceholder(self, "månedstal (01-12)")
            self.year = entryWithPlaceholder.EntryWithPlaceholder(self, "år")
        else:
            self.date = tk.Entry(self, text ="dag")
            self.month = tk.Entry(self, text ="månedstal (01-12)")
            self.year = tk.Entry(self, text = "år")
        
        billedeText = tk.Label(self, text = "Billede til identifikation")        
        self.btn_billede = tk.Button(self, text = "Tag billede", command=self.toggleLiveView)
         
        
        
        navnText.grid(row = 1, column = 0, padx = 0, pady = 0)
        self.navnInput.grid(row = 2, column = 0, padx = 5, pady = 5)
        
        emailText.grid(row = 3, column = 0, padx = 30, pady = 5,)
        self.emailInput.grid(row = 4, column = 0, padx = 5, pady = 5)
        
        adresseText.grid(row = 5, column = 0, padx = 5, pady = 5)
        self.adresseInput.grid(row = 6, column = 0, padx = 5, pady = 5)
        
        birthdayText.grid(row = 7, column = 0, padx = 5, pady = 5)
        self.date.grid(row = 8, column = 0, padx = 5, pady = 5)
        self.month.grid(row = 9, column = 0, padx = 5, pady = 5)
        self.year.grid(row = 10, column = 0, padx = 5, pady = 5)
          
        billedeText.grid(row = 11, column = 0, padx = 5, pady = 5)
        self.btn_billede.grid(row = 12, column = 0, padx = 30, pady = 5)
        
        
         # ---------------------------------------------------------
        # CAMERA SETUP STARTS HERE
        # ---------------------------------------------------------

        self.vcap = cv2.VideoCapture(0)
        self.width = 400
        self.height = 400
    
        #Canvas
        self.canvas1 = tk.Canvas(self)
        self.canvas1.configure( width= self.width, height=self.height)
        self.canvas1.grid(column= 0, row=13,padx = 10, pady=10)
        
        
        #Start-image
        self.takeImage()
        
        # ---------------------------------------------------------
        # CAMERA SETUP ENDs HERE
        # ---------------------------------------------------------
    
    def toggleLiveView(self):
        if self.liveView == False:
            self.liveView = True
            self.takeImage()
            self.btn_billede.config(text = "Tag billede")
        else: 
            self.liveView = False
            self.btn_billede.config(text = "Nyt billede")
            
    def takeImage(self): #Triggers image capture       
        if self.liveView:
            _, self.frame = self.vcap.read()
            
            self.frame1 = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)

            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(self.frame1))
            
            self.canvas1.create_image(0,0, image = self.photo, anchor = tk.CENTER)

            self.after(15, self.takeImage)
            
        else:
            pass
               
        
class Bip_Bar(page):
    def __init__(self, *args, **kwargs):
        page.__init__(self, *args, **kwargs)
        self.text = tk.Label(self, text = "New Transaction", width=20, font="FreeMono")
        self.text.grid(row = 0, column = 0, padx = 30, pady = 5)
        self.btn_getUser = tk.Button(self, text = "Hent chip", command = self.getUser, width=50, height=10, activebackground="green yellow")
        self.btn_getUser.grid(row = 1, column = 0, padx = 30, pady = 5)
    
    def getUser(self): #Public data
        userID, chipID = nfcReader.readData()
        self.btn_getUser.destroy()
        self.text.destroy()
        
        #Get relevant user data and image
        serverComm.getUser_public(userID, chipID)
        print("Awaiting data...")
        global userData
        global userImage
        while userData == {}:
            time.sleep(0.2)
        print("Data ready to be inserted!")
        
        with open(f"currentImage.jpg", "wb") as binary_file: #Save image for later
            binary_file.write(userImage) # Write bytes to file
        
        #calculate age
        birthdayList = userData["birthday"].split("-")
        today = str(date.today())
        todayList = today.split("-")
        todayList.reverse()
        age = int(todayList[2]) - int(birthdayList[2]) - ((int(todayList[1]), int(todayList[0])) < (int(birthdayList[1]), int(birthdayList[0])))
        
        drinkLabelWidth = 18
        
        #10 rows and 12 coloumns
        
        #Creation of GUI
        birthdayLabel = tk.Label(self, text = f"Date of Birth: {userData['birthday']}", width=30, font="FreeMono", padx = 5,  bg = "gray82")
        ageLabel = tk.Label(self, text = f"Current Age: {age}", width=30, font="FreeMono", bg = "gray82")
        balanceLabel = tk.Label(self, text = f"Account Balance: {userData['balance']}", width=30, font="FreeMono", bg = "gray82")
        canvas = tk.Canvas(self, width = 250, height = 250)
        
        colaregLabel = tk.Label(self, text = "Coca Cola Regular", width=drinkLabelWidth, font="FreeMono", padx = 5)
        colazeroLabel = tk.Label(self, text = "Coca Cola Zero", width=drinkLabelWidth, font="FreeMono", padx = 5)
        spriteLabel = tk.Label(self, text = "Sprite", width=drinkLabelWidth, font="FreeMono", padx = 5)
        fantaLabel = tk.Label(self, text = "Fanta", width=drinkLabelWidth, font="FreeMono", padx = 5)
        
        colaregImage = tk.Label(self, text = "Coca Cola Regular", width=drinkLabelWidth, font="FreeMono", padx = 5)
        colazeroImage = tk.Label(self, text = "Coca Cola Zero", width=drinkLabelWidth, font="FreeMono", padx = 5)
        spriteImage = tk.Label(self, text = "Sprite", width=drinkLabelWidth, font="FreeMono", padx = 5)
        fantaImage = tk.Label(self, text = "Fanta", width=drinkLabelWidth, font="FreeMono", padx = 5)
        
        colaRegBtnDown = tk.Button(self, text = "-")
        colaRegAmountLabel = tk.Label(self, text = "0")
        colaRegBtnUp = tk.Button(self, text = "+")
        colaZeroBtnDown = tk.Button(self, text = "-")
        colaZeroAmountLabel = tk.Label(self, text = "0")
        colaZeroBtnUp = tk.Button(self, text = "+")
        spriteBtnDown = tk.Button(self, text = "-")
        spriteAmountLabel = tk.Label(self, text = "0")
        spriteBtnUp = tk.Button(self, text = "+")
        fantaBtnDown = tk.Button(self, text = "-")
        fantaAmountLabel = tk.Label(self, text = "0")
        fantaBtnUp = tk.Button(self, text = "+")
        
              
        
        
        #Packing of GUI
        birthdayLabel.grid(row = 0, column = 0, columnspan = 9, sticky = "N", pady = 5)
        ageLabel.grid(row = 1, column = 0, columnspan = 9, sticky = "N", pady = 5)
        balanceLabel.grid(row = 2, column = 0, columnspan = 9, sticky = "N", pady = 5)
        canvas.grid(column = 9, row = 0 , rowspan = 3, columnspan = 3)
        
        colaregLabel.grid(row = 3, column = 0, columnspan = 3)
        colazeroLabel.grid(row = 3, column = 3, columnspan = 3)
        spriteLabel.grid(row = 3, column = 6, columnspan = 3)
        fantaLabel.grid(row = 3, column = 9, columnspan = 3)
        
        colaregImage.grid(row = 4, column = 0, columnspan = 3)
        colazeroImage.grid(row = 4, column = 3, columnspan = 3)
        spriteImage.grid(row = 4, column = 6, columnspan = 3)
        fantaImage.grid(row = 4, column = 9, columnspan = 3)
        
        colaRegBtnDown.grid(row = 5, column = 0)
        colaRegAmountLabel.grid(row = 5, column = 1)
        colaRegBtnUp.grid(row = 5, column = 2)
        colaZeroBtnDown.grid(row = 5, column = 3)
        colaZeroAmountLabel.grid(row = 5, column = 4)
        colaZeroBtnUp.grid(row = 5, column = 5)
        spriteBtnDown.grid(row = 5, column = 6)
        spriteAmountLabel.grid(row = 5, column = 7)
        spriteBtnUp.grid(row = 5, column = 8)
        fantaBtnDown.grid(row = 5, column = 9)
        fantaAmountLabel.grid(row = 5, column = 10)
        fantaBtnUp.grid(row = 5, column = 11)
        
        
        
         
        self.photo = PIL.ImageTk.PhotoImage(PIL.Image.open(f"currentImage.jpg")) #Image to ImageTK object
        canvas.create_image(0,0, image = self.photo, anchor = tk.CENTER) #Show image on screen
        
        ###CREATE TRANSACTION MENU HERE
        print(userData)
    
        
        userData = {}
        userImage = None
    
    def createTransaction(self):
        pass
    
class Edit_User(page):
    def __init__(self, *args, **kwargs):
        page.__init__(self, *args, **kwargs)
        text = tk.Label(self, text = "Edit User Information", width=20, font="FreeMono")
        text.grid(row = 0, column = 0, padx = 30, pady = 5)
        self.btn_getUser = tk.Button(self, text = "Hent chip", command = self.getUser, width=50, height=10, activebackground="green yellow")
        self.btn_getUser.grid(row = 1, column = 0, padx = 30, pady = 5)
    
        
        #LiveView Boolean
        self.liveView = False
        
    def getUser(self): #Private and public data
        userID, chipID = nfcReader.readData()
        #print(data)
        self.btn_getUser.destroy()
        #data = ServerCommunication.getUser_private()
        
        #Creates boxes for input
        self.userInfo(placeholder=False)
        self.btn_billede.config(text="Nyt billede")
        
        serverComm.getUser_private(userID, chipID)
        
        print("Awaiting data...")
        
        global userData
        global userImage
        
        while userData == {}:
            time.sleep(0.2)
        
        
        print("Data ready to be inserted!")
        
        #Inserting data i boxes
        self.navnInput.insert(0, userData["name"])
        self.emailInput.insert(0, userData["email"])
        self.adresseInput.insert(0, userData["adress"])
        
        dateList = userData["birthday"].split("-")
        self.date.insert(0, dateList[0])
        self.month.insert(0, dateList[1])
        self.year.insert(0, dateList[2])    
        
        with open(f"currentImage.jpg", "wb") as binary_file:
            binary_file.write(userImage) # Write bytes to file 
        
        self.photo = PIL.ImageTk.PhotoImage(PIL.Image.open(f"currentImage.jpg")) #Image to ImageTK object
        self.canvas1.create_image(0,0, image = self.photo, anchor = tk.CENTER) #Show image on screen
        
        userData = {}
        userImage = None
        
            
    def updateUser(self):
        pass

class New_User(page):
    def __init__(self, *args, **kwargs):
        page.__init__(self, *args, **kwargs)
        
        newUserText = tk.Label(self, text = "Register New User", width=20, font="FreeMono")
        newUserText.grid(row = 0, column = 0, padx = 0, pady = 0)
        
        #LiveView Boolean
        self.liveView = True
        
        #Creates boxes for input
        self.userInfo(placeholder=True)
        
        newUserButton = tk.Button(self, text = "Opret ny bruger", command = self.newUser)
        newUserButton.grid(row = 2, column = 1, padx = 0, pady = 0)
          
        
            
    def newUser(self): #Private and public data
        #GENERATION OF USERID
        UserID = str(uuid.uuid1()) #Generate User ID

        ID = nfcReader.writeData(UserID) #WRITE UserID TO NFC-CHIP AND SECURE
   
        cv2.imwrite(f"IDPhotos/{UserID}.jpg", self.frame) #Save image of user for identification
        
        #Get userdata and format in order to send to server
        #userData = f"{str(UserID)}, {str(self.navnInput.get())}, {str(self.emailInput.get())}, {str(self.adresseInput.get())}, {str(self.date.get()+'-'+self.month.get()+'-'+self.year.get())}"
        userData = {UserID : {"name" : str(self.navnInput.get()),
                              "email" : str(self.emailInput.get()),
                              "adress" : str(self.adresseInput.get()),
                              "birthday" : str(self.date.get()+'-'+self.month.get()+'-'+self.year.get()),
                              "chipID" : ID,
                              "balance" : 0,
                              "transactions" : {}
                              }} 
        print(userData)
        
        self.photo = PIL.ImageTk.PhotoImage(PIL.Image.open(f"IDPhotos/{UserID}.jpg")) #Image to ImageTK object
        self.canvas1.create_image(0,0, image = self.photo, anchor = tk.CENTER) #Show image on screen
        
        image_data = [UserID]
        
        #Load image again to send in right format
        with open(f'IDPhotos/{UserID}.jpg', 'rb') as f:
            image_data.append(f.read())
            
        #Send UserData and Image to Server
        serverComm.updateUser(userData, image_data)
            
        

class NFC_Reader():
    def __init__(self):
        import nfc
            
        self.clf = nfc.ContactlessFrontend() #NFC-reader object
        
    
    def readData(self):
        #Check NFC-reader connection
        try:
            assert self.clf.open('usb') is True #Determened in cmd by command: "python -m nfc"
            print(f"Using device: {self.clf}")

        except AssertionError:
            print("NFC-reader not set up correctly. Try again! (Maybe the error is in the code!)")
            self.clf.close()  #Test over - New connection will be needed
            
        tag = self.clf.connect(rdwr={'on-connect': lambda tag: False})
        print("Tag found!")
        print(tag)
        
        chipID = tag.identifier.hex()
        
        if tag.ndef == None: #If tag is authenticated or carries no data.
            tag.authenticate(b"203ec79c-9288-4612-bac3-9e827d43c5d3")
        
        if not tag.ndef == None: #If tag carries data
            record = tag.ndef.records[0]
            userID = record.resource.uri #Gets the userID from the NFC-tag records
            
            self.clf.close()
            return(userID, chipID)
        
        else: 
            print(tag.dump())
            print("Card Carries No Data!\n")
            self.clf.close()
            return(None, None)
    
    
    def writeData(self, inputData):
        #Check NFC-reader connection
        try:
            assert self.clf.open('usb') is True #Determened in cmd by command: "python -m nfc"
            print(f"Using device: {self.clf}")

        except AssertionError:
            print("NFC-reader not set up correctly. Try again! (Maybe the error is in the code!)")
            self.clf.close()  #Test over - New connection will be needed
            
        tag = self.clf.connect(rdwr={'on-connect': lambda tag: False})
        if tag.ndef == None: #If tag is authenticated or carries no data.
            tag.authenticate(b"203ec79c-9288-4612-bac3-9e827d43c5d3") #Unlocks tag
        print("Tag found!")
        print(tag)
        
        chipID = tag.identifier.hex()
        print("unique chip id:", chipID)

        tag.ndef.records = [ndef.SmartposterRecord(inputData)]
        tag.protect(password = b"203ec79c-9288-4612-bac3-9e827d43c5d3", read_protect = True)
        
        self.clf.close()
        
        return chipID
        
    
class ServerCommunication():
    def __init__(self):
        global sio
    
    def getUser_private(self, userID, chipID):
        print("Making private user data request...")
        data = [userID, chipID]
        sio.emit("PrivateData", data)
        sio.emit("GetBillede", userID)
    
    def getUser_public(self, userID, chipID):
        print("Making public user data request...")
        sio.emit("PublicData", [userID, chipID])
        sio.emit("GetBillede", userID)
    
    def updateUser(self, userData, imageData):
        print("Making updateUser request...")
        sio.emit("NewUser", userData)
        sio.emit("Billede", imageData)
    
    def createTransaction(self, transInfo):
        print("Making transaction request...")
        sio.emit("Trans", transInfo)

if __name__ == "__main__":
    nfcReader = NFC_Reader()
    serverComm = ServerCommunication()
    base = tk.Tk()
    base.title("Bip Bar")
    main = MainFrame(base)
    main.pack(side = "top", fill = "both", expand = True)
    base.wm_geometry("1200x700") #Vi skal definere en størrelse fordi siden ville collapse ind på kasserne til knapperne 

    userData = {}
    userImage = None
    
    #base.mainloop() #USE ONLY FOR TESTING WITHOUT SERVER
    
    #Setup of socketio
    sio = socketio.Client()
    
    @sio.event
    def connect():
        print("I'm connected!")

    @sio.event
    def connect_error(data):
        print("The connection failed!\n", str(data))

    @sio.event
    def disconnect():
        print("I'm disconnected!")
        
    @sio.on("recieveData")
    def recievePrivateData(data):
        print("USER DATA RECIEVED!")
        global userData
        global userImage
        
        userImage = data[1]
        userData = data[0]
                
        print(data[0])
        
    
    sio.connect('http://127.0.0.1:5000') #Connect to server
    
    
    base.mainloop() #TKINTER MAIN LOOP
    



import tkinter as tk
import sys
import os
from time import gmtime, strftime
import entryWithPlaceholder
import cv2
import PIL.Image, PIL.ImageTk


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
        
    def userInfo(self):
        navnText = tk.Label(self, text = "Fuldt navn")
        self.navnInput = tk.Entry(self)

        emailText = tk.Label(self, text = "E-mail adresse")
        self.emailInput = tk.Entry(self)
        
        adresseText = tk.Label(self, text = "Adresse")
        self.adresseInput = tk.Entry(self)

        birthdayText = tk.Label(self, text = "Fødselsdato")        
        self.date = entryWithPlaceholder.EntryWithPlaceholder(self, "dag")
        self.month = entryWithPlaceholder.EntryWithPlaceholder(self, "månedstal (1-12)")
        self.year = entryWithPlaceholder.EntryWithPlaceholder(self, f"år")
        
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
        self.width = 300
        self.height = 300
    
        #Canvas
        self.canvas1 = tk.Canvas(self)
        self.canvas1.configure( width= self.width, height=self.height)
        self.canvas1.grid(column= 0, row=20,padx = 10, pady=10)
        
        
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
            _, frame = self.vcap.read()

            frame1 = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame1))
            
            
            self.canvas1.create_image(0,0, image = self.photo, anchor = tk.CENTER)

            self.after(15, self.takeImage)
            
        else:
            pass
        
          
        
class Bip_Bar(page):
    def __init__(self, *args, **kwargs):
        page.__init__(self, *args, **kwargs)
        text = tk.Label(self, text = "New Transaction", width=20, font="FreeMono")
        text.grid(row = 0, column = 0, padx = 30, pady = 5)
        self.btn_getUser = tk.Button(self, text = "Hent chip", command = self.getUser, width=50, height=10, activebackground="green yellow")
        self.btn_getUser.grid(row = 1, column = 0, padx = 30, pady = 5)
    
    def getUser(self): #Public data
        data = nfcReader.readData()
        print(data)
        
        self.btn_getUser.destroy()
    
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
        data = nfcReader.readData()
        print(data)
        self.btn_getUser.destroy()
        #data = ServerCommunication.getUser_private()
        
        #Creates boxes for input
        self.userInfo()
        self.btn_billede.config(text="Nyt billede")
        
        #INSERT data INTO userInfo() BOXES
          
    
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
        self.userInfo()
          
         
            
    def newUser(self): #Private and public data
        pass
    

        
        

class NFC_Reader():
    def __init__(self):
        import nfc
        self.clf = nfc.ContactlessFrontend()
        
    
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
            
        if not tag.ndef == None:
            for record in tag.ndef.records:
                print(record)
            self.clf.close()
            return(tag.ndef.records)
        
        else: 
            print(tag.dump())
            print("Card Carries No Data!\n")
            self.clf.close()
            return(None)
    
    def writeData(self):
        pass
    
class ServerCommunication():
    def __init__(self):
        pass
    
    def getUser_private(self):
        pass
    
    def getUser_public(self):
        pass
    
    def updateUser(self):
        pass
    
    def createTransaction(self):
        pass

if __name__ == "__main__":
    nfcReader = NFC_Reader()
    serverComm = ServerCommunication()
    base = tk.Tk()
    base.title("Bip Bar")
    main = MainFrame(base)
    main.pack(side = "top", fill = "both", expand = False)
    base.wm_geometry("1200x700") #Vi skal definere en størrelse fordi siden ville collapse ind på kasserne til knapperne 
    base.mainloop() 
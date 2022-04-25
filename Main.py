import tkinter as tk # (pip install tkinter)
import entryWithPlaceholder #entryWithPlaceholder.py (local file)
import cv2 #Camera stuff (pip install opencv-python)
import PIL.Image, PIL.ImageTk #tkinter stuff with PIL (pip install Pillow)
import uuid #Random uuid-generation
import ndef # (pip install ndefpy)? - might be included in (pip install nfc)?
import socketio # (pip install "python-socketio[client]")
import time
from datetime import date
import shutil
import winsound

class MainFrame(tk.Frame): 
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs, bg = '#bcc8e8')


        #Først laver vi kasser til selve knapperne.
        ButtonFrame = tk.Frame(self, bg = '#bcc8e8', borderwidth = 3, relief = 'raised')
        self.Box = tk.Frame(self)
        ButtonFrame.pack(side = "left", fill = "both", expand= False)
        self.Box.pack(side = "left", fill = "both", expand= True)


        mainMenu = tk.Label(ButtonFrame, text = "Main Menu", bg = '#bcc8e8')
        mainMenu.config(font=("Courier", 24), bg = '#bcc8e8')
        

        #Selve knapperne bliver lavet
        self.Bip_Bar_Button = tk.Button(ButtonFrame, text = "Bip Bar", height = 10, width = 20)
        self.Edit_User_Button = tk.Button(ButtonFrame, text = "Edit User", height = 10, width = 20)
        self.New_User_Button = tk.Button(ButtonFrame, text = "New User", height = 10, width = 20)
        Reset_Button = tk.Button(ButtonFrame, text = "reset", height = 3, width = 20, command = lambda: self.reset("all"))
        
        #Skab vinduer
        self.createWindows("all")

        #Knapper formatteres i tabel
        mainMenu.grid(row = 0, column = 0, padx = 0, pady = 15)
        self.Bip_Bar_Button.grid(row = 1, column = 0, padx = 0, pady = 0)
        self.Edit_User_Button.grid(row = 2, column = 0, padx = 0, pady = 0)
        self.New_User_Button.grid(row = 3, column = 0, padx = 0, pady = 0)
        Reset_Button.grid(row = 4, column = 0, padx = 0, pady = 15)
        
        #SERVER STATUS ELEMENTS!
        statusLabel = tk.Label(ButtonFrame, text = "Server Status", font=("Courier", 16), bg = '#bcc8e8')
        self.statusCanvas = tk.Canvas(ButtonFrame, width = 64, height = 64, bg = '#bcc8e8', highlightbackground = '#bcc8e8')
        self.statusMsg = tk.Label(ButtonFrame, text = "", font=("Courier", 10), bg = '#bcc8e8')
        
        self.succesIcon = PIL.ImageTk.PhotoImage(PIL.Image.open("Icons\succesIcon.png"))
        self.errorIcon = PIL.ImageTk.PhotoImage(PIL.Image.open("Icons\errorIcon.png"))
        self.waitIcon = PIL.ImageTk.PhotoImage(PIL.Image.open("Icons\waitIcon.png"))
        
        statusLabel.grid(row = 5, column = 0, padx = 0, pady = (200, 0))
        self.statusCanvas.grid(row = 6, column = 0)
        self.statusMsg.grid(row = 7, column = 0)  

    
    def createWindows(self, windowsToCreate):
        if windowsToCreate == "all":
            self.Bip_Bar_Window = Bip_Bar(self)
            self.Edit_User_Window = Edit_User(self)
            self.New_User_Window = New_User(self)
            
            #Placering for kasserne
            self.Bip_Bar_Window.place(in_= self.Box, x = 0, y = 0, relwidth = 1, relheight = 1)
            self.Edit_User_Window.place(in_= self.Box, x = 0, y = 0, relwidth = 1, relheight = 1)
            self.New_User_Window.place(in_= self.Box, x = 0, y = 0, relwidth = 1, relheight = 1)
            
            self.Bip_Bar_Button.configure(command = self.Bip_Bar_Window.show)
            self.Edit_User_Button.configure(command = self.Edit_User_Window.show)
            self.New_User_Button.configure(command = self.New_User_Window.show)
            
            #Hvilken side programmet skal starte i
            self.Bip_Bar_Window.show()
            
            
        elif windowsToCreate == "Bip_Bar":
            self.Bip_Bar_Window = Bip_Bar(self)
            
            #Placering for kasserne
            self.Bip_Bar_Window.place(in_= self.Box, x = 0, y = 0, relwidth = 1, relheight = 1)
            
            self.Bip_Bar_Button.configure(command = self.Bip_Bar_Window.show)
            
            #Hvilken side programmet skal starte i
            self.Bip_Bar_Window.show()
            
            
        elif windowsToCreate == "Edit_User":
            self.Edit_User_Window = Edit_User(self)
            
            #Placering for kasserne
            self.Edit_User_Window.place(in_= self.Box, x = 0, y = 0, relwidth = 1, relheight = 1)
            
            self.Edit_User_Button.configure(command = self.Edit_User_Window.show)
            
            #Hvilken side programmet skal starte i
            self.Edit_User_Window.show()
                
                
        elif windowsToCreate == "New_User":
            self.New_User_Window = New_User(self)
            
            #Placering for kasserne
            self.New_User_Window.place(in_= self.Box, x = 0, y = 0, relwidth = 1, relheight = 1)
            
            self.New_User_Button.configure(command = self.New_User_Window.show) 
            
            #Hvilken side programmet skal starte i
            self.New_User_Window.show()     
        
    
    def reset(self, windowsToReset):
        if windowsToReset == "all":
            self.Bip_Bar_Window.destroy()   
            self.Edit_User_Window.destroy()
            self.New_User_Window.destroy()
            
            self.createWindows("all")
            
        elif windowsToReset == "Bip_Bar":
            self.Bip_Bar_Window.destroy() 
            
            self.createWindows("Bip_Bar")
            
        elif windowsToReset == "Edit_User":
            self.Edit_User_Window.destroy() 
                
            self.createWindows("Edit_User")
                
        elif windowsToReset == "New_User":
            self.New_User_Window.destroy() 
                
            self.createWindows("New_User")


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
            self.date = tk.Entry(self)
            self.month = tk.Entry(self)
            self.year = tk.Entry(self)
        
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
        self.userID, chipID = nfcReader.readData()
        self.btn_getUser.destroy()
        self.text.destroy()
        
        #Get relevant user data and image
        serverComm.getUser_public(self.userID, chipID)
        print("Awaiting data...")
        global userData
        global userImage
        while userData == {}: #Await user data
            time.sleep(0.2)
        print("Data ready to be inserted!")
        main.statusCanvas.delete("all")
        main.statusCanvas.create_image(2, 2, image = main.succesIcon, anchor = "nw")
        main.statusMsg.config(text = "User data inserted")
        
        self.userData = userData #For using userdata in other functions
        
        with open(f"currentImage.jpg", "wb") as binary_file: #Save image for later
            binary_file.write(userImage) # Write bytes to file
        
        #calculate age
        birthdayList = userData["birthday"].split("-")
        today = str(date.today())
        todayList = today.split("-")
        todayList.reverse()
        self.age = int(todayList[2]) - int(birthdayList[2]) - ((int(todayList[1]), int(todayList[0])) < (int(birthdayList[1]), int(birthdayList[0])))
        
        informationWidth = 28
        informationHeight = 1
        informationFont = ("FreeMono", 24, "bold")
        informationBG = "gray82"
        drinkLabelWidth = 22
        drinkFont = ("FreeMono", 20)
        imageSize = 200
        
        #10 rows and 12 coloumns
        
        #Creation of GUI
        infoBG = tk.Frame(self, bg = informationBG, height = 12, width = 200, borderwidth=4, relief="ridge", pady=4)
        cancelTransactionBtn = tk.Button(infoBG, text = "Cancel Transaction", height = 15, width = 23, bg = "red", command = lambda: main.reset("Bip_Bar"))
        createTransactionBtn = tk.Button(infoBG, text = "Create Transaction", height = 15, width = 23, bg = "lawngreen", command = self.createTransaction)
        totalAmountLabel = tk.Label(infoBG, text = "Total Amount: ", width = 21, bg = informationBG, font = drinkFont)
        self.remainBalanceLabel = tk.Label(infoBG, text = "Remaining Balance: ", width = 21, bg = informationBG, font = drinkFont)
        self.totalAmountValue = tk.Label(infoBG, text = "0", width = 8, anchor='w', bg = informationBG, font = drinkFont)
        self.remainBalanceValue = tk.Label(infoBG, text = userData['balance'], width = 8, anchor='w', bg = informationBG, font = drinkFont)
        ageLabel = tk.Label(infoBG, text = f"Current Age: {self.age}", width=informationWidth, height = informationHeight, font=informationFont, padx=6, bg = informationBG)
        balanceLabel = tk.Label(infoBG, text = f"Account Balance: {userData['balance']}", width=informationWidth, height = informationHeight, font=informationFont, padx=6, bg = informationBG)
        canvas = tk.Canvas(infoBG, width = 320, height = 240)
        if self.age >= 18: alcoholAllowedLabel = tk.Label(infoBG, text = "Alcohol is allowed", width=informationWidth, height = informationHeight, font=informationFont, padx=6, bg = informationBG, fg = "lime green") 
        else: alcoholAllowedLabel = tk.Label(infoBG, text = "Alcohol not allowed", width=informationWidth, height = informationHeight, font=informationFont, padx=6, bg = informationBG, fg = "red")
        
        #Prototype version - Add credits to account
        self.insertMoneyEntry = entryWithPlaceholder.EntryWithPlaceholder(infoBG, placeholder = "Add balance here (Whole number)", width = 40)
        self.updateInsert = tk.Button(infoBG, text = "Update", command = lambda: self.updateLabel("nothing", "nothing"))
        
        colaregLabel = tk.Label(self, text = "Coca Cola Regular", width=drinkLabelWidth, font=drinkFont, padx = 5, pady = 10)
        colazeroLabel = tk.Label(self, text = "Coca Cola Zero", width=drinkLabelWidth, font=drinkFont, padx = 5, pady = 10)
        spriteLabel = tk.Label(self, text = "Sprite", width=drinkLabelWidth, font=drinkFont, padx = 5, pady = 10)
        fantaLabel = tk.Label(self, text = "Fanta", width=drinkLabelWidth, font=drinkFont, padx = 5, pady = 10)
        nesteaLabel = tk.Label(self, text = "Nestea Peach", width=drinkLabelWidth, font=drinkFont, padx = 5, pady = 10)
        waterLabel = tk.Label(self, text = "Water", width=drinkLabelWidth, font=drinkFont, padx = 5, pady = 10)
        
        if self.age >= 18: #Alkohol
            pilsnerLabel = tk.Label(self, text = "Tuborg Grøn", width=drinkLabelWidth, font=drinkFont, padx = 5, pady = 10)
            classicLabel = tk.Label(self, text = "Tuborg Classic", width=drinkLabelWidth, font=drinkFont, padx = 5, pady = 10)
        else: pass
        
        self.colaregImage = PIL.ImageTk.PhotoImage(PIL.Image.open("MenuPhotos\CocaColaReg.png"))
        colaregCanvas = tk.Canvas(self, width = imageSize, height = imageSize)
        self.colazeroImage = PIL.ImageTk.PhotoImage(PIL.Image.open("MenuPhotos\CocaColaZero.png"))
        colazeroCanvas = tk.Canvas(self, width = imageSize, height = imageSize)
        self.spriteImage = PIL.ImageTk.PhotoImage(PIL.Image.open("MenuPhotos\Sprite.png"))
        spriteCanvas = tk.Canvas(self, width = imageSize, height = imageSize)
        self.fantaImage = PIL.ImageTk.PhotoImage(PIL.Image.open("MenuPhotos\Fanta.png"))
        fantaCanvas = tk.Canvas(self, width = imageSize, height = imageSize)
        self.nesteaImage = PIL.ImageTk.PhotoImage(PIL.Image.open("MenuPhotos/Nestea.png"))
        nesteaCanvas = tk.Canvas(self, width = imageSize, height = imageSize)
        self.waterImage = PIL.ImageTk.PhotoImage(PIL.Image.open("MenuPhotos\Water.png"))
        waterCanvas = tk.Canvas(self, width = imageSize, height = imageSize)
        if self.age >= 18: #Alkohol
            self.pilsnerImage = PIL.ImageTk.PhotoImage(PIL.Image.open("MenuPhotos\TuborgGrøn.png"))
            pilsnerCanvas = tk.Canvas(self, width = imageSize, height = imageSize)
            self.classicImage = PIL.ImageTk.PhotoImage(PIL.Image.open("MenuPhotos\TuborgClassic.png"))
            classicCanvas = tk.Canvas(self, width = imageSize, height = imageSize)
        
        self.minusImage = tk.PhotoImage(file='MenuPhotos/minusBtn.png')
        self.plusImage = tk.PhotoImage(file='MenuPhotos/plusBtn.png')
        
        colaRegBtnDown = tk.Button(self, image = self.minusImage, borderwidth=0, command=lambda: self.updateLabel("-", "Cola_Reg"))
        self.colaRegAmountLabel = tk.Label(self, text = "0", font = informationFont)
        colaRegBtnUp = tk.Button(self, image = self.plusImage, borderwidth=0, command=lambda: self.updateLabel("+", "Cola_Reg"))
        colaZeroBtnDown = tk.Button(self, image = self.minusImage, borderwidth=0, command=lambda: self.updateLabel("-", "Cola_Zero"))
        self.colaZeroAmountLabel = tk.Label(self, text = "0", font = informationFont)
        colaZeroBtnUp = tk.Button(self, image = self.plusImage, borderwidth=0, command=lambda: self.updateLabel("+", "Cola_Zero"))
        spriteBtnDown = tk.Button(self, image = self.minusImage, borderwidth=0, command=lambda: self.updateLabel("-", "Sprite"))
        self.spriteAmountLabel = tk.Label(self, text = "0", font = informationFont)
        spriteBtnUp = tk.Button(self, image = self.plusImage, borderwidth=0, command=lambda: self.updateLabel("+", "Sprite"))
        fantaBtnDown = tk.Button(self, image = self.minusImage, borderwidth=0, command=lambda: self.updateLabel("-", "Fanta"))
        self.fantaAmountLabel = tk.Label(self, text = "0", font = informationFont)
        fantaBtnUp = tk.Button(self, image = self.plusImage, borderwidth=0, command=lambda: self.updateLabel("+", "Fanta"))
        nesteaBtnDown = tk.Button(self, image = self.minusImage, borderwidth=0, command=lambda: self.updateLabel("-", "Nestea"))
        self.nesteaAmountLabel = tk.Label(self, text = "0", font = informationFont)
        nesteaBtnUp = tk.Button(self, image = self.plusImage, borderwidth=0, command=lambda: self.updateLabel("+", "Nestea"))
        waterBtnDown = tk.Button(self, image = self.minusImage, borderwidth=0, command=lambda: self.updateLabel("-", "Water"))
        self.waterAmountLabel = tk.Label(self, text = "0", font = informationFont)
        waterBtnUp = tk.Button(self, image = self.plusImage, borderwidth=0, command=lambda: self.updateLabel("+", "Water"))
        
        if self.age >= 18: #Alkohol
            pilsnerBtnDown = tk.Button(self, image = self.minusImage, borderwidth=0, command=lambda: self.updateLabel("-", "Pilsner"))
            self.pilsnerAmountLabel = tk.Label(self, text = "0", font = informationFont)
            pilsnerBtnUp = tk.Button(self, image = self.plusImage, borderwidth=0, command=lambda: self.updateLabel("+", "Pilsner"))
            classicBtnDown = tk.Button(self, image = self.minusImage, borderwidth=0, command=lambda: self.updateLabel("-", "Classic"))
            self.classicAmountLabel = tk.Label(self, text = "0", font = informationFont)
            classicBtnUp = tk.Button(self, image = self.plusImage, borderwidth=0, command=lambda: self.updateLabel("+", "Classic"))
        
              
        
        
        #Packing of GUI
        infoBG.grid(row = 0, column = 0, columnspan = 12, rowspan = 3)
        cancelTransactionBtn.grid(row = 0, column = 0, rowspan = 3, padx = 5)
        createTransactionBtn.grid(row = 0, column = 1, rowspan = 3, padx = (5, 18))
        totalAmountLabel.grid(row = 0, column = 2, columnspan = 3)
        self.remainBalanceLabel.grid(row = 1, column = 2, columnspan = 3)
        self.insertMoneyEntry.grid(row = 2, column = 2, columnspan = 3) #PROTOTYPE ENTRY
        self.updateInsert.grid(row = 2, column = 5, sticky = "w")  #PROTOTYPE BUTTON
        self.totalAmountValue.grid(row = 0, column = 5)
        self.remainBalanceValue.grid(row = 1, column = 5)
        ageLabel.grid(row = 0, column = 6, columnspan = 3, pady = 5)
        balanceLabel.grid(row = 1, column = 6, columnspan = 3, pady = 5)
        alcoholAllowedLabel.grid(row = 2, column = 6, columnspan = 3, pady = 5)
        canvas.grid(column = 9, row = 0 , rowspan = 3, columnspan = 3)
        
        
        
        colaregLabel.grid(row = 3, column = 0, columnspan = 3)
        colazeroLabel.grid(row = 3, column = 3, columnspan = 3)
        spriteLabel.grid(row = 3, column = 6, columnspan = 3)
        fantaLabel.grid(row = 3, column = 9, columnspan = 3)
        nesteaLabel.grid(row = 7, column = 0, columnspan = 3)
        waterLabel.grid(row = 7, column = 3, columnspan = 3)
        
        if self.age >= 18: #Alkohol
            pilsnerLabel.grid(row = 7, column = 6, columnspan = 3)
            classicLabel.grid(row = 7, column = 9, columnspan = 3)
        
        colaregCanvas.grid(row = 4, column = 0, columnspan = 3)
        colazeroCanvas.grid(row = 4, column = 3, columnspan = 3)
        spriteCanvas.grid(row = 4, column = 6, columnspan = 3)
        fantaCanvas.grid(row = 4, column = 9, columnspan = 3)
        nesteaCanvas.grid(row = 8, column = 0, columnspan = 3)
        waterCanvas.grid(row = 8, column = 3, columnspan = 3)
        
        if self.age >= 18: #Alkohol
            pilsnerCanvas.grid(row = 8, column = 6, columnspan = 3)
            classicCanvas.grid(row = 8, column = 9, columnspan = 3)
        
        
        colaRegBtnDown.grid(row = 5, column = 0) #Første række starter her
        self.colaRegAmountLabel.grid(row = 5, column = 1)
        colaRegBtnUp.grid(row = 5, column = 2)
        colaZeroBtnDown.grid(row = 5, column = 3)
        self.colaZeroAmountLabel.grid(row = 5, column = 4)
        colaZeroBtnUp.grid(row = 5, column = 5)
        spriteBtnDown.grid(row = 5, column = 6)
        self.spriteAmountLabel.grid(row = 5, column = 7)
        spriteBtnUp.grid(row = 5, column = 8)
        fantaBtnDown.grid(row = 5, column = 9)
        self.fantaAmountLabel.grid(row = 5, column = 10)
        fantaBtnUp.grid(row = 5, column = 11)
        
        #Indsættelse af en frame til afstand
        distanceFrame = tk.Frame(self)
        spacing = tk.Label(distanceFrame, width = 120, height = 4)
        distanceFrame.grid(row = 6, column = 0, columnspan = 12)
        spacing.pack()
        
        nesteaBtnDown.grid(row = 9, column = 0) #Anden række starter her
        self.nesteaAmountLabel.grid(row = 9, column = 1)
        nesteaBtnUp.grid(row = 9, column = 2)
        waterBtnDown.grid(row = 9, column = 3)
        self.waterAmountLabel.grid(row = 9, column = 4)
        waterBtnUp.grid(row = 9, column = 5)
        
        if self.age >= 18: #Alkohol
            pilsnerBtnDown.grid(row = 9, column = 6)
            self.pilsnerAmountLabel.grid(row = 9, column = 7)
            pilsnerBtnUp.grid(row = 9, column = 8)
            classicBtnDown.grid(row = 9, column = 9)
            self.classicAmountLabel.grid(row = 9, column = 10)
            classicBtnUp.grid(row = 9, column = 11)
        
        colaregCanvas.create_image(2, 2, image = self.colaregImage, anchor = "nw")
        colazeroCanvas.create_image(2, 2, image = self.colazeroImage, anchor = "nw")
        spriteCanvas.create_image(2, 2, image = self.spriteImage, anchor = "nw")
        fantaCanvas.create_image(2, 2, image = self.fantaImage, anchor = "nw")
        nesteaCanvas.create_image(2, 2, image = self.nesteaImage, anchor = "nw")
        waterCanvas.create_image(2, 2, image = self.waterImage, anchor = "nw")
        
        if self.age >= 18: #Alkohol
            pilsnerCanvas.create_image(2, 2, image = self.pilsnerImage, anchor = "nw")
            classicCanvas.create_image(2, 2, image = self.classicImage, anchor = "nw")
        
         
        self.photo = PIL.ImageTk.PhotoImage(PIL.Image.open(f"currentImage.jpg")) #Image to ImageTK object
        canvas.create_image(0,0, image = self.photo, anchor = tk.CENTER) #Show image on screen
    
        
        userData = {}
        userImage = None 
    
    def createTransaction(self):
        transEntry = {str(uuid.uuid1()) : -self.totalToPay}
        newBalance = self.remainBalance
        
        print([self.userID, transEntry, newBalance])
        serverComm.createTransaction([self.userID, transEntry, newBalance])
        main.statusCanvas.delete("all")
        main.statusCanvas.create_image(2, 2, image = main.waitIcon, anchor = "nw")
        main.statusMsg.config(text = "Please Wait...")
    
    def updateLabel(self, operation, item):
        ops = {"+": (lambda x,y: x+y), "-": (lambda x,y: x-y)} #Used as ops["+"] (x,y) or ops["-"] (x,y)
        
        #First evalutation
        self.totalToPay = 0

        labels = [[self.colaRegAmountLabel, 20], [self.colaZeroAmountLabel, 20],
                  [self.spriteAmountLabel, 20], [self.fantaAmountLabel, 20],
                  [self.nesteaAmountLabel, 25], [self.waterAmountLabel, 10]] #labels are built like [[label1, price], [label2, price]...]
        
        if self.insertMoneyEntry.get() !=  "Add balance here (Whole number)": #Prototype money insert
                try: self.totalToPay -= int(self.insertMoneyEntry.get())
                except: pass
        
        if self.age >= 18: 
            labels.append([self.pilsnerAmountLabel, 30]) 
            labels.append([self.classicAmountLabel, 30])
        
        for label in labels:
            self.totalToPay += int(label[0].cget("text"))*label[1] #Current total
            
        self.remainBalance = int(self.userData['balance'])-self.totalToPay #self.remainBalance before new item
        
        #Update items if user can affor
        if item == "Cola_Reg" and self.remainBalance >= 20 or item == "Cola_Reg" and operation != "+":
            self.colaRegAmountLabel.config(text = ops[operation] (int(self.colaRegAmountLabel.cget("text")), 1))
            if int(self.colaRegAmountLabel.cget("text")) < 0: self.colaRegAmountLabel.config(text = "0")
        elif item == "Cola_Zero" and self.remainBalance >= 20 or item == "Cola_Zero" and operation != "+":
            self.colaZeroAmountLabel.config(text = ops[operation] (int(self.colaZeroAmountLabel.cget("text")), 1))
            if int(self.colaZeroAmountLabel.cget("text")) < 0: self.colaZeroAmountLabel.config(text = "0")
        elif item == "Sprite" and self.remainBalance >= 20 or item == "Sprite" and operation != "+":
            self.spriteAmountLabel.config(text = ops[operation] (int(self.spriteAmountLabel.cget("text")), 1))
            if int(self.spriteAmountLabel.cget("text")) < 0: self.spriteAmountLabel.config(text = "0")
        elif item == "Fanta" and self.remainBalance >= 20 or item == "Fanta" and operation != "+":
            self.fantaAmountLabel.config(text = ops[operation] (int(self.fantaAmountLabel.cget("text")), 1))  
            if int(self.fantaAmountLabel.cget("text")) < 0: self.fantaAmountLabel.config(text = "0")
        elif item == "Nestea" and self.remainBalance >= 25 or item == "Nestea" and operation != "+":
            self.nesteaAmountLabel.config(text = ops[operation] (int(self.nesteaAmountLabel.cget("text")), 1))
            if int(self.nesteaAmountLabel.cget("text")) < 0: self.nesteaAmountLabel.config(text = "0")
        elif item == "Water" and self.remainBalance >= 10 or item == "Water" and operation != "+":
            self.waterAmountLabel.config(text = ops[operation] (int(self.waterAmountLabel.cget("text")), 1))
            if int(self.waterAmountLabel.cget("text")) < 0: self.waterAmountLabel.config(text = "0")
        elif item == "Classic" and self.remainBalance >= 30 or item == "Classic" and operation != "+":
            self.classicAmountLabel.config(text = ops[operation] (int(self.classicAmountLabel.cget("text")), 1))
            if int(self.classicAmountLabel.cget("text")) < 0: self.classicAmountLabel.config(text = "0")
        elif item == "Pilsner" and self.remainBalance >= 30 or item == "Pilsner" and operation != "+":
            self.pilsnerAmountLabel.config(text = ops[operation] (int(self.pilsnerAmountLabel.cget("text")), 1))
            if int(self.pilsnerAmountLabel.cget("text")) < 0: self.pilsnerAmountLabel.config(text = "0")
        else: pass   
        

        
        #New evalutation
        self.totalToPay = 0
        
        
        if self.insertMoneyEntry.get() !=  "Add balance here (Whole number)": #Prototype money insert
                try: self.totalToPay -= int(self.insertMoneyEntry.get())
                except: pass
        
        for label in labels:
            self.totalToPay += int(label[0].cget("text"))*label[1]
            
        self.remainBalance = int(self.userData['balance'])-self.totalToPay #self.remainBalance after new item
        
        for label in labels: #Make red labels on items not affordable, black on items with 0 selected and green on selected items
            if label[1] > self.remainBalance: label[0].config(foreground = "red")
            elif int(label[0].cget("text")) == 0: label[0].config(foreground = "black")
            else: label[0].config(foreground = "lime green")
        
        self.totalAmountValue.config(text = str(self.totalToPay))
        self.remainBalanceValue.config(text = str(self.remainBalance))
              
        
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
        #Read NFC
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
        main.statusCanvas.delete("all")
        main.statusCanvas.create_image(2, 2, image = main.succesIcon, anchor = "nw")
        main.statusMsg.config(text = "User data inserted")
        
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
        
        editUserButton = tk.Button(self, width = 30, height = 2, text = "Opdatér bruger og scan NFC", command = lambda: self.updateUser(userID, userData["balance"], userData["transactions"]))
        editUserButton.grid(row = 2, column = 1, padx = 0, pady = 0)       
            
    def updateUser(self, UserID, balance, transactions):
        global userData
        global userImage
        
        ID = nfcReader.writeData(UserID) #WRITE UserID TO NFC-CHIP AND SECURE
   
        try: cv2.imwrite(f"IDPhotos/{UserID}.jpg", self.frame) #Save image of user for identification
        except: shutil.copyfile("currentImage.jpg", f"IDPhotos/{UserID}.jpg")
        
        #Get userdata and format in order to send to server
        #userData = f"{str(UserID)}, {str(self.navnInput.get())}, {str(self.emailInput.get())}, {str(self.adresseInput.get())}, {str(self.date.get()+'-'+self.month.get()+'-'+self.year.get())}"
        userData = {UserID : {"name" : str(self.navnInput.get()),
                              "email" : str(self.emailInput.get()),
                              "adress" : str(self.adresseInput.get()),
                              "birthday" : str(self.date.get()+'-'+self.month.get()+'-'+self.year.get()),
                              "chipID" : ID,
                              "balance" : balance,
                              "transactions" : transactions
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
        main.statusCanvas.delete("all")
        main.statusCanvas.create_image(2, 2, image = main.waitIcon, anchor = "nw")
        main.statusMsg.config(text = "Please Wait...")
        
        userData = {}
        userImage = None


class New_User(page):
    def __init__(self, *args, **kwargs):
        page.__init__(self, *args, **kwargs)
        
        newUserText = tk.Label(self, text = "Register New User", width=20, font="FreeMono")
        newUserText.grid(row = 0, column = 0, padx = 0, pady = 0)
        
        #LiveView Boolean
        self.liveView = True
        
        #Creates boxes for input
        self.userInfo(placeholder=True)
        
        newUserButton = tk.Button(self, width = 30, height = 2, text = "Opret ny bruger og scan NFC", command = self.newUser)
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
        main.statusCanvas.delete("all")
        main.statusCanvas.create_image(2, 2, image = main.waitIcon, anchor = "nw")
        main.statusMsg.config(text = "Please Wait...")
                   

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
        try:
            if tag.ndef == None: #If tag is authenticated or carries no data.
                tag.authenticate(b"203ec79c-9288-4612-bac3-9e827d43c5d3")
            
            if not tag.ndef == None: #If tag carries data
                record = tag.ndef.records[0]
                userID = record.resource.uri #Gets the userID from the NFC-tag records
                
                self.clf.close()
                winsound.Beep(frequency=2000, duration=400) #Beep-sound (Make this on the nfc-reader if possible)
                return(userID, chipID)
            
            else: 
                print(tag.dump())
                print("Card Carries No Data!\n")
                self.clf.close()
                return(None, None)
        except:
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
        winsound.Beep(frequency=2000, duration=400) #Beep-sound (Make this on the nfc-reader if possible)
        
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
    base.state('zoomed') #Laver windowed fullscreen
    main = MainFrame(base)
    main.pack(side = "top", fill = "both", expand = True)

    userData = {}
    userImage = None
    
    #base.mainloop() #USE ONLY FOR TESTING WITHOUT SERVER
    
    #Setup of socketio
    sio = socketio.Client()
    
    @sio.event
    def connect():
        print("I'm connected!")
        main.statusCanvas.delete("all")
        main.statusCanvas.create_image(2, 2, image = main.succesIcon, anchor = "nw")
        main.statusMsg.config(text = "Connected to server!")

    @sio.event
    def connect_error(data):
        print("The connection failed!\n", str(data))
        main.statusCanvas.delete("all")
        main.statusCanvas.create_image(2, 2, image = main.errorIcon, anchor = "nw")
        main.statusMsg.config(text = "The connection to\n server failed!")

    @sio.event
    def disconnect():
        print("I'm disconnected!")
        main.statusCanvas.delete("all")
        main.statusCanvas.create_image(2, 2, image = main.errorIcon, anchor = "nw")
        main.statusMsg.config(text = "Server Disconnected!")
        
        
    @sio.on("recieveData")
    def recieveData(data):
        print("USER DATA RECIEVED!")
        global userData
        global userImage
        
        userImage = data[1]
        userData = data[0]
                
        print(data[0])
        
    @sio.on("serverConfirmation")
    def serverConfirmation(data):
        print(data)
        if data == "Transaction recieved!": main.reset("Bip_Bar")
        elif data == "Transaction recieved,\n but balance does\n not match list\n of transactions!": main.reset("Bip_Bar")
        elif data == "User Updated!": main.reset("Edit_User")
        elif data == "New user created!": main.reset("New_User")
        else: main.reset("all")  #Reset windows
        
        main.statusCanvas.delete("all")
        main.statusCanvas.create_image(2, 2, image = main.succesIcon, anchor = "nw")
        main.statusMsg.config(text = data)
        
    @sio.on("serverDenied")
    def serverDenied(data):
        print(data)
        
        global userData
        userData = {"failure" : "failure"} #To break wait loop in tkinter
        
        if data == "Transaction failed\n for unknown reasons!": main.reset("Bip_Bar")
        elif data == "FALSE CHIP-ID\n Public": main.reset("Bip_Bar")
        elif data == "FALSE USER-ID\n Public": main.reset("Bip_Bar")
        elif data == "FALSE CHIP-ID\n Private": main.reset("Edit_User")
        elif data == "FALSE USER-ID\n Private": main.reset("Edit_User")
        elif data == "User edit failed!": main.reset("Edit_User")
        elif data == "New user failed!": main.reset("New_User")
        else: main.reset("all") #Reset all windows
        
        userData = {} #reset
        
        main.statusCanvas.delete("all")
        main.statusCanvas.create_image(2, 2, image = main.errorIcon, anchor = "nw")
        main.statusMsg.config(text = data)
        
        
        
        
        
    #print("Connecting to server... please wait up to 60 seconds")
    #sio.connect('https://froemosen.pythonanywhere.com', wait_timeout = 60) #Connect to online server
    
    sio.connect('http://127.0.0.1:5000/' ) #Connect to local server
    
    
    base.mainloop() #TKINTER MAIN LOOP
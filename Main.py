import tkinter as tk

class MainFrame(tk.Frame): 
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs, bg = '#bcc8e8')

        Bip_Bar_Window = Bip_Bar(self)
        Edit_User_Window = Edit_User(self)

        #Først laver vi kasser til selve knapperne.
        ButtonFrame = tk.Frame(self, bg = '#bcc8e8', borderwidth = 3, relief = 'raised')
        Box = tk.Frame(self)
        ButtonFrame.pack(side = "left", fill = "both", expand= False)
        Box.pack(side = "left", fill = "both", expand= True)

        #Placering for kasserne
        Bip_Bar_Window.place(in_= Box, x = 0, y = 0, relwidth = 1, relheight = 1)
        Edit_User_Window.place(in_= Box, x = 0, y = 0, relwidth = 1, relheight = 1)

        mainMenu = tk.Label(ButtonFrame, text = "Main Menu", bg = '#bcc8e8')
        mainMenu.config(font=("Courier", 24), bg = '#bcc8e8')
        
        #Selve knapperne bliver lavet
        Bip_BarButton = tk.Button(ButtonFrame, text = "Bip Bar", height = 16, width = 20, command = Bip_Bar_Window.lift)
        Edit_UserButton = tk.Button(ButtonFrame, text = "Edit User", height = 16, width = 20, command = Edit_User_Window.lift)

        #Knapper formatteres i tabel
        mainMenu.grid(row = 0, column = 0, padx = 0, pady = 15)
        Bip_BarButton.grid(row = 1, column = 0, padx = 0, pady = 0)
        Edit_UserButton.grid(row = 2, column = 0, padx = 0, pady = 0)
        
        #Hvilken side programmet skal starte i
        Bip_Bar_Window.show()
        

class page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        
    def show(self):
        self.lift()
        
class Bip_Bar(page):
    def __init__(self, *args, **kwargs):
        page.__init__(self, *args, **kwargs)
        
    
    def getUser(self): #Public data
        pass
    
    def createTransaction(self):
        pass
    
class Edit_User(page):
    def __init__(self, *args, **kwargs):
        page.__init__(self, *args, **kwargs)
        
        navnText = tk.Label(self, text = "Fuldt navn")
        self.navnInput = tk.Entry(self)

        emailText = tk.Label(self, text = "E-mail adresse")
        self.emailInput = tk.Entry(self)
        
        adresseText = tk.Label(self, text = "Adresse")
        self.adresseInput = tk.Entry(self)

        birthdayText = tk.Label(self, text = "Fødselsdato")
        self.birthdayInput = tk.Entry(self)
        
        billedeText = tk.Label(self, text = "Billede til identifikation")
        self.billedeInput = tk.Entry(self)
        
        btn_update = tk.Button(self, text = "Opdater bruger")
        btn_getUser = tk.Button(self, text = "Hent chip")
        
        navnText.grid(row = 0, column = 0, padx = 30, pady = 5)
        self.navnInput.grid(row = 1, column = 0, padx = 5, pady = 5)
        
        emailText.grid(row = 2, column = 0, padx = 30, pady = 5,)
        self.emailInput.grid(row = 3, column = 0, padx = 5, pady = 5)
        
        adresseText.grid(row = 4, column = 0, padx = 5, pady = 5)
        self.adresseInput.grid(row = 5, column = 0, padx = 5, pady = 5)
        
        birthdayText.grid(row = 6, column = 0, padx = 5, pady = 5)
        self.birthdayInput.grid(row = 7, column = 0, padx = 5, pady = 5)
        
        billedeText.grid(row = 8, column = 0, padx = 5, pady = 5)
        self.billedeInput.grid(row = 9, column = 0, padx = 5, pady = 5)
        
        btn_update.grid(row = 10, column = 0, padx = 30, pady = 5)
        btn_getUser.grid(row = 11, column = 0, padx = 30, pady = 5)    
        
    def getUser(self): #Private and public data
        pass
    
    def updateUser(self):
        pass
    
    def newUser(self):
        pass
    

class NFC_Reader():
    def __init__(self):
        import nfc
    
    def readData(self):
        pass
    
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
    base = tk.Tk()
    base.title("Bip Bar")
    main = MainFrame(base)
    main.pack(side = "top", fill = "both", expand = True)
    base.wm_geometry("1200x600") #Vi skal definere en størrelse fordi siden ville collapse ind på kasserne til knapperne 
    base.mainloop() 
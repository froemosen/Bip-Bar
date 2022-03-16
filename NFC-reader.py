import nfc
from time import sleep
from nfc.clf import RemoteTarget
import winsound

clf = nfc.ContactlessFrontend()

data = None

#Check NFC-reader connection
try:
    assert clf.open('usb') is True #Determened in cmd by command: "python -m nfc"
    print(f"Using device: {clf}")

except AssertionError:
    print("NFC-reader not set up correctly. Try again! (Maybe the error is in the code!)")
    clf.close()  #Test over - New connection will be needed


def getData():
    tag = clf.connect(rdwr={'on-connect': lambda tag: False})
    print(tag)
        
    if not tag.ndef == None:
        winsound.Beep(frequency=2000, duration=250) #Beep-sound (Make this on the nfc-reader if possible)
        print(tag.dump())
        for record in tag.ndef.records:
            print(record)
        return(tag.ndef.records)
    
    else: 
        print(tag.dump())
        print("Card Carries No Data!\n")
        #MayHaps tag.sector_select(???)
        return(None)
    

    
    
    


while True:
    try:
        if data == None:    
            data = getData()
            
        else:
            #Do stuff with data
            
            data = None
        
    except Exception as errorCode:
        print(errorCode)
        print("Exception catched - Closing device")
        clf.close()  #Test over - New connection will be needed
        break


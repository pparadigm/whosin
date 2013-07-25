# written in Python 2.7.5 by Prime Paradigm (@pparadigm on GitHub)
# developed on a Win7 system
# last updated: July 25, 2013 @ 4:06PM

# This is code. It might join other code in this repo in the future.

# FEATURES TO IMPLEMENT
#
# 1. need to make sure a card can't be in the keyInfo database more than once
# 2. shouldn't be able to delete all MASTER keys
# 3. interval backups (30 minutes?) of the list to the file, in case of
#    power failure
#
# ---------



import serial


keyInfo = []
listening = True
count = 0


class Key:
    def __init__(self):
        self.choice = input('''
Would you like to add or remove a key?

1. Add key
2. Remove key
3. Exit
''')
        if self.choice == 1:
            Key.add()
        elif self.choice == 2:
            Key.remove()
        elif self.choice == 3:
            return
        else:
            raise ValueError
        

    def MASTER(self, ID):
        keyInfo.append(ID, " : MASTER")
        

    def add(self):
        print "Please scan tag to be added."
        self.ID = self.ser.readline()[2:14]
        if keyInfo.get(self.ID, 0):
            print "Successful scan."
            self.name = input("To whom is this tag assigned?\n")
            keyInfo.append("%s : %s"%(self.ID, self.name))
        else:
            print "Tag is already registered."
            self.choice = input('''Would you like to make this tag MASTER?
1. Yes
2. No
''')
            if choice == 1:
                Key.MASTER(self.ID)
            elif choice == 2:
                return
            else:
                raise ValueError


# double-check this dubious code, I think it's wrong
##    def remove(self):
##        print "Please scan tag to be removed from the system."
##        self.ID = ser.readline()[2:14]
##        if keyInfo.get(self.ID, 1):
##            keyInfo.remove("%s : %s"%(self.ID, self.name))
##            print "Successful removal."
##        else:
##            print "Tag already does not exist."
##            self.choice = input()

        

class RFIDReader:
    def __init__(self):
        self.data = open("RFIDKeyData.txt", "r")
        keyInfo = self.data.readlines()
        self.data.close()
        self.ser = serial.Serial("COM6", 9600)
        print "Now connected to RFID reader."
    if len(keyInfo) == 0:
        print '''No keys in memory.
Please scan tag you wish to become MASTER.'''
        Key.MASTER(self.ser.readline()[1:13])
        count = 1
        while listening:
            count = count + 1
            if count == 1:
                self.serIn = self.ser.readline()[1:13]
            else:
                self.serIn = self.ser.readline()[2:14]
            if self.serIn in keyInfo:
                if keyInfo[name] == "MASTER":
                    print "MASTER mode initialized."
                    Key.MASTER()
                else:
                    print "Key recognized.\nWelcome, %s."%(keyInfo[name])
            else:
                print "Unrecognized key."


    print keyInfo



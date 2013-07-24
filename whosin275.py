# written in Python 2.7.5 by Prime Paradigm (@pparadigm on GitHub)
# developed on a Win7 system
# last updated: July 24, 2013 @ 2:47PM

# This program is meant to handle the sign-in process with the RFID keys, and
# allow management of the system.
# It can also keep track of who is in the office, which is a bit creepy,
# so that will be have to be talked about when this is implemented.

# FEATURES TO IMPLEMENT
#
# 1. Make it so RFIDKeyDict comes from a separate document
# 2. Ability to have keys changed (added to system, deleted from system)
# 3. Ask for port name on first run, have options to save preferences
# 4. Create list and process of who is in the building
#
# ---------



import serial


# The 16-bit numbers originate from scanned tags
RFIDKeyDict = {"06004FE1953D": "Joseph Livingdale",# 1 (see 'RFID Chart Info.txt')
               "06006F570B35": "Alice Varr",       # 2
               "06007266F7E5": "Grey Shultz",      # 3
               "0600727FF0FB": "MASTER"}           # 5

listening = True

def main():
##    ser = serial.Serial(serialSetup(), 9600)
    ser = serial.Serial("COM6", 9600)
    count = 0
    while listening:
        count = count + 1
        if count == 1:
            serIn = ser.readline()[1:13]
        else:
            serIn = ser.readline()[2:14]
        if serIn in RFIDKeyDict:
            if RFIDKeyDict[serIn] == "MASTER":
                masterKey()
            else:
                print "Key recognized.\nWelcome, %s."%(RFIDKeyDict[serIn])
        else:
            print "Unrecognized key."


def masterKey():
    print "MASTER mode engaged."
    # will come back to this later


#in progress
##def serialSetup():
##    try:
##        settings = open("settings.txt", "r")
##        port = settings.readline()[17:]
##        if port == "":
##            raise IOError
##    except IOError:
##        settings = open("settings.txt", "w")
##        port = input("What port is your RFID reader on?\n")
##        save = input("Save this setting:\nTrue\nFalse")
##        if save:
##            settings.write("Port preference: ", port)
##    settings.close()
##    print port
##    return port

main()

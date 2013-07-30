# written in Python 2.7.5 by Prime Paradigm (@pparadigm on GitHub)
# developed on a Win7 system
# last updated: July 25, 2013 @ 1:36PM

# This program is meant to handle the sign-in process with the RFID keys, and
# allow management of the system.
# It can also keep track of who is in the office, which is a bit creepy,
# so that will be have to be talked about when this is implemented.

# FEATURES TO IMPLEMENT
#
# 1. Finish implementing RFIDReader and Key classes.
# 2. Ask for port name(s) on first run, have options to save preferences
# 3. Create list and process of who is in the building
# 4. Change references to RFIDKeyDict
#
# ---------


import serial
import RFIDReader

listening = True



def main():
##    ser = serial.Serial(serialSetup(), 9600)
    serReader = serial.Serial("COM6", 9600)
    data = open("RFIDKeyData.txt", "r")
    count = 0
    while listening:
        count = count + 1
        if count == 1:
            serRIn = serReader.readline()[1:13]
        else:
            serRIn = serReader.readline()[2:14]
        if ser in RFIDKeyDict:
            if RFIDKeyDict[ser] == "MASTER":
                masterKey()
            else:
                print "Key recognized.\nWelcome, %s."%(RFIDKeyDict[serRIn])
        else:
            print "Unrecognized key."


def masterKey():
    print "MASTER mode engaged."
    # will come back to this later


# don't know how to proceed, doesn't work
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

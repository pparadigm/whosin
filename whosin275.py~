#!/usr/bin/python
# written in Python 2.7.5 by Prime Paradigm (@pparadigm on GitHub)
# developed on a Win7 system
# last updated: July 30, 2013 @ 3:41PM

# This program is meant to handle the door management process with the RFID
# keys, and allow management of the system. Might track who is in the building.

# FEATURES TO IMPLEMENT
#
# 1. Create list and process for determining who is in the building
# 2. No duplicate IDs in key database
# 3. Back up whenever a card is added or removed, in case of power failure
#
# ---------


import RFID
import sys

listening = True



def access(info):
    scan = info[0]
    valid = info[1]
    if valid:
        # permission checks will be performed, door will open or remain closed
        # based on that check, status message will be displayed on LCD screen.
        # But for now:
        print scan
    else:
        print "Bad scan. Please rescan your tag."
        return

    

def portConfig():
    try:
        setDoc = open("settings.txt", "r")
        name, rate = setDoc.readline().split(" : ")
        setDoc.close()
    except (ValueError, IOError):
        save = False
        name = str(raw_input("Please enter the name of the port you would like to connect to.\n(Capitalization matters.)\n"))
        rate = int(raw_input("Please enter the baud rate you would like to connect with.\n(If you don't know, enter 9600.)\n"))
        save = raw_input("Save these settings? [Y/n]:  ")
        # honestly, I don't really care how the user says "no"
        if save.lower() in ("y" or "Y" or ""):
            settings = "%s : %s"%(name, rate)
            setDoc = open("settings.txt", "w")
            setDoc.write(settings)
            setDoc.close()
        else:
            print "Settings not saved, no valid configurations exist. Exiting..."
            sys.exit(1)
    return name, rate



def main():
    # retrieving database information
    keyDoc = open("RFIDKeyData.txt", "r")
    # there should be one line, a printout of the last list backup, if any
    keyInfo = list(keyDoc.readline())
    keyDoc.close()
    settings = portConfig()
    portName, baudRate = settings[0], settings[1]
    connection = RFID.RFIDReader(portName, baudRate)
    print "Now listening to RFID device."
    while listening:
        access(RFID.RFIDReader.read(connection))


main()

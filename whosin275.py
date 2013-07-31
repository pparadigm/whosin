#!/usr/bin/python
# written in Python 2.7.5 by Prime Paradigm (@pparadigm on GitHub)
# developed on a Win7 system
# last updated: July 31, 2013 @ 10:13AM

# This program is meant to handle the door management process with the RFID
# keys, and allow management of the system. Might track who is in the building.

# FEATURES TO IMPLEMENT
#
# 1. Create list and process for determining who is in the building
# 2. No duplicate IDs in key database
# 3. Back up whenever a card is added or removed, in case of power failure
# 4. Way to change settings without deleting whosin.conf file
#
# ---------


import RFID

listening = True



def access(scan):
    # An ID will eventually be produced. At this point, it is the whole scan.
    ID = scan.serIn
    if scan.isValid:
        # Permission checks will be performed, door will open or remain closed
        # based on that check, status message will be displayed on LCD screen.
        # But for now:
        print ID
    else:
        # will eventually print to the LCD screen
        print "Bad scan. Please rescan your tag."
        return

def portConfig():
    try:
        setDoc = open("whosin.conf", "r")
        name, rate = setDoc.readline().split(" : ")
        setDoc.close()
    except (ValueError, IOError):
        save = False
        name = str(raw_input("System port descripter (case-sensitive): "))
        rate = int(raw_input("Transmission rate: "))
        save = raw_input("Save these settings? [Y/N]: ").lower()
        # Honestly, I don't really care how the user says "no".
        if save == ("y" or "yes"):
            settings = "%s : %s"%(name, rate)
            setDoc = open("whosin.conf", "w")
            setDoc.write(settings)
            setDoc.close()
        else:
            print "Settings not saved."
    return name, rate

def main():
    # retrieving database information
    keyDoc = open("RFIDKeyData.db", "r")
    # There should be one line, a printout of the last list backup, if any.
    keyInfo = list(keyDoc.readline())
    keyDoc.close()
    settings = portConfig()
    portName, baudRate = settings[0], settings[1]
    connection = RFID.RFIDReader(portName, baudRate)
    print "Now listening to specified port."
    while listening:
        connection.readProtocol()
        access(connection)


main()

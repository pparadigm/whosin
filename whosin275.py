#!/usr/bin/python
# written in Python 2.7.5 by Prime Paradigm (@pparadigm on GitHub)
# developed on a Win7 system
# last updated: July 30, 2013 @ 11:43AM

# This program is meant to handle the door management process with the RFID
# keys, and allow management of the system. Might track who is in the building.

# FEATURES TO IMPLEMENT
#
# 1. Ask for port info on "first" run, have options to save preferences
# 2. Create list and process for determining who is in the building
# 3. No duplicate IDs in key database
# 4. Back up whenever a card is added or removed, in case of power failure
#
# ---------


import RFID

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

    

def main():
    # retrieving database information
    keyDoc = open("RFIDKeyData.txt", "r")
    # there should be one line, a printout of the last list backup, if any
    keyInfo = [keyDoc.readline()]
    keyDoc.close()
    # for now, I am assuming settings already exist. In the future, they will
    # be configurable when setDoc is empty.
    setDoc = open("settings.txt", "r")
    settings = setDoc.readline().split(" : ")
    setDoc.close()
    connection = RFID.RFIDReader(str(settings[0]), int(settings[1]))
    while listening:
        access(RFID.RFIDReader.protocol(connection))


main()

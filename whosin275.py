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
import logging

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
        logging.info("Checking for configuration")
        setDoc = open("whoisin.conf", "r")
        name, rate = setDoc.readline().split(" : ")
        setDoc.close()
    except (ValueError, IOError):
        logging.warning("No configuration found, creating one")
        save = False
        name = str(raw_input("System port descripter: "))
        rate = int(raw_input("Transmission rate: "))
        save = raw_input("Save these settings? [Y/n]:  ")
        # honestly, I don't really care how the user says "no"
        if save.lower() in ("y" or "Y" or ""):
            settings = "%s:%s" %(name, rate)
            setDoc = open("whoisin.conf", "w")
            setDoc.write(settings)
            setDoc.close()
        else:
            logging.error("No valid configuration found")
            print "Settings not saved, no valid configurations exist. Exiting..."
            sys.exit(1)
    return name, rate



def main():
    logging.info("Welcome to 'whoisin'".center(80, '-'))
    # retrieving database information
    logging.info("Opening key database")
    keyDoc = open("RFIDKeyData.db", "r")
    # there should be one line, a printout of the last list backup, if any
    keyInfo = list(keyDoc.read())
    keyDoc.close()
    settings = portConfig()
    portName, baudRate = settings[0], settings[1]
    connection = RFID.RFIDReader(portName, baudRate)
    print "Now listening to RFID device."
    while listening:
        logging.debug("Polling reader for new data")
        access(RFID.RFIDReader.read(connection))



logging.basicConfig(level=logging.DEBUG)
main()

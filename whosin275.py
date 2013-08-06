#!/usr/bin/python
# written in Python 2.7.5 by Prime Paradigm (@pparadigm on GitHub)
# developed on a Win7 system
# last updated: August 2, 2013 @ 10:36AM

# This program is meant to handle the door management process with the RFID
# keys, and allow management of the system. Might track who is in the building.

# FEATURES TO IMPLEMENT
#
# 1. How to run a CLI and the door system at the same time
#    a. In the meantime, I will have two ways of running the program, which
#       require a restart in between. I would like to improve this, because
#       the doors would not be operable while the program database information
#       was modified.
# 2. No duplicate IDs in key database
#    a. What happens if one is manually added to the database? (json might
#       handle this already)
# 3. Back up whenever a card is added or removed, in case of power failure
# 4. Way to change settings without deleting whosin.conf file (will be done
#    with CLI)
# 5. Add door database.
# 6. Create list and process for determining who is in the building ("in" and
#    "out" scanner tags)
# 7. Add LCD screen outputs.
# 8. Make databases pretty.
#
# ---------

import RFID
import sys
import logging

listening = True


def access(scan):
    # capitalized as a stylistic choice
    ID = scan.ID.upper()
    if scan.isValid:
        # Permission checks will be performed, door will open or remain closed
        # based on that check, status message will be displayed on LCD screen.
        # But for now:
        print ID
    else:
        # will eventually print to the LCD screen
        print "Bad scan. Try rescanning."
        return


def portConfig():
    try:
        setDoc = open("whosin.conf", "r")
        name, rate = setDoc.readline().split(" : ")
        setDoc.close()
    except (ValueError, IOError):
        logging.warning("No configuration found, creating one")
        save = False
        name = str(raw_input("System port descripter (case-sensitive): "))
        rate = int(raw_input("Transmission rate: "))
        save = raw_input("Save these settings? [y/N]: ").lower().strip()
        # Honestly, I don't really care how the user says "no".
        if save == ("y" or "yes"):
            settings = "%s : %s"%(name, rate)
            setDoc = open("whosin.conf", "w")
            setDoc.write(settings)
            setDoc.close()
        else:
            print "Settings not saved."
    return name, rate


def init():
    global keydb
    global doordb
    global connection
    logging.basicConfig(level=logging.DEBUG)
    logging.info("Welcome to 'whosin'".center(80, '-'))
    keydb = jsondb.db("keys.db")
    doordb = jsondb.db("doors.db")
    portName, bautRate = portConfig()
    connection = RFID.RFIDReader(portName, baudRate)
    
def main():
    while listening:
        connection.readProtocol()
        access(connection)

init()
main()

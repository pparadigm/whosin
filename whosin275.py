#!/usr/bin/python
# written in Python 2.7.5 by Prime Paradigm (@pparadigm on GitHub)
# developed on a Win7 system
# last updated: August 6, 2013 @ 4:34PM

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
# 5. Create list and process for determining who is in the building ("in" and
#    "out" scanner tags)
# 6. Add LCD screen outputs.
# 7. Add door control (servos).
# 8. Make databases pretty.
#
# ---------

import json
import logging

import RFID

listening = True


# Print statements in this function should eventually print to the LCD screen.
def access(scan):
    # capitalized as a stylistic choice
    scan.ID = scan.ID.upper()
    if scan.isValid:
        logging.info("Retrieving key info from database...")
        for index in range(len(keyDB)):
            if scan.ID in keyDB[index]:
                for name in keyDB[index][scan.ID]:
                    level = keyDB[index][scan.ID][name]
                    logging.info("Information found.")
                    logging.debug("Key returned name of %s and access level \
%s."%(name, level))
                    print "Welcome, %s."%(name)
                    return
        print "Key does not exist. No access."
    else:
        print "Bad scan. Try rescanning."
        return


def portConfig():
    try:
        setDoc = open("whosin.conf", "r")
        name, rate = setDoc.readline().split(" : ")
        setDoc.close()
    except (ValueError, IOError):
        logging.warning("No configuration found, attempting to create one...")
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


def startup():
    global keyDB
    global doorDB
    global connection
    logging.basicConfig(level = logging.DEBUG)
    logging.info("Welcome to Who's In.".center(80, '-'))
    # I feel like there is a way to condense the next 15 lines. If you know
    # how, please let me know.
    try:
        keyDoc = open("keys.db", "r")
        keyDB = keyDoc.readline()
    except IOError:
        keyDoc = open("keys.db", "w")
        keyDoc.write("[{}]")
        keyDB = "[{}]"
    keyDoc.close()
    try:
        doorDoc = open("doors.db", "r")
        doorDB = doorDoc.readline()
    except IOError:
        doorDoc = open("doors.db", "w")
        doorDoc.write("[{}]")
        doorDB = "[{}]"
    doorDoc.close()
    keyDB = json.loads(keyDB)
    doorDB = json.loads(doorDB)
    portName, baudRate = portConfig()
    connection = RFID.RFIDReader(portName, baudRate)
    print "Now listening to specified port."


def main():
    while listening:
        print "Scanner is ready."
        connection.readProtocol()
        access(connection)



startup()
main()

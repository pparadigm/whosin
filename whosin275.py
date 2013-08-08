#!/usr/bin/python
# written in Python 2.7.5 by Prime Paradigm (@pparadigm on GitHub)
# developed on a Win7 system
# last updated: August 8, 2013 @ 3:00PM

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


def keyRetrieval(ID):
    '''Find data tied to ID, return it. If none, return None.'''
    logging.info("Retrieving key info from database...")
    try:
        for person in key_Database[ID]:
            level = int(key_Database[ID][person])
            logging.info("Information found.")
            logging.debug("Key returned name of %s and access level %i."
                          %(person, level))
            return level, person
    except KeyError:
        logging.info("No information found.")
        return None, None


def doorRetrieval():
    '''Find authorization required to pass the scanner.''' 
    # Since there is no way to have more than one connection at the moment,
    # door will be hardcoded.
    door = "Front Door IN"
    logging.info("Tag scanned at %s."%(door))
    # door will never not be in the database, as it is equivalent to the
    # scanner that the key ID is sent from.
    logging.info("Retrieving door info from database...")
    if door in door_Database:
        level = door_Database[door]
    logging.debug("Door lookup returned required access level of %i."%(level))
    return level


# Print statements in this function should eventually print to the LCD screen.
def access(scan):
    '''Determine if tag has access level required to enter room.'''
    # capitalized as a stylistic choice
    scan.ID = scan.ID.upper()
    if scan.isValid:
        roomLevel = doorRetrieval()
        search = keyRetrieval(scan.ID)
        accessLevel, name = search[0], search[1]
        if accessLevel is None:
            print "Key does not exist. No access."
        else:
            if accessLevel <= roomLevel:
                print "Welcome, %s."%(name)
            else:
                print "%s does not have access to this room."%(name)
    else:
        print "Bad scan. Try rescanning."
        return


def portConfig():
    '''Poll user for scanner connection data. Optionally save it.'''
    try:
        logging.info("Looking for configuration...")
        setDoc = open("whosin.conf", "r")
        name, rate = setDoc.read().split(" : ")
        setDoc.close()
        logging.info("Configuration found.")
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
            logging.info("Configuration saved.")
        else:
            logging.info("Configuration was not saved.")
            print "Settings not saved."
    return name, rate


def startup():
    '''Get saved database information, invoke instance of RFIDReader class.'''
    global key_Database
    global door_Database
    global connection
    logging.basicConfig(level = logging.DEBUG)
    logging.info("Welcome to Who's In.".center(80, '-'))
    # I feel like there is a way to condense the next 15 lines. If you know
    # how, please let me know.
    try:
        keyDoc = open("keys.db", "r")
        key_Database = keyDoc.read()
    except IOError:
        keyDoc = open("keys.db", "w")
        keyDoc.write("{}")
        key_Database = "{}"
    keyDoc.close()
    try:
        doorDoc = open("doors.db", "r")
        door_Database = doorDoc.read()
    except IOError:
        doorDoc = open("doors.db", "w")
        doorDoc.write("{}")
        door_Database = "{}"
    doorDoc.close()
    key_Database = json.loads(key_Database)
    door_Database = json.loads(door_Database)
    portName, baudRate = portConfig()
    connection = RFID.RFIDReader(portName, baudRate)
    print "Now listening to specified port."


def main():
    '''Continually listen to scanner connection.'''
    while listening:
        print "Scanner is ready."
        connection.readProtocol()
        access(connection)



startup()
main()

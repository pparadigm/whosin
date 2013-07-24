# written in Python 2.7.5 by Prime Paradigm (@pparadigm on GitHub)
# developed on a Win7 system
# last updated: July 24, 2013 @ 1:00PM

# This program is meant to handle the sign-in process with the RFID keys, and
# allow management of the system.
# It can also keep track of who is in the office, which is a bit creepy,
# so that will be have to be talked about when this is implemented.

# FEATURES TO IMPLEMENT
#
# 1. Make it so RFIDKeyDict comes from a separate document
# 2. Ability to have keys changed (added to system, deleted from system)
# 3. Master key
# 4. Greet people as they scan in, something like "Valid key.\nWelcome,
#    Joseph."
# 5. Ask for port name on first run, have options to save preferences
#
# ---------



import serial


# The 16-bit numbers appear when tags are scanned
RFIDKeyDict = {06004FE1953D: "Joseph Livingdale",# 1 (see 'RFID Chart Info.txt')
               06006F570B35: "Alice Varr",      # 2
               06007266F7E5: "Grey Shultz",     # 3
               0600530B6C32: "Madilynne Fuller",# 4
               0600727FF0FB: "Sean Parmey"}     # 5
count = 0
listening = True


# the port will need to be changed, depending on where you need to be listening
# and your OS
ser = serial.Serial("COM6", 9600)

while listening:
    count = count + 1
    if count == 1:
        serIn = ser.readline()[1:13]
        print serIn
    else:
        serIn = ser.readline()[2:14]
        print serIn

#!/usr/bin/python
# written in Python 2.7.5 by Prime Paradigm (@pparadigm on GitHub)
# developed on a Win7 system
# last updated: July 30, 2013 @ 12:42PAM

# This is code. Should be usuable with similar setups. I have been using an
# ID-12 RFID reader from Innovations with this code.

# FEATURES TO IMPLEMENT
#
# 1. Scan integrity check
#
# ---------


import serial
import logging



class RFIDReader:
    def __init__(self, port, baud):
        self.port = serial.Serial(port, baud)
        logging.info("Attempted to open serial port.")

    def read(self):
        self.serIn = self.port.readline()
        logging.info('Read in: "%s"'%(self.serIn))
        # isValid will later be determined by a calculated checksum vs.
        # provided checksum comparison. If they match, isValid will be
        # set to True.
        self.isValid = True
        if self.isValid:
            logging.info("Scan was good.")
        else:
            logging.info("Scan was bad.")
        return self.serIn, self.isValid

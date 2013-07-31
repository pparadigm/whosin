#!/usr/bin/python
# written in Python 2.7.5 by Prime Paradigm (@pparadigm on GitHub)
# developed on a Win7 system
# last updated: July 31, 2013 @ 10:13AM

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
        logging.info("Opened serial port: ", port)

    def readProtocol(self):
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

    

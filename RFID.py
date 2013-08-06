#!/usr/bin/python
# written in Python 2.7.5 by Prime Paradigm (@pparadigm on GitHub)
# developed on a Win7 system
# last updated: August 2, 2013 @ 10:21AM

# This is code. Should be usuable with similar setups. I have been using an
# ID-12 RFID reader from Innovations with this code.


import logging
import binascii

import serial


class RFIDReader:
    def __init__(self, port, baud):
        self.port = serial.Serial(port, baud)
        logging.info("Opened serial port: ", port)

    def readProtocol(self):
        self.serIn = self.port.readline()
        logging.info('Read in: "%s"'%(self.serIn))
        # "" signifies the start of the information stream, while "" denotes
        # the end. Before the end is \r\n. ".readline()" splits after the \n,
        # so I just need to remove those characters from the end of my string,
        # resulting in a checksummable scan.
        self.rawScan = self.serIn.split("")[1][:-2]
        self.scan = binascii.unhexlify(self.rawScan)
        # The first 4 hex bytes are the ID of the card, while the last one is a
        # provided checksum.
        self.unhexID = self.scan[:5]
        self.ID = binascii.hexlify(self.unhexID)
        self.scanCksm = ord(self.scan[5])
        # performing xor calculation to get the checksum
        self.calcCksm = ord(self.unhexID[0])
        for byte in range(1, 5):
            self.calcCksm ^= ord(self.unhexID[byte])
        if self.calcCksm == self.scanCksm:
            self.isValid = True
            logging.info("Scan was good.")
        else:
            self.isValid = False
            logging.info("Scan was bad. Provided checksum was %i, while \
calculated checksum was %i"%(self.scanCksm, self.calcCksm))

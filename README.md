whosin
======

This program aims to provide an authorization and access control system using
RFID cards.  Cards are read using proximity readers, and sent serially to the
server where they are checked against a database and then a response is sent
to the microprocessor which controls the door locks.


This program should run well wherever the PySerial and jsondb libraries can be
installed:
http://pyserial.sourceforge.net/pyserial.html

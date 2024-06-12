#! env python3
# Get a text file from a TRS-80 Pocket Computer 2 via CE-158X.
# This should work with the original CE-158 or PC-2 RS-232 interface (just at a lower baud rate).
#
# The putput is sent to stdout
# get_text_file > myprog.txt
#
# Parameters:
# -b baud, --baud baud - The speed of the serial port - default 119200
# -p port, --port port - The device of the serial port - default /dev/ttyUSB0
#
# Usage:
#     On the PC, get this script ready to run - but do not execute
#     On the PC-2, do a SETDEV U1,CI,CO (adjust your options - I'm assuming you are using the CWE-158X USB serial port)
#     On the PC-2, do a CSAVEa
#     Execute this script

import serial
import getopt
import sys

# Defaults
serial_port = "/dev/ttyUSB0"
baud_rate = 19200

# Optional command line parameters to change baud and port
try:
    options, arguments = getopt.getopt(sys.argv[1:], "b:p:", ["baud=","port="])
except getopt.GetoptError as err:
    # print help information and exit:
    print(err)  # will print something like "option -a not recognized"
    raise SystemExit('get_text_file --baud=19200 --port=/dev/ttyUSB0')
    sys.exit(2)

if len(options) > 2:
    raise SystemExit('get_text_file --baud=19200 --port=/dev/ttyUSB0')

for o, a in options:
    if o in ("-b", "--baud"):
        baud_rate = int(a)
    if o in ("-p", "--port"):
        serial_port = a

# Open the serial port to the PC-2
pc2 = serial.Serial(serial_port,baud_rate,serial.EIGHTBITS,serial.PARITY_NONE,1)

line = ""
while (line != "\r"):  # The file ends with an empty line
    # The line ends with a CR.  So we read until we hit the \r
	# We need to convert the data from bytes to uft-8 characters
    line = pc2.read_until(b'\r').decode("utf-8")
	# Write what we read to stdout
    print(line)

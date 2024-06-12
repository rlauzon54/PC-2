#! env python3
# Send a binary file to a TRS-80 Pocket Computer 2 via CE-158X.
# This should work with the original CE-158 or PC-2 RS-232 interface (just at a lower baud rate).
#
# Parameters:
# -i filename, --input filename - the file on the PC to send
# -b baud, --baud baud - The speed of the serial port - default 119200
# -p port, --port port - The device of the serial port - default /dev/ttyUSB0
#
# Usage:
#     On the PC, get this script ready to run - but do not execute
#     On the PC-2, do a SETDEV U1,CI,CO (adjust your options - I'm assuming you are using the CWE-158X USB serial port)
#     On the PC-2, do a CLOAD
#     Execute this script

import serial
import getopt
import sys
import time

# Defaults
serial_port = "/dev/ttyUSB0"
baud_rate = 19200
input_file=""

# Allow override of defaults and get input file
try:
    options, arguments = getopt.getopt(sys.argv[1:], "b:p:i:v", ["baud=","port=","input="])
except getopt.GetoptError as err:
    # print help information and exit:
    print(err)  # will print something like "option -a not recognized"
    raise SystemExit('put_binary_file --baud=19200 --port=/dev/ttyUSB0 --input=infile')
    sys.exit(2)

# User must provide at least 1 option, and up to 3
if not options or len(options) > 3:
    raise SystemExit('put_binary_file --baud=19200 --port=/dev/ttyUSB0 --input=infile')

for o, a in options:
    if o in ("-i", "--input"):
        input_file = a
    if o in ("-b", "--baud"):
        baud_rate = int(a)
    if o in ("-p", "--port"):
        serial_port = a

# The input file is required
if input_file == "":
    print('No input file specified')
    exit(1)

# Open the serial port to the PC-2
pc2 = serial.Serial(serial_port,baud_rate,serial.EIGHTBITS,serial.PARITY_NONE,1)

# Open the file as binary - important
f = open(input_file, "rb")

# Process the header - 28 bytes
header= f.read(28)
pc2.write(header)
print('Pausing after header')
time.sleep(0.2) # Give PC2 time to process header

# Now get the rest of the file
rest_of_file = f.read()
pc2.write(rest_of_file) # And send it
f.close()

#! env python3
# Get a binary file from a TRS-80 Pocket Computer 2 via CE-158X.
# This should work with the original CE-158 or PC-2 RS-232 interface (just at a lower baud rate).
#
# Parameters:
# -o filename, --output filename - the file to place the binary file on the PC
# -b baud, --baud baud - The speed of the serial port - default 119200
# -p port, --port port - The device of the serial port - default /dev/ttyUSB0
#
# Usage:
#     On the PC, get this script ready to run - but do not execute
#     On the PC-2, do a SETDEV U1,CI,CO (adjust your options - I'm assuming you are using the CWE-158X USB serial port)
#     On the PC-2, do a CSAVE
#     Execute this script

import serial
import getopt
import sys

# Defaults
serial_port = "/dev/ttyUSB0"
baud_rate = 19200
output_file=""

# Allow override of the defaults and get the output file
try:
    options, arguments = getopt.getopt(sys.argv[1:], "b:p:o:v", ["baud=","port=","output="])
except getopt.GetoptError as err:
    # print help information and exit:
    print(err)  # will print something like "option -a not recognized"
    raise SystemExit('get_binary_file --baud=19200 --port=/dev/ttyUSB0 --output=outfile')
    sys.exit(2)

# At least 1 parm must be provided, but no more than 3
if not options or len(options) > 3:
    raise SystemExit('get_binary_file --baud=19200 --port=/dev/ttyUSB0 --output=outfile')

for o, a in options:
    if o in ("-o", "--output"):
        output_file = a
    if o in ("-b", "--baud"):
        baud_rate = int(a)
    if o in ("-p", "--port"):
        serial_port = a

# The output file is required
if output_file == "":
    print('No output file specified')
    exit(1)

# Timeout = 5 seconds for the read - important
pc2 = serial.Serial(serial_port,baud_rate,serial.EIGHTBITS,serial.PARITY_NONE,1,5)

# Important - we want to tell Python this is a binary file
f = open(output_file, "wb")

# Read the first 100 characters
block=1
print(f"{block}: Reading block of 100 bytes...")
byte_read = pc2.read(100)

# Read until there's no more data in the buffer
while byte_read != b'':
	block=block+1
	f.write(byte_read) # Write the data read to the file
	byte_read = pc2.read(100) # Get the next 100 characters
	print(f"{block}: Reading block of 100 bytes...")
	# If there's less than 100 characters left to read, the read will take 5 second.
	# Then no more data will take 5 more seconds.

f.close()


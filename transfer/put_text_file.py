#! env python3
# Send a text file to a TRS-80 Pocket Computer 2 via CE-158X.
# This should work with the original CE-158 or PC-2 RS-232 interface (just at a lower baud rate).
#
# The input file is piped in from stdin. ex:
# put_text_file < myprog.txt
#
# Parameters:
# -b baud, --baud baud - The speed of the serial port - default 119200
# -p port, --port port - The device of the serial port - default /dev/ttyUSB0
#
# Usage:
#     On the PC, get this script ready to run - but do not execute
#     On the PC-2, do a SETDEV U1,CI,CO (adjust your options - I'm assuming you are using the CWE-158X USB serial port)
#     On the PC-2, do a CLOADa
#     Execute this script

import serial
import sys
import time
import getopt

# Defaults
serial_port = "/dev/ttyUSB0"
baud_rate = 19200

# Optional command line parms to override the defaults
try:
    options, arguments = getopt.getopt(sys.argv[1:], "b:p:", ["baud=","port="])
except getopt.GetoptError as err:
    # print help information and exit:
    print(err)  # will print something like "option -a not recognized"
    raise SystemExit('put_text_file --baud=19200 --port=/dev/ttyUSB0')
    sys.exit(2)

# Max of 2 options permitted
if len(options) > 2:
    raise SystemExit('put_text_file --baud=19200 --port=/dev/ttyUSB0')

# Open the serial port to the PC-2
pc2 = serial.Serial(serial_port,baud_rate,serial.EIGHTBITS,serial.PARITY_NONE,1)

# For each line from stdin
for line in sys.stdin:
	line = line.rstrip() # Pull the \n off the end
	print(line) # Display status of upload
	b_line = bytes(line, 'utf-8') # Convert the line read from utf-8 chars to bytes
	
	pc2.write(b_line) # Write the line to the PC-2
	pc2.write(b'\r') # Send the PC-2 the end of line
	pc2.flush()
	
	time.sleep(0.5)  # Pause to let the PC-2 process the line

# The transfer finishes with an empty line
pc2.write(b'\r')  # End of file
pc2.flush()

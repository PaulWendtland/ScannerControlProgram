import serial

ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=0.2)		# Create serial device

ser.write(b'++mode 1' + b'\n')		# Switch to controller mode
					# "b'<string>' is a short form to convert to bytearray
ser.write(b'++savecfg 0' + b'\n')    # Prevent writes to the EEPROM of the adapter, e.g. on address change

ser.write(bytearray(('++ver' + '\n').encode('utf-8')))	# Request the version number of the Prologix
							# More flexible form for String conversion
print(ser.read(50))	# Read up to 50 bytes (i.e. the above requested version information)


def cmd(address, command, raw=5, n=256):    # "raw": read-after-write-Status (siehe unten);   "n": Zu lesende Bytes
	"Sends <command> to <address> with read-after-write setting <raw> and read up to <n> Bytes: cmd(address, command, raw, n)"

	if raw==0:      # Set device to LISTEN, only send command, do not read a response
		ser.write(bytearray(('++addr ' + str(address) + '\n').encode('utf-8')))
		ser.write(bytearray(('++auto 0' + '\n').encode('utf-8')))
		ser.write(bytearray((str(command) + '\n').encode('utf-8')))
		return

	elif raw==1:	# Set device to LISTEN, send command, read a response until "eoi" flag or n bytes
		ser.write(bytearray(('++addr ' + str(address) + '\n').encode('utf-8')))
		ser.write(bytearray(('++auto 0' + '\n').encode('utf-8')))
		ser.write(bytearray((str(command) + '\n').encode('utf-8')))
		ser.write(bytearray(('++read eoi' + '\n').encode('utf-8')))
		return ser.read(n).decode("utf-8")

	else:       # Activate automatic read-after-write, send command, read up to n bytes
		ser.write(bytearray(('++addr ' + str(address) + '\n').encode('utf-8')))
		ser.write(bytearray(('++auto 1' + '\n').encode('utf-8')))
		ser.write(bytearray((str(command) + '\n').encode('utf-8')))
		return ser.read(n).decode("utf-8")

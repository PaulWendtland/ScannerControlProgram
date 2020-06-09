import subprocess, serial
from PyQt5.QtCore import QObject, pyqtSignal
from time import sleep


class Position(QObject):
	
	status = pyqtSignal(str)
	
	def __init__(self):
		super(Position, self).__init__()
		self.targetx = 0
		self.targety = 0
		self.targetz = 0

		self.initPosZ()

	#===== X-Axis (Tic) =====#
	
	def ticcmdx(self, *args):
		# Call "ticcmd" with the serial number specified and further arguments
		#return subprocess.check_output(['ticcmd', '-d', '00289226'] + list(args))
		return(0)
		
	def xstatus(self):
		# Query the status of the Tic controller and return as status signal
		ticxstatus = self.ticcmdx('-s').decode('ascii')
		self.status.emit(ticxstatus)
		
	def xresume(self):
		# Send "resume" command; identical to "--energize --exit-safe-start"
		self.ticcmdx('--resume')
		self.status.emit('X-axis motor energized - moves to target')
		
	def xdeenergize(self):
		# Turn off stepper motor current
		self.ticcmdx('--deenergize')
		self.status.emit('X-axis motor deenergized')
		
	def xtarget(self):
		# Set new target position. Only actually drives if motor is energized!
		self.ticcmdx('-p' , str(self.targetx))
		self.status.emit('X: ' + str(self.targetx))


	#===== Y-Axis (Tic) =====#
	
	def ticcmdy(self, *args):
		# Call "ticcmd" with the serial number specified and further arguments
		return subprocess.check_output(['ticcmd', '-d', '00288952'] + list(args))
		
	def ystatus(self):
		# Query the status of the Tic controller and return as status signal
		ticystatus = self.ticcmdy('-s').decode('ascii')
		self.status.emit(ticystatus)
		
	def yresume(self):
		# Send "resume" command; identical to "--energize --exit-safe-start"
		self.ticcmdy('--resume')
		self.status.emit('Y-axis motor energized - moves to target')
		
	def ydeenergize(self):
		# Turn off stepper motor current
		self.ticcmdy('--deenergize')
		self.status.emit('Y-axis motor deenergized')
		
	def ytarget(self):
		# Set new target position. Only actually drives if motor is energized!
		self.ticcmdy('-p' , str(self.targety))
		self.status.emit('Y: ' + str(self.targety))


	#===== Z-Achse (Owis) =====#
		
	def initPosZ(self):
		# Start serial connection to the PS-10-32 interface
		self.ps10 = serial.Serial('/dev/ttyACM0', 9600, timeout=0.1)
		sleep(0.1)
		self.ps10.write(b'INIT1\r')		# Initialize axis
		sleep(0.1)
		self.ps10.write(b'ABSOL1\r')		# Activate absolute positioning
		
	def zref_run(self):
		# Do a reference run to the lower end switch, calibrate position
		self.ps10.write(b'REF1=4\r')
	
	def zstatus(self):
		# Query the status and send it as a status signal
		self.ps10.write(b'?MSG\r')
		sleep(0.1)
		self.status.emit('MSG:\n' + self.ps10.read(127).decode('ascii'))
		self.ps10.write(b'?ASTAT\r')
		sleep(0.1)
		self.status.emit('ASTAT:\n' + self.ps10.read(127).decode('ascii'))
		self.ps10.write(b'?ERR\r')
		sleep(0.1)
		self.status.emit('ERR:\n' + self.ps10.read(127).decode('ascii'))
		
	def zdrive(self):
		# Set new (absolute) position and drive
		self.ps10.write(bytearray(('PSET1=' + str(self.targetz) + '\r').encode('ascii')))
		sleep(0.2)
		self.ps10.write(b'PGO1\r')
		self.status.emit('Z: ' + str(self.targetz))
		
	def zpos_query(self):
		# Query the currently set target position (for debugging)
		self.ps10.write(b'?PSET1\r')
		sleep(0.2)
		self.status.emit(self.ps10.read(127).decode('ascii'))
		
	def zefree(self):
		# After the end position switches have been activated:
		# Move away from them and do a reference run
		# Mode 4: "Referenzschalter anfahren und auf Position 0 fahren" (from manual)
		# I am not sure if the motor always travels to the lower end switch!
		self.ps10.write(b'INIT1\r')
		sleep(0.3)
		self.ps10.write(b'EFREE1\r')
		sleep(2)
		self.ps10.write(b'REF1=4')
		self.status.emit('End switches free!')
		
	def zmotor_on(self):
		# Energize the stepper motor
		self.ps10.write(b'MON1\r')
		
	def zmotor_off(self):
		# Deenenergize the motor
		# After doing this, the position is uncalibrated!
		self.ps10.write(b'MOFF1\r')
		
		

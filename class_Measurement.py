import GPIB
from PyQt5.QtCore import QTimer, QObject, pyqtSignal
from time import sleep

class Measurement(QObject):

	status = pyqtSignal(str)	# General status messages
	spec_status = pyqtSignal(str)	# Progress of the current spectrum
	autosave_signal = pyqtSignal()	# Signal is emitted when a spectrum is finished

	def __init__(self):
		super(Measurement, self).__init__()
		
		self.point_count = 400	# Number of data points per spectrum
		self.point_index = 0	# Index/number of the current data point
		self.maxvolt = 0.5	# Maximum voltage of the Magnet PSU controller
		self.bfield_start = 0.02	# B-field at which a spectrum should start
		self.bfield_stop = 0.5		# B-field at which a spectrum should stop
		self.freq = 10.0	# Microwave frequency in GHz as float number
		self.b_cal = []         # Calibration list, b-field values
		self.u_cal = []         # Calibration list, voltage values
		self.u_list = []	# List of voltages for a spectrum
		self.xdata = []		# measured x-data of a spectrum (B-field)
		self.y1data = []	# measured y-data of a spectrum (lock-in R value)
		self.y2data = []	# measured y-data of a spectrum (lock-in phase)
		self.interval = 1000	# Time between datapoints in ms
		self.measurement_runs = False     # Flag whether a measurement is running
		
		self.timer = QTimer()   # Create timer object
		self.timer.timeout.connect(self.update)  # Connect timeout signal with update function
		

	def test(self):
		print("Test!")

	def start(self):
		# Checks if calibration lists are non-empty
		# Checks if planned start and stop fields are within the calibrated range
		# Generates a list of B-field control voltages for a spectrum
		# Resets the x/y1/y2 data lists (Save before re-starting a spectrum!)
		
		if len(self.b_cal) == 0 or len(self.u_cal) == 0:
			self.status.emit('Calibration list empty!')
		elif self.bfield_start < self.b_cal[0] or self.bfield_stop > self.b_cal[-1]:
			self.status.emit('B-field outside of calibrated range!')
		else:
			self.cal_gen() # Generate U(B)-list
			GPIB.cmd(4, ('VSET 1,' + str(self.u_list[0]) + '\n'), 0) # Set first voltage
			#GPIB.cmd(6,(':FREQ ' + str(self.freq) + 'GHz'),0)       # Set MW frequency
			sleep(1)
			self.timer.start(self.interval)
			self.xdata = []        # Reset
			self.y1data = []
			self.y2data = []
			self.measurement_runs = True
			self.status.emit('Measurement started!')

	def stop(self):
		# Stop the recording of a spectrum
		# B-field is set to 0
		# Data lists are not reset yet, they can be manually saved
		self.timer.stop()
		self.measurement_runs = False
		self.point_index = 0
		GPIB.cmd(4, 'VSET 1,0', 0)
		self.status.emit("Measurement stopped!")

	def pause(self):
		self.timer.stop()
		self.measurement_runs = False
		self.status.emit("Measurement paused!")

	def resume(self):
		self.timer.start(self.interval)
		self.measurement_runs = True
		self.status.emit("Measurement resumed!")

	def measure(self):
		# Read Group3 and lock-in values, remove trailing newline character
		# Handles ValueError if the devices return garbage
		# Returns a list of data: (x, R, phi)
		try:
			xval = float(GPIB.cmd(27,'f',1)[1:-1])
			y1val = float(GPIB.cmd(12,'OUTP?3',1)[:-1]) 	# R-value
			y2val = float(GPIB.cmd(12,'OUTP?4',1)[:-1])	# Phi-value
		except ValueError:      # Occasionally the Group3 returns garbage
			xval = 0
			y1val = 0
			y2val = 0

		# Set HP 6625A to the next voltage (for next data point)
		if self.point_index < len(self.u_list) - 1:
			GPIB.cmd(4, ('VSET 1,' + str(self.u_list[self.point_index + 1]) + '\n'), 0)

		return(xval,y1val,y2val)

	def update(self):
		# Update slot function, called by the timeout signal every <self.interval> ms
		# Calls the measure() function to retrieve data from the devices

		data_point = self.measure()
		self.xdata.append(data_point[0])
		self.y1data.append(data_point[1])
		self.y2data.append(data_point[2])
		self.spec_status.emit('Measurement ' + str(self.point_index + 1) + '/' + str(self.point_count))

		if self.point_index >= (self.point_count - 1):
			self.point_index = 0
			GPIB.cmd(4, ('VSET 1,' + str(self.u_list[0]) + '\n'), 0) # Set to first voltage
			self.stop()
			self.autosave_signal.emit()
			
		self.point_index += 1

	def cal_gen(self):
		# Generates a list of control voltages for the magnet PSU for each
		# data point in a spectrum. Uses linear interpolation based on calibration lists
		# The number of points in the output list is given by self.point_count
		bc = self.b_cal		# Abbreviation
		uc = self.u_cal
		bstart = self.bfield_start
		bstop = self.bfield_stop
		datap = self.point_count
		
		bn = len(bc)
		i = 0               # Index for data points
		j = 0               # Index for the calibration list
		bl = []
		ul = []
		while i < datap:
			bcurrent = bstart + i*(bstop - bstart)/datap
			while bc[j] < bcurrent and j < (bn - 1):
				j += 1
				
			ul.append(uc[j-1] + (uc[j] - uc[j-1]) * (bcurrent - bc[j-1])/(bc[j] - bc[j-1]))
			bl.append(bcurrent)
			i +=1
		self.b_list = bl       # Writing back to instance variables only here
		self.u_list = ul

		self.status.emit("Field calibration generated!")





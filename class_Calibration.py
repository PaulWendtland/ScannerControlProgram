import GPIB
from PyQt5.QtCore import QTimer

class Calibration(object):

	def __init__(self):
		self.point_count = 200
		self.point_index = 0
		self.maxvolt = 6.5
		self.volt_start = 0
		self.volt_stop = 4
		self.u_cal = []		# List of control voltages
		self.b_cal = []		# List of measured magnetic fields
		self.xdata = []		# For compatibility with "PlotWindow"
		self.y1data = []	# For compatibility with "PlotWindow"
		self.interval = 500	# Time between measurements in ms
		self.measurement_runs = False	# Activity flag (currently unused)
		self.timer = QTimer()
		self.timer.timeout.connect(self.update)
		self.status = "Idle"

	def start(self):
		self.timer.start(self.interval)
		self.measurement_runs = True
		self.status = "Calibration running!"

	def stop(self):
		self.timer.stop()
		self.measurement_runs = False
		self.point_index = 0
		GPIB.cmd(4, 'VSET 1,0', 0)
		self.status = "Calibration stopped!"

	def cancel(self):
		self.timer.stop()
		self.measurement_runs = False
		self.point_index = 0
		self.u_cal = []
		self.b_cal = []
		GPIB.cmd(4, 'VSET 1,0', 0)
		self.status = "Calibration canceled (reset)!"

	def measure(self, utarget):
		"Returns the value for the magnetic field in Tesla and sets utarget"
		# Read from Group3, remove first and last character (\n)
		xval = float(GPIB.cmd(27,'f',1)[1:-1])

		# Set HP 6625A to the next voltage value (utarget)
		GPIB.cmd(4, ('VSET 1,' + str(utarget) + '\n'), 0)

		return(xval)

	def update(self):
		utarget = (self.volt_stop - self.volt_start)*self.point_index/self.point_count + self.volt_start
		self.u_cal.append(utarget)	# Appends the new target value
		self.b_cal.append(self.measure(utarget))	# Appends the current field value
		self.status = 'Data point ' + str(self.point_index) + 'of' + str(self.point_count)
		self.point_index += 1

		self.xdata = self.u_cal
		self.y1data = self.b_cal

		if self.point_index > self.point_count:
			self.u_cal = self.u_cal[1:]	# Shift u_list down by 1
			self.b_cal = self.b_cal[:-1]	# Remove last b_list value

			self.xdata = self.u_cal
			self.y1data = self.b_cal

			self.stop()



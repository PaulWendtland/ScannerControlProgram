import GPIB
from PyQt5.QtCore import QTimer, QObject, pyqtSignal
from time import sleep

class AFC(QObject):
	
	status = pyqtSignal(str)
	
	def __init__(self):
		super(AFC,self).__init__()
		
		self.afc_timer = QTimer()
		self.afc_timer.timeout.connect(self.afc_update)
		self.afc_point_count = 11	# Number of data points for the AFC calibration
		self.afc_point_index = 0	# Index for the AFC calibration
		self.afc_freq = 10			# Current microwave (MW) frequency
		self.afc_freq_start = 9.8	# MW Frequency to start
		self.afc_freq_stop = 10.2	# MW Frequency to stop
		self.afc_fm_span = 1		# Frequency modulation amplitude in MHz
		self.afc_flist = []		# Calibration list: Frequencies
		self.afc_ulist = []		# Calibration list: Voltages of the lock-in amp
		self.afc_const = 1		# AFC constant: Volts per GHz; init
		self.xdata = []
		self.ydata = []
		
		
		
		
	def afc_config(self):
		# Settings for the SMR40:
		GPIB.cmd(6,'AM:STAT OFF',0)	# Switch off AM, (if used)
		GPIB.cmd(6,'FREQ:MODE CW',0)	# Switch of frequency sweep
		GPIB.cmd(6,'FM:DEV ' + str(self.afc_fm_span) + 'MHz',0)      # FM span corresp. to 1 Volt
		GPIB.cmd(6,'FM:SOUR EXT1',0)	# Use EXT1 as a modulation input
		GPIB.cmd(6,'FM:STAT ON',0)	# Switch on FM
		GPIB.cmd(6,'FREQ ' + str(self.afc_freq_start),0)     # Set first frequency
		GPIB.cmd(6,'OUTP:STAT ON',0)	# Switch on the RF output
		
		# Set lock-in amplitude to approx. 0.7 V rms so it's about 1 V_pp
		# Set modulation frequency, sensitivity and integration time
		GPIB.cmd(8,('SLVL' + str(0.695) + '; FREQ 2000; SENS 19; OFLT 6'),0)
		
		sleep(0.5)      # Wait a bit for the signal to settle
		
		GPIB.cmd(8,'APHS',0)	# Do an "autophase" calibration
		
		self.freq = self.afc_freq_start
		self.status.emit('AFC configuration done!')
		
	def afc_on(self):
		# Switch on FM
		GPIB.cmd(6,'FM:STAT ON',0)
		GPIB.cmd(6,'FREQ ' + str(self.afc_freq),0)
		GPIB.cmd(6,'FREQ:MODE CW',0)    # Switch of sweep mode

		self.status.emit('AFC active (FM on, sweep off)')

	def afc_off(self):
		# Swtich off FM
		GPIB.cmd(6,'FREQ:MODE SWE',0)    # Switch on sweep mode
		GPIB.cmd(6,'FM:STAT OFF',0)

		self.status.emit('AFC inactive (FM off, sweep on')

	def afc_cal_start(self):
		self.afc_ulist = []
		self.afc_flist = []
		self.freq = self.afc_freq_start
		GPIB.cmd(6,'FREQ ' + str(self.afc_freq),0)     # Set to first frequency value
		self.afc_timer.start(500)
		self.status.emit('AFC timer started!')

	def afc_cal_stop(self):
		self.afc_timer.stop()
		self.afc_point_index = 0

		self.status.emit("AFC calibration cancelled (reset)")
	
	def afc_update(self):

		self.afc_ulist.append(float(GPIB.cmd(8,'OUTP?1',1)[:-1]))
		self.afc_flist.append(self.freq)

		self.afc_point_index += 1

		if self.afc_point_index >= self.afc_point_count:
			self.afc_timer.stop()
			self.afc_calculate()
			self.afc_cal_stop()
			self.xdata = self.afc_flist
			self.ydata = self.afc_ulist
		
		self.freq = self.afc_freq_start + (self.afc_point_index/self.afc_point_count)*(self.afc_freq_stop - self.afc_freq_start)
		GPIB.cmd(6,('FREQ ' + str(self.afc_freq) + 'GHz'),0)        # Set frequency
		self.status.emit('Frequency:' + str(self.afc_freq))


	def afc_calculate(self):
		# Calculates a linear fit from the data (slope: V per GHz)
		ul = self.afc_ulist
		fl = self.afc_flist
		# Check for sign change; if it didn't change, no resonance dip was found
		if ul[0] < 0 and ul[-1] < 0:
			self.status.emit('No resonance dip found!')
		elif ul[0] > 0 and ul[-1] > 0:
			self.status.emit('No resonance dip found!')

		N = min(len(ul),len(fl))  # N should be equal to self.point_count
		ms = 0       # Sum of sucessive slopes (differences); init
		
		i = 0
		while i < (N-1):        # Adds the slopes between points i and i+1
			ms += ((ul[i+1] - ul[i])/(fl[i+1] - fl[i]))
			i += 1

		self.afc_const = ms/N       # Normalized, unit is V/GHz

		self.status.emit("AFC constant for the current resonance dip calculated!")
		self.status.emit('AFC constant: ' + str(self.afc_const))


	def afc(self):
		# Changes the MW frequency to center of dip (minimal lock-in signal)
		self.afc_on()
		sleep(1)
		lockin = float(GPIB.cmd(8,'OUTP?1',1))     # query x-value
		fshift = -(lockin / self.afc_const)    # Calculated frequency shift in GHz
		self.status.emit('LockIn:' + 'Frequecy shift:' + str(fshift) + ' GHz')
		GPIB.cmd(6,('FREQ ' + str(self.afc_freq + fshift) + ' GHz'),0)
		self.freq += fshift
		self.afc_off()

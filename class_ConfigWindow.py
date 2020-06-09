from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSignal, QTimer
import sys

class ConfigWindow(QtGui.QWidget):

	def __init__(self, fmr_measure, cal_measure, afc, pos_control):
		super(ConfigWindow, self).__init__()
		self.FMRmes = fmr_measure	# Instance name of FMR measurement
		self.Calmes = cal_measure       # Instance name of calibration measurement
		self.AFC = afc		# Instance name of "automatic frequency correction"
		self.Position = pos_control # Instance name of position control
		self.initUI()


	def initUI(self):
		
		self.setWindowTitle('Configuration Window')

		self.layout = QtGui.QGridLayout()
		self.setLayout(self.layout)
		
		self.scan = False
		self.settle_timer = QTimer()
		self.settle_timer.timeout.connect(self.scan_settle)

		# Create tabs
		self.tabs = QtGui.QTabWidget()
		self.tab1 = QtGui.QWidget()
		self.tab2 = QtGui.QWidget()
		self.tab3 = QtGui.QWidget()
		self.tab4 = QtGui.QWidget()
		self.tab5 = QtGui.QWidget()

		self.tabs.addTab(self.tab1,"Measurement")
		self.tabs.addTab(self.tab2,"Calibration")
		self.tabs.addTab(self.tab3,"AFC")
		self.tabs.addTab(self.tab4,"Position")
		self.tabs.addTab(self.tab5,"Motor control")

		# Set tab layout
		self.tab1.layout = QtGui.QGridLayout()
		self.tab2.layout = QtGui.QGridLayout()
		self.tab3.layout = QtGui.QGridLayout()
		self.tab4.layout = QtGui.QGridLayout()
		self.tab5.layout = QtGui.QGridLayout()
		
		self.tab1.setLayout(self.tab1.layout)
		self.tab2.setLayout(self.tab2.layout)
		self.tab3.setLayout(self.tab3.layout)
		self.tab4.setLayout(self.tab4.layout)
		self.tab5.setLayout(self.tab5.layout)
		

		#====== Add the widgets to the tabs =======

		# Tab1: "Measurement", central measurement parameters
		# Define the widgets

		self.tab1.startbtn = QtGui.QPushButton('Start')
		self.tab1.pausebtn = QtGui.QPushButton('Pause')
		self.tab1.stopbtn = QtGui.QPushButton('Stop')
		self.tab1.data_savebtn = QtGui.QPushButton('Save current spectrum')
		self.tab1.quitbtn = QtGui.QPushButton('Quit program')

		self.tab1.spectrum_path_label = QtGui.QLabel('Spectrum save path:')
		self.tab1.spectrum_path = QtGui.QLineEdit("/home/paul/Desktop/Messdaten/2020-03-03/Spektrum.dat")

		self.tab1.bfield_start_label = QtGui.QLabel('B-field start [T]:')
		self.tab1.bfield_start = QtGui.QLineEdit('0.03')
		
		self.tab1.bfield_stop_label = QtGui.QLabel('B-field stop [T]:')
		self.tab1.bfield_stop = QtGui.QLineEdit('0.5')
		
		self.tab1.point_count_label = QtGui.QLabel('Data points')
		self.tab1.point_count = QtGui.QLineEdit('200')

		# Adding the widgets to the layout:
		
		self.tab1.layout.addWidget(self.tab1.startbtn, 0, 0)
		self.tab1.layout.addWidget(self.tab1.pausebtn, 1, 0)
		self.tab1.layout.addWidget(self.tab1.stopbtn, 2, 0)
		self.tab1.layout.addWidget(self.tab1.quitbtn, 3, 0)
		self.tab1.layout.addWidget(self.tab1.data_savebtn, 4,0)
		
		self.tab1.layout.addWidget(self.tab1.spectrum_path_label, 0, 2)
		self.tab1.layout.addWidget(self.tab1.spectrum_path, 0, 3)
		self.tab1.layout.addWidget(self.tab1.bfield_start_label, 2, 2)
		self.tab1.layout.addWidget(self.tab1.bfield_start, 2, 3)
		self.tab1.layout.addWidget(self.tab1.bfield_stop_label, 3, 2)
		self.tab1.layout.addWidget(self.tab1.bfield_stop, 3, 3)
		
		self.tab1.layout.addWidget(self.tab1.point_count_label, 4, 2)
		self.tab1.layout.addWidget(self.tab1.point_count, 4, 3)


		# Tab2: "Calibration", Control elements for generating a calibration file
		
		self.tab2.cal_path_label = QtGui.QLabel('Calibration file path:')
		self.tab2.cal_path = QtGui.QLineEdit(sys.path[0] + "/calibration.dat")
		self.tab2.cal_startbtn = QtGui.QPushButton('Start calibration')
		self.tab2.cal_stopbtn = QtGui.QPushButton('Abort calibration')
		self.tab2.cal_setbtn = QtGui.QPushButton('Set calibration')
		self.tab2.cal_loadbtn = QtGui.QPushButton('Load calibration')
		self.tab2.cal_savebtn = QtGui.QPushButton('Save calibration')

		# Add the widgets to the layout
		
		self.tab2.layout.addWidget(self.tab2.cal_startbtn, 6, 3)
		self.tab2.layout.addWidget(self.tab2.cal_stopbtn, 7, 3)
		self.tab2.layout.addWidget(self.tab2.cal_setbtn, 8, 3)
		self.tab2.layout.addWidget(self.tab2.cal_loadbtn, 9, 3)
		self.tab2.layout.addWidget(self.tab2.cal_savebtn, 10, 3)
		self.tab2.layout.addWidget(self.tab2.cal_path_label, 5, 2)
		self.tab2.layout.addWidget(self.tab2.cal_path, 5, 3)


		# Tab3: "AFC", Control elements for the AFC

		self.tab3.afc_configbtn = QtGui.QPushButton('Configure devices')
		self.tab3.afc_calstartbtn = QtGui.QPushButton('Start AFC-cal.')
		self.tab3.afc_calstopbtn = QtGui.QPushButton('Stop AFC-cal.')
		self.tab3.afc_dobtn = QtGui.QPushButton('Do AFC')

		self.tab3.afc_onoff_box = QtGui.QCheckBox('AFC on/off')
		self.tab3.afc_point_count_label = QtGui.QLabel('Datapoints:')
		self.tab3.afc_point_count = QtGui.QLineEdit('11')
		self.tab3.afc_startfreq_label = QtGui.QLabel('Startfreq. in GHz:')
		self.tab3.afc_startfreq = QtGui.QLineEdit('9.1')
		self.tab3.afc_stopfreq_label = QtGui.QLabel('Stopfreq. in GHz:')
		self.tab3.afc_stopfreq = QtGui.QLineEdit('9.2')

		self.tab3.testbtn = QtGui.QPushButton('Test signal/slot')

		# ToDo: do AFC only if it is calibrated

		# Add the widgets to the layout

		self.tab3.layout.addWidget(self.tab3.afc_configbtn, 1, 1)
		self.tab3.layout.addWidget(self.tab3.afc_calstartbtn, 2, 1)
		self.tab3.layout.addWidget(self.tab3.afc_calstopbtn, 3, 1)
		self.tab3.layout.addWidget(self.tab3.afc_dobtn, 4, 1)

		self.tab3.layout.addWidget(self.tab3.afc_onoff_box, 1,2)
		self.tab3.layout.addWidget(self.tab3.afc_point_count_label, 2, 2)
		self.tab3.layout.addWidget(self.tab3.afc_point_count, 2, 3)
		self.tab3.layout.addWidget(self.tab3.afc_startfreq_label, 3, 2)
		self.tab3.layout.addWidget(self.tab3.afc_startfreq, 3, 3)
		self.tab3.layout.addWidget(self.tab3.afc_stopfreq_label, 4, 2)
		self.tab3.layout.addWidget(self.tab3.afc_stopfreq, 4, 3)

		self.tab3.layout.addWidget(self.tab3.testbtn, 5, 1)
		
		
		# Tab4: Controls and displays for the positioning system
		
		# Label:
		self.tab4.pos_unit_label = QtGui.QLabel('Positions in µm!')
		self.tab4.pos_axis_label = QtGui.QLabel('Axis:')
		self.tab4.pos_current_label = QtGui.QLabel('Current:')
		self.tab4.pos_new_abs_label = QtGui.QLabel('New absolute:')
		self.tab4.pos_new_rel_label = QtGui.QLabel('New relative:')
		self.tab4.pos_increment_label = QtGui.QLabel('Increment:')
		self.tab4.pos_x_label = QtGui.QLabel('X-axis')
		self.tab4.pos_y_label = QtGui.QLabel('Y-axis')
		self.tab4.pos_z_label = QtGui.QLabel('Z-axis')
		
		# Displayint the current position:
		self.tab4.pos_x = QtGui.QLineEdit('0')
		self.tab4.pos_y = QtGui.QLineEdit('0')
		self.tab4.pos_z = QtGui.QLineEdit('0')
		
		# Next position (absolute):
		self.tab4.pos_abs_set_x = QtGui.QLineEdit('0')
		self.tab4.pos_abs_set_y = QtGui.QLineEdit('0')
		self.tab4.pos_abs_set_z = QtGui.QLineEdit('0')
		
		# Next position (relative change):
		self.tab4.pos_rel_set_x = QtGui.QLineEdit('0')
		self.tab4.pos_rel_set_y = QtGui.QLineEdit('0')
		self.tab4.pos_rel_set_z = QtGui.QLineEdit('0')
		
		# Increment per spectrum:
		self.tab4.pos_incr_x = QtGui.QLineEdit('0')
		self.tab4.pos_incr_y = QtGui.QLineEdit('0')
		self.tab4.pos_incr_z = QtGui.QLineEdit('0')
		
		# Buttons:
		self.tab4.pos_set_btn = QtGui.QPushButton('Set position')
		self.tab4.pos_zero_set_btn = QtGui.QPushButton('Set zero')
		self.tab4.pos_scan_check = QtGui.QCheckBox('Scanning')
		
		
		# Add the widgets to the tab layout
		
		self.tab4.layout.addWidget(self.tab4.pos_unit_label, 0,1)
		self.tab4.layout.addWidget(self.tab4.pos_axis_label, 1,1)
		self.tab4.layout.addWidget(self.tab4.pos_current_label, 2,1)
		self.tab4.layout.addWidget(self.tab4.pos_new_abs_label, 3,1)
		self.tab4.layout.addWidget(self.tab4.pos_new_rel_label, 4,1)
		self.tab4.layout.addWidget(self.tab4.pos_increment_label, 5,1)
		
		self.tab4.layout.addWidget(self.tab4.pos_x_label, 1,2)
		self.tab4.layout.addWidget(self.tab4.pos_y_label, 1,3)
		self.tab4.layout.addWidget(self.tab4.pos_z_label, 1,4)
		
		self.tab4.layout.addWidget(self.tab4.pos_x, 2,2)
		self.tab4.layout.addWidget(self.tab4.pos_y, 2,3)
		self.tab4.layout.addWidget(self.tab4.pos_z, 2,4)
		
		self.tab4.layout.addWidget(self.tab4.pos_abs_set_x, 3,2)
		self.tab4.layout.addWidget(self.tab4.pos_abs_set_y, 3,3)
		self.tab4.layout.addWidget(self.tab4.pos_abs_set_z, 3,4)
		
		self.tab4.layout.addWidget(self.tab4.pos_rel_set_x, 4,2)
		self.tab4.layout.addWidget(self.tab4.pos_rel_set_y, 4,3)
		self.tab4.layout.addWidget(self.tab4.pos_rel_set_z, 4,4)
		
		self.tab4.layout.addWidget(self.tab4.pos_incr_x, 5,2)
		self.tab4.layout.addWidget(self.tab4.pos_incr_y, 5,3)
		self.tab4.layout.addWidget(self.tab4.pos_incr_z, 5,4)
		
		self.tab4.layout.addWidget(self.tab4.pos_zero_set_btn, 2,6)
		self.tab4.layout.addWidget(self.tab4.pos_set_btn, 4,6)
		self.tab4.layout.addWidget(self.tab4.pos_scan_check, 5,6)
		
		
		# Tab5: Stepper motor control (Pololu Tic + OWIS PS 10-32)
		
		self.tab5.motor_x_label = QtGui.QLabel('X-axis')
		self.tab5.motor_y_label = QtGui.QLabel('Y-axis')
		self.tab5.motor_z_label = QtGui.QLabel('Z-axis')
		
		self.tab5.motor_x_status_btn = QtGui.QPushButton('Request status')
		self.tab5.motor_x_deenergize_btn = QtGui.QPushButton('Motor off')
		self.tab5.motor_x_resume_btn = QtGui.QPushButton('Motor on')
		
		self.tab5.motor_y_status_btn = QtGui.QPushButton('Request status')
		self.tab5.motor_y_deenergize_btn = QtGui.QPushButton('Motor off')
		self.tab5.motor_y_resume_btn = QtGui.QPushButton('Motor on')
		
		self.tab5.motor_z_status_btn = QtGui.QPushButton('Request status')
		self.tab5.motor_z_pos_check_btn = QtGui.QPushButton('Request position')
		self.tab5.motor_z_efree_btn = QtGui.QPushButton('Move away from stops')
		self.tab5.pos_z_motor_check = QtGui.QCheckBox('Z-Motor on/off')
		self.tab5.pos_z_calibration_run_btn = QtGui.QPushButton('Calibration run')
		
		# Add the widgets to the tab layout
		
		self.tab5.layout.addWidget(self.tab5.motor_x_label, 1,1)
		self.tab5.layout.addWidget(self.tab5.motor_y_label, 1,2)
		self.tab5.layout.addWidget(self.tab5.motor_z_label, 1,3)
		
		self.tab5.layout.addWidget(self.tab5.motor_x_status_btn, 2,1)
		self.tab5.layout.addWidget(self.tab5.motor_x_deenergize_btn, 3,1)
		self.tab5.layout.addWidget(self.tab5.motor_x_resume_btn, 4,1)
		
		self.tab5.layout.addWidget(self.tab5.motor_y_status_btn, 2,2)
		self.tab5.layout.addWidget(self.tab5.motor_y_deenergize_btn, 3,2)
		self.tab5.layout.addWidget(self.tab5.motor_y_resume_btn, 4,2)
		
		self.tab5.layout.addWidget(self.tab5.motor_z_status_btn, 2,3)
		self.tab5.layout.addWidget(self.tab5.motor_z_pos_check_btn, 3,3)
		self.tab5.layout.addWidget(self.tab5.motor_z_efree_btn, 4,3)
		self.tab5.layout.addWidget(self.tab5.pos_z_motor_check, 5,3)
		self.tab5.layout.addWidget(self.tab5.pos_z_calibration_run_btn, 6,3)
		
		


		#===== Add the objects/widgets to the main window =====

		self.status = QtGui.QTextEdit()
		self.spec_status = QtGui.QLabel('Measurement n/N')

		
		# self.GPIB_cmd = QtGui.QTextEdit("12,'APHAS',0")
		# self.GPIB_cmd_btn = QtGui.QPushButton('Send')

		self.layout.addWidget(self.tabs, 0,0)
		
		self.layout.addWidget(self.status, 15, 0)
		self.layout.addWidget(self.spec_status, 16, 0)

		#===== Signal-slot connections =====

		# Tab1
		self.tab1.startbtn.clicked.connect(self.start_meas)
		self.tab1.pausebtn.clicked.connect(self.FMRmes.pause)
		self.tab1.stopbtn.clicked.connect(self.FMRmes.stop)
		self.tab1.data_savebtn.clicked.connect(self.save_meas)
		self.tab1.quitbtn.clicked.connect(sys.exit)
		
		# Tab2
		self.tab2.cal_startbtn.clicked.connect(self.Calmes.start)
		self.tab2.cal_stopbtn.clicked.connect(self.Calmes.cancel)
		self.tab2.cal_setbtn.clicked.connect(self.cal_set)
		self.tab2.cal_loadbtn.clicked.connect(self.cal_load)
		self.tab2.cal_savebtn.clicked.connect(self.cal_save)

		# Tab3
		self.tab3.afc_configbtn.clicked.connect(self.afc_config)
		self.tab3.afc_calstartbtn.clicked.connect(self.afc_cal_start)
		self.tab3.afc_calstopbtn.clicked.connect(self.AFC.afc_cal_stop)
		self.tab3.afc_dobtn.clicked.connect(self.AFC.afc)
		self.tab3.testbtn.clicked.connect(self.signaltest)
		self.tab3.afc_onoff_box.toggled.connect(self.afc_onoff)
		
		# Tab4
		self.tab4.pos_set_btn.clicked.connect(self.pos_set)

		self.tab4.pos_abs_set_x.textEdited.connect(self.pos_abs_mod_x)
		self.tab4.pos_rel_set_x.textEdited.connect(self.pos_rel_mod_x)

		self.tab4.pos_abs_set_y.textEdited.connect(self.pos_abs_mod_y)
		self.tab4.pos_rel_set_y.textEdited.connect(self.pos_rel_mod_y)

		self.tab4.pos_abs_set_z.textEdited.connect(self.pos_abs_mod_z)
		self.tab4.pos_rel_set_z.textEdited.connect(self.pos_rel_mod_z)

		self.tab4.pos_scan_check.toggled.connect(self.pos_scan_onoff)
		self.tab4.pos_zero_set_btn.clicked.connect(self.pos_zero_set)
		
		self.tab4.pos_x.setReadOnly(True)
		self.tab4.pos_y.setReadOnly(True)
		self.tab4.pos_z.setReadOnly(True)
		
		# Tab5
		self.tab5.motor_x_status_btn.clicked.connect(self.Position.xstatus)
		self.tab5.motor_x_deenergize_btn.clicked.connect(self.Position.xdeenergize)
		self.tab5.motor_x_resume_btn.clicked.connect(self.Position.xresume)

		self.tab5.motor_y_status_btn.clicked.connect(self.Position.ystatus)
		self.tab5.motor_y_deenergize_btn.clicked.connect(self.Position.ydeenergize)
		self.tab5.motor_y_resume_btn.clicked.connect(self.Position.yresume)
		
		self.tab5.motor_z_status_btn.clicked.connect(self.Position.zstatus)
		self.tab5.motor_z_pos_check_btn.clicked.connect(self.Position.zpos_query)
		self.tab5.motor_z_efree_btn.clicked.connect(self.Position.zefree)
		self.tab5.pos_z_motor_check.toggled.connect(self.pos_z_motor_onoff)
		self.tab5.pos_z_calibration_run_btn.clicked.connect(self.Position.zref_run)
		
		self.tab5.pos_z_motor_check.setChecked(True)

		# Main window
		self.status.setReadOnly(True)

		self.FMRmes.status.connect(self.status_update)
		self.FMRmes.spec_status.connect(self.spec_status_update)
		self.Position.status.connect(self.status_update)
		self.FMRmes.autosave_signal.connect(self.autosave)





	def status_update(self, message):
		self.status.append(message)

	def spec_status_update(self, message):
		self.spec_status.setText(message)


#========== Measurement methods ==========

	def test(self):
		self.status_update('Message test!')

	def start_meas(self):
		# Write all necessary parameters to the measurement instance
		try:
			self.FMRmes.bfield_start = float(self.tab1.bfield_start.text())
			self.FMRmes.bfield_stop = float(self.tab1.bfield_stop.text())
			self.FMRmes.point_count = int(self.tab1.point_count.text())
			self.FMRmes.start()
		except ValueError:
			self.status_update('Start-/Stop field not a float number!')

	def save_meas(self):
		try:
			result = open(self.tab1.spectrum_path.text(),"w")
			xdat = self.FMRmes.xdata
			y1dat = self.FMRmes.y1data
			y2dat = self.FMRmes.y2data
			i = 0           # Counter index
			output = ''	# Initializing output string
		
			while i < len(xdat) and i < len(y1dat) and i < len(y2dat):
				output += str(xdat[i]) + "\t" + str(y1dat[i]) + "\t" + str(y2dat[i]) + "\n"
				i += 1
		
			result.write(output)
			result.close()
			self.status_update('Measurement saved!')
		except:
			self.status_update('Some error occured during saving!\n Folder not existing?')
			
	def autosave(self):
		if self.scan == True:
			save_path = self.tab1.spectrum_path.text()[:-4]
			self.tab1.spectrum_path.setText(save_path + '_pos_x' + self.tab4.pos_x.text() + '_y' + self.tab4.pos_y.text() + '_z' + self.tab4.pos_z.text() + '.dat')
			self.save_meas()
			self.tab1.spectrum_path.setText(save_path + '.dat')
			self.scan_increment()
			self.settle_timer.start(5000)
			self.status_update('Moving increment. Waiting 5 sec. for field to settle.')
			
	def scan_settle(self):
		self.settle_timer.stop()
		self.start_meas()
		
		

#========== Calibration methods ==========#

	def cal_set(self):
		self.FMRmes.u_cal = self.Calmes.u_cal
		self.FMRmes.b_cal = self.Calmes.b_cal
		self.status_update('Measurement calibrated. Length: ' + str(len(self.FMRmes.u_cal)))

	def cal_save(self):
		output = ''     # String to be written to the calibration file
		i = 0           # index
		uc = self.Calmes.u_cal
		bc = self.Calmes.b_cal
		
		while i < len(uc) and i < len(bc):
			output += str(uc[i]) + "\t" + str(bc[i]) + "\n"
			i += 1
		
		try:
			calib_file = open(self.tab2.cal_path.text(), "w")
			calib_file.write(output)
			calib_file.close()
		except:
			self.status_update('Some error occured during saving!\n Folder not existing?')
						  
	def cal_load(self):
		# Loads a file with two columns and splits it into two lists

		input = ''      # String to be read from the file
		i = 0           # Counter index
		s = ''          # Splitted string
		uc = []         # List of voltages
		bc = []         # List of B-fields
		
		try:
			calib_file = open(self.tab2.cal_path.text(), "r")
			# Split string into list of strings (x1, y1, x2, y2,...):
			s = calib_file.read().split()
			calib_file.close()
		except:
			self.status_update('Some error occured during loading!\n Folder or file not existing?')
		
		while i < len(s):
			# Append to the lists alternatingly
			uc.append(float(s[i]))
			bc.append(float(s[i+1]))
			i += 2

		self.Calmes.u_cal = uc
		self.Calmes.b_cal = bc
		
		self.status_update('Calibration loaded!   uc: ' + str(len(uc)) + ';  bc: ' + str(len(bc)))


#========== AFC methods ============#

	def afc_config(self):
		try:
			self.AFC.afc_freq_start = float(self.tab3.afc_startfreq.text())
			self.AFC.afc_freq_stop = float(self.tab3.afc_stopfreq.text())
			self.AFC.afc_config()
		except ValueError:
			self.status_update('AFC frequency not a float!')
	
	
	def afc_cal_start(self):
		try:
			self.AFC.afc_freq_start = float(self.tab3.afc_startfreq.text())
			self.AFC.afc_freq_stop = float(self.tab3.afc_stopfreq.text())
		except ValueError:
			self.status_update('AFC frequency not a float!')
			
		try:
			self.AFC.afc_point_count = int(self.tab3.afc_point_count.text())
			self.AFC.afc_cal_start()
		except ValueError:
			self.status_update('Number of AFC data points not an integer!')
			
		
		
	def afc_onoff(self):
		if self.tab3.afc_onoff_box.isChecked() == True:
			self.AFC.afc_on()
		elif self.tab3.afc_onoff_box.isChecked() == False:
			self.AFC.afc_off()
		
		
	def signaltest(self):
		self.status_update('Signal-Test')


#========== Position methods ============#

	#===== X-axis =====#
			
	def pos_abs_mod_x(self):
		# Is called when the new absolute x target position was changed
		# Synchronizes the new relative and absolue target positions
		try:
			xpos = int(self.tab4.pos_x.text())
			xpos_abs = int(self.tab4.pos_abs_set_x.text())
			self.tab4.pos_rel_set_x.setText(str(xpos_abs - xpos))
		except ValueError:
			self.status_update('Position not an integer!')
		
	def pos_rel_mod_x(self):
		# As above, but now the absolute position is synced with the relative one
		try:
			xpos = int(self.tab4.pos_x.text())
			xpos_rel = int(self.tab4.pos_rel_set_x.text())
			self.tab4.pos_abs_set_x.setText(str(xpos + xpos_rel))
		except ValueError:
			self.status_update('Position not an integer!')

	#===== y-axis =====#
			
	def pos_abs_mod_y(self):
		# Is called when the new absolute y target position was changed
		# Synchronizes the new relative and absolue target positions
		try:
			ypos = int(self.tab4.pos_y.text())
			ypos_abs = int(self.tab4.pos_abs_set_y.text())
			self.tab4.pos_rel_set_y.setText(str(ypos_abs - ypos))
		except ValueError:
			self.status_update('Position not an integer!')
		
	def pos_rel_mod_y(self):
		# As above, but now the absolute position is synced with the relative one
		try:
			ypos = int(self.tab4.pos_y.text())
			ypos_rel = int(self.tab4.pos_rel_set_y.text())
			self.tab4.pos_abs_set_y.setText(str(ypos + ypos_rel))
		except ValueError:
			self.status_update('Position not an integer!')



	#===== Z-axis =====#

	def pos_abs_mod_z(self):
		# As for x and y axes, synchronizes realtive and absolute positions
		try:
			zpos = int(self.tab4.pos_z.text())
			zpos_abs = int(self.tab4.pos_abs_set_z.text())
			self.tab4.pos_rel_set_z.setText(str(zpos_abs - zpos))
		except ValueError:
			self.status_update('Z-Position kein Integer!')

	def pos_rel_mod_z(self):
		# As for x and y axes, synchronizes realtive and absolute positions
		try:
			zpos = int(self.tab4.pos_z.text())
			zpos_rel = int(self.tab4.pos_rel_set_z.text())
			self.tab4.pos_abs_set_z.setText(str(zpos + zpos_rel))
		except ValueError:
			self.status_update('Z-Position kein Integer!')

	def pos_z_motor_onoff(self):
		# Turns the stepper motor of the HUMES60 on or off
		if self.tab5.pos_z_motor_check.isChecked() == True:
			self.Position.zmotor_on()
			self.status_update('Z stage motor on!')
		elif self.tab5.pos_z_motor_check.isChecked() == False:
			self.Position.zmotor_off()
			self.status_update('Z stage motor off!')


	#===== All Axes =====#

	def pos_set(self):
		# Set the new positions and drive
		try:
			# Read the new absolute positions:
			xpos = int(self.tab4.pos_abs_set_x.text())
			ypos = int(self.tab4.pos_abs_set_y.text())
			zpos = int(self.tab4.pos_abs_set_z.text())

			# Set them into the text fields for the current position
			self.tab4.pos_x.setText(str(xpos))
			self.tab4.pos_y.setText(str(ypos))
			self.tab4.pos_z.setText(str(zpos))

			# Set the target position variables in the Position instance
			self.Position.targetx = int(round(xpos/0.375))
			self.Position.targety = int(round(ypos/0.375))
			self.Position.targetz = int(round(zpos*20))

			# Synchronize absolute and relative position (i.e. set rel. pos. to 0)
			self.pos_abs_mod_x()
			self.pos_abs_mod_y()
			self.pos_abs_mod_z()

			# Start the positioning of the stepper motors
			self.Position.xtarget()
			self.Position.ytarget()
			self.Position.zdrive()
		except ValueError:
			self.status_update('Positions not integers!')	
			
	def pos_zero_set(self):
		# Define current position as 0
		self.tab4.pos_x.setText('0')
		self.tab4.pos_y.setText('0')
		self.tab4.pos_z.setText('0')
				
	def pos_scan_onoff(self):
		# Sets a flag whether the position should be changed by the set
		# increment after each spectrum is recorded
		if self.tab4.pos_scan_check.isChecked() == True:
			self.status_update('Scanning enabled!')
			self.scan = True
		elif self.tab4.pos_scan_check.isChecked() == False:
			self.status_update('Scanning disabled!')
			self.scan = False
			
	def scan_increment(self):
		# Set the new incremented positions and drive
		try:
			# Calculate the new positions:
			xpos = int(self.tab4.pos_x.text()) + int(self.tab4.pos_incr_x.text())
			ypos = int(self.tab4.pos_y.text()) + int(self.tab4.pos_incr_y.text())
			zpos = int(self.tab4.pos_z.text()) + int(self.tab4.pos_incr_z.text())

			# Set them into the text fields for the current position
			self.tab4.pos_x.setText(str(xpos))
			self.tab4.pos_y.setText(str(ypos))
			self.tab4.pos_z.setText(str(zpos))

			# Set the target position variables in the Position instance
			self.Position.targetx = int(round(xpos/0.375))
			self.Position.targety = int(round(ypos/0.375))
			self.Position.targetz = int(round(zpos*20))

			# Synchronize absolute and relative position (i.e. set rel. pos. to 0)
			self.pos_abs_mod_x()
			self.pos_abs_mod_y()
			self.pos_abs_mod_z()

			# Start the positioning of the stepper motors
			self.Position.xtarget()
			self.Position.ytarget()
			self.Position.zdrive()
		except ValueError:
			self.status_update('Positions not integers!')	


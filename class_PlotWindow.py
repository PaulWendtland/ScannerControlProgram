from PyQt5 import QtGui
import pyqtgraph as pg

class PlotWindow(QtGui.QWidget):
	
	def __init__(self, SourceName):
		super(PlotWindow, self).__init__()
		self.Source1 = SourceName
		self.initUI()

	def initUI(self):
		
		self.setWindowTitle('Plot Window')

		self.timer = pg.QtCore.QTimer()		# Create timer
		self.timer.timeout.connect(self.update)	# Set timeout target
		self.timer.start(200)
		
		self.plotwidget = pg.PlotWidget()
		self.plot = self.plotwidget.plot()
		self.status = QtGui.QLabel('Started')
		
		self.layout = QtGui.QGridLayout()
		self.setLayout(self.layout)

		self.layout.addWidget(self.status, 3, 0)
		self.layout.addWidget(self.plotwidget, 0, 1, 6, 1)

	def update(self):

		self.plot.setData(self.Source1.xdata, self.Source1.y1data)

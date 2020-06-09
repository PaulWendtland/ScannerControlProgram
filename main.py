from PyQt5 import QtGui

from class_Measurement import Measurement
from class_Calibration import Calibration
from class_PlotWindow import PlotWindow
from class_ConfigWindow import ConfigWindow
from class_Position import Position
from class_AFC import AFC

app = QtGui.QApplication([])

FMR = Measurement()
Calib = Calibration()
AFC = AFC()
Stage = Position()

measwin = PlotWindow(FMR)
measwin.show()

calibwin = PlotWindow(Calib)
calibwin.show()

confwin = ConfigWindow(FMR, Calib, AFC, Stage)
confwin.show()

app.exec_()

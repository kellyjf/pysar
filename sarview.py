# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'sarview.ui'
#
# Created: Sun Mar 20 13:43:31 2016
#      by: PyQt4 UI code generator 4.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from ui_sarview import *
from app_export import *
import subprocess

class SarView (QMainWindow, Ui_SarView):

	[MODE_DEVICE, MODE_METRIC] = range(2)

	def __init__(self, Parent=None, filename=None):
		super(QMainWindow,self).__init__(Parent)
		self.setupUi(self)

		self.connect(self.action_Open, SIGNAL("activated()"), self.openFile)
		self.connect(self.action_Plot, SIGNAL("activated()"), self.drawGraph)
		self.connect(self.action_Export, SIGNAL("activated()"), self.exportSettings)
		self.connect(self.action_Lines, SIGNAL("triggered(bool)"), self.toggleLines)
		self.connect(self.action_All, SIGNAL("triggered(bool)"), self.allCombos)
		self.connect(self.metricCombo, SIGNAL("currentIndexChanged(QString)"), self.metricSelect)
		self.connect(self.deviceCombo, SIGNAL("currentIndexChanged(QString)"), self.deviceSelect)

		self.device_dict={}
		self.metric_dict={}
		
		self.connect(self.action_Devices, SIGNAL("activated()"), self.deviceCombo.showPopup)
		self.connect(self.action_Metrics, SIGNAL("activated()"), self.metricCombo.showPopup)

		self.output = None
		self.format = None
		self.exportDialog=Export(self)
		self.connect(self.exportDialog, SIGNAL("accepted()"), self.exportGraph)

		if(filename != None):
			self.processFile(filename)

	def devpop(self):
		self.deviceCombo.showPopup()	

	def allCombos(self, allBool):
		self.comboTable.setRangeSelected(QTableWidgetSelectionRange(0,0,self.comboTable.rowCount()-1,0),allBool)
			
	def exportSettings(self):
		self.exportDialog.show()

	def exportGraph(self):
		self.output = self.exportDialog.filename
		self.format = self.exportDialog.format			
		self.drawGraph()

	def toggleLines(self, value):
		print value

	def drawGraph(self):
		plots=[]
		metname=str(self.metricCombo.currentText())
		devname=str(self.deviceCombo.currentText())
		for item in self.comboTable.selectedItems():
			if self.mode==SarView.MODE_METRIC:
				devname=item.text()
				filter=" \"<(sadf -U -- -A %s | awk -vdev=%s -vmet=%s 'NR==1{off=$3}$4==dev&&$5==met{print $3-off,$6}')\" using 1:2 with lines title \"%s\""%(self.filename, devname, metname,devname)
			elif self.mode==SarView.MODE_DEVICE:
				metname=item.text()
				filter=" \"<(sadf -U -- -A %s | awk -vdev=%s -vmet=%s 'NR==1{off=$3}$4==dev&&$5==met{print $3-off,$6}')\" using 1:2 with lines title \"%s\""%(self.filename, devname, metname,metname)

			plots.append(filter)
		
		proc=subprocess.Popen(["gnuplot","-p"], stdin=subprocess.PIPE)
		if self.output != None:
			proc.stdin.write("set terminal \"%s\"\n"%(self.format.lower()))
			proc.stdin.write("set output \"%s\"\n"%(self.output))
			self.output = None
			self.format = None
	
		if self.mode==SarView.MODE_METRIC:
			proc.stdin.write("set title \"%s\"\n"%(metname))
		elif self.mode==SarView.MODE_DEVICE:
			proc.stdin.write("set title \"%s\"\n"%(devname))
		proc.stdin.write("set title \"%s\"\n"%(metname))
		proc.stdin.write("set xlabel \"seconds\"\n")

		proc.stdin.write( "plot "+",".join(plots)+"\n")


	def metricSelect(self, metric):
		self.mode=SarView.MODE_METRIC
		self.comboTable.clear()
		self.comboTable.setHorizontalHeaderItem(0, QTableWidgetItem("Device"))
		for row in range(1+self.comboTable.rowCount()):
			self.comboTable.removeRow(0)
		for (row,device) in enumerate(self.metric_dict[str(metric)]):
			self.comboTable.insertRow(row)
			self.comboTable.setItem(row, 0, QTableWidgetItem(device))
		self.allCombos(True)

	def deviceSelect(self, metric):
		self.mode=SarView.MODE_DEVICE
		self.comboTable.clear()
		self.comboTable.setHorizontalHeaderItem(0, QTableWidgetItem("Metric"))
		for row in range(1+self.comboTable.rowCount()):
			self.comboTable.removeRow(0)
		for (row,metric) in enumerate(self.device_dict[str(metric)]):
			self.comboTable.insertRow(row)
			self.comboTable.setItem(row, 0, QTableWidgetItem(metric))
		self.allCombos(True)

	def processFile(self, filename):
		self.filename=filename
		self.device_dict={}
		self.metric_dict={}
		proc=subprocess.Popen(
			"sadf -U -- -A %s | awk '{print $4,$5}'|sort |uniq"%(filename),
			shell=True, stdout=subprocess.PIPE)
		combos=proc.stdout.readlines()
		for line in combos:
			line = line.replace("\n","")
			(device, metric) = line.split(" ")
			if device not in self.device_dict:
				self.device_dict[device]=[]
				self.deviceCombo.addItem(device)
			if metric not in self.metric_dict:
				self.metric_dict[metric]=[]
			self.device_dict[device].append(metric)
			self.metric_dict[metric].append(device)
		keys=self.metric_dict.keys()
		keys.sort()
		for metric in keys:	
			self.metricCombo.addItem(metric)
		
		

	def openFile(self):
		filename=QFileDialog.getOpenFileName(self, "Select A SAR File", filter="*.sadf")
		if len(filename)>0:
			self.processFile(filename)
					


if __name__ == "__main__":
    import sys
    import signal
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QApplication(sys.argv)
    if(len(sys.argv)>1):
	    mainwin = SarView(None, sys.argv[1])
    else:
	    mainwin = SarView(None)

    mainwin.show()
    sys.exit(app.exec_())


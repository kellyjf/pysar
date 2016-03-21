
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from ui_export import *
import subprocess

class Export (QDialog, Ui_Export):

	def __init__(self, Parent=None, filename=None):
		super(QDialog,self).__init__(Parent)
		self.setupUi(self)
		self.filename = "output.png"
		self.format = "PNG"
		self.fmt = "png"
	
			
		self.connect(self.fileButton, SIGNAL("clicked()"), self.fileSelect)
		self.connect(self.formatCombo, SIGNAL("currentIndexChanged(QString)"), self.formatSelect)

	def formatSelect(self, metric):
		self.format= str(self.formatCombo.currentText())
		ofmt=self.fmt
		self.fmt=self.format.lower()
		self.fmt=self.fmt[0:3]

		if self.fmt=="pos":
			self.fmt="ps"
		ondx= self.filename.rfind(".%s"%(ofmt))
		if ondx>-1:
			self.filename="%s.%s"%(self.filename[0:ondx],self.fmt)

			self.fileLabel.setText(self.filename)
			
		
	def fileSelect(self):

		self.filename=QFileDialog.getSaveFileNameAndFilter(self, "Select Output Filename", self.filename, filter=fmt)
		self.fileLabel.setText(self.filename)


if __name__ == "__main__":
    import sys
    import signal
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QApplication(sys.argv)
    mainwin = Export(None)
    mainwin.show()
    sys.exit(app.exec_())


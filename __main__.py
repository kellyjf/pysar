

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import app_sarview


import sys
import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)
app = QApplication(sys.argv)
if(len(sys.argv)>1):
    mainwin = app_sarview.SarView(None, sys.argv[1])
else:
    mainwin = app_sarview.SarView(None)
mainwin.show()
sys.exit(app.exec_())


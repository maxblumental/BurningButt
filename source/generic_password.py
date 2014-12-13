import sys
from PyQt4 import QtGui, QtCore
import itertools
import string
import threading
import hacker
import time
from time import strftime

class PassThread(QtCore.QThread):
  def __init__(self, filename, key, length, np, event):
    QtCore.QThread.__init__(self)
    self._filename = filename
    self._key = key
    self._length = length
    self._np = np
    self._event = event

  def run(self):

    print('PassThread')

    threads = [ hacker.HackerThread(i, 0, self._np, self._event, str(self._filename), self._length, str(self._key)) for i in range(self._np) ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join(timeout=None)    

class TimeThread(QtCore.QThread):
  def __init__(self, ginfo, flag, event):
    QtCore.QThread.__init__(self)
    self._flag = flag
    self._event = event
    self._ginfo = ginfo

  def run(self):

    print('TimeThread')
    if self._flag == 0:
        self._ginfo.ptimer.start()
        self._ginfo.start.setText('Stop')
        self._flag = 1
        while True:
          if self._event.isSet():
            self._ginfo.ptimer.stop()
            self._ginfo.start.setText('Start')
            self._flag = 0
            break
    else:
        self._ginfo.ptimer.stop()
        self._ginfo.start.setText('Start')
        self._flag = 0
        self._event.set()
    
                

    

class PauseableTimer:
    def __init__(self, parent, updatefunc):
        self.old_seconds = 0    # seconds which have passed during an older run
        self.reference = 0      # the time this run of the timer has started
        self.enable = False     # we don't start right now
        self.updatefunc = updatefunc  # the function that is called to update the GUI
    def incrementer(self):
        self.updatefunc(self.formatTime(time.time() - self.reference + self.old_seconds))
        if (self.enable):
            threading.Timer(0.5, self.incrementer).start()
        else:
            self.old_seconds += (time.time() - self.reference)
    def start(self):
        self.reference = time.time()
        self.enable = True
        self.incrementer()
    def stop(self):
        self.enable = False
    def formatTime(self, seconds):
        return "{0:02d}:{1:02d}".format((int(seconds / 60)), (int(seconds % 60)))
        
class Get_info(QtGui.QWidget):
   def __init__(self, parent=None):
       QtGui.QWidget.__init__(self, parent)
       self.filename = ''
       self.key = ''
       self.len = 0 
       self.flag = 0
       self.threads = -1
       self.setGeometry(300, 300, 250, 315)
       self.setWindowTitle('Passwords Killer')
       #self.setWindowIcon(QtGui.QIcon('icons\Joc_shot_Killer.png'))
       
       self.hint = QtGui.QPushButton('Hint', self)
       self.hint.setFocusPolicy(QtCore.Qt.NoFocus)
       self.hint.move(70,100)
       self.connect(self.hint, QtCore.SIGNAL('clicked()'), self.showDialog_hint)
       
       self.num = QtGui.QPushButton('Threads', self)
       self.num.setFocusPolicy(QtCore.Qt.NoFocus)
       self.num.move(70,140)
       self.connect(self.num, QtCore.SIGNAL('clicked()'), self.showDialog_threads)
       
       self.length = QtGui.QPushButton('Length', self)
       self.length.setFocusPolicy(QtCore.Qt.NoFocus)
       self.length.move(70,60)
       self.connect(self.length, QtCore.SIGNAL('clicked()'), self.showDialog_length)
       self.center()
       
       self.open = QtGui.QPushButton('File', self)
       self.open.setFocusPolicy(QtCore.Qt.NoFocus)
       self.open.move(70,20)
       self.connect(self.open, QtCore.SIGNAL('clicked()'), self.showDialog_file)
       
       self.start = QtGui.QPushButton('Start', self)
       self.start.setFocusPolicy(QtCore.Qt.NoFocus)
       self.start.move(70,180)
       self.connect(self.start, QtCore.SIGNAL('clicked()'), self.onStart) 
       self.lcd = QtGui.QLCDNumber(self) 
       self.lcd.move(66,215)
       self.lcd.resize(100,50)
       self.lcd.display("00:00")
       
       
       self.ptimer = PauseableTimer(None, self.update_clock)
       
   def update_clock(self, time):
        self.lcd.display(time)   
   def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, 'Quit',"Are you sure to quit?", QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
   def showDialog_hint(self):
        text, ok = QtGui.QInputDialog.getText(self, 'Hint', 'Enter known part of password:')
        if ok:
            self.key = text
   def showDialog_length(self):
       text, ok = QtGui.QInputDialog.getText(self, 'Length', 'Enter lenght of password:')
       if ok and text != '':
            self.len = int(text)
   def showDialog_threads(self):
       text, ok = QtGui.QInputDialog.getText(self, 'Threads', 'Enter number of threads:')
       if ok and text != '':
            self.threads = int(text)
   def center(self):
       screen = QtGui.QDesktopWidget().screenGeometry() #screen resolution
       size = self.geometry()#widget resolution
       self.move((screen.width() - size.width())/2,(screen.height() - size.height())/2)
       
   def showDialog_file(self):
       filename = QtGui.QFileDialog.getOpenFileName(self, 'Open file','')
       self.filename  = filename
       if filename == '':
            errorMessage = QtGui.QErrorMessage(self)
            errorMessage.showMessage("Please choose file.")
   
   def onStart(self):
        
        if self.filename == '':
                QtGui.QMessageBox.information(None, 'Need some information', "Please choose file. Click button \"File\".")
                return
        if self.threads == -1:
                QtGui.QMessageBox.information(None, 'Need some information', "Please enter number of threads or by default it will be 1!")
                self.threads = 1
                return  
        event = threading.Event()
        t_thread = TimeThread(self, self.flag, event)
        t_thread.start()
        p_thread = PassThread(str(self.filename), str(self.key), self.len, self.threads, event)
        p_thread.start()
        t_thread.wait()
        p_thread.wait()
        QtGui.QMessageBox.information(None, 'Success!', "File was unlocked!!!")
app = QtGui.QApplication(sys.argv)
dop = Get_info()
dop.show()
sys.exit(app.exec_())

            #             


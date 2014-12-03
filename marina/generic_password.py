import sys
from PyQt4 import QtGui, QtCore
import itertools
import string, random
 
user_password = 'aaaaab'
   
class Get_info(QtGui.QWidget):
   def __init__(self, parent=None):
       QtGui.QWidget.__init__(self, parent)
       self.filename = ''
       self.key = ''
       self.len = 0 
       self.setGeometry(300, 300, 250, 250)
       self.setWindowTitle('Passwords Killer')
       self.setWindowIcon(QtGui.QIcon('icons\Joc_shot_Killer.png'))
       
       self.hint = QtGui.QPushButton('Hint', self)
       self.hint.setFocusPolicy(QtCore.Qt.NoFocus)
       self.hint.move(70,100)
       self.connect(self.hint, QtCore.SIGNAL('clicked()'), self.showDialog_hint)
       
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
       self.start.move(70,140)
       self.connect(self.start, QtCore.SIGNAL('clicked()'), self.onStart) 
       
             
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
            print(self.len)
   def center(self):
       screen = QtGui.QDesktopWidget().screenGeometry() #Получили разрешение нашего дисплея
       size = self.geometry()#Получили разрешение нашего виджета
       self.move((screen.width() - size.width())/2,(screen.height() - size.height())/2)
       
   def showDialog_file(self):
       filename = QtGui.QFileDialog.getOpenFileName(self, 'Open file','')
       self.filename  = filename
       if filename == '':
            errorMessage = QtGui.QErrorMessage(self)
            errorMessage.showMessage("Please choose file.")
   
   def onStart(self):
        print("self.hint = %s" % self.key)
        flag = 0
        parts = []
        if self.filename == '':
           errorMessage = QtGui.QErrorMessage(self)
           errorMessage.showMessage("Please choose file. Click button \"File\".") 
           return
        self.start.setText('Stop')
        #Generic password
        #First step of checking the pasword
        fFt = open('full_Fool_table.txt','r')
        for line in fFt:
           if line[0:-1] == user_password:
                flag = 1
                self.start.setText('Start')
                infoMessage = QtGui.QErrorMessage(self)
                infoMessage.showMessage("It is stupid password: " + line[0:-1]) 
                self.key = ''
                self.len = 0 
                return
        #Second step of checking the pasword
        password = ''
        if flag == 0:
            infoMessage = QtGui.QErrorMessage(self)
            infoMessage.showMessage("It is not standart password. Be strong and wait!!") 
        if self.key == '' and self.len == 0:
            itertable = 'abcdefjhiklmnoprqrstvxyzABCDEFGHIKLMNOPQRSTVXYZ1234567890!@#%^&*_=+()'
            for j in range (16):
                for i in itertools.combinations_with_replacement(itertable, j):
                    for k in range(j):
                        password += i[k]
                    if password == user_password:
                        flag = 1
                        self.start.setText('Start')
                        infoMessage = QtGui.QErrorMessage(self)
                        infoMessage.showMessage("It was found: " + password) 
                        self.key = ''
                        self.len = 0 
                        return 
                    password = ''
        if self.len != 0 and self.key == '':
           itertable = 'abcdefjhiklmnoprqrstvxyzABCDEFGHIKLMNOPQRSTVXYZ1234567890!@#%^&*_=+()'
           for i in itertools.combinations_with_replacement(itertable, self.len):
                    for k in range(self.len):
                        password += i[k]
                    if password == user_password:
                        flag = 1
                        self.start.setText('Start')
                        infoMessage = QtGui.QErrorMessage(self)
                        infoMessage.showMessage("It was found: " + password) 
                        self.key = ''
                        self.len = 0 
                        return 
                    password = ''
        if self.key != '' and self.len == 0:
            print("YRA")
            itertable = 'abcdefjhiklmnoprqrstvxyzABCDEFGHIKLMNOPQRSTVXYZ1234567890!@#%^&*_=+()'
            for j in range (16):
                for i in itertools.combinations_with_replacement(itertable, j):
                    for k in range(j):
                        parts.append(i[k])
                    parts.append(self.key)
                    for k in itertools.permutations(parts):
                        for m in range(j + 1):
                            password += k[m]
                        if password == user_password:
                            flag = 1
                            self.start.setText('Start')
                            infoMessage = QtGui.QErrorMessage(self)
                            infoMessage.showMessage("It was found: " + password) 
                            self.key = ''
                            self.len = 0 
                            return 
                        password = ''
                    parts = []
        if self.key != '' and self.len != 0:
            print("HOPA")
            itertable = 'abcdefjhiklmnoprqrstvxyzABCDEFGHIKLMNOPQRSTVXYZ1234567890!@#%^&*_=+()'
            for i in itertools.combinations_with_replacement(itertable, self.len):
                    for k in range(self.len):
                        parts.append(i[k])
                    parts.append(self.key)
                    for k in itertools.permutations(parts):
                        for m in range(self.len + 1):
                            password += k[m]
                        if password == user_password:
                            flag = 1
                            self.start.setText('Start')
                            infoMessage = QtGui.QErrorMessage(self)
                            infoMessage.showMessage("It was found: " + password) 
                            self.key = ''
                            self.len = 0 
                            return 
                        password = ''
                    parts = []
app = QtGui.QApplication(sys.argv)
dop = Get_info()
dop.show()
sys.exit(app.exec_())

            #             


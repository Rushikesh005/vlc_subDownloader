from PyQt4 import QtGui, QtCore
from PyQt4.phonon import Phonon
import time
import vlc_sub
import subprocess
import logging
path = ""

class SleepProgress(QtCore.QThread):
     procDone = QtCore.pyqtSignal(bool)
     partDone = QtCore.pyqtSignal(int)
     def run(self):
         logging.basicConfig("temp.txt")
         k = vlc_sub.sub_downloader(path)
         if k == True:
             #print("found")
             for a in range(1, 1+35):

                 self.partDone.emit(float(a)/35.0*100)
                # print 'sleep', a
                 time.sleep(0.25)

             self.procDone.emit(True)
         else:
#             print("no found")
             app.setStyle("mac")
             for a in range(1, 1+35):

                 self.partDone.emit(float(a)/35.0*100)
 #                print 'sleep', a
                 time.sleep(0.25)
             self.procDone.emit(True)
  #       print 'proc ended'

class Window(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('VLC_Subs')
#        self.setWindowIcon(QtGui.QIcon('\\icon\vlc.ico'))
        self.thread = SleepProgress()
        self.media = Phonon.MediaObject(self)
        self.media.stateChanged.connect(self.handleStateChanged)
        self.video = Phonon.VideoWidget(self)
        self.video.setMinimumSize(300, 300)
        self.audio = Phonon.AudioOutput(Phonon.VideoCategory, self)
        Phonon.createPath(self.media, self.audio)
        Phonon.createPath(self.media, self.video)
        if path:
            self.media.setCurrentSource(Phonon.MediaSource(path))
            self.media.play()

        layout = QtGui.QVBoxLayout(self)

        self.thread = SleepProgress()

        self.nameLabel = QtGui.QLabel("0.0%")
        self.nameLine = QtGui.QLineEdit()
        self.progressbar = QtGui.QProgressBar()
        self.progressbar.setMinimum(1)
        self.progressbar.setMaximum(100)
        layout.addWidget(self.progressbar)
        layout.addWidget(self.nameLabel)
        self.thread.partDone.connect(self.updatePBar)
        self.thread.procDone.connect(self.fin)

        layout.addWidget(self.video, 1)
        self.thread.start()

    def updatePBar(self, val):
         self.progressbar.setValue(val)
         perct = "{0}%".format(val)
         self.nameLabel.setText(perct)

    def fin(self):
        print(path)
        subprocess.Popen('vlc.exe %s'%path)
        sys.exit()


    def handleButton(self):
        pass

    def handleStateChanged(self, newstate, oldstate):
        if newstate == Phonon.ErrorState:
            source = self.media.currentSource().fileName()
            print ('ERROR: could not play:', source.toLocal8Bit().data())
            print ('  %s' % self.media.errorString().toLocal8Bit().data())


if __name__ == '__main__':

    import sys
    app = QtGui.QApplication(sys.argv)
    path = sys.argv[1]
    app.setApplicationName('vlc_sub')
    app.setStyle("cleanlooks")
    window = Window()
    window.show()
    sys.exit(app.exec_())
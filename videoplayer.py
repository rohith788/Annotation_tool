from PyQt5.QtCore import (pyqtSignal,QDir, pyqtSlot, Q_ARG, QAbstractItemModel,
        QFileInfo, qFuzzyCompare, QMetaObject, QModelIndex, QObject, Qt,
        QThread, QTime, QUrl)
from PyQt5.QtGui import QColor, qGray, QImage, QPainter, QPalette, QIcon
from PyQt5.QtMultimedia import (QAbstractVideoBuffer, QMediaContent,
        QMediaMetaData, QMediaPlayer, QMediaPlaylist, QVideoFrame, QVideoProbe)
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (QApplication, QAction, QComboBox, QDialog, QFileDialog,
        QFormLayout, QMenuBar, QHBoxLayout, QLabel, QListView, QMessageBox, QPushButton,
        QSizePolicy, QSlider, QSpinBox,  QStyle, QVBoxLayout, QWidget, QGridLayout)
import sys
import cv2

class VideoWidget(QVideoWidget):

    def __init__(self, parent=None):
        super(VideoWidget, self).__init__(parent)

        self.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)

        p = self.palette()
        p.setColor(QPalette.Window, Qt.black)
        self.setPalette(p)

        self.setAttribute(Qt.WA_OpaquePaintEvent)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape and self.isFullScreen():
            self.setFullScreen(False)
            event.accept()
        elif event.key() == Qt.Key_Enter and event.modifiers() & Qt.Key_Alt:
            self.setFullScreen(not self.isFullScreen())
            event.accept()
        else:
            super(VideoWidget, self).keyPressEvent(event)

    def mouseDoubleClickEvent(self, event):
        self.setFullScreen(not self.isFullScreen())
        event.accept()

class ShowVideo(QObject):
 
    #initiating the built in camera
    # camera_port = 0
    camera = cv2.VideoCapture("C:/Users/srohi/Downloads/test.mp4")
    VideoSignal = pyqtSignal(QImage)
 
    def __init__(self, parent = None):
        super(ShowVideo, self).__init__(parent)
        print("working")
        
    @pyqtSlot()
    def startVideo(self):
        print("running????")
        run_video = True
        while run_video:
            ret, image = self.camera.read()
 
            color_swapped_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
 
            height, width, _ = color_swapped_image.shape
 
            qt_image = QImage(color_swapped_image.data,
                                    width,
                                    height,
                                    color_swapped_image.strides[0],
                                    QImage.Format_RGB888)
 
            self.VideoSignal.emit(qt_image)

class ImageViewer(QWidget):
    def __init__(self, parent = None):
        super(ImageViewer, self).__init__(parent)
        self.image = QImage()
        self.setAttribute(Qt.WA_OpaquePaintEvent)
 
 
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawImage(0,0, self.image)
        self.image = QImage()
 
    def initUI(self):
        self.setWindowTitle('Test')
 
    @pyqtSlot(QImage)
    def setImage(self, image):
        if image.isNull():
            print("Viewer Dropped frame!")
 
        self.image = image
        # if image.size() != self.size():
        #     self.setFixedSize(image.size())
        self.update()

class Main_win(QWidget):
    fullScreenChanged = pyqtSignal(bool)
    def __init__(self, parent=None):
        super(Main_win, self).__init__(parent)
        self.resize(2000,970)
        layout  = QGridLayout()
    #------------------CV-to-media----------------#
        self.thread = QThread()
        self.thread.start()
        self.vid = ShowVideo()
        self.vid.moveToThread(self.thread)
        image_viewer = ImageViewer()      
        self.vid.VideoSignal.connect(image_viewer.setImage)
    #------------------MediaPlayer----------------#
        self.player = QMediaPlayer()
        self.videoWidget = VideoWidget()
        self.player.setVideoOutput(self.videoWidget)
        # layout.addWidget(self.videoWidget, 1, 1, 10, 7)
        self.playButton = QPushButton()
        self.playButton.setEnabled(False)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.play)
        self.player.stateChanged.connect(self.mediaStateChanged)
        layout.addWidget(self.playButton, 11,1)

        self.positionSlider = QSlider(Qt.Horizontal)
        self.positionSlider.setRange(0, 0)
        layout.addWidget(self.positionSlider, 11,2)
        self.positionSlider.sliderMoved.connect(self.setPosition)
        self.player.stateChanged.connect(self.mediaStateChanged)
        self.player.positionChanged.connect(self.positionChanged)
        self.player.durationChanged.connect(self.durationChanged)
        # print(self.player.duration())
        self.frameSlider = QSlider(Qt.Horizontal)
        self.frameSlider.setRange(0, 0)
        testbtn = QPushButton()
        layout.addWidget(testbtn, 12,1)
        testbtn.clicked.connect(self.test1)
        testbtn2 = QPushButton()
        testbtn2.setText("working")
        testbtn2.clicked.connect(self.vid.startVideo)
        layout.addWidget(image_viewer, 1,1,10,7)
        layout.addWidget(testbtn2,12, 7)
   
    #------------------Expressions----------------#
        self.Anger = QPushButton("Anger")
        layout.addWidget(self.Anger, 1, 0)
        self.Happiness = QPushButton("Happiness")
        layout.addWidget(self.Happiness, 2, 0)
        self.Suprise = QPushButton("Suprise")
        layout.addWidget(self.Suprise, 3, 0)
        self.Disgust = QPushButton("Disgust")
        layout.addWidget(self.Disgust, 4, 0)
        self.Distrust = QPushButton("Distrust")
        layout.addWidget(self.Distrust, 5, 0)
        self.Distress = QPushButton("Distress")
        layout.addWidget(self.Distress, 6, 0)
        self.Fear = QPushButton("Fear")
        layout.addWidget(self.Fear, 7, 0)
        self.Embarassment = QPushButton("Embarassment")
        layout.addWidget(self.Embarassment, 8, 0)
        self.Contempt = QPushButton("Contempt")
        layout.addWidget(self.Contempt, 9, 0)
    #-------------------------FACS---------------------------------------#
        self.lbl1 = QLabel()
        self.lbl1.setText("1")
        layout.addWidget(self.lbl1, 2, 12)
        self.lbl2 = QLabel()
        self.lbl2.setText("2")
        layout.addWidget(self.lbl2, 2, 14)
        self.lbl3 = QLabel()
        self.lbl3.setText("3")
        layout.addWidget(self.lbl3, 2, 16)
        self.lbl4 = QLabel()
        self.lbl4.setText("4")
        layout.addWidget(self.lbl4, 3, 12)
        self.lbl5 = QLabel()
        self.lbl5.setText("5")
        layout.addWidget(self.lbl5, 3, 14)
        self.lbl6 = QLabel()
        self.lbl6.setText("6")
        layout.addWidget(self.lbl6, 3, 16)
        self.lbl7 = QLabel()
        self.lbl7.setText("7")
        layout.addWidget(self.lbl7, 4, 12)
        self.lbl8 = QLabel()
        self.lbl8.setText("8")
        layout.addWidget(self.lbl8, 4, 14)
        self.lbl9 = QLabel()
        self.lbl9.setText("9")
        layout.addWidget(self.lbl9, 4, 16)
        self.lbl10 = QLabel()
        self.lbl10.setText("10")
        layout.addWidget(self.lbl10, 5, 12)
        self.lbl11 = QLabel()
        self.lbl11.setText("11")
        layout.addWidget(self.lbl11, 5, 14)
        self.lbl12 = QLabel()
        self.lbl12.setText("12")
        layout.addWidget(self.lbl12, 5, 16)
        self.lbl13 = QLabel()
        self.lbl13.setText("14")
        layout.addWidget(self.lbl13, 6, 12)
        self.lbl14 = QLabel()
        self.lbl14.setText("14")
        layout.addWidget(self.lbl14, 6, 14)
        self.lbl15 = QLabel()
        self.lbl15.setText("15")
        layout.addWidget(self.lbl15, 6, 16)
        self.lbl16 = QLabel()
        self.lbl16.setText("16")
        layout.addWidget(self.lbl16, 7, 12)
        self.lbl17 = QLabel()
        self.lbl17.setText("17")
        layout.addWidget(self.lbl17, 7, 14)
        self.lbl18 = QLabel()
        self.lbl18.setText("18")
        layout.addWidget(self.lbl18, 7, 16)
        self.lbl19 = QLabel()
        self.lbl19.setText("19")
        layout.addWidget(self.lbl19, 8, 12)
        self.lbl20 = QLabel()
        self.lbl20.setText("20")
        layout.addWidget(self.lbl20, 8, 14)
        self.lbl21 = QLabel()
        self.lbl21.setText("21")
        layout.addWidget(self.lbl21, 8, 16)
        self.lbl22 = QLabel()
        self.lbl22.setText("22")
        layout.addWidget(self.lbl22, 9, 12)
        self.lbl23 = QLabel()
        self.lbl23.setText("23")
        layout.addWidget(self.lbl23, 9, 14)
        self.lbl24 = QLabel()
        self.lbl24.setText("24")
        layout.addWidget(self.lbl24, 9, 16)
        self.lbl25 = QLabel()
        self.lbl25.setText("25")
        layout.addWidget(self.lbl25, 10, 12)
        self.lbl26 = QLabel()
        self.lbl26.setText("26")
        layout.addWidget(self.lbl26, 10, 14)
        self.lbl27 = QLabel()
        self.lbl27.setText("27")
        layout.addWidget(self.lbl27, 10, 16)
        self.lbl28 = QLabel()
        self.lbl28.setText("28")
        layout.addWidget(self.lbl28, 11, 12)
        self.lbl29 = QLabel()
        self.lbl29.setText("29")
        layout.addWidget(self.lbl29, 11, 14)
        self.lbl30 = QLabel()
        self.lbl30.setText("30")
        layout.addWidget(self.lbl30, 11, 16)
        self.lbl31 = QLabel()
        self.lbl31.setText("31")
        layout.addWidget(self.lbl31, 12, 12)
        self.lbl32 = QLabel()
        self.lbl32.setText("32")
        layout.addWidget(self.lbl32, 12, 14)
        self.lbl33 = QLabel()
        self.lbl33.setText("33")
        layout.addWidget(self.lbl33, 12, 16)
        self.lbl34 = QLabel()
        self.lbl34.setText("34")
        layout.addWidget(self.lbl34, 13, 12)
        self.lbl35 = QLabel()
        self.lbl35.setText("35")
        layout.addWidget(self.lbl35, 13, 14)
        self.lbl36 = QLabel()
        self.lbl36.setText("36")
        layout.addWidget(self.lbl36, 13, 16)
        self.lbl37 = QLabel()
        self.lbl37.setText("37")
        layout.addWidget(self.lbl37, 14, 12)
        self.lbl38 = QLabel()
        self.lbl38.setText("38")
        layout.addWidget(self.lbl38, 14, 14)
        self.lbl39 = QLabel()
        self.lbl39.setText("39")
        layout.addWidget(self.lbl39, 14,16)
        
        #---------FAC LAbels------------------#
    #-----------------------------------Menu Bar-----------------------------------------------#
        openAction = QAction(QIcon('open.png'), '&Open', self)        
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Open movie')
        openAction.triggered.connect(self.openFile)
        menuBar = QMenuBar()
        fileMenu = menuBar.addMenu('&File')
        fileMenu.addAction(openAction)
        # fileMenu.addAction(exitAction)
        layout.setMenuBar(menuBar)

    #----------------------FAC Spinners----------------#
        for i in range(39):
            j = 2
            while(j <15):
                k = 13
                while(k <= 17):
                    spin = QSpinBox()
                    spin.setAlignment(Qt.AlignCenter)
                    spin.setRange(0,5)
                    spin.resize(5,5)
                    layout.addWidget(spin, j, k)
                    k += 2
                j += 1

        Main_win.setLayout(self, layout)
#------------------videoPlayerFunctions-----------------------#
    def test1(self):
        print(self.player.duration())
    def test2(self):
        print(self.fileName)

    def openFile(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Movie",
                QDir.homePath())
        self.fileName = fileName
        if fileName != '':
            print(fileName)
            self.player.setMedia(
                    QMediaContent(QUrl.fromLocalFile(fileName)))
            self.playButton.setEnabled(True)
    def mediaStateChanged(self, state):
        if self.player.state() == QMediaPlayer.PlayingState:
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPlay))
    def play(self):
        if self.player.state() == QMediaPlayer.PlayingState:
            self.player.pause()
        else:
            self.player.play()
    def setPosition(self, position):
        # print(position)
        self.player.setPosition(position)
    def mediaStateChanged(self, state):
        if self.player.state() == QMediaPlayer.PlayingState:
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPlay))

    def positionChanged(self, position):
        self.positionSlider.setValue(position)

    def durationChanged(self, duration):
        self.positionSlider.setRange(0, duration)
    
    #------------------videoPlayerFunctions-----------------------#
if __name__ == '__main__':

    app = QApplication(sys.argv)
    player = Main_win()
    player.show()

    sys.exit(app.exec_())
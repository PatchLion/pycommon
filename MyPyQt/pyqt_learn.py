from PyQt5 import QtCore, QtWidgets, QtGui, QtNetwork
import sys
from MySqlAlchemy import *
from Projects.Spiders.meizitu.datas.tables import *
from Projects.Spiders.meizitu.datas.MeizituSession import meizituSession, allImageFromDB, allPageFromDB

class Donwloader(QtCore.QObject):
    finshed = QtCore.pyqtSignal()

    def __init__(self):
        self.__init__("")

    def __init__(self, url):
        super(Donwloader, self).__init__()
        self.url = url
        self.data = None
        self.networkManager = QtNetwork.QNetworkAccessManager()
        self.readed = True

    def setUrl(self, url):
        self.url = url

    def start(self):
        print("Download start!")
        self.readed = False
        request = QtNetwork.QNetworkRequest(QtCore.QUrl(self.url))
        self.reply = self.networkManager.get(request)
        self.reply.finished.connect(self.finish)

    def finish(self):
        print("Finished!")
        self.data = self.reply.readAll()
        self.reply = None
        self.readed = True
        self.finshed.emit()

    def isFinished(self):
        return self.readed

    def imageData(self):
        return self.data



class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.imageUrls = records(meizituSession, ImageUrls)
        self.index = 0
        #print(self.imageUrls)
        self.donwloder = Donwloader("")
        self.donwloder.finshed.connect(self.imageFinished)
        self.perButton = QtWidgets.QPushButton("上一张", self)
        self.nextButton = QtWidgets.QPushButton("下一张", self)
        self.perButton.clicked.connect(self.onPerButtonClicked)
        self.nextButton.clicked.connect(self.onNextButtonClicked)
        self.perButton.setDisabled(True)
        self.nextButton.setDisabled(len(self.imageUrls) == 0)

    def onNextButtonClicked(self, checked):
        print("下一张")
        self.nextButton.setDisabled(True)
        self.perButton.setDisabled(True)
        if self.index < (len(self.imageUrls)-1):
            self.index = self.index + 1
            self.onImageIndexChanged()


    def onPerButtonClicked(self, checked):
        print("上一张")
        self.nextButton.setDisabled(True)
        self.perButton.setDisabled(True)
        if self.index > 0:
            self.index = self.index - 1
            self.onImageIndexChanged()

    def onImageIndexChanged(self):
        if self.donwloder is not None and self.donwloder.isFinished():
            self.donwloder.setUrl(self.imageUrls[self.index].image_url)
            self.donwloder.start()

    def imageFinished(self):
        self.nextButton.setDisabled(False)
        self.perButton.setDisabled(False)
        if self.index == (len(self.imageUrls)-1):
            self.nextButton.setDisabled(True)
        if self.index == 0:
            self.perButton.setDisabled(True)
        self.update()

    def resizeEvent(self, a0: QtGui.QResizeEvent):
        self.perButton.move(QtCore.QPoint(0, self.height()/2))
        self.nextButton.move(QtCore.QPoint(self.width() - self.nextButton.width(), self.height()/2))
        self.update()

    def paintEvent(self, a0: QtGui.QPaintEvent):
        if self.donwloder.isFinished() and self.donwloder.imageData() is not None:
            image = QtGui.QImage.fromData(self.donwloder.imageData())
            if not image.isNull():
                p = QtGui.QPainter(self)
                thumbImage = image.scaled(self.size(), QtCore.Qt.KeepAspectRatio)
                rect = QtCore.QRect(self.rect().center().x() - thumbImage.width()/2.0, self.rect().center().y() - thumbImage.height()/2.0, thumbImage.width(), thumbImage.height())
                p.drawImage(rect, image)

app = QtWidgets.QApplication(sys.argv)

tree = QtWidgets.QTreeWidget()
tree.resize(450, 400)
tree.setHeaderHidden(True)
for key, value in allImageFromDB().items():
    topLevelItem = QtWidgets.QTreeWidgetItem()
    topLevelItem.setText(0, value[0])
    tree.insertTopLevelItem(tree.topLevelItemCount(), topLevelItem)
    for v in value[1:]:
        item = QtWidgets.QTreeWidgetItem(topLevelItem)
        item.setText(0, v)
    topLevelItem.setExpanded(True)


tree.show()

windows = MainWindow()
windows.show()
windows.resize(QtCore.QSize(800, 600))

sys.exit(app.exec_())
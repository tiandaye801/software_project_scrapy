# encoding:utf-8
from PyQt5.Qt import *
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import QTableWidgetItem,QTabWidget
import os
#from pipelines import MongoDBPipeline

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi()

    def setupUi(self):
        self.resize(1200, 800)
        self.setWindowTitle('MyScrapy')  # 创建一个窗口标题
        window_pale = QtGui.QPalette()
        window_pale.setColor(self.backgroundRole(), QColor(240, 248, 255))
        self.setPalette(window_pale)
        self.setWindowIcon(QIcon('../../images/logo.png'))  # 创建一个QIcon对象并接收一个我们要显示的图片路径作为参数。
        self.pix = QPixmap('../../images/logo.png')

        self.Co_Width = 500
        self.Co_Heigth = 60
        self.process = QtCore.QProcess()

#控件标签
        self.tabWidget = QTabWidget(self)
        self.tabWidget.setGeometry(QtCore.QRect(210, 400, 800, 251))
        self.tabWidget.setObjectName("tabWidget")
        self.tab_1 = QtWidgets.QWidget()
        self.tab_1.setObjectName("tab_1")
        self.tab_1.setStyleSheet("background-color: rgb(240, 248, 255)")
        self.urlin = QtWidgets.QLineEdit(self.tab_1)
        self.urlin.setGeometry(QtCore.QRect(10, 90, 481, 41))
        self.urlin.setObjectName("lineEdit")
        self.urlin.setPlaceholderText("请输入想要采集评论的百家号新闻网址。")
        self.pushButton = QtWidgets.QPushButton("开始采集",self.tab_1)
        self.pushButton.setGeometry(QtCore.QRect(520, 90, 131, 41))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.btclicked1)
        self.tabWidget.addTab(self.tab_1, "评论采集")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tab_2.setStyleSheet("background-color: rgb(240, 248, 255)")
        self.wordin = QtWidgets.QLineEdit(self.tab_2)
        self.wordin.setGeometry(QtCore.QRect(10, 90, 481, 41))
        self.wordin.setObjectName("lineEdit_2")
        self.wordin.setPlaceholderText("请输入想要采集的新闻关键词。")
        self.pushButton_2 = QtWidgets.QPushButton("开始采集",self.tab_2)
        self.pushButton_2.setGeometry(QtCore.QRect(520, 90, 131, 41))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.btclicked2)
        self.tabWidget.addTab(self.tab_2, "关键词采集")
        self.logo = QLabel(self)
        self.logo.setPixmap(self.pix)
        self.logo.setScaledContents(True)

        self.logo.resize(200,200)
        self.logo.move(int(self.width()/2-100),int(self.height()/6))

        


    def btclicked1(self):
        Url = self.urlin.text()
        with open("links.txt","w") as f:
            f.write(Url)
        os.system('scrapy crawl baijiahao')
        self.resultWindow = resultWindow()
        self.resultWindow.show()
        self.hide()

    def btclicked2(self):
        words = self.wordin.text()
        with open("words.txt","w") as f:
            f.write(words)
        os.chdir('../../../crawling_hotspots/crawling_hotspots/spiders')
        os.system('scrapy crawl hotspots')
        self.resultWindow = resultWindow()
        self.resultWindow.show()
        self.hide()

class resultWindow(QtWidgets.QWidget):
    def __init__(self):
        super(resultWindow, self).__init__()
        self.setupUi()

    def setupUi(self):
        self.resize(1200, 800)
        self.setWindowTitle('MyScrapy')  # 创建一个窗口标题
        window_pale = QtGui.QPalette()
        window_pale.setColor(self.backgroundRole(), QColor(240, 248, 255))
        self.setPalette(window_pale)
        self.setWindowIcon(QIcon('../../images/logo.png')) 


        self.analyzebt = QPushButton("生成词云", self)  # 将评论内容生成词云
        #self.analyzebt.clicked.connect(self.btclicked)

        self.Co_Width = 500
        self.Co_Heigth = 60

        #cur.execute('select * from list')
        #self.rows = cur.fetchall()
        #self.row = len(self.rows)

        #控件标签
        self.model = QTableWidget()
        self.model.setRowCount(20)
        self.model.setColumnCount(3)
        # 设置水平方向头标签文本内容
        self.model.setHorizontalHeaderLabels(['用户名', '时间', '评论'])
        self.model.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.model.setEditTriggers(QAbstractItemView.NoEditTriggers)

        QTableWidget.resizeColumnsToContents(self.model)
        QTableWidget.resizeRowsToContents(self.model)

        self.model.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        layout = QVBoxLayout()
        layout.addWidget(self.model)
        self.setLayout(layout)
    
    def resizeEvent(self, evt):  # 重新设置控件座标事件

        self.analyzebt.resize(self.width() / 2, self.height() / 10)
        self.analyzebt.move(int(self.width() / 4), int(self.height() / 5) * 4)

    #def btclicked(self):

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())

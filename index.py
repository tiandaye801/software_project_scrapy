# encoding:utf-8
from PyQt5.Qt import *
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import QTableWidgetItem,QTabWidget
import os
from pymongo import MongoClient
client = MongoClient('localhost', 27017)
mydb = client["scrapy_db"]
mycol = mydb["books"]

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
        self.setWindowIcon(QIcon('./static/images/logo.png'))  # 创建一个QIcon对象并接收一个我们要显示的图片路径作为参数。
        self.pix = QPixmap('./static/images/logo.png')

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
        self.bufferWindow = bufferWindow()
        self.bufferWindow.show()
        Url = self.urlin.text()
        with open("links.txt","w") as f:
            f.write(Url)
        client.drop_database('scrapy_db')
        os.chdir('./crawling/crawling/spiders')
        os.system('scrapy crawl baijiahao')
        os.chdir('../../../')
        self.bufferWindow.hide()
        self.resultWindow = resultWindow1()
        self.resultWindow.show()
        self.hide()

    def btclicked2(self):
        self.bufferWindow = bufferWindow()
        self.bufferWindow.show()
        words = self.wordin.text()
        with open("words.txt","w") as f:
            f.write(words)
        client.drop_database('scrapy_db')
        os.chdir('./crawling_hotspots/crawling_hotspots/spiders')
        os.system('scrapy crawl hotspots')
        os.chdir('../../../')
        self.bufferWindow.hide()
        self.resultWindow = resultWindow2()
        self.resultWindow.show()
        self.hide()

class resultWindow1(QtWidgets.QWidget):
    def __init__(self):
        super(resultWindow1, self).__init__()
        self.setupUi()

    def setupUi(self):
        self.resize(1200, 800)
        self.setWindowTitle('MyScrapy')  # 创建一个窗口标题
        window_pale = QtGui.QPalette()
        window_pale.setColor(self.backgroundRole(), QColor(240, 248, 255))
        self.setPalette(window_pale)
        self.setWindowIcon(QIcon('./static/images/logo.png')) 

        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(50, 40, 131, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self)
        self.label_2.setGeometry(QtCore.QRect(190, 50, 831, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.wordButton = QtWidgets.QPushButton(self)
        self.wordButton.setGeometry(QtCore.QRect(340, 650, 520, 50))
        self.wordButton.setObjectName("pushButton")
        self.wordButton.clicked.connect(self.btclicked)
        self.wordButton.setStyleSheet("background-color: rgb(240, 248, 255)")
        self.returnButton = QtWidgets.QPushButton(self)
        self.returnButton.setGeometry(QtCore.QRect(20, 10, 100, 30))
        self.returnButton.setObjectName("pushButton")
        self.returnButton.setStyleSheet("background-color: rgb(240, 248, 255)")
        self.returnButton.clicked.connect(self.btclicked1)

        self.array = mycol.find()
        self.num = 0
        for i in self.array:
            self.num += 1
        self.words_list = []
        self.tableWidget = QtWidgets.QTableWidget(self)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(self.num)
        self.tableWidget.setGeometry(QtCore.QRect(20, 100, 1160, 500))
        self.tableWidget.setHorizontalHeaderLabels(['用户名', '时间', '评论'])
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.topic = mycol.find({},{ "_id": 0,"topic": 1}).limit(1)
        self.name = mycol.find({},{ "_id": 0,"name": 1})
        self.time = mycol.find({},{ "_id": 0,"time": 1})
        self.comment = mycol.find({},{ "_id": 0,"comment": 1})

        
        for j in range(3):
            if j == 0:
                i = 0
                for x in self.name:
                    temp_data = x['name']  # 临时记录，不能直接插入表格
                    data = QTableWidgetItem(str(temp_data))  # 转换后可插入表格
                    self.tableWidget.setItem(i, j, data)
                    i += 1
            elif j == 1 :
                i = 0
                for x in self.time:
                    temp_data = x['time']  # 临时记录，不能直接插入表格
                    data = QTableWidgetItem(str(temp_data))  # 转换后可插入表格
                    self.tableWidget.setItem(i, j, data)
                    i += 1
            elif j == 2 :
                i = 0
                for x in self.comment:
                    temp_data = x['comment']  # 临时记录，不能直接插入表格
                    data = QTableWidgetItem(str(temp_data))  # 转换后可插入表格
                    self.tableWidget.setItem(i, j, data)
                    i += 1

    def resizeEvent(self, evt):  # 重新设置控件座标事件

        self.label.setText("新闻标题：")
        for x in self.topic:
            self.label_2.setText(str(x['topic']))
        self.wordButton.setText("将评论生成词云")
        self.returnButton.setText("↩️返回")

    def btclicked(self):
        os.system('python getfrequency.py')

    def btclicked1(self):
        self.MainWindow = MainWindow()
        self.MainWindow.show()
        self.hide()

class resultWindow2(QtWidgets.QWidget):
    def __init__(self):
        super(resultWindow2, self).__init__()
        self.setupUi()

    def setupUi(self):
        self.resize(1200, 800)
        self.setWindowTitle('MyScrapy')  # 创建一个窗口标题
        window_pale = QtGui.QPalette()
        window_pale.setColor(self.backgroundRole(), QColor(240, 248, 255))
        self.setPalette(window_pale)
        self.setWindowIcon(QIcon('./static/images/logo.png')) 

        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(50, 40, 131, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self)
        self.label_2.setGeometry(QtCore.QRect(190, 50, 831, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")

        self.returnButton = QtWidgets.QPushButton(self)
        self.returnButton.setGeometry(QtCore.QRect(20, 10, 100, 30))
        self.returnButton.setObjectName("pushButton")
        self.returnButton.setStyleSheet("background-color: rgb(240, 248, 255)")
        self.returnButton.clicked.connect(self.btclicked1)

        self.array = mycol.find()
        self.num = 0
        for i in self.array:
            self.num += 1
        self.words_list = []
        self.tableWidget = QtWidgets.QTableWidget(self)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(self.num)
        self.tableWidget.setGeometry(QtCore.QRect(20, 100, 1160, 650))
        self.tableWidget.setHorizontalHeaderLabels(['标题', '网址'])
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.topic = mycol.find({},{ "_id": 0,"topic": 1})
        self.address = mycol.find({},{ "_id": 0,"address": 1})
        
        for j in range(2):
            if j == 0:
                i = 0
                for x in self.topic:
                    temp_data = x['topic']  # 临时记录，不能直接插入表格
                    data = QTableWidgetItem(str(temp_data))  # 转换后可插入表格
                    self.tableWidget.setItem(i, j, data)
                    i += 1
            elif j == 1 :
                i = 0
                for x in self.address:
                    temp_data = x['address']  # 临时记录，不能直接插入表格
                    data = QTableWidgetItem(str(temp_data))  # 转换后可插入表格
                    self.tableWidget.setItem(i, j, data)
                    i += 1

    def resizeEvent(self, evt):  # 重新设置控件座标事件

        self.label.setText("关键词：")
        f = open('./words.txt', 'r')
        content = f.read()
        f.close()
        self.label_2.setText(content)
        self.returnButton.setText("↩️返回")

    def btclicked1(self):
        #os.chdir()
        self.MainWindow = MainWindow()
        self.MainWindow.show()
        self.hide()

class bufferWindow(QtWidgets.QWidget):
    def __init__(self):
        super(bufferWindow, self).__init__()
        self.setupUi()

    def setupUi(self):
        self.resize(450, 240)
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(90, 20, 411, 171))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName("label")

        self.setWindowTitle('MyScrapy')  # 创建一个窗口标题
        window_pale = QtGui.QPalette()
        window_pale.setColor(self.backgroundRole(), QColor(240, 248, 255))
        self.setPalette(window_pale)
        self.setWindowIcon(QIcon('./static/images/logo.png')) 
        self.label.setText("正在采集中，请耐心等待...")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())

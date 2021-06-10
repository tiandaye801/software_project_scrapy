# encoding:utf-8
from PyQt5.Qt import *
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import QTableWidgetItem,QTabWidget
import os
import cv2
import numpy as np
from pymongo import MongoClient
client = MongoClient('localhost', 27017)
mydb = client["scrapy_db"]
mycol = mydb["books"]



class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi()

    def setupUi(self):
        with open('./static/qss/result1.qss', 'r') as f:
            qss = f.read()
        self.setStyleSheet(qss)
        self.resize(1200, 800)
        self.setWindowTitle('MyScrapy')  # 创建一个窗口标题
        window_pale = QtGui.QPalette()
        window_pale.setColor(self.backgroundRole(), QColor(255, 255, 255))
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
        #self.tab_1.setStyleSheet("background-color: white")
        self.urlin = QtWidgets.QLineEdit(self.tab_1)
        self.urlin.setGeometry(QtCore.QRect(10, 90, 550, 41))
        self.urlin.setObjectName("lineEdit")
        self.urlin.setPlaceholderText("请输入想要采集评论的百家号新闻网址。")
        self.numin = QtWidgets.QLineEdit(self.tab_1)
        self.numin.setGeometry(QtCore.QRect(565, 90, 181, 41))
        self.numin.setObjectName("lineEdit_1")
        self.numin.setPlaceholderText("采集评论数")

        self.pushButton = QtWidgets.QPushButton("开始采集",self.tab_1)
        self.pushButton.setGeometry(QtCore.QRect(680, 90, 101, 41))
        self.pushButton.setObjectName("pushButton1")
        self.pushButton.clicked.connect(self.btclicked1)
        self.tabWidget.addTab(self.tab_1, "评论采集")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        #self.tab_2.setStyleSheet("background-color: rgb(240, 248, 255)")
        self.wordin = QtWidgets.QLineEdit(self.tab_2)
        self.wordin.setGeometry(QtCore.QRect(10, 90, 550, 41))
        self.wordin.setObjectName("lineEdit_2")
        self.wordin.setPlaceholderText("请输入想要采集的新闻关键词。")
        self.pagein = QtWidgets.QLineEdit(self.tab_2)
        self.pagein.setGeometry(QtCore.QRect(565, 90, 181, 41))
        self.pagein.setObjectName("lineEdit_3")
        self.pagein.setPlaceholderText("采集页数")
        self.pushButton_2 = QtWidgets.QPushButton("开始采集",self.tab_2)
        self.pushButton_2.setGeometry(QtCore.QRect(680, 90, 101, 41))
        self.pushButton_2.setObjectName("pushButton1")
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
        num = self.numin.text()
        with open("num.txt","w") as f:
            f.write(num)
        client.drop_database('scrapy_db')
        os.chdir('./crawling/crawling/spiders')
        os.system('scrapy crawl baijiahao')
        os.chdir('../../../')
        self.resultWindow = resultWindow1()
        self.resultWindow.show()
        self.hide()

    def btclicked2(self):
        words = self.wordin.text()
        with open("words.txt","w") as f:
            f.write(words)
        page = self.pagein.text()
        with open("page.txt","w") as f:
            f.write(page)
        client.drop_database('scrapy_db')
        os.chdir('./crawling_hotspots/crawling_hotspots/spiders')
        os.system('scrapy crawl hotspots')
        os.chdir('../../../')
        self.resultWindow = resultWindow2()
        self.resultWindow.show()
        self.hide()

class resultWindow1(QtWidgets.QWidget):
    def __init__(self):
        super(resultWindow1, self).__init__()
        self.setupUi()


    def setupUi(self):
        with open('./static/qss/result1.qss', 'r') as f:
            qss = f.read()
        self.setStyleSheet(qss)
        self.resize(1200, 800)
        self.setWindowTitle('MyScrapy')  # 创建一个窗口标题
        window_pale = QtGui.QPalette()
        window_pale.setColor(self.backgroundRole(), QColor(255, 255, 255))
        self.setPalette(window_pale)
        self.setWindowIcon(QIcon('./static/images/logo.png')) 

        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(50, 40, 131, 80))
        # font = QtGui.QFont()
        # font.setPointSize(14)
        # self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self)
        self.label_2.setGeometry(QtCore.QRect(190, 40, 831, 80))
        # font = QtGui.QFont()
        # font.setPointSize(14)
        # self.label_2.setFont(font)
        self.label_2.setObjectName("label2")
        self.wordButton = QtWidgets.QPushButton(self)
        self.wordButton.setGeometry(QtCore.QRect(500, 650, 520, 130))
        self.wordButton.setObjectName("pushButton3")
        self.wordButton.clicked.connect(self.btclicked)
        self.wordButton.setStyleSheet("background-image:url(./static/images/cloud.png) ")
        self.returnButton = QtWidgets.QPushButton(self)
        self.returnButton.setGeometry(QtCore.QRect(20, 10, 50, 30))
        self.returnButton.setObjectName("pushButton3")
        self.returnButton.setStyleSheet("background-image:url(./static/images/arrow-left.png) ;")
        self.returnButton.clicked.connect(self.btclicked1)
        self.imgButton = QtWidgets.QPushButton(self)
        self.imgButton.setGeometry(QtCore.QRect(90, 10, 150, 30))
        self.imgButton.setObjectName("pushButton3")
        self.imgButton.setStyleSheet("background-image:url(./static/images/changeimage.png) ;")
        self.imgButton.clicked.connect(self.btclicked2)

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
                    temp = str(temp_data).strip('[\'')
                    temp = temp.strip(']\'')
                    data = QTableWidgetItem(temp)  # 转换后可插入表格
                    self.tableWidget.setItem(i, j, data)
                    i += 1
            elif j == 1 :
                i = 0
                for x in self.time:
                    temp_data = x['time']  # 临时记录，不能直接插入表格
                    temp = str(temp_data).strip('[\'')
                    temp = temp.strip(']\'')
                    data = QTableWidgetItem(temp)  # 转换后可插入表格
                    self.tableWidget.setItem(i, j, data)
                    i += 1
            elif j == 2 :
                i = 0
                for x in self.comment:
                    temp_data = x['comment']  # 临时记录，不能直接插入表格
                    temp = str(temp_data).strip('[\'')
                    temp = temp.strip(']\'')
                    data = QTableWidgetItem(temp)  # 转换后可插入表格
                    self.tableWidget.setItem(i, j, data)
                    i += 1


    def resizeEvent(self, evt):  # 重新设置控件座标事件

        self.label.setText("新闻标题：")
        for x in self.topic:
            temp_data = x['topic']
            temp = str(temp_data).strip('[\'')
            temp = temp.strip(']\'')
            self.label_2.setText(temp)

    def btclicked(self):
        os.system('python getfrequency.py')

    def btclicked1(self):
        self.MainWindow = MainWindow()
        self.MainWindow.show()
        self.hide()

    def btclicked2(self):
        imgName, imgType = QFileDialog.getOpenFileName(self, "打开图片", "","*.jpg;;*.png;;All Files(*)")
        img = cv2.imread(imgName)
        os.remove("static/images/bg_1.png")
        cv2.imwrite("static/images/bg_1.png",img)


class resultWindow2(QtWidgets.QWidget):
    def __init__(self):
        super(resultWindow2, self).__init__()
        self.setupUi()

    def setupUi(self):
        with open('./static/qss/result1.qss', 'r') as f:
            qss = f.read()
        self.setStyleSheet(qss)
        self.resize(1200, 800)
        self.setWindowTitle('MyScrapy')  # 创建一个窗口标题
        window_pale = QtGui.QPalette()
        window_pale.setColor(self.backgroundRole(), QColor(255, 255, 255))
        self.setPalette(window_pale)
        self.setWindowIcon(QIcon('./static/images/logo.png')) 

        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(50, 40, 131, 80))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self)
        self.label_2.setGeometry(QtCore.QRect(190, 40, 831, 80))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label2")

        self.returnButton = QtWidgets.QPushButton(self)
        self.returnButton.setGeometry(QtCore.QRect(20, 10, 50, 30))
        self.returnButton.setObjectName("pushButton3")
        self.returnButton.setStyleSheet("background-image:url(./static/images/arrow-left.png)")
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
                    temp = str(temp_data).strip('[\'')
                    temp = temp.strip(']\'')
                    data = QTableWidgetItem(temp)  # 转换后可插入表格
                    self.tableWidget.setItem(i, j, data)
                    i += 1
            elif j == 1 :
                i = 0
                for x in self.address:
                    temp_data = x['address']  # 临时记录，不能直接插入表格
                    temp = str(temp_data).strip('[\'')
                    temp = temp.strip(']\'')
                    data = QTableWidgetItem(temp)  # 转换后可插入表格
                    self.tableWidget.setItem(i, j, data)
                    i += 1


    def resizeEvent(self, evt):  # 重新设置控件座标事件

        self.label.setText("关键词：")
        f = open('./words.txt', 'r')
        content = f.read()
        f.close()
        self.label_2.setText(content)

    def btclicked1(self):
        self.MainWindow = MainWindow()
        self.MainWindow.show()
        self.hide()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())

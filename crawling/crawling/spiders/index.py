from PyQt5.Qt import *
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import QTableWidgetItem
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
        window_pale.setColor(self.backgroundRole(), QColor(237, 237, 237))
        self.setPalette(window_pale)
        self.setWindowIcon(QIcon('../../images/icon.png'))  # 创建一个QIcon对象并接收一个我们要显示的图片路径作为参数。
        self.pix = QPixmap('../../images/logo.png')

        self.Co_Width = 500
        self.Co_Heigth = 60
        self.process = QtCore.QProcess()
#控件标签

        self.urlin = QLineEdit(self)
        self.urlin.setPlaceholderText("请输入想要采集的百家号新闻网址。")
        self.button = QPushButton("开始采集", self)  # 添加
        self.button.clicked.connect(self.btclicked)
        self.logo = QLabel(self)
        #self.logo.setGeometry(0,0,300,200)
        self.logo.setPixmap(self.pix)
        self.logo.setScaledContents(True)


    def btclicked(self):
        Url = self.urlin.text()
        with open("links.txt","w") as f:
            f.write(Url)
        os.system('scrapy crawl baijiahao')
        self.resultWindow = resultWindow()
        self.resultWindow.show()
        self.hide()

    def resizeEvent(self, evt):  # 重新设置控件座标事件
        self.urlin.resize(self.Co_Width, self.Co_Heigth)
        self.urlin.move(int(self.width() / 4), int(self.height() / 2))
        self.button.resize(200, self.Co_Heigth)
        self.button.move(int(self.urlin.x()+self.urlin.width()), int(self.urlin.y()))
        self.logo.resize(200,200)
        self.logo.move(int(self.width()/2-100),int(self.height()/6))

class resultWindow(QtWidgets.QWidget):
    def __init__(self):
        super(resultWindow, self).__init__()
        self.setupUi()

    def setupUi(self):
        self.resize(1200, 800)
        self.setWindowTitle('MyScrapy')  # 创建一个窗口标题
        window_pale = QtGui.QPalette()
        window_pale.setColor(self.backgroundRole(), QColor(237, 237, 237))
        self.setPalette(window_pale)
        self.setWindowIcon(QIcon('../../images/icon.png')) 


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
        '''
        for i in range(20):
            for j in range(3):
                if j == 0 :
                    temp_data = self.rows[i][j+1]  # 临时记录，不能直接插入表格
                    data = QTableWidgetItem(str(temp_data))  # 转换后可插入表格
                    self.model.setItem(i, j, data)
                elif j == 1:
                    year_data = self.rows[i][2]
                    month_data = self.rows[i][3]
                    day_data = self.rows[i][4]
                    data = QTableWidgetItem(str(year_data)+"年"+str(month_data)+"月"+str(day_data)+"日")
                    self.model.setItem(i, j, data)
                else :
                    end = QDateTime(self.rows[i][2], self.rows[i][3], self.rows[i][4], 00, 00, 00)  # 截至时间
                    now = QDateTime.currentDateTime()  # 当前日期
                    m_time = QTime()
                    m_time.setHMS(0, 0, 0, 0)
                    day = now.daysTo(end)
                    time = m_time.addSecs(now.secsTo(end)).toString("hh时mm分ss秒")
                    data = QTableWidgetItem("还剩" + str(day-1) + "天" + time)
                    self.model.setItem(i, j, data)
        '''
    def resizeEvent(self, evt):  # 重新设置控件座标事件

        self.analyzebt.resize(self.width() / 2, self.height() / 10)
        self.analyzebt.move(int(self.width() / 4), int(self.height() / 5) * 4)

    #def btclicked(self):

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())

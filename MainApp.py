from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtChart import QChart, QChartView, QPieSeries, QPieSlice, QLegend
from PyQt5.QtGui import QFont, QIcon, QPalette, QColor, QPainter
from PyQt5.QtCore import Qt, QTranslator, QLocale, QLibraryInfo, pyqtSlot
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QGridLayout, QVBoxLayout, QLabel, QComboBox, QSizePolicy, QCheckBox)
import pickle
import datetime
from datetime import datetime
from enterDataexec import Ui_Dialog



class Ui_MainWindow3(object):
    def openwindow(self):
        self.window2 = QtWidgets.QDialog()
        self.ui2 = Ui_Dialog()
        self.ui2.setupUi(self.window2)
        self.window2.show()
    
    


    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(520, 960)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.TOTAL = QtWidgets.QGraphicsView(self.centralwidget)
        self.TOTAL.setGeometry(QtCore.QRect(20, 700, 480, 125))
        self.TOTAL.setObjectName("TOTAL")
        self.revenue = QtWidgets.QGraphicsView(self.centralwidget)
        self.revenue.setGeometry(QtCore.QRect(20, 140, 480, 540))
        self.revenue.setObjectName("revenue")
        self.Header = QtWidgets.QGraphicsView(self.centralwidget)
        self.Header.setGeometry(QtCore.QRect(0, 0, 520, 61))
        self.Header.setObjectName("Header")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 150, 490, 51))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(0, 10, 520, 41))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.dateView = QtWidgets.QGraphicsView(self.centralwidget)
        self.dateView.setGeometry(QtCore.QRect(20, 80, 255, 50))
        self.dateView.setObjectName("dateView")
        self.Month = QtWidgets.QLabel(self.centralwidget)
        self.Month.setGeometry(QtCore.QRect(40, 80, 110, 50))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.Month.setFont(font)
        self.Month.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.Month.setObjectName("Month")
        month = datetime.now().strftime("%B")
        year = datetime.now().year
        self.Month.setText(str(month))
        self.Slash = QtWidgets.QLabel(self.centralwidget)
        self.Slash.setGeometry(QtCore.QRect(150, 80, 50, 50))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.Slash.setFont(font)
        self.Slash.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.Slash.setObjectName("Slash")
        self.Year = QtWidgets.QLabel(self.centralwidget)
        self.Year.setGeometry(QtCore.QRect(200, 80, 120, 50))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.Year.setFont(font)
        self.Year.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.Year.setObjectName("Year")
        self.Year.setText(str(year))
        self.costsText = QtWidgets.QLabel(self.centralwidget)
        self.costsText.setGeometry(QtCore.QRect(810, 410, 231, 265))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.costsText.setFont(font)
        self.costsText.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.costsText.setText("")
        self.costsText.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.costsText.setObjectName("costsText")
        self.totalText = QtWidgets.QLabel(self.centralwidget)
        self.totalText.setGeometry(QtCore.QRect(390, 350, 231, 31))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.totalText.setFont(font)
        self.totalText.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.totalText.setText("")
        self.totalText.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.totalText.setObjectName("totalText")
        self.enterData = QtWidgets.QPushButton(self.centralwidget, clicked = lambda: self.openwindow())
        self.enterData.setGeometry(QtCore.QRect(20,850, 200, 60))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.enterData.setFont(font)

        

        #Calculations
        print("hello")
        file = open('data.txt','r')
        content = file.read()
        splittedContent = content.split(",")
        print(splittedContent)
        len(splittedContent)
        
        nMonths = 12


        sal = splittedContent[len(splittedContent)-1].split("/")
        print(sal)
        monthP = 0
        if sal[1] == "year":
            monthP = int(sal[0]) / nMonths
            print(monthP)
        elif sal[1] == "month":
            monthP = int(sal[0])
            print(monthP)

        with open('array_data.pkl', 'rb') as f:
            cost_array = pickle.load(f)

        print("Loaded array in other script:")
        print(cost_array)

        print(cost_array[0][1])    
        names = [item[0] for item in cost_array]  # First elements (labels)
        values = [item[1] for item in cost_array]  # Second elements (values)

        print(names)
        print(values)
        self.label4 = QtWidgets.QLabel(self.centralwidget)
        self.label4.setGeometry(QtCore.QRect(30, 185, 490, 51))  # Starting position
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label4.setFont(font)
        self.label4.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label4.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.label4.setObjectName("label4")

        self.label5 = QtWidgets.QLabel(self.centralwidget)
        self.label5.setGeometry(QtCore.QRect(30, 220, 490, 51))  # Changed y position to 220 (185 + 35)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label5.setFont(font)
        self.label5.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label5.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.label5.setObjectName("label5")

        self.label6 = QtWidgets.QLabel(self.centralwidget)
        self.label6.setGeometry(QtCore.QRect(30, 255, 490, 51))  # Changed y position to 255 (220 + 35)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label6.setFont(font)
        self.label6.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label6.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.label6.setObjectName("label6")

        self.label7 = QtWidgets.QLabel(self.centralwidget)
        self.label7.setGeometry(QtCore.QRect(30, 290, 490, 51))  # Changed y position to 290 (255 + 35)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label7.setFont(font)
        self.label7.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label7.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.label7.setObjectName("label7")

        self.label8 = QtWidgets.QLabel(self.centralwidget)
        self.label8.setGeometry(QtCore.QRect(30, 325, 490, 51))  # Changed y position to 325 (290 + 35)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label8.setFont(font)
        self.label8.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label8.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.label8.setObjectName("label8")

        self.label9 = QtWidgets.QLabel(self.centralwidget)
        self.label9.setGeometry(QtCore.QRect(30, 360, 490, 51))  # Changed y position to 360 (325 + 35)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label9.setFont(font)
        self.label9.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label9.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.label9.setObjectName("label9")
        self.label10 = QtWidgets.QLabel(self.centralwidget)
        self.label10.setGeometry(QtCore.QRect(30, 710, 490, 51))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label10.setFont(font)
        self.label10.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label10.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label10.setObjectName("label10")
        totalcosts = values[0] + values [1] + values [2] + values [3] + values [4] + values [5] + values [6] + values [7] + values [8] + values [9] + values [10] + values [11] + values [12] + values[13]

        self.label11 = QtWidgets.QLabel(self.centralwidget)
        self.label11.setGeometry(QtCore.QRect(30, 395, 490, 51))  # Adjusted position (360 + 35)
        self.label11.setFont(font)
        font.setPointSize(12)
        self.label11.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label11.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.label11.setObjectName("label11")

        self.label12 = QtWidgets.QLabel(self.centralwidget)
        self.label12.setGeometry(QtCore.QRect(30, 430, 490, 51))  # Adjusted position (395 + 35)
        self.label12.setFont(font)
        font.setPointSize(12)
        self.label12.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label12.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.label12.setObjectName("label12")

        self.label13 = QtWidgets.QLabel(self.centralwidget)
        self.label13.setGeometry(QtCore.QRect(30, 465, 490, 51))  # Adjusted position (430 + 35)
        self.label13.setFont(font)
        font.setPointSize(12)
        self.label13.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label13.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.label13.setObjectName("label13")

        self.label14 = QtWidgets.QLabel(self.centralwidget)
        self.label14.setGeometry(QtCore.QRect(30, 500, 490, 51))  # Adjusted position (465 + 35)
        self.label14.setFont(font)
        font.setPointSize(12)
        self.label14.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label14.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.label14.setObjectName("label14")

        self.label15 = QtWidgets.QLabel(self.centralwidget)
        self.label15.setGeometry(QtCore.QRect(30, 535, 490, 51))  # Adjusted position (500 + 35)
        self.label15.setFont(font)
        font.setPointSize(12)
        self.label15.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label15.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.label15.setObjectName("label15")

        self.label16 = QtWidgets.QLabel(self.centralwidget)
        self.label16.setGeometry(QtCore.QRect(30, 570, 490, 51))  # Adjusted position (535 + 35)
        self.label16.setFont(font)
        font.setPointSize(12)
        self.label16.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label16.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.label16.setObjectName("label16")

        self.label17 = QtWidgets.QLabel(self.centralwidget)
        self.label17.setGeometry(QtCore.QRect(30, 605, 490, 51))  # Adjusted position (570 + 35)
        self.label17.setFont(font)
        font.setPointSize(12)

        self.label17.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label17.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.label17.setObjectName("label17")

        # Total costs calculation
        totalcosts = sum(values)  # Calculate total costs for all values

        # Set labels with costs and their percentages
        self.label10.setText("Total Costs = " + "$" + str(totalcosts))
        self.label.setText("Housing Costs = " + "$" + str(values[0]) + " (" + str(round((values[0] / totalcosts) * 100, 2)) + "%)")
        self.label4.setText("Transportation Costs = " + "$" + str(values[1]) + " (" + str(round((values[1] / totalcosts) * 100, 2)) + "%)")
        self.label5.setText("Groceries Costs = " + "$" + str(values[2]) + " (" + str(round((values[2] / totalcosts) * 100, 2)) + "%)")
        self.label6.setText("Healthcare Costs = " + "$" + str(values[3]) + " (" + str(round((values[3] / totalcosts) * 100, 2)) + "%)")
        self.label7.setText("Utilities Costs = " + "$" + str(values[4]) + " (" + str(round((values[4] / totalcosts) * 100, 2)) + "%)")
        self.label8.setText("Insurance Costs = " + "$" + str(values[5]) + " (" + str(round((values[5] / totalcosts) * 100, 2)) + "%)")
        self.label9.setText("Personal Care Costs = " + "$" + str(values[6]) + " (" + str(round((values[6] / totalcosts) * 100, 2)) + "%)")
        self.label11.setText("Entertainment Costs = " + "$" + str(values[7]) + " (" + str(round((values[7] / totalcosts) * 100, 2)) + "%)")
        self.label12.setText("Savings Costs = " + "$" + str(values[8]) + " (" + str(round((values[8] / totalcosts) * 100, 2)) + "%)")
        self.label13.setText("Clothing Costs = " + "$" + str(values[9]) + " (" + str(round((values[9] / totalcosts) * 100, 2)) + "%)")
        self.label14.setText("Education Costs = " + "$" + str(values[10]) + " (" + str(round((values[10] / totalcosts) * 100, 2)) + "%)")
        self.label15.setText("Childcare Costs = " + "$" + str(values[11]) + " (" + str(round((values[11] / totalcosts) * 100, 2)) + "%)")
        self.label16.setText("Taxes Costs = " + "$" + str(values[12]) + " (" + str(round((values[12] / totalcosts) * 100, 2)) + "%)")
        self.label17.setText("Travel Costs = " + "$" + str(values[13]) + " (" + str(round((values[13] / totalcosts) * 100, 2)) + "%)")
        
         


        """def salaryMonthly():
            print("hello")
            file = open('data.txt','r')
            content = file.read()
            x = content.split(",")
            print(x)
            sal = x[4].split("/")
            print(sal)"""

        
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 640, 18))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "EasyFlow"))
        self.label_2.setText(_translate("MainWindow", "Monthly Estimate"))
        
        self.Slash.setText(_translate("MainWindow", "/"))
        
        self.enterData.setText(_translate("MainWindow", "Enter Cost Data"))



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow3()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

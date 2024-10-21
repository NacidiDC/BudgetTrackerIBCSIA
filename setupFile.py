from PyQt5 import QtCore, QtGui, QtWidgets
import csv
from MainApp import Ui_MainWindow3
import time

class Ui_MainWindow2(object):

    def __init__(self):
        self.CancelPushed1 = False  
        self.FinishPushed1 = False
        choice1 = ""

    def openMainApp(self):
        self.window3 = QtWidgets.QMainWindow()
        self.ui3 = Ui_MainWindow3()
        self.ui3.setupUi(self.window3)
        self.window3.show()
 
    def setupUi(self, MainWindow):
        
        

        MainWindow.setObjectName("SetupWindow")
        MainWindow.resize(1080, 720)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(0, 0, 1081, 81))
        self.graphicsView.setObjectName("graphicsView")
        self.Page1Button = QtWidgets.QPushButton(self.centralwidget)
        self.Page1Button.setGeometry(QtCore.QRect(10, 640, 150, 71))
        font = QtGui.QFont()
        font.setFamily("White Rabbit")
        font.setPointSize(13)
        self.Page1Button.setFont(font)
        self.Page1Button.setObjectName("Page1Button")
        self.graphicsView_2 = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView_2.setGeometry(QtCore.QRect(0, 630, 1091, 91))
        self.graphicsView_2.setObjectName("graphicsView_2")
        self.Page3Button = QtWidgets.QPushButton(self.centralwidget)
        self.Page3Button.setGeometry(QtCore.QRect(330, 640, 150, 71))
        font = QtGui.QFont()
        font.setFamily("White Rabbit")
        font.setPointSize(13)
        self.Page3Button.setFont(font)
        self.Page3Button.setObjectName("Page3Button")
        self.Page2Button = QtWidgets.QPushButton(self.centralwidget)
        self.Page2Button.setGeometry(QtCore.QRect(170, 640, 150, 71))
        font = QtGui.QFont()
        font.setFamily("White Rabbit")
        font.setPointSize(13)
        self.Page2Button.setFont(font)
        self.Page2Button.setObjectName("Page2Button")
        font = QtGui.QFont()
        font.setFamily("White Rabbit")
        font.setPointSize(13)
        font = QtGui.QFont()
        font.setFamily("White Rabbit")
        font.setPointSize(13)
        self.FinishButton = QtWidgets.QPushButton(self.centralwidget)
        self.FinishButton.setGeometry(QtCore.QRect(490, 640, 301, 71))




        font = QtGui.QFont()
        font.setFamily("White Rabbit")
        font.setPointSize(13)
        self.FinishButton.setFont(font)
        self.FinishButton.setObjectName("FinishButton")
        self.CancelButton = QtWidgets.QPushButton(self.centralwidget)
        self.CancelButton.setGeometry(QtCore.QRect(820, 640, 231, 71))
        font = QtGui.QFont()
        font.setFamily("White Rabbit")
        font.setPointSize(13)
        self.CancelButton.setFont(font)
        self.CancelButton.setObjectName("CancelButton")
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setGeometry(QtCore.QRect(0, 80, 1081, 551))

        def cancelSetupS1():
            if not self.CancelPushed1:  # Check if self.pushed1 is False
                self.CancelButton.setText(QtCore.QCoreApplication.translate("MainWindow", "Confirm?"))
                self.CancelPushed1 = True  # Set self.pushed1 to True after the first press
            else:  # If self.pushed1 is True
                quit()  # Quit the application
               
        self.CancelButton.clicked.connect(cancelSetupS1)        


        self.stackedWidget.setObjectName("stackedWidget")
        self.page_1 = QtWidgets.QWidget()
        self.page_1.setObjectName("page_1")
        self.Question = QtWidgets.QLabel(self.page_1)
        self.Question.setGeometry(QtCore.QRect(110, 10, 801, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.Question.setFont(font)
        self.Question.setObjectName("Question")
        self.Personal = QtWidgets.QRadioButton(self.page_1)
        self.Personal.setGeometry(QtCore.QRect(130, 70, 171, 51))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Personal.setFont(font)
        self.Personal.setObjectName("Personal")
        self.Question_2 = QtWidgets.QLabel(self.page_1)
        self.Question_2.setGeometry(QtCore.QRect(20, 490, 1011, 31))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.Question_2.setFont(font)
        self.Question_2.setObjectName("Question_2")
        self.Question_3 = QtWidgets.QLabel(self.page_1)
        self.Question_3.setGeometry(QtCore.QRect(110, 40, 1011, 31))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.Question_3.setFont(font)
        self.Question_3.setObjectName("Question_3")
        self.graphicsView_3 = QtWidgets.QGraphicsView(self.page_1)
        self.graphicsView_3.setGeometry(QtCore.QRect(20, 10, 71, 61))
        self.graphicsView_3.setObjectName("graphicsView_3")
        self.label_2 = QtWidgets.QLabel(self.page_1)
        self.label_2.setGeometry(QtCore.QRect(20, 9, 71, 61))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.Family = QtWidgets.QRadioButton(self.page_1)
        self.Family.setGeometry(QtCore.QRect(410, 70, 171, 51))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Family.setFont(font)
        self.Family.setObjectName("Family")
        self.stackedWidget.addWidget(self.page_1)

        self.buttonGroup = QtWidgets.QButtonGroup(MainWindow)
        self.buttonGroup.addButton(self.Family)
        self.buttonGroup.addButton(self.Personal)
        def record_choice(self):
        # Determine which radio button is checked and write to file
            choice1 = None
            if self.Personal.isChecked():
                choice1 = "Personal"
                print("personal")
            elif self.Family.isChecked():
                choice1 = "Family"
                print("family")
        
            if choice1:
                with open('data.txt', 'a') as file:  # Use 'a' for appending
                    file.write(choice1)
                    


        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.Check_PersCare = QtWidgets.QCheckBox(self.page_2)
        self.Check_PersCare.setGeometry(QtCore.QRect(130, 251, 241, 51))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Check_PersCare.setFont(font)
        self.Check_PersCare.setTristate(False)
        self.Check_PersCare.setObjectName("Check_PersCare")
        self.Question_5 = QtWidgets.QLabel(self.page_2)
        self.Question_5.setGeometry(QtCore.QRect(20, 491, 1011, 31))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.Question_5.setFont(font)
        self.Question_5.setObjectName("Question_5")
        self.Check_Transport = QtWidgets.QCheckBox(self.page_2)
        self.Check_Transport.setGeometry(QtCore.QRect(130, 101, 241, 51))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Check_Transport.setFont(font)
        self.Check_Transport.setTristate(False)
        self.Check_Transport.setObjectName("Check_Transport")
        self.Check_Entertainment = QtWidgets.QCheckBox(self.page_2)
        self.Check_Entertainment.setGeometry(QtCore.QRect(410, 71, 241, 51))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Check_Entertainment.setFont(font)
        self.Check_Entertainment.setTristate(False)
        self.Check_Entertainment.setObjectName("Check_Entertainment")
        self.Check_Housing = QtWidgets.QCheckBox(self.page_2)
        self.Check_Housing.setGeometry(QtCore.QRect(130, 71, 241, 51))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Check_Housing.setFont(font)
        self.Check_Housing.setTristate(False)
        self.Check_Housing.setObjectName("Check_Housing")
        self.Check_Childcare = QtWidgets.QCheckBox(self.page_2)
        self.Check_Childcare.setGeometry(QtCore.QRect(410, 191, 241, 51))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Check_Childcare.setFont(font)
        self.Check_Childcare.setTristate(False)
        self.Check_Childcare.setObjectName("Check_Childcare")
        self.Check_Taxes = QtWidgets.QCheckBox(self.page_2)
        self.Check_Taxes.setGeometry(QtCore.QRect(410, 221, 241, 51))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Check_Taxes.setFont(font)
        self.Check_Taxes.setTristate(False)
        self.Check_Taxes.setObjectName("Check_Taxes")
        self.graphicsView_4 = QtWidgets.QGraphicsView(self.page_2)
        self.graphicsView_4.setGeometry(QtCore.QRect(20, 11, 71, 61))
        self.graphicsView_4.setObjectName("graphicsView_4")
        self.Check_Utilities = QtWidgets.QCheckBox(self.page_2)
        self.Check_Utilities.setGeometry(QtCore.QRect(130, 191, 241, 51))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Check_Utilities.setFont(font)
        self.Check_Utilities.setTristate(False)
        self.Check_Utilities.setObjectName("Check_Utilities")
        self.Check_Insurance = QtWidgets.QCheckBox(self.page_2)
        self.Check_Insurance.setGeometry(QtCore.QRect(130, 221, 241, 51))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Check_Insurance.setFont(font)
        self.Check_Insurance.setTristate(False)
        self.Check_Insurance.setObjectName("Check_Insurance")
        self.Check_Groceries = QtWidgets.QCheckBox(self.page_2)
        self.Check_Groceries.setGeometry(QtCore.QRect(130, 131, 241, 51))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Check_Groceries.setFont(font)
        self.Check_Groceries.setTristate(False)
        self.Check_Groceries.setObjectName("Check_Groceries")
        self.Check_Travel = QtWidgets.QCheckBox(self.page_2)
        self.Check_Travel.setGeometry(QtCore.QRect(410, 251, 241, 51))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Check_Travel.setFont(font)
        self.Check_Travel.setTristate(False)
        self.Check_Travel.setObjectName("Check_Travel")
        self.Question_7 = QtWidgets.QLabel(self.page_2)
        self.Question_7.setGeometry(QtCore.QRect(110, 41, 1011, 31))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.Question_7.setFont(font)
        self.Question_7.setObjectName("Question_7")
        self.Question_4 = QtWidgets.QLabel(self.page_2)
        self.Question_4.setGeometry(QtCore.QRect(110, 11, 801, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.Question_4.setFont(font)
        self.Question_4.setObjectName("Question_4")
        self.label_3 = QtWidgets.QLabel(self.page_2)
        self.label_3.setGeometry(QtCore.QRect(20, 10, 71, 61))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.Check_Education= QtWidgets.QCheckBox(self.page_2)
        self.Check_Education.setGeometry(QtCore.QRect(410, 161, 241, 51))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Check_Education.setFont(font)
        self.Check_Education.setTristate(False)
        self.Check_Education.setObjectName("Check_Education")
        self.Check_Healthcare = QtWidgets.QCheckBox(self.page_2)
        self.Check_Healthcare.setGeometry(QtCore.QRect(130, 161, 241, 51))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Check_Healthcare.setFont(font)
        self.Check_Healthcare.setTristate(False)
        self.Check_Healthcare.setObjectName("Check_Healthcare")
        self.Check_Clothing = QtWidgets.QCheckBox(self.page_2)
        self.Check_Clothing.setGeometry(QtCore.QRect(410, 131, 171, 51))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Check_Clothing.setFont(font)
        self.Check_Clothing.setTristate(False)
        self.Check_Clothing.setObjectName("Check_Clothing")
        self.Check_Savings = QtWidgets.QCheckBox(self.page_2)
        self.Check_Savings.setGeometry(QtCore.QRect(410, 101, 171, 51))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Check_Savings.setFont(font)
        self.Check_Savings.setTristate(False)
        self.Check_Savings.setObjectName("Check_Savings")
        self.stackedWidget.addWidget(self.page_2)
        self.page_3 = QtWidgets.QWidget()
        self.page_3.setObjectName("page_3")
        self.stackedWidget.addWidget(self.page_3)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 10, 1081, 61))


        self.Q3 = QtWidgets.QGraphicsView(self.page_3)
        self.Q3.setGeometry(QtCore.QRect(20, 11, 71, 61))
        self.Q3.setObjectName("Q3")

        self.QR3 = QtWidgets.QLabel(self.page_3)
        self.QR3.setGeometry(QtCore.QRect(20, 10, 71, 61))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.QR3.setFont(font)
        self.QR3.setAlignment(QtCore.Qt.AlignCenter)
        self.QR3.setObjectName("QR3")

        self.Qu3 = QtWidgets.QLabel(self.page_3)
        self.Qu3.setGeometry(QtCore.QRect(110, 11, 801, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.Qu3.setFont(font)
        self.Qu3.setObjectName("Qu3")
        self.Q73 = QtWidgets.QLabel(self.page_3)
        self.Q73.setGeometry(QtCore.QRect(110, 41, 1011, 31))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.Q73.setFont(font)
        self.Q73.setObjectName("Q73")

        self.check_Income = QtWidgets.QCheckBox(self.page_3)
        self.check_Income.setGeometry(QtCore.QRect(130, 71, 500, 51))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.check_Income.setFont(font)
        self.check_Income.setTristate(False)
        self.check_Income.setObjectName("check_Income")        

        self.IncomeLabel = QtWidgets.QLabel(self.page_3)
        self.IncomeLabel.setGeometry(QtCore.QRect(130, 105, 1000, 61))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.IncomeLabel.setFont(font)
        self.IncomeLabel.setObjectName("IncomeLabel")


        self.salaryNum = QtWidgets.QLineEdit(self.page_3)
        self.salaryNum.setGeometry(QtCore.QRect(130, 160, 140, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.salaryNum.setFont(font)
        self.salaryNum.setObjectName("salaryNum")
        self.salaryNum.setPlaceholderText("Enter salary")  

        self.salaryPeriod = QtWidgets.QComboBox(self.page_3)
        self.salaryPeriod.setGeometry(QtCore.QRect(290, 160, 100, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.salaryPeriod.setFont(font)
        self.salaryPeriod.setObjectName("salaryPeriod") 
        self.salaryPeriod.addItem("/month")
        self.salaryPeriod.addItem("/year")

        self.confirmSalary = QtWidgets.QPushButton(self.page_3)
        self.confirmSalary.setGeometry(QtCore.QRect(410,160, 120, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.confirmSalary.setFont(font)



        def writeSalary(self):
            # Ensure self is an instance of SomeClass
            with open('data.txt  ', 'a') as file:
                salary = self.salaryNum.text()
                period = self.salaryPeriod.currentText()
                file.write(",")
                file.write(salary)
                file.write(period)

        font = QtGui.QFont()    
        font.setPointSize(21)
        font.setBold(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.graphicsView_2.raise_()
        self.graphicsView.raise_()
        self.Page1Button.raise_()
        self.Page3Button.raise_()
        self.Page2Button.raise_()
        self.FinishButton.raise_()
        self.CancelButton.raise_()
        self.stackedWidget.raise_()
        self.label.raise_()
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        #pagebuttons
        def page1Click():
            self.stackedWidget.setCurrentIndex(0)
        def page2Click():
            self.stackedWidget.setCurrentIndex(1)
        def page3Click():
            self.stackedWidget.setCurrentIndex(2)        

        self.Page1Button.clicked.connect(page1Click)
        self.Page2Button.clicked.connect(page2Click)
        self.Page3Button.clicked.connect(page3Click)            

        #Page 2 choices
        def record_choice2(self):
            # Initialize an empty list to collect selected choices
            choices = []
            
            # Check which checkboxes are checked and add corresponding choices to the list
            if self.Check_PersCare.isChecked():
                choices.append("Personal Care")
                print("Personal Care")

            if self.Check_Transport.isChecked():
                choices.append("Transport")
                print("Transport")

            if self.Check_Housing.isChecked():
                choices.append("Housing")
                print("Housing")

            if self.Check_Childcare.isChecked():
                choices.append("Childcare")
                print("Childcare") 
                           
            if self.Check_Taxes.isChecked():
                choices.append("Taxes")
                print("Taxes")

            if self.Check_Groceries.isChecked():
                choices.append("Groceries")
                print("Groceries")

            if self.Check_Travel.isChecked():
                choices.append("Travel")
                print("Travel")

            if self.Check_Education.isChecked():
                choices.append("Education")
                print("Education") 
                           
            if self.Check_Healthcare.isChecked():
                choices.append("Healthcare")
                print("Healthcare")

            if self.Check_Clothing.isChecked():
                choices.append("Clothing")
                print("Clothing")

            if self.Check_Savings.isChecked():
                choices.append("Savings")
                print("Savings") 
            
            if self.Check_Utilities.isChecked():
                choices.append("Utilities")
                print("Utilities")
            
            if self.Check_Entertainment.isChecked():
                choices.append("Entertainment")
                print("Entertainment")
              
            if self.Check_Entertainment.isChecked():
                choices.append("Insurance")
                print("Insurance")  
            # Add more checkboxes as needed here
            
            # Write the choices to a file if any checkboxes are selected
            if choices:
                # Read the existing content of the file
                try:
                    with open('data.txt', 'r') as file:
                        content = file.read()
                except FileNotFoundError:
                    content = ''  # File does not exist, start with an empty content
                
                # Split the content by commas and strip any extra whitespace
                items = [item.strip() for item in content.split(',') if item.strip()]

                # Append the new choices to the existing items
                items.extend(choices)

                # Join the items back together with a comma and a space
                new_content = ','.join(items)

                # Write the updated content to the file
                with open('data.txt', 'w') as file:
                    file.write(new_content)

        


        def finishSetup():
            if not self.FinishPushed1:  # Check if self.pushed2 is False
                self.FinishButton.setText(QtCore.QCoreApplication.translate("MainWindow", "Confirm?"))
                self.FinishPushed1 = True  # Set self.pushed2 to True after the first press
            else:  # If self.pushed2 is True
                record_choice(self)
                record_choice2(self)
                writeSalary(self)
                quit()  # Quit the application
                 
            
        self.FinishButton.clicked.connect(finishSetup)  


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Setup"))
        self.Page1Button.setText(_translate("MainWindow", "Page 1"))
        self.Page3Button.setText(_translate("MainWindow", "Page 3"))
        self.Page2Button.setText(_translate("MainWindow", "Page 2"))
        self.FinishButton.setText(_translate("MainWindow", "Finish"))
        self.CancelButton.setText(_translate("MainWindow", "Cancel"))
        self.Question.setText(_translate("MainWindow", "Please choose if you want to setup a family or personal budget."))
        self.Personal.setText(_translate("MainWindow", "Personal"))
        self.Question_2.setText(_translate("MainWindow", "* - These caterogies are considered important and are recommended to be included."))
        self.Question_3.setText(_translate("MainWindow", "NOTE: This will add some features such as \"Shared Shopping List\", and a Trust Fund for children."))
        self.label_2.setText(_translate("MainWindow", "1"))
        self.Family.setText(_translate("MainWindow", "Family"))
        self.Check_PersCare.setText(_translate("MainWindow", "Personal Care"))
        self.Question_5.setText(_translate("MainWindow", "* - These caterogies are considered important and are recommended to be included."))
        self.Check_Transport.setText(_translate("MainWindow", "Transportation*"))
        self.Check_Entertainment.setText(_translate("MainWindow", "Entertainment"))
        self.Check_Housing.setText(_translate("MainWindow", "Housing*"))
        self.Check_Childcare.setText(_translate("MainWindow", "Childcare"))
        self.Check_Taxes.setText(_translate("MainWindow", "Taxes"))
        self.Check_Utilities.setText(_translate("MainWindow", "Utilities"))
        self.Check_Insurance.setText(_translate("MainWindow", "Insurance"))
        self.Check_Groceries.setText(_translate("MainWindow", "Groceries*"))
        self.Check_Travel.setText(_translate("MainWindow", "Travel"))
        self.Question_7.setText(_translate("MainWindow", "NOTE: You will be able to change these after you have finished creating the budget"))
        self.Q73.setText(_translate("MainWindow", "NOTE: You will be able to change these after you have finished creating the budget"))
        self.Question_4.setText(_translate("MainWindow", "Please choose which categories you want to include:"))
        self.label_3.setText(_translate("MainWindow", "2"))
        self.QR3.setText(_translate("MainWindow", "3"))
        self.Qu3.setText(_translate("MainWindow", "Please choose the remaining preferences:"))
        self.Check_Education.setText(_translate("MainWindow", "Education"))
        self.Check_Healthcare.setText(_translate("MainWindow", "Healthcare*"))
        self.Check_Clothing.setText(_translate("MainWindow", "Clothing"))
        self.Check_Savings.setText(_translate("MainWindow", "Savings"))
        self.label.setText(_translate("MainWindow", "MY SETUP WIZARD"))
        self.check_Income.setText(_translate("MainWindow", "Include Income?"))
        self.IncomeLabel.setText(_translate("MainWindow", "If so, please enter value using of the periods below. Please only use numbers without commas."))
        self.confirmSalary.setText(_translate("MainWindow", "Confirm"))



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow2()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

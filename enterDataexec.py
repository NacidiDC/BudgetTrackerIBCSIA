from PyQt5 import QtCore, QtGui, QtWidgets
import pickle


class Ui_Dialog(object):
    cancelData = False
    
    def setupUi(self, Dialog):
        cancelData = False
        self.dataFinished = False
        Dialog.setObjectName("Dialog")
        Dialog.resize(1040, 600)
        self.title = QtWidgets.QLabel(Dialog)
        self.title.setGeometry(QtCore.QRect(20, 25, 581, 40))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.title.setFont(font)
        self.title.setObjectName("title")
        self.frame1 = QtWidgets.QGraphicsView(Dialog)
        self.frame1.setGeometry(QtCore.QRect(0, 0, 1040, 90))
        self.frame1.setObjectName("frame1")
        self.note1 = QtWidgets.QLabel(Dialog)
        self.note1.setGeometry(QtCore.QRect(500, 20, 540, 20))
        self.note1.setObjectName("note1")
        self.chosenCat = QtWidgets.QLabel(Dialog)
        self.chosenCat.setGeometry(QtCore.QRect(500, 50, 400, 20))
        self.chosenCat.setObjectName("chosenCat")
        self.Housing = QtWidgets.QLabel(Dialog)
        self.Housing.setGeometry(QtCore.QRect(60, 140, 250, 35))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Housing.setFont(font)
        self.Housing.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.Housing.setObjectName("Housing")
        self.Transportation = QtWidgets.QLabel(Dialog)
        self.Transportation.setGeometry(QtCore.QRect(60, 190, 250, 35))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Transportation.setFont(font)
        self.Transportation.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.Transportation.setObjectName("Transportation")
        self.Groceries = QtWidgets.QLabel(Dialog)
        self.Groceries.setGeometry(QtCore.QRect(60, 240, 240, 35))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Groceries.setFont(font)
        self.Groceries.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.Groceries.setObjectName("Groceries")
        self.Healthcare = QtWidgets.QLabel(Dialog)
        self.Healthcare.setGeometry(QtCore.QRect(60, 290, 250, 35))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Healthcare.setFont(font)
        self.Healthcare.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.Healthcare.setObjectName("Healthcare")
        self.Utilities = QtWidgets.QLabel(Dialog)
        self.Utilities.setGeometry(QtCore.QRect(60, 340, 250, 35))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Utilities.setFont(font)
        self.Utilities.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.Utilities.setObjectName("Utilities")
        self.PersonalCare = QtWidgets.QLabel(Dialog)
        self.PersonalCare.setGeometry(QtCore.QRect(60, 390, 250, 35))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.PersonalCare.setFont(font)
        self.PersonalCare.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.PersonalCare.setObjectName("PersonalCare")
        self.Insurance = QtWidgets.QLabel(Dialog)
        self.Insurance.setGeometry(QtCore.QRect(60, 440, 250, 35))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Insurance.setFont(font)
        self.Insurance.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.Insurance.setObjectName("Insurance")
        self.housingEdit = QtWidgets.QLineEdit(Dialog)
        self.housingEdit.setGeometry(QtCore.QRect(270, 140, 80, 30))
        self.housingEdit.setObjectName("housingEdit")
        font = QtGui.QFont()
        font.setPointSize(12)
        self.transportEdit = QtWidgets.QLineEdit(Dialog)
        self.transportEdit.setGeometry(QtCore.QRect(270, 190, 80, 30))
        self.transportEdit.setObjectName("transportEdit")
        self.healthcareEdit = QtWidgets.QLineEdit(Dialog)
        self.healthcareEdit.setGeometry(QtCore.QRect(270, 240, 80, 30))
        self.healthcareEdit.setObjectName("healthcareEdit")
        self.groceriesEdit = QtWidgets.QLineEdit(Dialog)
        self.groceriesEdit.setGeometry(QtCore.QRect(270, 290, 80, 30))
        self.groceriesEdit.setObjectName("groceriesEdit")
        self.insuranceEdit = QtWidgets.QLineEdit(Dialog)
        self.insuranceEdit.setGeometry(QtCore.QRect(270, 340, 80, 30))
        self.insuranceEdit.setObjectName("insuranceEdit")
        self.utilitiesEdit = QtWidgets.QLineEdit(Dialog)
        self.utilitiesEdit.setGeometry(QtCore.QRect(270, 390, 80, 30))
        self.utilitiesEdit.setObjectName("utilitiesEdit")
        self.perscareEdit = QtWidgets.QLineEdit(Dialog)
        self.perscareEdit.setGeometry(QtCore.QRect(270, 440, 80, 30))
        self.perscareEdit.setObjectName("perscareEdit")
        self.frame2 = QtWidgets.QGraphicsView(Dialog)
        self.frame2.setGeometry(QtCore.QRect(40, 120, 375, 375))
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        self.frame2.setBackgroundBrush(brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        self.frame2.setForegroundBrush(brush)
        self.frame2.setObjectName("frame2")
        self.frame3 = QtWidgets.QGraphicsView(Dialog)
        self.frame3.setGeometry(QtCore.QRect(625, 120, 375, 375))
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        self.frame3.setBackgroundBrush(brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        self.frame3.setForegroundBrush(brush)
        self.frame3.setObjectName("frame3")
        self.educationEdit = QtWidgets.QLineEdit(Dialog)
        self.educationEdit.setGeometry(QtCore.QRect(855, 290, 80, 30))
        self.educationEdit.setObjectName("educationEdit")
        self.Entertainment = QtWidgets.QLabel(Dialog)
        self.Entertainment.setGeometry(QtCore.QRect(645, 140, 250, 35))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Entertainment.setFont(font)
        self.Entertainment.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.Entertainment.setObjectName("Entertainment")
        self.childcareEdit = QtWidgets.QLineEdit(Dialog)
        self.childcareEdit.setGeometry(QtCore.QRect(855, 340, 80, 30))
        self.childcareEdit.setObjectName("childcareEdit")
        self.Travel = QtWidgets.QLabel(Dialog)
        self.Travel.setGeometry(QtCore.QRect(645, 440, 250, 35))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Travel.setFont(font)
        self.Travel.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.Travel.setObjectName("Travel")
        self.savingsEdit = QtWidgets.QLineEdit(Dialog)
        self.savingsEdit.setGeometry(QtCore.QRect(855, 190, 80, 30))
        self.savingsEdit.setObjectName("savingsEdit")
        self.Childcare = QtWidgets.QLabel(Dialog)
        self.Childcare.setGeometry(QtCore.QRect(645, 340, 250, 35))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Childcare.setFont(font)
        self.Childcare.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.Childcare.setObjectName("Childcare")
        self.Clothing = QtWidgets.QLabel(Dialog)
        self.Clothing.setGeometry(QtCore.QRect(645, 240, 250, 35))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Clothing.setFont(font)
        self.Clothing.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.Clothing.setObjectName("Clothing")
        self.Savings = QtWidgets.QLabel(Dialog)
        self.Savings.setGeometry(QtCore.QRect(645, 190, 250, 35))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Savings.setFont(font)
        self.Savings.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.Savings.setObjectName("Savings")
        self.travelEdit = QtWidgets.QLineEdit(Dialog)
        self.travelEdit.setGeometry(QtCore.QRect(855, 440, 80, 30))
        self.travelEdit.setObjectName("travelEdit")
        self.Taxes = QtWidgets.QLabel(Dialog)
        self.Taxes.setGeometry(QtCore.QRect(645, 390, 250, 35))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Taxes.setFont(font)
        self.Taxes.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.Taxes.setObjectName("Taxes")
        self.clothingEdit = QtWidgets.QLineEdit(Dialog)
        self.clothingEdit.setGeometry(QtCore.QRect(855, 240, 80, 30))
        self.clothingEdit.setObjectName("clothingEdit")
        self.taxesEdit = QtWidgets.QLineEdit(Dialog)
        self.taxesEdit.setGeometry(QtCore.QRect(855, 390, 80, 30))
        self.taxesEdit.setObjectName("taxesEdit")
        self.Education = QtWidgets.QLabel(Dialog)
        self.Education.setGeometry(QtCore.QRect(645, 290, 250, 35))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Education.setFont(font)
        self.Education.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.Education.setObjectName("Education")
        self.entertEdit = QtWidgets.QLineEdit(Dialog)
        self.entertEdit.setGeometry(QtCore.QRect(855, 140, 80, 30))
        self.entertEdit.setObjectName("entertEdit")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(880, 530, 120, 40))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(740, 530, 120, 40))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")

         


        def writeCosts(self):
            
            if self.housingEdit.text() == "":
                housingCost = 0
            else:
                housingCost = float(self.housingEdit.text())
            
            if self.transportEdit.text() == "":
                transportCost = 0
            else:
                transportCost = float(self.transportEdit.text())
            
            if self.groceriesEdit.text() == "":
                groceriesCost = 0
            else:
                groceriesCost = float(self.groceriesEdit.text())

            if self.healthcareEdit.text() == "":
                healthcareCost = 0
            else:
                healthcareCost = float(self.healthcareEdit.text())
                
            if self.utilitiesEdit.text() == "":
                utilitiesCost = 0
            else:
                utilitiesCost = float(self.utilitiesEdit.text())

            if self.insuranceEdit.text() == "":
                insuranceCost = 0
            else:
                insuranceCost = float(self.insuranceEdit.text())

            if self.perscareEdit.text() == "":
                perscareCost = 0
            else:
                perscareCost = float(self.perscareEdit.text())

            if self.entertEdit.text() == "":
                entertCost = 0
            else:
               entertCost = float(self.entertEdit.text()) 
                
            if self.savingsEdit.text() == "":
                savingsCost = 0
            else:
                savingsCost = float(self.savingsEdit.text())

            if self.clothingEdit.text() == "":
                clothing = 0
            else:
                clothing = float(self.clothingEdit.text())

            if self.educationEdit.text() == "":
                educationCost = 0
            else:
                educationCost = float(self.educationEdit.text())

            if self.childcareEdit.text() == "":
                childcareCost = 0  
            else: 
                childcareCost = float(self.childcareEdit.text())

            if self.taxesEdit.text() == "":
                taxesCost = 0
            else:
                taxesCost = float(self.taxesEdit.text())

            if self.travelEdit.text() == "":
                travelCost = 0
            else: 
                travelCost = float(self.travelEdit.text())

            cost_array = [
                ["Housing", housingCost],
                ["Transportation", transportCost],
                ["Groceries", groceriesCost],
                ["Healthcare", healthcareCost],
                ["Utilities", utilitiesCost],
                ["Insurance", insuranceCost],
                ["Personal Care", perscareCost],
                ["Entertainment", entertCost],
                ["Savings", savingsCost],
                ["Education", educationCost],
                ["Clothing", clothing],
                ["Childcare", childcareCost],
                ["Taxes", taxesCost],
                ["Travel", travelCost]
            ]

            print(cost_array)
            with open('array_data.pkl', 'wb') as f:
                pickle.dump(cost_array, f)


        def finishData():
            if not self.dataFinished:  # Check if self.pushed2 is False
                self.pushButton.setText(QtCore.QCoreApplication.translate("MainWindow", "Confirm?"))
                self.dataFinished = True  # Set self.pushed2 to True after the first press
            else:  # If self.pushed2 is True
                writeCosts(self)
                quit()  # Quit the application
                
            
        self.pushButton.clicked.connect(finishData)


        def cancelData():
            if not self.cancelData:  # Check if self.pushed1 is False
                self.pushButton_2.setText(QtCore.QCoreApplication.translate("MainWindow", "Confirm?"))
                self.cancelData = True  # Set self.pushed1 to True after the first press
            else:  # If self.pushed1 is True
                quit()  # Quit the application
            
        self.pushButton_2.clicked.connect(cancelData)

        

        self.frame2.raise_()
        self.frame1.raise_()
        self.title.raise_()
        self.note1.raise_()
        self.chosenCat.raise_()
        self.Housing.raise_()
        self.Transportation.raise_()
        self.Groceries.raise_()
        self.Healthcare.raise_()
        self.Utilities.raise_()
        self.PersonalCare.raise_()
        self.Insurance.raise_()
        self.housingEdit.raise_()
        self.transportEdit.raise_()
        self.healthcareEdit.raise_()
        self.groceriesEdit.raise_()
        self.insuranceEdit.raise_()
        self.utilitiesEdit.raise_()
        self.perscareEdit.raise_()
        self.frame3.raise_()
        self.educationEdit.raise_()
        self.Entertainment.raise_()
        self.childcareEdit.raise_()
        self.Travel.raise_()
        self.savingsEdit.raise_()
        self.Childcare.raise_()
        self.Clothing.raise_()
        self.Savings.raise_()
        self.travelEdit.raise_()
        self.Taxes.raise_()
        self.clothingEdit.raise_()
        self.taxesEdit.raise_()
        self.Education.raise_()
        self.entertEdit.raise_()
        self.pushButton.raise_()
        self.pushButton_2.raise_()

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.title.setText(_translate("Dialog", "Enter your cost data (monthly)"))
        self.note1.setText(_translate("Dialog", "NOTE: Do not fill any information in the categories you have not chosen"))
        self.chosenCat.setText(_translate("Dialog", "Chosen catagories: "))
        self.Housing.setText(_translate("Dialog", "Housing"))
        self.Transportation.setText(_translate("Dialog", "Transportation"))
        self.Groceries.setText(_translate("Dialog", "Groceries"))
        self.Healthcare.setText(_translate("Dialog", "Healthcare"))
        self.Utilities.setText(_translate("Dialog", "Utilities"))
        self.PersonalCare.setText(_translate("Dialog", "Personal Care"))
        self.Insurance.setText(_translate("Dialog", "Insurance"))
        self.Entertainment.setText(_translate("Dialog", "Entertainment"))
        self.Travel.setText(_translate("Dialog", "Travel"))
        self.Childcare.setText(_translate("Dialog", "Childcare"))
        self.Clothing.setText(_translate("Dialog", "Clothing"))
        self.Savings.setText(_translate("Dialog", "Savings"))
        self.Taxes.setText(_translate("Dialog", "Taxes"))
        self.Education.setText(_translate("Dialog", "Education"))
        self.pushButton.setText(_translate("Dialog", "Confirm"))
        self.pushButton_2.setText(_translate("Dialog", "Cancel"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

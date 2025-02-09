from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QInputDialog
from setupFile import Ui_MainWindow2
import sqlite3
from mainAppRework import Ui_MainWindow3
import tempfile

import os


class Ui_MainWindow(object):
    def openSetup(self):
        self.window1 = QtWidgets.QMainWindow()
        self.ui1 = Ui_MainWindow2()
        self.ui1.setupUi(self.window1)
        self.window1.show()
    
    def openMainApp(self):
        # Ensure the database path is set
        if not hasattr(self, 'db_path') or not self.db_path:
            try:
                with open("db_path.txt", "r") as file:
                    self.db_path = file.read().strip()
                print(f"DEBUG: Loaded db_path from file: {self.db_path}")
            except FileNotFoundError:
                QMessageBox.warning(None, "No Database Selected", "Please select a valid database first.")
                return
            except Exception as e:
                QMessageBox.warning(None, "Error", f"Failed to load database path: {str(e)}")
                return

        # Validate the database
        if not self.is_valid_database(self.db_path):
            QMessageBox.warning(None, "Invalid Database", "The selected file is not a valid budget database.")
            return

        # Prompt for password
        password, ok = QInputDialog.getText(
            None,
            "Password Required",
            "Enter your password:",
            QtWidgets.QLineEdit.Password
        )
        if not ok or not password:
            QMessageBox.warning(None, "Password Missing", "You must enter a valid password.")
            return

        # Verify password
        if not self.verify_password(self.db_path, password):
            QMessageBox.critical(None, "Invalid Password", "The password you entered is incorrect.")
            return

        # Initialize and show the main application window
        try:
            self.window3 = QtWidgets.QMainWindow()
            self.ui3 = Ui_MainWindow3(self.db_path)  # Pass db_path to Ui_MainWindow3
            self.ui3.setupUi(self.window3)
            self.window3.show()
 
            print("DEBUG: Main app window opened successfully.")
        except Exception as e:
            print(f"DEBUG: Error opening main app: {e}")
            QMessageBox.critical(None, "Error", f"Failed to open main app: {str(e)}")



    
    def verify_password(self, db_path, password):
        """
        Verify the user's password by checking it against the hashed password stored in the database.
        """
        try:
            connection = sqlite3.connect(db_path)
            cursor = connection.cursor()

            # Retrieve the hashed password from the database
            cursor.execute("SELECT hash FROM password LIMIT 1")  # Adjust table and column names as needed
            result = cursor.fetchone()
            if not result:
                QMessageBox.warning(None, "Database Error", "No password found in the database.")
                return False

            hashed_password = result[0]

            # Hash the input password and compare
            import hashlib
            hashed_input = hashlib.sha256(password.encode()).hexdigest()
            return hashed_input == hashed_password

        except sqlite3.DatabaseError as e:
            QMessageBox.critical(None, "Database Error", f"Failed to verify password: {e}")
            return False
        finally:
            connection.close()
    
    def select_database(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(
            None, "Select Budget Database", "", "SQLite Database (*.db);;All Files (*)", options=options
        )

        if not file_path:  # User canceled the dialog
            print("No file selected.")
            return

        print(f"DEBUG: Selected file path: {file_path}")  # Debugging

        if not self.is_valid_database(file_path):
            QMessageBox.warning(None, "Invalid Database", "The selected file is not a valid budget database.")
            return

        # Set the selected database file path for use
        self.db_path = file_path
        print(f"DEBUG: Database path set to {self.db_path}")  # Debugging

        # Save the path to db_path.txt
        try:
            with open("db_path.txt", "w") as file:
                file.write(self.db_path)
            print("DEBUG: Database path saved to db_path.txt")
        except Exception as e:
            print(f"DEBUG: Failed to save database path to file: {e}")

        # Open the main app 
        self.openMainApp()
            


    def is_valid_database(self, db_path):
        if not os.path.exists(db_path):
            print(f"Database file {db_path} does not exist.")
            return False

        try:
            connection = sqlite3.connect(db_path)
            cursor = connection.cursor()

            # Get all table names
            cursor.execute("SELECT LOWER(name) FROM sqlite_master WHERE type='table';")
            tables = {table[0] for table in cursor.fetchall()}

            print(f"Tables found in {db_path}: {tables}")

            required_tables = {"budgets", "categories", "expenses", "income_sources", "password"}
            missing_tables = required_tables - tables

            if missing_tables:
                print(f"ERROR: Missing tables: {missing_tables}")
                return False

            # Validate the relationship between `password` and `budgets`
            cursor.execute("""
                SELECT p.budget_id
                FROM password p
                LEFT JOIN budgets b ON p.budget_id = b.id
                WHERE b.id IS NULL
            """)
            if cursor.fetchone():
                print("ERROR: Orphaned password records found!")
                return False

            # Ensure it's a valid SQLite file
            cursor.execute("PRAGMA integrity_check;")
            integrity_result = cursor.fetchone()
            if integrity_result[0] != "ok":
                print("Database integrity check failed!")
                return False

            print("Database is valid and ready to use!")
            connection.close()
            return True

        except sqlite3.DatabaseError as e:
            print(f"Database error: {e}")
            return False


        
        



    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(740, 540)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.fileNew = QtWidgets.QPushButton(self.centralwidget, clicked = lambda: self.openSetup())
        self.fileNew.setGeometry(QtCore.QRect(244.5, 160, 251, 51))
        font = QtGui.QFont()
        font.setFamily("White Rabbit")
        font.setPointSize(11)
        self.fileNew.setFont(font)
        self.fileNew.setObjectName("fileNew")
        self.openFile = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.select_database())
        self.openFile.setGeometry(QtCore.QRect(220, 305.5, 300, 51))
        font = QtGui.QFont()
        font.setFamily("White Rabbit")
        font.setPointSize(11)
        self.openFile.setFont(font)
        self.openFile.setObjectName("openFile")
        MainWindow.setCentralWidget(self.centralwidget)
        self.actionNew_File = QtWidgets.QAction(MainWindow)
        self.actionNew_File.setObjectName("actionNew_File")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.fileNew.setText(_translate("MainWindow", "New Budget"))
        self.openFile.setText(_translate("MainWindow", "Open  Existing Budget"))
        self.actionNew_File.setText(_translate("MainWindow", "New File"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

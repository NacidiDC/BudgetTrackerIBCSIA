from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QInputDialog, QWidget, QVBoxLayout
from datetime import datetime
import sqlite3
import os
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from dateutil.relativedelta import relativedelta





class Ui_MainWindow3(object):
    def __init__(self, db_path):
        self.db_path = db_path  # Store the database path for use in the app
        print(f"DEBUG: Main app initialized with db_path: {self.db_path}")

    def load_categories(self):
        try:
            # Connect to the database
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()

            # Retrieve categories and corresponding expenses
            cursor.execute("""
                SELECT c.category, 
                    COALESCE(SUM(e.amount), 0) AS total_expense
                FROM categories c
                LEFT JOIN expenses e ON c.id = e.category_id
                GROUP BY c.id
            """)
            categories = cursor.fetchall()

            # Compute total expenses
            total_expense = sum(expense for _, expense in categories)

            # Set up the table: Rows = Categories + 1 for Total Costs, Columns = ["Category", "Expense", "% of Total"]
            self.tableWidget.setColumnCount(3)  # Three columns: Category, Expense, Percentage of Total
            self.tableWidget.setHorizontalHeaderLabels(["Category", "Expense", "% of Total"])
            self.tableWidget.setRowCount(len(categories) + 1)  # Extra row for total costs

            # Populate the table with category names, expenses, and percentage of total
            for row, (category, expense) in enumerate(categories):
                category_item = QtWidgets.QTableWidgetItem(category)
                expense_item = QtWidgets.QTableWidgetItem(f"{expense:.2f}")  # Format expense as currency

                # Calculate percentage of total
                percentage = (expense / total_expense) * 100 if total_expense > 0 else 0
                percentage_item = QtWidgets.QTableWidgetItem(f"{percentage:.2f}%")

                # Center-align text
                category_item.setTextAlignment(QtCore.Qt.AlignCenter)
                expense_item.setTextAlignment(QtCore.Qt.AlignCenter)
                percentage_item.setTextAlignment(QtCore.Qt.AlignCenter)

                self.tableWidget.setItem(row, 0, category_item)  # Category column
                self.tableWidget.setItem(row, 1, expense_item)   # Expense column
                self.tableWidget.setItem(row, 2, percentage_item)  # % of Total column

            # Add a row for total costs at the bottom
            total_label = QtWidgets.QTableWidgetItem("Total")
            total_label.setTextAlignment(QtCore.Qt.AlignCenter)
            total_expense_item = QtWidgets.QTableWidgetItem(f"{total_expense:.2f}")
            total_expense_item.setTextAlignment(QtCore.Qt.AlignCenter)
            total_percentage_item = QtWidgets.QTableWidgetItem("100.00%")  # Total is always 100%
            total_percentage_item.setTextAlignment(QtCore.Qt.AlignCenter)

            # Insert total row at the bottom
            total_row_index = len(categories)
            self.tableWidget.setItem(total_row_index, 0, total_label)
            self.tableWidget.setItem(total_row_index, 1, total_expense_item)
            self.tableWidget.setItem(total_row_index, 2, total_percentage_item)

            # Adjust column widths to divide equally
            table_width = self.tableWidget.width() - 20  # Subtract a bit to account for padding
            self.tableWidget.setColumnWidth(0, table_width // 3)
            self.tableWidget.setColumnWidth(1, table_width // 3)
            self.tableWidget.setColumnWidth(2, table_width // 3)

            # Adjust row heights to avoid scroll bars
            table_height = self.tableWidget.height() - 20  # Subtract for extra padding or headers
            num_rows = self.tableWidget.rowCount()
            if num_rows > 0:
                row_height = table_height // num_rows
                for row in range(num_rows):
                    self.tableWidget.setRowHeight(row, row_height)

            # Disable scroll bars
            self.tableWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
            self.tableWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

            connection.close()
            print("DEBUG: Categories, expenses, and table refreshed successfully!")

        except sqlite3.DatabaseError as e:
            QtWidgets.QMessageBox.warning(None, "Database Error", f"Failed to load categories: {e}")




    def generate_pie_chart(self):
        try:
            # Read the database path
            with open("db_path.txt", "r") as file:
                db_path = file.read().strip()

            # Connect to the database
            connection = sqlite3.connect(db_path)
            cursor = connection.cursor()

            # Fetch data for the pie chart
            cursor.execute("""
                SELECT c.category, COALESCE(SUM(e.amount), 0) AS total_expense
                FROM categories c
                LEFT JOIN expenses e ON c.id = e.category_id
                GROUP BY c.id
            """)
            data = cursor.fetchall()
            connection.close()

            # Prepare labels and values
            labels = [row[0] for row in data]
            values = [row[1] for row in data]
            filtered_data = [(label, value) for label, value in zip(labels, values) if value > 0]
            if not filtered_data:
                QtWidgets.QMessageBox.information(None, "No Data", "No expenses to display.")
                return

            labels, values = zip(*filtered_data)
            pastel_colors = ["#FFB3BA", "#FFDFBA", "#FFFFBA", "#BAFFC9", "#BAE1FF", "#D5BAFF"] * (len(labels) // 6 + 1)

            # Create the figure
            figure = Figure(figsize=(5.5, 5.5))
            canvas = FigureCanvas(figure)
            ax = figure.add_subplot(111)

            # Plot pie chart
            ax.pie(
                values,
                labels=labels,
                autopct="%1.1f%%",
                startangle=90,
                textprops={"fontsize": 14},
                colors=pastel_colors[:len(labels)],
                labeldistance=1.1
            )
            ax.axis("equal")

            layout = self.PieChart.layout()
            if layout is None:
                layout = QtWidgets.QVBoxLayout(self.PieChart)
                self.PieChart.setLayout(layout)

            for i in reversed(range(layout.count())):
                widget = layout.itemAt(i).widget()
                if widget:
                    widget.setParent(None)

            # Add the canvas to the layout
            layout.addWidget(canvas)
            print("Pie chart updated successfully!")

        except sqlite3.DatabaseError as e:
            QtWidgets.QMessageBox.warning(None, "Database Error", f"Failed to load pie chart data: {e}")
        except Exception as e:
            QtWidgets.QMessageBox.warning(None, "Error", f"An unexpected error occurred: {e}")
        
    def calculate_progress(self):
        """Calculate and display progress, total income, total expenses, number of incomes, remaining balance, and status."""
        try:
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()

            # Fetch Total Income from the `budgets` table
            cursor.execute("SELECT COALESCE(income, 0) FROM budgets LIMIT 1")
            total_income = cursor.fetchone()[0]

            # Fetch Total Expenses
            cursor.execute("SELECT COALESCE(SUM(amount), 0) FROM expenses")
            total_expenses = cursor.fetchone()[0]

            # Count of Categories with and without Expenses
            cursor.execute("""
                SELECT COUNT(*)
                FROM categories c
                LEFT JOIN expenses e ON c.id = e.category_id
                WHERE e.amount IS NULL OR e.amount = 0
            """)
            categories_without_expenses = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM categories")
            total_categories = cursor.fetchone()[0]

            # Calculate Progress as a Percentage
            progress_percentage = ((total_categories - categories_without_expenses) / total_categories * 100 
                                    if total_categories > 0 else 0.0)

            # Calculate Remaining Balance
            remaining_balance = total_income - total_expenses

            # Determine Status (Over or Under Budget)
            if remaining_balance >= 0:
                status_text = "Under Budget"
                status_color = "green"
            else:
                status_text = "Over Budget"
                status_color = "red"

            # Update UI Labels
            self.label.setText(f"Expenses missing: {categories_without_expenses}")
            self.label_2.setText(f"Progress: {progress_percentage:.2f}%")
            self.tIncome.setText(f"Total Income: {total_income:.2f}")
            self.label_3.setText(f"Total Income: {total_income:.2f}")
            self.tExpenses.setText(f"Total Expenses: {total_expenses:.2f}")
            self.remBal.setText(f"Remaining Balance: {remaining_balance:.2f}")
            self.label_4.setText(f"Number of incomes: {max(1, total_categories)}")  # Minimum 1 for main income
            self.statusChangeable.setText(status_text)
            self.statusChangeable.setStyleSheet(f"color: {status_color}; font-weight: bold;")

            connection.close()
        except sqlite3.DatabaseError as e:
            QtWidgets.QMessageBox.critical(None, "Database Error", f"Failed to calculate progress: {e}")
        except Exception as e:
            QtWidgets.QMessageBox.critical(None, "Error", f"Unexpected error: {e}")



    def generate_category_bar_charts(self):
        """Generate bar charts for each category and update the BarTabView dynamically."""
        try:
            print("DEBUG: Generating category bar charts...")

            # Connect to the database
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()

            # Fetch categories and their expenses
            cursor.execute("""
                SELECT c.category, COALESCE(SUM(e.amount), 0) AS total_expense
                FROM categories c
                LEFT JOIN expenses e ON c.id = e.category_id
                GROUP BY c.id
            """)
            categories = cursor.fetchall()
            connection.close()

            # Debug output to check categories and expenses
            print(f"DEBUG: Categories fetched: {categories}")

            if not categories:
                print("DEBUG: No categories available.")
                return

            # Clear existing tabs
            while self.BarTabView.count() > 0:
                self.BarTabView.removeTab(0)

            # Add a bar chart for each category
            for category_name, total_expense in categories:
                new_tab = QtWidgets.QWidget()
                layout = QVBoxLayout(new_tab)

                # Create the bar chart
                figure = Figure(figsize=(5, 3))
                canvas = FigureCanvas(figure)
                ax = figure.add_subplot(111)
                ax.bar([category_name], [total_expense], color="#69b3a2")

                # Improved labels and title
                ax.set_title(f"Total Expenses for {category_name}", fontsize=14, fontweight="bold")
                ax.set_xlabel("Category", fontsize=12)
                ax.set_ylabel("Expense Amount ($)", fontsize=12)

                # Add the chart to the layout
                layout.addWidget(canvas)

                # Add the new tab to BarTabView
                self.BarTabView.addTab(new_tab, category_name)

            print("DEBUG: Bar charts successfully generated and added to tabs.")

        except sqlite3.DatabaseError as e:
            print(f"DEBUG: Database error: {e}")
            QtWidgets.QMessageBox.warning(None, "Database Error", f"Failed to load category bar charts: {e}")
        except Exception as e:
            print(f"DEBUG: Unexpected error: {e}")
            QtWidgets.QMessageBox.warning(None, "Error", f"An unexpected error occurred: {e}")



    def add_other_income(self):
        """Clear the input fields to allow for entering another income source."""
        try:
            # Clear input fields
            self.lineEdit_3.clear()
            self.lineEdit_4.clear()
            self.checkBox_3.setChecked(False)
            self.comboBox_3.setCurrentIndex(3)  # Reset to "Monthly (Default)"

            print("DEBUG: Input fields cleared for adding another income source.")
        except Exception as e:
            print(f"DEBUG: Error clearing input fields: {e}")
            QtWidgets.QMessageBox.warning(None, "Error", f"Failed to clear input fields: {e}")

    def reset_monthly_expenses(self):
        """Reset one-time and non-constant expenses at the start of a new month."""
        try:
            # Get the current month
            current_month = datetime.now().strftime("%B %Y")

            # Connect to the database
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()

            # Reset non-constant and one-time expenses
            cursor.execute("""
                UPDATE expenses
                SET amount = 0
                WHERE frequency IN ('One-Time', 'Weekly', 'Bi-weekly', 'Quarterly', 'Annually')
                AND is_constant = 0
                AND month != ?
            """, (current_month,))
            connection.commit()
            connection.close()

            print("DEBUG: Monthly expenses reset successfully.")
        except sqlite3.DatabaseError as e:
            print(f"DEBUG: Failed to reset monthly expenses: {e}")

    def notify_reminders(self):
        try:
            # Get the current month
            current_month = datetime.now().strftime("%B %Y")

            # Connect to the database
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()

            # Fetch categories with reminders turned on
            cursor.execute("""
                SELECT c.category, e.amount
                FROM expenses e
                JOIN categories c ON e.category_id = c.id
                WHERE e.remind = 1 AND e.month = ?
            """, (current_month,))
            reminders = cursor.fetchall()
            connection.close()

            # Display reminders
            if reminders:
                reminder_text = "\n".join([f"Category: {category}, Amount: {amount}" for category, amount in reminders])
                QtWidgets.QMessageBox.information(None, "Expense Reminders", f"Please update the following expenses:\n\n{reminder_text}")
            else:
                print("DEBUG: No reminders for this month.")
        except sqlite3.DatabaseError as e:
            print(f"DEBUG: Failed to fetch reminders: {e}")

    def update_expense(self):
        try:
            print("DEBUG: update_expense triggered")
            # Fetch input values
            selected_month = self.monthSelect.currentText()
            selected_category = self.catSelect.currentText()
            expense_value = self.lineEdit.text()
            is_constant = 1 if self.checkBox.isChecked() else 0
            remind = 1 if self.checkBox_2.isChecked() else 0
            frequency = self.comboBox.currentText()
            payment_method = self.comboBox_2.currentText()

            # Validate inputs
            if not selected_month or not selected_category or not expense_value:
                QtWidgets.QMessageBox.warning(None, "Error", "All fields must be filled out")
                return

            # Calculate total amount based on frequency
            expense_value = float(expense_value)
            if frequency == "Weekly":
                expense_value *= 4  # Approximation for the month
            elif frequency == "Bi-weekly":
                expense_value *= 2  # Approximation for the month
            elif frequency == "Quarterly":
                expense_value /= 3  # Divide the total amount for 3 months
            elif frequency == "Annually":
                expense_value /= 12  # Divide the total amount for 12 months

            # Connect to the database
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()

            # Update or insert the expense
            cursor.execute("""
                INSERT INTO expenses (budget_id, category_id, amount, month, is_constant, remind, frequency, payment_method)
                SELECT b.id, c.id, ?, ?, ?, ?, ?, ?
                FROM budgets b
                JOIN categories c ON b.id = c.budget_id
                WHERE c.category = ?
                ON CONFLICT (budget_id, category_id, month) DO UPDATE SET
                    amount = CASE
                                WHEN excluded.frequency = 'One-Time' THEN excluded.amount
                                ELSE amount + excluded.amount
                            END,
                    is_constant = excluded.is_constant,
                    remind = excluded.remind,
                    frequency = excluded.frequency,
                    payment_method = excluded.payment_method
            """, (expense_value, selected_month, is_constant, remind, frequency, payment_method, selected_category))
            connection.commit()
            connection.close()

            print("DEBUG: Expense added/updated in database")

            # Notify user
            QtWidgets.QMessageBox.information(None, "Success", "Expense updated successfully!")

            # Reload all visuals
            self.load_categories()  # Reload the table
            self.generate_pie_chart()  # Update the pie chart
            self.generate_category_bar_charts()  # Update the bar charts
            self.calculate_progress()  # Update total income, expenses, and remaining balance
            self.generate_line_chart()
            self.generate_stacked_bar_chart()
            self.generate_bar_chart()
            self.generate_pie_chart_page2()
            print("DEBUG: Table, Pie Chart, Bar Charts, and Progress refreshed")

        except sqlite3.DatabaseError as e:
            QtWidgets.QMessageBox.critical(None, "Database Error", f"Failed to update expense: {e}")
        except ValueError:
            QtWidgets.QMessageBox.warning(None, "Error", "Invalid input for expense value!")


    def update_income(self):
        """Add or update an income source in the database and recalculate totals."""
        try:
            print("DEBUG: confirm_income triggered")

            # Fetch input values
            income_value = self.lineEdit_3.text()
            source_name = self.lineEdit_4.text()
            is_constant = 1 if self.checkBox_3.isChecked() else 0
            frequency = self.comboBox_3.currentText()

            # Validate inputs
            if not income_value or not source_name:
                QtWidgets.QMessageBox.warning(None, "Error", "All fields must be filled out!")
                return

            # Connect to the database
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()

            # Calculate monthly equivalent for non-constant incomes
            income_amount = float(income_value)
            if not is_constant:
                if frequency == "One-Time":
                    pass  # No modification needed
                elif frequency == "Weekly":
                    income_amount *= 4  # Assume 4 weeks in a month
                elif frequency == "Bi-weekly":
                    income_amount *= 2  # Assume 2 periods in a month
                elif frequency == "Monthly (Default)":
                    pass  # No modification needed
                elif frequency == "Quarterly":
                    income_amount /= 3  # Spread across 3 months
                elif frequency == "Annually":
                    income_amount /= 12  # Spread across 12 months

            print(f"DEBUG: Calculated income amount based on frequency: {income_amount}")

            # Update or insert the income source
            cursor.execute("""
                INSERT INTO income_sources (budget_id, source_name, amount, is_constant, frequency)
                VALUES ((SELECT id FROM budgets LIMIT 1), ?, ?, ?, ?)
                ON CONFLICT(budget_id, source_name) DO UPDATE SET
                    amount = amount + excluded.amount,
                    is_constant = excluded.is_constant,
                    frequency = excluded.frequency
            """, (source_name, income_amount, is_constant, frequency))
            connection.commit()

            # Update the total income in the `budgets` table
            cursor.execute("""
                UPDATE budgets
                SET income = (
                    SELECT COALESCE(SUM(amount), 0)
                    FROM income_sources
                    WHERE budget_id = budgets.id
                )
                WHERE id = (SELECT id FROM budgets LIMIT 1)
            """)
            connection.commit()

            # Close the database connection
            connection.close()

            # Notify user and refresh UI
            QtWidgets.QMessageBox.information(None, "Success", "Income source added/updated successfully!")
            self.generate_pie_chart()  # Update the pie chart
            self.calculate_progress()  # Recalculate totals and update UI
            self.generate_line_chart()
            self.generate_stacked_bar_chart()
            self.generate_bar_chart()
            self.generate_pie_chart_page2()
            print("DEBUG: Total income updated, Pie Chart refreshed, and progress recalculated.")

        except sqlite3.DatabaseError as e:
            print(f"DEBUG: Failed to add/update income source: {e}")
            QtWidgets.QMessageBox.critical(None, "Database Error", f"Failed to add/update income source: {e}")
        except Exception as e:
            print(f"DEBUG: Unexpected error in confirm_income: {e}")
            QtWidgets.QMessageBox.warning(None, "Error", f"An unexpected error occurred: {e}")


    def generate_line_chart(self):
        """Generate an interactive line chart for total expenses per month."""
        try:
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()

            # Fetch total expenses per month
            cursor.execute("""
                SELECT month, COALESCE(SUM(amount), 0) AS total_expense
                FROM expenses
                GROUP BY month
                ORDER BY date(month) ASC
            """)
            data = cursor.fetchall()
            connection.close()

            # Validate data: Ensure there are at least two months with expenses
            if not data or len(data) < 2:
                QtWidgets.QMessageBox.information(None, "Missing Data",
                                                "You need to add expense data from at least two past months for this graph to work.")
                return

            # Process Data
            months = []
            expenses = []

            for row in data:
                month, expense = row
                if expense is None:  # Skip if data is missing
                    continue
                months.append(month)
                expenses.append(expense)

            # If less than two months have valid expenses, cancel
            if len(months) < 2:
                QtWidgets.QMessageBox.information(None, "Insufficient Data",
                                                "At least two months of data are required to generate this chart.")
                return

            # Create figure
            figure = Figure(figsize=(6, 4))
            canvas = FigureCanvas(figure)
            ax = figure.add_subplot(111)

            # Plot line chart
            ax.plot(months, expenses, marker="o", linestyle="-", color="blue", label="Total Expenses")
            ax.set_title("Total Expenses Per Month", fontsize=14, fontweight="bold")
            ax.set_xlabel("Month", fontsize=12)
            ax.set_ylabel("Expenses ($)", fontsize=12)
            ax.grid(True)
            ax.legend()

            # Add canvas to the layout
            layout = self.LineGraphView.layout()
            if layout is None:
                layout = QVBoxLayout(self.LineGraphView)
                self.LineGraphView.setLayout(layout)

            for i in reversed(range(layout.count())):
                widget = layout.itemAt(i).widget()
                if widget:
                    widget.setParent(None)

            layout.addWidget(canvas)
            print("DEBUG: Line chart successfully rendered.")

        except sqlite3.DatabaseError as e:
            QtWidgets.QMessageBox.warning(None, "Database Error", f"Failed to load line chart data: {e}")
        except Exception as e:
            QtWidgets.QMessageBox.warning(None, "Error", f"An unexpected error occurred: {e}")




    def generate_stacked_bar_chart(self):
        """Generate an interactive stacked bar chart for category-wise expenses over time."""
        try:
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()

            # Fetch category-wise monthly expenses
            cursor.execute("""
                SELECT c.category, e.month, SUM(e.amount)
                FROM categories c
                JOIN expenses e ON c.id = e.category_id
                GROUP BY c.category, e.month
                ORDER BY e.month ASC
            """)
            data = cursor.fetchall()
            connection.close()

            # Ensure at least two months of valid data exist
            if not data or len(set(row[1] for row in data)) < 2:
                QtWidgets.QMessageBox.information(None, "Missing Data",
                                                "You need at least two months of data for this chart to work.")
                return

            # Prepare data
            categories = list(set(row[0] for row in data))
            months = sorted(set(row[1] for row in data))
            category_expenses = {category: [0] * len(months) for category in categories}

            for category, month, amount in data:
                if amount is None:
                    continue  # Skip missing data
                category_expenses[category][months.index(month)] += amount

            # Create figure
            figure = Figure(figsize=(6, 4))
            canvas = FigureCanvas(figure)
            ax = figure.add_subplot(111)

            bottom_values = [0] * len(months)
            for category, expenses in category_expenses.items():
                ax.bar(months, expenses, bottom=bottom_values, label=category)
                bottom_values = [sum(x) for x in zip(bottom_values, expenses)]

            ax.set_title("Category-Wise Monthly Expenses", fontsize=14, fontweight="bold")
            ax.set_xlabel("Month", fontsize=12)
            ax.set_ylabel("Expenses ($)", fontsize=12)
            ax.legend()

            # Add canvas to the layout
            layout = self.stackedGraphView.layout()
            if layout is None:
                layout = QVBoxLayout(self.stackedGraphView)
                self.stackedGraphView.setLayout(layout)

            for i in reversed(range(layout.count())):
                widget = layout.itemAt(i).widget()
                if widget:
                    widget.setParent(None)

            layout.addWidget(canvas)
            print("DEBUG: Stacked bar chart generated successfully.")

        except sqlite3.DatabaseError as e:
            QtWidgets.QMessageBox.warning(None, "Database Error", f"Failed to load stacked bar chart data: {e}")
        except Exception as e:
            QtWidgets.QMessageBox.warning(None, "Error", f"An unexpected error occurred: {e}")




    def generate_bar_chart_page2(self):
        """Generate a bar chart for total expenses by category."""
        try:
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()

            # Fetch total expenses per category
            cursor.execute("""
                SELECT c.category, COALESCE(SUM(e.amount), 0)
                FROM categories c
                LEFT JOIN expenses e ON c.id = e.category_id
                GROUP BY c.id
            """)
            data = cursor.fetchall()
            connection.close()

            # Ensure there are at least two categories with expenses
            valid_data = [(category, exp) for category, exp in data if exp > 0]
            if len(valid_data) < 2:
                QtWidgets.QMessageBox.information(None, "Missing Data", "You need at least two categories with expenses for this chart to work.")
                return

            categories, expenses = zip(*valid_data)

            # Create figure
            figure = Figure(figsize=(6, 4))
            canvas = FigureCanvas(figure)
            ax = figure.add_subplot(111)

            # Plot bar chart
            ax.bar(categories, expenses, color="blue")
            ax.set_title("Total Expenses by Category", fontsize=14, fontweight="bold")
            ax.set_xlabel("Category", fontsize=12)
            ax.set_ylabel("Expenses ($)", fontsize=12)

            # Add canvas to the layout
            layout = self.BarViewAll.layout()
            if layout is None:
                layout = QVBoxLayout(self.BarViewAll)
                self.BarViewAll.setLayout(layout)

            for i in reversed(range(layout.count())):
                widget = layout.itemAt(i).widget()
                if widget:
                    widget.setParent(None)

            layout.addWidget(canvas)
            print("DEBUG: Bar chart successfully generated.")

        except sqlite3.DatabaseError as e:
            QtWidgets.QMessageBox.warning(None, "Database Error", f"Failed to load bar chart data: {e}")
        except Exception as e:
            QtWidgets.QMessageBox.warning(None, "Error", f"An unexpected error occurred: {e}")




    def generate_bar_chart(self):
        """Generate a bar chart for total expenses across categories."""
        try:
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()

            # Fetch category-wise expenses
            cursor.execute("""
                SELECT c.category, SUM(e.amount) AS total_expense
                FROM categories c
                LEFT JOIN expenses e ON c.id = e.category_id
                GROUP BY c.category
            """)
            data = cursor.fetchall()
            connection.close()

            # Prepare data
            categories = [row[0] for row in data]
            expenses = [row[1] for row in data]

            if not categories or not expenses:
                QtWidgets.QMessageBox.information(None, "No Data", "No data to display in the bar chart.")
                return

            # Create the figure
            figure = Figure(figsize=(5.5, 5.5))
            canvas = FigureCanvas(figure)
            ax = figure.add_subplot(111)

            # Plot bar chart
            ax.bar(categories, expenses, color="green")
            ax.set_title("Total Expenses by Category", fontsize=14, fontweight="bold")
            ax.set_xlabel("Category", fontsize=12)
            ax.set_ylabel("Expenses ($)", fontsize=12)
            ax.tick_params(axis="x", rotation=45)

            # Clear and add the chart to the layout
            layout = self.BarViewAll.layout()
            if layout is None:
                layout = QVBoxLayout(self.BarViewAll)
                self.BarViewAll.setLayout(layout)

            for i in reversed(range(layout.count())):
                widget = layout.itemAt(i).widget()
                if widget:
                    widget.setParent(None)

            layout.addWidget(canvas)
            print("DEBUG: Bar chart successfully rendered.")

        except sqlite3.DatabaseError as e:
            QtWidgets.QMessageBox.warning(None, "Database Error", f"Failed to load data for the bar chart: {e}")

    def generate_pie_chart_page2(self):
        """Generate a pie chart for expenses and render it in the PieChartView on Page 2."""
        try:
            # Connect to the database
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()

            # Fetch data for the pie chart
            cursor.execute("""
                SELECT c.category, COALESCE(SUM(e.amount), 0) AS total_expense
                FROM categories c
                LEFT JOIN expenses e ON c.id = e.category_id
                GROUP BY c.id
            """)
            data = cursor.fetchall()
            connection.close()

            # Prepare labels and values
            labels = [row[0] for row in data]
            values = [row[1] for row in data]
            filtered_data = [(label, value) for label, value in zip(labels, values) if value > 0]
            if not filtered_data:
                QtWidgets.QMessageBox.information(None, "No Data", "No expenses to display in the pie chart.")
                return

            labels, values = zip(*filtered_data)
            pastel_colors = ["#FFB3BA", "#FFDFBA", "#FFFFBA", "#BAFFC9", "#BAE1FF", "#D5BAFF"] * (len(labels) // 6 + 1)

            # Create the figure
            figure = Figure(figsize=(5.5, 5.5))
            canvas = FigureCanvas(figure)
            ax = figure.add_subplot(111)

            # Plot pie chart
            ax.pie(
                values,
                labels=labels,
                autopct="%1.1f%%",
                startangle=90,
                textprops={"fontsize": 14},
                colors=pastel_colors[:len(labels)],
                labeldistance=1.1
            )
            ax.axis("equal")

            # Clear existing widgets in the PieChartView layout
            layout = self.PieChartView.layout()
            if layout is None:
                layout = QVBoxLayout(self.PieChartView)
                self.PieChartView.setLayout(layout)

            for i in reversed(range(layout.count())):
                widget = layout.itemAt(i).widget()
                if widget:
                    widget.setParent(None)

            # Add the canvas to the layout
            layout.addWidget(canvas)
            print("Pie chart updated successfully for Page 2!")

        except sqlite3.DatabaseError as e:
            QtWidgets.QMessageBox.warning(None, "Database Error", f"Failed to load pie chart data: {e}")
        except Exception as e:
            QtWidgets.QMessageBox.warning(None, "Error", f"An unexpected error occurred: {e}")


    def setupUi(self, MainWindow):
        try:
            with open("db_path.txt", "r") as file:
                self.db_path = file.read().strip()
            print(f"DEBUG: Loaded database path: {self.db_path}")
        except FileNotFoundError:
            QMessageBox.warning(None, "No Database Selected", "Please select a valid database first.")
            return

        from PyQt5 import QtCore
        
        

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1920, 1080)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 1920, 1050))
        font = QtGui.QFont()
        font.setFamily("White Rabbit")
        font.setPointSize(20)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        font.setKerning(True)
        # Tab Widget
        self.tabWidget.setFont(font)
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.South)
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Triangular)
        self.tabWidget.setUsesScrollButtons(True)
        self.tabWidget.setDocumentMode(False)
        self.tabWidget.setTabsClosable(False)
        self.tabWidget.setMovable(False)
        self.tabWidget.setTabBarAutoHide(False)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")

        #######################################################################################################################################################
        #######################################################################################################################################################
        #######################################################################################################################################################
        # Budget Summary
        self.tableWidget = QtWidgets.QTableWidget(self.tab)
        self.tableWidget.setGeometry(QtCore.QRect(20, 100, 800, 850))
        font = QtGui.QFont()
        font.setFamily("White Rabbit")
        font.setPointSize(12)
        self.tableWidget.setFont(font)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(1)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        self.PieChart = QtWidgets.QGraphicsView(self.tab)
        self.PieChart.setGeometry(QtCore.QRect(850, 100, 550, 550))
        self.PieChart.setObjectName("PieChart")
        self.BarChart = QtWidgets.QGraphicsView(self.tab)
        self.BarChart.setGeometry(QtCore.QRect(1425, 100, 475, 550))
        self.BarChart.setObjectName("BarChart")
        self.Header = QtWidgets.QGraphicsView(self.tab)
        self.Header.setGeometry(QtCore.QRect(0, 0, 1920, 64))
        self.Header.setObjectName("Header")
        self.Summary = QtWidgets.QGraphicsView(self.tab)
        self.Summary.setGeometry(QtCore.QRect(850, 675, 1050, 275))
        self.Summary.setObjectName("Summary")
        self.BarTabView = QtWidgets.QTabWidget(self.tab)
        self.BarTabView.setGeometry(QtCore.QRect(1425, 100, 475, 550))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.BarTabView.setFont(font)
        self.BarTabView.setDocumentMode(False)
        self.BarTabView.setMovable(True)
        self.BarTabView.setTabBarAutoHide(False)
        self.BarTabView.setObjectName("BarTabView")
        self.tab_6 = QtWidgets.QWidget()
        self.tab_6.setObjectName("tab_6")
        self.smallbarChart = QtWidgets.QGraphicsView(self.tab_6)
        self.smallbarChart.setGeometry(QtCore.QRect(0, 0, 475, 550))
        self.smallbarChart.setObjectName("smallbarChart")
        self.BarTabView.addTab(self.tab_6, "")
        self.tab_7 = QtWidgets.QWidget()
        self.tab_7.setObjectName("tab_7")
        self.smallbarChart_2 = QtWidgets.QGraphicsView(self.tab_7)
        self.smallbarChart_2.setGeometry(QtCore.QRect(0, 0, 475, 550))
        self.smallbarChart_2.setObjectName("smallbarChart_2")
        self.BarTabView.addTab(self.tab_7, "")
        self.tIncome = QtWidgets.QLabel(self.tab)
        self.tIncome.setGeometry(QtCore.QRect(870, 685, 1000, 65))
        self.tIncome.setObjectName("tIncome")
        self.tExpenses = QtWidgets.QLabel(self.tab)
        self.tExpenses.setGeometry(QtCore.QRect(870, 735, 1000, 65))
        self.tExpenses.setObjectName("tExpenses")
        self.remBal = QtWidgets.QLabel(self.tab)
        self.remBal.setGeometry(QtCore.QRect(870, 815, 1000, 65))
        self.remBal.setObjectName("remBal")
        self.divider = QtWidgets.QFrame(self.tab)
        self.divider.setGeometry(QtCore.QRect(870, 800, 1000, 2))
        self.divider.setFrameShape(QtWidgets.QFrame.Box)
        self.divider.setFrameShadow(QtWidgets.QFrame.Plain)
        self.divider.setLineWidth(7)
        self.divider.setObjectName("divider")
        self.statusLabel = QtWidgets.QLabel(self.tab)
        self.statusLabel.setGeometry(QtCore.QRect(870, 865, 250, 65))
        self.statusLabel.setObjectName("statusLabel")
        self.statusChangeable = QtWidgets.QLabel(self.tab)
        self.statusChangeable.setGeometry(QtCore.QRect(1050, 865, 400, 65))
        self.statusChangeable.setObjectName("statusChangeable")
        self.Date = QtWidgets.QLabel(self.tab)
        self.Date.setGeometry(QtCore.QRect(10, 0, 1920, 64))
        self.Date.setObjectName("Date")
        self.tabWidget.addTab(self.tab, "")

        #######################################################################################################################################################
        #######################################################################################################################################################
        #######################################################################################################################################################
        # Tab 2
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.Header_2 = QtWidgets.QGraphicsView(self.tab_2)
        self.Header_2.setGeometry(QtCore.QRect(0, 0, 1920, 64))
        self.Header_2.setObjectName("Header_2")
        self.BarViewAll = QtWidgets.QGraphicsView(self.tab_2)
        self.BarViewAll.setGeometry(QtCore.QRect(150, 100, 900, 425))
        self.BarViewAll.setObjectName("BarViewAll")
        self.PieChartView = QtWidgets.QGraphicsView(self.tab_2)
        self.PieChartView.setGeometry(QtCore.QRect(1200, 100, 450, 425))
        self.PieChartView.setObjectName("PieChartView")
        self.Date_2 = QtWidgets.QLabel(self.tab_2)
        self.Date_2.setGeometry(QtCore.QRect(10, 0, 1920, 64))
        self.Date_2.setObjectName("Date_2")
        self.LineGraphView = QtWidgets.QGraphicsView(self.tab_2)
        self.LineGraphView.setGeometry(QtCore.QRect(150, 550, 900, 425))
        self.LineGraphView.setObjectName("LineGraphView")
        self.stackedGraphView = QtWidgets.QGraphicsView(self.tab_2)
        self.stackedGraphView.setGeometry(QtCore.QRect(1200, 550, 450, 425))
        self.stackedGraphView.setObjectName("stackedGraphView")
        self.tabWidget.addTab(self.tab_2, "")

        # Tab 3
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.Header_3 = QtWidgets.QGraphicsView(self.tab_3)
        self.Header_3.setGeometry(QtCore.QRect(0, 0, 1920, 64))
        self.Header_3.setObjectName("Header_3")
        self.date = QtWidgets.QLabel(self.tab_3)
        self.date.setGeometry(QtCore.QRect(10, 0, 1920, 64))
        self.date.setObjectName("date")
        self.confirm = QtWidgets.QPushButton(self.tab_3)
        self.confirm.setGeometry(QtCore.QRect(100, 760, 400, 40))
        self.confirm.setObjectName("confirm")
        self.monthSelect = QtWidgets.QComboBox(self.tab_3)
        self.monthSelect.setGeometry(QtCore.QRect(100, 125, 300, 40))
        self.monthSelect.setObjectName("monthSelect")
        self.p1 = QtWidgets.QLabel(self.tab_3)
        self.p1.setGeometry(QtCore.QRect(100, 75, 600, 40))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.p1.setFont(font)
        self.p1.setObjectName("p1")
        self.p2 = QtWidgets.QLabel(self.tab_3)
        self.p2.setGeometry(QtCore.QRect(100, 200, 600, 40))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.p2.setFont(font)
        self.p2.setObjectName("p2")
        self.catSelect = QtWidgets.QComboBox(self.tab_3)
        self.catSelect.setGeometry(QtCore.QRect(100, 250, 300, 40))
        self.catSelect.setObjectName("catSelect")
        self.catSelect.addItem("")
        self.catSelect.setItemText(0, "")
        self.lineEdit = QtWidgets.QLineEdit(self.tab_3)
        self.lineEdit.setGeometry(QtCore.QRect(100, 325, 300, 40))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(12)
        self.lineEdit.setFont(font)
        self.lineEdit.setObjectName("lineEdit")
        self.checkBox = QtWidgets.QCheckBox(self.tab_3)
        self.checkBox.setGeometry(QtCore.QRect(100, 400, 300, 40))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.checkBox.setFont(font)
        self.checkBox.setObjectName("checkBox")
        self.p2_2 = QtWidgets.QLabel(self.tab_3)
        self.p2_2.setGeometry(QtCore.QRect(100, 485, 400, 40))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.p2_2.setFont(font)
        self.p2_2.setObjectName("p2_2")
        self.comboBox = QtWidgets.QComboBox(self.tab_3)
        self.comboBox.setGeometry(QtCore.QRect(100, 525, 300, 40))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(12)
        self.comboBox.setFont(font)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.checkBox_2 = QtWidgets.QCheckBox(self.tab_3)
        self.checkBox_2.setGeometry(QtCore.QRect(100, 435, 650, 40))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.checkBox_2.setFont(font)
        self.checkBox_2.setObjectName("checkBox_2")
        self.comboBox_2 = QtWidgets.QComboBox(self.tab_3)
        self.comboBox_2.setGeometry(QtCore.QRect(100, 635, 300, 40))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(12)
        self.comboBox_2.setFont(font)
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.p2_3 = QtWidgets.QLabel(self.tab_3)
        self.p2_3.setGeometry(QtCore.QRect(100, 575, 326, 40))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.p2_3.setFont(font)
        self.p2_3.setObjectName("p2_3")
        self.label = QtWidgets.QLabel(self.tab_3)
        self.label.setGeometry(QtCore.QRect(100, 840, 800, 40))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.tab_3)
        self.label_2.setGeometry(QtCore.QRect(100, 890, 500, 40))
        self.label_2.setObjectName("label_2")
        # Income entry section 

        self.p1_2 = QtWidgets.QLabel(self.tab_3)
        self.p1_2.setGeometry(QtCore.QRect(800, 75, 600, 40))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.p1_2.setFont(font)
        self.p1_2.setObjectName("p1_2")
        self.monthSelect_3 = QtWidgets.QComboBox(self.tab_3)
        self.monthSelect_3.setGeometry(QtCore.QRect(800, 125, 300, 40))
        self.monthSelect_3.setObjectName("monthSelect_3")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.tab_3)
        self.lineEdit_3.setGeometry(QtCore.QRect(800, 325, 300, 40))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(12)
        self.lineEdit_3.setFont(font)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.income2Value = QtWidgets.QLabel(self.tab_3)
        self.income2Value.setGeometry(QtCore.QRect(800, 200, 336, 40))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.income2Value.setFont(font)
        self.income2Value.setObjectName("income2Value")
        self.addOtherIncome = QtWidgets.QPushButton(self.tab_3)
        self.addOtherIncome.setGeometry(QtCore.QRect(800, 635, 400, 40))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.addOtherIncome.setFont(font)
        self.addOtherIncome.setObjectName("addOtherIncome")
        self.comboBox_3 = QtWidgets.QComboBox(self.tab_3)
        self.comboBox_3.setGeometry(QtCore.QRect(800, 525, 300, 40))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(12)
        self.comboBox_3.setFont(font)
        self.comboBox_3.setObjectName("comboBox_3")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.p2_4 = QtWidgets.QLabel(self.tab_3)
        self.p2_4.setGeometry(QtCore.QRect(800, 485, 400, 40))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.p2_4.setFont(font)
        self.p2_4.setObjectName("p2_4")
        self.lineEdit_4 = QtWidgets.QLineEdit(self.tab_3)
        self.lineEdit_4.setGeometry(QtCore.QRect(800, 250, 300, 40))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(12)
        self.lineEdit_4.setFont(font)
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.checkBox_3 = QtWidgets.QCheckBox(self.tab_3)
        self.checkBox_3.setGeometry(QtCore.QRect(800, 400, 300, 40))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.checkBox_3.setFont(font)
        self.checkBox_3.setObjectName("checkBox_3")
        self.confirm_2 = QtWidgets.QPushButton(self.tab_3)
        self.confirm_2.setGeometry(QtCore.QRect(800, 760, 400, 40))
        self.confirm_2.setObjectName("confirm_2")
        self.label_3 = QtWidgets.QLabel(self.tab_3)
        self.label_3.setGeometry(QtCore.QRect(800, 840, 700, 40))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.tab_3)
        self.label_4.setGeometry(QtCore.QRect(800, 890, 800, 40))
        self.label_4.setObjectName("label_4")
        self.tabWidget.addTab(self.tab_3, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionNew_File = QtWidgets.QAction(MainWindow)
        self.actionNew_File.setObjectName("actionNew_File")
        self.actionClose = QtWidgets.QAction(MainWindow)
        self.actionClose.setObjectName("actionClose")
        self.actionClose_2 = QtWidgets.QAction(MainWindow)
        self.actionClose_2.setObjectName("actionClose_2")
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        self.BarTabView.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        ###################################################################
        # functions
        
        # Updates today's date and visualized month
        today = datetime.now()
        formatted_today = today.strftime("%d %B, %Y")
        visualizing_month = today.strftime("%B")
        visualizing_year = today.year

        self.Date.setText(f"Today is {formatted_today} || Visualizing: {visualizing_month} {visualizing_year}")
        self.Date_2.setText(f"Today is {formatted_today} || Visualizing: {visualizing_month} {visualizing_year}")

        self.date.setText(f"Today is {formatted_today}")


        


        

        self.load_categories()
        self.addOtherIncome.clicked.connect(self.add_other_income)
        self.comboBox.setCurrentIndex(3)  # Default to "Monthly"
        self.comboBox_2.setCurrentIndex(0)  # Default to "Credit/Debit Card"
        self.comboBox_3.setCurrentIndex(3)
        
        def populate_last_six_months():
            """Populate the monthSelect and monthSelect_3 combo boxes with the current and past 5 months."""
            try:
                # Generate the last 6 months
                months = []
                current_date = datetime.now()
                for i in range(6):  # Current month + 5 previous months
                    month_year = (current_date - relativedelta(months=i)).strftime("%B %Y")
                    months.append(month_year)

                # Populate monthSelect
                self.monthSelect.clear()
                self.monthSelect.addItems(months)
                self.monthSelect.setCurrentIndex(0)  # Set the current month as default

                # Populate monthSelect_3
                self.monthSelect_3.clear()
                self.monthSelect_3.addItems(months)
                self.monthSelect_3.setCurrentIndex(0)  # Set the current month as default

                print(f"Months loaded into combo boxes: {months}")
            except Exception as e:
                QMessageBox.critical(None, "Error", f"Failed to populate months: {e}")
            
        def populate_categories():
            """Populate the catSelect combo box with all categories stored in the database."""
            try:
                # Connect to the database
                connection = sqlite3.connect(self.db_path)
                cursor = connection.cursor()

                # Fetch all categories for the current budget
                cursor.execute("SELECT category FROM categories")
                categories = cursor.fetchall()

                # Ensure no duplicates and remove any unnecessary structures
                category_names = [category[0] for category in categories]

                # Populate catSelect
                self.catSelect.clear()
                self.catSelect.addItems(category_names)

                print(f"Categories loaded into combo box: {category_names}")
                connection.close()
            except sqlite3.DatabaseError as e:
                QMessageBox.critical(None, "Database Error", f"Failed to load categories: {e}")
            except Exception as e:
                QMessageBox.critical(None, "Error", f"Unexpected error occurred while loading categories: {e}")
        
        
        populate_last_six_months()  # Populate month combo boxes
        populate_categories() 

        def set_combobox_font(combo_box, font_size=12):
            font = QtGui.QFont()
            font.setPointSize(font_size)
            combo_box.setFont(font)
        set_combobox_font(self.monthSelect)
        set_combobox_font(self.monthSelect_3)
        set_combobox_font(self.catSelect)
        
        ##############
        



        self.confirm.clicked.connect(self.update_expense)
        self.calculate_progress()
        self.generate_pie_chart()
        self.generate_category_bar_charts()
        self.confirm_2.clicked.connect(self.update_income)
        self.reset_monthly_expenses()
        self.notify_reminders()
        self.generate_line_chart()
        self.generate_stacked_bar_chart()
        self.generate_bar_chart_page2()
        self.generate_pie_chart_page2()



    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        item = self.tableWidget.verticalHeaderItem(0)
        item.setText(_translate("MainWindow", ""))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Cost"))
        self.BarTabView.setTabText(self.BarTabView.indexOf(self.tab_6), _translate("MainWindow", "Tab 1"))
        self.BarTabView.setTabText(self.BarTabView.indexOf(self.tab_7), _translate("MainWindow", "Tab 2"))
        self.tIncome.setText(_translate("MainWindow", "Total Income:"))
        self.tExpenses.setText(_translate("MainWindow", "Total Expenses:"))
        self.remBal.setText(_translate("MainWindow", "Remaining Balance:"))
        self.statusLabel.setText(_translate("MainWindow", "Status:"))
        self.statusChangeable.setText(_translate("MainWindow", "statusR"))
        self.Date.setText(_translate("MainWindow", "Today is"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Budget Summary"))
        self.Date_2.setText(_translate("MainWindow", "Today is"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Chart View"))
        self.date.setText(_translate("MainWindow", "Today is"))
        self.confirm.setText(_translate("MainWindow", "Confirm"))
        self.p1.setText(_translate("MainWindow", "Select Month to edit expenses"))
        self.p2.setText(_translate("MainWindow", "Select Category to edit"))
        self.lineEdit.setPlaceholderText(_translate("MainWindow", "Input Expense Value"))
        self.checkBox.setText(_translate("MainWindow", "Constant?"))
        self.p2_2.setText(_translate("MainWindow", "Frequency of Expense"))
        self.comboBox.setItemText(0, _translate("MainWindow", "One-Time"))
        self.comboBox.setItemText(1, _translate("MainWindow", "Weekly"))
        self.comboBox.setItemText(2, _translate("MainWindow", "Bi-weekly"))
        self.comboBox.setItemText(3, _translate("MainWindow", "Monthly (Default)"))
        self.comboBox.setItemText(4, _translate("MainWindow", "Quarterly"))
        self.comboBox.setItemText(5, _translate("MainWindow", "Annually"))
        self.checkBox_2.setText(_translate("MainWindow", "Remind me about this expense"))
        self.comboBox_2.setItemText(0, _translate("MainWindow", "Credit/Debit Card"))
        self.comboBox_2.setItemText(1, _translate("MainWindow", "Cash"))
        self.comboBox_2.setItemText(2, _translate("MainWindow", "Bank Transfer"))
        self.comboBox_2.setItemText(3, _translate("MainWindow", "Other"))
        self.p2_3.setText(_translate("MainWindow", "How was this paid?"))
        self.label.setText(_translate("MainWindow", "Expenses missing:"))
        self.label_2.setText(_translate("MainWindow", "Progress:"))
        self.p1_2.setText(_translate("MainWindow", "Select Month to edit income"))
        self.lineEdit_3.setPlaceholderText(_translate("MainWindow", "Input Income Value"))
        self.income2Value.setText(_translate("MainWindow", "Edit Income"))
        self.addOtherIncome.setText(_translate("MainWindow", "Add Another Income Source"))
        self.comboBox_3.setItemText(0, _translate("MainWindow", "One-Time"))
        self.comboBox_3.setItemText(1, _translate("MainWindow", "Weekly"))
        self.comboBox_3.setItemText(2, _translate("MainWindow", "Bi-weekly"))
        self.comboBox_3.setItemText(3, _translate("MainWindow", "Monthly (Default)"))
        self.comboBox_3.setItemText(4, _translate("MainWindow", "Quarterly"))
        self.comboBox_3.setItemText(5, _translate("MainWindow", "Annually"))
        self.p2_4.setText(_translate("MainWindow", "Frequency of Income"))
        self.lineEdit_4.setPlaceholderText(_translate("MainWindow", "Source of Income"))
        self.checkBox_3.setText(_translate("MainWindow", "Constant?"))
        self.confirm_2.setText(_translate("MainWindow", "Confirm"))
        self.label_3.setText(_translate("MainWindow", "Total Income:"))
        self.label_4.setText(_translate("MainWindow", "Number of incomes:"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "Data Entry"))
        self.actionNew_File.setText(_translate("MainWindow", "New File"))
        self.actionClose.setText(_translate("MainWindow", "Close"))
        self.actionClose_2.setText(_translate("MainWindow", "Close"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui3 = Ui_MainWindow3()
    ui3.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

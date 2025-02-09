import sqlite3
import hashlib
from datetime import datetime

class DatabaseHandler:
    def __init__(self, db_file="budgets.db"):
        self.db_file = db_file
        self.create_database()

    def create_database(self):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        # Budgets Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS budgets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                income REAL DEFAULT 0.0
            )
        """)

        # Income Sources Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS income_sources (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                budget_id INTEGER NOT NULL,
                source_name TEXT NOT NULL,
                amount REAL DEFAULT 0.0,
                is_main BOOLEAN DEFAULT 0,
                is_constant BOOLEAN DEFAULT 0,
                frequency TEXT DEFAULT 'Monthly',
                FOREIGN KEY (budget_id) REFERENCES budgets(id),
                UNIQUE (budget_id, source_name)
            )
        """)

        # Categories Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                budget_id INTEGER NOT NULL,
                category TEXT NOT NULL,
                FOREIGN KEY (budget_id) REFERENCES budgets(id),
                UNIQUE (budget_id, category)
            )
        """)

        # Expenses Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                budget_id INTEGER NOT NULL,
                category_id INTEGER NOT NULL,
                amount REAL DEFAULT 0.0,
                month TEXT NOT NULL,
                is_constant BOOLEAN DEFAULT 0,
                remind BOOLEAN DEFAULT 0,
                frequency TEXT DEFAULT 'Monthly',
                payment_method TEXT DEFAULT 'Credit/Debit Card',
                FOREIGN KEY (budget_id) REFERENCES budgets(id),
                FOREIGN KEY (category_id) REFERENCES categories(id),
                UNIQUE (budget_id, category_id, month)
            )
        """)

        # Password Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS password (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                budget_id INTEGER NOT NULL,
                hash TEXT NOT NULL,
                FOREIGN KEY (budget_id) REFERENCES budgets(id) ON DELETE CASCADE,
                UNIQUE (budget_id)
            )
        """)

        # Ensure the `frequency` column exists in `income_sources`
        cursor.execute("PRAGMA table_info(income_sources)")
        income_sources_columns = [col[1] for col in cursor.fetchall()]
        if "frequency" not in income_sources_columns:
            cursor.execute("ALTER TABLE income_sources ADD COLUMN frequency TEXT DEFAULT 'Monthly'")

        # Ensure new columns exist in the `expenses` table
        self.ensure_expenses_columns(cursor)

        conn.commit()
        conn.close()

    def ensure_expenses_columns(self, cursor):
        """Ensure that the required columns are in the expenses table."""
        cursor.execute("PRAGMA table_info(expenses)")
        existing_columns = [col[1] for col in cursor.fetchall()]

        # Add missing columns if they do not exist
        if "is_constant" not in existing_columns:
            cursor.execute("ALTER TABLE expenses ADD COLUMN is_constant BOOLEAN DEFAULT 0")
        if "remind" not in existing_columns:
            cursor.execute("ALTER TABLE expenses ADD COLUMN remind BOOLEAN DEFAULT 0")
        if "frequency" not in existing_columns:
            cursor.execute("ALTER TABLE expenses ADD COLUMN frequency TEXT DEFAULT 'Monthly'")
        if "payment_method" not in existing_columns:
            cursor.execute("ALTER TABLE expenses ADD COLUMN payment_method TEXT DEFAULT 'Credit/Debit Card'")

    # ----------------- PASSWORD SYSTEM -----------------
    def set_password(self, password, budget_id):
        hashed_password = self.hash_password(password)
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        try:
            # Insert or update the password for the given budget_id
            cursor.execute("""
                INSERT INTO password (budget_id, hash) 
                VALUES (?, ?)
                ON CONFLICT(budget_id) DO UPDATE SET hash = excluded.hash
            """, (budget_id, hashed_password))
            conn.commit()
        except sqlite3.DatabaseError as e:
            raise Exception(f"Failed to set password: {e}")
        finally:
            conn.close()

    def verify_password(self, budget_id, password):
        """Check if the entered password matches the stored hashed password for a specific budget."""
        hashed_password = self.hash_password(password)
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        cursor.execute("SELECT hash FROM password WHERE budget_id = ?", (budget_id,))
        stored_password = cursor.fetchone()

        conn.close()
        return stored_password and stored_password[0] == hashed_password

    def hash_password(self, password):
        """Hash the password using sha256."""
        hashed = hashlib.sha256(password.encode()).hexdigest()
        return hashed

    # ----------------- BUDGET SYSTEM -----------------
    def add_budget(self, name, income=0.0):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO budgets (name, income) VALUES (?, ?)", (name, income))
            budget_id = cursor.lastrowid
            conn.commit()
            return budget_id
        except sqlite3.IntegrityError:
            raise ValueError("Budget name already exists.")
        finally:
            conn.close()

    def update_expense(self, budget_id, category_id, amount, month, is_constant, remind, frequency, payment_method):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO expenses (budget_id, category_id, amount, month, is_constant, remind, frequency, payment_method) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT (budget_id, category_id, month) DO UPDATE 
                SET amount = excluded.amount,
                    is_constant = excluded.is_constant,
                    remind = excluded.remind,
                    frequency = excluded.frequency,
                    payment_method = excluded.payment_method
            """, (budget_id, category_id, amount, month, is_constant, remind, frequency, payment_method))
            conn.commit()
        except sqlite3.DatabaseError as e:
            raise Exception(f"Failed to update expense: {e}")
        finally:
            conn.close()


    # Retrieve expenses for a specific month
    def get_expenses_for_month(self, budget_id, month):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT c.category, e.amount 
            FROM expenses e
            JOIN categories c ON e.category_id = c.id
            WHERE e.budget_id = ? AND e.month = ?
        """, (budget_id, month))
        expenses = cursor.fetchall()
        conn.close()
        return expenses

    # Delete a budget
    def delete_budget(self, budget_id):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM expenses WHERE budget_id = ?", (budget_id,))
        cursor.execute("DELETE FROM categories WHERE budget_id = ?", (budget_id,))
        cursor.execute("DELETE FROM income_sources WHERE budget_id = ?", (budget_id,))
        cursor.execute("DELETE FROM budgets WHERE id = ?", (budget_id,))
        conn.commit()
        conn.close()

    def add_categories(self, budget_id, categories):
        """Add categories to the database for a specific budget."""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        try:
            for category in categories:
                cursor.execute(
                    "INSERT OR IGNORE INTO categories (budget_id, category) VALUES (?, ?)",
                    (budget_id, category)
                )
            conn.commit()
            print(f"DEBUG: Categories added for budget_id {budget_id}: {categories}")
        except sqlite3.DatabaseError as e:
            raise Exception(f"Failed to add categories: {e}")
        finally:
            conn.close()

# Example usage
if __name__ == "__main__":
    db = DatabaseHandler()

    # Create a new budget
    budget_id = db.add_budget("Family Budget", income=3000)

    # Add income sources
    db.add_income_source(budget_id, "Salary", 3000, is_main=True)
    db.add_income_source(budget_id, "Freelance", 1500)
    db.add_income_source(budget_id, "Investments", 800)
    db.add_income_source(budget_id, "Other", 300)

    # Fetch income sources
    income_sources = db.get_income_sources(budget_id)
    print("Income Sources:", income_sources)

    # Fetch budget and total income
    budget, total_income = db.get_budget_with_income(budget_id)
    print(f"Budget: {budget}")
    print(f"Total Income: {total_income}")

    # Setting a password (only runs once)
    try:
        db.set_password("my_secure_password")
        print("Password set successfully!")
    except ValueError:
        print("Password already exists.")

    # Verifying password
    if db.verify_password("my_secure_password"):
        print("Password verification successful!")
    else:
        print("Password incorrect!")

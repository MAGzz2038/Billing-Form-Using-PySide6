from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QComboBox, QTextEdit, QTableWidget, QTableWidgetItem
import mysql.connector
import sys

class BillingForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Billing Form")
        self.setGeometry(100, 100, 600, 700)

        layout = QVBoxLayout()

        # CUSTOMER ENTRY
        layout.addWidget(QLabel("Add Customer"))
        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("Enter Name")
        self.phone_input = QLineEdit(self)
        self.phone_input.setPlaceholderText("Enter Phone Number")
        self.email_input = QLineEdit(self)
        self.email_input.setPlaceholderText("Enter Email")
        self.city_input = QLineEdit(self)
        self.city_input.setPlaceholderText("Enter City")
        self.state_input = QLineEdit(self)
        self.state_input.setPlaceholderText("Enter State")
        self.zip_input = QLineEdit(self)
        self.zip_input.setPlaceholderText("Enter Zip Code")
        self.add_customer_btn = QPushButton("Add Customer")
        self.add_customer_btn.clicked.connect(self.add_customer)
        layout.addWidget(self.name_input)
        layout.addWidget(self.phone_input)
        layout.addWidget(self.email_input)
        layout.addWidget(self.city_input)
        layout.addWidget(self.state_input)
        layout.addWidget(self.zip_input)
        layout.addWidget(self.add_customer_btn)

        # BILL ENTRY
        layout.addWidget(QLabel("Create Bill"))
        self.customer_id_input = QLineEdit(self)
        self.customer_id_input.setPlaceholderText("Enter Customer ID")
        self.amount_input = QLineEdit(self)
        self.amount_input.setPlaceholderText("Enter Total Amount")
        self.payment_method = QComboBox(self)
        self.payment_method.addItems(["Cash", "Credit Card", "UPI"])
        self.status = QComboBox(self)
        self.status.addItems(["Paid", "Unpaid", "Pending"])
        self.notes_input = QTextEdit(self)
        self.notes_input.setPlaceholderText("Enter Additional Notes")
        self.add_bill_btn = QPushButton("Add Bill")
        self.add_bill_btn.clicked.connect(self.add_bill)
        layout.addWidget(self.customer_id_input)
        layout.addWidget(self.amount_input)
        layout.addWidget(self.payment_method)
        layout.addWidget(self.status)
        layout.addWidget(self.notes_input)
        layout.addWidget(self.add_bill_btn)

        # DATA RETRIEVAL
        layout.addWidget(QLabel("List of Customers"))
        self.customer_table = QTableWidget()
        self.customer_table.setColumnCount(6)
        self.customer_table.setHorizontalHeaderLabels(["ID", "Name", "Phone", "Email", "City", "State", "Zip"])
        self.load_customers()
        layout.addWidget(self.customer_table)

        layout.addWidget(QLabel("Stored Bills"))
        self.bill_table = QTableWidget()
        self.bill_table.setColumnCount(6)
        self.bill_table.setHorizontalHeaderLabels(["ID", "Customer ID", "Total Amount", "Payment Method", "Status", "Bill Date"])
       
        layout.addWidget(self.bill_table)
        self.load_bills()

        self.setLayout(layout)

    def add_customer(self):
        name = self.name_input.text()
        phone = self.phone_input.text()
        email = self.email_input.text()
        city = self.city_input.text()
        state = self.state_input.text()
        zip_code = self.zip_input.text()
        if not name or not phone or not email or not city or not state or not zip_code:
            QMessageBox.warning(self, "Error", "All customer fields are required!")
            return
        try:
            db = mysql.connector.connect(host="localhost", user="root", password="0000Anmol0000", database="billing_form")
            cursor = db.cursor()
            cursor.execute("INSERT INTO customers (name, phone, email, city, state, zip_code) VALUES (%s, %s, %s, %s, %s, %s)", (name, phone, email, city, state, zip_code))
            db.commit()
            QMessageBox.information(self, "Success", "Customer Added Successfully!")
            self.load_customers()
            cursor.close()
            db.close()
        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Database Error", f"Error: {err}")

    def add_bill(self):
        customer_id = self.customer_id_input.text()
        amount = self.amount_input.text()
        payment = self.payment_method.currentText()
        status = self.status.currentText()
        notes = self.notes_input.toPlainText()
        if not customer_id or not amount:
            QMessageBox.warning(self, "Error", "Customer ID and Amount are required!")
            return
        try:
            db = mysql.connector.connect(host="localhost", user="root", password="0000Anmol0000", database="billing_form")
            cursor = db.cursor()
            cursor.execute("INSERT INTO bills (customer_id, total_amount, payment_method, status, notes) VALUES (%s, %s, %s, %s, %s)", (customer_id, amount, payment, status, notes))
            db.commit()
            QMessageBox.information(self, "Success", "Bill Added Successfully!")
            self.load_bills()
            cursor.close()
            db.close()
        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Database Error", f"Error: {err}")

    def load_customers(self):
        self.customer_table.setRowCount(0)
        try:
            db = mysql.connector.connect(host="localhost", user="root", password="0000Anmol0000", database="billing_form")
            cursor = db.cursor()
            cursor.execute("SELECT id, name, phone, email, city, state, zip_code FROM customers")
            for row, data in enumerate(cursor.fetchall()):
                self.customer_table.insertRow(row)
                for col, value in enumerate(data):
                    self.customer_table.setItem(row, col, QTableWidgetItem(str(value)))
            cursor.close()
            db.close()
        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Database Error", f"Error: {err}")

    def load_bills(self):
        try:
            conn = mysql.connector.connect(host="localhost", user="root", password="0000Anmol0000", database="billing_form")
            cursor = conn.cursor()
            cursor.execute("SELECT id, customer_id, total_amount, payment_method, status, bill_date FROM bills")
            bills = cursor.fetchall()
            cursor.close()
            conn.close()
            
            self.bill_table.setRowCount(len(bills))
            for row_idx, bill in enumerate(bills):
                for col_idx, value in enumerate(bill):
                    self.bill_table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))
        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Database Error", f"Error: {err}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BillingForm()
    window.show()
    sys.exit(app.exec())
import sqlite3
import os 
import logging

from src.models.schemas import InvoiceData

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

class DatabaseManager: 

    def __init__(self, db_path: str = "data/database.sqlite"):
        self.db_path = db_path
        self._initialize_database()

    def _initialize_database(self):
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS invoices (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    merchant_name TEXT NOT NULL,
                    merchant_cif TEXT,
                    merchant_iban TEXT,
                    client_name TEXT,
                    client_code TEXT,
                    client_address TEXT,
                    invoice_number TEXT,
                    date TEXT,
                    due_date TEXT,
                    billing_period TEXT,
                    total_amount REAL,
                    previous_balance REAL,
                    total_payable REAL,
                    currency TEXT
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS invoice_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    invoice_id INTEGER,
                    description TEXT,
                    quantity REAL,
                    unit_price REAL,
                    tax_amount REAL,
                    total_price REAL,
                    FOREIGN KEY (invoice_id) REFERENCES invoices (id)
                )
            """)

            conn.commit()
            logger.info("Database initialized successfully.")

    def save_invoice(self, invoice_data: InvoiceData):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                cursor.execute("""
                    INSERT INTO invoices (
                        merchant_name, merchant_cif, merchant_iban,
                        client_name, client_code, client_address,
                        invoice_number, date, due_date, billing_period,
                        total_amount, previous_balance, total_payable, currency
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    invoice_data.merchant_name,
                    invoice_data.merchant_cif,
                    invoice_data.merchant_iban,
                    invoice_data.client_name,
                    invoice_data.client_code,
                    invoice_data.client_address,
                    invoice_data.invoice_number,
                    invoice_data.date,
                    invoice_data.due_date,
                    invoice_data.billing_period,
                    invoice_data.total_amount,
                    invoice_data.previous_balance,
                    invoice_data.total_payable,
                    invoice_data.currency
                ))

                invoice_id = cursor.lastrowid

                for item in invoice_data.items:
                    cursor.execute("""
                        INSERT INTO invoice_items (
                            invoice_id, description, quantity, unit_price, tax_amount, total_price
                        )
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (
                        invoice_id,
                        item.description,
                        item.quantity,
                        item.unit_price,
                        item.tax_amount,
                        item.total_price
                    ))

                conn.commit()
                logger.info(f"Invoice '{invoice_data.invoice_number}' saved to database successfully.")
        except Exception as e:
            logger.error(f"Database error while saving invoice: {e}")
            raise e
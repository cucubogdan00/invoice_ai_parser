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
                    invoice_number TEXT,
                    date TEXT,
                    total_amount REAL
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS invoice_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    invoice_id INTEGER,
                    description TEXT,
                    quantity REAL,
                    unit_price REAL,
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
                    INSERT INTO invoices (merchant_name, invoice_number, date, total_amount)
                    VALUES (?, ?, ?, ?)
                """, (
                    invoice_data.merchant_name,
                    invoice_data.invoice_number,
                    invoice_data.date,
                    invoice_data.total_amount
                ))

                invoice_id = cursor.lastrowid

                for item in invoice_data.items:
                    cursor.execute("""
                        INSERT INTO invoice_items (invoice_id, description, quantity, unit_price)
                        VALUES (?, ?, ?, ?)
                    """, (
                        invoice_id,
                        item.description,
                        item.quantity,
                        item.unit_price
                    ))

                conn.commit()
                logger.info(f"Invoice '{invoice_data.invoice_number}' saved to database successfully.")
        except Exception as e:
            logger.error(f"Database error while saving invoice: {e}")
            raise e
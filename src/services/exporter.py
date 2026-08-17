import sqlite3
import pandas as pd
import logging
import os

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

class ExporterService:
    """
    Service responsible for extracting data from SQLite and 
    exporting it to standard spreadsheet formats (Excel/CSV).
    """

    def __init__(self, db_path: str = "data/database.sqlite"):
        self.db_path = db_path

    def export_to_excel(self, output_path: str = "data/invoices_export.xlsx"):
        """
        Reads invoices and their items from the database using a SQL JOIN,
        and saves them as a beautifully formatted Excel file.
        """
        if not os.path.exists(self.db_path):
            logger.error("Database not found. Nothing to export.")
            return

        try:
            with sqlite3.connect(self.db_path) as conn:
                sql_query = """
                    SELECT 
                        i.invoice_number AS 'Invoice Number',
                        i.date AS 'Date',
                        i.due_date AS 'Due Date',
                        i.billing_period AS 'Billing Period',
                        i.merchant_name AS 'Merchant Name',
                        i.merchant_cif AS 'Merchant CIF',
                        i.merchant_iban AS 'Merchant IBAN',
                        i.client_name AS 'Client Name',
                        i.client_code AS 'Client Code',
                        i.client_address AS 'Client Address',
                        it.description AS 'Item Description',
                        it.quantity AS 'Qty',
                        it.unit_price AS 'Unit Price',
                        it.tax_amount AS 'Tax Amount',
                        it.total_price AS 'Total Item Price',
                        i.total_amount AS 'Total Invoice (No Balance)',
                        i.previous_balance AS 'Previous Balance',
                        i.total_payable AS 'Total Payable',
                        i.currency AS 'Currency'
                    FROM invoices i
                    JOIN invoice_items it ON i.id = it.invoice_id
                """

                invoices_dataframe = pd.read_sql_query(sql_query, conn)
                invoices_dataframe.to_excel(output_path, index=False, engine='openpyxl')
                
                logger.info(f"Successfully exported {len(invoices_dataframe)} rows to {output_path}")
        except Exception as e:
            logger.error(f"Failed to export data to Excel: {e}")
            raise e





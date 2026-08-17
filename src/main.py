import os 
import logging

from src.services.ai_extractor import AIExtractorService
from src.repositories.db_manager import DatabaseManager
from src.services.exporter import ExporterService

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def main():
    logger.info("Starting the Invoice AI Parser...")

    test_file_path = "data/input_docs/sample_receipt.jpg"

    if not os.path.exists(test_file_path):
        logger.error(f"Please place a test image or PDF at: {test_file_path}")
        return 

    try:
        extractor = AIExtractorService()
        logger.info(f"Initiating extraction for: {test_file_path}")
        extracted_data = extractor.extract_data(file_path=test_file_path)

        logger.info("Extraction complete! Here are the structured results:")
        print("\n" + extracted_data.model_dump_json(indent=2) + "\n")

        logger.info("Connecting to the database...")
        db = DatabaseManager()
        db.save_invoice(invoice_data=extracted_data)

        logger.info("Exporting database records to Excel...")
        exporter = ExporterService()
        exporter.export_to_excel()

        logger.info("Pipeline execution finished successfully!")
    except Exception as e:
        logger.error(f"An error occurred during execution: {e}")

if __name__ == "__main__":
    main()
import os 
import logging

from src.services.ai_extractor import AIExtractorService
from src.repositories.db_manager import DatabaseManager
from src.services.exporter import ExporterService
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def main():
    logger.info("Starting the Invoice AI Parser...")

    input_dir = Path("data/input_docs")
    if not input_dir.exists():
        logger.error(f"Input directory not found: {input_dir}")
        return

    extractor = AIExtractorService()
    db = DatabaseManager()
    exporter = ExporterService()

    valid_extensions = {".jpg", ".jpeg", ".png", ".pdf"}
    files_to_process = [f for f in input_dir.iterdir() if f.suffix.lower() in valid_extensions]

    if not files_to_process:
        logger.warning(f"No valid documents found in {input_dir}.")
        return

    for file_path in files_to_process:
        if "sample_receipt" in file_path.name.lower():
            continue

        logger.info(f"--- Processing: {file_path.name} ---")
        try:
            extracted_data = extractor.extract_data(file_path=str(file_path))
            db.save_invoice(invoice_data=extracted_data)
            logger.info(f"Successfully saved {file_path.name} to database.")
        except Exception as e:
            logger.error(f"Failed to process {file_path.name}: {e}")

    logger.info("--- Exporting all records to Excel ---")
    try:
        exporter.export_to_excel()
        logger.info("Batch Pipeline execution finished successfully!")
    except Exception as e:
        logger.error(f"Failed during export: {e}")

if __name__ == "__main__":
    main()
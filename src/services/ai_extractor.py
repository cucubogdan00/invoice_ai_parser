import os
import logging

from google import genai
from google.genai import types
from src.utils.config import Config
from src.models.schemas import InvoiceData

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

class AIExtractorService:

    def __init__(self):
        self.client = genai.Client(api_key=Config.GEMINI_API_KEY)
        self.model_name = 'gemini-3.7-flash'
        logger.info("AIExtractorService initialized successfully with google-genai.")

    def extract_data(self, file_path: str) -> InvoiceData:
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            raise FileNotFoundError(f"The file {file_path} was not found.")

        logger.info(f"Uploading {file_path} to Gemini API...")

        uploaded_file = self.client.files.upload(file=file_path)

        prompt = (
            "Analyze this invoice/receipt document. Extract all the relevant details "
            "and map them exactly to the provided JSON schema. Ensure types match."
        )

        logger.info("Processing document with AI... Please wait.")
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=[prompt, uploaded_file],
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=InvoiceData
                )
            )

            validated_data = response.parsed

            logger.info("Data extracted and validated successfully!")
            return validated_data
        except Exception as e:
            logger.error(f"Failed to extract data: {e}")
            raise
        finally:
            logger.info("Cleaning up temporary file from Google servers.")
            self.client.files.delete(name=uploaded_file.name)

        

import os
import json
import logging
import google.generativeai as genai

from google.generativeai.types import GenerationConfig
from src.utils.config import Config
from src.models.schemas import InvoiceData

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

class AIExtractorService:

    def __init__(self):
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        logger.info("AIExtractorService initialized successfully.")

    def extract_data(self, file_path: str) -> InvoiceData:
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            raise FileNotFoundError(f"The file {file_path} was not found.")

        logger.info(f"Uploading {file_path} to Gemini API...")
        uploaded_file = genai.upload_file(path=file_path)

        prompt = (
            "Analyze this invoice/receipt document. Extract all the relevant details "
            "and map them exactly to the provided JSON schema. Ensure types match."
        )

        logger.info("Processing document with AI... Please wait.")
        try:
            response = self.model.generate_content(
                [prompt, uploaded_file],
                generation_config=GenerationConfig(
                    response_mime_type="application/json",
                    response_schema=InvoiceData
                )
            )

            raw_json_data = json.loads(response.text)

            validated_data = InvoiceData(**raw_json_data)

            logger.info("Data extracted and validated successfully!")
            return validated_data
        except Exception as e:
            logger.error(f"Failed to extract data: {e}")
            raise
        finally:
            logger.info("Cleaning up temporary file from Google servers.")
            uploaded_file.delete()

        

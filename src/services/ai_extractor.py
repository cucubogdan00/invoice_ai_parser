import os
import logging
import time

from google import genai
from google.genai import types
from src.utils.config import Config
from src.utils.prompts import Prompts, AIModelConfig
from src.models.schemas import InvoiceData

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

class AIExtractorService:

    def __init__(
        self,
        model_name: str = AIModelConfig.DEFAULT_MODEL,
        temperature: float = AIModelConfig.DEFAULT_TEMPERATURE
    ):
        self.client = genai.Client(api_key=Config.GEMINI_API_KEY)
        self.model_name = model_name
        self.temperature = temperature
        logger.info("AIExtractorService initialized successfully with google-genai.")

    def extract_data(self, file_path: str) -> InvoiceData:
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            raise FileNotFoundError(f"The file {file_path} was not found.")

        logger.info(f"Uploading {file_path} to Gemini API...")
        uploaded_file = self.client.files.upload(file=file_path)

        logger.info("Processing document with AI... Please wait.")

        max_retries = AIModelConfig.MAX_RETRIES

        try:
            for attempt in range(max_retries):
                try:
                    response = self.client.models.generate_content(
                        model=self.model_name,
                        contents=[Prompts.INVOICE_PARSER_SYSTEM_PROMPT, uploaded_file],
                        config=types.GenerateContentConfig(
                            response_mime_type="application/json",
                            response_schema=InvoiceData,
                            temperature=self.temperature
                        )
                    )

                    validated_data = response.parsed
                    logger.info("Data extracted and validated successfully!")
                    return validated_data
                except Exception as e:
                    error_message = str(e)

                    if '503' in error_message and attempt < max_retries - 1: 
                        sleep_time = AIModelConfig.RETRY_BACKOFF_FACTOR ** attempt
                        logger.warning(f"Server is busy (503). Retrying in {sleep_time} seconds (Attempt {attempt + 1}/{max_retries})...")
                        time.sleep(sleep_time)
                    else:
                        raise e
                    
        except Exception as final_e:
            logger.error(f"Failed to extract data after multiple attempts: {final_e}")
            raise
        finally:
            logger.info("Cleaning up temporary file from Google servers.")
            self.client.files.delete(name=uploaded_file.name)

        

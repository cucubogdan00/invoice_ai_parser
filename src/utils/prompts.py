class Prompts:

    INVOICE_PARSER_SYSTEM_PROMPT: str = (
        "You are an expert Document AI specialized in enterprise invoice parsing. "
        "Analyze this invoice/receipt document with extreme precision. "
        "Extract all relevant merchant, client, date, financial, and line-item details, "
        "and map them strictly into the provided JSON schema."
    )

class AIModelConfig:

    DEFAULT_MODEL: str = "gemini-3.5-flash"
    DEFAULT_TEMPERATURE: float = 0.1
    MAX_RETRIES: int = 3
    RETRY_BACKOFF_FACTOR: int = 2

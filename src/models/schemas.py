from pydantic import BaseModel, Field
from typing import List

class InvoiceItem(BaseModel):
    description: str = Field(description="The exact description of the product or service.")
    quantity: float = Field(description="The quantity purchased. If not explicitly specified, default to 1.0.")
    unit_price: float = Field(description="The unit price, strictly without the currency symbol.")

class InvoiceData(BaseModel):
    """Main model representing the entire invoice data."""
    merchant_name: str = Field(description="The name of the company or store that issued the document.")
    invoice_number: str = Field(description="The invoice or receipt number/series.")
    date: str = Field(description="The date of issue, strictly in YYYY-MM-DD format.")
    total_amount: float = Field(description="The total amount to be paid on the invoice.")
    items: List[InvoiceItem] = Field(description="The list of all products or services purchased.")

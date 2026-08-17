from pydantic import BaseModel, Field
from typing import List,Optional

class InvoiceItem(BaseModel):
    description: str = Field(description="The exact description of the product or service.")
    quantity: float = Field(description="The quantity purchased. If not explicitly specified, default to 1.0.")
    unit_price: float = Field(description="The unit price, strictly without the currency symbol.")
    tax_amount: Optional[float] = Field(default=0.0, description="The tax (VAT) amount for this specific item.")
    total_price: float = Field(description="The total price for this item, including tax.")

class InvoiceData(BaseModel):
    """Main model representing the entire invoice data with comprehensive fields."""

    # 1. Merchant Details
    merchant_name: str = Field(description="The name of the company or store that issued the document.")
    merchant_cif: Optional[str] = Field(default=None, description="The tax identification number (C.I.F. / CUI) of the merchant.")
    merchant_iban: Optional[str] = Field(default=None, description="The main IBAN account number of the merchant.")

    # 2. Client Details
    client_name: Optional[str] = Field(default=None, description="The name of the client receiving the invoice.")
    client_code: Optional[str] = Field(default=None, description="The unique client code or ID.")
    client_address: Optional[str] = Field(default=None, description="The full address of the client.")

    # 3. Invoice Metadata
    invoice_number: str = Field(description="The invoice or receipt number/series.")
    date: str = Field(description="The date of issue, strictly in YYYY-MM-DD format.")
    due_date: Optional[str] = Field(default=None, description="The due date for payment, strictly in YYYY-MM-DD format.")
    billing_period: Optional[str] = Field(default=None, description="The billing period covered by this invoice.")

    # 4. Financials
    total_amount: float = Field(description="The total amount to be paid on the invoice.")
    previous_balance: Optional[float] = Field(default=0.0, description="Any previous balance carried over.")
    total_payable: Optional[float] = Field(default=None, description="The final total amount to be paid (current invoice + previous balance).")
    currency: Optional[str] = Field(default="RON", description="The currency of the invoice (e.g., RON, EUR).")

    # 5. Items
    items: List[InvoiceItem] = Field(description="The list of all products or services purchased.")

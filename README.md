# 📄 Invoice AI Parser: Enterprise Document Extraction System

## 📌 Project Overview
**Invoice AI Parser** is a production-ready, end-to-end Document AI system designed to automate the extraction of unstructured data from invoices and receipts (images and PDFs) into highly structured, relational business formats. 

Bypassing legacy OCR limitations, this system leverages **Vision-Language Models (Google Gemini)** guided by strict **Pydantic** schemas to achieve deterministic, highly accurate data extraction. It features a robust, decoupled architecture including API resilience mechanisms, persistent storage, and business reporting capabilities.

## 🏗️ Architecture & Core Features

The project is built on strict **SOLID principles** and **Separation of Concerns**, divided into autonomous layers:

*   🧠 **Schema-Driven Extraction (Domain Layer):** Uses strictly typed `Pydantic` models to force the LLM into generating precise, predictable JSON outputs. It actively ignores irrelevant data and maps complex entities (e.g., Merchant CIF, IBAN, line-item taxes).
*   🛡️ **Resilient AI Service (Service Layer):** Implements an exponential backoff retry mechanism to handle Google API rate limits (`503 Service Unavailable`), ensuring production stability during high-demand spikes.
*   🗄️ **Relational Storage (Repository Layer):** Uses `SQLite3` with the Repository Pattern. Secures data persistence using parameterized queries to prevent SQL Injection attacks.
*   📊 **Automated Reporting (Export Layer):** Integrates `Pandas` and `OpenPyXL` to execute complex SQL `JOIN` operations, transforming relational data into human-readable Excel (`.xlsx`) reports.

## 🛠️ Technology Stack
*   **Language:** Python 3.12
*   **AI SDK:** `google-genai` (Gemini 3.5 Flash)
*   **Data Validation:** `pydantic`
*   **Database:** `sqlite3` (Native)
*   **Data Manipulation:** `pandas`, `openpyxl`
*   **Environment Management:** `python-dotenv`

---

# 🚀 Installation & Setup

## 1. Clone the repository

```bash
git clone https://github.com/yourusername/invoice_ai_parser.git
cd invoice_ai_parser
```

## 2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate  
# On Windows: 
venv\Scripts\activate
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 4. Environment Configuration

Create a `.env` file in the root directory and add your Google Gemini API key:

```env
GEMINI_API_KEY="your_api_key_here"
```

---

# 💻 Usage

1. Place your target document (e.g., `sample_receipt.jpg` or a PDF) in the `data/input_docs/` directory.

2. Ensure `src/main.py` points to your target file.

3. Run the orchestrator:

```bash
python -m src.main
```

---

# ⚙️ Expected Pipeline Execution

1. ✅ Ingests the document.
2. ✅ Connects to Gemini API (with auto-retries if needed).
3. ✅ Validates the extracted JSON via Pydantic.
4. ✅ Initializes the SQLite database and inserts records securely.
5. ✅ Exports the normalized data to `data/invoices_export.xlsx`.

---

# 🔒 Security Notes

- **Data Privacy**: Real invoices and the SQLite database are explicitly ignored in `.gitignore` to prevent leaking PII (Personally Identifiable Information) or sensitive financial data.
- **API Keys**: Managed exclusively through `.env` files.

---

# 👨‍💻 Author

**Bogdan Cucu**  - https://github.com/cucubogdan00
Software Developer 
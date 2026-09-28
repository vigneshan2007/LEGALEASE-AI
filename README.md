LegalEaseAI — AI-Powered Legal Document Generator

LegalEaseAI is an AI-assisted legal document drafting prototype. It accepts basic document details and uses Google Gemini to create an editable first draft of common agreements.


Important: LegalEaseAI generates AI-assisted drafts for information and editing. It is not a substitute for legal advice, legal representation, or jurisdiction-specific review. Important documents must be reviewed by a qualified legal professional before signing or use.

Team Details

Field
Details
Team ID
SWTID-2026-7680
Team Size
3
Team Leader
Vigneshan P
Team Members
Udhaya kumar R; Vimal S




Features

•
Generate AI-assisted first drafts for:

•
Freelance Work Contract

•
Employment Contract

•
Non-Disclosure Agreement (NDA)

•
Lease Agreement

•
Service Agreement

•
General Agreement

•
Custom document types



•
Enter document type, effective date, parties, and terms.

•
Generate drafts using Google Gemini.

•
Edit the generated document before downloading.

•
Preview the document in the browser.

•
Download the edited draft as:

•
TXT

•
DOCX

•
PDF



•
Upload an optional PNG or JPG logo.

•
FastAPI backend with Pydantic request validation.

•
Health-check endpoint for backend monitoring.

•
Retry handling for temporary Gemini errors such as 429 and 503.

•
Safety instructions to avoid invented names, dates, amounts, laws, courts, or registration numbers.

•
Missing information is represented as [TO BE COMPLETED].

System Architecture

Plain Text


User
  |
  v
Streamlit Frontend
  |
  | HTTP POST /generate
  v
FastAPI Backend
  |
  v
Pydantic Validation
  |
  v
GeminiDocumentGenerator
  |
  v
Google Gemini API
  |
  v
Generated Draft
  |
  +--> Editable Preview
  +--> TXT Export
  +--> DOCX Export
  +--> PDF Export



Project Structure

Plain Text


LegalEaseAI/
├── app.py                         # Streamlit frontend
├── main.py                        # FastAPI application
├── routes.py                      # API routes and request model
├── requirements.txt               # Python dependencies
├── .env                           # Local secrets and configuration; do not commit
├── .gitignore                     # Ignored files and secrets
├── ai_core/
│   ├── __init__.py
│   └── gemini_generator.py         # Gemini client and prompt logic
└── utils/
    ├── __init__.py
    └── document_formatter.py       # TXT, DOCX, and PDF formatting



Do not include .venv/, __pycache__/, .pyc files, or .env in a source-code release.

Requirements

•
Python 3.10 or newer

•
Google Gemini API key

•
Internet connection for Gemini generation

•
Supported operating systems: Windows, macOS, or Linux

Installation

1. Clone or copy the project

Bash


git clone <repository-url>
cd LegalEaseAI



2. Create a virtual environment

Windows PowerShell

Plain Text


python -m venv .venv
.venv\\Scripts\\Activate.ps1



Windows Command Prompt

Plain Text


python -m venv .venv
.venv\\Scripts\\activate



macOS or Linux

Bash


python3 -m venv .venv
source .venv/bin/activate



3. Install dependencies

Bash


python -m pip install --upgrade pip
pip install -r requirements.txt



Environment Configuration

Create a .env file in the project root:

Plain Text


GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=your_supported_gemini_model
BACKEND_URL=http://127.0.0.1:8000



Configuration variables

Variable
Required
Description
Example
GEMINI_API_KEY
Yes
API key used to call Gemini
your_api_key
GEMINI_MODEL
No
Gemini model name
your_supported_model
BACKEND_URL
No
URL used by Streamlit to reach FastAPI
http://127.0.0.1:8000




Never commit the .env file or share the API key. The .gitignore file should contain:

Plain Text


.venv/
__pycache__/
*.pyc
.env
.streamlit/secrets.toml



Running the Application

LegalEaseAI uses two processes: a FastAPI backend and a Streamlit frontend.

Terminal 1 — Start FastAPI

Bash


uvicorn main:app --reload --host 127.0.0.1 --port 8000



The backend will be available at:

•
API root: http://127.0.0.1:8000/

•
Health check: http://127.0.0.1:8000/health

•
Swagger documentation: http://127.0.0.1:8000/docs

Terminal 2 — Start Streamlit

Bash


streamlit run app.py



Open the URL shown by Streamlit, normally:

Plain Text


http://localhost:8501



User Workflow

1.
Open the Streamlit application.

2.
Select a document type.

3.
Enter the effective date.

4.
Enter all parties involved.

5.
Enter the terms and conditions.

6.
Optionally upload a PNG or JPG logo.

7.
Click Generate Document.

8.
Wait for Gemini to create the first draft.

9.
Review and edit the document in the text area.

10.
Download the edited document as TXT, DOCX, or PDF.

11.
Complete all [TO BE COMPLETED] fields.

12.
Ask a qualified legal professional to review important documents.

API Documentation

GET /

Checks whether the API is running.

Example response:

JSON


{
  "message": "LegalEase API is running",
  "status": "success"
}



GET /health

Returns the service health status.

Example response:

JSON


{
  "status": "healthy"
}



POST /generate

Generates an AI-assisted legal document draft.

Request body

JSON


{
  "document_type": "Service Agreement",
  "parties": "Jane Doe (Service Provider ), Example Corp (Client)",
  "terms": "Payment within 30 days; delivery by the agreed deadline; confidentiality; termination with 15 days notice",
  "effective_date": "28/09/2026"
}



Successful response

JSON


{
  "document": "SERVICE AGREEMENT\n\n1. PARTIES\n..."
}



Request limits

Field
Minimum
Maximum
document_type
2 characters
100 characters
parties
2 characters
5,000 characters
terms
2 characters
10,000 characters
effective_date
2 characters
100 characters




Example cURL request

Bash


curl -X POST http://127.0.0.1:8000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "document_type": "NDA",
    "parties": "Company A and Company B",
    "terms": "Confidential information must be protected for two years.",
    "effective_date": "28/09/2026"
  }'



Gemini Prompt Safety Rules

The generation service instructs Gemini to:

•
Generate only a first draft.

•
Use only facts supplied by the user.

•
Avoid inventing names, addresses, dates, money amounts, laws, courts, or registration numbers.

•
Use [TO BE COMPLETED] when important information is missing.

•
Use professional and understandable language.

•
Include sections, obligations, termination provisions, confidentiality provisions, and signature areas where appropriate.

•
Return plain text without Markdown code fences.

•
Avoid claiming that the document is legally valid.

•
Avoid providing legal advice.

Error Handling

Common errors include:

Error
Possible Cause
Recommended Action
Cannot connect to FastAPI
Backend is not running
Start uvicorn main:app --reload
Gemini API key is missing
.env is absent or incorrectly configured
Add GEMINI_API_KEY to .env
Gemini temporarily unavailable
Provider 429/503 or quota issue
Wait and retry later
Validation error
Input is empty, too short, or too long
Correct the fields and submit again
Empty Gemini response
Provider returned no text
Retry and check model configuration
Export error
Invalid input or formatting dependency problem
Reinstall dependencies and retry




Testing Checklist

Before a release, verify:




GET / returns a successful response.




GET /health returns healthy.




Valid POST /generate returns a non-empty document.




Empty required fields are rejected.




Oversized fields are rejected.




Missing Gemini configuration is handled clearly.




Temporary Gemini failures are retried.




Generated text can be edited.




TXT download opens correctly.




DOCX download opens correctly.




PDF download opens correctly.




Optional logo upload works with supported image formats.




The legal disclaimer is visible.




No API key appears in source files, logs, or generated output.




.venv/, .env, __pycache__/, and .pyc files are excluded from release archives.

Security and Privacy Notes

Before public deployment:

1.
Restrict FastAPI CORS from allow_origins=["*"] to the real frontend domain.

2.
Add authentication and authorization to the API.

3.
Add rate limiting and abuse prevention.

4.
Use HTTPS for all network communication.

5.
Store the Gemini key in a secret manager.

6.
Do not log parties, terms, or sensitive document contents unnecessarily.

7.
Define a privacy policy and data-retention policy.

8.
Sanitize internal provider errors before returning them to users.

9.
Review generated documents for prompt injection and data leakage risks.

10.
Require qualified legal review before important documents are signed or used.

Known Limitations

•
No user authentication.

•
No persistent document history.

•
No database or audit trail.

•
No jurisdiction-aware legal validation.

•
No legal citation verification.

•
No electronic-signature workflow.

•
No public API rate limiting.

•
No automated legal-content quality guarantee.

•
Gemini output may contain factual or legal errors.

•
The system is a drafting aid, not a legal decision system.

Future Enhancements

•
User accounts and secure document history.

•
Document version control and audit logs.

•
Jurisdiction and governing-law selection.

•
Approved clause library and organization templates.

•
Lawyer review and approval workflow.

•
Document comparison and tracked changes.

•
Retrieval from approved legal sources with citations.

•
Multilingual document drafting.

•
Automated regression testing and lawyer-reviewed benchmarks.

•
Secure cloud storage and enterprise access controls.

•
Rate limiting, usage analytics, monitoring, and cost controls.

License and Usage

Add an appropriate project license before public distribution. Until a license is added, treat the source code and generated documents as project materials for authorized use only.

Final Disclaimer

LegalEaseAI does not create an attorney-client relationship and does not replace a lawyer. AI-generated documents can contain errors, omissions, unsuitable clauses, or jurisdictional problems. Always verify the facts and obtain qualified professional review before relying on any generated legal document.


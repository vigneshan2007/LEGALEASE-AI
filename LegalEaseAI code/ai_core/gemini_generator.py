import os
import time

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()


class GeminiDocumentGenerator:

    def __init__(self):

        self.api_key = os.getenv("GEMINI_API_KEY")

        # Primary model
        self.model = os.getenv(
            "GEMINI_MODEL",
            "gemini-3.5-flash-lite"
        )

        if not self.api_key:
            self.client = None
        else:
            self.client = genai.Client(
                api_key=self.api_key
            )

    def generate_document(
        self,
        document_type,
        parties,
        terms,
        effective_date
    ):

        if not self.client:
            raise RuntimeError(
                "GEMINI_API_KEY is missing. "
                "Please add your Gemini API key to the .env file."
            )

        prompt = f"""
You are LegalEase, an AI-assisted legal document drafting system.

Create a professional FIRST DRAFT of the following legal document.

DOCUMENT TYPE:
{document_type}

PARTIES:
{parties}

TERMS AND CONDITIONS:
{terms}

EFFECTIVE DATE:
{effective_date}

IMPORTANT INSTRUCTIONS:

1. Create a properly structured legal document.
2. Start with a clear document title.
3. Include the parties and effective date.
4. Organize the document using numbered sections.
5. Include obligations and responsibilities based only on
   information supplied by the user.
6. Do not invent names, addresses, dates, money amounts,
   laws, courts, registration numbers, or other facts.
7. If important information is missing, write:
   [TO BE COMPLETED]
8. Use professional but understandable language.
9. Include termination provisions when appropriate.
10. Include confidentiality provisions when appropriate.
11. Include dispute-related provisions only when appropriate.
12. Finish with signature sections for the relevant parties.
13. Do not use Markdown code fences.
14. Return plain text.
15. Do not claim that the document is legally valid.
16. Do not provide legal advice.

Generate only the document.
"""

        last_error = None

        # Retry temporary 503 errors
        for attempt in range(4):

            try:

                response = self.client.models.generate_content(
                    model=self.model,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        temperature=0.2,
                        max_output_tokens=8000
                    )
                )

                document = (response.text or "").strip()

                if document:
                    return document

                last_error = RuntimeError(
                    "Gemini returned an empty response."
                )

            except Exception as error:

                last_error = error
                error_text = str(error).upper()

                # Retry temporary server errors
                if (
                    "503" in error_text
                    or "UNAVAILABLE" in error_text
                    or "429" in error_text
                    or "RESOURCE_EXHAUSTED" in error_text
                ):

                    if attempt < 3:

                        wait_time = 2 ** attempt

                        print(
                            f"Gemini temporarily unavailable. "
                            f"Retrying in {wait_time} seconds..."
                        )

                        time.sleep(wait_time)

                        continue

                break

        raise RuntimeError(
            "Gemini is temporarily unavailable.\n\n"
            "Please wait a little and click Generate Document again.\n\n"
            f"Last error: {last_error}"
        )
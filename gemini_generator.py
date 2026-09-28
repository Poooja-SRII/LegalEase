import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is missing in the .env file")

genai.configure(api_key=api_key)


class GeminiDocumentGenerator:

    def __init__(self):
        self.model = genai.GenerativeModel("gemini-3.8-flash")

    def generate_document(self, document_type, parties, terms, dates):

        prompt = f"""
Create a professional legal document.

Document Type: {document_type}

Parties Involved: {parties}

Terms and Conditions: {terms}

Effective Date: {dates}

Write the document in a clear and professional legal format.
Include suitable headings, clauses, terms and conditions, and signature sections.
"""

        response = self.model.generate_content(prompt)

        return response.text

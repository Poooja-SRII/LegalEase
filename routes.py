from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from gemini_generator import GeminiDocumentGenerator

router = APIRouter()

generator = GeminiDocumentGenerator()


class DocumentRequest(BaseModel):
    document_type: str
    parties: str
    terms: str
    dates: str


@router.post("/generate")
def generate_document(request: DocumentRequest):

    try:

        document = generator.generate_document(
            request.document_type,
            request.parties,
            request.terms,
            request.dates
        )

        return {
            "success": True,
            "document": document
        }

    except Exception as e:

        error_message = str(e)

        if "429" in error_message or "quota" in error_message.lower():
            raise HTTPException(
                status_code=429,
                detail="Gemini API quota has been exceeded. Please try again after the quota resets."
            )

        raise HTTPException(
            status_code=500,
            detail="Failed to generate the legal document."
        )

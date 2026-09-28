from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from ai_core.gemini_generator import GeminiDocumentGenerator


router = APIRouter()

generator = GeminiDocumentGenerator()


class DocumentRequest(BaseModel):

    document_type: str = Field(
        ...,
        min_length=2,
        max_length=100
    )

    parties: str = Field(
        ...,
        min_length=2,
        max_length=5000
    )

    terms: str = Field(
        ...,
        min_length=2,
        max_length=10000
    )

    effective_date: str = Field(
        ...,
        min_length=2,
        max_length=100
    )


@router.post("/generate")
def generate_document(request: DocumentRequest):

    try:

        document = generator.generate_document(
            document_type=request.document_type,
            parties=request.parties,
            terms=request.terms,
            effective_date=request.effective_date
        )

        return {
            "document": document
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )
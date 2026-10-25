
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class DocumentationStepCreate(BaseModel):
    step_number: int = Field(ge=1)
    title: str = Field(min_length=1, max_length=200)
    instructions: str = Field(min_length=1)
    image_path: str | None = None


class DocumentationStepResponse(DocumentationStepCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    session_id: int
    created_at: datetime


class DocumentationSessionCreate(BaseModel):
    title: str = Field(
        default="Untitled Documentation",
        min_length=1,
        max_length=200,
    )


class DocumentationSessionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    created_at: datetime
    steps: list[DocumentationStepResponse] = []

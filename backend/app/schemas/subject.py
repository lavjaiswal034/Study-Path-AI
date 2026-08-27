from pydantic import BaseModel


class SubjectCreate(BaseModel):
    name: str
    code: str
    credits: int | None = None


class SubjectResponse(BaseModel):
    id: int
    name: str
    code: str
    credits: int | None
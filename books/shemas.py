from typing import Optional

from pydantic import BaseModel, conint


class SBooks(BaseModel):
    id: int
    name: str
    author: str
    year: conint(le=2025)
    ISBN: int
    quantity: int
    description: str

class SBooksModel(BaseModel):
    name: str
    author: str
    year: conint(le=2025)
    ISBN: Optional[int]
    quantity: int = 1
    description: Optional[str]


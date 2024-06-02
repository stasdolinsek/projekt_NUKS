from pydantic import BaseModel
from typing import Optional

class File(BaseModel):
    id: Optional[int]
    filename: str
    content: Optional[str]  # Dovoli None kot vrednost

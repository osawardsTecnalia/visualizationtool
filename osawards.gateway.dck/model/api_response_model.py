from pydantic import BaseModel # type: ignore
from typing import Optional


class ApiResponse(BaseModel):
    code: str
    error: bool
    result: Optional[str] = None
    message: Optional[str] = None

from pydantic import BaseModel # type: ignore


class Report(BaseModel):
    title: str
    description: str
    link: str

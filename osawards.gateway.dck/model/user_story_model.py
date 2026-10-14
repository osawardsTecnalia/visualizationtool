from pydantic import BaseModel # type: ignore


class UserStory(BaseModel):
    description: str
    link: str

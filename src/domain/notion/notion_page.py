from pydantic import BaseModel, Field
from typing import Any


class NotionPage(BaseModel):
    object: str = Field()
    id: str = Field()
    properties: dict[str, Any] = Field()
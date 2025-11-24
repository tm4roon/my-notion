from typing import Any

from pydantic import BaseModel
from pydantic import Field


class NotionPage(BaseModel):
    object: str = Field()
    id: str = Field()
    properties: dict[str, Any] = Field()

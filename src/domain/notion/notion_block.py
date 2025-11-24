from pydantic import BaseModel, Field
from .notion_block_type import NotionBlockType
from typing import Any


class NotionBlock(BaseModel):
    """Notionのブロックを表すデータクラス"""

    object: str = Field(..., description="")
    id: str = Field(..., description="ブロックID")
    type: NotionBlockType = Field(..., description="ブロックタイプ")
    content: dict[str, Any] = Field(default_factory=dict, description="ブロックのテキスト内容")

    @property
    def plain_text(self) -> str:
        if "rich_text" not in self.content:
            return ""

        res = ""
        for e in self.content.get("rich_text"):
            if "plain_text" not in e:
                continue
            res += e["plain_text"]
        return res

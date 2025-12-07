from pydantic import BaseModel
from pydantic import Field

from .diary_entry import DiaryEntry


class DiaryEntryRevision(BaseModel):
    """日記エントリ（Heading2 単位のセクション）"""
    title: str = Field(..., description="エントリのタイトル.")
    origin: DiaryEntry = Field(..., description="エントリの中身.")
    revised: DiaryEntry = Field(..., description="LLMで修正したエントリの中身.")

    @property
    def origin_content(self) -> str:
        return self.origin.content

    @property
    def revised_content(self) -> str:
        return self.revised.content


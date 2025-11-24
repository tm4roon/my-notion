from pydantic import BaseModel, Field
from datetime import date
from .diary_entry import DiaryEntry


class Diary(BaseModel):
    """日記ドメインオブジェクト"""

    title: str = Field(..., description="日記のタイトル.")
    diary_date: date | None = Field(None, description="日記の日付")
    entries: list[DiaryEntry] = Field(..., description="日記のエントリのリスト.")

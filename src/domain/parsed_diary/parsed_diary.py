from pydantic import BaseModel, Field
from datetime import date 
from .parsed_diary_entry import ParsedDiaryEntry

class ParsedDiary(BaseModel):
    title: str = Field(..., description="日記のタイトル.")
    diary_date: date | None = Field(None, description="日記の日付")
    original_entries: list[ParsedDiaryEntry] = Field(..., description="日記のオリジナルエントリのリスト.")
    revised_entries: list[ParsedDiaryEntry] = Field(..., description="LLMで修正した日記エントリのリスト.")
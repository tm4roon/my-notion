from pydantic import BaseModel, Field


class DiaryEntry(BaseModel):
    title: str
    content: str = Field(..., description="エントリの内容（Markdown形式）")

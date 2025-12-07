from pydantic import BaseModel, Field


class DiaryEntryStats(BaseModel):
    """日記の統計量を表すクラス"""

    vocab: set[str] = Field(..., description="ユニークな単語の集合")
    n_sentences: int = Field(..., description="文の総数")
    n_words: int = Field(..., description="単語の総数")

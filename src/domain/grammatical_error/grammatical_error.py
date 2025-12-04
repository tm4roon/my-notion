
from pydantic import BaseModel, Field
from .grammatical_error_type import GrammaticalErrorType

class GrammaticalError(BaseModel):
    type: GrammaticalErrorType = Field(..., description="エラーの種類.")
    err: str = Field(..., description="エラー箇所のテキスト.")
    fix: str = Field(..., description="修正後のテキスト.")
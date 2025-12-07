from google.genai import types

from pydantic import BaseModel, Field

from infra.gemini_client import GeminiClient
from domain.diary.diary_entry_revision import DiaryEntryRevision
from domain.diary_feedback import GrammaticalError
from domain.diary_feedback.diary_entry_error_analysis import DiaryEntryErrorAnalysis

from .base import DetectGrammaticalErrorBase


DEFAULT_SYSTEM_PROMPT = """
# 責務
- あなたは英語の文法エラー検出する責務を担っています。

# エラーの定義
- ARTICLE（冠詞）: a/an/theの使い方の誤り
- PREPOSITION（前置詞）: in/on/at/for/toなどの前置詞の誤用
- PRONOUN（代名詞）: he/she/it/they/him/herなどの代名詞の誤り
- SPELLING（スペルミス）: 単語のつづりの間違い
- TENSE（時制）: 過去形・現在形・未来形などの時制の誤り
- WORD_CHOICE（語彙選択）: 文脈に合わない単語の選択
- WORD_ORDER（語順）: 単語の並び順の誤り
- SUBJECT_VERB_AGREEMENT（主語と動詞の一致）: 主語の単数/複数と動詞の形の不一致
- VERB_FORM（動詞の形）: 不定詞・動名詞・分詞などの動詞形態の誤り
- OTHER（その他）: 上記に分類できないその他の文法エラー

# タスク
以下の指示に従ってください。
1. 与えられた原文の英語日記と修正後の英語日記を比較してください。
2. 修正前後の差分から文法エラーを検出してください。
3. 各文法エラーについて、以下の情報を抽出してください。
   - エラーの種類（例：スペルミス、句読点の誤り、主語と動詞の一致の誤りなど）
   - エラー箇所のテキスト
   - 修正後のテキスト
4. 出力は原文の先頭から順にリスト形式で提供してください。
"""

DEFAULT_USER_PROMPT_TEMPLATE = """
# 日記のタイトル
{entry_title}

# 原文の英語日記
{original_entry}

# 修正後の英語日記
{revised_entry}
"""

class OutputSchema(BaseModel):
    grammatical_errors: list[GrammaticalError] = Field(
        description="検出された文法エラーのリスト."
    )

class DetectGrammaticalErrorGemini(DetectGrammaticalErrorBase):

    def __init__(
        self, 
        gemini_client: GeminiClient, 
        system_prompt: str | None = None, 
        user_prompt_template: str | None = None
    ):
        self.gemini_client = gemini_client
        self.system_prompt = system_prompt if system_prompt else DEFAULT_SYSTEM_PROMPT
        self.user_prompt_template = user_prompt_template if user_prompt_template else DEFAULT_USER_PROMPT_TEMPLATE


    def invoke(self, revision: DiaryEntryRevision) -> DiaryEntryErrorAnalysis:
        input_prompt = f"{self.system_prompt}\n{self.user_prompt_template}"

        original_entry = self.preprocess_entry_content(revision.origin_content)
        revised_entry = self.preprocess_entry_content(revision.revised_content)

        contents = input_prompt.format(
            entry_title=revision.title,
            original_entry=original_entry,
            revised_entry=revised_entry,
        )
        res = self.gemini_client.invoke(
            contents=contents,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=OutputSchema,
            ),
        )
        return DiaryEntryErrorAnalysis(errors=res.parsed.grammatical_errors)

    @staticmethod 
    def preprocess_entry_content(content: str) -> str:
        return content.replace("’", "'").replace("\n", '')
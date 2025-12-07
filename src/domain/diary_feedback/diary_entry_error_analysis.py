from collections import Counter

from pydantic import BaseModel, Field
from .grammatical_error import GrammaticalError
from .grammatical_error_type import GrammaticalErrorType


class DiaryEntryErrorAnalysis(BaseModel):
    errors: list[GrammaticalError] = Field(..., description="日記に含まれる文法エラーのリスト.")
    
    def count_errors(self) -> dict:
        counter = Counter(e.type for e in self.errors)
        return {t: counter.get(t, 0) for t in GrammaticalErrorType}

    def extract_errors(self, error_type: GrammaticalErrorType) -> list[GrammaticalError]:
        return [err for err in self.errors if err.type == error_type]

    @property
    def errors_article(self) -> list[GrammaticalError]:
        return self.extract_errors(GrammaticalErrorType.ARTICLE)
    
    @property
    def errors_preposition(self) -> list[GrammaticalError]:
        return self.extract_errors(GrammaticalErrorType.PREPOSITION)

    @property
    def errors_pronoun(self) -> list[GrammaticalError]:
        return self.extract_errors(GrammaticalErrorType.PRONOUN)
    
    @property
    def errors_spelling(self) -> list[GrammaticalError]:
        return self.extract_errors(GrammaticalErrorType.SPELLING)
    
    @property
    def errors_tense(self) -> list[GrammaticalError]:
        return self.extract_errors(GrammaticalErrorType.TENSE)
    
    @property
    def errors_word_choice(self) -> list[GrammaticalError]:
        return self.extract_errors(GrammaticalErrorType.WORD_CHOICE)

    @property
    def errors_word_order(self) -> list[GrammaticalError]:
        return self.extract_errors(GrammaticalErrorType.WORD_ORDER)

    @property
    def errors_subject_verb_agreement(self) -> list[GrammaticalError]:
        return self.extract_errors(GrammaticalErrorType.SUBJECT_VERB_AGREEMENT)

    @property
    def errors_verb_form(self) -> list[GrammaticalError]:
        return self.extract_errors(GrammaticalErrorType.VERB_FORM)

    @property
    def errors_other(self) -> list[GrammaticalError]:
        return self.extract_errors(GrammaticalErrorType.OTHER)
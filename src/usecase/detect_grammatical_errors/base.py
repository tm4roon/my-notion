from abc import ABC, abstractmethod

from domain.diary.diary_entry_revision import DiaryEntryRevision
from domain.diary_feedback import GrammaticalError

class DetectGrammaticalErrorBase(ABC):

    @abstractmethod
    def invoke(self, diary: DiaryEntryRevision) -> list[GrammaticalError]:
        """日記ドメインオブジェクトを受け取り、文法エラーのリストを返す"""
        raise NotImplementedError
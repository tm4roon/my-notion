from abc import ABC, abstractmethod
from domain.diary.diary_entry import DiaryEntry
from domain.diary.parsed_diary_entry import ParsedDiaryEntry


class BaseDiaryParser(ABC):


    @abstractmethod
    def invoke(self, entry: DiaryEntry) -> ParsedDiaryEntry:
        raise NotImplementedError
from abc import ABC
from abc import abstractmethod
from collections.abc import AsyncGenerator
from datetime import date

from domain.diary import Diary


class IDiaryRepository(ABC):
    @abstractmethod
    async def get(
        self,
        start: date | None = None,
        end: date | None = None,
    ) -> AsyncGenerator[Diary, None]:
        """日記を取得"""
        raise NotImplementedError

    # @abstractmethod
    # async def create(self, diary: Diary) -> str:
    #     """日記を作成し、作成されたページIDを返す"""
    #     raise NotImplementedError

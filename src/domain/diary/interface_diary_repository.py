from abc import ABC, abstractmethod
from typing import AsyncGenerator

from .diary import Diary
from datetime import date

class IDiaryRepository(ABC):
    ...
    # @abstractmethod
    # async def get_page(self, page_id: str) -> dict:
    #     raise NotImplementedError

    # @abstractmethod
    # async def get_pages(self, start: date | None, end: date | None = None) -> dict:
    #     raise NotImplementedError
    
    # @abstractmethod
    # async def create(self, diary: Diary) -> str:
    #     """日記を作成し、作成されたページIDを返す"""
    #     raise NotImplementedError

import asyncio
from datetime import date

from infra.diary_repository import DiaryRepository
from infra.gemini_client import GeminiClient
from usecase.diary_parser import EnglishDiaryParser
from settings import Settings


async def main():
    settings = Settings()
    diary_repository = DiaryRepository(
        api_key=settings.notion_api_key,
        database_id=settings.diary_database_id,
    )
    parser = EnglishDiaryParser()
    gemini_client=GeminiClient(
        model_name="gemini-2.5-flash",
        api_key=settings.gemini_api_key
    )
    start = date(2025, 11, 26)
    end = date(2025, 11, 30)
    async for diary in diary_repository.get(start, end):
        parsed_diary = parser.invoke(diary)
        print(parsed_diary)

if __name__ == "__main__":
    asyncio.run(main())

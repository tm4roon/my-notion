import asyncio
from datetime import date

from infra.diary_repository import DiaryRepository
from settings import Settings


async def main():
    settings = Settings()
    diary_repository = DiaryRepository(
        api_key=settings.notion_api_key,
        database_id=settings.diary_database_id,
    )

    start = date(2025, 10, 1)
    end = date(2025, 11, 30)
    async for diary in diary_repository.get(start, end):
        print(diary.diary_date, diary.title)


if __name__ == "__main__":
    asyncio.run(main())

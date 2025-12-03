import asyncio
from datetime import date

from infra.diary_repository import DiaryRepository
from usecase.parse_diary import ParseEnglishDiary
from settings import Settings


async def main():
    settings = Settings()
    diary_repository = DiaryRepository(
        api_key=settings.notion_api_key,
        database_id=settings.diary_database_id,
    )
    parse_diary = ParseEnglishDiary()
    
    start = date(2025, 11, 26)
    end = date(2025, 11, 30)
    async for diary in diary_repository.get(start, end):
        parsed_diary = parse_diary.invoke(diary)
        import pdb; pdb.set_trace()
        print(parsed_diary)

if __name__ == "__main__":
    asyncio.run(main())

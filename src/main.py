import asyncio
import logging
from datetime import date

from infra.diary_repository import DiaryRepository
from infra.gemini_client import GeminiClient
from settings import Settings

# ロガーの設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


async def main():
    settings = Settings()
    diary_repository = DiaryRepository(
        api_key=settings.notion_api_key,
        database_id=settings.diary_database_id,
    )
    # from usecase.diary_parser import EnglishDiaryParser
    # parser = EnglishDiaryParser()

    from usecase.grammatical_error_detector import GeminiBasedGED
    ged = GeminiBasedGED(
        gemini_client=GeminiClient(
            model_name="gemini-2.5-flash",
            api_key=settings.gemini_api_key
        )
    )
    
    start = date(2025, 11, 26)
    end = date(2025, 11, 30)
    async for diary in diary_repository.get(start, end):
        errs = ged.invoke(diary)
        print(errs)

if __name__ == "__main__":
    asyncio.run(main())

import asyncio
import logging
from datetime import date

from infra.diary_repository import DiaryRepository
from infra.gemini_client import GeminiClient
from settings import Settings

from usecase.parse_diary_content_to_revisions import ParseDiaryContentToRevisions
from usecase.nlp_diary_entry import NLPDiaryEntryEnglish
from usecase.calculate_diary_stats import CalculateDiaryStats
from usecase.detect_grammatical_errors.gemini import DetectGrammaticalErrorGemini
from usecase.generate_diary_feedback import GenerateDiaryFeedback

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
# TODO: 適切な統計量計算器を初期化

    generator = GenerateDiaryFeedback(
        parser=ParseDiaryContentToRevisions(),
        calculator=CalculateDiaryStats(nlp=NLPDiaryEntryEnglish()),
        detector=DetectGrammaticalErrorGemini(
            gemini_client=GeminiClient(
                model_name="gemini-2.5-flash",
                api_key=settings.gemini_api_key
            )
        )
    )
    
    start = date(2025, 12, 5)
    end = date(2025, 12, 6)
    async for diary in diary_repository.get(start, end):
        ret = generator.invoke(diary)


if __name__ == "__main__":
    asyncio.run(main())

from collections.abc import Generator
from datetime import date

from pydantic import BaseModel
from pydantic import Field

from domain.notion import NotionBlockType

from .diary_entry import DiaryEntry
from .diary_entry import DiaryEntryFactory
from .diary_page import DiaryPageFactory


class Diary(BaseModel):
    """日記ドメインオブジェクト"""

    title: str = Field(..., description="日記のタイトル.")
    diary_date: date | None = Field(None, description="日記の日付")
    original_entries: list[DiaryEntry] = Field(..., description="日記のエントリのリスト.")
    revised_entries: list[DiaryEntry] = Field(..., description="LLMで修正した日記エントリ.")


class DiaryFactory:
    """Notion APIレスポンスからドメインオブジェクトを生成するファクトリ"""

    def __init__(self):
        self.page_factory = DiaryPageFactory()
        self.entry_factory = DiaryEntryFactory()

    def from_notion(self, page: dict, children: dict) -> Diary:
        diary_page = self.page_factory.from_notion(page)

        sections = self.split_by_heading1(children)
        original_entries = []
        revised_entries = []
        for section in sections:
            if self.is_original_entry_section(section):
                original_entries = self.entry_factory.from_notion(section)
                continue
            if self.is_revised_entry_section(section):
                revised_entries = self.entry_factory.from_notion(section)
                continue

        return Diary(
            title=diary_page.properties.title,
            diary_date=diary_page.properties.diary_date,
            original_entries=original_entries,
            revised_entries=revised_entries,
        )

    def split_by_heading1(self, children: list[dict]) -> Generator[list[dict], None, None]:
        """Heading1 単位でブロックを分割"""
        offsets = [idx for idx, block in enumerate(children) if block["type"] == NotionBlockType.HEADING1]

        for i in range(len(offsets)):
            s = offsets[i]
            t = offsets[i + 1] if i + 1 < len(offsets) else len(children)
            yield list(children[s:t])

    def is_original_entry_section(self, blocks: list[dict]) -> bool:
        """'Entryのセクションかどうかを判定"""
        head_block = blocks[0]
        if head_block.get("type", "") != NotionBlockType.HEADING1:
            return False

        heading = head_block.get(NotionBlockType.HEADING1, {})
        rich_text = heading.get("rich_text", {})

        plain_text = ""
        for e in rich_text:
            plain_text += e.get("plain_text", "")
        if plain_text.strip() != "Entry":
            return False
        return True


    def is_revised_entry_section(self, blocks: list[dict]) -> bool:
        """'Entryのセクションかどうかを判定"""
        head_block = blocks[0]
        if head_block.get("type", "") != NotionBlockType.HEADING1:
            return False

        heading = head_block.get(NotionBlockType.HEADING1, {})
        rich_text = heading.get("rich_text", {})

        plain_text = ""
        for e in rich_text:
            plain_text += e.get("plain_text", "")
        if plain_text.strip().startswith("Revised"):
            return True
        return False
from collections.abc import Generator
from datetime import date

from pydantic import BaseModel
from pydantic import Field

from domain.notion import NotionBlockType
from domain.language import Language

from .diary_entry_revision import DiaryEntryRevision
from .diary_entry_revision import DiaryEntryRevisionFactory

from .diary_page import DiaryPageFactory


class Diary(BaseModel):
    """日記ドメインオブジェクト"""
    page_id: str | None = Field(None, description="NotionページID")
    language: str = Field(default=Language.EN, description="日記の言語.")
    title: str = Field(..., description="日記のタイトル.")
    diary_date: date | None = Field(None, description="日記の日付")
    entries: list[DiaryEntryRevision] = Field(..., description="日記のエントリの修正前後差分のリスト")



class DiaryFactory:
    """Notion APIレスポンスからドメインオブジェクトを生成するファクトリ"""

    def __init__(self):
        self.page_factory = DiaryPageFactory()
        self.entry_factory = DiaryEntryRevisionFactory()

    def from_notion(self, page: dict, children: dict) -> Diary:
        diary_page = self.page_factory.from_notion(page)

        sections = self.split_by_heading1(children)

        origin_sections = [s for s in sections if self.is_origin_entry_section(s)]
        revised_sections = [s for s in sections if self.is_revised_entry_section(s)]


        if len(origin_sections) == 0 or len(revised_sections) == 0:
            raise ValueError("No original entry section found in the diary page.")
            
        entries = self.entry_factory.from_notion(
            origin_section=origin_sections[0],
            revised_section=revised_sections[0],
        )
        return Diary(
            page_id=page.get("id"),
            title=diary_page.properties.title,
            diary_date=diary_page.properties.diary_date,
            entries=entries,
        )

    def split_by_heading1(self, children: list[dict]) -> list[dict]:
        """Heading1 単位でブロックを分割"""
        offsets = [idx for idx, block in enumerate(children) if block["type"] == NotionBlockType.HEADING1]

        ret = []
        for i in range(len(offsets)):
            s = offsets[i]
            t = offsets[i + 1] if i + 1 < len(offsets) else len(children)
            ret.append(children[s:t])
        return ret

    def is_origin_entry_section(self, blocks: list[dict]) -> bool:
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
from datetime import date
from typing import Generator

from .diary import Diary
from .diary_entry import DiaryEntry, DiaryEntryFactory
from domain.notion.notion_block import NotionBlock
from domain.notion.notion_block_type import NotionBlockType
from .diary_page import DiaryPage, DiaryPageFactory

class DiaryFactory:
    """Notion APIレスポンスからドメインオブジェクトを生成するファクトリ"""
    
    def __init__(self):
        self.page_factory = DiaryPageFactory()
        self.entry_factory = DiaryEntryFactory()
    
    def from_notion(self, page: dict, children: dict) -> Diary:
        diary_page = self.page_factory.from_notion(page)
        
        sections = self.split_by_heading1(children)
        entries = []
        for section in sections:
            if self.is_entry_section(section):
                entries = self.entry_factory.from_notion(section)

        return Diary(
            title=diary_page.properties.title,
            diary_date=diary_page.properties.diary_date,
            entries=entries,
        )
        
    
    def split_by_heading1(self, children: list[dict]) -> Generator[list[dict], None, None]:
        """Heading1 単位でブロックを分割"""
        offsets = [idx for idx, block in enumerate(children) if block["type"] == NotionBlockType.HEADING1]

        for i in range(len(offsets)):
            s = offsets[i]
            t = offsets[i + 1] if i + 1 < len(offsets) else len(children)
            yield [c for c in children[s:t]]

    def is_entry_section(self, blocks: list[dict]) -> bool:
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
        
   
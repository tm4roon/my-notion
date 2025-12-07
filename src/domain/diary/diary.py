from collections.abc import Generator
from datetime import date

from pydantic import BaseModel
from pydantic import Field

from domain.notion import NotionBlockType
from domain.language import Language

from .diary_page import DiaryPageFactory


class Diary(BaseModel):
    """日記ドメインオブジェクト"""
    page_id: str | None = Field(None, description="NotionページID")

    # properties
    title: str = Field(..., description="日記のタイトル.")
    diary_date: date | None = Field(None, description="日記の日付")
    language: str = Field(default=Language.EN, description="日記の言語.")
    # content
    content: str = Field(..., description="日記の内容（Markdown形式）.")



class DiaryFactory:
    """Notion APIレスポンスからドメインオブジェクトを生成するファクトリ"""

    def __init__(self):
        self.page_factory = DiaryPageFactory()

    def from_notion(self, page: dict, children: list[dict]) -> Diary:
        diary_page = self.page_factory.from_notion(page)

        content = self._blocks_to_markdown(children)

        return Diary(
            page_id=page.get("id"),
            title=diary_page.properties.title,
            diary_date=diary_page.properties.diary_date,
            content=content,
        )

    def _blocks_to_markdown(self, blocks: list[dict]) -> str:
        """Notionブロックのリストをmarkdownに変換"""
        markdown_lines = []
        for block in blocks:
            md_line = self._block_to_markdown(block)
            if md_line:
                markdown_lines.append(md_line)
        return "\n".join(markdown_lines)

    def _block_to_markdown(self, block: dict) -> str:
        """個々のNotionブロックをmarkdownに変換"""
        block_type = block.get("type", "")
        content = block.get(block_type, {})

        # rich_textから plain_text を取得
        rich_text = content.get("rich_text", [])
        text = "".join(rt.get("plain_text", "") for rt in rich_text)

        if block_type == NotionBlockType.HEADING1:
            return f"# {text}"
        elif block_type == NotionBlockType.HEADING2:
            return f"## {text}"
        elif block_type == NotionBlockType.HEADING3:
            return f"### {text}"
        elif block_type == NotionBlockType.PARAGRAPH:
            return text
        elif block_type == NotionBlockType.BULLETED_LIST_ITEM:
            return f"- {text}"
        elif block_type == NotionBlockType.NUMBERED_LIST_ITEM:
            return f"1. {text}"
        elif block_type == NotionBlockType.CODE:
            language = content.get("language", "")
            return f"```{language}\n{text}\n```"
        elif block_type == NotionBlockType.QUOTE:
            return f"> {text}"
        elif block_type == NotionBlockType.DIVIDER:
            return "---"
        else:
            return text
from pydantic import BaseModel
from pydantic import Field

from domain.notion import NotionBlock
from domain.notion import NotionBlockType


class DiaryEntry(BaseModel):
    """日記エントリ（Heading2 単位のセクション）"""

    title: str = Field(..., description="エントリのタイトル. HEADING2で与えられる文字列.")
    blocks: list[NotionBlock] = Field(..., description="エントリの中身.")

    @property
    def text(self) -> str:
        return "\n".join(b.plain_text for b in self.blocks)


class DiaryEntryFactory:
    def from_notion(self, obj: list[dict]) -> list[DiaryEntry]:
        return [self.create_entry(blocks) for blocks in self.split_by_entry(obj)]

    def split_by_entry(self, blocks: list[dict]) -> list[list[dict]]:
        """Heading2 単位でブロックを分割してエントリを生成"""
        offsets = [idx for idx, b in enumerate(blocks) if b.get("type", "") == NotionBlockType.HEADING2]

        res = []
        for i in range(len(offsets)):
            s = offsets[i]
            t = offsets[i + 1] if i + 1 < len(offsets) else len(blocks)
            res.append(blocks[s:t])
        return res

    def create_entry(self, obj: list[dict]) -> DiaryEntry:
        """NotionBlockのリストからDiaryEntryを生成"""
        if len(obj) == 0:
            raise ValueError("blocks must not be empty")

        head = obj[0]
        if head.get("type", "") != NotionBlockType.HEADING2:
            raise ValueError("first block must be HEADING2")

        blocks = [self.create_block(e) for e in obj]
        return DiaryEntry(
            title=blocks[0].plain_text,
            blocks=blocks[1:],
        )

    def create_block(self, obj: dict) -> NotionBlock:
        """Notion APIのレスポンスからNotionBlockを生成"""
        block_type = obj.get("type", "")
        return NotionBlock(
            object=obj.get("object", ""),
            id=obj.get("id", ""),
            type=NotionBlockType(block_type),
            content=obj.get(block_type, {}),
        )

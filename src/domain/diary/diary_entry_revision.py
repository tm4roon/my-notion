from pydantic import BaseModel
from pydantic import Field


from .diary_entry import DiaryEntry
from .diary_entry import DiaryEntryFactory

class DiaryEntryRevision(BaseModel):
    """日記エントリ（Heading2 単位のセクション）"""
    title: str = Field(..., description="エントリのタイトル.")
    origin: DiaryEntry = Field(..., description="エントリの中身.")
    revised: DiaryEntry = Field(..., description="LLMで修正したエントリの中身.")

    @property
    def origin_content(self) -> str:
        return self.origin.content

    @property
    def revised_content(self) -> str:
        return self.revised.content


class DiaryEntryRevisionFactory:
    entry_factory = DiaryEntryFactory()

    def from_notion(
            self, 
            origin_section: list[dict], 
            revised_section: list[dict],
        ) -> list[DiaryEntry]:

        origin_entries =  self.entry_factory.from_notion(origin_section)
        revised_entries = self.entry_factory.from_notion(revised_section)

        ret = []
        for org, rev in zip(origin_entries, revised_entries):
            if org.title != rev.title: # タイトルが異なる場合
                raise ValueError("Original and Revised entries must have the same title")
            ret.append(
                DiaryEntryRevision(
                    title=org.title,
                    origin=org,
                    revised=rev,
                )
            )
        return ret


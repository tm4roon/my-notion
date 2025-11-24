from datetime import date

from pydantic import BaseModel
from pydantic import Field

from domain.notion import NotionPage

COLUMN_DIARY_DATE = "diary_date"
COLUMN_TITLE = "title"


class DiaryProperties(BaseModel):
    diary_date: date | None = Field(..., description="いつの日記なのかを表す日付.")
    title: str = Field(..., description="日記のタイトル.")


class DiaryPage(NotionPage):
    properties: DiaryProperties = Field(..., description="日記DBのカラム.")


class DiaryPageFactory:
    def from_notion(self, obj: dict) -> DiaryPage:
        assert obj["object"] == "page"
        return DiaryPage(
            object="page",
            id=obj["id"],
            properties=DiaryProperties(
                title=self.extract_title(obj),
                diary_date=self.extract_date(obj),
            ),
        )

    def extract_title(self, obj: dict) -> str:
        """ページオブジェクトからタイトルを抽出"""
        properties = obj.get("properties", {})
        for prop_value in properties.values():
            if prop_value.get("type") == "title":
                title_list = prop_value.get("title", [])
                return "".join(t.get("plain_text", "") for t in title_list)
        return ""

    def extract_date(self, obj: dict) -> date | None:
        """ページオブジェクトから日付プロパティを抽出"""
        properties = obj.get("properties", {})
        if COLUMN_DIARY_DATE not in properties:
            return None

        prop = properties[COLUMN_DIARY_DATE]
        if prop.get("type") == "date" and prop.get("date"):
            s = prop["date"].get("start")
            if s:
                return date.fromisoformat(s[:10])
        return None

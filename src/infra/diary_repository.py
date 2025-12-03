from collections.abc import AsyncGenerator
from datetime import date

import httpx

from domain.diary import Diary
from domain.diary import DiaryFactory
from domain.interface import IDiaryRepository


class DiaryRepository(IDiaryRepository):
    BASE_URL = "https://api.notion.com/v1"

    def __init__(self, api_key: str, database_id: str, timeout: float = 30.0):
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json",
        }
        self.database_id = database_id
        self._timeout = timeout
        self._factory = DiaryFactory()

    async def get(
        self,
        start: date | None = None,
        end: date | None = None,
    ) -> AsyncGenerator[Diary, None]:
        async for page in self.__get_pages(start=start, end=end):
            page_id = page.get("id", None)
            if page_id is None:
                continue
            children = await self.__get_children(page_id)
            yield self._factory.from_notion(page=page, children=children)

    async def __get_children(self, page_id: str) -> list[dict]:
        """ページのコンテンツ（ブロック）とプロパティを取得"""
        async with httpx.AsyncClient(timeout=self._timeout) as client:
            res = await client.get(f"{self.BASE_URL}/blocks/{page_id}/children", headers=self.headers)
            res.raise_for_status()
        data = res.json()
        return data["results"]

    async def __get_pages(
        self,
        start: date | None = None,
        end: date | None = None,
    ) -> AsyncGenerator[dict, None]:
        """日付範囲でフィルタリングしてページを取得（半開区間 [start, end)）"""
        cursor = None

        # フィルタ構築
        filter_conditions = []
        if start:
            filter_conditions.append({"property": "diary_date", "date": {"on_or_after": start.isoformat()}})
        if end:
            filter_conditions.append({"property": "diary_date", "date": {"before": end.isoformat()}})

        async with httpx.AsyncClient(timeout=self._timeout) as client:
            while True:
                payload = {}
                if cursor:
                    payload["start_cursor"] = cursor
                if filter_conditions:
                    if len(filter_conditions) == 1:
                        payload["filter"] = filter_conditions[0]
                    else:
                        payload["filter"] = {"and": filter_conditions}

                res = await client.post(
                    f"{self.BASE_URL}/databases/{self.database_id}/query",
                    headers=self.headers,
                    json=payload,
                )
                res.raise_for_status()
                data = res.json()

                for page in data["results"]:
                    yield page
                if not data.get("has_more"):
                    break
                cursor = data["next_cursor"]

    # async def create(self, diary: Diary) -> str:
    #     """日記を作成し、作成されたページIDを返す"""
    #     properties = {
    #         "title": {"title": [{"text": {"content": diary.title}}]},
    #     }
    #     if diary.diary_date:
    #         properties["date"] = {"date": {"start": diary.diary_date.isoformat()}}

    #     children = []
    #     children.append(
    #         {
    #             "object": "block",
    #             "type": "heading_1",
    #             "heading_1": {"rich_text": [{"type": "text", "text": {"content": "Entry"}}]},
    #         }
    #     )
    #     children.append({"object": "block", "type": "divider", "divider": {}})
    #     for entry in diary.entries:
    #         children.append(
    #             {
    #                 "object": "block",
    #                 "type": "heading_2",
    #                 "heading_2": {"rich_text": [{"type": "text", "text": {"content": entry.title}}]},
    #             }
    #         )
    #         for block in entry.content_blocks:
    #             block_data = {
    #                 "object": "block",
    #                 "type": block.block_type.value,
    #                 block.block_type.value: block.content,
    #             }
    #             children.append(block_data)

    #     payload = {
    #         "parent": {"database_id": self.database_id},
    #         "properties": properties,
    #         "children": children,
    #     }

    #     import json

    #     async with httpx.AsyncClient(timeout=self._timeout) as client:
    #         response = await client.post(
    #             f"{self.BASE_URL}/pages",
    #             headers=self.headers,
    #             json=payload,
    #         )
    #         response.raise_for_status()
    #         return response.json()["id"]

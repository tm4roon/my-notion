"""DiaryのmarkdownコンテンツからDiaryEntryRevisionを生成するユースケース"""
from domain.diary import Diary
from domain.diary.diary_entry import DiaryEntry
from domain.diary.diary_entry_revision import DiaryEntryRevision


class ParseDiaryContentToRevisions:
    """DiaryのmarkdownからDiaryEntryRevisionのリストを生成"""

    def invoke(self, diary: Diary) -> list[DiaryEntryRevision]:
        """
        DiaryのmarkdownをパースしてDiaryEntryRevisionのリストを生成

        Diaryのcontentは以下のような構造を想定:
        # Entry
        ## Section 1
        content...
        ## Section 2
        content...

        # Revised Entry
        ## Section 1
        revised content...
        ## Section 2
        revised content...
        """
        sections = self._split_by_h1(diary.content)

        origin_section = None
        revised_section = None

        for section in sections:
            title = self._extract_h1_title(section)
            if title == "Entry":
                origin_section = section
            elif title.startswith("Revised"):
                revised_section = section

        if not origin_section or not revised_section:
            raise ValueError("Diary must have both 'Entry' and 'Revised' sections")

        origin_entries = self._parse_entries(origin_section)
        revised_entries = self._parse_entries(revised_section)

        if len(origin_entries) != len(revised_entries):
            raise ValueError("Origin and Revised sections must have the same number of entries")

        revisions = []
        for origin, revised in zip(origin_entries, revised_entries):
            if origin.title != revised.title:
                raise ValueError(f"Entry titles must match: {origin.title} != {revised.title}")

            revisions.append(DiaryEntryRevision(
                title=origin.title,
                origin=origin,
                revised=revised,
            ))

        return revisions

    def _split_by_h1(self, markdown: str) -> list[str]:
        """# で始まる行でmarkdownを分割"""
        lines = markdown.split('\n')
        sections = []
        current_section = []

        for line in lines:
            if line.startswith('# ') and not line.startswith('## '):
                if current_section:
                    sections.append('\n'.join(current_section))
                current_section = [line]
            else:
                current_section.append(line)

        if current_section:
            sections.append('\n'.join(current_section))

        return sections

    def _extract_h1_title(self, section: str) -> str:
        """セクションの最初の# 行からタイトルを抽出"""
        lines = section.strip().split('\n')
        if lines and lines[0].startswith('# '):
            return lines[0][2:].strip()
        return ""

    def _parse_entries(self, section: str) -> list[DiaryEntry]:
        """セクション内の## で区切られたエントリをパース"""
        lines = section.split('\n')
        entries = []
        current_title = None
        current_content = []

        for line in lines:
            if line.startswith('## '):
                # 前のエントリを保存
                if current_title is not None:
                    entries.append(DiaryEntry(
                        title=current_title,
                        content='\n'.join(current_content).strip()
                    ))

                # 新しいエントリを開始
                current_title = line[3:].strip()
                current_content = []
            elif current_title is not None and not line.startswith('# '):
                # タイトル行(#)はスキップ
                current_content.append(line)

        # 最後のエントリを保存
        if current_title is not None:
            entries.append(DiaryEntry(
                title=current_title,
                content='\n'.join(current_content).strip()
            ))

        return entries

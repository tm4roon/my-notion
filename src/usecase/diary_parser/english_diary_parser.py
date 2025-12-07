import stanza
from domain.diary.diary import Diary
from domain.diary.diary_entry_revision import DiaryEntry
from domain.diary.parsed_diary_entry import ParsedDiaryEntry
from domain.language import Language

class EnglishDiaryEntryParser:
    def __init__(self):
        # Stanzaのパイプラインを初期化（トークン化、品詞タグ付け、lemmatizationを含む）
        self.nlp = stanza.Pipeline(
            'en', 
            processors='tokenize,pos,lemma', 
            download_method=None, 
            verbose=False
        )

    def invoke(self, entry: DiaryEntry) -> ParsedDiaryEntry:
        """エントリのテキストを文単位に分割し、lemmaとPOSタグも抽出"""
        content = entry.content
        # Stanzaで文に分割
        doc = self.nlp(content)
        sentences = [
            " ".join([w.text.lower() for w in s.words])
            for s in doc.sentences
        ]
        # lemmaを抽出（全単語のlemmaを小文字で取得）
        lemmas = [
            " ".join([word.lemma.lower() for word in sentence.words])
            for sentence in doc.sentences
        ]
        # POSタグを抽出
        pos_tags = [
            " ".join([word.pos for word in sentence.words])
            for sentence in doc.sentences
        ]

        return ParsedDiaryEntry(
            sentences=sentences, 
            lemmas=lemmas, 
            pos_tags=pos_tags,
        )
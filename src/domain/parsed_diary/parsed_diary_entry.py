from pydantic import BaseModel, Field
 

class ParsedDiaryEntry(BaseModel):
    parser_name: str = Field(default="stanza", description="使用したパーサーの名前")
    sentences: list[str] = Field(default_factory=list, description="日記エントリの文のリスト. 文はスペース区切りの単語列として表現される.")
    lemmas: list[str] = Field(default_factory=list, description="日記エントリの単語の原形のリスト. 単語はスペース区切りの単語列として表現される.")
    pos_tags: list[str] = Field(default_factory=list, description="日記エントリの品詞タグのリスト. 品詞タグはスペース区切りのタグ列として表現される.")

    @property
    def vocab(self) -> set[str]:
        """日記エントリ内のユニークな単語の集合を返すプロパティ"""
        unique_words = set()
        for lemma_sentence in self.lemmas:
            words = lemma_sentence.split()
            unique_words.update(words)
        return unique_words

    @property
    def n_sentences(self) -> int:
        """日記エントリ内の文の数を返すプロパティ"""
        return len(self.sentences)

    @property
    def n_words(self) -> int:
        """日記エントリ内の単語の数を返すプロパティ"""
        return sum(len(s.split()) for s in self.lemmas)

 
    def vocab_size(self) -> int:
        """日記エントリ内のユニークな単語の数を返すプロパティ"""
        return len(self.vocab)

    @property
    def avg_words_per_sentence(self) -> float:
        """日記エントリ内の平均単語数/文を返すプロパティ"""
        if self.n_sentences == 0:
            return 0.0
        return self.n_words() / self.n_sentences


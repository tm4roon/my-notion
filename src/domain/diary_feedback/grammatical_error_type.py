from enum import StrEnum


class GrammaticalErrorType(StrEnum):
    ARTICLE = "article" # 冠詞
    PREPOSITION = "preposition" # 前置詞
    PRONOUN = "pronoun" # 代名詞
    SPELLING = "spelling" # スペルミス
    TENSE = "tense" # 時制
    WORD_CHOICE = "word_choice" # 語彙選択
    WORD_ORDER = "word_order" # 語順
    SUBJECT_VERB_AGREEMENT = "subject_verb_agreement" # 主語と動詞の一致
    VERB_FORM = "verb_form" # 動詞の形
    OTHER = "other" # その他

    def description(self) -> str:
        descriptions = {
            GrammaticalErrorType.ARTICLE: "a/an/theの使い方の誤り",
            GrammaticalErrorType.PREPOSITION: "in/on/at/for/toなどの前置詞の誤用",
            GrammaticalErrorType.PRONOUN: "he/she/it/they/him/herなどの代名詞の誤り",
            GrammaticalErrorType.SPELLING: "単語のつづりの間違い",
            GrammaticalErrorType.TENSE: "過去形・現在形・未来形などの時制の誤り",
            GrammaticalErrorType.WORD_CHOICE: "文脈に合わない単語の選択",
            GrammaticalErrorType.WORD_ORDER: "単語の並び順の誤り",
            GrammaticalErrorType.SUBJECT_VERB_AGREEMENT: "主語の単数/複数と動詞の形の不一致",
            GrammaticalErrorType.VERB_FORM: "不定詞・動名詞・分詞などの動詞形態の誤り",
            GrammaticalErrorType.OTHER: "上記に分類できないその他の文法エラー",
        }
        return descriptions[self]
    
    def name(self) -> str:
        names = {
            GrammaticalErrorType.ARTICLE: "冠詞",
            GrammaticalErrorType.PREPOSITION: "前置詞",
            GrammaticalErrorType.PRONOUN: "代名詞",
            GrammaticalErrorType.SPELLING: "スペルミス",
            GrammaticalErrorType.TENSE: "時制",
            GrammaticalErrorType.WORD_CHOICE: "語彙選択",
            GrammaticalErrorType.WORD_ORDER: "語順",
            GrammaticalErrorType.SUBJECT_VERB_AGREEMENT: "主語と動詞の一致",
            GrammaticalErrorType.VERB_FORM: "動詞の形",
            GrammaticalErrorType.OTHER: "その他",
        }
        return names[self]
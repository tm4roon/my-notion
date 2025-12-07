
from domain.diary.diary_entry import DiaryEntry
from domain.diary_feedback.diary_entry_stats import DiaryEntryStats
from usecase.nlp_diary_entry import NLPDiaryEntryBase 


class CalculateDiaryStats:
    def __init__(self, nlp: NLPDiaryEntryBase):
        self.nlp = nlp

    def invoke(self, entry: DiaryEntry) -> DiaryEntryStats:
        parsed_entry = self.nlp.invoke(entry)
        n_sentences = len(parsed_entry.sentences)

        total_words = sum(len(sentence.split(" ")) for sentence in parsed_entry.sentences)

        vocab = set()
        for sentence in parsed_entry.lemmas:
            for word in sentence.split(" "):
                vocab.add(word.lower())

        ret = DiaryEntryStats(
            vocab=vocab,
            n_words=total_words,
            n_sentences=n_sentences,
        )
        return ret
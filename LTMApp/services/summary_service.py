# long_term_memory_app/app/services/summary_service.py

import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from heapq import nlargest

nlp = spacy.load("en_core_web_md")


def summarize_conversation(conversation_text, summary_length=5):
    doc = nlp(conversation_text)
    sentences = list(doc.sents)
    if len(sentences) < summary_length:
        # If the conversation is shorter than the desired summary, return it as is
        return conversation_text

    # Calculate sentence scores based on word frequencies (excluding stop words and punctuation)
    word_frequencies = {}
    for word in doc:
        if word.text.lower() not in STOP_WORDS and not word.is_punct:
            if word.text not in word_frequencies.keys():
                word_frequencies[word.text] = 1
            else:
                word_frequencies[word.text] += 1

    max_frequency = max(word_frequencies.values())
    for word in word_frequencies.keys():
        word_frequencies[word] = word_frequencies[word] / max_frequency

    sentence_scores = {}
    for sent in doc.sents:
        for word in sent:
            if word.text in word_frequencies.keys():
                if sent not in sentence_scores.keys():
                    sentence_scores[sent] = word_frequencies[word.text]
                else:
                    sentence_scores[sent] += word_frequencies[word.text]

    # Select the top N sentences with the highest scores
    summarized_sentences = nlargest(summary_length, sentence_scores, key=sentence_scores.get)
    final_summary = " ".join([sent.text for sent in summarized_sentences])

    return final_summary

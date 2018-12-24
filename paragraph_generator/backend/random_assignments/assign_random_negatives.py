import random

from paragraph_generator.tags.status_tag import StatusTag
from paragraph_generator.word_groups.paragraph import Paragraph
from paragraph_generator.words.verb import Verb


def assign_random_negatives(paragraph: Paragraph, p_negative):
    out = paragraph
    for s_index, w_index, word in paragraph.indexed_all_words():
        if isinstance(word, Verb) and random.random() < p_negative:
            out = out.set(s_index, w_index, word.negative())
    return out.set_tags(paragraph.tags.add(StatusTag.HAS_NEGATIVES))

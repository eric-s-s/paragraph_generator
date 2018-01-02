from sentences.words.pronoun import Pronoun
from sentences.words.verb import Verb
from sentences.words.noun import Noun, PluralNoun
from sentences.words.word import Word


def requires_third_person(raw_sentence) -> bool:
    index = find_subject(raw_sentence)
    if index == -1:
        return False
    return is_third_person(raw_sentence[index])


def find_subject(raw_sentence) -> int:
    index = -1
    for i, val in enumerate(raw_sentence):
        if isinstance(val, Verb):
            index = i - 1
            break
    return index


def is_third_person(word) -> bool:
    if isinstance(word, Pronoun):
        return word in (Pronoun.HE, Pronoun.HIM, Pronoun.SHE, Pronoun.HER, Pronoun.IT)
    if isinstance(word, Noun):
        return not isinstance(word, PluralNoun)
    return word in [Word('He'), Word('She'), Word('It')]


def is_word_in_sentence(word, raw_sentence):
    if isinstance(word, Pronoun):
        return any(word.is_pair(element) for element in raw_sentence)
    return word in raw_sentence
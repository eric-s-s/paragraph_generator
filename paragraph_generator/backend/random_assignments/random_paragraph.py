import random
from typing import List

from paragraph_generator.backend.random_assignments.random_sentences import RandomSentences
from paragraph_generator.tags.status_tag import StatusTag
from paragraph_generator.tags.tags import Tags
from paragraph_generator.word_groups.paragraph import Paragraph
from paragraph_generator.word_groups.verb_group import VerbGroup
from paragraph_generator.words.noun import Noun
from paragraph_generator.words.pronoun import Pronoun
from paragraph_generator.words.wordtools.abstractword import AbstractWord


class RandomParagraph(object):
    def __init__(self, probability_pronoun, verb_list: List[VerbGroup], noun_list: List[Noun]):
        self._p_pronoun = probability_pronoun
        self._word_maker = RandomSentences(verb_list, noun_list)
        self._raw_tag = Tags([StatusTag.RAW])

    def get_subject_pool(self, size) -> List[AbstractWord]:
        pool = []
        safety_count = 0
        safety_limit = 100 + size
        while len(pool) < size:
            new_subj = self._word_maker.subject(self._p_pronoun)
            if new_subj not in pool:
                pool.append(new_subj)
            else:
                safety_count += 1
                if safety_count > safety_limit:
                    raise ValueError('pool size is too large for available nouns loaded from file')
        return pool

    def create_pool_paragraph(self, pool_size: int, num_sentences: int) -> Paragraph:
        subjects = self.get_subject_pool(pool_size)

        sentences = []
        for _ in range(num_sentences):
            subj = random.choice(subjects)
            sentences.append(self._word_maker.sentence(subj, self._p_pronoun))
        return Paragraph(sentences, self._raw_tag)

    def create_chain_paragraph(self, num_sentences: int) -> Paragraph:
        sentences = []

        new_subj = self._word_maker.subject(self._p_pronoun)
        for _ in range(num_sentences):
            sentence = self._word_maker.sentence(new_subj, self._p_pronoun)
            sentences.append(sentence)
            subj_candidate = sentence.get(-2)
            if isinstance(subj_candidate, Pronoun):
                new_subj = subj_candidate.subject()
            elif isinstance(subj_candidate, Noun):
                new_subj = subj_candidate
            else:
                new_subj = self._word_maker.subject(self._p_pronoun)

        return Paragraph(sentences, self._raw_tag)

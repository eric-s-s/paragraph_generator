from abc import ABC, abstractmethod
from typing import List

from paragraph_generator.word_groups.verb_group import VerbGroup
from paragraph_generator.words.basicword import BasicWord
from paragraph_generator.words.noun import Noun
from paragraph_generator.words.verb import Verb


class AbstractWordLists(ABC):
    @property
    @abstractmethod
    def verbs(self) -> List[VerbGroup]:
        raise NotImplementedError

    @property
    @abstractmethod
    def nouns(self) -> List[Noun]:
        raise NotImplementedError


class WordLists(object):
    def __init__(self, verbs=None, countable=None, uncountable=None, static=None):
        """

        :param verbs: {'verb': str, 'irregular_past': str, 'preposition': str, 'particle': str, 'objects': int}
        :param countable: {'noun': str, 'irregular_plural': str}
        :param uncountable: {'noun': str}
        :param static: {'noun': str, 'is_plural': bool}
        """
        self._verbs = verbs if verbs else []
        self._countable = countable if countable else []
        self._uncountable = uncountable if uncountable else []
        self._static = static if static else []

    @property
    def verbs(self):
        return self._generate_verb_groups()

    @property
    def nouns(self):
        return self._generate_countable() + self._generate_uncountable() + self._generate_static()

    def _generate_verb_groups(self):
        return [_generate_verb_group(verb_json) for verb_json in self._verbs]

    def _generate_countable(self):
        return [Noun(el['noun'], irregular_plural=el['irregular_plural']) for el in self._countable]

    def _generate_uncountable(self):
        return [Noun.uncountable_noun(el['noun']) for el in self._uncountable]

    def _generate_static(self):
        return [Noun.proper_noun(el['noun'], el['is_plural']) for el in self._static]


def _generate_verb_group(verb_json):
    """
    :param verb_json: keys='verb', 'irregular_past', 'objects', 'preposition', 'particle'
    :return: VerbGroup
    """
    verb = Verb(verb_json['verb'], irregular_past=verb_json['irregular_past'])
    objects = verb_json['objects']

    preposition = BasicWord.preposition(verb_json['preposition'])
    particle = BasicWord.particle((verb_json['particle']))

    if preposition.value == '':
        preposition = None
    if particle.value == '':
        particle = None

    return VerbGroup(verb=verb, objects=objects, preposition=preposition, particle=particle)

from abc import ABCMeta
from enum import Enum

from paragraph_generator.tags.tags import Tags
from paragraph_generator.tags.wordtag import WordTag
from paragraph_generator.words.basicword import BasicWord
from paragraph_generator.words.wordtools.abstractword import AbstractWord
from paragraph_generator.words.wordtools.common_functions import bold


class BeVerb(Enum):
    BE = 'be'

    IS = 'is'
    AM = 'am'
    ARE = 'are'

    IS_NOT = 'is not'
    AM_NOT = 'am not'
    ARE_NOT = 'are not'

    WAS = 'was'
    WERE = 'were'

    WAS_NOT = 'was not'
    WERE_NOT = 'were not'

    @property
    def tags(self) -> Tags:
        tag_list = []
        if 'IS' in self.name:
            tag_list.append(WordTag.THIRD_PERSON)
        if 'NOT' in self.name:
            tag_list.append(WordTag.NEGATIVE)
        if 'WAS' in self.name or 'WERE' in self.name:
            tag_list.append(WordTag.PAST)
        return Tags(tag_list)

    def has_tags(self, *tags: WordTag) -> bool:
        return all(self.tags.has(tag) for tag in tags)

    def capitalize(self) -> AbstractWord:
        return BasicWord(self.value.capitalize())

    def de_capitalize(self) -> 'BeVerb':
        return self

    def bold(self) -> AbstractWord:
        return BasicWord(bold(self.value))

    def negative(self):
        if self.has_tags(WordTag.NEGATIVE) or self == BeVerb.BE:
            return self
        return getattr(self, '{}_NOT'.format(self.name))

    def past_tense(self):
        if self.has_tags(WordTag.PAST):
            return self
        new_name = self.name
        pairs = {'AM': 'WAS', 'IS': 'WAS', 'ARE': 'WERE'}
        for present, past in pairs.items():
            new_name = new_name.replace(present, past)
        return getattr(self, new_name)


ABCMeta.register(AbstractWord, BeVerb)

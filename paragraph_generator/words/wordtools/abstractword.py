from abc import ABC, abstractmethod

from paragraph_generator.tags.tags import Tags
from paragraph_generator.tags.wordtag import WordTag


class AbstractWord(ABC):

    @property
    @abstractmethod
    def value(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def tags(self) -> Tags:
        raise NotImplementedError

    @abstractmethod
    def capitalize(self) -> 'AbstractWord':
        raise NotImplementedError

    @abstractmethod
    def de_capitalize(self) -> 'AbstractWord':
        raise NotImplementedError

    @abstractmethod
    def bold(self) -> 'AbstractWord':
        raise NotImplementedError

    def has_tags(self, *tags: WordTag) -> bool:
        owned_tags = self.tags
        return all(owned_tags.has(tag) for tag in tags)

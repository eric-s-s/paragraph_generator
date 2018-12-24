
from abc import ABC, abstractmethod
from paragraph_generator.tags.tags import Tags
from paragraph_generator.tags.wordtag import WordTag


class AbstractWord(ABC):

    @property
    @abstractmethod
    def value(self) -> str:
        pass

    @property
    @abstractmethod
    def tags(self) -> Tags:
        pass

    @abstractmethod
    def capitalize(self) -> 'AbstractWord':
        pass

    @abstractmethod
    def de_capitalize(self) -> 'AbstractWord':
        pass

    @abstractmethod
    def bold(self) -> 'AbstractWord':
        pass

    def has_tags(self, *tags: WordTag) -> bool:
        owned_tags = self.tags
        return all(owned_tags.has(tag) for tag in tags)

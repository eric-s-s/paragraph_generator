from typing import Optional

from paragraph_generator.words.basicword import BasicWord
from paragraph_generator.words.verb import Verb


class VerbGroup(object):
    def __init__(self, verb: Verb, preposition: Optional[BasicWord], particle: Optional[BasicWord], objects: int):
        self._verb = verb
        self._preposition = preposition
        self._particle = particle
        self._objects = objects

    @property
    def verb(self):
        return self._verb

    @property
    def preposition(self):
        return self._preposition

    @property
    def particle(self):
        return self._particle

    @property
    def objects(self):
        return self._objects

    def __eq__(self, other):
        if not isinstance(other, VerbGroup):
            return False
        return (self.verb, self.preposition, self.particle, self.objects) == (
            other.verb, other.preposition, other.particle, other.objects)

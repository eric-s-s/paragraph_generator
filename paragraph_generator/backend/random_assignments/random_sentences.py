import random
from typing import List

from paragraph_generator.tags.wordtag import WordTag
from paragraph_generator.word_groups.sentence import Sentence
from paragraph_generator.word_groups.verb_group import VerbGroup
from paragraph_generator.words.noun import Noun
from paragraph_generator.words.pronoun import Pronoun
from paragraph_generator.words.punctuation import Punctuation
from paragraph_generator.words.wordtools.abstractword import AbstractWord


class RandomSentences(object):
    def __init__(self, verb_list: List[VerbGroup], noun_list: List[Noun]):
        self._pronouns = list(Pronoun.__members__.values())
        self._endings = [Punctuation.PERIOD, Punctuation.PERIOD, Punctuation.EXCLAMATION]

        self._verbs = verb_list[:]  # type: List[VerbGroup]
        self._nouns = noun_list[:]  # type: List[Noun]
        self._check_empty_lists()

    def _check_empty_lists(self):
        if not self._verbs:
            raise ValueError('There are no verbs in the verb list.')
        if not self._nouns:
            raise ValueError('There are no nouns in any of the nouns lists.')

    def sentence(self, subject: AbstractWord, p_pronoun=0.2):
        p_pronoun = min(max(p_pronoun, 0), 1)
        to_test = subject
        if isinstance(subject, Pronoun):
            to_test = subject.object()

        max_loops_until_repeats_allowed = 100
        predicate = self.predicate(p_pronoun)  # linter issue
        for _ in range(max_loops_until_repeats_allowed):
            if to_test not in predicate:
                break
            predicate = self.predicate(p_pronoun)
        predicate.insert(0, subject)
        return Sentence(predicate)

    def predicate(self, p_pronoun=0.2):
        p_pronoun = min(max(p_pronoun, 0), 1)

        verb_group = random.choice(self._verbs)

        objects = self._get_objects(verb_group.objects, p_pronoun)

        predicate = assign_objects(verb_group, objects)

        predicate.append(random.choice(self._endings))
        return predicate

    def _get_objects(self, object_count, p_pronoun):
        objects = []
        loop_count = 0
        max_loops_until_repeats_allowed = 100
        while len(objects) < object_count:
            if not objects:
                new_obj = self.object(p_pronoun)
            else:
                new_obj = self.object(p_pronoun=0)

            if new_obj not in objects or loop_count > max_loops_until_repeats_allowed:
                objects.append(new_obj)

            loop_count += 1
        return objects

    def subject(self, p_pronoun):
        if random.random() < p_pronoun:
            return random.choice(self._pronouns).subject()
        else:
            return random.choice(self._nouns)

    def object(self, p_pronoun):
        if random.random() < p_pronoun:
            return random.choice(self._pronouns).object()
        else:
            return random.choice(self._nouns)


def assign_objects(verb_group: VerbGroup, objects: List[AbstractWord]):
    preposition = [verb_group.preposition]
    separable_particle = [verb_group.particle]
    predicate = [verb_group.verb]  # type: List[AbstractWord]

    while objects:
        obj = objects.pop()
        if len(preposition) < 2:
            preposition.append(obj)
        elif isinstance(obj, Pronoun):
            separable_particle.insert(0, obj)
        else:
            separable_particle.append(obj)
    if does_preposition_precede_separable_particle(preposition, separable_particle):
        answer = predicate + preposition + separable_particle
    else:
        answer = predicate + separable_particle + preposition

    return [word for word in answer if word is not None]


def does_preposition_precede_separable_particle(preposition, separable_particle):
    lacks_preposition = None in preposition
    only_separable_particle = (
            None not in separable_particle and
            all(word.has_tags(WordTag.SEPARABLE_PARTICLE) for word in separable_particle)
    )
    preposition_with_pronoun = any(isinstance(word, Pronoun) for word in preposition)
    return lacks_preposition and only_separable_particle and preposition_with_pronoun

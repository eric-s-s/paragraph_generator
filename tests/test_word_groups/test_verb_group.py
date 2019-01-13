import unittest

from paragraph_generator.word_groups.verb_group import VerbGroup
from paragraph_generator.words.basicword import BasicWord
from paragraph_generator.words.verb import Verb


class TestVerbGroup(unittest.TestCase):
    def test_init_with_values(self):
        verb = Verb('go')
        preposition = BasicWord.preposition('with')
        particle = BasicWord.particle('away')
        to_test = VerbGroup(
            verb=verb,
            preposition=preposition,
            particle=particle,
            objects=2)
        self.assertEqual(to_test.verb, verb)
        self.assertEqual(to_test.preposition, preposition)
        self.assertEqual(to_test.particle, particle)
        self.assertEqual(to_test.objects, 2)

    def test_init_with_none_values(self):
        verb = Verb('go')
        objects = 0
        to_test = VerbGroup(
            verb=verb,
            preposition=None,
            particle=None,
            objects=objects
        )
        self.assertEqual(to_test.verb, verb)
        self.assertIsNone(to_test.preposition)
        self.assertIsNone(to_test.particle)
        self.assertEqual(to_test.objects, objects)

import unittest

from paragraph_generator.word_groups.verb_group import VerbGroup
from paragraph_generator.words.basicword import BasicWord
from paragraph_generator.words.noun import Noun
from paragraph_generator.words.verb import Verb


class WordListsGenerator(object):
    def __init__(self, verbs=None, countable=None, uncountable=None, static=None):
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


class TestWordListsGenerator(unittest.TestCase):
    def assert_unordered_lists(self, first, second):
        for el in first:
            self.assertIn(el, second)
        self.assertEqual(len(first), len(second))

    def test_init_empty(self):
        lists = WordListsGenerator()
        self.assertEqual(lists.verbs, [])
        self.assertEqual(lists.nouns, [])

    def test_init_verbs(self):
        verbs = [{'verb': 'take', 'irregular_past': 'took', 'objects': 2,
                  'particle': 'away', 'preposition': 'with'},
                 {'verb': 'play', 'irregular_past': '', 'objects': 1,
                  'particle': '', 'preposition': ''}]

        lists = WordListsGenerator(verbs=verbs)

        expected_verbs = [VerbGroup(verb=Verb('take', 'took'), preposition=BasicWord.preposition('with'),
                                    particle=BasicWord.particle('away'), objects=2),
                          VerbGroup(verb=Verb('play'), preposition=None, particle=None,
                                    objects=1)]
        self.assert_unordered_lists(lists.verbs, expected_verbs)
        self.assertEqual(lists.nouns, [])

    def test_init_countable_nouns(self):
        countable_nouns = [{'noun': 'dog', 'irregular_plural': ''},
                           {'noun': 'child', 'irregular_plural': 'children'}]

        lists = WordListsGenerator(countable=countable_nouns)
        expected = [Noun('dog'), Noun('child', 'children')]
        self.assert_unordered_lists(lists.nouns, expected)
        self.assertEqual(lists.verbs, [])

    def test_init_uncountable_nouns(self):
        uncountable_nouns = [{'noun': 'water'}, {'noun': 'air'}]

        lists = WordListsGenerator(uncountable=uncountable_nouns)
        expected = [Noun.uncountable_noun('water'), Noun.uncountable_noun('air')]
        self.assert_unordered_lists(lists.nouns, expected)
        self.assertEqual(lists.verbs, [])

    def test_init_static_nouns(self):
        static_nouns = [{'noun': 'the Dude', 'is_plural': False},
                        {'noun': 'the Joneses', 'is_plural': True}]
        lists = WordListsGenerator(static=static_nouns)

        expected_nouns = [Noun.proper_noun('the Dude', plural=False),
                          Noun.proper_noun('the Joneses', plural=True)]
        self.assert_unordered_lists(expected_nouns, lists.nouns)
        self.assertEqual(lists.verbs, [])

    def test_init_all_types(self):
        verbs = [{'verb': 'play', 'irregular_past': '', 'preposition': '', 'particle': '', 'objects': 1}]
        countable = [{'noun': 'dog', 'irregular_plural': ''}]
        uncountable = [{'noun': 'water'}]
        static = [{'noun': 'Joe', 'is_plural': False}]

        lists = WordListsGenerator(verbs=verbs, countable=countable, uncountable=uncountable, static=static)
        expected_verbs = [VerbGroup(Verb('play'), None, None, 1)]
        expected_nouns = [Noun('dog'), Noun.uncountable_noun('water'), Noun.proper_noun('Joe')]
        self.assert_unordered_lists(lists.verbs, expected_verbs)
        self.assert_unordered_lists(lists.nouns, expected_nouns)

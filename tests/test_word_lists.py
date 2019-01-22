import unittest

from paragraph_generator.word_groups.verb_group import VerbGroup
from paragraph_generator.word_lists import WordLists, AbstractWordLists
from paragraph_generator.words.basicword import BasicWord
from paragraph_generator.words.noun import Noun
from paragraph_generator.words.verb import Verb


class TestWordLists(unittest.TestCase):
    def assert_unordered_lists(self, first, second):
        for el in first:
            self.assertIn(el, second)
        self.assertEqual(len(first), len(second))

    def test_regression_test_isinstance_AbstractWordList(self):
        self.assertIsInstance(WordLists(), AbstractWordLists)

    def test_init_empty(self):
        lists = WordLists()
        self.assertEqual(lists.verbs, [])
        self.assertEqual(lists.nouns, [])

    def test_init_verbs(self):
        verbs = [{'verb': 'take', 'irregular_past': 'took', 'objects': 2,
                  'particle': 'away', 'preposition': 'with'},
                 {'verb': 'play', 'irregular_past': '', 'objects': 1,
                  'particle': '', 'preposition': ''}]

        lists = WordLists(verbs=verbs)

        expected_verbs = [VerbGroup(verb=Verb('take', 'took'), preposition=BasicWord.preposition('with'),
                                    particle=BasicWord.particle('away'), objects=2),
                          VerbGroup(verb=Verb('play'), preposition=None, particle=None,
                                    objects=1)]
        self.assert_unordered_lists(lists.verbs, expected_verbs)
        self.assertEqual(lists.nouns, [])

    def test_init_countable_nouns(self):
        countable_nouns = [{'noun': 'dog', 'irregular_plural': ''},
                           {'noun': 'child', 'irregular_plural': 'children'}]

        lists = WordLists(countable=countable_nouns)
        expected = [Noun('dog'), Noun('child', 'children')]
        self.assert_unordered_lists(lists.nouns, expected)
        self.assertEqual(lists.verbs, [])

    def test_init_uncountable_nouns(self):
        uncountable_nouns = [{'noun': 'water', 'definite': True}, {'noun': 'air', 'definite': False}]

        lists = WordLists(uncountable=uncountable_nouns)
        expected = [Noun.uncountable_noun('water').definite(), Noun.uncountable_noun('air')]
        self.assert_unordered_lists(lists.nouns, expected)
        self.assertEqual(lists.verbs, [])

    def test_init_static_nouns(self):
        static_nouns = [{'noun': 'the Dude', 'is_plural': False},
                        {'noun': 'the Joneses', 'is_plural': True}]
        lists = WordLists(static=static_nouns)

        expected_nouns = [Noun.proper_noun('the Dude', plural=False),
                          Noun.proper_noun('the Joneses', plural=True)]
        self.assert_unordered_lists(expected_nouns, lists.nouns)
        self.assertEqual(lists.verbs, [])

    def test_init_all_types(self):
        verbs = [{'verb': 'play', 'irregular_past': '', 'preposition': '', 'particle': '', 'objects': 1}]
        countable = [{'noun': 'dog', 'irregular_plural': ''}]
        uncountable = [{'noun': 'water', 'definite': False}]
        static = [{'noun': 'Joe', 'is_plural': False}]

        lists = WordLists(verbs=verbs, countable=countable, uncountable=uncountable, static=static)
        expected_verbs = [VerbGroup(Verb('play'), None, None, 1)]
        expected_nouns = [Noun('dog'), Noun.uncountable_noun('water'), Noun.proper_noun('Joe')]
        self.assert_unordered_lists(lists.verbs, expected_verbs)
        self.assert_unordered_lists(lists.nouns, expected_nouns)

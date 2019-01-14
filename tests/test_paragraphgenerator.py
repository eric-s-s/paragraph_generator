import random
import unittest
from collections import namedtuple

from paragraph_generator.paragraphsgenerator import ParagraphsGenerator
from paragraph_generator.tags.wordtag import WordTag
from paragraph_generator.word_groups.verb_group import VerbGroup
from paragraph_generator.words.basicword import BasicWord
from paragraph_generator.words.noun import Noun
from paragraph_generator.words.pronoun import AbstractPronoun
from paragraph_generator.words.verb import Verb


def count_word_tags(answer, tag):
    count = 0
    for word in answer.all_words():  # type: BasicWord
        count += word.has_tags(tag)
    return count


def count_nouns_and_pronouns(answer):
    nouns = 0
    pronouns = 0
    for word in answer.all_words():
        if isinstance(word, Noun):
            nouns += 1
        if isinstance(word, AbstractPronoun):
            pronouns += 1
    return nouns, pronouns


WordLists = namedtuple('WordLists', ['nouns', 'verbs'])


class TestParagraphsGenerator(unittest.TestCase):
    def setUp(self):
        self.config_state = {
            'error_probability': 1.0,
            'noun_errors': True,
            'pronoun_errors': True,
            'verb_errors': True,
            'is_do_errors': True,
            'preposition_transpose_errors': True,
            'punctuation_errors': True,

            'tense': 'simple_present',
            'probability_plural_noun': 1.0,
            'probability_negative_verb': 1.0,
            'probability_pronoun': 1.0,

            'paragraph_type': 'chain',
            'subject_pool': 1,
            'paragraph_size': 1,
        }

        self.verbs = [
            VerbGroup(Verb('go'), BasicWord.preposition('with'), BasicWord.particle('away'), 1),
            VerbGroup(Verb('eat'), None, None, 1)
        ]
        self.countable_nouns = [Noun('dog'), Noun('cat')]
        self.uncountable_nouns = [Noun.uncountable_noun('water'), Noun.uncountable_noun('air')]
        self.static_nouns = [Noun.proper_noun('Joe'), Noun.proper_noun('The Dude')]
        self.word_lists = WordLists(nouns=self.countable_nouns, verbs=self.verbs)

    def test_init_default_config_state(self):
        default = {
            'error_probability': 0.2,
            'noun_errors': True,
            'pronoun_errors': True,
            'verb_errors': True,
            'punctuation_errors': True,
            'is_do_errors': False,
            'preposition_transpose_errors': False,

            'tense': 'simple_present',
            'probability_plural_noun': 0.2,
            'probability_negative_verb': 0.3,
            'probability_pronoun': 0.3,

            'paragraph_type': 'chain',
            'subject_pool': 5,
            'paragraph_size': 15,
        }
        to_test = ParagraphsGenerator({}, self.word_lists)
        for key, value in default.items():
            self.assertEqual(to_test.get(key), value)

    def test_init(self):
        to_test = ParagraphsGenerator(self.config_state, self.word_lists)
        for key, value in self.config_state.items():
            self.assertEqual(to_test.get(key), value)

        self.assertEqual(to_test.get_nouns(), self.word_lists.nouns)
        self.assertEqual(to_test.get_verbs(), self.word_lists.verbs)

    def test_generate_paragraphs_paragraph_size(self):
        for paragraph_size in range(1, 5):
            config = {'paragraph_size': paragraph_size}
            answer, error = ParagraphsGenerator(config, self.word_lists).generate_paragraphs()
            self.assertEqual(len(answer), paragraph_size)
            self.assertEqual(len(error), paragraph_size)

    def test_generate_paragraphs_probability_pronouns_zero(self):
        config = {'probability_pronoun': 0.0, 'paragraph_size': 1}
        to_test = ParagraphsGenerator(config, self.word_lists)
        answer, error = to_test.generate_paragraphs()
        nouns, pronouns = count_nouns_and_pronouns(answer)
        self.assertEqual(nouns, 2)
        self.assertEqual(pronouns, 0)

    def test_generate_paragraphs_probability_pronouns_one(self):
        config = {'probability_pronoun': 1.0, 'paragraph_size': 1}
        answer, error = ParagraphsGenerator(config, self.word_lists).generate_paragraphs()
        nouns, pronouns = count_nouns_and_pronouns(answer)
        self.assertEqual(nouns, 0)
        self.assertEqual(pronouns, 2)

    def test_generate_paragraphs_probability_pronouns_middle(self):
        random.seed(32487590)
        config = {'probability_pronoun': 0.5, 'paragraph_size': 2}
        answer, error = ParagraphsGenerator(config, self.word_lists).generate_paragraphs()
        nouns, pronouns = count_nouns_and_pronouns(answer)
        self.assertEqual(nouns, 2)
        self.assertEqual(pronouns, 2)

    def test_generate_paragraphs_probability_plural_noun_zero(self):
        config = {'probability_pronoun': 0.0, 'paragraph_size': 1, 'probability_plural_noun': 0.0}
        word_lists = WordLists(self.countable_nouns, self.verbs)
        to_test = ParagraphsGenerator(config, word_lists)
        answer, error = to_test.generate_paragraphs()
        plural_noun = count_word_tags(answer, WordTag.PLURAL)
        self.assertEqual(plural_noun, 0)

    def test_generate_paragraphs_probability_plural_noun_one(self):
        config = {'probability_pronoun': 0.0, 'paragraph_size': 1, 'probability_plural_noun': 1.0}
        word_lists = WordLists(self.countable_nouns, self.verbs)
        answer, error = ParagraphsGenerator(config, word_lists).generate_paragraphs()
        plural_noun = count_word_tags(answer, WordTag.PLURAL)
        self.assertEqual(plural_noun, 2)

    def test_generate_paragraphs_probability_plural_noun_middle(self):
        random.seed(324870)
        config = {'probability_pronoun': 0.0, 'paragraph_size': 1, 'probability_plural_noun': 0.5}
        word_lists = WordLists(self.countable_nouns, self.verbs)
        answer, error = ParagraphsGenerator(config, word_lists).generate_paragraphs()
        plural_noun = count_word_tags(answer, WordTag.PLURAL)
        self.assertEqual(plural_noun, 1)

    def test_generate_paragraphs_probability_negative_verb_zero(self):
        config = {'probability_pronoun': 0.0, 'paragraph_size': 4, 'probability_negative_verb': 0.0}
        word_lists = WordLists(self.countable_nouns, self.verbs)
        to_test = ParagraphsGenerator(config, word_lists)
        answer, error = to_test.generate_paragraphs()
        negative_verb = count_word_tags(answer, WordTag.NEGATIVE)
        self.assertEqual(negative_verb, 0)

    def test_generate_paragraphs_probability_negative_verb_one(self):
        config = {'probability_pronoun': 0.0, 'paragraph_size': 4, 'probability_negative_verb': 1.0}
        word_lists = WordLists(self.countable_nouns, self.verbs)
        answer, error = ParagraphsGenerator(config, word_lists).generate_paragraphs()
        negative_verb = count_word_tags(answer, WordTag.NEGATIVE)
        self.assertEqual(negative_verb, 4)

    def test_generate_paragraphs_probability_negative_verb_middle(self):
        random.seed(32470)
        config = {'probability_pronoun': 0.0, 'paragraph_size': 4, 'probability_negative_verb': 0.5}
        word_lists = WordLists(self.countable_nouns, self.verbs)
        answer, error = ParagraphsGenerator(config, word_lists).generate_paragraphs()
        negative_verb = count_word_tags(answer, WordTag.NEGATIVE)
        self.assertEqual(negative_verb, 2)

# TODO   'error_probability': 0.2,
# TODO   'noun_errors': True,
# TODO   'pronoun_errors': True,
# TODO   'verb_errors': True,
# TODO   'punctuation_errors': True,
# TODO   'is_do_errors': False,
# TODO   'preposition_transpose_errors': False,
#
# TODO   'tense': 'simple_present',

#     'probability_plural_noun': 0.2,
#     'probability_negative_verb': 0.3,
#     'probability_pronoun': 0.3,
#
# TODO   'paragraph_type': 'chain',
# TODO   'subject_pool': 5,

#     'paragraph_size': 15,

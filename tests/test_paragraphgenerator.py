import random
import unittest

from paragraph_generator.paragraphsgenerator import ParagraphsGenerator
from paragraph_generator.tags.status_tag import StatusTag
from paragraph_generator.tags.wordtag import WordTag
from paragraph_generator.word_groups.verb_group import VerbGroup
from paragraph_generator.word_lists import AbstractWordLists
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


class DummyWordLists(AbstractWordLists):
    def __init__(self, nouns, verbs):
        self._nouns = nouns
        self._verbs = verbs

    @property
    def nouns(self):
        return self._nouns[:]

    @property
    def verbs(self):
        return self._verbs[:]


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
        self.word_lists = DummyWordLists(nouns=self.countable_nouns, verbs=self.verbs)

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
        word_lists = DummyWordLists(self.countable_nouns, self.verbs)
        to_test = ParagraphsGenerator(config, word_lists)
        answer, error = to_test.generate_paragraphs()
        plural_noun = count_word_tags(answer, WordTag.PLURAL)
        self.assertEqual(plural_noun, 0)

    def test_generate_paragraphs_probability_plural_noun_one(self):
        config = {'probability_pronoun': 0.0, 'paragraph_size': 1, 'probability_plural_noun': 1.0}
        word_lists = DummyWordLists(self.countable_nouns, self.verbs)
        answer, error = ParagraphsGenerator(config, word_lists).generate_paragraphs()
        plural_noun = count_word_tags(answer, WordTag.PLURAL)
        self.assertEqual(plural_noun, 2)

    def test_generate_paragraphs_probability_plural_noun_middle(self):
        random.seed(324870)
        config = {'probability_pronoun': 0.0, 'paragraph_size': 1, 'probability_plural_noun': 0.5}
        word_lists = DummyWordLists(self.countable_nouns, self.verbs)
        answer, error = ParagraphsGenerator(config, word_lists).generate_paragraphs()
        plural_noun = count_word_tags(answer, WordTag.PLURAL)
        self.assertEqual(plural_noun, 1)

    def test_generate_paragraphs_probability_negative_verb_zero(self):
        config = {'probability_pronoun': 0.0, 'paragraph_size': 4, 'probability_negative_verb': 0.0}
        word_lists = DummyWordLists(self.countable_nouns, self.verbs)
        to_test = ParagraphsGenerator(config, word_lists)
        answer, error = to_test.generate_paragraphs()
        negative_verb = count_word_tags(answer, WordTag.NEGATIVE)
        self.assertEqual(negative_verb, 0)

    def test_generate_paragraphs_probability_negative_verb_one(self):
        config = {'probability_pronoun': 0.0, 'paragraph_size': 4, 'probability_negative_verb': 1.0}
        word_lists = DummyWordLists(self.countable_nouns, self.verbs)
        answer, error = ParagraphsGenerator(config, word_lists).generate_paragraphs()
        negative_verb = count_word_tags(answer, WordTag.NEGATIVE)
        self.assertEqual(negative_verb, 4)

    def test_generate_paragraphs_probability_negative_verb_middle(self):
        random.seed(32470)
        config = {'probability_pronoun': 0.0, 'paragraph_size': 4, 'probability_negative_verb': 0.5}
        word_lists = DummyWordLists(self.countable_nouns, self.verbs)
        answer, error = ParagraphsGenerator(config, word_lists).generate_paragraphs()
        negative_verb = count_word_tags(answer, WordTag.NEGATIVE)
        self.assertEqual(negative_verb, 2)

    def test_generate_paragraphs_tense_simple_present(self):
        config = {'paragraph_size': 5, 'tense': 'simple_present'}
        answer, error = ParagraphsGenerator(config, self.word_lists).generate_paragraphs()
        past_count = count_word_tags(answer, WordTag.PAST)
        self.assertEqual(past_count, 0)

    def test_generate_paragraphs_tense_simple_past(self):
        config = {'paragraph_size': 5, 'tense': 'simple_past'}
        answer, error = ParagraphsGenerator(config, self.word_lists).generate_paragraphs()
        past_count = count_word_tags(answer, WordTag.PAST)
        self.assertEqual(past_count, 5)

    def test_generate_paragraphs_paragraph_type_pool_pool_size_one(self):
        config = {'paragraph_size': 5, 'paragraph_type': 'pool', 'pool_size': 1, 'probability_pronoun': 1.0}
        answer, error = ParagraphsGenerator(config, self.word_lists).generate_paragraphs()

        subject = answer.sentence_list()[0].word_list()[0]  # type: AbstractPronoun
        for _, w_index, word in answer.indexed_all_words():
            if w_index == 0:
                self.assertEqual(word, subject)
            else:
                self.assertNotEqual(word, subject)

    def test_generate_paragraphs_paragraph_type_pool_pool_size_two(self):
        random.seed(243758)
        config = {'paragraph_size': 5, 'paragraph_type': 'pool', 'pool_size': 2, 'probability_pronoun': 1.0}
        answer, error = ParagraphsGenerator(config, self.word_lists).generate_paragraphs()

        subjects = set()
        for _, w_index, word in answer.indexed_all_words():
            if w_index == 0:
                subjects.add(word)
        self.assertEqual(len(subjects), 2)

    def test_generate_paragraph_type_chain(self):
        config = {'paragraph_size': 5, 'paragraph_type': 'chain', 'probability_pronoun': 1.0}
        answer, error = ParagraphsGenerator(config, self.word_lists).generate_paragraphs()
        first_sentence = answer.get_sentence(0)
        expected_subject = first_sentence.get(-2).subject().capitalize()
        for index in range(1, len(answer)):
            current_sentence = answer.get_sentence(index)
            self.assertEqual(current_sentence.get(0), expected_subject)
            expected_subject = current_sentence.get(-2).subject().capitalize()

    def test_generate_paragraphs_error_probability_zero(self):
        config = {'error_probability': 0.0, 'verb_errors': True}
        answer, error = ParagraphsGenerator(config, self.word_lists).generate_paragraphs()
        self.assertEqual(answer.sentence_list(), error.sentence_list())

    def test_generate_paragraphs_error_probability_one_all_errors_set_false(self):
        config = {'error_probability': 1.0}
        errors = {key: False for key in
                  ['noun_errors', 'pronoun_errors', 'verb_errors', 'punctuation_errors', 'is_do_errors',
                   'preposition_transpose_errors']}
        config.update(errors)
        answer, error = ParagraphsGenerator(config, self.word_lists).generate_paragraphs()
        self.assertEqual(answer, error)

    def test_generate_paragraphs_error_probability_one_with_errors(self):
        config = {'error_probability': 1.0, 'verb_errors': True}
        answer, error = ParagraphsGenerator(config, self.word_lists).generate_paragraphs()
        self.assertNotEqual(answer.sentence_list(), error.sentence_list())

    def test_generate_paragraphs_error_probability_middle(self):
        random.seed(34578)
        config = {'error_probability': 0.5, 'verb_errors': True, 'paragraph_size': 4}
        answer, error = ParagraphsGenerator(config, self.word_lists).generate_paragraphs()
        error_count = 0
        for error_sentence, sentence in zip(error, answer):
            error_verb = error_sentence.get(error_sentence.get_verb())
            answer_verb = sentence.get(sentence.get_verb())
            if error_verb != answer_verb:
                error_count += 1
        self.assertEqual(error_count, 2)

    def assert_only_error_has_one_error_tag(self, answer, error, test_tag):
        errors = [StatusTag.NOUN_ERRORS, StatusTag.PRONOUN_ERRORS, StatusTag.VERB_ERRORS, StatusTag.IS_DO_ERRORS,
                  StatusTag.PREPOSITION_ERRORS, StatusTag.PUNCTUATION_ERRORS]
        for status in errors:
            self.assertFalse(answer.tags.has(status))
            if status == test_tag:
                self.assertTrue(error.tags.has(status))
            else:
                self.assertFalse(error.tags.has(status))

    def test_noun_errors(self):
        errors_keys = ['noun_errors', 'pronoun_errors', 'verb_errors', 'is_do_errors', 'preposition_transpose_errors',
                       'punctuation_errors']
        config = {key: False for key in errors_keys}
        config.update({'error_probability': 1.0, 'paragraph_size': 1, 'noun_errors': 1.0})

        answer, error = ParagraphsGenerator(config, self.word_lists).generate_paragraphs()
        self.assert_only_error_has_one_error_tag(answer, error, StatusTag.NOUN_ERRORS)

    def test_pronoun_errors(self):
        errors_keys = ['noun_errors', 'pronoun_errors', 'verb_errors', 'is_do_errors', 'preposition_transpose_errors',
                       'punctuation_errors']
        config = {key: False for key in errors_keys}
        config.update(
            {'error_probability': 1.0, 'paragraph_size': 1, 'pronoun_errors': 1.0})

        answer, error = ParagraphsGenerator(config, self.word_lists).generate_paragraphs()
        self.assert_only_error_has_one_error_tag(answer, error, StatusTag.PRONOUN_ERRORS)

    def test_verb_errors(self):
        errors_keys = ['noun_errors', 'pronoun_errors', 'verb_errors', 'is_do_errors', 'preposition_transpose_errors',
                       'punctuation_errors']
        config = {key: False for key in errors_keys}
        config.update({'error_probability': 1.0, 'paragraph_size': 1, 'verb_errors': 1.0})

        answer, error = ParagraphsGenerator(config, self.word_lists).generate_paragraphs()
        self.assert_only_error_has_one_error_tag(answer, error, StatusTag.VERB_ERRORS)

    def test_is_do_errors(self):
        errors_keys = ['noun_errors', 'pronoun_errors', 'verb_errors', 'is_do_errors', 'preposition_transpose_errors',
                       'punctuation_errors']
        config = {key: False for key in errors_keys}
        config.update({'error_probability': 1.0, 'paragraph_size': 1, 'is_do_errors': 1.0})

        answer, error = ParagraphsGenerator(config, self.word_lists).generate_paragraphs()
        self.assert_only_error_has_one_error_tag(answer, error, StatusTag.IS_DO_ERRORS)

    def test_preposition_transpose_errors(self):
        errors_keys = ['noun_errors', 'pronoun_errors', 'verb_errors', 'is_do_errors', 'preposition_transpose_errors',
                       'punctuation_errors']
        config = {key: False for key in errors_keys}
        config.update({'error_probability': 1.0, 'paragraph_size': 1, 'preposition_transpose_errors': 1.0})

        answer, error = ParagraphsGenerator(config, self.word_lists).generate_paragraphs()
        self.assert_only_error_has_one_error_tag(answer, error, StatusTag.PREPOSITION_ERRORS)

    def test_punctuation_errors(self):
        errors_keys = ['noun_errors', 'pronoun_errors', 'verb_errors', 'is_do_errors', 'preposition_transpose_errors',
                       'punctuation_errors']
        config = {key: False for key in errors_keys}
        config.update({'error_probability': 1.0, 'paragraph_size': 1, 'punctuation_errors': 1.0})

        answer, error = ParagraphsGenerator(config, self.word_lists).generate_paragraphs()
        self.assert_only_error_has_one_error_tag(answer, error, StatusTag.PUNCTUATION_ERRORS)

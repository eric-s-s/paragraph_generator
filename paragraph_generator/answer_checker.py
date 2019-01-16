"""
strategy. take answer string and original paragraph.

use create_answer_paragraph to generate new paragraph with correct plural nouns.
use ParagraphComparisons to generate comparitor.

return requested json including answer paragraph according to kind of comparison requested. 

"""
import unittest

from paragraph_generator.backend.create_answer_paragraph import create_answer_paragraph
from paragraph_generator.backend.paragraph_comparison import ParagraphComparison
from paragraph_generator.word_groups.paragraph import Paragraph
from paragraph_generator.word_groups.sentence import Sentence
from paragraph_generator.words.noun import Noun
from paragraph_generator.words.pronoun import CapitalPronoun, Pronoun
from paragraph_generator.words.punctuation import Punctuation
from paragraph_generator.words.verb import Verb


class AnswerChecker(object):
    def __init__(self, submission: str, original: Paragraph):
        self._submission = submission
        self._original = original

    @property
    def submission(self):
        return self._submission

    @property
    def original(self):
        return self._original

    def is_submission_correct(self) -> bool:
        return self.count_sentence_errors() == 0

    def count_sentence_errors(self) -> int:
        return self.get_sentence_hints()['error_count']

    def count_word_errors(self) -> int:
        return self.get_word_hints()['error_count']

    def get_sentence_hints(self):
        """

        :return: {'error_count': int, 'hint_paragraph': str, 'missing_sentences': int}
        """
        return self._get_comparitor().compare_by_sentences()

    def get_word_hints(self):
        """

        :return: {'error_count': int, 'hint_paragraph': str, 'missing_words': int}
        """
        return self._get_comparitor().compare_by_words()

    def _get_comparitor(self):
        answer_paragraph = create_answer_paragraph(self._submission, self._original)
        comparison = ParagraphComparison(answer_paragraph, self._submission)
        return comparison


class TestAnswerChecker(unittest.TestCase):
    def setUp(self):
        self.test_paragraph = Paragraph(
            [
                Sentence([
                    CapitalPronoun.I, Verb('like'), Noun('squirrel').plural(), Punctuation.EXCLAMATION
                ]),
                Sentence([
                    Noun('squirrel').plural().definite().capitalize(), Verb('like'), Pronoun.ME, Punctuation.PERIOD
                ])
            ]
        )

    def test_init(self):
        submission = 'Submission paragraph'
        original = Paragraph([])
        to_test = AnswerChecker(submission, original)
        self.assertEqual(to_test.submission, submission)
        self.assertEqual(to_test.original, original)

    def test_is_submission_correct_true_noun_did_not_change_number(self):
        correct_submission = 'I like squirrels! The squirrels like me.'
        to_test = AnswerChecker(correct_submission, self.test_paragraph)
        self.assertTrue(to_test.is_submission_correct())

    def test_is_submission_correct_true_with_bad_white_spaces(self):
        correct_submission = '  I like squirrels!   The squirrels like me.  '
        to_test = AnswerChecker(correct_submission, self.test_paragraph)
        self.assertTrue(to_test.is_submission_correct())

    def test_is_submission_correct_true_noun_changed_number(self):
        correct_submission = 'I like a squirrel! The squirrel likes me.'
        to_test = AnswerChecker(correct_submission, self.test_paragraph)
        self.assertTrue(to_test.is_submission_correct())

    def test_is_submission_correct_false(self):
        incorrect_submission = 'i like squirrels? The squirrels like me.'
        to_test = AnswerChecker(incorrect_submission, self.test_paragraph)
        self.assertFalse(to_test.is_submission_correct())

    def test_count_sentence_errors_no_errors(self):
        all_correct = [
            'I like squirrels! The squirrels like me.',
            'I like a squirrel! The squirrel likes me.',
            '  I like squirrels!   The squirrels like me.  ',
        ]
        for submission in all_correct:
            checker = AnswerChecker(submission, self.test_paragraph)
            self.assertEqual(checker.count_sentence_errors(), 0)

    def test_count_sentence_error_two_errors(self):
        two_errors = 'a. b.'
        self.assertEqual(AnswerChecker(two_errors, self.test_paragraph).count_sentence_errors(), 2)

    def test_count_word_errors_no_errors(self):
        all_correct = [
            'I like squirrels! The squirrels like me.',
            'I like a squirrel! The squirrel likes me.',
            '  I like squirrels!   The squirrels like me.  ',
        ]
        for submission in all_correct:
            checker = AnswerChecker(submission, self.test_paragraph)
            self.assertEqual(checker.count_word_errors(), 0)

    def test_count_word_errors_three_errors(self):
        submission = 'I like squirrels! A squirrel liked me?'
        checker = AnswerChecker(submission, self.test_paragraph)
        self.assertEqual(checker.count_word_errors(), 3)

    def test_get_sentence_hints(self):
        submission = 'a. b.'
        checker = AnswerChecker(submission, self.test_paragraph)
        expected = {
            'error_count': 2,
            'hint_paragraph': '<bold>a.</bold> <bold>b.</bold>',
            'missing_sentences': 0,
        }
        self.assertEqual(checker.get_sentence_hints(), expected)

    def test_get_word_hints(self):
        submission = 'Me liked squirrels! The squirrels like me.'
        checker = AnswerChecker(submission, self.test_paragraph)
        expected = {
            'error_count': 2,
            'hint_paragraph': '<bold>Me</bold> <bold>liked</bold> squirrels! The squirrels like me.',
            'missing_words': 0,
        }
        self.assertEqual(checker.get_word_hints(), expected)

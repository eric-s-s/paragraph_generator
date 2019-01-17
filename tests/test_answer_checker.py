import unittest

from paragraph_generator.answer_checker import AnswerChecker
from paragraph_generator.word_groups.paragraph import Paragraph
from paragraph_generator.word_groups.sentence import Sentence
from paragraph_generator.words.noun import Noun
from paragraph_generator.words.pronoun import CapitalPronoun, Pronoun
from paragraph_generator.words.punctuation import Punctuation
from paragraph_generator.words.verb import Verb


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
            'missing_sentences': 0,
        }
        self.assertEqual(checker.get_word_hints(), expected)

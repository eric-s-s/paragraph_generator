import unittest

from sentences.alt_backend.paragraph_comparison import (
    ParagraphComparison, find_noun_group, find_verb_group, find_word,
    find_word_group, compare_sentences
)
from sentences.word_groups.paragraph import Paragraph
from sentences.word_groups.sentence import Sentence
from sentences.words.basicword import BasicWord
from sentences.words.noun import Noun
from sentences.words.punctuation import Punctuation
from sentences.words.verb import Verb


class TestParagraphComparison(unittest.TestCase):
    def test_init(self):
        answer_paragraph = Paragraph([Sentence([BasicWord('a')])])
        submission_str = 'b'

        comparitor = ParagraphComparison(answer_paragraph, submission_str)
        self.assertEqual(comparitor.answer, answer_paragraph)
        self.assertEqual(comparitor.submission, 'b')

    def test_compare_by_sentence_paragraph_str_eq_submission_str(self):
        answer_paragraph = Paragraph([Sentence([BasicWord('a')])])
        submission_str = str(answer_paragraph)
        comparitor = ParagraphComparison(answer_paragraph, submission_str)
        comparison = comparitor.compare_by_sentences()
        expected = {
            'error_count': 0,
            'hint_paragraph': submission_str,
            'missing_sentences': 0
        }
        self.assertEqual(comparison, expected)

    def test_compare_by_sentence_one_sentence_different_by_internals(self):
        answer = Paragraph([Sentence([BasicWord('Hello'), Punctuation.PERIOD]),
                            Sentence([BasicWord('I'), BasicWord('am'), BasicWord('man'), Punctuation.EXCLAMATION])])
        submission = 'Hello. I am man.'
        hint_paragraph = 'Hello. <bold>I am man.</bold>'

        comparitor = ParagraphComparison(answer, submission)
        hints = comparitor.compare_by_sentences()
        expected = {
            'error_count': 1,
            'hint_paragraph': hint_paragraph,
            'missing_sentences': 0
        }
        self.assertEqual(hints, expected)

    def test_compare_by_sentence_commas_are_counted_as_sentences(self):
        answer = Paragraph([Sentence([BasicWord(wd), Punctuation.PERIOD]) for wd in 'ABC'])
        submission = 'A, B. C,'
        hint_paragraph = '<bold>A,</bold> B. <bold>C,</bold>'

        comparitor = ParagraphComparison(answer, submission)
        hints = comparitor.compare_by_sentences()
        expected = {
            'error_count': 2,
            'hint_paragraph': hint_paragraph,
            'missing_sentences': 0
        }
        self.assertEqual(hints, expected)

    def test_compare_by_sentence_can_identify_period_comma_exclamation_question(self):
        answer = Paragraph([Sentence([BasicWord('a'), Punctuation.PERIOD]),
                            Sentence([BasicWord('b'), Punctuation.EXCLAMATION]),
                            Sentence([BasicWord('c'), Punctuation.QUESTION]),
                            Sentence([BasicWord('d'), Punctuation.COMMA])])
        submission = 'a, b, c, d,'
        hint_paragraph = '<bold>a,</bold> <bold>b,</bold> <bold>c,</bold> d,'

        comparitor = ParagraphComparison(answer, submission)
        hints = comparitor.compare_by_sentences()
        expected = {
            'error_count': 3,
            'hint_paragraph': hint_paragraph,
            'missing_sentences': 0
        }
        self.assertEqual(hints, expected)

    def test_compare_by_sentence_will_find_the_final_sentence_with_missing_punctuation(self):
        answer = Paragraph([Sentence([BasicWord('a'), Punctuation.PERIOD]),
                            Sentence([BasicWord('b'), Punctuation.PERIOD])])
        submission = 'a. b'
        hint_paragraph = 'a. <bold>b</bold>'

        comparitor = ParagraphComparison(answer, submission)
        hints = comparitor.compare_by_sentences()
        expected = {
            'error_count': 1,
            'hint_paragraph': hint_paragraph,
            'missing_sentences': 0
        }
        self.assertEqual(hints, expected)

    def test_compare_by_sentence_answer_has_more_sentences(self):
        answer = Paragraph([Sentence([BasicWord('a'), Punctuation.PERIOD]),
                            Sentence([BasicWord('b'), Punctuation.PERIOD])])
        submission = 'a and b.'
        hint_paragraph = '<bold>a and b.</bold> '

        comparitor = ParagraphComparison(answer, submission)
        hints = comparitor.compare_by_sentences()
        expected = {
            'error_count': 1,
            'hint_paragraph': hint_paragraph,
            'missing_sentences': 1
        }
        self.assertEqual(hints, expected)

    def test_compare_by_sentence_answer_has_less_sentences(self):
        answer = Paragraph([Sentence([BasicWord('a'), Punctuation.PERIOD]),
                            Sentence([BasicWord('b'), Punctuation.PERIOD])])
        submission = 'a. c. b.'
        hint_paragraph = 'a. <bold>c.</bold> <bold>b.</bold>'

        comparitor = ParagraphComparison(answer, submission)
        hints = comparitor.compare_by_sentences()
        expected = {
            'error_count': 2,
            'hint_paragraph': hint_paragraph,
            'missing_sentences': -1
        }
        self.assertEqual(hints, expected)

    def test_find_noun_group_word_not_present(self):
        submission_str = ''
        word = Noun('dog')
        self.assertIsNone(find_noun_group(word, submission_str))

    def test_find_noun_group_all_noun_forms_simple_case(self):
        dogs = [Noun('dog'), Noun('dog').plural(), Noun('dog').indefinite(),
                Noun('dog').definite(), Noun('dog').plural().definite()]
        capital_dogs = [word.capitalize() for word in dogs]
        submission_str = 'go dog go.'
        for word in dogs + capital_dogs:
            answer = find_noun_group(word, submission_str)
            expected = (3, 6)
            self.assertEqual(answer, expected)

    def test_find_noun_group_noun_forms_complex_case(self):
        dogs = [Noun('dog'), Noun('dog').plural(), Noun('dog').indefinite(),
                Noun('dog').definite(), Noun('dog').plural().definite()]
        capital_dogs = [word.capitalize() for word in dogs]
        submission_str = 'a the dogs bark.'
        for word in dogs + capital_dogs:
            answer = find_noun_group(word, submission_str)
            start = submission_str.find('the dogs')
            end = start + len('the dogs')
            self.assertEqual(answer, (start, end))

    def test_find_noun_group_all_prefixes(self):
        prefixes = ['a', 'A', 'an', 'An', 'the', 'The']
        word = Noun('cat')
        for prefix in prefixes:
            submission_str = f'x {prefix} cat '
            answer = find_noun_group(word, submission_str)
            start = 2
            end = start + len(f'{prefix} cat')
            self.assertEqual(answer, (start, end))

    def test_find_noun_group_upper_case(self):
        submission_str = 'the Dogs.'
        word = Noun('dog')
        answer = find_noun_group(word, submission_str)
        start = 0
        end = len('the Dogs')
        self.assertEqual(answer, (start, end))

    def test_find_noun_group_lower_case_edge_case(self):
        submission_str = 'The bMWs'
        word = Noun('BMW')
        self.assertIsNone(find_noun_group(word, submission_str))

    def test_find_noun_group_submission_str_special_rule_regular_plural(self):
        submission_str = 'look at the cute babies.'
        word = Noun('baby')
        answer = find_noun_group(word, submission_str)
        start = submission_str.find('babies')
        end = start + len('babies')
        self.assertEqual(answer, (start, end))

    def test_find_noun_group_submission_str_irregular_plural(self):
        submission_str = 'I loves the feets.'
        base_noun = Noun('foot', 'feet')
        answer = find_noun_group(base_noun, submission_str)
        start = submission_str.find('the feets')
        end = start + len('the feets')
        self.assertEqual(answer, (start, end))

    def test_find_verb_group_verb_not_present(self):
        submission_str = ''
        verb = Verb('play')
        self.assertIsNone(find_verb_group(verb, submission_str))

    def test_find_verb_group_all_verb_forms_simple(self):
        submission_str = 'i go home.'
        go = Verb('go', 'went')
        verbs = [go, go.third_person(), go.negative(), go.negative().third_person(), go.past_tense(),
                 go.negative().past_tense()]
        capital_verbs = [verb.capitalize() for verb in verbs]
        for verb in verbs + capital_verbs:
            answer = find_verb_group(verb, submission_str)
            expected = (2, 4)
            self.assertEqual(answer, expected)

    def test_find_verb_group_all_verb_forms_complex(self):
        submission_str = "i didn't went home."
        go = Verb('go', 'went')
        verbs = [go, go.third_person(), go.negative(), go.negative().third_person(), go.past_tense(),
                 go.negative().past_tense()]
        capital_verbs = [verb.capitalize() for verb in verbs]
        for verb in verbs + capital_verbs:
            answer = find_verb_group(verb, submission_str)
            start = submission_str.find("didn't went")
            end = start + len("didn't went")
            self.assertEqual(answer, (start, end))

    def test_find_verb_group_all_prefixes(self):
        prefixes = ["Don't", "don't", "Doesn't", "doesn't", "Didn't", "didn't"]
        verb = Verb('play')
        for prefix in prefixes:
            submission_str = f'the cat {prefix} play here.'
            answer = find_verb_group(verb, submission_str)
            start = len('the cat ')
            end = start + len(f'{prefix} play')
            self.assertEqual(answer, (start, end))

    def test_find_verb_group_upper_case(self):
        submission_str = 'the dogs Play.'
        word = Verb('play')
        answer = find_verb_group(word, submission_str)
        start = len('the Dogs ')
        end = start + len('Play')
        self.assertEqual(answer, (start, end))

    def test_find_verb_group_submission_str_special_rule_regular_third_person(self):
        submission_str = 'He babies me.'
        word = Verb('baby')
        answer = find_verb_group(word, submission_str)
        start = submission_str.find('babies')
        end = start + len('babies')
        self.assertEqual(answer, (start, end))

    def test_find_verb_group_submission_str_special_rule_regular_past_tense(self):
        submission_str = 'He babied me.'
        word = Verb('baby')
        answer = find_verb_group(word, submission_str)
        start = submission_str.find('babied')
        end = start + len('babied')
        self.assertEqual(answer, (start, end))

    def test_find_verb_group_submission_str_irregular_past(self):
        submission_str = 'I went home.'
        base_verb = Verb('go', 'went')
        answer = find_verb_group(base_verb, submission_str)
        start = submission_str.find('went')
        end = start + len('went')
        self.assertEqual(answer, (start, end))

    def test_find_word_word_not_present(self):
        submission_str = ''
        self.assertIsNone(find_word(BasicWord('x'), submission_str))

    def test_find_word_word_breaks(self):
        submission_str = ' x,'
        word = BasicWord('x')
        answer = find_word(word, submission_str)
        expected = (1, 2)
        self.assertEqual(answer, expected)

    def test_find_word_does_not_allow_substring(self):
        word = BasicWord('x')
        prefixed = 'yx'
        postfixed = 'xy'
        self.assertIsNone(find_word(word, prefixed))
        self.assertIsNone(find_word(word, postfixed))

    def test_find_word_group_noun(self):
        word = Noun('dog')
        submission_str = 'The dogs fly.'
        answer = find_word_group(word, submission_str)
        expected = (0, len('the dogs'))
        self.assertEqual(answer, expected)

    def test_find_word_group_verb(self):
        word = Verb('play')
        submission_str = "a didn't play."
        answer = find_word_group(word, submission_str)
        start = 2
        end = start + len("didn't play")
        self.assertEqual(answer, (start, end))

    def test_find_word_group_other(self):
        word = BasicWord('x')
        submission_str = 'I x.'
        answer = find_word_group(word, submission_str)
        expected = (2, 3)
        self.assertEqual(answer, expected)

    def test_find_word_group_not_present(self):
        submission_str = ''
        for word in (Noun('a'), Verb('a'), BasicWord('a')):
            self.assertIsNone(find_word_group(word, submission_str))

    def test_compare_sentences(self):
        sentence = Sentence([Noun('dog').definite().capitalize(), Verb('play').third_person(), Punctuation.PERIOD])
        submission_str = 'The dog plays.'
        answer = compare_sentences(sentence, submission_str)
        expected = {
            'hint_sentence': submission_str,
            'error_count': 0
        }
        self.assertEqual(answer, expected)

    def test_compare_sentences_with_error_basic(self):
        sentence = Sentence([Noun('dog').definite().capitalize(), Verb('play').third_person(), Punctuation.PERIOD])
        submission_str = 'A dog played.'
        answer = compare_sentences(sentence, submission_str)
        expected = {
            'hint_sentence': "<bold>A dog</bold> <bold>played</bold>.",
            'error_count': 2
        }
        self.assertEqual(answer, expected)

    def test_compare_sentences_punctuation_error(self):
        sentence = Sentence([Verb('go').capitalize(), Punctuation.PERIOD])
        submission_str = 'Go!'
        answer = compare_sentences(sentence, submission_str)
        expected = {
            'hint_sentence': "Go<bold>!</bold>",
            'error_count': 1
        }
        self.assertEqual(answer, expected)

    def test_compare_sentences_missing_punctuation(self):
        sentence = Sentence([Verb('go').capitalize(), Punctuation.PERIOD])
        submission_str = 'Go'
        answer = compare_sentences(sentence, submission_str)
        expected = {
            'hint_sentence': 'Go <bold>MISSING</bold>',
            'error_count': 1
        }
        self.assertEqual(answer, expected)

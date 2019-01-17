"""
strategy. take answer string and original paragraph.

use create_answer_paragraph to generate new paragraph with correct plural nouns.
use ParagraphComparisons to generate comparitor.

return requested json including answer paragraph according to kind of comparison requested. 

"""

from paragraph_generator.backend.create_answer_paragraph import create_answer_paragraph
from paragraph_generator.backend.paragraph_comparison import ParagraphComparison
from paragraph_generator.word_groups.paragraph import Paragraph


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

        :return: {'error_count': int, 'hint_paragraph': str, 'missing_sentences': int}
        """
        return self._get_comparitor().compare_by_words()

    def _get_comparitor(self):
        answer_paragraph = create_answer_paragraph(self._submission, self._original)
        comparison = ParagraphComparison(answer_paragraph, self._submission)
        return comparison

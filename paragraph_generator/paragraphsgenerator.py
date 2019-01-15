from paragraph_generator.backend.error_maker import ErrorMaker
from paragraph_generator.backend.grammarizer import Grammarizer
from paragraph_generator.backend.random_assignments.assign_random_negatives import assign_random_negatives
from paragraph_generator.backend.random_assignments.plurals_assignement import PluralsAssignment
from paragraph_generator.backend.random_assignments.random_paragraph import RandomParagraph
from paragraph_generator.word_lists_generator import AbstractWordLists


class ParagraphsGenerator(object):
    def __init__(self, config_state, word_lists_generator: AbstractWordLists):
        """
        :config_state required keys:
        - 'error_probability'
        - 'noun_errors'
        - 'pronoun_errors'
        - 'verb_errors'
        - 'is_do_errors'
        - 'preposition_transpose_errors'
        - 'punctuation_errors'


        - 'tense'
        - 'probability_plural_noun'
        - 'probability_negative_verb'
        - 'probability_pronoun'

        - 'paragraph_type'
        - 'subject_pool'
        - 'num_paragraphs'
        - 'paragraph_size'
        """
        self._config = {
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

        self._config.update(config_state)
        self._word_list_generator = word_lists_generator

    def get(self, key):
        return self._config[key]

    def get_nouns(self):
        return self._word_list_generator.nouns

    def get_verbs(self):
        return self._word_list_generator.verbs

    def generate_paragraphs(self):
        paragraph_size = self.get('paragraph_size')
        probability_pronoun = self.get('probability_pronoun')
        generator = RandomParagraph(probability_pronoun, self.get_verbs(), self.get_nouns())
        if self.get('paragraph_type') == 'chain':
            raw = generator.create_chain_paragraph(paragraph_size)
        else:
            raw = generator.create_pool_paragraph(self.get('pool_size'), paragraph_size)

        probability_plural_noun = self.get('probability_plural_noun')
        with_plurals = PluralsAssignment(raw).assign_random_plurals(probability_plural_noun)

        probability_negative_verb = self.get('probability_negative_verb')
        with_negatives = assign_random_negatives(with_plurals, probability_negative_verb)

        grammarizer = Grammarizer(with_negatives)
        if self.get('tense') == 'simple_present':
            answer = grammarizer.grammarize_to_present_tense()
        else:
            answer = grammarizer.grammarize_to_past_tense()

        error_maker = self._create_errors(answer)

        return answer, error_maker.get_paragraph()

    def _create_errors(self, answer):
        preposition_errors_config_to_method_name = {'preposition_transpose_errors': 'preposition_errors'}
        error_types = ['noun_errors', 'pronoun_errors', 'verb_errors', 'is_do_errors', 'punctuation_errors']
        config_name_to_method_name = {key: key for key in error_types}
        config_name_to_method_name.update(preposition_errors_config_to_method_name)
        methods = [value for key, value in config_name_to_method_name.items() if self.get(key)]

        error_maker = ErrorMaker(answer)
        p_error = self.get('error_probability')
        for method in methods:
            error_maker = getattr(error_maker, method)(p_error)
        return error_maker

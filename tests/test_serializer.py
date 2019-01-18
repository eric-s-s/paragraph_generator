import json
import unittest

from paragraph_generator.serializer import Serializer
from paragraph_generator.tags.status_tag import StatusTag
from paragraph_generator.tags.tags import Tags
from paragraph_generator.tags.wordtag import WordTag
from paragraph_generator.word_groups.paragraph import Paragraph
from paragraph_generator.word_groups.sentence import Sentence
from paragraph_generator.words.basicword import BasicWord
from paragraph_generator.words.be_verb import BeVerb
from paragraph_generator.words.noun import Noun
from paragraph_generator.words.pronoun import Pronoun, CapitalPronoun
from paragraph_generator.words.punctuation import Punctuation
from paragraph_generator.words.verb import Verb


class TestSerializer(unittest.TestCase):
    def test_empty_paragraph_to_dict(self):
        answer = Serializer.to_dict(Paragraph([]))
        expected = {
            'class': 'Paragraph',
            'sentence_list': [

            ],
            'tags': [
            ]
        }
        self.assertEqual(expected, answer)

    def test_paragraph_with_empty_sentence(self):
        answer = Serializer.to_dict(Paragraph([Sentence([])]))
        expected = {
            'class': 'Paragraph',
            'sentence_list': [
                {'class': 'Sentence', 'word_list': []}
            ],
            'tags': [],
        }
        self.assertEqual(answer, expected)

    def test_paragraph_with_tags(self):
        tag_list = [tag for tag in StatusTag]
        paragraph = Paragraph([], Tags(tag_list))

        answer = Serializer.to_dict(paragraph)
        tag_names = [tag.name for tag in StatusTag]
        expected = {
            'class': 'Paragraph',
            'sentence_list': [],
            'tags': tag_names
        }
        self.assertEqual(answer, expected)

    def test_to_obj_with_empty_paragraph(self):
        paragraph = Paragraph([])
        as_dict = Serializer.to_dict(paragraph)
        self.assertEqual(Serializer.to_obj(as_dict), paragraph)

    def test_to_obj_with_empty_sentence(self):
        paragraph = Paragraph([Sentence()])
        as_dict = Serializer.to_dict(paragraph)
        self.assertEqual(Serializer.to_obj(as_dict), paragraph)

    def test_to_obj_with_tags(self):
        tag_list = [tag for tag in StatusTag]
        paragraph = Paragraph([], Tags(tag_list))
        as_dict = Serializer.to_dict(paragraph)
        self.assertEqual(Serializer.to_obj(as_dict), paragraph)

    def test_to_dict_with_tagless_BasicWord_in_sentence(self):
        paragraph = Paragraph([Sentence([BasicWord('x'), BasicWord('y')])])
        word_list = [
            {'class': 'BasicWord', 'value': 'x', 'tags': []},
            {'class': 'BasicWord', 'value': 'y', 'tags': []}
        ]
        expected = {
            'class': 'Paragraph',
            'sentence_list': [
                {'class': 'Sentence', 'word_list': word_list}
            ],
            'tags': [],
        }
        self.assertEqual(Serializer.to_dict(paragraph), expected)

    def test_to_dict_with_tagged_BasicWord_in_sentence(self):
        paragraph = Paragraph([Sentence([BasicWord('x', Tags([tag for tag in WordTag]))])])
        tag_list = [tag.name for tag in WordTag]
        word_list = [
            {'class': 'BasicWord', 'value': 'x', 'tags': tag_list},
        ]
        expected = {
            'class': 'Paragraph',
            'sentence_list': [
                {'class': 'Sentence', 'word_list': word_list}
            ],
            'tags': [],
        }
        self.assertEqual(Serializer.to_dict(paragraph), expected)

    def test_to_obj_with_tagless_BasicWord_in_sentence(self):
        paragraph = Paragraph([Sentence([BasicWord('x'), BasicWord('y')])])
        as_dict = Serializer.to_dict(paragraph)
        self.assertEqual(Serializer.to_obj(as_dict), paragraph)

    def test_to_obj_with_tagged_BasicWord_in_sentence(self):
        paragraph = Paragraph([Sentence([BasicWord('x', Tags([tag for tag in WordTag])), BasicWord('y')])])
        as_dict = Serializer.to_dict(paragraph)
        self.assertEqual(Serializer.to_obj(as_dict), paragraph)

    def test_to_dict_with_tagless_Noun_in_sentence(self):
        paragraph = Paragraph([Sentence([Noun('x'), Noun('y', 'z', 'q')])])
        word_list = [
            {'class': 'Noun', 'value': 'x', 'irregular_plural': '', 'base_noun': 'x', 'tags': []},
            {'class': 'Noun', 'value': 'y', 'irregular_plural': 'z', 'base_noun': 'q', 'tags': []}
        ]
        expected = {
            'class': 'Paragraph',
            'sentence_list': [
                {'class': 'Sentence', 'word_list': word_list}
            ],
            'tags': [],
        }
        self.assertEqual(Serializer.to_dict(paragraph), expected)

    def test_to_dict_with_tagged_Noun_in_sentence(self):
        paragraph = Paragraph([Sentence([Noun('x', tags=Tags([tag for tag in WordTag]))])])
        tag_list = [tag.name for tag in WordTag]
        word_list = [
            {'class': 'Noun', 'value': 'x', 'irregular_plural': '', 'base_noun': 'x', 'tags': tag_list},
        ]
        expected = {
            'class': 'Paragraph',
            'sentence_list': [
                {'class': 'Sentence', 'word_list': word_list}
            ],
            'tags': [],
        }
        self.assertEqual(Serializer.to_dict(paragraph), expected)

    def test_to_obj_with_tagless_Noun_in_sentence(self):
        paragraph = Paragraph([Sentence([Noun('x'), Noun('y')])])
        as_dict = Serializer.to_dict(paragraph)
        self.assertEqual(Serializer.to_obj(as_dict), paragraph)

    def test_to_obj_with_tagged_Noun_in_sentence(self):
        paragraph = Paragraph([Sentence([Noun('x', Tags([tag for tag in WordTag])), Noun('y')])])
        as_dict = Serializer.to_dict(paragraph)
        self.assertEqual(Serializer.to_obj(as_dict), paragraph)

    def test_to_dict_with_tagless_Verb_in_sentence(self):
        paragraph = Paragraph([Sentence([Verb('x'), Verb('y', 'z', 'q')])])
        word_list = [
            {'class': 'Verb', 'value': 'x', 'irregular_past': '', 'infinitive': 'x', 'tags': []},
            {'class': 'Verb', 'value': 'y', 'irregular_past': 'z', 'infinitive': 'q', 'tags': []}
        ]
        expected = {
            'class': 'Paragraph',
            'sentence_list': [
                {'class': 'Sentence', 'word_list': word_list}
            ],
            'tags': [],
        }
        self.assertEqual(Serializer.to_dict(paragraph), expected)

    def test_to_dict_with_tagged_Verb_in_sentence(self):
        paragraph = Paragraph([Sentence([Verb('x', tags=Tags([tag for tag in WordTag]))])])
        tag_list = [tag.name for tag in WordTag]
        word_list = [
            {'class': 'Verb', 'value': 'x', 'irregular_past': '', 'infinitive': 'x', 'tags': tag_list},
        ]
        expected = {
            'class': 'Paragraph',
            'sentence_list': [
                {'class': 'Sentence', 'word_list': word_list}
            ],
            'tags': [],
        }
        self.assertEqual(Serializer.to_dict(paragraph), expected)

    def test_to_obj_with_tagless_Verb_in_sentence(self):
        paragraph = Paragraph([Sentence([Verb('x'), Verb('y')])])
        as_dict = Serializer.to_dict(paragraph)
        self.assertEqual(Serializer.to_obj(as_dict), paragraph)

    def test_to_obj_with_tagged_Verb_in_sentence(self):
        paragraph = Paragraph([Sentence([Verb('x', Tags([tag for tag in WordTag])), Verb('y')])])
        as_dict = Serializer.to_dict(paragraph)
        self.assertEqual(Serializer.to_obj(as_dict), paragraph)

    def test_to_dict_with_Pronoun_in_sentence(self):
        paragraph = Paragraph([Sentence([pronoun for pronoun in Pronoun])])
        word_list = [{'class': 'Pronoun', 'name': pronoun.name} for pronoun in Pronoun]
        expected = {
            'class': 'Paragraph',
            'sentence_list': [
                {'class': 'Sentence', 'word_list': word_list}
            ],
            'tags': [],
        }
        self.assertEqual(Serializer.to_dict(paragraph), expected)

    def test_to_obj_with_Pronoun_in_sentence(self):
        paragraph = Paragraph([Sentence([pronoun for pronoun in Pronoun])])
        as_dict = Serializer.to_dict(paragraph)
        self.assertEqual(Serializer.to_obj(as_dict), paragraph)

    def test_to_dict_with_CapitalPronoun_in_sentence(self):
        paragraph = Paragraph([Sentence([pronoun for pronoun in CapitalPronoun])])
        word_list = [{'class': 'CapitalPronoun', 'name': pronoun.name} for pronoun in Pronoun]
        expected = {
            'class': 'Paragraph',
            'sentence_list': [
                {'class': 'Sentence', 'word_list': word_list}
            ],
            'tags': [],
        }
        self.assertEqual(Serializer.to_dict(paragraph), expected)

    def test_to_obj_with_CapitalPronoun_in_sentence(self):
        paragraph = Paragraph([Sentence([pronoun for pronoun in CapitalPronoun])])
        as_dict = Serializer.to_dict(paragraph)
        self.assertEqual(Serializer.to_obj(as_dict), paragraph)

    def test_to_dict_with_Punctuation_in_sentence(self):
        paragraph = Paragraph([Sentence([pronoun for pronoun in Punctuation])])
        word_list = [{'class': 'Punctuation', 'name': pronoun.name} for pronoun in Punctuation]
        expected = {
            'class': 'Paragraph',
            'sentence_list': [
                {'class': 'Sentence', 'word_list': word_list}
            ],
            'tags': [],
        }
        self.assertEqual(Serializer.to_dict(paragraph), expected)

    def test_to_obj_with_Punctuation_in_sentence(self):
        paragraph = Paragraph([Sentence([pronoun for pronoun in Punctuation])])
        as_dict = Serializer.to_dict(paragraph)
        self.assertEqual(Serializer.to_obj(as_dict), paragraph)

    def test_to_dict_with_BeVerb_in_sentence(self):
        paragraph = Paragraph([Sentence([pronoun for pronoun in BeVerb])])
        word_list = [{'class': 'BeVerb', 'name': pronoun.name} for pronoun in BeVerb]
        expected = {
            'class': 'Paragraph',
            'sentence_list': [
                {'class': 'Sentence', 'word_list': word_list}
            ],
            'tags': [],
        }
        self.assertEqual(Serializer.to_dict(paragraph), expected)

    def test_to_obj_with_BeVerb_in_sentence(self):
        paragraph = Paragraph([Sentence([pronoun for pronoun in BeVerb])])
        as_dict = Serializer.to_dict(paragraph)
        self.assertEqual(Serializer.to_obj(as_dict), paragraph)

    def test_to_dict_and_back_with_all_word_types_in_multiple_sentences(self):
        paragraph = Paragraph([
            Sentence([
                Verb('go').past_tense().capitalize().bold(), Noun.uncountable_noun('water'), Punctuation.PERIOD
            ]),
            Sentence([
                BasicWord.preposition('a'), Pronoun.I, CapitalPronoun.ME, BeVerb.AM, Punctuation.COMMA.bold()
            ])
        ])
        as_dict = Serializer.to_dict(paragraph)
        as_obj = Serializer.to_obj(as_dict)
        self.assertEqual(as_obj, paragraph)

    def test_to_json(self):
        paragraph = Paragraph(
            [
                Sentence([
                    Verb('go').past_tense().capitalize().bold(), Noun.uncountable_noun('water'), Punctuation.PERIOD
                ]),
                Sentence([
                    BasicWord.preposition('a'), Pronoun.I, CapitalPronoun.ME, BeVerb.AM, Punctuation.COMMA.bold()
                ])
            ],
            Tags([StatusTag.PUNCTUATION_ERRORS])
        )
        as_dict = Serializer.to_dict(paragraph)
        self.assertEqual(json.dumps(as_dict), Serializer.to_json(paragraph))

    def test_from_json(self):
        paragraph = Paragraph(
            [
                Sentence([
                    Verb('go').past_tense().capitalize().bold(), Noun.uncountable_noun('water'), Punctuation.PERIOD
                ]),
                Sentence([
                    BasicWord.preposition('a'), Pronoun.I, CapitalPronoun.ME, BeVerb.AM, Punctuation.COMMA.bold()
                ])
            ],
            Tags([StatusTag.RAW])
        )
        as_json = Serializer.to_json(paragraph)

        self.assertEqual(paragraph, Serializer.from_json(as_json))

import json

from paragraph_generator.tags.status_tag import StatusTag
from paragraph_generator.tags.tags import Tags
from paragraph_generator.tags.wordtag import WordTag
from paragraph_generator.word_groups.paragraph import Paragraph
from paragraph_generator.word_groups.sentence import Sentence
from paragraph_generator.words.basicword import BasicWord
from paragraph_generator.words.be_verb import BeVerb
from paragraph_generator.words.noun import Noun
from paragraph_generator.words.pronoun import AbstractPronoun, Pronoun, CapitalPronoun
from paragraph_generator.words.punctuation import Punctuation
from paragraph_generator.words.verb import Verb


class Serializer(object):
    @classmethod
    def to_json(cls, python_obj):
        return json.dumps(cls.to_dict(python_obj))

    @classmethod
    def from_json(cls, json_str):
        return cls.to_obj(json.loads(json_str))

    @classmethod
    def to_dict(cls, python_obj):
        if isinstance(python_obj, Paragraph):
            return cls._paragraph_to_dict(python_obj)

    @classmethod
    def _paragraph_to_dict(cls, python_obj):
        class_ = 'Paragraph'
        sentence_list = [cls._sentence_to_dict(sentence) for sentence in python_obj.sentence_list()]
        tags = cls._tags_to_list(python_obj.tags)
        return {'class': class_, 'sentence_list': sentence_list, 'tags': tags}

    @classmethod
    def _sentence_to_dict(cls, sentence):
        word_list = [cls._word_to_dict(word) for word in sentence]
        return {'class': 'Sentence', 'word_list': word_list}

    @classmethod
    def _tags_to_list(cls, tags):
        tag_list = tags.to_list()
        return [tag.name for tag in tag_list]

    @classmethod
    def _word_to_dict(cls, word):
        class_ = word.__class__.__name__

        if isinstance(word, (AbstractPronoun, Punctuation, BeVerb)):
            return {'class': class_, 'name': word.name}
        fields = {
            'BasicWord': ['value'],
            'Noun': ['value', 'irregular_plural', 'base_noun'],
            'Verb': ['value', 'irregular_past', 'infinitive']
        }
        answer = {'class': class_, 'tags': cls._tags_to_list(word.tags)}
        for field in fields[class_]:
            answer[field] = getattr(word, field)
        return answer

    @classmethod
    def to_obj(cls, python_dict):
        if python_dict['class'] == 'Paragraph':
            return cls._to_paragraph(python_dict)

    @classmethod
    def _to_paragraph(cls, python_dict):
        sentence_list = [cls._to_sentence(sentence) for sentence in python_dict['sentence_list']]
        tags = cls._to_status_tags(python_dict['tags'])
        return Paragraph(sentence_list, tags)

    @classmethod
    def _to_sentence(cls, sentence_dict):
        return Sentence([cls._to_word(word) for word in sentence_dict['word_list']])

    @classmethod
    def _to_word(cls, word):
        params = {
            'BasicWord': (BasicWord, ('value',)),
            'Noun': (Noun, ('value', 'irregular_plural', 'base_noun')),
            'Verb': (Verb, ('value', 'irregular_past', 'infinitive'))
        }
        try:
            class_, param_fields = params[word['class']]
        except KeyError:
            return cls._to_word_from_enum(word)

        params = [word[field] for field in param_fields]
        params.append(cls._to_word_tags(word['tags']))
        return class_(*params)

    @classmethod
    def _to_word_from_enum(cls, word):
        classes = {
            'Pronoun': Pronoun,
            'CapitalPronoun': CapitalPronoun,
            'Punctuation': Punctuation,
            'BeVerb': BeVerb

        }
        class_ = classes[word['class']]
        return getattr(class_, word['name'])

    @classmethod
    def _to_status_tags(cls, name_list):
        tag_list = [getattr(StatusTag, name) for name in name_list]
        return Tags(tag_list)

    @classmethod
    def _to_word_tags(cls, name_list):
        tag_list = [getattr(WordTag, name) for name in name_list]
        return Tags(tag_list)

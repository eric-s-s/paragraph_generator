.. image:: https://travis-ci.com/eric-s-s/paragraph_generator.svg?branch=master
    :target: https://travis-ci.com/eric-s-s/paragraph_generator

.. image:: https://coveralls.io/repos/github/eric-s-s/paragraph_generator/badge.svg?branch=master
    :target: https://coveralls.io/github/eric-s-s/paragraph_generator?branch=master


paragraph_generator v1.0
========================

A micro-service component for an English Language Learners website
------------------------------------------------------------------

This is the basic back-end entry points for a service that creates a paragraph with
specific kinds of errors for ELL students (especially Mandarin Chinese speakers) to practice
basic proof reading. It is installable using pip and provides objects and functions for
generating jsons and python objects. This should then be easy to plug into almost any
server.



To install:

.. code-block:: bash

    $ pip install git+https://github.com/eric-s-s/paragraph_generator

or:

.. code-block:: bash

    $ git clone https://github.com/eric-s-s/paragraph_generator
    $ cd sentences
    $ python setup.py install  # or pip install .


Basic Documentation:
--------------------
::


    class: AnswerChecker
        __init__
            types: {'submission': <class 'str'>, 'original': <class 'paragraph_generator.word_groups.paragraph.Paragraph'>}
    
        method: count_sentence_errors
            types: {'return': <class 'int'>}
    
        method: count_word_errors
            types: {'return': <class 'int'>}
    
        method: get_sentence_hints
            docs: 
    
            :return: {'error_count': int, 'hint_paragraph': str, 'missing_sentences': int}
            
    
        method: get_word_hints
            docs: 
    
            :return: {'error_count': int, 'hint_paragraph': str, 'missing_sentences': int}
            
    
        method: is_submission_correct
            types: {'return': <class 'bool'>}
    
        method: original
    
        method: submission
    
    
    
    class: WordLists
        __init__
            docs: 
    
            :param verbs: {'verb': str, 'irregular_past': str, 'preposition': str, 'particle': str, 'objects': int}
            :param countable: {'noun': str, 'irregular_past': str}
            :param uncountable: {'noun': str}
            :param static: {'noun': str, 'is_plural': bool}
            
        method: nouns
    
        method: verbs
    
    
    
    class: ParagraphsGenerator
        __init__
            types: {'word_lists_generator': <class 'paragraph_generator.word_lists.AbstractWordLists'>}
            docs: 
    
            :config_state optional keys:
            - 'error_probability': 0.0 <= float <= 1.0
            - 'noun_errors': 0.0 <= float <= 1.0
            - 'pronoun_errors': bool
            - 'verb_errors': bool
            - 'is_do_errors': bool
            - 'preposition_transpose_errors': bool
            - 'punctuation_errors': bool
    
            - 'tense': str - 'simple_past'|'simple_present'
            - 'probability_plural_noun': 0.0 <= float <= 1.0
            - 'probability_negative_verb': 0.0 <= float <= 1.0
            - 'probability_pronoun': 0.0 <= float <= 1.0
    
            - 'paragraph_type': str - 'chain'|'pool'
            - 'subject_pool': 0 < int
            - 'paragraph_size': 0 < int
            
        method: generate_paragraphs
    
        method: get
    
        method: get_nouns
            types: {'return': typing.List[paragraph_generator.words.noun.Noun]}
    
        method: get_verbs
            types: {'return': typing.List[paragraph_generator.word_groups.verb_group.VerbGroup]}
    
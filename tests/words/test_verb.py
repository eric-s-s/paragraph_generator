import unittest

from sentences.words.verb import Verb, ConjugatedVerb, BasicVerb, NegativeVerb


class TestVerb(unittest.TestCase):

    def test_verb(self):
        verb = Verb('go')
        self.assertEqual(verb.value, 'go')
        self.assertEqual(verb.infinitive, 'go')
        self.assertEqual(verb.add_s(), Verb('goes'))
        self.assertEqual(verb.add_ed(), Verb('goed'))
        self.assertEqual(verb.capitalize(), Verb('Go', 'go'))
        self.assertEqual(repr(verb), "Verb('go', 'go')")

    def test_verb_eq(self):
        c_verb = ConjugatedVerb("don't go", 'go')
        n_verb = NegativeVerb('go')
        self.assertEqual(n_verb.value, "don't go")
        self.assertEqual(n_verb.infinitive, "go")

        self.assertTrue(n_verb.__eq__(c_verb))
        self.assertTrue(c_verb.__eq__(n_verb))
        self.assertNotEqual(Verb('go'), n_verb)

        basic = BasicVerb('go', 'went')
        self.assertEqual(basic.value, 'go')
        self.assertEqual(basic.infinitive, 'go')
        self.assertTrue(basic.__eq__(Verb('go')))
        self.assertTrue(Verb('go').__eq__(basic))

    def test_conjugated_verb(self):
        c_verb = ConjugatedVerb('went', 'go')
        self.assertEqual(c_verb.value, 'went')
        self.assertEqual(c_verb.infinitive, 'go')

    def test_conjugated_verb_repr(self):
        verb = ConjugatedVerb('don\'t do', 'do')
        self.assertEqual(repr(verb), 'ConjugatedVerb("don\'t do", \'do\')')

    def test_basic_verb_repr(self):
        verb = BasicVerb('go', 'went')
        self.assertEqual(repr(verb), "BasicVerb('go', 'went')")

        verb = BasicVerb('play')
        self.assertEqual(repr(verb), "BasicVerb('play', '')")

    def test_basic_verb_value_is_infinitive(self):
        verb = BasicVerb('go', 'went')
        self.assertEqual(verb.infinitive, 'go')
        self.assertEqual(verb.value, 'go')

    def test_basic_verb_past_tense_regular_verb(self):
        verb = BasicVerb('play')
        answer = verb.past_tense()
        self.assertIsInstance(answer, ConjugatedVerb)
        self.assertEqual(answer, ConjugatedVerb('played', 'play'))

        verb = BasicVerb('bat')
        answer = verb.past_tense()
        self.assertIsInstance(answer, ConjugatedVerb)
        self.assertEqual(answer, ConjugatedVerb('batted', 'bat'))

        verb = BasicVerb('copy')
        answer = verb.past_tense()
        self.assertIsInstance(answer, ConjugatedVerb)
        self.assertEqual(answer, ConjugatedVerb('copied', 'copy'))

        verb = BasicVerb('like')
        answer = verb.past_tense()
        self.assertIsInstance(answer, ConjugatedVerb)
        self.assertEqual(answer, ConjugatedVerb('liked', 'like'))

    def test_basic_verb_past_tense_with_irregular_verb(self):
        verb = BasicVerb('go', 'went')
        answer = verb.past_tense()
        self.assertIsInstance(answer, ConjugatedVerb)
        self.assertEqual(answer, ConjugatedVerb('went', 'go'))

    def test_basic_verb_third_person(self):
        verb = BasicVerb('go', 'went')
        answer = verb.third_person()
        self.assertIsInstance(answer, ConjugatedVerb)
        self.assertEqual(answer, ConjugatedVerb('goes', 'go'))

        verb = BasicVerb('wax')
        answer = verb.third_person()
        self.assertIsInstance(answer, ConjugatedVerb)
        self.assertEqual(answer, ConjugatedVerb('waxes', 'wax'))

        verb = BasicVerb('copy')
        answer = verb.third_person()
        self.assertIsInstance(answer, ConjugatedVerb)
        self.assertEqual(answer, ConjugatedVerb('copies', 'copy'))

    def test_basic_verb_negative(self):
        verb = BasicVerb('do', 'did')
        answer = verb.negative()
        self.assertIsInstance(answer, NegativeVerb)
        self.assertEqual(answer.value, 'don\'t do')
        self.assertEqual(answer.infinitive, 'do')

    def test_negative_verb_value_and_infinitive(self):
        verb = NegativeVerb('play')
        self.assertEqual(verb.infinitive, 'play')
        self.assertEqual(verb.value, 'don\'t play')

    def test_negative_verb_repr(self):
        verb = NegativeVerb('play')
        self.assertEqual(repr(verb), "NegativeVerb('play')")

    def test_negative_verb_past_tense(self):
        verb = NegativeVerb('play')
        answer = verb.past_tense()
        self.assertIsInstance(answer, ConjugatedVerb)
        self.assertEqual(answer, ConjugatedVerb("didn't play", 'play'))

    def test_negative_verb_third_person(self):
        verb = NegativeVerb('play')
        answer = verb.third_person()
        self.assertIsInstance(answer, ConjugatedVerb)
        self.assertEqual(answer, ConjugatedVerb("doesn't play", 'play'))

    def test_to_basic_verb(self):
        verb = Verb('play')
        basic = verb.to_basic_verb()
        self.assertEqual(verb, basic)
        self.assertIsInstance(basic, BasicVerb)

    def test_to_basic_verb_does_not_retain_special_past_tense(self):
        verb = BasicVerb('go', 'went')
        past = verb.past_tense()
        from_past_tense = past.to_basic_verb()
        from_verb = verb.to_basic_verb()

        self.assertEqual(verb, from_past_tense)
        self.assertEqual(verb, from_verb)

        past_from_past_tense = from_past_tense.past_tense()
        past_from_verb = from_verb.past_tense()

        self.assertEqual(past_from_past_tense, past_from_verb)
        self.assertNotEqual(past, past_from_verb)

        self.assertEqual(past.value, 'went')
        self.assertEqual(past_from_verb.value, 'goed')

    def test_to_basic_negative_verb(self):
        verb = BasicVerb('play').negative()
        self.assertEqual(verb.to_basic_verb(), BasicVerb('play'))

    def test_capitalize(self):
        self.assertEqual(Verb('go').capitalize(), Verb('Go', 'go'))
        self.assertEqual(ConjugatedVerb('went', 'go').capitalize(), Verb('Went', 'go'))
        basic = BasicVerb('eat')
        self.assertEqual(basic.capitalize(), BasicVerb('Eat', ))

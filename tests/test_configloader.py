import os
import unittest
from shutil import rmtree

from sentences import DATA_PATH, APP_NAME
from sentences.configloader import (CONFIG_FILE, DEFAULT_CONFIG, COUNTABLE_NOUNS_CSV, UNCOUNTABLE_NOUNS_CSV,
                                    VERBS_CSV, DEFAULT_SAVE_DIR,
                                    create_default_config, save_config, load_config, ConfigLoader,
                                    get_documents_folder, _get_key_value, _get_key_value_list,
                                    _create_line)
from sentences.gui.errordetails import ErrorDetails
from sentences.gui.filemanagement import FileManagement
from sentences.gui.grammardetails import GrammarDetails
from sentences.gui.paragraphtype import ParagraphType


def rm_config():
    if os.path.exists(CONFIG_FILE):
        os.remove(CONFIG_FILE)


def rm_app_folder():
    target = os.path.join(get_documents_folder(), APP_NAME)
    if os.path.exists(target):
        rmtree(target)


class TestConfigLoader(unittest.TestCase):

    @classmethod
    def tearDownClass(cls):
        rm_config()

    def setUp(self):
        rm_config()
        rm_app_folder()

    def test_CONFIG_FILE(self):
        self.assertEqual(CONFIG_FILE, os.path.join(DATA_PATH, 'config.cfg'))

    def test_get_documents_folder(self):
        user_dir = os.path.expanduser('~')
        docs = os.path.join(user_dir, 'Documents')
        my_docs = os.path.join(user_dir, 'My Documents')

        answer = get_documents_folder()
        self.assertIn(answer, [user_dir, docs, my_docs])
        self.assertTrue(os.path.exists(answer))

    def test_create_default_config(self):
        with open(CONFIG_FILE, 'w') as f:
            f.write('hi')

        with open(CONFIG_FILE, 'r') as f:
            before = f.read()
        self.assertEqual(before, 'hi')

        create_default_config()
        with open(DEFAULT_CONFIG, 'r') as f:
            default = f.read()

        with open(CONFIG_FILE, 'r') as f:
            current = f.read()

        self.assertNotEqual(current, before)
        self.assertEqual(current, default)

    def test_get_key_value_positive_int(self):
        self.assertEqual(_get_key_value('my_int = 123'), ('my_int', 123))
        self.assertEqual(_get_key_value(' my_int =  0 '), ('my_int', 0))

    def test_get_key_value_float(self):
        self.assertEqual(_get_key_value('my_float = 123.44'), ('my_float', 123.44))
        self.assertEqual(_get_key_value('my_float = -0.01'), ('my_float', -0.01))

    def test_get_key_value_special(self):
        self.assertEqual(_get_key_value('special = true'), ('special', True))
        self.assertEqual(_get_key_value('special = false'), ('special', False))
        self.assertEqual(_get_key_value('special = none'), ('special', None))

        self.assertEqual(_get_key_value('special = TRUE'), ('special', True))
        self.assertEqual(_get_key_value('special = FALSE'), ('special', False))
        self.assertEqual(_get_key_value('special = NONE'), ('special', None))

    def test_get_key_value_others(self):
        self.assertEqual(_get_key_value('thing = this is my thing. '), ('thing', 'this is my thing.'))

    def test_get_key_value_empty(self):
        self.assertEqual(_get_key_value(' '), ('', None))

    def test_get_key_value_list_bad_file(self):
        bad_text = 'no comment and no equal'
        to_delete = os.path.join(DATA_PATH, 'to_delete.cfg')
        with open(to_delete, 'w') as f:
            f.write(bad_text)

        self.assertRaises(ValueError, _get_key_value_list, to_delete)
        os.remove(to_delete)

    def test_get_key_value_list_default_config(self):
        answer = [
            ('# all values are case-insensitive and convert to lower case', None),
            ('', None),
            ('# FILE DETAILS', None),
            ('# home_directory = none defaults to system home. ex: C:/Users/<username>/My Documents/sentence_mangler',
             None),
            ('# save_directory = none defaults to home_directory/pdfs', None),
            ('home_directory', None),
            ('save_directory', None),
            ('', None),
            ('# word lists', None),
            ('# If none, defaults to home_directory/<filename>/[nouns.csv|uncountable.csv|verbs.csv]', None),
            ('countable_nouns', None),
            ('uncountable_nouns', None),
            ('verbs', None),
            ('', None),
            ('# ERROR DETAILS', None),
            ('error_probability', 0.2),
            ('', None),
            ('noun_errors', True),
            ('verb_errors', True),
            ('punctuation_errors', True),
            ('', None),
            ('# GRAMMAR DETAILS', None),
            ('# tense option: simple_present, simple_past', None),
            ('tense', 'simple_present'),
            ('probability_plural_noun', 0.3),
            ('probability_negative_verb', 0.3),
            ('probability_pronoun', 0.2),
            ('', None),
            ('# PARAGRAPH TYPE AND SIZE', None),
            ('# paragraph_type option: chain, pool', None),
            ('# subject_pool determines the number of subjects for pool type', None),
            ('paragraph_type', 'chain'),
            ('subject_pool', 5),
            ('num_paragraphs', 4),
            ('paragraph_size', 15),
            ('', None),
        ]
        self.assertEqual(_get_key_value_list(DEFAULT_CONFIG), answer)

    def test_create_line(self):
        self.assertEqual(_create_line('thing', 'string'), 'thing = string')
        self.assertEqual(_create_line('file', 'E:/data/thing.csv'), 'file = E:/data/thing.csv')
        self.assertEqual(_create_line('file', 'E:\\data\\thing.csv'), 'file = E:\\data\\thing.csv')
        self.assertEqual(_create_line('int', 10), 'int = 10')
        self.assertEqual(_create_line('float', 3.5), 'float = 3.5')
        self.assertEqual(_create_line('TRUE', True), 'TRUE = true')
        self.assertEqual(_create_line('FALSE', False), 'FALSE = false')
        self.assertEqual(_create_line('NONE', None), 'NONE = none')

    def test_save_config(self):
        with open(DEFAULT_CONFIG, 'r') as f:
            default_text = f.read()
        save_config({'paragraph_type': 'bobo', 'paragraph_size': 10})
        with open(CONFIG_FILE, 'r') as f:
            config_text = f.read()

        answer = default_text.replace('paragraph_size = 15', 'paragraph_size = 10')
        answer = answer.replace('paragraph_type = chain', 'paragraph_type = bobo')
        self.assertEqual(answer, config_text)

    def test_load_config_default_config(self):
        answer = load_config(DEFAULT_CONFIG)
        self.assertEqual(answer, {
            'home_directory': None,
            'save_directory': None,
            'countable_nouns': None,
            'uncountable_nouns': None,
            'verbs': None,

            'error_probability': 0.2,
            'noun_errors': True,
            'verb_errors': True,
            'punctuation_errors': True,

            'tense': 'simple_present',
            'probability_plural_noun': 0.3,
            'probability_negative_verb': 0.3,
            'probability_pronoun': 0.2,

            'paragraph_type': 'chain',
            'subject_pool': 5,
            'num_paragraphs': 4,
            'paragraph_size': 15,
        })

    def test_load_config_bad_file_ValueError(self):
        bad_text = 'no comment and no equal'
        to_delete = os.path.join(DATA_PATH, 'to_delete.cfg')
        with open(to_delete, 'w') as f:
            f.write(bad_text)

        self.assertRaises(ValueError, load_config, to_delete)
        os.remove(to_delete)

    def test_load_config_missing_file_OSError(self):
        self.assertRaises(OSError, load_config, 'not_there.cfg')

    def assert_ConfigLoader_state(self, config_loader, home_dir, save_dir, *exclude_files):
        all_files = {'countable_nouns': COUNTABLE_NOUNS_CSV,
                     'uncountable_nouns': UNCOUNTABLE_NOUNS_CSV,
                     'verbs': VERBS_CSV}
        to_check = {key: filename for key, filename in all_files.items() if filename not in exclude_files}

        for key, filename in to_check.items():
            full_path = os.path.join(home_dir, filename)
            self.assertEqual(config_loader.state[key], full_path)
            with open(os.path.join(DATA_PATH, filename), 'r') as default:
                with open(full_path, 'r') as target:
                    self.assertEqual(default.read(), target.read())

        self.assertEqual(config_loader.state['home_directory'], home_dir)
        self.assertEqual(config_loader.state['save_directory'], save_dir)

    def assert_default_ConfigLoader_state(self, config_loader):
        with open(DEFAULT_CONFIG, 'r') as default:
            with open(CONFIG_FILE, 'r') as target:
                self.assertEqual(default.read(), target.read())

        home_dir = os.path.join(get_documents_folder(), APP_NAME)
        save_dir = os.path.join(home_dir, DEFAULT_SAVE_DIR)
        self.assert_ConfigLoader_state(config_loader, home_dir, save_dir)

    def test_ConfigLoader_state_is_copy(self):
        to_test = ConfigLoader()
        self.assertIsNot(to_test._dictionary, to_test.state)

    def test_ConfigLoader_init_whole_state(self):
        answer = ConfigLoader().state
        home = os.path.join(get_documents_folder(), APP_NAME)
        expected = {
            'home_directory': home,
            'save_directory': os.path.join(home, DEFAULT_SAVE_DIR),
            'countable_nouns': os.path.join(home, COUNTABLE_NOUNS_CSV),
            'uncountable_nouns': os.path.join(home, UNCOUNTABLE_NOUNS_CSV),
            'verbs': os.path.join(home, VERBS_CSV),

            'error_probability': 0.2,
            'noun_errors': True,
            'verb_errors': True,
            'punctuation_errors': True,

            'tense': 'simple_present',
            'probability_plural_noun': 0.3,
            'probability_negative_verb': 0.3,
            'probability_pronoun': 0.2,

            'paragraph_type': 'chain',
            'subject_pool': 5,
            'num_paragraphs': 4,
            'paragraph_size': 15,
        }
        self.assertEqual(answer, expected)

    def test_ConfigLoader_init_no_config_file_no_home_dir(self):
        new = ConfigLoader()
        self.assert_default_ConfigLoader_state(new)

    def test_ConfigLoader_init_corrupted_config_file(self):
        with open(CONFIG_FILE, 'w') as f:
            f.write('ooooops')

        new = ConfigLoader()
        self.assert_default_ConfigLoader_state(new)

    def test_ConfigLoader_init_no_config_file_has_home_dir_and_some_files(self):
        app_folder = os.path.join(get_documents_folder(), APP_NAME)
        os.mkdir(app_folder)
        with open(os.path.join(app_folder, VERBS_CSV), 'w') as f:
            f.write('hi there')

        new = ConfigLoader()
        save = os.path.join(app_folder, DEFAULT_SAVE_DIR)
        self.assert_ConfigLoader_state(new, app_folder, save, VERBS_CSV)

        with open(os.path.join(app_folder, VERBS_CSV), 'r') as f:
            self.assertEqual(f.read(), 'hi there')
        self.assertEqual(new.state['verbs'], os.path.join(app_folder, VERBS_CSV))

    def test_ConfigLoader_init_existing_config_file_existing_files(self):
        home = os.path.abspath('to_delete')
        save = os.path.abspath('bogus_save')
        existing_verbs = os.path.join(home, 'my_verb.csv')

        os.mkdir(home)
        os.mkdir(save)
        with open(existing_verbs, 'w') as f:
            f.write('exists')

        save_config({'home_directory': home, 'save_directory': save, 'verbs': existing_verbs})

        new = ConfigLoader()
        self.assert_ConfigLoader_state(new, home, save, VERBS_CSV)

        with open(existing_verbs, 'r') as f:
            self.assertEqual(f.read(), 'exists')
        self.assertEqual(new.state['verbs'], existing_verbs)

        rmtree(home)
        rmtree(save)

    def test_ConfigLoader_init_existing_config_file_non_existent_files(self):
        home = os.path.abspath('to_delete')
        save = os.path.abspath('bogus_save')
        existing_verbs = os.path.join(home, 'not_really_there.csv')

        os.mkdir(home)
        os.mkdir(save)

        save_config({'home_directory': home, 'save_directory': save, 'verbs': existing_verbs})

        new = ConfigLoader()
        self.assert_ConfigLoader_state(new, home, save)

        # cleanup
        rmtree(home)
        rmtree(save)

    def test_ConfigLoader_init_existing_config_file_non_existent_directories_only_if_parent_path_exists(self):
        home = os.path.abspath('to_delete')
        save = os.path.join(home, 'bogus_save')

        save_config({'home_directory': home, 'save_directory': save})

        new = ConfigLoader()
        self.assert_ConfigLoader_state(new, home, save)

        # cleanup
        rmtree(home)

    def test_ConfigLoader_init_existing_config_fails_when_directory_parent_not_there(self):
        home = 'not_there/really_not_there'
        save_config({'home_directory': home})
        self.assertRaises(OSError, ConfigLoader)

    def test_ConfigLoader_reload_config_config_did_not_change(self):
        new = ConfigLoader()
        new.reload()
        self.assert_default_ConfigLoader_state(new)

    def test_ConfigLoader_reload_home_directory_change(self):
        new = ConfigLoader()
        new_home = os.path.abspath('delete_me')
        old_home = os.path.join(get_documents_folder(), APP_NAME)
        full_config = new.state
        full_config.update({'home_directory': new_home})
        self.assertNotEqual(full_config, new.state)

        save_config(full_config)
        new.reload()

        self.assertEqual(full_config, new.state)
        for filename in [COUNTABLE_NOUNS_CSV, UNCOUNTABLE_NOUNS_CSV, VERBS_CSV]:
            with open(os.path.join(DATA_PATH, filename), 'r') as default:
                with open(os.path.join(old_home, filename), 'r') as target:
                    self.assertEqual(default.read(), target.read())
        # new_home should be empty. If this raises an error, there's something very wrong.
        os.rmdir(new_home)

    def test_ConfigLoader_reload_home_directory_change_NEEDS_TO_UPDATE_FULL_CONFIG(self):
        new = ConfigLoader()
        new_home = os.path.abspath('delete_me')
        old_home = os.path.join(get_documents_folder(), APP_NAME)

        save_config({'home_directory': new_home})
        new.reload()

        to_check = {'countable_nouns': COUNTABLE_NOUNS_CSV,
                    'uncountable_nouns': UNCOUNTABLE_NOUNS_CSV,
                    'verbs': VERBS_CSV}
        for key, filename in to_check.items():
            self.assertEqual(new.state[key], os.path.join(new_home, filename))

            with open(os.path.join(DATA_PATH, filename), 'r') as default:
                default_text = default.read()

            with open(os.path.join(old_home, filename), 'r') as old_file:
                self.assertEqual(old_file.read(), default_text)
            with open(os.path.join(new_home, filename), 'r') as new_file:
                self.assertEqual(new_file.read(), default_text)
        rmtree(new_home)

    def test_ConfigLoader_save_and_update_home_directory_change_keeps_original_csvs(self):
        new = ConfigLoader()
        new_home = os.path.abspath('delete_me')
        old_home = os.path.join(get_documents_folder(), APP_NAME)
        full_config = new.state
        full_config.update({'home_directory': new_home})
        self.assertNotEqual(full_config, new.state)

        new.save_and_reload({'home_directory': new_home})

        self.assertEqual(full_config, new.state)
        for filename in [COUNTABLE_NOUNS_CSV, UNCOUNTABLE_NOUNS_CSV, VERBS_CSV]:
            with open(os.path.join(DATA_PATH, filename), 'r') as default:
                with open(os.path.join(old_home, filename), 'r') as target:
                    self.assertEqual(default.read(), target.read())
        # new_home should be empty. If this raises an error, there's something very wrong.
        os.rmdir(new_home)

    def test_ConfigLoader_save_and_update_does_not_overwrite_files(self):
        new = ConfigLoader()
        home = os.path.join(get_documents_folder(), APP_NAME)
        save = os.path.join(home, DEFAULT_SAVE_DIR)
        verb_file = os.path.join(home, VERBS_CSV)
        with open(verb_file, 'w') as f:
            f.write('new stuff')
        new.save_and_reload({})

        self.assert_ConfigLoader_state(new, home, save, VERBS_CSV)
        with open(verb_file, 'r') as f:
            self.assertEqual(f.read(), 'new stuff')
        self.assertEqual(new.state['verbs'], verb_file)

    def test_ConfigLoader_revert_to_default_resets_csvs_but_leaves_other_files(self):
        new = ConfigLoader()
        home = os.path.join(get_documents_folder(), APP_NAME)
        save = os.path.join(home, DEFAULT_SAVE_DIR)
        home_files = [VERBS_CSV, COUNTABLE_NOUNS_CSV, 'foo.txt', 'bar.txt']
        save_files = ['foo.txt', 'bar.txt']
        write_files = [os.path.join(home, filename) for filename in home_files]
        write_files += [os.path.join(save, filename) for filename in save_files]
        files_not_reset = write_files[2:]
        for filename in write_files:
            with open(filename, 'w') as f:
                f.write('foobar')

        new.revert_to_default()

        self.assert_default_ConfigLoader_state(new)
        for filename in files_not_reset:
            with open(filename, 'r') as f:
                self.assertEqual(f.read(), 'foobar')

    def test_ConfigLoader_revert_to_default_creates_files_and_directories(self):
        home_to_delete = os.path.abspath('delete_me')
        save_config({'home_directory': home_to_delete})
        new = ConfigLoader()

        home = os.path.join(get_documents_folder(), APP_NAME)
        self.assertFalse(os.path.exists(home))

        for filename in [VERBS_CSV, COUNTABLE_NOUNS_CSV, UNCOUNTABLE_NOUNS_CSV]:
            self.assertTrue(os.path.exists(os.path.join(home_to_delete, filename)))

        new.revert_to_default()

        for filename in [VERBS_CSV, COUNTABLE_NOUNS_CSV, UNCOUNTABLE_NOUNS_CSV]:
            self.assertTrue(os.path.exists(os.path.join(home_to_delete, filename)))
        self.assert_default_ConfigLoader_state(new)

        rmtree(home_to_delete)

    def test_ConfigLoader_set_up_frame_FileManagement(self):
        fm = FileManagement()
        loader = ConfigLoader()
        loader.set_up_frame(fm)
        home = os.path.join(get_documents_folder(), APP_NAME)
        answer = {'home_directory': home,
                  'save_directory': os.path.join(home, DEFAULT_SAVE_DIR),
                  'countable_nouns': os.path.join(home, COUNTABLE_NOUNS_CSV),
                  'uncountable_nouns': os.path.join(home, UNCOUNTABLE_NOUNS_CSV),
                  'verbs': os.path.join(home, VERBS_CSV)}

        self.assertEqual(fm.get_values(), answer)

    def test_ConfigLoader_set_up_frame_ErrorDetails(self):
        ed = ErrorDetails()
        loader = ConfigLoader()
        loader.set_up_frame(ed)
        answer = {'error_probability': 0.2,
                  'noun_errors': True,
                  'verb_errors': True,
                  'punctuation_errors': True}

        self.assertEqual(ed.get_values(), answer)

    def test_ConfigLoader_set_up_frame_GrammarDetails(self):
        gd = GrammarDetails()
        loader = ConfigLoader()
        loader.set_up_frame(gd)
        answer = {'tense': 'simple_present',
                  'probability_plural_noun': 0.3,
                  'probability_negative_verb': 0.3,
                  'probability_pronoun': 0.2}

        self.assertEqual(gd.get_values(), answer)

    def test_ConfigLoader_set_up_frame_ParagraphType(self):
        pt = ParagraphType()
        loader = ConfigLoader()
        loader.set_up_frame(pt)
        answer = {'paragraph_type': 'chain',
                  'subject_pool': 5,
                  'num_paragraphs': 4,
                  'paragraph_size': 15}

        self.assertEqual(pt.get_values(), answer)

    def test_ConfigLoader_change_default_then_set_up_again(self):
        pt = ParagraphType()
        loader = ConfigLoader()
        loader.set_up_frame(pt)
        loader.save_and_reload({'subject_pool': 3})
        loader.set_up_frame(pt)

        answer = {'paragraph_type': 'chain',
                  'subject_pool': 3,
                  'num_paragraphs': 4,
                  'paragraph_size': 15}

        self.assertEqual(pt.get_values(), answer)

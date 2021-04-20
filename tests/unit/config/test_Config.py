from unittest import TestCase

from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Files import folder_exists, folder_delete_all, file_not_exists, file_exists,temp_folder
from osbot_utils.utils.Misc import list_set

from config.Config import *
import os
class test_Config(TestCase):

    config = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.config  = Config()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.config.load_values()

    def test_load_values(self):
        config = self.config

        self.assertEqual(config.file_generator_location , os.environ.get("FILE_GENERATOR_LOCATION" , FILE_GENERATOR_LOCATION))
        assert folder_exists(config.file_generator_location        )

    def test_ensure_last_char_is_not_forward_slash(self):
        assert self.config.ensure_last_char_is_not_forward_slash(''     ) == ''
        assert self.config.ensure_last_char_is_not_forward_slash('\\'   ) == ''
        assert self.config.ensure_last_char_is_not_forward_slash('/'    ) == ''
        assert self.config.ensure_last_char_is_not_forward_slash('/a'   ) == '/a'
        assert self.config.ensure_last_char_is_not_forward_slash('./a'  ) == './a'
        assert self.config.ensure_last_char_is_not_forward_slash('./a/' ) == './a'
        assert self.config.ensure_last_char_is_not_forward_slash('/a/b' ) == '/a/b'
        assert self.config.ensure_last_char_is_not_forward_slash('/a/b/') == '/a/b'

    def test_set_cdr_plugin_folder_to_folder(self):
        tmp_folder=temp_folder()
        file_generator_location = path_combine(tmp_folder, 'aaaa')
        assert file_not_exists(file_generator_location)
        self.config.set_generator_location(file_generator_location)
        assert self.config.file_generator_location == file_generator_location
        assert file_exists(file_generator_location)
        assert folder_delete_all(file_generator_location)


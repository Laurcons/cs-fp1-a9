
import unittest
from src.lib.settings import *

class TestSettings(unittest.TestCase):
    def setUp(self):
        self.__settings_string = """
            setting1 = value1
            setting2 = "value 2! "
            setting3 =    VALUEE   17!
            setting4  = "this quoted string contains ' "quotes" ' inside of it."
        """
        self.__settings = Settings()

    def test_processing(self):
        self.__settings.load_string(self.__settings_string)
        self.assertEqual(self.__settings['setting1'], 'value1')
        self.assertEqual(self.__settings['setting2'], 'value 2! ')
        self.assertEqual(self.__settings['setting3'], 'VALUEE   17!')
        self.assertEqual(self.__settings['setting4'], 'this quoted string contains \' "quotes" \' inside of it.')

        self.__settings_string = """setting with an unallowable name = blah"""
        with self.assertRaises(SettingsError):
            self.__settings.load_string(self.__settings_string)

        self.__settings_string = "setting_with_all_allowable_characters1234567890" \
                                 "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz = blah"
        # works
        self.__settings.load_string(self.__settings_string)

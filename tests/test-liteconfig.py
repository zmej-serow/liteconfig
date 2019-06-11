import os
import unittest
import liteconfig


config_as_string = """
; you can have properties belonging to no section (i.e., in very simple sectionless configs)
property = value

[section]
; this comment will be ignored
heads = tails
truth = lie
nokia = 3310

[misc]
# this comment will be ignored too
kill_all_humans = yes
pi = 3.14159

[юникод]
文字 = 😉
"""
config_as_list = ['; you can have properties belonging to no section (i.e., in very simple sectionless configs)',
'property = value','','[section]', '; this comment will be ignored', 'heads = tails', 'truth = lie', 'nokia = 3310',
'', '[misc]', '# this comment will be ignored too', 'kill_all_humans = yes', 'pi = 3.14159', '', '[юникод]', '文字 = 😉']


class TestLiteConfig(unittest.TestCase):
    variants = [liteconfig.Config('tests/fixtures/test.ini'),
                liteconfig.Config(config_as_list),
                liteconfig.Config(config_as_string)]

    def test_init_config(self):
        for x in self.variants:
            self.assertIsInstance(x, liteconfig.Config)

    def test_has_section(self):
        for x in self.variants:
            self.assertTrue(x.has_section('misc'))
            self.assertFalse(x.has_section('misq'))

    def test_has_property(self):
        for x in self.variants:
            self.assertTrue(x.has_property('pi', 'misc'))
            self.assertTrue(x.has_property('property'))
            self.assertFalse(x.has_property('properti'))
            self.assertFalse(x.has_property('e', 'misc'))
            self.assertFalse(x.has_property('e', 'misq'))
            self.assertFalse(x.has_property('pi', 'misq'))

    def test_dot_notation(self):
        for x in self.variants:
            self.assertEqual(x.misc.pi, 3.14159)
            self.assertEqual(x.property, 'value')
            self.assertFalse(x.nonexistent)
            self.assertFalse(x.void.nonexistent)
            self.assertFalse(x.void.nonexistent.etcetera)

    def test_write(self):
        test_values = ['property = value', '[section]', 'first = 1', '[partition]', 'second = 2']
        cfg1 = liteconfig.Config(test_values)
        cfg1.write('tests/fixtures/out.ini')
        cfg2 = liteconfig.Config('tests/fixtures/out.ini')
        self.assertEqual(cfg1._Config__properties, cfg2._Config__properties)
        self.assertEqual(len(cfg2._Config__properties), 3)
        self.assertEqual(cfg1._Config__sections, cfg2._Config__sections)
        self.assertEqual(len(cfg2._Config__sections), 2)
        self.assertEqual(cfg1.property, cfg2.property)
        self.assertEqual(cfg1.section.first, cfg2.section.first, 1)
        self.assertEqual(cfg1.partition.second, cfg2.partition.second, 2)
        os.remove('tests/fixtures/out.ini')

    def test_delimiter(self):
        cfg = liteconfig.Config(['property: is here'], delimiter=':')
        self.assertEqual(cfg.property, 'is here')

    def test_comment_markers(self):
        cfg = liteconfig.Config(['-property: is here', '=property: is here'], comment_markers='-=')
        self.assertFalse(cfg.property)

    def test_parse_numbers_yes(self):
        cfg = liteconfig.Config(['rough_pi = 3', 'pi = 3.14'], parse_numbers=True)
        self.assertEqual(cfg.rough_pi, 3)
        self.assertIsInstance(cfg.rough_pi, int)
        self.assertEqual(cfg.pi, 3.14)
        self.assertIsInstance(cfg.pi, float)

    def test_parse_numbers_no(self):
        cfg = liteconfig.Config(['rough_pi = 3', 'pi = 3.14'], parse_numbers=False)
        self.assertEqual(cfg.rough_pi, '3')
        self.assertEqual(cfg.pi, '3.14')

    def test_parse_booleans_yes(self):
        test_values = ['a = yes', 'b = no',
                       'c = True', 'd = False',
                       'e = on', 'f = off']
        cfg = liteconfig.Config(test_values, parse_booleans=True)
        self.assertTrue(cfg.a)
        self.assertTrue(cfg.c)
        self.assertTrue(cfg.e)
        self.assertFalse(cfg.b)
        self.assertFalse(cfg.d)
        self.assertFalse(cfg.f)

    def test_parse_booleans_no(self):
        test_values = ['a = yes', 'b = no',
                       'c = True', 'd = False',
                       'e = on', 'f = off']
        cfg = liteconfig.Config(test_values, parse_booleans=False)
        self.assertIsInstance(cfg.a, str)
        self.assertIsInstance(cfg.a, str)
        self.assertIsInstance(cfg.b, str)
        self.assertIsInstance(cfg.c, str)
        self.assertIsInstance(cfg.d, str)
        self.assertIsInstance(cfg.e, str)
        self.assertIsInstance(cfg.f, str)

    def test_unicode(self):
        for x in self.variants:
            self.assertEqual(x.юникод.文字, '😉')

    def test_encodings(self):
        cfg = liteconfig.Config('tests/fixtures/koi8-r.ini', encoding='koi8_r')
        self.assertEqual(cfg.бНОПНЯ, "Вопрос")
        self.assertFalse(cfg.Вопрос)
        cfg = liteconfig.Config('tests/fixtures/koi8-r.ini', encoding='cp1251')
        self.assertEqual(cfg.Вопрос, "чПРТПУ")
        self.assertFalse(cfg.чПРТПУ)
        with self.assertRaises(UnicodeError):
            _ = liteconfig.Config('tests/fixtures/koi8-r.ini')

    def test_exceptions(self):
        test_list = ['stray = cats', '[section]', 'truth = lie']
        cfg = liteconfig.Config(test_list, exceptions=False)
        self.assertFalse(cfg.void)
        self.assertFalse(cfg.nonexistent.void)
        self.assertFalse(cfg.section.void)
        self.assertTrue(cfg.stray)
        self.assertTrue(cfg.section.truth)
        cfg = liteconfig.Config(test_list, exceptions=True)
        with self.assertRaises(AttributeError):
            _ = cfg.void
        with self.assertRaises(AttributeError):
            _ = cfg.nonexistent
        with self.assertRaises(AttributeError):
            _ = cfg.void.nonexistent
        with self.assertRaises(AttributeError):
            _ = cfg.section.void

    def test_filenotfound(self):
        with self.assertRaises(FileNotFoundError):
            _ = liteconfig.Config('nonexistent.ini')

    def test_invalid_input(self):
        with self.assertRaises(ValueError):
            _ = liteconfig.Config(14)
        with self.assertRaises(ValueError):
            _ = liteconfig.Config(True)
        with self.assertRaises(ValueError):
            _ = liteconfig.Config((23,))
        with self.assertRaises(ValueError):
            _ = liteconfig.Config({'we': 'they'})


if __name__ == '__main__':
    unittest.main()

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
            assert isinstance(x, liteconfig.Config)

    def test_has_section(self):
        for x in self.variants:
            assert x.has_section('misc')
            assert not x.has_section('misq')

    def test_has_property(self):
        for x in self.variants:
            assert x.has_property('pi', 'misc')
            assert x.has_property('property')
            assert not x.has_property('properti')
            assert not x.has_property('e', 'misc')
            assert not x.has_property('e', 'misq')
            assert not x.has_property('pi', 'misq')

    def test_dot_notation(self):
        for x in self.variants:
            assert x.misc.pi == 3.14159
            assert x.property == 'value'
            assert not x.nonexistent
            assert not x.void.nonexistent
            assert not x.void.nonexistent.etcetera

    def test_write(self):
        test_values = ['property = value', '[section]', 'first = 1', '[partition]', 'second = 2']
        cfg1 = liteconfig.Config(test_values)
        cfg1.write('tests/fixtures/out.ini')
        cfg2 = liteconfig.Config('tests/fixtures/out.ini')
        assert cfg2._Config__properties == cfg1._Config__properties
        assert len(cfg2._Config__properties) == 3
        assert cfg2._Config__sections == cfg1._Config__sections
        assert len(cfg2._Config__sections) == 2
        assert cfg1.property == cfg2.property
        assert cfg1.section.first == cfg2.section.first == 1
        assert cfg1.partition.second == cfg2.partition.second == 2
        os.remove('tests/fixtures/out.ini')

    def test_delimiter(self):
        cfg = liteconfig.Config(['property: is here'], delimiter=':')
        assert cfg.property == 'is here'

    def test_comment_markers(self):
        cfg = liteconfig.Config(['-property: is here', '=property: is here'], comment_markers='-=')
        assert not cfg.property

    def test_parse_numbers_yes(self):
        cfg = liteconfig.Config(['rough_pi = 3', 'pi = 3.14'], parse_numbers=True)
        assert cfg.rough_pi == 3
        assert cfg.pi == 3.14

    def test_parse_numbers_no(self):
        cfg = liteconfig.Config(['rough_pi = 3', 'pi = 3.14'], parse_numbers=False)
        assert cfg.rough_pi == '3'
        assert cfg.pi == '3.14'

    def test_parse_booleans_yes(self):
        test_values = ['a = yes', 'b = no',
                       'c = True', 'd = False',
                       'e = on', 'f = off']
        cfg = liteconfig.Config(test_values, parse_booleans=True)
        assert cfg.a == cfg.c == cfg.e is True
        assert cfg.b == cfg.d == cfg.f is False

    def test_parse_booleans_no(self):
        test_values = ['a = yes', 'b = no',
                       'c = True', 'd = False',
                       'e = on', 'f = off']
        cfg = liteconfig.Config(test_values, parse_booleans=False)
        assert not isinstance(cfg.a, bool)
        assert not isinstance(cfg.b, bool)
        assert not isinstance(cfg.c, bool)
        assert not isinstance(cfg.d, bool)
        assert not isinstance(cfg.e, bool)
        assert not isinstance(cfg.f, bool)

    def test_unicode(self):
        for x in self.variants:
            assert x.юникод.文字 == '😉'

    def test_encodings(self):
        cfg = liteconfig.Config('tests/fixtures/koi8-r.ini', encoding='koi8_r')
        assert cfg.бНОПНЯ == "Вопрос"
        assert not cfg.Вопрос
        cfg = liteconfig.Config('tests/fixtures/koi8-r.ini', encoding='cp1251')
        assert cfg.Вопрос == "чПРТПУ"
        assert not cfg.чПРТПУ
        with self.assertRaises(UnicodeError):
            _ = liteconfig.Config('tests/fixtures/koi8-r.ini')

    def test_exceptions(self):
        test_list = ['stray = cats', '[section]', 'truth = lie']
        cfg = liteconfig.Config(test_list, exceptions=False)
        assert not cfg.void
        assert not cfg.nonexistent.void
        assert not cfg.section.void
        assert cfg.stray
        assert cfg.section.truth
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

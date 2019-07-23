import os
import liteconfig
import pytest


def test_init_config(common_configs):
    for config in common_configs:
        assert isinstance(config, liteconfig.Config)


def test_has_section(common_configs):
    for config in common_configs:
        assert config.has_section('misc')
        assert not config.has_section('misq')


def test_has_property(common_configs):
    for config in common_configs:
        assert config.has_property('pi', 'misc')
        assert config.has_property('property')
        assert not config.has_property('properti')
        assert not config.has_property('e', 'misc')
        assert not config.has_property('e', 'misq')
        assert not config.has_property('pi', 'misq')


def test_dot_notation(common_configs):
    for config in common_configs:
        assert config.misc.pi == 3.14159
        assert config.property == 'value'
        assert not config.nonexistent
        assert not config.void.nonexistent
        assert not config.void.nonexistent.etcetera


def test_unicode(common_configs):
    for config in common_configs:
        assert config.юникод.文字 == '😉'


def test_filenotfound():
    with pytest.raises(FileNotFoundError):
        _ = liteconfig.Config('nonexistent.ini')


def test_not_implemented():
    with pytest.raises(NotImplementedError):
        _ = liteconfig.Config(['hierarchy = test'], hierarchy=1)


def test_invalid_input():
    with pytest.raises(ValueError):
        _ = liteconfig.Config(14)
    with pytest.raises(ValueError):
        _ = liteconfig.Config(True)
    with pytest.raises(ValueError):
        _ = liteconfig.Config((23,))
    with pytest.raises(ValueError):
        _ = liteconfig.Config({'we': 'they'})


class TestLiteConfig:

    def test_write(self):
        test_values = ['property = value', '[section]', 'first = 1', '[partition]', 'second = 2']
        cfg1 = liteconfig.Config(test_values)
        cfg1.write('tests/fixtures/out.ini')
        cfg2 = liteconfig.Config('tests/fixtures/out.ini')
        assert cfg1._Config__properties == cfg2._Config__properties
        assert len(cfg2._Config__properties) == 3
        assert cfg1._Config__sections == cfg2._Config__sections
        assert len(cfg2._Config__sections) == 2
        assert cfg1.property == cfg2.property
        assert cfg1.section.first == cfg2.section.first, 1
        assert cfg1.partition.second == cfg2.partition.second, 2
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
        assert isinstance(cfg.rough_pi, int)
        assert cfg.pi == 3.14
        assert isinstance(cfg.pi, float)

    def test_parse_numbers_no(self):
        cfg = liteconfig.Config(['rough_pi = 3', 'pi = 3.14'], parse_numbers=False)
        assert cfg.rough_pi == '3'
        assert cfg.pi == '3.14'

    def test_parse_booleans_yes(self):
        test_values = ['a = yes', 'b = no',
                       'c = True', 'd = False',
                       'e = on', 'f = off']
        cfg = liteconfig.Config(test_values, parse_booleans=True)
        assert cfg.a
        assert cfg.c
        assert cfg.e
        assert not cfg.b
        assert not cfg.d
        assert not cfg.f

    def test_parse_booleans_no(self):
        test_values = ['a = yes', 'b = no',
                       'c = True', 'd = False',
                       'e = on', 'f = off']
        cfg = liteconfig.Config(test_values, parse_booleans=False)
        assert isinstance(cfg.a, str)
        assert isinstance(cfg.a, str)
        assert isinstance(cfg.b, str)
        assert isinstance(cfg.c, str)
        assert isinstance(cfg.d, str)
        assert isinstance(cfg.e, str)
        assert isinstance(cfg.f, str)

    def test_encodings(self):
        cfg = liteconfig.Config('tests/fixtures/koi8-r.ini', encoding='koi8_r')
        assert cfg.бНОПНЯ == "Вопрос"
        assert not cfg.Вопрос
        cfg = liteconfig.Config('tests/fixtures/koi8-r.ini', encoding='cp1251')
        assert cfg.Вопрос == "чПРТПУ"
        assert not cfg.чПРТПУ
        with pytest.raises(UnicodeError):
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
        with pytest.raises(AttributeError):
            _ = cfg.void
        with pytest.raises(AttributeError):
            _ = cfg.nonexistent
        with pytest.raises(AttributeError):
            _ = cfg.void.nonexistent
        with pytest.raises(AttributeError):
            _ = cfg.section.void

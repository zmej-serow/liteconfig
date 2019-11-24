import os
import liteconfig
import pytest


def test_init_config(common_configs):
    assert isinstance(common_configs, liteconfig.Config)


def test_has_section(common_configs):
    assert common_configs.has_section('misc')
    assert not common_configs.has_section('misq')


def test_has_property(common_configs):
    assert common_configs.has_property('pi', 'misc')
    assert common_configs.has_property('property')
    assert not common_configs.has_property('properti')
    assert not common_configs.has_property('e', 'misc')
    assert not common_configs.has_property('e', 'misq')
    assert not common_configs.has_property('pi', 'misq')


def test_dot_notation(common_configs):
    assert common_configs.misc.pi == 3.14159
    assert common_configs.property == 'value'
    assert not common_configs.nonexistent
    assert not common_configs.void.nonexistent
    assert not common_configs.void.nonexistent.etcetera


def test_unicode(common_configs):
    assert common_configs.юникод.文字 == '😉'


def test_file_not_found():
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


def test_write(simple_config):
    simple_config.write('tests/fixtures/out.ini')
    cfg2 = liteconfig.Config('tests/fixtures/out.ini')
    assert simple_config._Config__properties == cfg2._Config__properties
    assert len(cfg2._Config__properties) == 3
    assert simple_config._Config__sections == cfg2._Config__sections
    assert len(cfg2._Config__sections) == 2
    assert simple_config.property == cfg2.property
    assert simple_config.section.first == cfg2.section.first, 1
    assert simple_config.partition.second == cfg2.partition.second, 2
    os.remove('tests/fixtures/out.ini')


def test_delimiter(delimiter_configs):
    assert delimiter_configs.property == 'is here'


def test_comment_markers(comment_markers):
    assert not comment_markers.has_property('property')


def test_parsing_numbers(parse_numbers):
    if parse_numbers._Config__parse_numbers:
        assert parse_numbers.rough_pi == 3
        assert isinstance(parse_numbers.rough_pi, int)
        assert parse_numbers.pi == 3.14
        assert isinstance(parse_numbers.pi, float)
    else:
        assert parse_numbers.rough_pi == '3'
        assert parse_numbers.pi == '3.14'


def test_parsing_booleans(parse_booleans):
    if parse_booleans._Config__parse_booleans:
        assert parse_booleans.a
        assert parse_booleans.c
        assert parse_booleans.e
        assert not parse_booleans.b
        assert not parse_booleans.d
        assert not parse_booleans.f
    else:
        assert isinstance(parse_booleans.a, str)
        assert isinstance(parse_booleans.b, str)
        assert isinstance(parse_booleans.c, str)
        assert isinstance(parse_booleans.d, str)
        assert isinstance(parse_booleans.e, str)
        assert isinstance(parse_booleans.f, str)


def test_encodings(encodings):
    if encodings._Config__encoding == 'koi8_r':
        assert encodings.бНОПНЯ == "Вопрос"
        assert not encodings.Вопрос
    elif encodings._Config__encoding == 'cp1251':
        assert encodings.Вопрос == "чПРТПУ"
        assert not encodings.чПРТПУ


def test_exceptions(exceptions):
    if exceptions._Config__exceptions:
        with pytest.raises(AttributeError):
            _ = exceptions.void
        with pytest.raises(AttributeError):
            _ = exceptions.nonexistent
        with pytest.raises(AttributeError):
            _ = exceptions.void.nonexistent
        with pytest.raises(AttributeError):
            _ = exceptions.section.void
    else:
        assert not exceptions.void
        assert not exceptions.nonexistent.void
        assert not exceptions.section.void
        assert exceptions.stray
        assert exceptions.section.truth

import liteconfig
import pytest


list_input = ['; you can have properties belonging to no section (i.e., in very simple sectionless configs)',
                'property = value',
                '',
                '[section]',
                '; this comment will be ignored',
                'heads = tails',
                'truth = lie',
                'nokia = 3310',
                '',
                '[misc]',
                '# this comment will be ignored too',
                'kill_all_humans = yes',
                'pi = 3.14159',
                '',
                '[юникод]',
                '文字 = 😉'
              ]
string_input = '\n'.join(list_input)
unicode_file = 'tests/fixtures/test.ini'
koi8r_file = 'tests/fixtures/koi8-r.ini'


@pytest.fixture()
def config_list():
    return list_input


@pytest.fixture(params=[list_input, string_input, unicode_file])
def common_configs(request):
    return liteconfig.Config(request.param)


@pytest.fixture()
def simple_config():
    return liteconfig.Config(['property = value',
                              '[section]',
                              'first = 1',
                              '[partition]',
                              'second = 2'])


@pytest.fixture(params=[':', '='])
def delimiter_configs(request):
    return liteconfig.Config([f'property{request.param} is here'], delimiter=request.param)


@pytest.fixture()
def comment_markers():
    return liteconfig.Config(['-property: is here', '=property: is here'], comment_markers='-=')


@pytest.fixture(params=[True, False])
def parse_numbers(request):
    return liteconfig.Config(['rough_pi = 3', 'pi = 3.14'], parse_numbers=request.param)


@pytest.fixture(params=[True, False])
def parse_booleans(request):
    return liteconfig.Config(['a = yes', 'b = no', 'c = True',
                              'd = False', 'e = on', 'f = off'], parse_booleans=request.param)


@pytest.fixture(params=['koi8_r', 'cp1251'])
def encodings(request):
    return liteconfig.Config(koi8r_file, encoding=request.param)


@pytest.fixture(params=[True, False])
def exceptions(request):
    return liteconfig.Config(['stray = cats', '[section]', 'truth = lie'], exceptions=request.param)

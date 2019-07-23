import liteconfig
import pytest


@pytest.fixture
def list_fixture():
    return ['; you can have properties belonging to no section (i.e., in very simple sectionless configs)',
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


@pytest.fixture
def string_fixture():
    return '\n'.join(list_fixture())


@pytest.fixture
def unicode_file_fixture():
    return 'tests/fixtures/test.ini'


@pytest.fixture
def koi8r_file_fixture():
    return 'tests/fixtures/koi8-r.ini'


@pytest.fixture
def common_configs():
    return [liteconfig.Config(list_fixture()),
            liteconfig.Config(string_fixture()),
            liteconfig.Config(unicode_file_fixture())
            ]

#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Lightweight and configurable .ini config parser with dot notation property access.

Features:
    - dot notation (value = cfg.section.property);
    - customizable parsing options;
    - no dependencies inside, only plain Python;
    - can handle text files, multiline strings or lists as input data;
    - no singleton, you can use as much Config objects as you want;
    - multiple encodings support, including Unicode;
    - read/write config files.

Default parsing options and their meaning:
    - delimiter = '='
      Delimiter between property and value is "=".
    - comment_markers = '#;'
      Empty lines and lines beginning with "#" or ";" are ignored.
    - parse_numbers = True
      Will try to parse numeric values to int or float.
    - parse_booleans = True
      Will try to parse boolean values to bool.
    - boolean_true = ('yes', 'true', 'on')
      Case-insensitive tuple of string values, recognized as boolean "True".
    - boolean_false = ('no', 'false', 'off')
      Case-insensitive tuple of string values, recognized as boolean "False".
    - encoding = 'utf-8'
      Parser will try to read and write config files using this encoding.
    - exceptions = False
      If True, accessing nonexistent properties (or sections) of config will raise AttributeError.
      If False, nonexistent property will return None. Absent section will return special object Nothing,
      which can be tested against truth (and it will always return False). So you can use the construction like
      if cfg.section.property:
          # do something with cfg.section.property
      else:
          # handle nonexistence

Public methods of Config object:
    - __init__(input_data [, delimiter, comment_markers, parse_numbers, parse_booleans,
      boolean_true, boolean_false, encoding, exceptions]):
      Instantiates Config object and parses input_data. Depending on type of input_data,
      instance will parse it as list, as multiline string or will interpret string as path to
      config file and read it.
    - has_section(item):
      Return True or False depending on existence of config section.
    - has_property(item [, section]):
      Return True or False depending on existence of config property. Will search in all sections
      by default or in one concrete section if it is passed as second argument.
    - write(file):
      Export config to file with the same settings as when object was instantiated.

Error handling:
    - Attempt to load nonexistent config file will raise FileNotFoundError.
    - Also may raise PermissionError if process does not have sufficient privileges to read or write file.
    - If desired, access to nonexistent property (or section) will raise AttributeError.
    - If input_data is not list nor string nor path to config file, will raise ValueError.
    - Fail to decode input_data file will result in UnicodeError.

Example:

===BEGIN config.ini===
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
===END config.ini===

cfg = Config('config.ini')
print(cfg.property)                    # 'value'
print(cfg.section.heads)               # 'tails'
print(cfg.юникод.文字)                 # '😉'

print(cfg.section.nokia)               # 3310
print(type(cfg.section.nokia))         # int

print(cfg.misc.kill_all_humans)        # True
print(type(cfg.misc.kill_all_humans))  # bool

print(cfg.misc.pi)                     # 3.14159
print(type(cfg.misc.pi))               # float
print(cfg.nonexistent)                 # AttributeError exception or None
print(cfg.voidsection.nonexistent)     # AttributeError exception or Nothing (boolean False)
print(cfg.voidsection)                 # AttributeError exception or Nothing (boolean False)
"""


class Config(object):

    def __init__(self,
                 input_data,
                 delimiter='=',
                 comment_markers='#;',
                 hierarchy=None,
                 parse_numbers=True,
                 parse_booleans=True,
                 boolean_true=('yes', 'true', 'on'),
                 boolean_false=('no', 'false', 'off'),
                 encoding='utf-8',
                 exceptions=False
                 ):
        """
        Initializes Config instance.

        :param comment_markers: config line is ignored if it begins with one of these characters.
        :param delimiter: character delimiting property and value.
        :param hierarchy: (stub) .ini-file section hierarchy type.
        :param parse_numbers: if set, number-looking values will be parsed as float or integer, not strings.
        :param parse_booleans: if set, boolean-looking values will be parsed as real booleans, not strings.
        :param encoding: default is UTF-8 to manage unicode symbols in your config file

        :raise ValueError when input data is not list nor string nor path to config file
        """
        self.__comment_markers = comment_markers
        self.__delimiter = delimiter
        self.__hierarchy = hierarchy
        self.__parse_numbers = parse_numbers
        self.__parse_booleans = parse_booleans
        self.__boolean_true = boolean_true
        self.__boolean_false = boolean_false
        self.__encoding = encoding
        self.__exceptions = exceptions

        self.__sections = []
        self.__properties = []

        if isinstance(input_data, list):
            self._parse_list(input_data)
        elif isinstance(input_data, str):
            if '\n' in input_data:
                self._parse_string(input_data)
            else:
                self._parse_file(input_data)
        else:
            raise ValueError('Unsupported value. Expected path to file, multiline string or list of strings')

    def has_section(self, item):
        return True if item in self.__sections else False

    def has_property(self, item, section=None):
        if not section:
            return True if item in self.__properties else False
        if self.has_section(section):
            return True if item in self.__dict__[section] else False

    def write(self, file):
        """Export config to file with the same settings as it was read in."""
        export_list = self._export(self)
        export_lines = '\n'.join([x for x in export_list if not isinstance(x, list)])
        with open(file, 'w', encoding=self.__encoding) as f:
            f.writelines(export_lines)

    def _export(self, section, accumulator=[]):
        """Returns config representation as list of strings"""
        for key, value in section.__dict__.items():
            if isinstance(value, (str, int, bool, float)) and key[0] is not '_':
                accumulator.append(key + self.__delimiter + str(value))
            elif isinstance(value, ConfigSection):
                accumulator.append('[' + key + ']')
                accumulator.append(self._export(value, accumulator))
        return accumulator

    def _parse_file(self, config_file):
        """Used to initialize Config object data structures from file"""
        with open(config_file, 'r', encoding=self.__encoding) as f:
            config_lines = f.readlines()
            self._parse_list(config_lines)

    def _parse_string(self, config_string):
        config_lines = config_string.split('\n')
        self._parse_list(config_lines)

    def _parse_list(self, config_list):
        config_list = [x.strip() for x in config_list]
        config_list = [x for x in config_list if (len(x) > 2 and x[0] not in self.__comment_markers)]
        self.__dict__ = {**self.__dict__, **self._parser_factory()(config_list).__dict__}

    @staticmethod
    def _parse_numbers(value):
        """If string value can be represented as number,
        method will return it as int or float, else untouched."""
        try:
            conv_float = float(value)
            if conv_float - int(conv_float) == 0:
                value = int(conv_float)
            else:
                value = conv_float
        except ValueError:
            return value
        return value

    def _parse_booleans(self, value):
        """If string value can be interpreted as boolean,
        method will return it as True or as False, else untouched."""
        lowercase_value = value.lower()
        if lowercase_value in self.__boolean_true:
            return True
        elif lowercase_value in self.__boolean_false:
            return False
        return value

    def _parser_factory(self):
        """
        Factory for choosing correct parsing method for selected hierarchy style.
        :return parser method
        """
        if not self.__hierarchy:
            return self._default_parser
        else:
            raise NotImplementedError("Parsing hierarchical INI configs is not yet implemented")

    def _default_parser(self, lines, section_name=None):
        """
        Default parser: sections' structure is flat (no hierarchy).
        :param lines: list of lines of config file.
        :return ConfigSection object.
        """
        section = dict()
        is_section = lambda line: True if line.startswith('[') and line.endswith(']') else False

        while lines:
            line = lines.pop(0)

            if is_section(line):
                property_key = line[1:-1]
                self.__sections.append(property_key)
                section_content = []
                while lines and not is_section(lines[0]):  # rip section lines and feed them to separate parser
                    section_content.append(lines.pop(0))
                section[property_key] = self._default_parser(section_content, property_key)

            else:
                equator = line.find(self.__delimiter)  # chop key:value line
                property_key = line[:equator].strip()
                property_value = line[equator + 1:].strip()

                saved_pv = property_value
                if self.__parse_booleans:
                    property_value = self._parse_booleans(property_value)
                if saved_pv is property_value:
                    if self.__parse_numbers:
                        property_value = self._parse_numbers(property_value)

                section[property_key] = property_value
                self.__properties.append(property_key)
        return ConfigSection(self.__exceptions, section_name, section)

    def __getattr__(self, item):
        if not self.__exceptions:
            return Nothing()
        else:
            raise AttributeError(f'Config does not contain section "{item}"')


class Singleton(type):
    """
    Singleton pattern realization via metaclass
    https://stackoverflow.com/questions/6760685/creating-a-singleton-in-python
    """
    _instances = {}

    def __call__(cls):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__()
        return cls._instances[cls]


class Nothing(object, metaclass=Singleton):
    """
    A special class.
    If instance of Nothing is tested against truth, it always return False.
    If one is trying to access it's attribute, it will return itself.
    Eventually chain of attribute calls will end and object will return False.
    Have to create it because one cannot override __getattribute__ of NoneType.
    """
    def __bool__(self):
        return False

    def __getattr__(self, item):
        return self


class ConfigSection(object):
    """
    Data container object
    """
    def __init__(self, exceptions, section_name, argv):
        self.__exceptions = exceptions
        self.__name = section_name
        for key, value in argv.items():
            self.__dict__[key] = value

    def __iter__(self):
        yield from self.__dict__

    def __getattr__(self, item):
        if not self.__exceptions:
            return None
        else:
            raise AttributeError(f'Section "{self.__name}" does not contain property "{item}"')

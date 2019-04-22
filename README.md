# liteconfig

Easy, fast and lightweight config parser with dot notation property access.

### Features:
- dot notation: `value = cfg.section.property`;
- customizable parsing options;
- no dependencies inside, only plain Python;
- can handle text files, multiline strings or lists as input data;
- no singleton, you can use as much Config objects as you want;
- multiple encodings support, including Unicode;
- read/write config files.

### Default parsing options and their meaning:
- `delimiter = '='`  
delimiter between property and value is "=".
- `comment_markers = '#;'`  
empty lines and lines beginning with "#" or ";" are ignored.
- `parse_numbers = True`  
will try to parse numeric values to int or float.
- `parse_booleans = True`  
will try to parse boolean values to bool.
- `boolean_true = ('1', 'yes', 'true', 'on')`  
case-insensitive tuple of string values, recognized as boolean "True".
- `boolean_false = ('0', 'no', 'false', 'off')`  
case-insensitive tuple of string values, recognized as boolean "False".
- `encoding = 'utf-8'`  
parser will try to read and write config files using this encoding.

### Public methods of Config object:
- `__init__(input_data [, delimiter, comment_markers, parse_numbers, parse_booleans,
  boolean_true, boolean_false, encoding])`  
Instantiates Config object and parses input_data. Depending on type of input_data,
instance will parse it as list, as multiline string or will interpret string as path to
config file and read it.
- `has_section(item)`  
Return True or False depending on existence of config section.
- `has_property(item [, section])`  
Return True or False depending on existence of config property.
Will search in all sections by default or in one concrete section if it is passed
as second argument.
- `write(file)`  
Export config to file with the same settings as when object was instantiated.

### Error handling:
- Attempt to load nonexistent config file will raise `FileNotFoundError`.
- Also may raise `PermissionError` if process does not have sufficient privileges to read or write file.
- Access to nonexistent property (or section) will raise `AttributeError`.
- If `input_data` is not list nor string nor path to config file, will raise `ValueError`.
- Fail to decode `input_data` file will result in `UnicodeError`.

### Example:

```ini
===BEGIN config.ini===
; liteconfig support very simple sectionless configs too
property = value

[section]
; this comment will be ignored
heads=tails
truth = lie
nokia = 3310

[misc]
# this comment will be ignored too
kill_all_humans = yes
pi = 3.1459

[юникод]
文字 = 😉
===END config.ini===
```

Here we have: comments and empty lines, three sections and one "free" item.
Some sections are named using ASCII symbols and one is Unicode. Also notice
`heads=tails` key-value: it isn't necessary to have spaces before and after delimiter.
Property and values can also be Unicode: cyrillic, hieroglyphs and emoji are welcome,
thanks to Python3.  

Default behaviour is to try to represent all numbers as ints and floats, not strings.
The same goes to boolean values: notice how `yes` became `True` for `kill_all_humans`
property. 

```python
cfg = Config('config.ini')
print(cfg.property)                    # 'value'
print(cfg.section.heads)               # 'tails'
print(cfg.юникод.文字)                 # '😉'

print(cfg.section.nokia)               # 3310
print(type(cfg.section.nokia))         # int

print(cfg.misc.kill_all_humans)        # True
print(type(cfg.misc.kill_all_humans))  # bool

print(cfg.misc.pi)                     # 3.1459
print(type(cfg.misc.pi))               # float
print(cfg.nonexistent)                 # AttributeError exception
```

### TO-DO:
- Parsing various formats of hierarchical configs (with subsections).
- Add option to return None for nonexistent sections and properties instead of rising exception. 

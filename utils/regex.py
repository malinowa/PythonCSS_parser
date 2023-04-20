import re

class Regexes:
    Identifier = re.compile(r'^[:]?[a-zA-Z\*\#_\.][0-9a-zA-Z\*\#_\.]*$')
    ExpressionLabel = re.compile(r'^[a-z]+(?:[-]?[a-z])+$')
    UnitValue = re.compile(r'[0-9][.]?[0-9]+(?:px|rem|em|cm|mm|in|pt|pc|ch|vw|vh|vmin|vmax|%)')
    ColorHexValue = re.compile(r'^#[0-9a-fA-F]{3}$|^#[0-9a-fA-F]{6}$')
    UrlValue = re.compile(r'url\([\w|\?|\=]*\)')
    StringValue = re.compile(r'"[\w| *]*"')
    TextValue = re.compile(r'^[a-zA-Z]+$')
    NumberValue = re.compile(r'[1-9][0-9]*')
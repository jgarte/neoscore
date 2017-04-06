import re

from doc.utils import clean_whitespace


class AttributeDoc:
    """A Python attribute or property as far as docs are concerned."""

    def __init__(self, name, parent, docstring, is_property, is_read_only,
                 default_value, global_index):
        self.name = name
        self.parent = parent
        self.docstring = docstring
        self.parse_attribute
        self.is_property = is_property
        self.default_value = default_value
        self.global_index = global_index
        self.global_index.add(self)
        self.type_string = ''
        self.summary = ''
        self.details = ''
        self.parse_attribute()

    @property
    def url(self):
        if type(self.parent).__name__ == 'ClassDoc':
            return self.parent.url + '.' + self.name
        else:
            return self.parent.url + '#' + self.name

    def parse_attribute(self):
        if '\n\n' in self.docstring:
            first_line, self.details = self.docstring.split('\n\n', 1)
        else:
            first_line = self.docstring
            self.details = ''
        if ':' in first_line:
            self.type_string, self.summary = first_line.split(':', 1)
        else:
            self.type_string = ''
            self.summary = first_line

    def clean_whitespace(self):
        """Strip excessive whitespace but leave blank lines in tact."""
        self.type_string = clean_whitespace(self.type_string)
        self.summary = clean_whitespace(self.summary)
        self.details = clean_whitespace(self.details)

"""Predefined validators."""

import re
try:
    from functools import reduce
except ImportError:
    pass

from .error import ValidationError
from . import utils


class Min(object):

    """Validator for minimum value."""

    def __init__(self, minimum_value, exclusive=False):
        """Init.

        :param minimum_value: Minimum value for validator.
        :param bool exclusive: If `True`, then validated value must be strongly
            lower than given threshold.

        """
        self.minimum_value = minimum_value
        self.exclusive = exclusive

    def validate(self, value):
        """Validate value."""
        if self.exclusive:
            if value <= self.minimum_value:
                raise ValidationError(
                    "'{}' is lower or equal than minimum ('{}').".format(
                        value, self.minimum_value))
        else:
            if value < self.minimum_value:
                raise ValidationError(
                    "'{}' is lower than minimum ('{}').".format(
                        value, self.minimum_value))

    def modify_schema(self, field_schema):
        """Modify field schema."""
        field_schema['minimum'] = self.minimum_value
        if self.exclusive:
            field_schema['exclusiveMinimum'] = True


class Max(object):

    """Validator for maximum value."""

    def __init__(self, maximum_value, exclusive=False):
        """Init.

        :param maximum_value: Maximum value for validator.
        :param bool exclusive: If `True`, then validated value must be strongly
            bigger than given threshold.

        """
        self.maximum_value = maximum_value
        self.exclusive = exclusive

    def validate(self, value):
        """Validate value."""
        if self.exclusive:
            if value >= self.maximum_value:
                raise ValidationError(
                    "'{}' is bigger or equal than maximum ('{}').".format(
                        value, self.maximum_value))
        else:
            if value > self.maximum_value:
                raise ValidationError(
                    "'{}' is bigger than maximum ('{}').".format(
                        value, self.maximum_value))

    def modify_schema(self, field_schema):
        """Modify field schema."""
        field_schema['maximum'] = self.maximum_value
        if self.exclusive:
            field_schema['exclusiveMaximum'] = True


class Regex(object):

    """Validator for regular expressions."""

    ATTRIBUTES_TO_FLAGS = {
        'ignorecase': re.I,
        'multiline': re.M,
    }

    def __init__(self, pattern, **flags):
        """Init.

        Note, that if given pattern is ECMA regex, given flags will be
        **completely ignored** and taken from given regex.


        :param string pattern: Pattern of regex.
        :param dict flags: Allowed flags can be found in attribute
            `ATTRIBUTES_TO_FLAGS`. Invalid flags will be ignored.

        """
        flags = {
            key: value for key, value in flags.items()
            if key in self.ATTRIBUTES_TO_FLAGS}

        if utils.is_ecma_regex(pattern):
            result = utils.convert_ecma_regex_to_python(pattern)
            self.pattern = result.regex

            for key, _ in flags.items():
                flags.update(
                    {key: self.ATTRIBUTES_TO_FLAGS[key] in result.flags})
        else:
            self.pattern = pattern

        self.flags = [
            self.ATTRIBUTES_TO_FLAGS[key] for key, value
            in flags.items() if value]

    def validate(self, value):
        """Validate value."""
        flags = self._calculate_flags()

        try:
            result = re.search(self.pattern, value, flags)
        except TypeError as te:
            raise ValidationError(*te.args)

        if not result:
            raise ValidationError(
                'Value "{}" did not match pattern "{}".'.format(
                    value, self.pattern))

    def _calculate_flags(self):
        return reduce(lambda x, y: x | y, self.flags, 0)

    def modify_schema(self, field_schema):
        """Modify field schema."""
        field_schema['pattern'] = utils.convert_python_regex_to_ecma(
            self.pattern, self.flags)

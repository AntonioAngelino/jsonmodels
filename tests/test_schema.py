from jsonmodels import models, fields, validators
from jsonmodels.utilities import compare_schemas

from .utilities import get_fixture


def test_model1():

    class Person(models.Base):

        name = fields.StringField(required=True)
        surname = fields.StringField(required=True)
        age = fields.IntField()

    alan = Person()
    schema = alan.to_json_schema()

    pattern = get_fixture('schema1.json')
    assert compare_schemas(pattern, schema) is True


def test_model2():

    class Car(models.Base):

        brand = fields.StringField(required=True)
        registration = fields.StringField(required=True)

    class Toy(models.Base):

        name = fields.StringField(required=True)

    class Kid(models.Base):

        name = fields.StringField(required=True)
        surname = fields.StringField(required=True)
        age = fields.IntField()
        toys = fields.ListField(Toy)

    class Person(models.Base):

        name = fields.StringField(required=True)
        surname = fields.StringField(required=True)
        age = fields.IntField()
        kids = fields.ListField(Kid)
        car = fields.EmbeddedField(Car)

    chuck = Person()
    schema = chuck.to_json_schema()

    pattern = get_fixture('schema2.json')
    assert compare_schemas(pattern, schema) is True


def test_model3():

    class Viper(models.Base):

        brand = fields.StringField()
        capacity = fields.FloatField()

    class Lamborghini(models.Base):

        brand = fields.StringField()
        velocity = fields.FloatField()

    class PC(models.Base):

        name = fields.StringField()
        ports = fields.StringField()

    class Laptop(models.Base):

        name = fields.StringField()
        battery_voltage = fields.FloatField()

    class Tablet(models.Base):

        name = fields.StringField()
        os = fields.StringField()

    class Person(models.Base):

        name = fields.StringField(required=True)
        surname = fields.StringField(required=True)
        age = fields.IntField()
        car = fields.EmbeddedField([Viper, Lamborghini])
        computer = fields.ListField([PC, Laptop, Tablet])

    chuck = Person()
    schema = chuck.to_json_schema()

    pattern = get_fixture('schema3.json')
    assert compare_schemas(pattern, schema) is True


def test_model_with_constructors():

    class Car(models.Base):

        def __init__(self, some_value):
            pass

        brand = fields.StringField(required=True)
        registration = fields.StringField(required=True)

    class Toy(models.Base):

        def __init__(self, some_value):
            pass

        name = fields.StringField(required=True)

    class Kid(models.Base):

        def __init__(self, some_value):
            pass

        name = fields.StringField(required=True)
        surname = fields.StringField(required=True)
        age = fields.IntField()
        toys = fields.ListField(Toy)

    class Person(models.Base):

        def __init__(self, some_value):
            pass

        name = fields.StringField(required=True)
        surname = fields.StringField(required=True)
        age = fields.IntField()
        kids = fields.ListField(Kid)
        car = fields.EmbeddedField(Car)

    schema = Person.to_json_schema()

    pattern = get_fixture('schema2.json')
    assert compare_schemas(pattern, schema) is True


def test_datetime_fields():

    class Event(models.Base):

        time = fields.TimeField()
        date = fields.DateField()
        end = fields.DateTimeField()

    schema = Event.to_json_schema()

    pattern = get_fixture('schema4.json')
    assert compare_schemas(pattern, schema) is True


def test_bool_field():

    class Person(models.Base):

        has_childen = fields.BoolField()

    schema = Person.to_json_schema()

    pattern = get_fixture('schema5.json')
    assert compare_schemas(pattern, schema) is True


def test_validators_can_modify_schema():

    class ClassBasedValidator(object):

        def validate(self, value):
            raise RuntimeError()

        def modify_schema(self, field_schema):
            field_schema['some'] = 'unproper value'

    def function_validator(value):
        raise RuntimeError()

    class Person(models.Base):

        name = fields.StringField(validators=ClassBasedValidator())
        surname = fields.StringField(validators=function_validator)

    for person in [Person, Person()]:
        schema = person.to_json_schema()

        pattern = get_fixture('schema6.json')
        assert compare_schemas(pattern, schema) is True


def test_min_validator():

    class Person(models.Base):

        name = fields.StringField()
        surname = fields.StringField()
        age = fields.IntField(validators=validators.Min(18))

    schema = Person.to_json_schema()

    pattern = get_fixture('schema_min.json')
    assert compare_schemas(pattern, schema)


def test_min_validator_with_exclusive():

    class Person(models.Base):

        name = fields.StringField()
        surname = fields.StringField()
        age = fields.IntField(validators=validators.Min(18, True))

    schema = Person.to_json_schema()

    pattern = get_fixture('schema_min_exclusive.json')
    assert compare_schemas(pattern, schema)


def test_max_validator():

    class Person(models.Base):

        name = fields.StringField()
        surname = fields.StringField()
        age = fields.IntField(validators=validators.Max(18))

    schema = Person.to_json_schema()

    pattern = get_fixture('schema_max.json')
    assert compare_schemas(pattern, schema)


def test_max_validator_with_exclusive():

    class Person(models.Base):

        name = fields.StringField()
        surname = fields.StringField()
        age = fields.IntField(validators=validators.Max(18, True))

    schema = Person.to_json_schema()

    pattern = get_fixture('schema_max_exclusive.json')
    assert compare_schemas(pattern, schema)


def test_regex_validator():

    class Person(models.Base):

        name = fields.StringField(
            validators=validators.Regex('^some pattern$'))

    schema = Person.to_json_schema()

    pattern = get_fixture('schema_pattern.json')
    assert compare_schemas(pattern, schema)


def test_regex_validator_when_ecma_regex_given():

    class Person(models.Base):

        name = fields.StringField(
            validators=validators.Regex('/^some pattern$/'))

    schema = Person.to_json_schema()

    pattern = get_fixture('schema_pattern.json')
    assert compare_schemas(pattern, schema)


def test_regex_validator_with_flag():

    class Person(models.Base):

        name = fields.StringField(
            validators=validators.Regex(
                '^some pattern$', ignorecase=True))

    schema = Person.to_json_schema()

    pattern = get_fixture('schema_pattern_flag.json')
    assert compare_schemas(pattern, schema)


def test_length_validator_min():

    class Person(models.Base):

        name = fields.StringField(validators=validators.Length(5))
        surname = fields.StringField()
        age = fields.IntField()

    schema = Person.to_json_schema()

    pattern = get_fixture('schema_length_min.json')
    assert compare_schemas(pattern, schema)


def test_length_validator():

    class Person(models.Base):

        name = fields.StringField(validators=validators.Length(5, 20))
        surname = fields.StringField()
        age = fields.IntField()

    schema = Person.to_json_schema()

    pattern = get_fixture('schema_length.json')
    assert compare_schemas(pattern, schema)

=====
Usage
=====

To use JSON models in a project:

.. code-block:: python

    import jsonmodels

Creating models
---------------

To create models you need to create class that inherits from
:class:`jsonmodels.models.Base` (and *NOT* :class:`jsonmodels.models.PreBase`
to which although refers links in documentation) and have class attributes
which values inherits from :class:`jsonmodels.fields.BaseField` (so all other
fields classes from :mod:`jsonmodels.fields`).

.. code-block:: python

    class Cat(models.Base):

        name = fields.StringField(required=True)
        breed = fields.StringField()


    class Dog(models.Base):

        name = fields.StringField(required=True)
        age = fields.IntField()


    class Car(models.Base):

        registration_number = fields.StringField(required=True)
        engine_capacity = fields.FloatField()
        color = fields.StringField()


    class Person(models.Base):

        name = fields.StringField(required=True)
        surname = fields.StringField(required=True)
        car = fields.EmbeddedField(Car)
        pets = fields.ListField([Cat, Dog])

Usage
-----

After that you can use it as normal object. You can pass kwargs in constructor
or :meth:`jsonmodels.models.PreBase.populate` method.

.. code-block:: python

    >>> person = Person(name='Chuck')
    >>> person.name
    'Chuck'
    >>> person.surname
    None
    >>> person.populate(surname='Norris')
    >>> person.surname
    'Norris'
    >>> person.name
    'Chuck'

Validation
----------

You can specify which fields are *required*, if required value is absent during
:meth:`jsonmodels.models.PreBase.validate` the
:class:`jsonmodels.error.ValidationError` will be raised.

.. code-block:: python

    >>> bugs = Person(name='Bugs', surname='Bunny')
    >>> bugs.validate()

    >>> dafty = Person()
    >>> dafty.validate()
    *** ValidationError: Field "name" is required!

Custom validators
~~~~~~~~~~~~~~~~~

You can always specify your own validators. Custom validator can be object with
`validate` method (which takes precedence) or function (or callable object).

Validators can be passed through `validators` keyword, as a single validator,
or list of validators (so, as you may be expecting, you can't pass object that
extends `List`). Each validator **must** raise exception to indicate validation
didn't pass. Returning values like `False` won't have any effect.

.. code-block:: python

    >>> class RangeValidator(object):
    ...
    ...   def __init__(self, min, max):
    ...     # Some logic here.
    ...
    ...   def validate(self, value):
    ...     # Some logic here.

    >>> def some_validator(value):
    ...   # Some logic here.

    >>> class Person(models.Base):
    ...
    ...   name = fields.StringField(required=True, validators=some_validator)
    ...   surname = fields.StringField(required=True)
    ...   age = fields.IntField(
    ...     Car, validators=[some_validator, RangeValidator(0, 100)])

Casting to Python struct (and JSON)
-----------------------------------

Instance of model can be easy casted to Python struct (and thanks to that,
later to JSON). See :meth:`jsonmodels.models.PreBase.to_struct`.

.. code-block:: python

    >>> cat = Cat(name='Garfield')
    >>> dog = Dog(name='Dogmeat', age=9)
    >>> car = Car(registration_number='ASDF 777', color='red')
    >>> person = Person(name='Johny', surname='Bravo', pets=[cat, dog])
    >>> person.car = car
    >>> person.to_struct()
    # (...)

Having Python struct it is easy to cast it to JSON.

.. code-block:: python

    >>> import json
    >>> person_json = json.dumps(person.to_struct())

Creating JSON schema for your model
-----------------------------------

JSON schema, although it is far more friendly than XML schema still have
something in common with its old friend: people don't like to write it and
(probably) they shouldn't do it or even read it. Thanks to `jsonmodels` it
is possible to you to operate just on models.

.. code-block:: python

    >>> person = Person()
    >>> schema = person.to_json_schema()

And thats it! You can serve then this schema through your api or use it for
validation incomming data.

.. ref-models:

Models
======

``Recommends`` uses these classes to represent similarities and recommendations.
These classes don't have be Django Models (ie: tied to a table in a database). All they have to do is implementing the properties descripted below.

.. class:: Similarity()

    A ``Similarity`` is an object with the following properties:

    .. attribute:: object

        The source object.

    .. attribute:: related_object

        The target object

    .. attribute:: score

        How much the ``related_object`` is similar to ``object``.

.. class:: Recommendation()

    A ``Recommendation`` is an object with the following properties:

    .. attribute:: object

        The object being suggested to the user.

    .. attribute:: user

        The user we are suggesting ``object`` to.

    .. attribute:: score

        How much the ``user`` is supposed to like ``object``.

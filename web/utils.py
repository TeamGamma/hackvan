# Taken from https://bitbucket.org/shadytrees/brownstone/
"""An example is in order. Say you have::

    user_table = Table(
        'user', meta.metadata,
        Column('id', Integer, primary_key=True),
        Column('name', sa.Unicode(100), unique=True))

and::

    class User(ReprMixin, InitMixin):
        __table__ = user_table

and::

    mapper(User, user_table)

Then ``User(name=u'Sassypants Johnston')`` does what you'd expect it
to do. And, furthermore::

    >>> User(name=u'Sassypants Johnston')
    User(id=[default value here], name=u'Sassypants Johnston')
    >>> repr(User(name=u'Sassypants Johnston'))
    "User(id=[default value here], name=u'Sassypants Johnston')"

Note that at no point did you have to use the declarative base
SQLAlchemy provides. Just some good ol'-fashioned introspection
magic."""

import sqlalchemy as sa

class ReprMixin(object):
    """Hooks into SQLAlchemy's magic to make :meth:`__repr__`s."""
    def __repr__(self):
        def reprs():
            for col in self.__table__.c:
                yield col.name, repr(getattr(self, col.name))

        def format(seq):
            for key, value in seq:
                yield '%s=%s' % (key, value)

        args = '(%s)' % ', '.join(format(reprs()))
        classy = type(self).__name__
        return classy + args

class InitMixin(object):
    def __init__(self, **kw):
        """For each keyword argument, finds the corresponding table
        column, sets it, and removes that argument. Goes up the
        inheritance hierarchy. Raises a :class:`AssertionError` if the
        list of arguments are not empty at the end, when it hits
        :class:`object`. This design is clever enough to take into
        account polymorphic inheritance *provided you do the right
        thing and inherit the mapped ORM classes as well*."""

        # A list of columns provided by SQLAlchemy's magic property.
        cols = set(col.name for col in self.__table__.c)

        # Dictionaries can't change during iteration.
        args = kw.copy()

        for k, v in kw.iteritems():
            setattr(self, k, v)

            # Variable set, now delete so the parent does not see.
            args.pop(k)

        # Python's complicated super() comes in handy at long last.
        parent = super(InitMixin, self)

        # I've reached the end of the line, so all the arguments
        # passed should be consume.
        if parent == object:
            assert len(args) == 0, args

        # Go up (or sideways! if you hate other programmers) the
        # inheritance hierarchy/diamond/globby thingy.
        else:
            parent.__init__(**args)

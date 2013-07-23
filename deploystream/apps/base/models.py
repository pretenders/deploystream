from sqlalchemy.sql.expression import ClauseElement

from deploystream import db


class Base(object):

    @classmethod
    def create(cls, *args, **kwargs):
        "Create, commit and return an object"
        obj = cls(*args, **kwargs)
        # Insert the record in our database and commit it
        db.session.add(obj)
        db.session.commit()
        return obj

    @classmethod
    def get_or_create(cls, defaults=None, **kwargs):
        """
        Get an instance identified by kwargs or create one.

        Defaults are added to the filtering dict if an object is needed to be
        created.

        For now this commits the created object as part of the call.
        """
        instance = db.session.query(cls).filter_by(**kwargs).first()
        if instance:
            return instance, False
        else:
            params = dict(
                (k, v)
                for k, v in kwargs.iteritems()
                if not isinstance(v, ClauseElement)
            )
            params.update(defaults)
            instance = cls(**params)
            db.session.add(instance)
            db.session.commit()
            return instance, True

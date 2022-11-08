from functools import reduce

from sqlalchemy import or_

from src.core.database import db


class Search(object):
    search_fields = list()

    @classmethod
    def get_clauses(cls, search_term):
        clauses = []
        if not search_term or not cls.search_fields:
            return None
        for search_field in cls.search_fields:
            clauses.append(search_field.cast(db.Unicode()).ilike(f"%{search_term}%"))
        return reduce(or_, clauses)

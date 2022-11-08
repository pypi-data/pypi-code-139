from sqlalchemy import Column
from sqlalchemy.sql.elements import ColumnClause

from src.microservice.core.database import db


class Ordering(object):
    id = db.column("id")

    actions = {
        "+": db.asc,
        "-": db.desc,
    }

    def __init__(self):
        self.fields = dict()
        for key, val in self.__class__.__dict__.items():
            if isinstance(val, (ColumnClause, Column)):
                self.fields[key] = val

    def order_by(self, *args):
        ordering_fields = []
        for value in args:
            ordering_field = self._prepare_ordered_field(value)
            if ordering_field is not None:
                ordering_fields.append(ordering_field)
        return ordering_fields

    def _prepare_ordered_field(self, value: str):
        if not value:
            return None
        sign, field = value[0], value[1:]
        if sign != "-":
            field = value
            sign = "+"

        if field not in self.fields:
            return None

        return self.actions[sign](self.fields[field])

import sqlalchemy as sql

from mipdb.database import DataBase
from mipdb.exceptions import UserInputError


class Schema:
    name: str
    schema: sql.MetaData

    def __init__(self, name) -> None:
        self.name = name
        self._is_schema_name_valid_python_identifier()
        self.schema = sql.MetaData(schema=self.name)

    def __repr__(self) -> str:
        return f"Schema(name={self.name})"

    def create(self, db: DataBase):
        db.create_schema(self.name)

    def drop(self, db: DataBase):
        db.drop_schema(self.name)

    def _is_schema_name_valid_python_identifier(self):
        if '"' in self.name:
            raise UserInputError(f'Data model\'s name: {self.name} is not a valid python identifier')

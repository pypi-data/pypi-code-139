"""
Crude is a descriptive ORM that allows you to access your entire database
programmatically with just a few lines, without having to define any schemas
or write any SQL commands.

Visit https://krude.net for more information.

Copyright (c) 2022 Kristoffer A. Wright
License: MIT (Please see LICENSE for the full license text)
"""

################################################################################
# Module metadata ##############################################################
################################################################################

__author__ = "Kristoffer A. Wright"
__version__ = "1.0.2"
__license__ = "MIT"

################################################################################
# Imports ######################################################################
################################################################################

import sqlite3
from typing import Any 

################################################################################
# Exceptions ###################################################################
################################################################################

class CrudeError(Exception):
    """Base class for all other custom exceptions used by Crude."""
    pass

class ConnectionFailure(CrudeError):
    """An attempt to connect to a database has failed."""
    pass

class AccessViolation(CrudeError):
    """An attempt to access a restricted property was made."""
    pass

class SchemaViolation(CrudeError):
    """An operation failed due to an invalid database schema."""
    pass

class OperationFailure(CrudeError):
    """An attempt to perform a SQL operation failed."""
    pass

class InvalidArgument(CrudeError):
    """An invalid method argument was given."""
    pass

class MissingMandatoryArgument(CrudeError):
    """A mandatory method argument is missing."""
    pass

class MissingResource(CrudeError):
    """The requested resource could not be found."""
    pass

################################################################################
# Metaclasses and Templates ####################################################
################################################################################

class TableTemplate:
    """
    Base class for all classes returned by `TableMetaclass.build_table_class`
    """
    pass

class TableMetaclass:
    """
    This is a factory class which is used to dynamically create classes for
    tables on this database. These classes can be used to instantiate single
    database records, where each of these record objects have common CRUD
    operations defined on them.
    """

    _database_path: str

    def __init__(self,
            database_path: str):

        self._database_path = database_path

    def build_table_class(self, 
            table_name: str) -> TableTemplate:
        """Build a new table class from the table with the given name."""

        database_path = self._database_path

        # Query the database for the column data:
        column_data_query_command = "PRAGMA table_info('{}');".format(
            table_name)
        try:
            connection = sqlite3.connect(self._database_path)
        except Exception:
            raise ConnectionFailure("Could not connect to the database.")

        try:
            cursor = connection.cursor()
            cursor.execute(column_data_query_command)
            rows = cursor.fetchall()
            connection.close()
        except Exception as err:
            raise OperationFailure("An error occurred while fetching table "
                + "data: {}".format(str(err)))

        # Reject missing tables:
        if len(rows) == 0:
            raise SchemaViolation("The requested table was not found.")

        # Create the class name, and the class itself:
        table_class_name = "{}Table".format(table_name.lower().capitalize())
        TableClass = type(table_class_name, (TableTemplate,), {})

        # Add the table name to the new class as a read-only property:
        TableClass._table_name = table_name

        def table_name_getter(self) -> str:
            return self._table_name

        def table_name_setter(self,
                value: str) -> None:
            raise AccessViolation("This is a read-only property")

        def table_name_deleter(self) -> None:
            raise AccessViolation("This property may not be deleted")

        TableClass.table_name = property(
            table_name_getter,
            table_name_setter,
            table_name_deleter,
            "The name of the database table this class corresponds with.")

        # Add the database path to the new class as a read-only property:
        TableClass._database_path = self._database_path

        def database_path_getter(self) -> str:
            return self._database_path

        def database_path_setter(self,
                value: str) -> None:
            raise AccessViolation("This is a read-only property")

        def database_path_deleter(self) -> None:
            raise AccessViolation("This property may not be deleted")

        TableClass.database_path = property(
            database_path_getter,
            database_path_setter,
            database_path_deleter,
            "The path to the database file.")

        # We need to make multiple passes over the column data. First, we need
        # to determine which columns comprise the primary key. Then we need
        # to pass over again in order to build the properties for each:
        primary_key_columns = []
        columns = []
        for row in rows:

            # Remember all column names, in addition to primary keys 
            # specifically, so that we know which arguments are legal to give 
            # for this class' `create` factory method.
            columns.append(str(row[1]))

            # If the column is a primary key...
            if int(row[5]) != 0:

                # Remember the column name, but also make sure to add the
                # column to the class as an uninitialized private attribute:
                primary_key_columns.append(str(row[1]))
                setattr(TableClass, "_{}".format(str(row[1])), None)

                # Add a property for the private attr:
                primary_key_property_methods = {}
                primary_key_getter_code = """
def _{column}_getter(self) -> Any:
    return self._{column}
primary_key_property_methods['getter'] = _{column}_getter
                """.format(column = str(row[1]))

                primary_key_setter_code = """
def _{column}_setter(self, value: Any) -> None:
    raise AccessViolation("This is a read-only property.")
primary_key_property_methods['setter'] = _{column}_setter
                """.format(column = str(row[1]))

                primary_key_deleter_code = """
def _{column}_deleter(self) -> None:
    raise AccessViolation("This property cannot be deleted.")
primary_key_property_methods['deleter'] = _{column}_deleter
                """.format(column = str(row[1]))

                exec(primary_key_getter_code)
                exec(primary_key_setter_code)
                exec(primary_key_deleter_code)

                setattr(TableClass, str(row[1]), property(
                    primary_key_property_methods['getter'],
                    primary_key_property_methods['setter'],
                    primary_key_property_methods['deleter'],
                    "The property for the primary key column {}"
                        .format(str(row[1]))
                ))


        # If no personal key columns were identified, use the 'rowid':
        if len(primary_key_columns) == 0:

            primary_key_columns.append("rowid")
            TableClass._rowid = None

            def row_id_getter(self) -> int:
                return self._rowid

            def row_id_setter(self, value: Any) -> None:
                raise AccessViolation("This is a read-only property.")

            def row_id_deleter(self) -> None:
                raise AccessViolation("This property may not be deleted.")

            TableClass.rowid = property(row_id_getter, row_id_setter, 
                row_id_deleter, "Property for the primary key column rowid")

        TableClass._primary_key_columns = primary_key_columns
        TableClass._columns = columns


        # Now that we have the primary keys, we can build the properties:
        for row in rows:

            # Ignore the personal key columns--we already processed them:
            if int(row[5]) != 0:
                continue

            # Define code that will be run with exec to define the property
            # methods. We do it this way so that we can dynamically assign the
            # method name, which is necessary since funcs are immutable:
            property_methods = {}
            getter_code = """
            
def _{column}_getter(self) -> Any:

    getter_sql_command = "SELECT {{}} FROM {{}} WHERE ".format(
        '{column}', self._table_name)
    getter_sql_arguments = []

    # Add the where clause:
    for primary_key_column in self._primary_key_columns:
        getter_sql_command += "{{}} = ? AND ".format(
            primary_key_column)
        getter_sql_arguments.append(getattr(self, 
            "_{{}}".format(primary_key_column)))
    
    # Remove the trailing AND:
    getter_sql_command = "{{}};".format(getter_sql_command[:-4])

    try:
        connection = sqlite3.connect(self._database_path)
    except Exception:
        raise ConnectionFailure("Could not connect to the database")

    try:
        cursor = connection.cursor()
        cursor.execute(getter_sql_command, getter_sql_arguments)
        rows = cursor.fetchall()
        return_data = rows[0][0]
        connection.close()
    except Exception as err:
        raise OperationFailure("An error occurred while attempting "
            + "to query the database: {{}}".format(str(err)))

    return return_data
property_methods['getter'] = _{column}_getter
            
            """.format(column = str(row[1]))

            setter_code = """
def _{column}_setter(self, value: Any) -> None:

    setter_sql_command = "UPDATE {{}} SET {{}} = ? WHERE ".format(
        self._table_name, '{column}')
    setter_sql_arguments = [value]

    # Add the where clause:
    for primary_key_column in self._primary_key_columns:
        setter_sql_command += "{{}} = ? AND ".format(
            primary_key_column)
        setter_sql_arguments.append(getattr(self, 
            "_{{}}".format(primary_key_column)))

    # Remove the trailing AND:
    setter_sql_command = "{{}};".format(setter_sql_command[:-4])

    try:
        connection = sqlite3.connect(self._database_path)
    except Exception:
        raise ConnectionFailure("Could not connect to the database")

    try:
        cursor = connection.cursor()
        cursor.execute(setter_sql_command, setter_sql_arguments)
        connection.commit()
        connection.close()
    except Exception as err:
        raise OperationFailure("An error occurred while attempting "
            + "to query the database: {{}}".format(str(err)))
property_methods['setter'] = _{column}_setter
            """.format(column = str(row[1]))

            deleter_code = """
def _{column}_deleter(self) -> None:
    raise AccessViolation("This property may not be deleted")
property_methods['deleter'] = _{column}_deleter
            """.format(column = str(row[1]))

            exec(getter_code)
            exec(setter_code)
            exec(deleter_code)

            setattr(TableClass, str(row[1]), property(
                property_methods['getter'], 
                property_methods['setter'], 
                property_methods['deleter'], 
                "Property for the {} column".format(str(row[1]))))
            
        # Add a constructor:
        def _constructor(self, **kwargs):

            # Ensure manditory args are present:
            for primary_key_column in primary_key_columns:
                if primary_key_column not in kwargs:
                    raise MissingMandatoryArgument("Missing required "
                     + "argument {}".format(primary_key_column))
            
            # Ensure no unexpected args were given:
            for kwarg in kwargs:
                if kwarg not in primary_key_columns:
                    raise InvalidArgument("Unknown argument given: {}".format(
                        kwarg))

                # Initialize the primary key attribute:
                setattr(self, "_{}".format(kwarg), kwargs[kwarg])

        TableClass.__init__ = _constructor

        # Add a factory method for loading existing records. This is basically
        # just a thin wrapper around the constructor that checks to make sure
        # the record exists in the first place:
        @classmethod
        def _load(cls, **kwargs):

            if len(kwargs) == 0:
                raise MissingMandatoryArgument("Must specify at least one "
                    + "primary key.")

            # Ensure manditory args are present:
            for primary_key_column in primary_key_columns:
                if primary_key_column not in kwargs:
                    raise MissingMandatoryArgument("Missing required "
                     + "argument {}".format(primary_key_column))
            
            # Ensure no unexpected args were given:
            for kwarg in kwargs:
                if kwarg not in primary_key_columns:
                    raise InvalidArgument("Unknown argument given: {}".format(
                        kwarg))

            # Build a sql query to fetch the requested record:
            sql_command = "SELECT * FROM {} WHERE ".format(table_name)
            sql_arguments = []
            for kwarg in kwargs:
                sql_command += "{} = ? AND ".format(kwarg)
                sql_arguments.append(kwargs[kwarg])
            sql_command = "{};".format(sql_command[:-4])

            try:
                connection = sqlite3.connect(database_path)
            except Exception:
                raise ConnectionFailure("Could not connect to the database")

            try:
                cursor = connection.cursor()
                cursor.execute(sql_command, sql_arguments)
                rows = cursor.fetchall()
                connection.close()
            except Exception as err:
                raise OperationFailure("An error occurred while attempting "
                    + "to query the database: {{}}".format(str(err)))

            if len(rows) == 0:
                raise MissingResource("The given record does not exist.")

            return cls(**kwargs)

        TableClass.load = _load

        # Add a factory method for deleting records:
        @classmethod
        def _delete(cls, **kwargs) -> None:

            if len(kwargs) == 0:
                raise MissingMandatoryArgument("Must specify at least one "
                    + "primary key.")

            # Ensure manditory args are present:
            for primary_key_column in primary_key_columns:
                if primary_key_column not in kwargs:
                    raise MissingMandatoryArgument("Missing required "
                     + "argument {}".format(primary_key_column))
            
            # Ensure no unexpected args were given:
            for kwarg in kwargs:
                if kwarg not in primary_key_columns:
                    raise InvalidArgument("Unknown argument given: {}".format(
                        kwarg))

            # Build a sql query to fetch the requested record:
            sql_command = "DELETE FROM {} WHERE ".format(table_name)
            sql_arguments = []
            for kwarg in kwargs:
                sql_command += "{} = ? AND ".format(kwarg)
                sql_arguments.append(kwargs[kwarg])
            sql_command = "{};".format(sql_command[:-4])

            try:
                connection = sqlite3.connect(database_path)
            except Exception:
                raise ConnectionFailure("Could not connect to the database")

            try:
                cursor = connection.cursor()
                cursor.execute(sql_command, sql_arguments)
                deleted = cursor.rowcount > 0
                connection.commit()
                connection.close()
            except Exception as err:
                raise OperationFailure("An error occurred while attempting "
                    + "to query the database: {{}}".format(str(err)))

            if not deleted:
                raise MissingResource("The given record does not exist.")

        TableClass.delete = _delete

        # Add a factory method for creating new records:
        @classmethod
        def _create(cls, **kwargs):

            # Ensure no unexpected args were given:
            for kwarg in kwargs:
                if kwarg not in columns:
                    raise InvalidArgument("Unknown argument given: {}".format(
                        kwarg))

            # Form the sql command and arguments for the insert:
            insert_sql_command = "INSERT INTO {} ".format(table_name)
            insert_sql_arguments = []

            if len(kwargs) == 0:
                insert_sql_command += "DEFAULT VALUES;"
            else:
                insert_sql_command += "("
                for kwarg in kwargs:
                    insert_sql_command += "{},".format(kwarg)
                    insert_sql_arguments.append(kwargs[kwarg])
                insert_sql_command = "{}) VALUES ({});".format(
                    insert_sql_command[:-1], 
                    ",".join(["?"]*len(insert_sql_arguments)))

            # Form the sql command for selecting the primary
            # keys of the new record:

            select_sql_command = "SELECT {} FROM {} WHERE rowid = ?;".format(
                ",".join(primary_key_columns), table_name)
            

            try:
                connection = sqlite3.connect(database_path)
            except Exception:
                raise ConnectionFailure("Could not connect to the database")

            try:
                cursor = connection.cursor()

                # Perform Insert:
                cursor.execute(insert_sql_command, insert_sql_arguments)
                new_row_id = cursor.lastrowid
                connection.commit()

                # Fetch the primary keys:
                cursor.execute(select_sql_command, [new_row_id])
                rows = cursor.fetchall()
                connection.close()
            except Exception as err:
                raise OperationFailure("An error occurred while attempting "
                    + "to perform a database operation: {}".format(str(err)))
            
            # Form the signature to call the constructor with:
            constructor_args = {}
            for i in range(len(primary_key_columns)):
                constructor_args[primary_key_columns[i]] = rows[0][i]

            return cls(**constructor_args)

        TableClass.create = _create
        
        return TableClass

################################################################################
# Factories ####################################################################
################################################################################

def connect(path: str) -> TableMetaclass:

    # Attempt to open the database to make sure the given path is valid:
    try:
        connection = sqlite3.connect(path)
    except Exception:
        raise ConnectionFailure("Could not connect to the database.")

    connection.close()
    return TableMetaclass(path)
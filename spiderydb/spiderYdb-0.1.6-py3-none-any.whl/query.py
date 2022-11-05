class Query:
    def __init__(self, table, args, kwargs):
        self.args = args
        self.table = table
        self.database = table._database_

    def select(self):
        objects = self[:]
        return [self.table.from_dict(item) for item in objects]

    def delete(self):
        declare = []
        where = []
        params = {}
        for _ in self.args:
            t, field, value = _
            name, title = f"{field.name}", field.title
            declare.append(f"DECLARE ${name} AS {title};")
            params[f'${name}'] = value
            where.append(f'{name} {t} ${name}')
        sql = f'DELETE from {self.table.table_name}'
        if declare:
            sql = '\n'.join(declare) + '\n' + sql
        if where:
            sql = sql + '\nWHERE ' + ' AND '.join(where)
        # print(sql)
        return self.database.query(sql, params)

    def get(self):
        objects = self[:2]
        if not objects:
            return None
        if len(objects) > 1:
            raise (Exception, 'Multiple objects were found. Use select(...) to retrieve them')
        return self.table.from_dict(objects[0])

    def _fetch(self, limit=None, offset=None, lazy=False):
        return QueryResult(self, limit, offset, lazy=lazy)

    def _actual_fetch(self, limit, offset):
        declare = []
        where = []
        params = {}
        for _ in self.args:
            t, field, value = _
            name, title = f"{field.name}", field.title
            declare.append(f"DECLARE ${name} AS {title};")
            params[f'${name}'] = value
            where.append(f'{name} {t} ${name}')
        sql = f'SELECT * from {self.table.table_name}'
        if declare:
            sql = '\n'.join(declare) + '\n' + sql
        if where:
            sql = sql + '\nWHERE ' + ' AND '.join(where)
        # print(sql)
        return self.database.query(sql, params)

    def __iter__(self):
        return iter(self._fetch(lazy=True))

    def __getitem__(self, key):
        if not isinstance(key, slice):
            raise (TypeError, 'If you want apply index to a query, convert it to list first')

        step = key.step
        if step is not None and step != 1:
            raise(TypeError, "Parameter 'step' of slice object is not allowed here")
        start = key.start
        if start is None:
            start = 0
        elif start < 0:
            raise (TypeError, "Parameter 'start' of slice object cannot be negative")
        stop = key.stop
        if stop is None:
            if not start:
                return self._fetch()
            else:
                return self._fetch(limit=None, offset=start)
        if start >= stop:
            return self._fetch(limit=0)
        return self._fetch(limit=stop-start, offset=start)

    @classmethod
    def save_item(cls, item):
        if not item.need_update:
            return False
        declare = []
        params = {}
        added = []
        for field in item.params:
            field = item.params[field]
            if field.need_update:
                field.changed = False
                added.append(field.name)
                params[f'${field.name}'] = field.to_save
                declare.append(f"DECLARE ${field.name} AS {field.title};")

        sql = f'''UPSERT INTO {item.table_name}
        ({', '.join([f'`{field}`' for field in added])})
        VALUES ({', '.join([f'${field}' for field in added])})'''
        if declare:
            sql = '\n'.join(declare) + '\n' + sql
        item._database_.query(sql, params)
        return True


class QueryResult:
    def __init__(self, query, limit, offset, lazy):
        self._query = query
        self._limit = limit
        self._offset = offset
        self._items = None if lazy else self._query._actual_fetch(limit, offset)

    def __len__(self):
        if self._items is None:
            self._items = self._query._actual_fetch(self._limit, self._offset)
        return len(self._items)

    def __getitem__(self, item):
        return self._items[item]
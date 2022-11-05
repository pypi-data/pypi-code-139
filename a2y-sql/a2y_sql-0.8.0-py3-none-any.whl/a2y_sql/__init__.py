# -*- coding: utf-8 -*-

import mysql.connector as _connector
from threading import Lock as _Lock


class CNXPool:
	def __init__(self, **dbconfig):
		self.__dbconfig = dbconfig
		self.__pool = []
		self.__lock = _Lock()

	def Get(self):
		with self.__lock:
			if len(self.__pool) == 0:
				connection = _connector.connect(**self.__dbconfig)
			else:
				connection = self.__pool.pop()
				if not connection.is_connected():
					connection.close()
					connection = _connector.connect(**self.__dbconfig)
			return connection

	def Put(self, connection):
		with self.__lock:
			if len(self.__pool) > 2:
				connection.close()
			else:
				self.__pool.append(connection)


class CNXGuard:
	# 默认情况下使用的 CNXPool。
	# 如果应用程序只使用一个数据库，那么在程序初始化时，
	# 把 POOL 属性设置为一个 CNXPool 对象会带来一些便利：
	# 构建 CNXGuard 对象时可以省略 pool 参数。
	# 见 __init__ 方法的实现。
	POOL = None

	def __init__(self, cnx=None, pool=None):
		if pool is None:
			pool = CNXGuard.POOL
		self.__pool = pool
		self.__need_put = (cnx is None)
		self.__cnx = cnx

	def __enter__(self):
		if self.__need_put:
			self.__cnx = self.__pool.Get()

		return self.__cnx

	def __exit__(self, exception_type, exception_value, exception_traceback):
		if self.__need_put:
			if self.__cnx.in_transaction:
				if exception_type is None:
					self.__cnx.commit()
				else:
					self.__cnx.rollback()
			self.__pool.Put(self.__cnx)

	@staticmethod
	def Select(id, table, _class, cnx=None, pool=None):
		with CNXGuard(cnx, pool) as cnx:
			cursor = cnx.cursor()
			cursor.execute('SELECT * FROM `%s` WHERE id = %d' % (table, id))
			for columns in cursor:
				return _class(*columns)
		raise KeyError('Table %s has no row with id = %d' % (table, id))

	@staticmethod
	def SelectForeignAttr(foreign_id, foreign_column, foreign_table, _class=None, cnx=None, pool=None):
		"""We don't implement this method, since it's not a good idea to cache multi foreign attribute table."""
		pass

	@staticmethod
	def Insert(table, column_names, column_values, cnx=None, pool=None):
		colno = len(column_names)
		if colno < 1:
			raise ValueError('Column count must be greater than 0 when inserting something into a table')

		if isinstance(column_values, dict):
			values = []
			for column_name in column_names:
				values.append(column_values[column_name])
		else:
			if colno != len(column_values):
				raise ValueError('argument column_names and column_values do not match in length.')
			values = column_values

		if colno == 1:
			query = 'INSERT INTO `%s` VALUES (%%s)' % table
		else:
			query = 'INSERT INTO `%s` VALUES (%%s%s)' % (table, ', %s' * (colno-1))

		with CNXGuard(cnx, pool) as cnx:
			cursor = cnx.cursor()
			cursor.execute(query, values)
			return cursor.lastrowid

	@staticmethod
	def Delete(id, table, cnx=None, pool=None):
		query = 'DELETE FROM `%s` WHERE id = %%s' % table
		with CNXGuard(cnx, pool) as cnx:
			cursor = cnx.cursor()
			cursor.execute(query, (id,))

	@staticmethod
	def AlterAutoIncrement(table, value=1, cnx=None, pool=None):
		query = 'ALTER TABLE `%s` AUTO_INCREMENT = %d' % (table, value)
		with CNXGuard(cnx, pool) as cnx:
			cursor = cnx.cursor()
			cursor.execute(query)

	@staticmethod
	def ClearTable(tables, cnx=None, pool=None):
		if isinstance(tables, str):
			tables = [tables]
		with CNXGuard(cnx, pool) as cnx:
			cursor = cnx.cursor()
			for table in tables:
				query = 'DELETE FROM `%s`' % table
				cursor.execute(query)


class Cache:
	def __init__(self, pool=None):
		self.__obj_dict = {}
		self.__class_dict = {}
		self.__pool = pool

	def __get_pool(self, pool):
		return pool if pool else self.__pool

	def SetPool(self, pool):
		self.__pool = pool

	def Select(self, id, table, _class=None, cnx=None, pool=None):
		cache = self.__obj_dict.setdefault(table, {})
		if id in cache:
			return cache[id]
		else:
			if _class is None:
				if table in self.__class_dict:
					_class = self.__class_dict[table]
				else:
					raise ValueError('We need a valid class object (argument 3) to construct row object.')
			elif table not in self.__class_dict:
				self.__class_dict[table] = _class

			obj = CNXGuard.Select(id, table, _class, cnx, self.__get_pool(pool))
			cache[id] = obj
			return obj

	def Delete(self, obj, table=None, cnx=None, pool=None):
		id = obj if isinstance(obj, int) else obj['id']
		if table is None:
			table = obj.TABLE_NAME
		CNXGuard.Delete(id, table, cnx, self.__get_pool(pool))
		if table in self.__obj_dict:
			table_cache = self.__obj_dict[table]
			if id in table_cache:
				table_cache.pop(id)

	def Insert(self, obj, table=None, cnx=None, pool=None):
		id = obj['id']
		if table is None:
			table = obj.TABLE_NAME
		cache = self.__obj_dict.setdefault(table, {})
		cache[id] = obj

	def CachedTable(self, table):
		return self.__obj_dict[table]

	def ClearTable(self, table):
		CNXGuard.ClearTable(table)
		self.__obj_dict.pop(table)

	def Cache(self, table, _class=None, cnx=None, pool=None):
		cache = self.__obj_dict.setdefault(table, {})
		if _class is None:
			if table in self.__class_dict:
				_class = self.__class_dict[table]
			else:
				raise ValueError('We need a valid class object (argument 3) to construct row object.')
		elif table not in self.__class_dict:
			self.__class_dict[table] = _class

		with CNXGuard(cnx, self.__get_pool(pool)) as cnx:
			cursor = cnx.cursor()
			cursor.execute('SELECT * FROM `%s`' % table)
			for columns in cursor:
				obj = _class(*columns)
				cache[columns[0]] = obj

		return cache

	def Refresh(self, table, clear=True, cnx=None, pool=None):
		if table not in self.__class_dict:
			raise KeyError('Table %s has not been cached yet.' % table)
		_class = self.__class_dict[table]
		if clear:
			self.__obj_dict[table] = {}
		self.Cache(table, _class, cnx, pool)

	def Tables(self):
		return self.__class_dict.keys()

	def Update(self, table, cnx=None, pool=None):
		self.Refresh(table, False, cnx, pool)


class ColumnAttribute:
	def __init__(self, name, default=None, isForeignKey=False, foreignTableName=None, foreignClass=None):
		self.name = name
		self.default = default
		self.isForeignKey = isForeignKey
		if isForeignKey:
			self.foreignTableName = name if foreignTableName is None else foreignTableName
			self.foreignClass = foreignClass


class MultiForeignAttr:
	def __init__(self, attr_name, foreign_name, foreign_attr_table, _class):
		self.attr_name = attr_name
		self.foreign_name = foreign_name
		self.foreign_attr_table = foreign_attr_table
		self._class = _class


class TableBase:
	""" Every derived table must override TABLE_NAME and COLUMN_NAMES.
	If derived table has foreign key(s), it must override COLUMN_ATTRIBUTES for foreign key column(s).

	If derived table has multiple-foreign attribute, it *should* override MULTI_FOREIGN_ATTR.
	If you do use features this class provides, it *must*.
	"""
	TABLE_NAME = 'table_base'
	COLUMN_NAMES = []
	COLUMN_ATTRIBUTES = {}
	MULTI_FOREIGN_ATTR = {}

	CACHE = None
	POOL = None

	def __init__(self, *column_tuple, **column_dict):
		column_names = self.COLUMN_NAMES
		self.__column_values = dict(zip(column_names, column_tuple))
		for (key, value) in column_dict.items():
			if key in column_names:
				self.__column_values[key] = value
			else:
				setattr(self, key, value)

		for column in column_names:
			default = self.__get_default(column)
			self.__column_values.setdefault(column, default)

	def __is_foreign(self, name):
		return name in self.COLUMN_ATTRIBUTES and self.COLUMN_ATTRIBUTES[name].isForeignKey

	def __is_foreign_key(self, name):
		attributes = self.COLUMN_ATTRIBUTES
		if name in attributes:
			return attributes[name].isForeignKey
		return False

	def __get_default(self, name):
		attributes = self.COLUMN_ATTRIBUTES
		if name in attributes:
			return attributes[name].default
		multi = self.MULTI_FOREIGN_ATTR
		if name in multi:
			return {}
		return None

	def __get_pool(self, pool):
		return pool if pool else self.POOL

	def __getitem__(self, name):
		if hasattr(self, name):
			return getattr(self, name)
		if name not in self.COLUMN_NAMES:
			if name in self.MULTI_FOREIGN_ATTR:
				self.FillForeign(False)
				return getattr(self, name)
			else:
				raise AttributeError("%s instance has no attribute '%s'" % (self.__class__.__name__, name))
		else:
			column_value = self.__column_values[name]
			if self.__is_foreign_key(name) and isinstance(column_value, int):
				attribute = self.COLUMN_ATTRIBUTES[name]
				table = attribute.foreignTableName
				_class = attribute.foreignClass

				if self.CACHE is None:
					value = CNXGuard.Select(column_value, table, _class)
				else:
					value = self.CACHE.Select(column_value, table, _class)

				self.__column_values[name] = value
				return value
			else:
				return column_value

	def __setitem__(self, name, value):
		if name in self.COLUMN_NAMES:
			self.__column_values[name] = value
		else:
			setattr(self, name, value)

	def __get_foreigns(self):
		foreigns = []
		for (column, attr) in self.COLUMN_ATTRIBUTES.items():
			if attr.isForeignKey:
				foreigns.append(column)
		return foreigns

	def FillForeign(self, deep=True, cnx=None, pool=None):
		with CNXGuard(cnx, self.__get_pool(pool)) as cnx:
			foreigns = self.__get_foreigns()
			for foreign in foreigns:
				obj = self[foreign]
				if deep:
					obj.FillForeign(deep, cnx, pool)

			for (attr_name, foreign_attr) in self.MULTI_FOREIGN_ATTR.items():
				if hasattr(self, attr_name):
					foreign_attr_objs = getattr(self, attr_name)
				else:
					foreign_attr_objs = []
					foreign_col_name = foreign_attr.foreign_name
					table = foreign_attr.foreign_attr_table
					_class = foreign_attr._class

					query = 'SELECT * FROM `%s` WHERE `%s` = %d' % (table, foreign_col_name, self['id'])
					cursor = cnx.cursor()
					cursor.execute(query)
					for cols in cursor:
						obj = _class(*cols)
						foreign_attr_objs.append(obj)

					setattr(self, attr_name, foreign_attr_objs)

				if deep:
					for obj in foreign_attr_objs:
						obj.FillForeign(deep, cnx, pool)

	def Insert(self, cnx=None, pool=None):
		pool = self.__get_pool(pool)
		foreigns = self.__get_foreigns()
		with CNXGuard(cnx, pool) as cnx:
			foreign_ids = {}
			for foreign in foreigns:
				obj = self[foreign]
				id = obj['id']
				if id <= 0:
					id = obj.Insert(cnx, pool)
				foreign_ids[foreign] = id

			if self['id'] <= 0:
				if len(foreigns) > 0:
					cp = self.__column_values.copy()
					for foreign in foreigns:
						cp[foreign] = foreign_ids[foreign]
				else:
					cp = self.__column_values

				id = CNXGuard.Insert(self.TABLE_NAME, self.COLUMN_NAMES, cp, cnx)
				self['id'] = id

				if self.CACHE is not None:
					self.CACHE.Insert(self, self.TABLE_NAME, cnx)
			else:
				self.__delete_multi_foreign_attr(cnx)

			self.__insert_multi_foreign_attr(cnx)

			return id

	def __insert_multi_foreign_attr(self, cnx):
		for (attr_name, foreign_attr) in self.MULTI_FOREIGN_ATTR.items():
			if not hasattr(self, attr_name):
				continue
			foreign_name = foreign_attr.foreign_name
			attr = getattr(self, attr_name)
			for obj in attr:
				obj[foreign_name] = self
				obj.Insert(cnx)

	def __delete_multi_foreign_attr(self, cnx):
		cursor = cnx.cursor()
		id = self['id']
		foreign_attrs = self.MULTI_FOREIGN_ATTR
		for (key, foreign_attr) in foreign_attrs.items():
			query = 'DELETE FROM `%s` WHERE `%s` = %d' % (foreign_attr.foreign_attr_table, foreign_attr.foreign_name, id)
			cursor.execute(query)

	def Delete(self, cnx=None, pool=None):
		with CNXGuard(cnx, self.__get_pool(pool)) as cnx:
			# It's not needed to delete foreigns

			self.__delete_multi_foreign_attr(cnx)

			if self.CACHE is None:
				CNXGuard.Delete(self, self.TABLE_NAME, cnx)
			else:
				self.CACHE.Delete(self, self.TABLE_NAME, cnx)

	def __column_value_for_update(self, column_name):
		value = self[column_name]
		if self.__is_foreign_key(column_name):
			return value['id']
		return value

	def Update(self, update_multi_foreign=True, cnx=None, pool=None):
		content = ''
		values = []
		for col in self.COLUMN_NAMES[2:]:
			content += ', `%s` = %%s' % col
			values.append(self.__column_value_for_update(col))
		values.insert(0, self.__column_value_for_update(self.COLUMN_NAMES[1]))
		query = 'UPDATE `%s` SET `%s` = %%s%s WHERE id = %d' % (self.TABLE_NAME, self.COLUMN_NAMES[1], content, self['id'])
		with CNXGuard(cnx, self.__get_pool(pool)) as cnx:
			cursor = cnx.cursor()
			cursor.execute(query, values)

			if update_multi_foreign:
				self.__delete_multi_foreign_attr(cnx)
				for (attr_name, foreign_attr) in self.MULTI_FOREIGN_ATTR.items():
					if not hasattr(self, attr_name):
						continue
					foreign_name = foreign_attr.foreign_name
					attr = getattr(self, attr_name)
					for obj in attr:
						obj['id'] = 0
				self.__insert_multi_foreign_attr(cnx)


def GetTableNames(cnx=None, pool=None):
	with CNXGuard(cnx, pool) as cnx:
		tables = []
		cursor = cnx.cursor()
		cursor.execute('SHOW TABLES')
		for (table,) in cursor:
			tables.append(table)
		return tables


def GetCreateTableStatement(table, cnx=None, pool=None):
	query = u'SHOW CREATE TABLE `%s`' % table
	with CNXGuard(cnx, pool) as cnx:
		cursor = cnx.cursor()
		cursor.execute(query)
		statements = []
		for (name, statement) in cursor:
			words = statement.split()
			index = 0
			count = len(words)
			while index != count:
				if words[index].startswith(u'AUTO_INCREMENT='):
					break
				index += 1
			if index != count:
				words.pop(index)
			statement = u' '.join(words)
			statements.append(statement)
		return statements[0]


def Execute(statement, cnx=None, pool=None):
	first = statement.split()[0].lower()
	querys = ['select', 'show']
	is_query = (first in querys)
	is_insert = (first == 'insert')
	with CNXGuard(cnx, pool) as cnx:
		cursor = cnx.cursor()
		cursor.execute(statement)
		if is_query:
			result = []
			for r in cursor:
				result.append(r)

			return result
		elif is_insert:
			return cursor.lastrowid

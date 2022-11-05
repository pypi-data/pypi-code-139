# engine/url.py
# Copyright (C) 2005-2022 the SQLAlchemy authors and contributors
# <see AUTHORS file>
#
# This module is part of SQLAlchemy and is released under
# the MIT License: https://www.opensource.org/licenses/mit-license.php

"""Provides the :class:`~sqlalchemy.engine.url.URL` class which encapsulates
information about a database connection specification.

The URL object is created automatically when
:func:`~sqlalchemy.engine.create_engine` is called with a string
argument; alternatively, the URL is a public-facing construct which can
be used directly and is also accepted directly by ``create_engine()``.
"""

import re

from .interfaces import Dialect
from .. import exc
from .. import util
from ..dialects import plugins
from ..dialects import registry
from ..util import collections_abc
from ..util import compat


class URL(
    util.namedtuple(
        "URL",
        [
            "drivername",
            "username",
            "password",
            "host",
            "port",
            "database",
            "query",
        ],
    )
):
    """
    Represent the components of a URL used to connect to a database.

    This object is suitable to be passed directly to a
    :func:`_sa.create_engine` call. The fields of the URL are parsed from a
    string by the :func:`.make_url` function. The string format of the URL
    generally follows `RFC-1738 <https://www.ietf.org/rfc/rfc1738.txt>`_, with
    some exceptions.

    To create a new :class:`_engine.URL` object, use the
    :func:`_engine.url.make_url` function.  To construct a :class:`_engine.URL`
    programmatically, use the :meth:`_engine.URL.create` constructor.

    .. versionchanged:: 1.4

        The :class:`_engine.URL` object is now an immutable object.  To
        create a URL, use the :func:`_engine.make_url` or
        :meth:`_engine.URL.create` function / method.  To modify
        a :class:`_engine.URL`, use methods like
        :meth:`_engine.URL.set` and
        :meth:`_engine.URL.update_query_dict` to return a new
        :class:`_engine.URL` object with modifications.   See notes for this
        change at :ref:`change_5526`.

    :class:`_engine.URL` contains the following attributes:

    * :attr:`_engine.URL.drivername`: database backend and driver name, such as
      ``postgresql+psycopg2``
    * :attr:`_engine.URL.username`: username string
    * :attr:`_engine.URL.password`: password string
    * :attr:`_engine.URL.host`: string hostname
    * :attr:`_engine.URL.port`: integer port number
    * :attr:`_engine.URL.database`: string database name
    * :attr:`_engine.URL.query`: an immutable mapping representing the query
      string.  contains strings for keys and either strings or tuples of
      strings for values.


    """

    def __new__(self, *arg, **kw):
        if kw.pop("_new_ok", False):
            return super(URL, self).__new__(self, *arg, **kw)
        else:
            util.warn_deprecated(
                "Calling URL() directly is deprecated and will be disabled "
                "in a future release.  The public constructor for URL is "
                "now the URL.create() method.",
                "1.4",
            )
            return URL.create(*arg, **kw)

    @classmethod
    def create(
        cls,
        drivername,
        username=None,
        password=None,
        host=None,
        port=None,
        database=None,
        query=util.EMPTY_DICT,
    ):
        """Create a new :class:`_engine.URL` object.

        :param drivername: the name of the database backend. This name will
          correspond to a module in sqlalchemy/databases or a third party
          plug-in.
        :param username: The user name.
        :param password: database password.  Is typically a string, but may
          also be an object that can be stringified with ``str()``.

          .. note::  A password-producing object will be stringified only
             **once** per :class:`_engine.Engine` object.  For dynamic password
             generation per connect, see :ref:`engines_dynamic_tokens`.

        :param host: The name of the host.
        :param port: The port number.
        :param database: The database name.
        :param query: A dictionary of string keys to string values to be passed
          to the dialect and/or the DBAPI upon connect.   To specify non-string
          parameters to a Python DBAPI directly, use the
          :paramref:`_sa.create_engine.connect_args` parameter to
          :func:`_sa.create_engine`.   See also
          :attr:`_engine.URL.normalized_query` for a dictionary that is
          consistently string->list of string.
        :return: new :class:`_engine.URL` object.

        .. versionadded:: 1.4

            The :class:`_engine.URL` object is now an **immutable named
            tuple**.  In addition, the ``query`` dictionary is also immutable.
            To create a URL, use the :func:`_engine.url.make_url` or
            :meth:`_engine.URL.create` function/ method.  To modify a
            :class:`_engine.URL`, use the :meth:`_engine.URL.set` and
            :meth:`_engine.URL.update_query` methods.

        """

        return cls(
            cls._assert_str(drivername, "drivername"),
            cls._assert_none_str(username, "username"),
            password,
            cls._assert_none_str(host, "host"),
            cls._assert_port(port),
            cls._assert_none_str(database, "database"),
            cls._str_dict(query),
            _new_ok=True,
        )

    @classmethod
    def _assert_port(cls, port):
        if port is None:
            return None
        try:
            return int(port)
        except TypeError:
            raise TypeError("Port argument must be an integer or None")

    @classmethod
    def _assert_str(cls, v, paramname):
        if not isinstance(v, compat.string_types):
            raise TypeError("%s must be a string" % paramname)
        return v

    @classmethod
    def _assert_none_str(cls, v, paramname):
        if v is None:
            return v

        return cls._assert_str(v, paramname)

    @classmethod
    def _str_dict(cls, dict_):
        if dict_ is None:
            return util.EMPTY_DICT

        def _assert_value(val):
            if isinstance(val, compat.string_types):
                return val
            elif isinstance(val, collections_abc.Sequence):
                return tuple(_assert_value(elem) for elem in val)
            else:
                raise TypeError(
                    "Query dictionary values must be strings or "
                    "sequences of strings"
                )

        def _assert_str(v):
            if not isinstance(v, compat.string_types):
                raise TypeError("Query dictionary keys must be strings")
            return v

        if isinstance(dict_, collections_abc.Sequence):
            dict_items = dict_
        else:
            dict_items = dict_.items()

        return util.immutabledict(
            {
                _assert_str(key): _assert_value(
                    value,
                )
                for key, value in dict_items
            }
        )

    def set(
        self,
        drivername=None,
        username=None,
        password=None,
        host=None,
        port=None,
        database=None,
        query=None,
    ):
        """return a new :class:`_engine.URL` object with modifications.

        Values are used if they are non-None.  To set a value to ``None``
        explicitly, use the :meth:`_engine.URL._replace` method adapted
        from ``namedtuple``.

        :param drivername: new drivername
        :param username: new username
        :param password: new password
        :param host: new hostname
        :param port: new port
        :param query: new query parameters, passed a dict of string keys
         referring to string or sequence of string values.  Fully
         replaces the previous list of arguments.

        :return: new :class:`_engine.URL` object.

        .. versionadded:: 1.4

        .. seealso::

            :meth:`_engine.URL.update_query_dict`

        """

        kw = {}
        if drivername is not None:
            kw["drivername"] = drivername
        if username is not None:
            kw["username"] = username
        if password is not None:
            kw["password"] = password
        if host is not None:
            kw["host"] = host
        if port is not None:
            kw["port"] = port
        if database is not None:
            kw["database"] = database
        if query is not None:
            kw["query"] = query

        return self._replace(**kw)

    def _replace(self, **kw):
        """Override ``namedtuple._replace()`` to provide argument checking."""

        if "drivername" in kw:
            self._assert_str(kw["drivername"], "drivername")
        for name in "username", "host", "database":
            if name in kw:
                self._assert_none_str(kw[name], name)
        if "port" in kw:
            self._assert_port(kw["port"])
        if "query" in kw:
            kw["query"] = self._str_dict(kw["query"])

        return super(URL, self)._replace(**kw)

    def update_query_string(self, query_string, append=False):
        """Return a new :class:`_engine.URL` object with the :attr:`_engine.URL.query`
        parameter dictionary updated by the given query string.

        E.g.::

            >>> from sqlalchemy.engine import make_url
            >>> url = make_url("postgresql://user:pass@host/dbname")
            >>> url = url.update_query_string("alt_host=host1&alt_host=host2&ssl_cipher=%2Fpath%2Fto%2Fcrt")
            >>> str(url)
            'postgresql://user:pass@host/dbname?alt_host=host1&alt_host=host2&ssl_cipher=%2Fpath%2Fto%2Fcrt'

        :param query_string: a URL escaped query string, not including the
         question mark.

        :param append: if True, parameters in the existing query string will
         not be removed; new parameters will be in addition to those present.
         If left at its default of False, keys present in the given query
         parameters will replace those of the existing query string.

        .. versionadded:: 1.4

        .. seealso::

            :attr:`_engine.URL.query`

            :meth:`_engine.URL.update_query_dict`

        """  # noqa: E501
        return self.update_query_pairs(
            util.parse_qsl(query_string), append=append
        )

    def update_query_pairs(self, key_value_pairs, append=False):
        """Return a new :class:`_engine.URL` object with the
        :attr:`_engine.URL.query`
        parameter dictionary updated by the given sequence of key/value pairs

        E.g.::

            >>> from sqlalchemy.engine import make_url
            >>> url = make_url("postgresql://user:pass@host/dbname")
            >>> url = url.update_query_pairs([("alt_host", "host1"), ("alt_host", "host2"), ("ssl_cipher", "/path/to/crt")])
            >>> str(url)
            'postgresql://user:pass@host/dbname?alt_host=host1&alt_host=host2&ssl_cipher=%2Fpath%2Fto%2Fcrt'

        :param key_value_pairs: A sequence of tuples containing two strings
         each.

        :param append: if True, parameters in the existing query string will
         not be removed; new parameters will be in addition to those present.
         If left at its default of False, keys present in the given query
         parameters will replace those of the existing query string.

        .. versionadded:: 1.4

        .. seealso::

            :attr:`_engine.URL.query`

            :meth:`_engine.URL.difference_update_query`

            :meth:`_engine.URL.set`

        """  # noqa: E501

        existing_query = self.query
        new_keys = {}

        for key, value in key_value_pairs:
            if key in new_keys:
                new_keys[key] = util.to_list(new_keys[key])
                new_keys[key].append(value)
            else:
                new_keys[key] = value

        if append:
            new_query = {}

            for k in new_keys:
                if k in existing_query:
                    new_query[k] = util.to_list(
                        existing_query[k]
                    ) + util.to_list(new_keys[k])
                else:
                    new_query[k] = new_keys[k]

            new_query.update(
                {
                    k: existing_query[k]
                    for k in set(existing_query).difference(new_keys)
                }
            )
        else:
            new_query = self.query.union(new_keys)
        return self.set(query=new_query)

    def update_query_dict(self, query_parameters, append=False):
        """Return a new :class:`_engine.URL` object with the
        :attr:`_engine.URL.query` parameter dictionary updated by the given
        dictionary.

        The dictionary typically contains string keys and string values.
        In order to represent a query parameter that is expressed multiple
        times, pass a sequence of string values.

        E.g.::


            >>> from sqlalchemy.engine import make_url
            >>> url = make_url("postgresql://user:pass@host/dbname")
            >>> url = url.update_query_dict({"alt_host": ["host1", "host2"], "ssl_cipher": "/path/to/crt"})
            >>> str(url)
            'postgresql://user:pass@host/dbname?alt_host=host1&alt_host=host2&ssl_cipher=%2Fpath%2Fto%2Fcrt'


        :param query_parameters: A dictionary with string keys and values
         that are either strings, or sequences of strings.

        :param append: if True, parameters in the existing query string will
         not be removed; new parameters will be in addition to those present.
         If left at its default of False, keys present in the given query
         parameters will replace those of the existing query string.


        .. versionadded:: 1.4

        .. seealso::

            :attr:`_engine.URL.query`

            :meth:`_engine.URL.update_query_string`

            :meth:`_engine.URL.update_query_pairs`

            :meth:`_engine.URL.difference_update_query`

            :meth:`_engine.URL.set`

        """  # noqa: E501
        return self.update_query_pairs(query_parameters.items(), append=append)

    def difference_update_query(self, names):
        """
        Remove the given names from the :attr:`_engine.URL.query` dictionary,
        returning the new :class:`_engine.URL`.

        E.g.::

            url = url.difference_update_query(['foo', 'bar'])

        Equivalent to using :meth:`_engine.URL.set` as follows::

            url = url.set(
                query={
                    key: url.query[key]
                    for key in set(url.query).difference(['foo', 'bar'])
                }
            )

        .. versionadded:: 1.4

        .. seealso::

            :attr:`_engine.URL.query`

            :meth:`_engine.URL.update_query_dict`

            :meth:`_engine.URL.set`

        """

        if not set(names).intersection(self.query):
            return self

        return URL(
            self.drivername,
            self.username,
            self.password,
            self.host,
            self.port,
            self.database,
            util.immutabledict(
                {
                    key: self.query[key]
                    for key in set(self.query).difference(names)
                }
            ),
            _new_ok=True,
        )

    @util.memoized_property
    def normalized_query(self):
        """Return the :attr:`_engine.URL.query` dictionary with values normalized
        into sequences.

        As the :attr:`_engine.URL.query` dictionary may contain either
        string values or sequences of string values to differentiate between
        parameters that are specified multiple times in the query string,
        code that needs to handle multiple parameters generically will wish
        to use this attribute so that all parameters present are presented
        as sequences.   Inspiration is from Python's ``urllib.parse.parse_qs``
        function.  E.g.::


            >>> from sqlalchemy.engine import make_url
            >>> url = make_url("postgresql://user:pass@host/dbname?alt_host=host1&alt_host=host2&ssl_cipher=%2Fpath%2Fto%2Fcrt")
            >>> url.query
            immutabledict({'alt_host': ('host1', 'host2'), 'ssl_cipher': '/path/to/crt'})
            >>> url.normalized_query
            immutabledict({'alt_host': ('host1', 'host2'), 'ssl_cipher': ('/path/to/crt',)})

        """  # noqa: E501

        return util.immutabledict(
            {
                k: (v,) if not isinstance(v, tuple) else v
                for k, v in self.query.items()
            }
        )

    @util.deprecated(
        "1.4",
        "The :meth:`_engine.URL.__to_string__ method is deprecated and will "
        "be removed in a future release.  Please use the "
        ":meth:`_engine.URL.render_as_string` method.",
    )
    def __to_string__(self, hide_password=True):
        """Render this :class:`_engine.URL` object as a string.

        :param hide_password: Defaults to True.   The password is not shown
         in the string unless this is set to False.

        """
        return self.render_as_string(hide_password=hide_password)

    def render_as_string(self, hide_password=True):
        """Render this :class:`_engine.URL` object as a string.

        This method is used when the ``__str__()`` or ``__repr__()``
        methods are used.   The method directly includes additional options.

        :param hide_password: Defaults to True.   The password is not shown
         in the string unless this is set to False.

        """
        s = self.drivername + "://"
        if self.username is not None:
            s += _sqla_url_quote(self.username)
            if self.password is not None:
                s += ":" + (
                    "***"
                    if hide_password
                    else _sqla_url_quote(str(self.password))
                )
            s += "@"
        if self.host is not None:
            if ":" in self.host:
                s += "[%s]" % self.host
            else:
                s += self.host
        if self.port is not None:
            s += ":" + str(self.port)
        if self.database is not None:
            s += "/" + self.database
        if self.query:
            keys = list(self.query)
            keys.sort()
            s += "?" + "&".join(
                "%s=%s" % (util.quote_plus(k), util.quote_plus(element))
                for k in keys
                for element in util.to_list(self.query[k])
            )
        return s

    def __str__(self):
        return self.render_as_string(hide_password=False)

    def __repr__(self):
        return self.render_as_string()

    def __copy__(self):
        return self.__class__.create(
            self.drivername,
            self.username,
            self.password,
            self.host,
            self.port,
            self.database,
            # note this is an immutabledict of str-> str / tuple of str,
            # also fully immutable.  does not require deepcopy
            self.query,
        )

    def __deepcopy__(self, memo):
        return self.__copy__()

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        return (
            isinstance(other, URL)
            and self.drivername == other.drivername
            and self.username == other.username
            and self.password == other.password
            and self.host == other.host
            and self.database == other.database
            and self.query == other.query
            and self.port == other.port
        )

    def __ne__(self, other):
        return not self == other

    def get_backend_name(self):
        """Return the backend name.

        This is the name that corresponds to the database backend in
        use, and is the portion of the :attr:`_engine.URL.drivername`
        that is to the left of the plus sign.

        """
        if "+" not in self.drivername:
            return self.drivername
        else:
            return self.drivername.split("+")[0]

    def get_driver_name(self):
        """Return the backend name.

        This is the name that corresponds to the DBAPI driver in
        use, and is the portion of the :attr:`_engine.URL.drivername`
        that is to the right of the plus sign.

        If the :attr:`_engine.URL.drivername` does not include a plus sign,
        then the default :class:`_engine.Dialect` for this :class:`_engine.URL`
        is imported in order to get the driver name.

        """

        if "+" not in self.drivername:
            return self.get_dialect().driver
        else:
            return self.drivername.split("+")[1]

    def _instantiate_plugins(self, kwargs):
        plugin_names = util.to_list(self.query.get("plugin", ()))
        plugin_names += kwargs.get("plugins", [])

        kwargs = dict(kwargs)

        loaded_plugins = [
            plugins.load(plugin_name)(self, kwargs)
            for plugin_name in plugin_names
        ]

        u = self.difference_update_query(["plugin", "plugins"])

        for plugin in loaded_plugins:
            new_u = plugin.update_url(u)
            if new_u is not None:
                u = new_u

        kwargs.pop("plugins", None)

        return u, loaded_plugins, kwargs

    def _get_entrypoint(self):
        """Return the "entry point" dialect class.

        This is normally the dialect itself except in the case when the
        returned class implements the get_dialect_cls() method.

        """
        if "+" not in self.drivername:
            name = self.drivername
        else:
            name = self.drivername.replace("+", ".")
        cls = registry.load(name)
        # check for legacy dialects that
        # would return a module with 'dialect' as the
        # actual class
        if (
            hasattr(cls, "dialect")
            and isinstance(cls.dialect, type)
            and issubclass(cls.dialect, Dialect)
        ):
            return cls.dialect
        else:
            return cls

    def get_dialect(self):
        """Return the SQLAlchemy :class:`_engine.Dialect` class corresponding
        to this URL's driver name.

        """
        entrypoint = self._get_entrypoint()
        dialect_cls = entrypoint.get_dialect_cls(self)
        return dialect_cls

    def translate_connect_args(self, names=None, **kw):
        r"""Translate url attributes into a dictionary of connection arguments.

        Returns attributes of this url (`host`, `database`, `username`,
        `password`, `port`) as a plain dictionary.  The attribute names are
        used as the keys by default.  Unset or false attributes are omitted
        from the final dictionary.

        :param \**kw: Optional, alternate key names for url attributes.

        :param names: Deprecated.  Same purpose as the keyword-based alternate
            names, but correlates the name to the original positionally.
        """

        if names is not None:
            util.warn_deprecated(
                "The `URL.translate_connect_args.name`s parameter is "
                "deprecated. Please pass the "
                "alternate names as kw arguments.",
                "1.4",
            )

        translated = {}
        attribute_names = ["host", "database", "username", "password", "port"]
        for sname in attribute_names:
            if names:
                name = names.pop(0)
            elif sname in kw:
                name = kw[sname]
            else:
                name = sname
            if name is not None and getattr(self, sname, False):
                if sname == "password":
                    translated[name] = str(getattr(self, sname))
                else:
                    translated[name] = getattr(self, sname)

        return translated


def make_url(name_or_url):
    """Given a string or unicode instance, produce a new URL instance.


    The format of the URL generally follows `RFC-1738
    <https://www.ietf.org/rfc/rfc1738.txt>`_, with some exceptions, including
    that underscores, and not dashes or periods, are accepted within the
    "scheme" portion.

    If a :class:`.URL` object is passed, it is returned as is.

    """

    if isinstance(name_or_url, util.string_types):
        return _parse_url(name_or_url)
    else:
        return name_or_url


def _parse_url(name):
    pattern = re.compile(
        r"""
            (?P<name>[\w\+]+)://
            (?:
                (?P<username>[^:/]*)
                (?::(?P<password>[^@]*))?
            @)?
            (?:
                (?:
                    \[(?P<ipv6host>[^/\?]+)\] |
                    (?P<ipv4host>[^/:\?]+)
                )?
                (?::(?P<port>[^/\?]*))?
            )?
            (?:/(?P<database>[^\?]*))?
            (?:\?(?P<query>.*))?
            """,
        re.X,
    )

    m = pattern.match(name)
    if m is not None:
        components = m.groupdict()
        if components["query"] is not None:
            query = {}

            for key, value in util.parse_qsl(components["query"]):
                if util.py2k:
                    key = key.encode("ascii")
                if key in query:
                    query[key] = util.to_list(query[key])
                    query[key].append(value)
                else:
                    query[key] = value
        else:
            query = None
        components["query"] = query

        if components["username"] is not None:
            components["username"] = _sqla_url_unquote(components["username"])

        if components["password"] is not None:
            components["password"] = _sqla_url_unquote(components["password"])

        ipv4host = components.pop("ipv4host")
        ipv6host = components.pop("ipv6host")
        components["host"] = ipv4host or ipv6host
        name = components.pop("name")

        if components["port"]:
            components["port"] = int(components["port"])

        return URL.create(name, **components)

    else:
        raise exc.ArgumentError(
            "Could not parse SQLAlchemy URL from string '%s'" % name
        )


def _sqla_url_quote(text):
    return re.sub(r"[:@/]", lambda m: "%%%X" % ord(m.group(0)), text)


def _sqla_url_unquote(text):
    return util.unquote(text)


def _parse_keyvalue_args(name):
    m = re.match(r"(\w+)://(.*)", name)
    if m is not None:
        (name, args) = m.group(1, 2)
        opts = dict(util.parse_qsl(args))
        return URL(name, *opts)
    else:
        return None

# Standard library imports.
import argparse
import copy
import json
import re
import sys
from _io import TextIOWrapper
from datetime import datetime as _dt
from datetime import timedelta as _td
from zoneinfo import ZoneInfo as ZI


# Define a tuple of the allowable object types that can be queried for
# data.
TYPES = (
    type({}), type([]), type(''), type(0.1), type(0), type(True), type(None),)

# Define functions that wrap conditional statements.
CO_FUNCS = (
    ('cond', lambda x, y: True if x == True and y == True else False),
    ('coor', lambda x, y: True if x == True or y == True else False),)

# These are the lambda functions that test for equality.
EQ_FUNCS = (
    ('eqgt', lambda x, y: x > y),
    ('eqge', lambda x, y: x >= y),
    ('eqeq', lambda x, y: x == y),
    ('eqne', lambda x, y: x != y),
    ('eqle', lambda x, y: x <= y),
    ('eqlt', lambda x, y: x < y))

EQ_SYMBOLS = ('>', '>=', '==', '!=', '<=', '<',)


# The special mapping method will return an instance of this class.
class GMap:
    def __init__(self, rows):
        self.rows = rows


# The special select method will return an instance of this class.
class GSlc:
    def __init__(self, obj):
        self.value = obj


class P:

    def __init__(self):

        # Define the environment that will be used to evaluate the
        # input expressions.
        self.env = {'__builtins__': {}, 'o': None}

        # Populate the '__builtins__' with the instance methods in
        # this class.
        for attr in dir(self):

            if attr.startswith('_P__f_'):

                obj = getattr(self, attr, None)

                if callable(obj):
                    self.env['__builtins__'][attr[6:]] = obj

        for co in CO_FUNCS:
            self.env['__builtins__'][co[0]] = co[1]

        for eq in EQ_FUNCS:
            self.env['__builtins__'][eq[0]] = eq[1]

        # Add the special methods.  These are methods that access
        # and/or change the eval environment.
        self.env['__builtins__'].update(
            {
                'gmap': self.__s_gmap,
                'gslc': self.__s_gslc,
                'svar': self.__s_svar})

        # The following instance variable is set when the program is
        # evaluating code after a generator is created.
        self.gen_loop = False

        return None

    def __is(self, index):
        """Create a string that represents the index of a value in a
        list, dictionary, or nested lists and/or dictionaries.

        """
        _is = ''

        if type(index) == type(0):
            _is = '[' + str(index) + ']'

        elif type(index) == type(''):
            _is = '["' + index + '"]'

        elif type(index) == type([]):

            _is = ''

            for i in index:

                if type(i) == type(''):
                    _is += '["' + i + '"]'

                else:
                    _is += '[' + str(i) + ']'

        return _is

    def __f_dprs(self, obj, tmpl, tz = None, to_tz = None):

        try:

            d = _dt.strptime(obj, tmpl)

            if (tz != None) and (to_tz != None):
                d = _dt.combine(d.date(), d.time(), ZI(tz))\
                    .astimezone(ZI(to_tz))

        except:
            d = None

        if d != None:
            d = str(d)

        return d

    def __f_fltr(self, obj, index, symb, value):

        if symb in EQ_SYMBOLS:

            if type(index) == type(None):
                exec('_ = lambda x: True')

            else:

                _x = 'x' + self.__is(index)
                _l = '_ = lambda x: {x} {symb} {value}'.format(
                    {'x': _x, 'symb': symb, 'value': value})
                exec(_l)

            ffunc = locals()['_']

            if 'generator' in str(type(obj)):

                try:
                    fltrd = filter(ffunc, obj)

                except:
                    raise Exception('Unable to filter generator')

            elif type(obj) == type([]):

                try:
                    fltrd = filter(ffunc, (x for x in obj))

                except:
                    raise Exception('Unable to filter list')

            else:
                raise Exception('obj is not an iterable or a generator')

        else:
            raise Exception('Invalid equality symbol')

        return list(fltrd)

    def __f_genr(self, obj):
        """Create a generator from a given list or dictionary object.
        This method will raise an exception if a generator can't be
        created.

        """
        if type(obj) == type([]):
            obj = (x for x in obj)

        else:
            raise Exception('Cannot create generator from obj')

        return obj

    def __f_getv(self, obj, index, default = None):

        _is = self.__is(index)

        try:
            value = eval('obj' + _is)

        except:
            value = default

        return value


    def __f_ifte(self, c, t, e):

        _c = c
        _t = t
        _e = e

        if type(_c) == type(''):
            _c = '"' + _c + '"'

        else:
            _c = str(c)

        if type(_t) == type(''):
            _t = '"' + _t + '"'

        else:
            _t = str(t)

        if type(_e) == type(''):
            _e = '"' + _e + '"'

        else:
            _e = str(e)

        try:
            ifte = eval(_t + ' if ' + _c + ' else ' + _e)

        except:
            raise Exception('Error evaluating ifte')

        return ifte

    def __f_keys(self, obj):
        """Get the keys of the given object.  If the object is a
        dictionary type, then the result is obvious.  If the object is
        a list, then the result is a list of integers representing each
        index in the list.

        """
        if type(obj) == type([]):
            keys = list(range(len(obj)))

        elif type(obj) == type({}):
            keys = obj.keys()

        else:
            keys = None

        return keys

    def __f_lngt(self, obj):
        """Return the length of the object.  This method effectively
        wraps the built-in Python "len" function.  Why?  All methods
        that can be used in a process for "Gzmo" is a four letter
        name.

        """
        return len(obj)

    def __f_rmfd(self, obj, key):
        """Remove the attribute with the given key from a dictionary
        object.

        """
        if type(obj) == type({}):
            if key in obj:
                del obj[key]

        return obj

    def __f_stat(self, obj):

        # Use this variable to store statistics.  If the input object
        # is a list of numbers, then the stats will be a dictionary.
        # Otherwise, if the input object is a list of lists, then
        # the stats will be a list containing stats dictionaries for
        # each element of the first list in the input object.  If the
        # input object is a list of dictionaries, the stats will be
        # a dictionary of stats dictionaries for each key in the first
        # dictionary in input object.
        stats = None

        # Set the type of the first element in the input object list
        # using this variable.
        ftype = None

        # Call to create an empty stats dictionary.
        def _e():
            return {'max': None, 'min': None, 'avg': None, 'num': 0, 'sum': 0}

        # Use this function internally to help calculate the list's
        # statistics.
        def _s(i, v, s):

            if type(v) in (type(0), type(0.0),):

                if s['max'] == None:
                    s['max'] = {'obj': i, 'val': v}

                elif v > s['max']['val']:
                    s['max'] = {'obj': i, 'val': v}

                if s['min'] == None:
                    s['min'] = {'obj': i, 'val': v}

                elif v < s['min']['val']:
                    s['min'] = {'obj': i, 'val': v}

                s['num'] += 1
                s['sum'] += v
                s['avg'] = s['sum'] / s['num']

            return s

        if type(obj) == type([]):

            counter = 0

            for i in obj:

                if ftype == None:
                    ftype = type(i)

                if stats == None:

                    if ftype == type({}):

                        stats = {}

                        for j in i.keys():
                            stats[j] = _e()

                    elif ftype == type([]):

                        stats = [None] * len(i)

                        for j in range(0, len(i)):
                            stats[j] = _e()

                    elif ftype in (type(0), type(0.0)):
                        stats = _e()

                if type(i) != ftype:
                    raise Exception('Mismatched types calculating stats')

                elif type(i) == type({}):
                    for j in i.keys():
                        if j in stats.keys():
                            _s(i, i[j], stats[j])

                elif type(i) == type([]):
                    if len(i) == len(stats):
                        for j in range(0, len(i)):
                            _s(i, i[j], stats[j])

                else:
                    _s(counter, i, stats)

                counter += 1

        if stats != None:

            if ftype == type({}):
                for j in stats.keys():
                    if stats[j]['num'] == 0:
                        stats[j] = None

            if ftype == type([]):
                for j in range(0, len(stats)):
                    if stats[j]['num'] == 0:
                        stats[j] = None

        return stats

    def __f_trim(self, obj, start, end):
        """Trim a string value.  This method will return a NoneType if
        the slice of the string is invalid.  i.e., the processing will
        continue if this fails.

        """
        try:
            value = obj[start:end]

        except:
            value = None

        return value

    def __s_gmap(self, rows):

        if self.gen_loop == True:

            if type(rows) == type([]):
                for row in rows:
                    if len(row) != 2:
                        raise Exception(
                            'gmap must take a list of two item lists')

            else:

                msg = 'gmap must take a list of two item lists'
                raise Exception(msg)

        else:

            msg = 'gmap can only be used in the stage after a generator '\
                + 'is created'
            raise Exception(msg)

        return GMap(rows)

    def __s_gslc(self, is_selected, obj):

        selected = GSlc(obj)

        if self.gen_loop == True:

            if type(obj) in TYPES:
                if is_selected == False:
                    selected = GSlc(None)

            else:
                raise Exception('Attempting to select an invalid object')

        else:

            msg = 'gslc can only be used in the stage after a generator '\
                + 'is created'
            raise Exception(msg)

        return selected

    def __s_svar(self, name, value):

        reserved = ['__builtins__', 'o']\
            + list(self.env['__builtins__'].keys())
        match = re.match('^[^\d][A-Za-z0-9_]*$', name)

        if (name not in reserved) and (match != None):
            self.env[name] = copy.deepcopy(value)

        else:
            raise Exception(name + ' is not a valid variable name')

        return self.env['o']

    def _parse_exprs(self, pstr):

        # Create a temporary string of expressions with underscores
        # replacing any quoted substrings (they may have spaces or
        # the pipe symbol).
        tmp = list(pstr)

        for r in re.finditer('"([^"]*)"', pstr):

            span = r.span()

            for i in range(span[0] + 1, span[1] - 1):
                tmp[i] = '_'

        tmp = "".join(tmp)

        # Slice up the process string by the pipe symbol into Python
        # expressions.
        exprs = []
        pos = 0

        for r in re.finditer('\|', tmp):

            exprs.append(pstr[pos:r.span()[0]].strip())
            pos = r.span()[1]

        if pos < len(pstr):
            exprs.append(pstr[pos:].strip())

        return exprs

    def _p(self, obj, pstr, **extras):

        def _rcrs(rdict, key, value):

            if len(key) == 1:

                if key[0] not in rdict:
                    rdict[key[0]] = []

                rdict[key[0]].append(value)

            elif len(key) > 1:

                if key[0] not in rdict:
                    rdict[key[0]] = {}

                _rcrs(rdict[key[0]], key[1:], value)

            return None

        if type(obj) in TYPES:
            self.env['o'] = copy.deepcopy(obj)

        # If any extra functions or variables are given in the extras
        # arguments, add them to the evaluation namespace.
        for k in extras.keys():
            if (callable(extras[k])) or type(extras[k]) in TYPES:
                self.__s_svar(k, extras[k])

        # Parse the expressions from the process string, then evaluate
        # each expression in the following loop.  Remember that in most
        # cases, the result of the evaluation is made available for the
        # next expression to be evaluated.
        stage = 0
        error = ''
        passing = True

        for expr in self._parse_exprs(pstr):

            if passing == True:

                try:

                    if 'generator' in str(type(self.env['o'])):

                        # Make sure that the slct method (if specified
                        # in the expression) knows that we are in the
                        # generator loop.
                        self.gen_loop = True

                        # Data from the generator loop will be stored
                        # using this variable.  If the data is a
                        # "primative," then this variable will be a
                        # list.  If the data is a result of the mapping
                        # method, then the variable will initially be a
                        # dictionary.  If the data is a result of a the
                        # select method, then the result will be a list.
                        gres = None

                        # Execute the generator.  As the generator is
                        # iterated, the "o" value will be updated with
                        # the current value of the iterator.
                        for i in self.env['o']:

                            self.env['o'] = i
                            _ =  eval(expr, self.env, {})

                            if type(_) == type(()):
                                _ = list(_)

                            if type(_) == type(GMap(None)):

                                if gres == None:
                                    gres = {}

                                if type(_.rows) == type([]):

                                    for row in _.rows:

                                        if type(row[0]) == type(''):

                                            if row[0] not in gres.keys():
                                                gres[row[0]] = []

                                            gres[row[0]].append(row[1])

                                        elif type(row[0]) == type([]):
                                            _rcrs(gres, row[0], row[1])

                            elif type(_) == type(GSlc(None)):

                                if gres == None:
                                    gres = []

                                if _.value != None:
                                    gres.append(_.value)

                            else:

                                if gres == None:
                                    gres = []

                                gres.append(_)

                        # Set the results of the iteration back into
                        # the eval environment.
                        self.env['o'] = gres

                    else:
                        self.env['o'] = eval(expr, self.env, {})

                except NameError as e:

                    error = str((stage, expr)) + ': ' + str(e)
                    passing = False

                except SyntaxError as e:

                    msg = '\'' + e.text[e.offset -1:e.end_offset - 1] + '\''
                    error = str((stage, expr)) + ': ' + msg
                    passing = False

                except TypeError as e:

                    error = str((stage, expr)) + ': ' + str(e)
                    passing = False

                except Exception as e:

                    error = str((stage, expr)) + ': ' + str(e)
                    passing = False

            # Before the next evaluation occurs, make sure that the
            # gen_loop flag is set to false.
            self.gen_loop = False

            # Increment the processing stage counter
            stage += 1

        # If the data object is a generator after all the process
        # strings have been evaluated, then generate a list as the
        # final data structure to be returned.
        if 'generator' in str(type(self.env['o'])):
            self.env['o'] = list(self.env['o'])

        # If all process stations passed, then output the new object,
        # otherwise output None.
        if passing == True:
            output = self.env['o']

        else:
            output = (error,)

        return output


def process(obj, pstr, **extras):

    # Create the process instance and return the results of the
    # evaluations of the process strings.
    return P()._p(obj, pstr, **extras)


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument(
        'pstr',
        type = str,
        help = 'A string of expressions used to process the given JSON data')
    parser.add_argument(
        '-i',
        '--input-file',
        type = argparse.FileType('r'),
        default = (None if sys.stdin.isatty() else sys.stdin))
    parser.add_argument(
        '-o',
        '--output-file',
        type = argparse.FileType('w'),
        default = sys.stdout)
    parser.add_argument(
        '-p',
        action = 'store_true',
        help = 'Pretty-print output, instead of compact')

    args = parser.parse_args()

    if type(args.input_file) == TextIOWrapper:

        try:
            contents = args.input_file.read()

        except:
            contents = None

        if contents != None:

            try:
                data = json.loads(contents)

            except:
                data = {}

            p = process(data, args.pstr)

            if type(p) in TYPES:

                if args.p == True:
                    output = json.dumps(p, indent = 1)

                else:
                    output = json.dumps(p)

                # Output the processed data to stdout.
                if type(output) == type(''):
                    args.output_file.write(output + '\n')

            elif type(p) == type((0,)):
                sys.stderr.write(p[0] + '\n')

    # Explicitly exit the script.
    sys.exit(0)


if __name__ == '__main__':
    main()

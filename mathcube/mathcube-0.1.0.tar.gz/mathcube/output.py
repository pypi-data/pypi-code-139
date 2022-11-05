from IPython.display import display as ipython_display
from itertools import product

class Latex:
    delimiter = '$$'

    def __init__(self, latex):
        self._latex = latex

    @property
    def latex(self):
        return self._latex

    def _repr_latex_(self):
        return ' {} {} {} '.format(
            self.delimiter, self.latex, self.delimiter
        )

    def __add__(self, other):
        if isinstance(other, str):
            other = Latex(other)
        return Latex(self.latex + ' ' + other.latex)

    def __radd__(self, other):
        return Latex(other + ' ' + self.latex)


class LatexInline(Latex):
    delimiter = '$'


class Text(Latex):
    delimiter = '$'

    def __init__(self, text):
        self.latex = r'\mbox{%s}' % text


class HTML:
    ...


class Table(HTML):

    def __init__(self, data=None):
        if data is None:
            data = [[]]
        self._data = data
        self.style = CellStyler(self)

    def _repr_html_(self):
        s = '<table>\n'
        for irow, row in enumerate(self._data):
            s += '<tr>\n'
            for icol, col in enumerate(row):
                s += '<td style="%s"> $' % (self.style[irow, icol]) + str(col) + ' $ </td>\n'
            s += '</tr>\n'
        s += '</table>\n'
        return s

    @property
    def shape(self):
        return len(self._data), len(self._data[0])

    def __getitem__(self, key):
        row_idx, col_idx = key
        return self._data[row_idx][col_idx]

    def __setitem__(self, key, value):
        row, col = key
        self._data[row][col] = value

    def insert_column(self, idx=None):
        if idx is None:
            for row in self._data:
                row.append('')
        elif idx < 0:
            raise ValueError('Negative indexing not allowed')
        else:
            for row in self._data:
                row.insert(idx, '')

    def insert_row(self, idx=None):
        nrows, ncols = self.shape
        if idx is None:
            self._data.append(['']*ncols)
        elif idx < 0:
            raise ValueError('Negative indexing not allowed')
        else:
            self._data.insert(idx, ['']*ncols)

    def add_row(self, row_data):
        self._data.append(row_data)


class CellStyler:

    def __init__(self, table):
        self.table = table
        self.styles = {}

    def __setitem__(self, key, value):
        nrows, ncols = self.table.shape
        all_row_idxs = list(range(nrows))
        all_col_idxs = list(range(ncols))
        row_idx, col_idx = key
        if isinstance(row_idx, slice):
            row_idxs = all_row_idxs[row_idx]
        else:
            row_idxs = [row_idx]
        if isinstance(col_idx, slice):
            col_idxs = all_col_idxs[col_idx]
        else:
            col_idxs = [col_idx]

        cell_idxs = product(row_idxs, col_idxs)
        for cell_idx in cell_idxs:
            self.styles[cell_idx] = value

    def __getitem__(self, key):
        return self.styles.get(key, '')

class HashableSlice:

    def __init__(self, slc):
        self.start = slc.start
        self.stop = slc.stop
        self.step = slc.step

    def to_slice(self):
        return slice(self.start, self.stop, self.step)

    def __hash__(self):
        return hash(repr('%s, %s, %s' % (self.start, self.stop, self.step)))


class Output:

    def __init__(self):
        self.lines = []

    def _to_latex(self, text):
        if isinstance(text, str):
            return Latex(text)
        return text

    def append(self, text):
        self.lines.append(self._to_latex(text))

    def _repr_latex_(self):
        out = ''
        for line in self.lines:
            out += line._repr_latex_()
        return out


def display(*args, **kwargs):
    for arg in args:
        if isinstance(arg, list) or isinstance(arg, tuple):
            for item in arg:
                ipython_display(item)
        return
    ipython_display(*args)

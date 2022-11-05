from collections import OrderedDict, defaultdict
from typing import List, Optional, Sequence, Tuple, Union

import pandas as pd

from sm.inputs.column import Column


class ColumnBasedTable:
    __slots__ = ("table_id", "columns", "index2columns", "_df")

    def __init__(self, table_id: str, columns: List[Column]):
        self.table_id = table_id
        self.columns = columns
        self.index2columns = {col.index: col for col in columns}
        self._df: Optional[pd.DataFrame] = None

    @property
    def df(self) -> pd.DataFrame:
        if self._df is None:
            self._df = self.as_dataframe()
        return self._df

    def shape(self) -> Tuple[int, int]:
        """Get shape of table: (number of rows, number of columns)"""
        if len(self.columns) == 0:
            return 0, 0
        return len(self.columns[0].values), len(self.columns)

    def get_column_by_index(self, col_idx: int) -> Column:
        return self.index2columns[col_idx]

    def as_dataframe(self) -> pd.DataFrame:
        d = OrderedDict()
        dup = defaultdict(int)
        for i, col in enumerate(self.columns):
            if col.name is None:
                cname = f"unk_{i:02}"
            else:
                cname = col.name

            if cname in d:
                dup[cname] += 1
                cname += f" ({dup[cname]})"
            d[cname] = col.values
        return pd.DataFrame(d)

    def subset(self, start_row: int, end_row: int):
        return ColumnBasedTable(
            self.table_id,
            [
                Column(c.index, c.name, c.values[start_row:end_row])
                for c in self.columns
            ],
        )

    def to_dict(self):
        return {
            "version": "2",
            "table_id": self.table_id,
            "columns": [col.to_dict() for col in self.columns],
        }

    def __getitem__(self, item: Tuple[int, int]):
        return self.columns[item[1]][item[0]]

    @staticmethod
    def from_dict(record: dict):
        assert record.get("version", None) == "2", record.get("version", None)
        return ColumnBasedTable(
            record["table_id"],
            [
                Column(col["index"], col["name"], col["values"])
                for col in record["columns"]
            ],
        )

    @staticmethod
    def from_dataframe(df: pd.DataFrame, table_id: str):
        columns = []
        for ci, c in enumerate(df.columns):
            values = [r[ci] for ri, r in df.iterrows()]
            column = Column(ci, c, values)
            columns.append(column)
        return ColumnBasedTable(table_id, columns)

    @staticmethod
    def from_rows(
        records: Sequence[Sequence[Union[str, int, float, bool]]],
        table_id: str,
        headers: Optional[Sequence[str]] = None,
        strict: bool = False,
    ):
        if len(records) == 0:
            return ColumnBasedTable(table_id, [])

        if headers is None:
            headers = ["" for _ in range(len(records[0]))]

        if strict:
            ncols = len(headers)
            assert all(
                len(r) == ncols for r in records
            ), "All rows must have the same number of columns"

        columns = []
        for ci, col in enumerate(headers):
            columns.append(Column(ci, col, values=[r[ci] for r in records]))

        return ColumnBasedTable(table_id, columns)

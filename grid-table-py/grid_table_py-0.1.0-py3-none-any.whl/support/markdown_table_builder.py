import textwrap
from copy import deepcopy
from typing import List

import numpy as np
import pandas as pd


class MarkdownTableBuilder:
    def __init__(self, data: pd.DataFrame | List | None = None,
                 labels: pd.Series | List | None = None):
        self.data: pd.DataFrame = pd.DataFrame(data=deepcopy(data))
        if type(data) != pd.DataFrame:
            self.data = self.data.T  # Probably

        if labels is None and type(data) == pd.DataFrame:
            # Infer Markdown Table labels from the data frame if not explicitly provided and they are present.
            if type(data.columns[0]) == str:
                labels = pd.Series(data.columns)
        if labels is not None:
            self.labels: pd.Series = pd.Series(labels)
        else:
            self.labels: pd.Series = pd.Series(dtype=object)

    def get_data_frame(self):
        frame = deepcopy(self.data)
        if self.labels.size == self.data.shape[1]:
            frame.columns = self.labels
        return frame

    def r_append(self, data: pd.DataFrame | pd.Series | List):
        match type(data):
            case pd.DataFrame:
                appendee_shape = data.shape
                appendor_shape = self.data.shape
                if appendor_shape[1] == data.shape[1] or appendor_shape[1] == 0:
                    pass
                elif appendor_shape[1] == data.shape[0]:
                    data = data.T
                else:
                    raise IndexError(f"Data to append is of incompatible size: expected {appendor_shape[1]} column "
                                     f"entries but data is {appendee_shape[0]} by {appendee_shape[1]}")
            case pd.Series:
                data = data.to_frame().T
            case List:
                data = pd.DataFrame(data=data).T

        self.data = pd.concat([self.data, data], ignore_index=True)

    def to_pipe_table(self):
        frame = self.get_data_frame()
        return frame.to_markdown()

    def to_grid_table(self, table_width: int = 80) -> List[str]:
        # frame = self.get_data_frame()
        # return frame.to_markdown(tablefmt="grid")
        data = self.get_data_frame()
        col_titles = np.array(data.columns.array, dtype=str)

        # Choosing to do dynamic column spacing based on column-mean entry length
        col_entries = data.values
        n_rows = col_entries.shape[0]
        n_cols = col_entries.shape[1]
        mean_col_lengths = np.zeros([n_cols])
        for column in range(n_cols):
            mean_col_lengths[column] = len(str(col_titles[column]))
            for row in range(n_rows):
                mean_col_lengths[column] = ((row + 1) * mean_col_lengths[column] + len(col_entries[row, column])) / (
                        row + 2
                )

        width_budget = table_width - n_cols * 3 - 1  # Accounts for borders and border whitespace
        relative_reconciled_lengths = np.array(
            mean_col_lengths / np.sum(mean_col_lengths) * width_budget, dtype=int)
        if np.sum(relative_reconciled_lengths) < width_budget:
            deficit: int = width_budget - np.sum(relative_reconciled_lengths)
            relative_reconciled_lengths[relative_reconciled_lengths.argmin()] += deficit
        elif np.sum(relative_reconciled_lengths > width_budget):
            deficit: int = np.sum(relative_reconciled_lengths) - width_budget
            relative_reconciled_lengths[relative_reconciled_lengths.argmax()] -= deficit

        newlines = np.zeros([n_rows + 1, n_cols], dtype=int)
        for column in range(col_titles.shape[0]):
            col_titles[column] = textwrap.fill(col_titles[column], relative_reconciled_lengths[column])
            newlines[-1, column] = col_titles[column].count('\n') + 1
            for row in range(col_entries.shape[0]):
                col_entries[row, column] = textwrap.fill(col_entries[row, column], relative_reconciled_lengths[column])
                newlines[row, column] = col_entries[row, column].count('\n') + 1

        str_array = []
        horizontal_line = "+"
        for col_length in relative_reconciled_lengths:
            horizontal_line += "-" * (col_length + 2) + "+"
        str_array.append(horizontal_line)
        max_col_title_newlines = np.array(np.max(newlines[-1, :]), dtype=int)
        for line in range(max_col_title_newlines):
            s = ""
            for column in range(n_cols):
                s += "| "
                line_entry = list(" " * (relative_reconciled_lengths[column] + 1))
                if len(col_titles[column]) > 0:
                    line_entry_length = col_titles[column].find('\n')
                    if line_entry_length == -1:
                        line_entry_length = len(col_titles[column])
                        line_entry[:line_entry_length] = list(col_titles[column])
                        col_titles[column] = ""
                    else:
                        line_entry[:line_entry_length] = list(col_titles[column][:line_entry_length])
                        col_titles[column] = col_titles[column][line_entry_length + 1:]
                s += ''.join(line_entry)

            s += "|"
            str_array.append(s)

        str_array.append(horizontal_line.replace('-', '='))

        for row in range(n_rows):
            max_col_newlines = np.max(newlines[row, :])
            for line in range(max_col_newlines):
                s = ""
                for column in range(n_cols):
                    s += "| "
                    line_entry = list(" " * (relative_reconciled_lengths[column] + 1))
                    if len(col_entries[row, column]) > 0:
                        line_entry_length = col_entries[row, column].find('\n')
                        if line_entry_length == -1:
                            line_entry_length = len(col_entries[row, column])
                            line_entry[:line_entry_length] = list(col_entries[row, column])
                            col_entries[row, column] = ""
                        else:
                            line_entry[:line_entry_length] = list(col_entries[row, column][:line_entry_length])
                            col_entries[row, column] = col_entries[row, column][line_entry_length + 1:]

                    s += ''.join(line_entry)

                s += "|"
                str_array.append(s)

            str_array.append(horizontal_line)
        return str_array

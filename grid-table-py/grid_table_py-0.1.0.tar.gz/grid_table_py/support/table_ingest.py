from typing import List

import numpy as np

from grid_table_py.support.markdown_table_builder import MarkdownTableBuilder

MARKER_CHARS = ['>', ' ', '|', ':', '-']
QUOTECHAR = '>'


def interpret_table_from_snippet(text: str, out: List | None = None) -> List[MarkdownTableBuilder]:
    def number_of_divisors(line: str):
        n = 0
        for i in range(len(line)):
            if line[i] == '|' and line[i - 1] != '\\':
                n += 1

        return n

    lines = np.array(text.split('\n'))
    table_lines = []
    marked_lines = np.ndarray([len(lines), 1], dtype=bool)
    marked_lines[:] = False
    for line in range(len(lines)):
        is_table_line = True
        if lines[line] == "":
            is_table_line = False
        else:
            has_minus = False
            has_pipe = False
            for character in lines[line]:
                if character not in MARKER_CHARS:
                    is_table_line = False
                    break
                elif character == "-":
                    has_minus = True
                elif character == "|":
                    has_pipe = True

            if not has_minus or not has_pipe:
                is_table_line = False

        if is_table_line:
            table_lines.append(line)
            marked_lines[line] = True

    table_lines = np.array(table_lines, dtype=int) - 1
    table_builders: List[MarkdownTableBuilder] = []

    for i in range(table_lines.shape[0]):
        index = table_lines[i]
        marked_lines[index] = True
        quoted = False

        def tokenize(line: str):
            if quoted:
                shorten = " ".join(np.array(line.split()[1:]))
                tokens = np.array(shorten.split(" | "))
            else:
                shorten = " ".join(np.array(line.split()))
                tokens = np.array(shorten.split(" | "))

            for i in range(len(tokens)):
                tokens[i] = tokens[i].replace("|", "").strip()
            return tokens

        table_col_title_line = lines[index]
        index += 2
        if table_col_title_line.startswith(QUOTECHAR):
            quoted = True

        table_col_titles = tokenize(table_col_title_line)
        n_divisors = number_of_divisors(table_col_title_line)
        line = lines[index]
        entries = np.ndarray([0, n_divisors-1])

        while number_of_divisors(line) == n_divisors:
            marked_lines[index] = True
            row_entries = tokenize(line)
            entries = np.append(entries, row_entries)
            index += 1
            line = lines[index]


        builder: MarkdownTableBuilder = MarkdownTableBuilder(data=entries, labels=table_col_titles)
        table_builders.append(builder)

    if out is not None:
        ctr = 0
        ptr = 0
        table_beginning = True
        for index in range(marked_lines.size):
            if marked_lines[index]:
                if table_beginning:
                    table_beginning = False
                    if lines[ptr].startswith(">"):
                        lines[ptr] = lines[ptr].split()[0] + f" ++TABLE++{ctr}++"
                    else:
                        lines[ptr] = f"++TABLE++{ctr}++"

                    ctr += 1
                    ptr += 1
                else:
                    if ptr != lines.shape[0]:
                        lines = np.append(lines[:ptr], lines[ptr+1:])
                    else:
                        lines = lines[:ptr]
            else:
                table_beginning = True
                ptr += 1

        placeholder_text = "\n".join(lines)
        out.append(placeholder_text)

    return table_builders


from typing import Union
import pandas as pd
from pandas.core.frame import Series


def how_many_to_add_until_even(n1: int, n2: int) -> int:
    number1original = n1
    number2original = n2
    number1 = number1original
    number2 = number2original
    while divmod(number1, number2)[-1] != 0:
        number1 += 1
    toadd = number1 - number1original
    return toadd


def series_to_dataframe(
    df: Union[pd.Series, pd.DataFrame]
) -> (Union[pd.Series, pd.DataFrame], bool):
    dataf = df.copy()
    isseries = False
    if isinstance(dataf, pd.Series):
        columnname = dataf.name
        dataf = dataf.to_frame()

        try:
            dataf.columns = [columnname]
        except Exception:
            dataf.index = [columnname]
            dataf = dataf.T
        isseries = True

    return dataf, isseries


def pd_vertical_to_horizontal(
    dframe: Union[pd.Series, pd.DataFrame],
    number_of_cells_to_join: int,
    drop_redundant: bool = False,
    negative: bool = True,
) -> pd.DataFrame:
    r"""
    from a_pandas_ex_vertical_to_horizontal import pd_add_vertical_to_horizontal
    pd_add_vertical_to_horizontal()

    df = pd.concat(
        [pd.Series(range(0, 20)), pd.Series(range(1000, 1020))], axis=0
    ).reset_index(drop=True)


    df1 = df.s_vertical_to_horizontal(number_of_cells_to_join=3, drop_redundant=False, negative=False)
    df2 = df.s_vertical_to_horizontal(number_of_cells_to_join=6, drop_redundant=True, negative=True)




    print(df.to_string())
    0        0
    1        1
    2        2
    3        3
    4        4
    5        5
    6        6
    7        7
    8        8
    9        9
    10      10
    11      11
    12      12
    13      13
    14      14
    15      15
    16      16
    17      17
    18      18
    19      19
    20    1000
    21    1001
    22    1002
    23    1003
    24    1004
    25    1005
    26    1006
    27    1007
    28    1008
    29    1009
    30    1010
    31    1011
    32    1012
    33    1013
    34    1014
    35    1015
    36    1016
    37    1017
    38    1018
    39    1019


    print(df1.to_string())
        col_0  col_1  col_2
    0       0   1019   1018
    1       1      0   1019
    2       2      1      0
    3       3      2      1
    4       4      3      2
    5       5      4      3
    6       6      5      4
    7       7      6      5
    8       8      7      6
    9       9      8      7
    10     10      9      8
    11     11     10      9
    12     12     11     10
    13     13     12     11
    14     14     13     12
    15     15     14     13
    16     16     15     14
    17     17     16     15
    18     18     17     16
    19     19     18     17
    20   1000     19     18
    21   1001   1000     19
    22   1002   1001   1000
    23   1003   1002   1001
    24   1004   1003   1002
    25   1005   1004   1003
    26   1006   1005   1004
    27   1007   1006   1005
    28   1008   1007   1006
    29   1009   1008   1007
    30   1010   1009   1008
    31   1011   1010   1009
    32   1012   1011   1010
    33   1013   1012   1011
    34   1014   1013   1012
    35   1015   1014   1013
    36   1016   1015   1014
    37   1017   1016   1015
    38   1018   1017   1016
    39   1019   1018   1017


    print(df2.to_string())
        col_0  col_1  col_2  col_3  col_4  col_5
    0       0      1      2      3      4      5
    6       6      7      8      9     10     11
    12     12     13     14     15     16     17
    18     18     19   1000   1001   1002   1003
    24   1004   1005   1006   1007   1008   1009
    30   1010   1011   1012   1013   1014   1015
    36   1016   1017   1018   1019      0      1

    """
    new_column_name = "col"
    df, _ = series_to_dataframe(dframe)
    colum_name = df.columns[0]
    howoften = number_of_cells_to_join
    toadd = howoften + how_many_to_add_until_even(n1=len(df), n2=howoften)
    if negative is True:
        nega = -1
        df2 = pd.concat([df.copy(), df[:toadd].copy()])
    else:
        nega = 1
        df2 = pd.concat([df[-1 * toadd :].copy(), df.copy()])
    df3 = pd.DataFrame(
        map(
            lambda x: (pd.Series(eval(f"{x}[{nu}]") for nu in range(howoften))),
            zip(
                df2[colum_name],
                *[
                    df2[colum_name].shift(_ * nega).fillna(0)
                    for _ in range(1, howoften + 1)
                ],
            ),
        ),
        index=df2.index,
    )
    df3.columns = [f"{new_column_name}_{x}" for x in df3.columns]
    for col in df3.columns:
        try:
            df3[col] = df3[col].astype(df[colum_name].dtype)
        except Exception as fea:
            pass
    if negative is True:
        df4 = df3[: toadd * -1].copy()
    else:
        df4 = df3[toadd:].copy()
    if drop_redundant:
        return df4[df4.index % number_of_cells_to_join == 0]
    return df4


def pd_add_vertical_to_horizontal():
    Series.s_vertical_to_horizontal = pd_vertical_to_horizontal





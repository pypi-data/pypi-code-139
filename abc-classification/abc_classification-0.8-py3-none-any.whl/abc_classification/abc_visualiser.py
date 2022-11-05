"""File contains functions for plotting."""
from typing import Optional
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter


def pareto_chart(data: pd.DataFrame,
                 values: str, labels: str,
                 title: Optional[str] = 'Pareto chart') -> None:
    """Plots pareto chart.

    Args:
        data (pd.DataFrame): abc classified dataframe.
        values (str): column of data containing values.
        labels (str): column of data containing labels.
        title (str, optional): title of plot. Defaults to 'Pareto chart'."""
    data = data.copy()
    data["cumulative_percentage"] = data[values].cumsum() / data[values].sum() * 100
    _, values_axis = plt.subplots()
    plt.xticks(rotation=25)
    plt.title(title)
    values_axis.bar(data[labels], data[values])
    cumulative_percentage_axis = values_axis.twinx()
    cumulative_percentage_axis.plot(data[labels],
                                    data["cumulative_percentage"],
                                    color="C1", marker="D", ms=7)
    cumulative_percentage_axis.yaxis.set_major_formatter(PercentFormatter())

    values_axis.tick_params(axis="y", colors="C0")
    cumulative_percentage_axis.tick_params(axis="y", colors="C1")
    plt.show()

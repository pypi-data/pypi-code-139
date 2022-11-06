import numpy as np
import pandas as pd

def get_best_combinations(series_1, series_2):
    output_dict = {}
    data_tabular = pd.crosstab(series_1, series_2)
    for _ in range(data_tabular.shape[0]):
        best_idx_col = data_tabular.stack().index[np.argmax(data_tabular.values)]
        output_dict[best_idx_col[1]] = best_idx_col[0]
        data_tabular = data_tabular.drop(best_idx_col[0], axis=0).drop(best_idx_col[1], axis=1)
    return output_dict
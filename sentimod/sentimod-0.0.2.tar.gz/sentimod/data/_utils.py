import numpy as np
import pandas as pd
import os
import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.rc("axes", labelsize=14)
mpl.rc("xtick", labelsize=12)
mpl.rc("ytick", labelsize=12)

# Where to save the figures
PROJECT_ROOT_DIR = "."
CHAPTER_ID = "end_to_end_project"
IMAGES_PATH = os.path.join(PROJECT_ROOT_DIR, "images", CHAPTER_ID)
os.makedirs(IMAGES_PATH, exist_ok=True)


def save_fig(fig_id, tight_layout=True, fig_extension="png", resolution=300) -> None:
    """save figures

    Args:
        fig_id (_type_): __
        tight_layout (bool, optional): __. Defaults to True.
        fig_extension (str, optional): __. Defaults to "png".
        resolution (int, optional): __. Defaults to 300.
    """
    path = os.path.join(IMAGES_PATH, fig_id + "." + fig_extension)
    print("Saving figure", fig_id)
    if tight_layout:
        plt.tight_layout()
    plt.savefig(path, format=fig_extension, dpi=resolution)


def split_train_test(data: pd.DataFrame, test_ratio: float) -> pd.DataFrame:
    """split train and test data

    Args:
        data (pd.DataFrame): __
        test_ratio (float): __

    Returns:
        pd.DataFrame: train, test
    """
    shuffled_indices = np.random.permutation(len(data))
    test_set_size = int(len(data) * test_ratio)
    test_indices = shuffled_indices[:test_set_size]
    train_indices = shuffled_indices[test_set_size:]

    return data.iloc[train_indices], data.iloc[test_indices]

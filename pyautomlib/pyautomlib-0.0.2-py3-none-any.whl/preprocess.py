import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neighbors import LocalOutlierFactor
from sklearn.decomposition import PCA
from sklearn.preprocessing import LabelEncoder
from .config import PreprocessModel


class DataProcessor:
    def __init__(
            self, data_frame: pd.DataFrame, config: PreprocessModel, target_col=None
    ):
        self.config = config
        self.data_frame = data_frame
        self.target_col = target_col

    def summary(self):
        num_of_hashtag = 40
        print("#" * num_of_hashtag, "Data Summary", "#" * num_of_hashtag, end="\n\n")

        print("#" * num_of_hashtag, "Describe", "#" * num_of_hashtag)
        print(self.data_frame.describe().T, end="\n\n")

        print("#" * num_of_hashtag, "Head", "#" * num_of_hashtag)
        print(self.data_frame.head(), end="\n\n")

        print("#" * num_of_hashtag, "Columns", "#" * num_of_hashtag)
        cat_cols, _, _ = self.grab_col_names(summary=True)

        print("#" * num_of_hashtag, "Correlations", "#" * num_of_hashtag)
        print(self.data_frame.corr(), end="\n\n")
        na_cols = [
            col
            for col in self.data_frame.columns
            if self.data_frame[col].isnull().sum() > 0
        ]
        if len(na_cols) > 0:
            print("#" * num_of_hashtag, "Nan Value Summary", "#" * num_of_hashtag)
            for col in na_cols:
                print(col, self.data_frame[col].isnull().sum())

            if self.target_col is not None:
                self.missing_vs_target(na_cols)

        if self.target_col is not None:
            print("#" * num_of_hashtag, "Rare Analysis", "#" * num_of_hashtag)
            self.rare_analyser(cat_cols)

    def missing_vs_target(self, na_columns):
        temp_df = self.data_frame.copy()

        for col in na_columns:
            temp_df[col + "_NA_FLAG"] = np.where(temp_df[col].isnull(), 1, 0)

        na_flags = temp_df.loc[:, temp_df.columns.str.contains("_NA_")].columns

        for col in na_flags:
            print(
                pd.DataFrame(
                    {
                        "TARGET_MEAN": temp_df.groupby(col)[self.target_col].mean(),
                        "Count": temp_df.groupby(col)[self.target_col].count(),
                    }
                ),
                end="\n\n\n",
            )

    def grab_col_names(self, data_frame, summary=False):
        # cat_cols, cat_but_car
        cat_th = self.config.categorical_threshold
        car_th = self.config.cardinal_threshold
        all_columns = data_frame.columns
        cat_cols = [col for col in all_columns if data_frame[col].dtypes == "O"]
        num_but_cat = [
            col
            for col in all_columns
            if data_frame[col].nunique() < cat_th
               and data_frame[col].dtypes != "O"
        ]
        cat_but_car = [
            col
            for col in all_columns
            if data_frame[col].nunique() > car_th
               and data_frame[col].dtypes == "O"
        ]
        cat_cols = cat_cols + num_but_cat
        cat_cols = [col for col in cat_cols if col not in cat_but_car]

        # num_cols
        num_cols = [col for col in all_columns if data_frame[col].dtypes != "O"]
        num_cols = [col for col in num_cols if col not in num_but_cat]

        if summary:
            print(f"Observations: {data_frame.shape[0]}")
            print(f"Variables: {data_frame.shape[1]}")
            print(f"cat_cols: {len(cat_cols)}")
            print(f"num_cols: {len(num_cols)}")
            print(f"cat_but_car: {len(cat_but_car)}")
            print(f"num_but_cat: {len(num_but_cat)}")

        return cat_cols, num_cols, cat_but_car

    def scale(self, num_cols):
        self.scaler = self.config.scaler()
        self.data_frame[num_cols] = self.scaler.fit_transform(self.data_frame[num_cols])
        return self.data_frame

    def handle_outliers(self):
        # Should be run after encoding
        df = self.data_frame.copy()
        clf = LocalOutlierFactor(n_neighbors=20)
        clf.fit_predict(df)
        df_scores = clf.negative_outlier_factor_
        diff2 = np.diff(np.sort(df_scores), 2)
        th = df_scores[np.argmax(np.abs(diff2)) + 2]

        df.drop(axis=0, labels=df[df_scores < th].index, inplace=True)

        return df

    def handle_missing(self):
        df = self.data_frame.copy()
        if self.config.missing_handling_method == "delete":
            df.dropna(inplace=True)
        elif self.config.missing_handling_method == "mean":
            df.fillna(df.mean(), inplace=True)
        elif self.config.missing_handling_method == "median":
            df.fillna(df.median(), inplace=True)
        return df

    def encode(self, cat_cols):
        df = self.data_frame.copy()
        if self.config.label_encode:
            self.label_encoder = LabelEncoder()
            df[self.target_col] = self.label_encoder.fit_transform(df[self.target_col])

        if self.config.one_hot_encode:
            non_target_cat_cols = [col for col in cat_cols if col != self.target_col]
            df = pd.get_dummies(df, columns=non_target_cat_cols, drop_first=True)

        return df

    def handle_PCA(self, num_cols):
        pca_cols = [col for col in num_cols if col != self.target_col]
        others = [col for col in self.data_frame.columns if col not in num_cols]
        pca = PCA()
        pca.fit_transform(self.data_frame[pca_cols])
        vairances = np.cumsum(pca.explained_variance_ratio_)
        self.optimum_comp = np.argmax(vairances > 0.90) + 1

        self.pca = PCA(n_components=self.optimum_comp)
        pca_fit = self.pca.fit_transform(self.data_frame)

        pca_df = pd.DataFrame(
            pca_fit, columns=[f"PC{i + 1}" for i in range(self.optimum_comp)]
        )
        final_df = pd.concat([pca_df, self.data_frame[others]], axis=1)
        return final_df

    def rare_analyser(self, cat_cols):

        for col in cat_cols:
            print(col, ":", len(self.data_frame[col].value_counts()))
            print(
                pd.DataFrame(
                    {
                        "COUNT": self.data_frame[col].value_counts(),
                        "RATIO": self.data_frame[col].value_counts()
                                 / len(self.data_frame),
                        "TARGET_MEAN": self.data_frame.groupby(col)[
                            self.target_col
                        ].mean(),
                    }
                ),
                end="\n\n\n",
            )

    def process_data(self):
        cat_cols, num_cols, cat_but_car = self.grab_col_names(self.data_frame)
        if self.config.drop_cardinals:
            self.data_frame.drop(cat_but_car, axis=1, inplace=True)
        if self.config.handle_missing:
            self.data_frame = self.handle_missing()
        if self.config.label_encode or self.config.one_hot_encode:
            self.data_frame = self.encode(cat_cols)
        if self.config.remove_outliers:
            self.data_frame = self.handle_outliers()
        if self.config.scale:
            self.data_frame = self.scale(num_cols)
        if self.config.perform_PCA:
            self.data_frame = self.handle_PCA(num_cols)

        return self.data_frame

    def process_as_previous(self, df):
        cat_cols, num_cols, _ = self.grab_col_names(df)

        if self.config.label_encode and self.target_col in df.columns:
            df[self.target_col] = self.label_encoder.transform(df[self.target_col])

        if self.config.one_hot_encode:
            non_target_cat_cols = [col for col in cat_cols if col != self.target_col]
            df = pd.get_dummies(df, columns=non_target_cat_cols, drop_first=True)

        if self.config.scale:
            df[num_cols] = self.scaler.transform(df[num_cols])

        if self.config.perform_PCA:
            others = [col for col in df.columns if col not in num_cols]
            pca_fit = self.pca.transform(df)
            pca_df = pd.DataFrame(
                pca_fit, columns=[f"PC{i + 1}" for i in range(self.optimum_comp)]
            )
            df = pd.concat([pca_df, df[others]], axis=1)

        return df

    def split_data(self):
        test_size = self.config.test_size
        X = self.data_frame.drop(self.target_col, axis=1)
        y = self.data_frame[self.target_col]
        x_train, x_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42
        )

        return x_train, x_test, y_train, y_test

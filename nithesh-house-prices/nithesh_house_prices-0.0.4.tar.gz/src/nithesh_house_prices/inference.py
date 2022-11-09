import pandas as pd
import joblib
import numpy as np
import warnings
warnings.filterwarnings('ignore')


def make_predictions(input_data: pd.DataFrame) -> np.ndarray:
    df = input_data[[
        'OverallQual',
        'GrLivArea',
        'GarageCars',
        'GarageArea',
        'TotalBsmtSF',
        'GarageFinish',
        'GarageType',
        'SaleCondition'
    ]]
    df = df.dropna(axis=0)

    # Preprocessing and Feature Engineering on this data
    numerical_columns = [
        cname for cname in df.columns if df[cname].dtype in [
            'int64', 'float64'
        ]
    ]
    categorical_columns = [
        cname for cname in df.columns if df[cname].dtype == "object"
    ]

    # Loading the scaler and encoder
    scaler = joblib.load('scaler.joblib')
    encoder = joblib.load('encoder.joblib')

    df_scaled = scaler.transform(df[numerical_columns])
    df_scaled = pd.DataFrame(df_scaled, columns=numerical_columns)

    df_encoded = encoder.transform(df[categorical_columns])
    df_encoded = pd.DataFrame(
        df_encoded, columns=encoder.get_feature_names(
            categorical_columns
        )
    )

    df = pd.concat([df_scaled, df_encoded], axis=1)

    # Predicting the SalePrice for df using the model
    model = joblib.load('model.joblib')
    y_pred = model.predict(df)

    return y_pred

import joblib
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import StandardScaler
import pandas as pd


def preprocess(input_data: pd.DataFrame) -> pd.DataFrame:
    df = input_data[
        ['OverallQual',
         'GrLivArea',
         'GarageCars',
         'GarageArea',
         'TotalBsmtSF',
         'GarageFinish',
         'GarageType',
         'SaleCondition',
         'SalePrice']
    ]
    df = df.dropna(axis=0)
    target = df['SalePrice']
    df = df.drop('SalePrice', axis=1)
    numerical_columns = [
        cname for cname in df.columns if df[cname].dtype in [
            'int64', 'float64'
        ]
    ]
    categorical_columns = [
        cname for cname in df.columns if df[cname].dtype == "object"
    ]
    scaler = StandardScaler()
    encoder = OneHotEncoder(handle_unknown='ignore', sparse=False)
    scaler = scaler.fit(df[numerical_columns])
    df_scaled = scaler.transform(df[numerical_columns])
    df_scaled = pd.DataFrame(df_scaled, columns=numerical_columns)
    encoder = encoder.fit(df[categorical_columns])
    df_encoded = encoder.transform(df[categorical_columns])
    df_encoded = pd.DataFrame(
        df_encoded, columns=encoder.get_feature_names(categorical_columns)
    )
    df = pd.concat([df_scaled, df_encoded], axis=1)
    joblib.dump(scaler, 'scaler.joblib')
    joblib.dump(encoder, 'encoder.joblib')
    return df, target

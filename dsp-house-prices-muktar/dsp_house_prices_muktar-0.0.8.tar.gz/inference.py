from joblib import load
import pandas as pd
import numpy as np


def model_inference(input_master: pd.DataFrame):
    input_trimmed = input_master[['LotArea', 'YearBuilt', '1stFlrSF', '2ndFlrSF', 'FullBath', 'BedroomAbvGr', 'TotRmsAbvGrd', 'SaleCondition', 'Street']]
    encoder = load('../models/encoder.joblib')
    scaler = load('../models/scaler.joblib')
    enc = pd.DataFrame(encoder.transform(input_trimmed[['SaleCondition', 'Street']]))
    input_trimmed.drop(input_trimmed.loc[:, ['SaleCondition', 'Street']], inplace=True, axis=1)
    input_df = pd.concat([input_trimmed, enc], axis=1)
    input_df[['LotArea', '1stFlrSF', '2ndFlrSF']] = scaler.transform(input_df[['LotArea', '1stFlrSF', '2ndFlrSF']])
    model = load('../models/model.joblib')
    return model.predict(input_df)


def make_prediction(input_data: pd.DataFrame) -> np.ndarray:
    predictions = model_inference(input_data)
    print(predictions)

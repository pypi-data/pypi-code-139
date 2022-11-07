from sklearn.preprocessing import MinMaxScaler

def fit_transform(bundles):
    bundles['y'] = bundles['entry'].apply(lambda x: len(x))
    bundles[['y']] = MinMaxScaler().fit_transform(bundles[['y']])
    bundles['score'] = bundles['y'].apply(lambda x: int(x*100))
    bundles['group'] = bundles['score'].apply(lambda x: "pass" if x > 7 else "fail")
    return bundles
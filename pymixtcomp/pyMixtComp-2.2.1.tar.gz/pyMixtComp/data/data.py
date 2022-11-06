import pandas as pd
import pkg_resources


def load_iris():
    """ Iris data

    The iris data set gives the measurements in centimeters of the variables sepal length and width and petal length and width,
    respectively, for 50 flowers from each of 3 species of iris. The species are Iris setosa, versicolor, and virginica.

    Returns
    -------
    (DataFrame, dict)
        Data are returned in a dataFrame with 5 columns.
        Model is returned as a dict

    References
    ----------
    Fisher, R. A. (1936) The use of multiple measurements in taxonomic problems. Annals of Eugenics, 7, Part II, 179–188.

    The data were collected by Anderson, Edgar (1935). The irises of the Gaspe Peninsula, Bulletin of the American
    Iris Society, 59, 2–5.

    Examples
    --------
    >>> import pyMixtComp
    >>> data, model = pyMixtComp.data.load_iris()
    """
    stream = pkg_resources.resource_stream(__name__, "iris.csv")
    data = pd.read_csv(stream)
    model = {"sepal length (cm)": "Gaussian", "sepal width (cm)": "Gaussian",
             "petal length (cm)": "Gaussian", "petal width (cm)": "Gaussian"}

    return data, model


def load_drugs():
    """ Drugs data

    The data set contains various information that effect the predictions like Age, Sex, BP, Cholesterol levels, Na to Potassium Ratio and finally the drug type.

    Returns
    -------
    (DataFrame, dict)
        Data are returned in a dataFrame with 6 columns.
        Model is returned as a dict

    Notes
    -----
    data contains 200 records described by 6 mixed variables:
    - Age: Age of the Patient (Continuous)
    - Sex: Gender of the patients (Binary)
    - BP: Blood Pressure level of the patient (Categorical)
    - Cholesterol: Cholesterol Levels (Binary)
    - Na_to_K: Sodium to potassium Ration in Blood (Continuous)
    - Drug: Drug Type (Categorical)

    References
    ----------
    https://www.kaggle.com/datasets/prathamtripathi/drug-classification

    Examples
    --------
    >>> import pyMixtComp
    >>> data, model = pyMixtComp.data.load_drugs()
    """
    stream = pkg_resources.resource_stream(__name__, "drug200.csv")
    data = pd.read_csv(stream)
    model = {"Age": "Gaussian", "Sex": "Multinomial",
             "BP": "Multinomial", "Cholesterol": "Multinomial",
             "Na_to_K": "Gaussian"}

    return data, model


def load_stars():
    """ Galaxy stars dataset

    NASA provides a tabular dataset of different features for stars that can be used to classify its type. The dataset contains 240 records and 7 features. The features are:

    Returns
    -------
    (DataFrame, dict)
        Data are returned in a dataFrame with 7 columns.
        Model is returned as a dict

    Notes
    -----
    data contains 200 records described by 7 mixed variables:
    - Temperature: Surface temperature in Kelvin (K) (Continuous)
    - L: Relative Luminosity (Continuous)
    - R: Relative Radius (Continuous)
    - A_M: Absolute Magnitude (Continuous)
    - Color: Star color (Categorical)
    - Spectral_Class: SMASS Spec Class (Categorical)
    - Type: Star Type (Categorical)

    References
    ----------
    https://www.kaggle.com/datasets/brsdincer/star-type-classification

    Examples
    --------
    >>> import pyMixtComp
    >>> data, model = pyMixtComp.data.load_stars()
    """
    stream = pkg_resources.resource_stream(__name__, "stars.csv")
    data = pd.read_csv(stream)
    model = {"Temperature": "Poisson", "L": "Poisson",
             "R": "Poisson", "A_M": "Poisson",
             "Color": "Poisson", "Spectral_Class": "Poisson"}

    return data, model

def load_titanic():
    """ Titanic Disaster Dataset

    The original Titanic dataset, describing the survival status of individual passengers on the Titanic. The titanic data does not contain information from the crew, but it does contain actual ages of half of the passengers. The principal source for data about Titanic passengers is the Encyclopedia Titanica. The datasets used here were begun by a variety of researchers. One of the original sources is Eaton & Haas (1994) Titanic: Triumph and Tragedy, Patrick Stephens Ltd, which includes a passenger list created by many researchers and edited by Michael A. Findlay.

    Thomas Cason of UVa has greatly updated and improved the titanic data frame using the Encyclopedia Titanica and created the dataset here. Some duplicate passengers have been dropped, many errors corrected, many missing ages filled in, and new variables created.

    For more information about how this dataset was constructed: http://biostat.mc.vanderbilt.edu/wiki/pub/Main/DataSets/titanic3info.txt

    Returns
    -------
    (DataFrame, dict)
        Data are returned in a dataFrame with 10 columns.
        Model is returned as a dict

    Notes
    -----
    data contains 1303 records described by 10 mixed variables:
    - Class: Passenger Class (Categorical)
    - Survived: Survival (Binary)
    - Sex: Sex (Binary)
    - Title: Title (Categorical)
    - Family_Size: Number of family size of the passenger (Continuous)
    - Age: Age (Continuous)
    - Fare: Passenger Fare (Continuous)
    - Cabin: Cabin (Binary)
    - Embarkation_Port: Port of Embarkation (Categorical)
    - Boat: Lifeboat (Binary)


    References
    ----------
    https://www.kaggle.com/datasets/vinicius150987/titanic3

    Examples
    --------
    >>> import pyMixtComp
    >>> data, model = pyMixtComp.data.load_titanic()
    """
    stream = pkg_resources.resource_stream(__name__, "titanic_clean.csv")
    data = pd.read_csv(stream)
    model = {
        "Class": "Multinomial", "Sex": "Multinomial",
        "Title": "Multinomial", "Family_Size": "Poisson", "Age": "Gaussian",
        "Fare": "Gaussian", "Cabin": "Multinomial",
        "Embarkation_Port": "Multinomial", "Boat": "Multinomial"
    }

    return data, model


def load_purchasing_behavior():
    """ Purchasing-behavior

    The dataset consists of information about the purchasing behavior of 2,000 individuals from a given area when entering a physical 'FMCG' store. All data has been collected through the loyalty cards they use at checkout. The data has been preprocessed and there are no missing values. In addition, the volume of the dataset has been restricted and anonymized to protect the privacy of the customers. 										
    
    Returns
    -------
    (DataFrame, dict)
        Data are returned in a dataFrame with 7 columns.
        Model is returned as a dict

    Notes
    -----
    data contains 2,000 records described by 7 mixed variables:
    - Sex: Biological sex (gender) of a customer. In this dataset there are only 2 different options. (Binary)
    - Marital status: Marital status of a customer. (Binary)
    - Age: The age of the customer in years, calculated as current year minus the year of birth of the customer at the time of creation of the dataset (Continuous)
    - Education: Level of education of the customer (Categorical)
    - Income: Self-reported annual income in US dollars of the customer. (Continuous)
    - Occupation: Category of occupation of the customer. (Categorical)
    - Settlement size: The size of the city that the customer lives in. (Categorical)

    References
    ----------
    https://www.kaggle.com/code/dev0914sharma/customer-clustering-model/data

    Examples
    --------
    >>> import pyMixtComp
    >>> data, model = pyMixtComp.data.load_purchasing_behavior()
    """
    stream = pkg_resources.resource_stream(__name__, "purchasing_behaviour.csv")
    data = pd.read_csv(stream, dtype=object, index_col='ID')
    model = {"Sex": "Multinomial", "Marital status": "Multinomial", "Age": "Gaussian", "Education": "Multinomial",
             "Income": "Gaussian", "Occupation": "Multinomial", "Settlement size": "Multinomial"}

    return data, model


def load_demographic():
    """ Household-level transactions

    This dataset contains household level transactions over two years from a group of 2,500 households who are frequent shoppers at a retailer. It contains all of each household’s purchases, not just those from a limited number of categories. For certain households, demographic information as well as direct marketing contact history are included.

    Due to the number of tables and the overall complexity of The Complete Journey, it is suggested that this database be used in more advanced classroom settings. Further, The Complete Journey would be ideal for academic research as it should enable one to study the effects of direct marketing to customers.
    
    Returns
    -------
    (DataFrame, dict)
        Data are returned in a dataFrame with 7 columns.
        Model is returned as a dict

    Notes
    -----
    data contains 801 records described by 7 mixed variables:
    - AGE_DESC: Age description (Categorical)
    - MARITAL_STATUS_CODE: Marital status (Categorical)
    - INCOME_DESC: Income description (Categorical)
    - HOMEOWNER_DESC: Home owner or not (Binary)
    - HH_COMP_DESC: Individual description (Categorical)
    - HOUSEHOLD_SIZE_DESC: Household size (Categorical)
    - KID_CATEGORY_DESC: How many kinds? (Categorical)

    References
    ----------
    https://www.kaggle.com/datasets/frtgnn/dunnhumby-the-complete-journey?select=hh_demographic.csv

    Examples
    --------
    >>> import pyMixtComp
    >>> data, model = pyMixtComp.data.load_demographic()
    """
    stream = pkg_resources.resource_stream(__name__, "housing.csv")
    data = pd.read_csv(stream, dtype=object, index_col='household_key')
    model = {"AGE_DESC": "Multinomial", "MARITAL_STATUS_CODE": "Multinomial", "INCOME_DESC": "Multinomial", "HOMEOWNER_DESC": "Multinomial",
             "HH_COMP_DESC": "Multinomial", "HOUSEHOLD_SIZE_DESC": "Multinomial", "KID_CATEGORY_DESC": "Multinomial"}

    return data, model


def load_candy():
    """ Halloween Candy Data

    It includes attributes for each candy along with its ranking. For binary variables, 1 means yes, 0 means no. This data set was obtained from Kaggle
    
    Returns
    -------
    (DataFrame, dict)
        Data are returned in a dataFrame with 12 columns.
        Model is returned as a dict

    Notes
    -----
    data contains 85 records described by 12 mixed variables:
    - chocolate: Does it contain chocolate? (Binary)
    - fruity: Is it fruit flavored? (Binary)
    - caramel: Is there caramel in the candy? (Binary)
    - peanutalmondy: Does it contain peanuts, peanut butter or almonds? (Binary)
    - nougat: Does it contain nougat? (Binary)
    - crispedricewafer: Does it contain crisped rice, wafers, or a cookie component? (Binary)
    - hard: Is it a hard candy? (Binary)
    - bar: Is it a candy bar? (Binary)
    - pluribus: Is it one of many candies in a bag or box? (Binary)
    - sugarpercent: The percentile of sugar it falls under within the data set. (Continuous)
    - pricepercent: The unit price percentile compared to the rest of the set. (Continuous)
    - winpercent: The overall win percentage according to 269,000 matchup. (Continuous)

    References
    ----------
    https://www.kaggle.com/code/jonathanbouchet/candies-data-visualization-clustering/data

    Examples
    --------
    >>> import pyMixtComp
    >>> data, model = pyMixtComp.data.load_candy()
    """
    stream = pkg_resources.resource_stream(__name__, "candy.csv")
    data = pd.read_csv(stream, dtype=object, index_col='competitorname')
    model = {"chocolate": "Multinomial", "fruity": "Multinomial", "caramel": "Multinomial", "peanutalmondy": "Multinomial",
             "nougat": "Multinomial", "crispedricewafer": "Multinomial", "hard": "Multinomial", "bar": "Multinomial",
             "pluribus": "Multinomial", "sugarpercent": "Gaussian", "pricepercent": "Gaussian", "winpercent": "Gaussian"}

    return data, model



def load_wine():
    """ Wine Quality Data Set

    This datasets is related to red variants of the Portuguese "Vinho Verde" wine. For more details, consult the reference [Cortez et al., 2009]. Due to privacy and logistic issues, only physicochemical (inputs) and sensory (the output) variables are available (e.g. there is no data about grape types, wine brand, wine selling price, etc.).

    The datasets can be viewed as classification or regression tasks. The classes are ordered and not balanced (e.g. there are much more normal wines than excellent or poor ones).

    This dataset is also available from the UCI machine learning repository, https://archive.ics.uci.edu/ml/datasets/wine+quality , I just shared it to kaggle for convenience. (If I am mistaken and the public license type disallowed me from doing so, I will take this down if requested.)

    Returns
    -------
    (DataFrame, dict)
        Data are returned in a dataFrame with 12 columns (see Notes).
        Model is returned as a dict

    Notes
    -----
    data contains 1599 individuals described by 12 mixed variables:
    - fixed acidity: most acids involved with wine or fixed or nonvolatile (do not evaporate readily)
    - volatile acidity: the amount of acetic acid in wine, which at too high of levels can lead to an unpleasant, vinegar taste
    - citric acid: found in small quantities, citric acid can add 'freshness' and flavor to wines
    - residual sugar: the amount of sugar remaining after fermentation stops, it's rare to find wines with less than 1 gram/liter and wines with greater than 45 grams/liter are considered sweet
    - chlorides: the amount of salt in the wine
    - free sulfur dioxide: the free form of SO2 exists in equilibrium between molecular SO2 (as a dissolved gas) and bisulfite ion; it prevents microbial growth and the oxidation of wine
    - total sulfur dioxide: amount of free and bound forms of S02; in low concentrations, SO2 is mostly undetectable in wine, but at free SO2 concentrations over 50 ppm, SO2 becomes evident in the nose and taste of wine
    - density: the density of water is close to that of water depending on the percent alcohol and sugar content
    - pH: describes how acidic or basic a wine is on a scale from 0 (very acidic) to 14 (very basic)
    - sulphates: a wine additive which can contribute to sulfur dioxide gas (S02) levels, wich acts as an antimicrobial and antioxidant
    - alcohol: the percent alcohol content of the wine
    - quality: output variable (based on sensory data, score between 0 and 10)

    References
    ----------
    P. Cortez, A. Cerdeira, F. Almeida, T. Matos and J. Reis. Modeling wine preferences by data mining from physicochemical properties. In Decision Support Systems, Elsevier, 47(4):547-553, 2009.
    P. Cortez, A. Cerdeira, F. Almeida, T. Matos and J. Reis. Modeling wine preferences by data mining from physicochemical properties. In Decision Support Systems, Elsevier, 47(4):547-553, 2009.

    Examples
    --------
    >>> import pyMixtComp
    >>> data, model = pyMixtComp.data.load_wine()
    """
    stream = pkg_resources.resource_stream(__name__, "wine.csv")
    data = pd.read_csv(stream, dtype=object)
    model = {"fixed acidity": "Gaussian", "volatile acidity": "Gaussian", "citric acid": "Gaussian", "residual sugar": "Gaussian",
             "chlorides": "Gaussian", "free sulfur dioxide": "Gaussian", "total sulfur dioxide": "Gaussian", "density": "Gaussian",
             "pH": "Gaussian", "sulphates": "Gaussian", "alcohol": "Gaussian"}

    return data, model


def load_prostate():
    """ Prostate cancer data

    This data set was obtained from a randomized clinical trial comparing four treatments for n = 506 patients
    with prostatic cancer grouped on clinical criteria into two Stages 3 and 4 of the disease.

    Returns
    -------
    (DataFrame, dict)
        Data are returned in a dataFrame with 12 columns (see Notes).
        Model is returned as a dict

    Notes
    -----
    data contains 506 individuals described by 12 mixed variables:
    - Age: Age (Continuous)
    - HG: Index of tumour stage and histolic grade (Continuous)
    - Wt: Weight (Continuous)
    - AP: Serum prostatic acid phosphatase C (Continuous)
    - BP: Systolic blood pressure (Continuous)
    - PF: Performance rating (Categorical)
    - DBP: Diastolic blood pressure (Continuous)
    - HX: Cardiovascular disease history (Categorical)
    - SG: Serum haemoglobin (Continuous)
    - BM: Bone metastasis (Categorical)
    - SZ: Size of primary tumour (Continuous)
    - EKG: Electrocardiogram code (Categorical)

    References
    ----------
    Yakovlev, Goot and Osipova (1994), The choice of cancer treatment based on covariate information. Statist. Med.,
    13: 1575-1581. doi:10.1002/sim.4780131508

    Examples
    --------
    >>> import pyMixtComp
    >>> data, model = pyMixtComp.data.load_prostate()
    """
    stream = pkg_resources.resource_stream(__name__, "prostate.csv")
    data = pd.read_csv(stream, dtype=object)
    model = {"Age": "Gaussian", "Wt": "Gaussian", "PF": "Multinomial", "HX": "Multinomial",
             "SBP": "Gaussian", "DBP": "Gaussian", "EKG": "Multinomial", "HG": "Gaussian",
             "SZ": "Gaussian", "SG": "Gaussian", "AP": "Gaussian", "BM": "Multinomial"}

    return data, model


def load_simulated_data():
    """ Simulated data

    Data simulated from the different models used in MixtComp.

    Returns
    -------
    (DataFrame, dict)
        Data are returned in a dataFrame with 9 columns: one for each model in pyMixtComp and the true labels (z_class).
        Model is returned as a dict (z_class is not included but can be added to perform supervised clustering).

    Examples
    --------
    >>> import pyMixtComp
    >>> data, model = pyMixtComp.data.load_prostate()
    """
    stream = pkg_resources.resource_stream(__name__, "simulated_data.csv")
    data = pd.read_csv(stream, dtype=object)
    model = {"Poisson1": "Poisson", "Gaussian1": "Gaussian", "Categorical1": "Multinomial",
             "nBinom1": "NegativeBinomial", "Weibull1": "Weibull",
             "Functional1": {"type": "Func_CS", "paramStr": "nSub: 2, nCoeff: 2"},
             "FunctionalSharedAlpha1": {"type": "Func_SharedAlpha_CS", "paramStr": "nSub: 2, nCoeff: 2"},
             "Rank1": "Rank_ISR"}

    return data, model


def load_canadian_weather():
    """ Canadian average annual weather cycle

    Daily temperature and precipitation at 35 different locations in Canada averaged over 1960 to 1994.
    Data from fda R package.

    Returns
    -------
    DataFrame, dict
        Data are returned in a dataFrame with 2 columns: tempav (average temperature in degrees celsius
        for each day of the year) and precav (average rainfall in millimetres for each day of the year).
        Model is returned as a dict

    References
    ----------
    - Ramsay, James O., and Silverman, Bernard W. (2006), Functional Data Analysis, 2nd ed., Springer, New York.
    - Ramsay, James O., and Silverman, Bernard W. (2002), Applied Functional Data Analysis, Springer, New York

    Examples
    --------
    >>> import pyMixtComp
    >>> data, model = pyMixtComp.data.load_canadian_weather()
    """
    stream = pkg_resources.resource_stream(__name__, "canadian_weather.csv")
    data = pd.read_csv(stream, dtype=object)
    model = {"tempav": {"type": "Func_CS", "paramStr": "nSub: 4, nCoeff: 2"},
             "precav": {"type": "Func_CS", "paramStr": "nSub: 4, nCoeff: 2"}}

    return data, model

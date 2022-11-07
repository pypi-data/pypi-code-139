def assign1():
    ans='''#Importing the required libraries\nimport pandas as pd\nimport numpy as np\nimport seaborn as sns\nimport matplotlib.pyplot as plt\ndf  = pd.read_csv('uber.csv')\ndf.pickup_datetime = pd.to_datetime(df.pickup_datetime, errors='coerce')\nfrom sklearn.model_selection import train_test_split X_train,X_test,y_train,y_test = train_test_split(x,y,test_size = 0.33)\nfrom sklearn.linear_model import LinearRegression\nregression = LinearRegression()\nregression.fit(X_train,y_train)\nprediction = regression.predict(X_test)\nprint(prediction)\ny_test\nfrom sklearn.metrics import r2_score \nr2_score(y_test,prediction)'''

    return ans




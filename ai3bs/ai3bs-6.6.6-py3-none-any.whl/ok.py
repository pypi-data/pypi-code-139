def ok():
    print("""

import pandas as pd
from sklearn import tree
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.externals.six import StringIO

data = pd.read_csv('tennisdata.csv')
print("The first 5 values of data is \n",data.head())

X = data.iloc[:,:-1]
print("\nThe first 5 values of Train data is \n",X.head())
y = data.iloc[:,-1]
print("\nThe first 5 values of Train output is \n",y.head())

le_outlook = LabelEncoder()
X.Outlook =  le_outlook.fit_transform(X.Outlook)
le_Temperature = LabelEncoder()
X.Temperature =  le_Temperature.fit_transform(X.Temperature)
le_Humidity = LabelEncoder()
X.Humidity =  le_Humidity.fit_transform(X.Humidity)
le_Windy = LabelEncoder()
X.Windy =  le_Windy.fit_transform(X.Windy)

print("\nNow the Train data is",X.head())

le_PlayTennis = LabelEncoder()
y =  le_PlayTennis.fit_transform(y)
print("\nNow the Train data is\n",y)

classifier = DecisionTreeClassifier()
classifier.fit(X,y)

def labelEncoderForInput(list1):
    list1[0] =  le_outlook.transform([list1[0]])[0]
    list1[1] =  le_Temperature.transform([list1[1]])[0]
    list1[2] =  le_Humidity.transform([list1[2]])[0]
    list1[3] =  le_Windy.transform([list1[3]])[0]
    return [list1]

inp = ["Rainy","Mild","High","False"]
inp1=["Rainy","Cool","High","False"]
pred1 = labelEncoderForInput(inp1)
y_pred = classifier.predict(pred1)
y_pred
print("\nfor input {0}, we obtain {1}".format(inp1, le_PlayTennis.inverse_transform(y_pred[0])))

    """)
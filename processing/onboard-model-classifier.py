import os
from sklearn import datasets
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import pandas as pd
import pickle

df = pd.read_csv(os.path.dirname(__file__)+'/iris.csv' )

X = df.drop(['variety'],axis=1).values
yLower = df['variety'].map(lambda x: x.lower())
y = yLower.values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

logistic = LogisticRegression(max_iter=10000)

logistic.fit(X_train, y_train)

with open('services/api/model_pkl', 'wb') as files:
    pickle.dump(logistic, files)

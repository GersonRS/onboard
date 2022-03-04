from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import pandas as pd
import pickle

from processing.constants import PROJECT_DIR

df = pd.read_csv(str(PROJECT_DIR) + "/data/iris.csv" )

X = df.drop(['variety'],axis=1).values
yLower = df['variety'].map(lambda x: x.lower())
y = yLower.values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

logistic = LogisticRegression(max_iter=10000)

logistic.fit(X_train, y_train)

with open('model_pkl', 'wb') as files:
    pickle.dump(logistic, files)

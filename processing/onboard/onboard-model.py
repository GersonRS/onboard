from datetime import datetime
import os
import hashlib

import mlflow
import mlflow.sklearn
import numpy as np
from sklearn import datasets
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (classification_report, mean_absolute_error,
                             mean_squared_error, r2_score)
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

os.environ["AWS_DEFAULT_REGION"] = "eu-west-3"
os.environ["AWS_REGION"] = "eu-west-3"
os.environ["AWS_ACCESS_KEY_ID"] = "admin"
os.environ["AWS_SECRET_ACCESS_KEY"] = "adminadmin"
os.environ["MLFLOW_S3_ENDPOINT_URL"] = "http://localhost:9020"

mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("Default")

tags = {
    "Projeto": "Onboard",
    "team": "Data Science",
    "dataset": "iris",
    "release.version": "0.1.0"
}


def eval_metrics(actual, pred):
    mse = mean_squared_error(actual, pred)
    rmse = np.sqrt(mean_squared_error(actual, pred))
    mae = mean_absolute_error(actual, pred)
    r2 = r2_score(actual, pred)
    return mse, rmse, mae, r2


iris = datasets.load_iris()
x = iris.data[:, 2:]
y = iris.target
X_train, X_test, y_train, y_test = train_test_split(
    x, y, test_size=0.33, random_state=101)

with mlflow.start_run(run_name="Onboard - Iris RF Experiment") as run:
    mlflow.set_tags(tags)

    # clf = make_pipeline(
    #     StandardScaler(),
    #     GridSearchCV(
    #         LogisticRegression(penalty='l2', max_iter=10000, tol=0.1),
    #         param_grid={'C': np.logspace(-3, 3, 50)},
    #         cv=2,
    #         refit=True
    #     )
    # )

    scaler = StandardScaler()

    logistic = LogisticRegression(max_iter=10000, tol=0.1)
    pipe = Pipeline(steps=[("scaler", scaler), ("logistic", logistic)])

    param_grid = {
        "logistic__C": np.logspace(-4, 4, 100),
    }
    clf = GridSearchCV(pipe, param_grid, n_jobs=2, refit=True)

    clf.fit(X_train, y_train)

    print("Best parameter (CV score=%0.3f):" % clf.best_score_)
    print("Best value for C=%s):" % clf.best_params_["logistic__C"])

    predicted_qualities = clf.predict(X_test)

    (mse, rmse, mae, r2) = eval_metrics(y_test, predicted_qualities)

    print("  MSE: %s" % mse)
    print("  RMSE: %s" % rmse)
    print("  MAE: %s" % mae)
    print("  R2: %s" % r2)
    

    print(classification_report(y_test, predicted_qualities))

    mlflow.log_param("C", clf.best_params_["logistic__C"])
    mlflow.log_param("max_iter", 10000)
    mlflow.log_param("penalty", "l2")
    mlflow.log_metric("mse", mse)
    mlflow.log_metric("rmse", rmse)
    mlflow.log_metric("r2", r2)
    mlflow.log_metric("mae", mae)
    mlflow.log_metric("score", clf.best_score_)

    mlflow.sklearn.log_model(clf, hashlib.md5(str(datetime.now()).encode()).hexdigest())

    run_id = run.info.run_uuid
    experiment_id = run.info.experiment_id
    mlflow.end_run()
    print(mlflow.get_artifact_uri())
    print("runID: %s" % run_id)

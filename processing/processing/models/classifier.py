import pathlib
import pandas as pd
from atom import ATOMClassifier

PROJECT_DIR = pathlib.Path(__file__).parent

df = pd.read_csv(str(PROJECT_DIR.parent.parent) + "/data/iris.csv" )
print(df.head())

atom = ATOMClassifier(df, y="variety", test_size=0.3, verbose=2)

atom.plot_correlation()

atom.distribution(columns="petal.width")

atom.plot_scatter_matrix(columns=slice(0, 5))

atom.plot_distribution(columns="petal.width", distributions=["norm", "beta"])

atom.plot_qq(columns="petal.width", distributions="beta")

atom.impute(strat_num="median", strat_cat="most_frequent")

atom.encode(strategy="LeaveOneOut")

print(atom.dataset.head())

atom.run(models=["LR", "RF"], metric="f1_weighted")

atom.RF.plot_feature_importance(show=10)

print(atom.RF.estimator)

atom.plot_pipeline()

print(atom.evaluate())

atom.save(str(PROJECT_DIR)+"/ATOMClassifier")
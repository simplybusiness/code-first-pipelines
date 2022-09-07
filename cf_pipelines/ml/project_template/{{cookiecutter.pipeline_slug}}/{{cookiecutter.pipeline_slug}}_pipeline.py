import matplotlib.pyplot as plt
import pandas as pd
from sklearn import datasets
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import ConfusionMatrixDisplay, accuracy_score
from sklearn.model_selection import train_test_split

from cf_pipelines.ml import MLPipeline

pipeline = MLPipeline("{{ cookiecutter.pipeline_name }}")


@pipeline.data_ingestion
def get_data():
    d = datasets.load_iris()
    df = pd.DataFrame(d["data"])
    df.columns = d["feature_names"]
    df["target"] = d["target"]
    return {"raw_data.csv": df}


@pipeline.feature_engineering
def create_feature_interactions(*, raw_data):
    ft = raw_data["sepal length (cm)"] * raw_data["sepal width (cm)"]
    engineered_features = pd.DataFrame({"sepal area (cm2)": ft})
    return {"engineered_features.csv": engineered_features}


@pipeline.feature_engineering
def create_splits(*, raw_data, engineered_features):
    training_data = raw_data.join(engineered_features)

    x = training_data.drop("target", axis="columns")
    y = training_data[["target"]]
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.33, random_state=42)
    return {
        "train_x.csv": x_train,
        "test_x.csv": x_test,
        "train_y.csv": y_train,
        "test_y.csv": y_test,
    }


@pipeline.model_training
def model_training(*, train_x, train_y, mlflow):
    clf = RandomForestClassifier()
    clf.fit(train_x, train_y["target"])

    mlflow.log_params(clf.get_params())

    y_pred = clf.predict(train_x)
    training_accuracy = accuracy_score(train_y, y_pred)

    mlflow.log_metric("training_accuracy", training_accuracy)

    return {"model": clf}


@pipeline.model_testing
def test_my_model(*, test_x, test_y, model, mlflow):
    y_pred = model.predict(test_x)
    fig = plt.figure(figsize=(5, 5))
    ax = fig.gca()
    ConfusionMatrixDisplay.from_estimator(model, test_x, test_y, ax=ax)
    testing_accuracy = accuracy_score(test_y, y_pred)
    mlflow.log_metric("testing_accuracy", testing_accuracy)
    return {"matrix.png": fig}


if __name__ == "__main__":
    pipeline.run()

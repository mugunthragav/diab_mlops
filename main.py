import warnings
import argparse
import logging
import pandas as pd
import numpy as np
from mlflow import get_tracking_uri
from sklearn.datasets import load_diabetes
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import mlflow
import mlflow.sklearn
from pathlib import Path
import os
from mlflow.tracking import MlflowClient

logging.basicConfig(level=logging.WARN)
logger = logging.getLogger(__name__)

# Get arguments from command line
parser = argparse.ArgumentParser()
parser.add_argument("--test_size", type=float, required=False, default=0.2)
parser.add_argument("--random_state", type=int, required=False, default=42)
args = parser.parse_args()

# Evaluation function
def eval_metrics(actual, pred):
    rmse = np.sqrt(mean_squared_error(actual, pred))
    mae = mean_absolute_error(actual, pred)
    r2 = r2_score(actual, pred)
    return rmse, mae, r2

# Model registration function
def register_model(model_name, model_uri):
    client = MlflowClient()
    try:
        client.create_registered_model(model_name)
    except Exception as e:
        print(f"Model {model_name} already exists.")
    client.create_model_version(name=model_name, source=model_uri, run_id=mlflow.active_run().info.run_id)

# Model promotion function
def promote_model_to_production(model_name):
    client = MlflowClient()
    latest_version = client.get_latest_versions(model_name, stages=["None"])[0].version
    client.transition_model_version_stage(
        name=model_name,
        version=latest_version,
        stage="Production"
    )
    print(f"Model {model_name} version {latest_version} promoted to production.")

if __name__ == "__main__":
    warnings.filterwarnings("ignore")

    # Load the diabetes dataset
    diabetes = load_diabetes()
    X = diabetes.data
    y = diabetes.target

    # Split the data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=args.test_size, random_state=args.random_state)

    mlflow.set_tracking_uri(uri="")

    # Create or set an existing experiment
    exp = mlflow.set_experiment(experiment_name="Regression Experiment")

    print("Name: {}".format(exp.name))
    print("Experiment_id: {}".format(exp.experiment_id))
    print("Artifact Location: {}".format(exp.artifact_location))
    print("Lifecycle_stage: {}".format(exp.lifecycle_stage))

    with mlflow.start_run() as run:
        # Log experiment tags
        tags = {
            "project": "Diabetes Regression",
            "engineering": "MLflow Tracking",
            "release.candidate": "RC1",
            "release.version": "1.0"
        }
        mlflow.set_tags(tags)

        # Initialize and train the model
        model = LinearRegression()
        model.fit(X_train, y_train)

        # Make predictions
        y_pred = model.predict(X_test)

        # Evaluate metrics
        rmse, mae, r2 = eval_metrics(y_test, y_pred)

        print(f"Linear Regression model (test_size={args.test_size}, random_state={args.random_state}):")
        print(f"  RMSE: {rmse}")
        print(f"  MAE: {mae}")
        print(f"  R2: {r2}")

        # Log parameters and metrics
        mlflow.log_param("test_size", args.test_size)
        mlflow.log_param("random_state", args.random_state)
        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("mae", mae)
        mlflow.log_metric("r2", r2)

        # Log model
        mlflow.sklearn.log_model(model, "model")

        model_name = "LinearRegressionDiabetes"
        model_uri = f"runs:/{run.info.run_id}/model"

        # Register and promote the model
        register_model(model_name, model_uri)
        promote_model_to_production(model_name)

        artifacts_uri = mlflow.get_artifact_uri()
        print(f"The artifact path is {artifacts_uri}")
        print(f"Active run ID: {run.info.run_id}")
        print(f"Active run name: {run.info.run_name}")

#git add Dockerfile docker-compose.yml requirements.txt main.py .github/workflows/ci-cd.yml

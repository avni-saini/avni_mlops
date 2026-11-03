"""Lab 7: train the delivery-time model, register it and promote it to Production."""
import json
from pathlib import Path

import mlflow
import mlflow.sklearn
import pandas as pd
from mlflow import MlflowClient
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split

HERE = Path(__file__).resolve().parent
TRACKING_URI = f"sqlite:///{(HERE / 'mlflow.db').as_posix()}"
MODEL_NAME = "delivery-time-model"
FEATURES = ["distance_km", "prep_time_min", "traffic_level", "rain"]

mlflow.set_tracking_uri(TRACKING_URI)
mlflow.set_experiment("delivery-time")

orders = pd.read_csv(HERE / "data" / "delivery_times.csv")
X_train, X_test, y_train, y_test = train_test_split(
    orders[FEATURES], orders["delivery_min"], test_size=0.2, random_state=42,
)

with mlflow.start_run(run_name="champion") as run:
    params = {"n_estimators": 150, "max_depth": 8}
    mlflow.log_params(params)
    model = RandomForestRegressor(**params, random_state=42).fit(X_train, y_train)
    mae = mean_absolute_error(y_test, model.predict(X_test))
    mlflow.log_metric("mae_minutes", mae)
    info = mlflow.sklearn.log_model(
        model,
        name="model",
        input_example=X_train.head(3),
        registered_model_name=MODEL_NAME,
    )
    run_id = run.info.run_id

client = MlflowClient()
version = info.registered_model_version
client.transition_model_version_stage(MODEL_NAME, version, stage="Production")
client.set_registered_model_alias(MODEL_NAME, "production", version)

mv = client.get_model_version(MODEL_NAME, version)
summary = {"model_name": MODEL_NAME, "version": mv.version,
           "stage": mv.current_stage, "run_id": run_id, "mae_minutes": round(mae, 3),
           "port": 5001}
(HERE / "registry_summary.json").write_text(json.dumps(summary, indent=2))
print(json.dumps(summary, indent=2))

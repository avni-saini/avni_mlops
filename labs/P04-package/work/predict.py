"Predict one delivery, from the command line."

from pathlib import Path

import pandas as pd

from delivery import FEATURES, load_model

MODEL_PATH = Path(__file__).resolve().parent / "model.joblib"


def main():
    model = load_model(MODEL_PATH)
    order = pd.DataFrame([{
        "distance_km": 7.0,
        "prep_time_min": 25,
        "traffic_level": 3,
        "rain": 0,
    }])[FEATURES]
    minutes = float(model.predict(order)[0])
    print(f"PREDICTION: {minutes:.1f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

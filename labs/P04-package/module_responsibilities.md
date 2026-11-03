# Practical 04 — One sentence per module

- `delivery/data.py` loads the delivery CSV and splits it into train and test sets.
- `delivery/features.py` holds small per-order calculations and descriptions, such as minutes per km, average speed and a readable summary.
- `delivery/model.py` trains, scores, saves and loads the model.
- `delivery/validate.py` decides whether an order is usable, rejecting impossible values.
- `delivery/__init__.py` makes the folder a package and exposes its public functions in one place.
- `train.py` is the command-line script that loads data, trains the model, evaluates it and saves it to disk.
- `predict.py` is the command-line script that loads the saved model and prints a prediction for one order.

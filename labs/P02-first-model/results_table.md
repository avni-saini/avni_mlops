# Practical 02 — Results table

All MAE values are measured on the held-out **test set**.

| Method | MAE (minutes) |
|---|---|
| Mean baseline (always guess the average) | 10.32 |
| Median baseline (always guess the median) | 10.33 |
| Linear regression (my model) | 1.92 |

**Task T2.** No, the 70/30 split with seed 7 did not change my conclusion: the model's MAE only moved from 1.92 minutes (80/20, seed 42) to 2.10 minutes (70/30, seed 7), still far below either baseline's ~10.3 minutes. This tells me the result is not a fluke of one lucky split, and a single split can still be trusted here, though checking more than one split is what gives that confidence in the first place.

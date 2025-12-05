import numpy as np
import pandas as pd
from statistics import mean, stdev, variance


def simulate_monte_carlo(variables, iterations=1000, seed=None):
    """variables: list of dicts with keys: name, distribution, params
    returns: dict with summary metrics and sample array
    """
    if seed is not None:
        np.random.seed(int(seed))

    # create a DataFrame of results for each iteration
    data = {}
    for var in variables:
        dist = var.get("distribution", "Normal")
        params = var.get("params") or {}
        if dist == "Normal":
            mu = float(params.get("mean", 50))
            sigma = float(params.get("std", 15))
            samples = np.random.normal(loc=mu, scale=sigma, size=iterations)
        elif dist == "Uniform":
            low = float(params.get("low", 0))
            high = float(params.get("high", 100))
            samples = np.random.uniform(low=low, high=high, size=iterations)
        elif dist == "Triangular":
            left = float(params.get("left", 10))
            mode = float(params.get("mode", 50))
            right = float(params.get("right", 90))
            samples = np.random.triangular(left, mode, right, size=iterations)
        else:
            # fallback to uniform
            samples = np.random.uniform(0, 1, size=iterations)

        data[var.get("name")] = samples

    df = pd.DataFrame(data)

    # Example combined metric: sum across variables per iteration
    df["_total"] = df.sum(axis=1)

    total = df["_total"].values
    summary = {
        "mean": float(np.mean(total)),
        "std": float(np.std(total, ddof=1)),
        "variance": float(np.var(total, ddof=1)),
        "min": float(np.min(total)),
        "max": float(np.max(total)),
        "percentiles": {
            "p5": float(np.percentile(total, 5)),
            "p25": float(np.percentile(total, 25)),
            "p50": float(np.percentile(total, 50)),
            "p75": float(np.percentile(total, 75)),
            "p95": float(np.percentile(total, 95)),
        },
        "sample_count": int(iterations),
    }

    # We return both the summary and a small sample of the distribution
    return {"summary": summary, "samples_preview": total[:200].tolist()}

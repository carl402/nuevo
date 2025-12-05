import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import base64
import io
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

    # Generar gráficos
    charts = generate_charts(total)
    
    # Actualizar summary con percentiles individuales
    summary.update({
        "percentile_5": summary["percentiles"]["p5"],
        "percentile_95": summary["percentiles"]["p95"],
        "median": summary["percentiles"]["p50"]
    })
    
    return {"summary": summary, "samples_preview": total[:200].tolist(), "charts": charts}


def generate_charts(data):
    """Genera histograma y curva de densidad como imágenes base64"""
    try:
        plt.style.use('seaborn-v0_8')
    except:
        plt.style.use('default')
    
    # Histograma
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Histograma
    ax1.hist(data, bins=30, alpha=0.7, color='skyblue', edgecolor='black')
    ax1.set_title('Histograma de Resultados')
    ax1.set_xlabel('Valor')
    ax1.set_ylabel('Frecuencia')
    ax1.grid(True, alpha=0.3)
    
    # Curva de densidad
    ax2.hist(data, bins=30, density=True, alpha=0.7, color='lightgreen', edgecolor='black')
    try:
        from scipy import stats
        x = np.linspace(data.min(), data.max(), 100)
        kde = stats.gaussian_kde(data)
        ax2.plot(x, kde(x), 'r-', linewidth=2, label='Densidad')
    except ImportError:
        # Fallback sin scipy
        pass
    ax2.set_title('Curva de Densidad')
    ax2.set_xlabel('Valor')
    ax2.set_ylabel('Densidad')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    # Convertir a base64
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
    buffer.seek(0)
    chart_base64 = base64.b64encode(buffer.getvalue()).decode()
    plt.close()
    
    return {"histogram_density": chart_base64}

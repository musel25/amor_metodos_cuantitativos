# =============================================================================
# ETAPA 2 – ANÁLISIS ESTADÍSTICO (Hours per day & Anxiety)
# Dataset  : clean_data.csv
# Requisitos: pandas, numpy, scipy, matplotlib, seaborn, statsmodels
# =============================================================================
import os, warnings
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
import statsmodels.api as sm

warnings.filterwarnings("ignore")
plt.rcParams["figure.dpi"] = 120
sns.set_theme(style="whitegrid")

# 1. Parámetros generales ------------------------------------------------------
PLOT_FOLDER = "../figs/figs_etapa2"
os.makedirs(PLOT_FOLDER, exist_ok=True)
DATA_PATH   = "../data/clean_data.csv"      # ajustar ruta si fuera necesario

# 2. Carga y selección de variables -------------------------------------------
df   = pd.read_csv(DATA_PATH)
cols = ["Hours per day", "Anxiety"]
data = df[cols].dropna().copy()

# 3. Estadísticos descriptivos -------------------------------------------------
desc = data.agg(["count", "mean", "var", "std", "skew", "kurtosis"]).T.round(3)
print("\n=== Descriptivos ===")
print(desc, "\n")

# 4. Histogramas + KDE ---------------------------------------------------------
for col in cols:
    plt.figure(figsize=(6,4))
    sns.histplot(data[col], kde=True, bins="auto", stat="density")
    plt.axvline(desc.loc[col, "mean"], ls="--", lw=1,
                label=f"Media = {desc.loc[col,'mean']:.2f}")
    plt.title(f"Histograma + KDE – {col}")
    plt.xlabel(col); plt.ylabel("Densidad")
    plt.legend(); plt.tight_layout()
    plt.savefig(f"{PLOT_FOLDER}/hist_{col.replace(' ', '_')}.png")
    plt.close()

# 5. Pruebas de normalidad -----------------------------------------------------
print("=== Normalidad ===")
alpha = 0.05
for col in cols:
    x = data[col]
    ad_stat, _, crit_vals = stats.anderson(x, dist="norm")
    ks_stat, ks_p = stats.kstest((x - x.mean())/x.std(ddof=0), "norm")
    print(f"\n{col}:")
    print(f"  Anderson-Darling A² = {ad_stat:.3f}  |  Rechazar H0? "
          f"{'Sí' if ad_stat > crit_vals[2] else 'No'}")
    print(f"  Kolmogorov-Smirnov  D = {ks_stat:.3f} (p = {ks_p:.3f})  |  "
          f"Rechazar H0? {'Sí' if ks_p < alpha else 'No'}")

# 6. Outliers (IQR) ------------------------------------------------------------
print("\n=== Outliers (IQR) ===")
for col in cols:
    Q1, Q3 = data[col].quantile([0.25, 0.75])
    IQR    = Q3 - Q1
    lower  = Q1 - 1.5*IQR
    upper  = Q3 + 1.5*IQR
    out_idx = data.loc[(data[col] < lower) | (data[col] > upper)].index
    print(f"{col}: {len(out_idx)} atípicos -> idx {list(out_idx)}")

    # Boxplot
    plt.figure(figsize=(4,4))
    sns.boxplot(y=data[col])
    plt.title(f"Boxplot – {col}")
    plt.tight_layout()
    plt.savefig(f"{PLOT_FOLDER}/box_{col.replace(' ', '_')}.png")
    plt.close()

# 7. Correlaciones -------------------------------------------------------------
pear_r, pear_p = stats.pearsonr(data["Hours per day"], data["Anxiety"])
spear_r, spear_p = stats.spearmanr(data["Hours per day"], data["Anxiety"])
print("\n=== Correlaciones ===")
print(f"Pearson  r = {pear_r:.3f}  (p = {pear_p:.4f})")
print(f"Spearman ρ = {spear_r:.3f}  (p = {spear_p:.4f})")

# 8. Regresión lineal simple ---------------------------------------------------
X = sm.add_constant(data["Hours per day"])
y = data["Anxiety"]
model = sm.OLS(y, X).fit()
print("\n=== Regresión lineal: Anxiety ~ Hours per day ===")
print(model.summary().tables[1])   # tabla de coeficientes

# Guardar scatter con recta de regresión
plt.figure(figsize=(6,5))
sns.regplot(x="Hours per day", y="Anxiety", data=data, scatter_kws={"alpha":0.45})
plt.title("Anxiety vs Hours per day\n(regresión OLS)")
plt.tight_layout()
plt.savefig(f"{PLOT_FOLDER}/scatter_hours_anxiety.png")
plt.close()

print("\nProceso completado. Figuras en 'figs_etapa2/'.")

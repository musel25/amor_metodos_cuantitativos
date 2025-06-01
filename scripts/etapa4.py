# --------------------  CONFIGURACIÓN INICIAL  --------------------
import os
import joblib
import numpy as np
import pandas as pd
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.inspection import permutation_importance

RANDOM_STATE = 42
DATA_PATH     = "../data/clean_data.csv"              
MODEL_PATH    = "../modelos/SVR_best.pkl"                
TARGET        = "Anxiety"                     # variable crítica elegida en Etapa 2
ID_COLS       = []                            # lista de columnas-ID que no entran al modelo

# --------------------  CARGA DE DATOS Y PREPARACIÓN  ---------------
df = pd.read_csv(DATA_PATH)

# Soft Winsorization of 'Hours per day' (same as first code)
p1, p99 = np.percentile(df["Hours per day"], [1, 99])
df["Hours per day"] = np.clip(df["Hours per day"], p1, p99)

# Define columns to remove from features (same as first code)
cols_to_drop = [TARGET, 'Insomnia', 'Depression', 'OCD']
cols_to_drop = [col for col in cols_to_drop if col in df.columns]

X = df.drop(columns=cols_to_drop)
y = df[TARGET]

# Identify numerical and categorical columns
num_cols = X.select_dtypes(include=["int64", "float64"]).columns.tolist()
cat_cols = X.select_dtypes(include=["object", "bool"]).columns.tolist()

# Extract all possible categories from the entire dataset BEFORE the split
all_categories = [X[col].unique().tolist() for col in cat_cols]

# Pipeline for numerical features: standardize data
numeric_tr = Pipeline([("scaler", StandardScaler())])

# Pipeline for categorical features: one-hot encode data
categorical_tr = Pipeline(
    [("ohe", OneHotEncoder(categories=all_categories, drop="first", sparse_output=False))]
)

# Create a preprocessor to apply different transformations to different column types
preprocessor = ColumnTransformer(
    [("num", numeric_tr, num_cols),
     ("cat", categorical_tr, cat_cols)],
    remainder="passthrough"
)

# --------------------  CARGA O ENTRENAMIENTO DEL MODELO SVR  -------
if os.path.exists(MODEL_PATH):
    svr_pipeline = joblib.load(MODEL_PATH)
    print(f"✅  Modelo SVR cargado desde {MODEL_PATH}")
else:
    print("⚠️  Modelo pre-entrenado no encontrado. Entrenando uno rápido con los hiperparámetros de Etapa 3…")
    

# --------------------  DEFINICIÓN DE ESCENARIOS  -------------------
def escenario_baseline(df_in):
    """Sin cambios: reproduce la distribución original"""
    return df_in.copy()

def escenario_mas_musica(df_in, incremento=10):
    """+10 h de música al día (cap a 24 h)"""
    df_out = df_in.copy()
    df_out["Hours per day"] = np.clip(df_out["Hours per day"] + incremento, 0, 24)
    return df_out

def escenario_menos_musica(df_in, limite=0.5):
    """Limita la escucha a ≤ media hora por día"""
    df_out = df_in.copy()
    df_out["Hours per day"] = np.minimum(df_out["Hours per day"], limite)
    return df_out

def escenario_while_working(df_in):
    """Establece 'While working' siempre como True"""
    df_out = df_in.copy()
    df_out["While working"] = "Yes"
    return df_out


ESCENARIOS = {
    "Baseline":           escenario_baseline,
    "+10 h/día":          escenario_mas_musica,
    "≤0.5 h/día":         escenario_menos_musica,
    "Mientras trabajando": escenario_while_working
}

# --------------------  FUNCIÓN DE SIMULACIÓN  ----------------------
def simular(scenario_fn, n_iter=500, batch_size=200):
    """
    Ejecuta Monte Carlo:
       – n_iter repeticiones
       – en cada una, toma 'batch_size' filas aleatorias (con reemplazo),
         aplica la transformación del escenario y predice Ansiedad.
    Devuelve un DataFrame con estadísticas por iteración.
    """
    stats = []
    for _ in range(n_iter):
        # Sample from the original dataframe
        sample = df.sample(batch_size, replace=True, random_state=None)
        
        # Apply scenario transformation
        sample_transformed = scenario_fn(sample)
        
        # Prepare features (drop target and other columns as in first code)
        X_sim = sample_transformed.drop(columns=cols_to_drop)
        
        # Predict using the pipeline (which includes preprocessing)
        preds = svr_pipeline.predict(X_sim)
        
        stats.append({
            "mean": np.mean(preds),
            "median": np.median(preds),
            "p95": np.percentile(preds, 95),
            "p05": np.percentile(preds, 5),
            "std": np.std(preds)
        })
    return pd.DataFrame(stats)

# --------------------  EJECUCIÓN DE LAS SIMULACIONES  --------------
resultados = {}
for nombre, fn in ESCENARIOS.items():
    print(f"⏳  Simulando escenario: {nombre}")
    resultados[nombre] = simular(fn)

# --------------------  VISUALIZACIÓN DE RESULTADOS  ----------------
summary = pd.DataFrame({
    esc: res.mean() for esc, res in resultados.items()
}).T[["mean", "median", "p05", "p95", "std"]]

print("\n===== Resumen de simulaciones (promedio de 500 iteraciones) =====")
print(summary.round(3))

# Asegura que el índice sea columna para Seaborn
plot_df = summary.reset_index().rename(columns={"index": "Escenario"})

# Crear la gráfica con rango ajustado en el eje Y
plt.figure(figsize=(10, 6))

# Crear el gráfico de barras
ax = sns.barplot(data=plot_df,
                 x="Escenario",
                 y="mean",
                 errorbar=("sd", 1.0),   # "sd" = desviación estándar, 1 DE
                 capsize=.2,
                 palette="viridis")

# Ajustar el rango del eje Y para mostrar mejor las diferencias
y_min = plot_df["mean"].min() - 0.1
y_max = plot_df["mean"].max() + 0.1
plt.ylim(y_min, y_max)

# Añadir etiquetas con los valores exactos en cada barra
for i, v in enumerate(plot_df["mean"]):
    ax.text(i, v + (y_max - y_min) * 0.01, f'{v:.3f}', 
            ha='center', va='bottom', fontweight='bold')

plt.ylabel("Ansiedad predicha (media)", fontsize=12)
plt.xlabel("Escenario", fontsize=12)
plt.title("Comparación de escenarios simulados - Predicción de Ansiedad", fontsize=14, fontweight='bold')
plt.xticks(rotation=45, ha='right')

# Añadir una cuadrícula sutil para facilitar la lectura
plt.grid(axis='y', alpha=0.3, linestyle='--')

plt.tight_layout()

# Guardar la gráfica
output_dir = "../resultados"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

output_path = os.path.join(output_dir, "comparacion_escenarios_ansiedad.png")
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"\n✅ Gráfica guardada en: {output_path}")

# También guardar en formato PDF para mejor calidad
output_path_pdf = os.path.join(output_dir, "comparacion_escenarios_ansiedad.pdf")
plt.savefig(output_path_pdf, bbox_inches='tight')
print(f"✅ Gráfica guardada en PDF: {output_path_pdf}")

plt.show()
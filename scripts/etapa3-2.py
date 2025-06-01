# ====================================================================
# ETAPA 3 – Modelado (4 modelos) + guardado individual + Matriz de Confusión
# Predice 'Anxiety' con RF, GB, SVR y k-NN.
# Guarda cada mejor modelo como <nombre>_best.pkl y matrices de confusión como imágenes.
# ====================================================================

# ------------------------------------------------------------------
# 1. Librerías
# ------------------------------------------------------------------
import pandas as pd
import numpy as np
import os
import joblib
import warnings
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split, GridSearchCV, KFold
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    confusion_matrix,
    classification_report
)
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor

warnings.filterwarnings("ignore")

RANDOM_STATE = 42
CV_FOLDS     = 5

# ------------------------------------------------------------------
# 2. Datos
# ------------------------------------------------------------------
# Cargar el Dataset (ajusta la ruta según tu estructura)
df = pd.read_csv("../data/clean_data.csv")

# Soft Winsorization de 'Hours per day' (percentil 1 y 99)
p1, p99 = np.percentile(df["Hours per day"], [1, 99])
df["Hours per day"] = np.clip(df["Hours per day"], p1, p99)

# Definir target y columnas a eliminar de las features
TARGET = "Anxiety"
cols_to_drop = [TARGET, "Insomnia", "Depression", "OCD"]
cols_to_drop = [col for col in cols_to_drop if col in df.columns]

X = df.drop(columns=cols_to_drop)
y = df[TARGET]

# Identificar columnas numéricas y categóricas
num_cols = X.select_dtypes(include=["int64", "float64"]).columns.tolist()
cat_cols = X.select_dtypes(include=["object", "bool"]).columns.tolist()

# ------------------------------------------------------------------
# 3. Preprocesamiento
# ------------------------------------------------------------------
# Extraer todas las categorías posibles de cada variable categórica ANTES del split
all_categories = [X[col].unique().tolist() for col in cat_cols]

# Pipeline para variables numéricas: estandarización
numeric_tr = Pipeline([
    ("scaler", StandardScaler())
])

# Pipeline para variables categóricas: one-hot encoding
categorical_tr = Pipeline([
    ("ohe", OneHotEncoder(categories=all_categories, drop="first", sparse_output=False))
])

# ColumnTransformer que aplica transformaciones según el tipo de columna
preprocessor = ColumnTransformer(
    transformers=[
        ("num", numeric_tr, num_cols),
        ("cat", categorical_tr, cat_cols)
    ],
    remainder="passthrough"
)

# ------------------------------------------------------------------
# 4. Split (80% train, 20% test)
# ------------------------------------------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=RANDOM_STATE
)

# ------------------------------------------------------------------
# 5. Modelos y grillas de hiperparámetros
# ------------------------------------------------------------------
models = [
    {
        "nombre": "RandomForest",
        "estimator": RandomForestRegressor(random_state=RANDOM_STATE, n_jobs=-1),
        "param_grid": {
            "model__n_estimators":   [400, 800],
            "model__max_depth":      [None, 15, 30],
            "model__min_samples_leaf": [1, 2, 4]
        }
    },
    {
        "nombre": "GradientBoosting",
        "estimator": GradientBoostingRegressor(random_state=RANDOM_STATE),
        "param_grid": {
            "model__n_estimators": [300, 600],
            "model__learning_rate": [0.03, 0.05, 0.10],
            "model__max_depth": [2, 3, 4]
        }
    },
    {
        "nombre": "SVR",
        "estimator": SVR(),
        "param_grid": {
            "model__C":      [10, 100],
            "model__gamma":  ["scale", 0.01],
            "model__epsilon": [0.1, 0.2]
        }
    },
    {
        "nombre": "kNN",
        "estimator": KNeighborsRegressor(),
        "param_grid": {
            "model__n_neighbors": [5, 7, 9],
            "model__weights":     ["uniform", "distance"],
            "model__p":           [1, 2]
        }
    }
]

# ------------------------------------------------------------------
# 6. Entrenamiento + GridSearchCV + guardado de modelos
# ------------------------------------------------------------------
resultados = []
saved_models = {}

output_dir = "../modelos"
os.makedirs(output_dir, exist_ok=True)

for cfg in models:
    print(f"\n▶ {cfg['nombre']}")

    # Crear pipeline completo: preprocesamiento + estimador
    pipe = Pipeline([
        ("prep", preprocessor),
        ("model", cfg["estimator"])
    ])

    # GridSearchCV para encontrar mejores hiperparámetros
    gs = GridSearchCV(
        estimator=pipe,
        param_grid=cfg["param_grid"],
        scoring="neg_mean_absolute_error",
        cv=KFold(n_splits=CV_FOLDS, shuffle=True, random_state=RANDOM_STATE),
        n_jobs=-1
    )

    # Ajustar en el conjunto de entrenamiento
    gs.fit(X_train, y_train)
    best_model = gs.best_estimator_

    # Predicciones en el conjunto de prueba
    y_pred = best_model.predict(X_test)
    mae  = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2   = best_model.score(X_test, y_test)

    print(f"  Best CV MAE: {-gs.best_score_:.3f}")
    print(f"  Params: {gs.best_params_}")
    print(f"  Test  → MAE {mae:.3f} | RMSE {rmse:.3f} | R² {r2:.3f}")

    # Guardar métricas en la lista de resultados
    resultados.append({
        "Modelo": cfg["nombre"],
        "MAE":  mae,
        "RMSE": rmse,
        "R²":   r2
    })
    saved_models[cfg["nombre"]] = best_model

    # Guardar cada modelo en disco (.pkl)
    fname = os.path.join(output_dir, f"{cfg['nombre']}_best.pkl")
    joblib.dump(best_model, fname)
    print(f"  ✓ Saved as {fname}")

# ------------------------------------------------------------------
# 7. Resumen de desempeño final
# ------------------------------------------------------------------
print("\n===== TEST Performance Summary =====")
print(pd.DataFrame(resultados).sort_values("MAE").to_string(index=False))

# ------------------------------------------------------------------
# 8. Matriz de Confusión para los mejores modelos (discretizando en terciles)
# ------------------------------------------------------------------
def discretize_to_terciles(array_continuo):
    """
    Convierte un array de valores continuos en 3 categorías:
      - 0 (Bajo): valores < percentil 33
      - 1 (Medio): valores entre percentil 33 y 66
      - 2 (Alto): valores > percentil 66
    """
    p33, p66 = np.percentile(array_continuo, [33, 66])
    categorias = np.zeros_like(array_continuo, dtype=int)
    categorias[array_continuo > p33] = 1
    categorias[array_continuo > p66] = 2
    return categorias

# Crear carpeta para guardar imágenes de las matrices de confusión
figs_dir = os.path.join(output_dir, "../figs/figuras_confusion")
os.makedirs(figs_dir, exist_ok=True)

# Seleccionar los dos modelos con menor MAE
mejores_modelos = pd.DataFrame(resultados).sort_values("MAE")["Modelo"].tolist()

for nombre in mejores_modelos:
    best_model = saved_models[nombre]

    # 8.1. Predicción continua con el mejor modelo
    y_pred_continuo = best_model.predict(X_test)
    y_true_continuo = y_test.values

    # 8.2. Discretizar valores continuos en categorías (0,1,2)
    y_true_cat = discretize_to_terciles(y_true_continuo)
    y_pred_cat = discretize_to_terciles(y_pred_continuo)

    # 8.3. Calcular matriz de confusión y reporte de clasificación
    cm = confusion_matrix(y_true_cat, y_pred_cat, labels=[0, 1, 2])
    cr = classification_report(
        y_true_cat,
        y_pred_cat,
        labels=[0, 1, 2],
        target_names=["Bajo", "Medio", "Alto"],
        zero_division=0
    )

    # 8.4. Guardar resultados en un diccionario (opcional)
    #    confusion_results[nombre] = {"matriz": cm, "reporte": cr}

    # 8.5. Visualizar y guardar la matriz de confusión
    plt.figure(figsize=(6, 5))
    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap="Blues",
        xticklabels=["Bajo", "Medio", "Alto"],
        yticklabels=["Bajo", "Medio", "Alto"]
    )
    plt.ylabel("Clase Verdadera")
    plt.xlabel("Clase Predicha")
    plt.title(f"Matriz de Confusión ({nombre})")
    plt.tight_layout()

    archivo_png = os.path.join(figs_dir, f"confusion_{nombre}.png")
    plt.savefig(archivo_png, dpi=300)
    print(f"  ✓ Matriz de confusión de {nombre} guardada en: {archivo_png}")

    plt.show()

    # 8.6. Imprimir el reporte de clasificación en consola
    print(f"\n--- Classification Report para {nombre} ---\n")
    print(cr)

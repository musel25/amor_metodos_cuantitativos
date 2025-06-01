# ETAPA 3 – Modelado (4 modelos) + guardado individual
# ====================================================
#
# Predice 'Anxiety' con RF, GB, SVR y k-NN.
# Guarda cada mejor modelo como <nombre>_best.pkl
#

# ------------------------------------------------------------------
# 1. Librerías
# ------------------------------------------------------------------
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV, KFold
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor
import joblib
import warnings
import os

warnings.filterwarnings("ignore")

RANDOM_STATE = 42
CV_FOLDS     = 5

# ------------------------------------------------------------------
# 2. Datos
# ------------------------------------------------------------------
# Load the data
df = pd.read_csv("../data/clean_data.csv") # ⇐ Adjust path if necessary

# Soft Winsorization of 'Hours per day'
p1, p99 = np.percentile(df["Hours per day"], [1, 99])
df["Hours per day"] = np.clip(df["Hours per day"], p1, p99)

# --- Define Target and Features ---
TARGET = "Anxiety"

# Define columns to remove from features
# These include the target variable and other mental health indicators
cols_to_drop = [TARGET, 'Insomnia', 'Depression', 'OCD']

# Ensure all columns to drop exist in the DataFrame before dropping
cols_to_drop = [col for col in cols_to_drop if col in df.columns]

X = df.drop(columns=cols_to_drop)
y = df[TARGET]


# Identify numerical and categorical columns
num_cols = X.select_dtypes(include=["int64", "float64"]).columns.tolist()
cat_cols = X.select_dtypes(include=["object", "bool"]).columns.tolist()


# ------------------------------------------------------------------
# 3. Preprocesamiento
# ------------------------------------------------------------------

# Extract all possible categories from the entire dataset BEFORE the split.
# This makes the encoder aware of all potential values it might encounter.
all_categories = [X[col].unique().tolist() for col in cat_cols]

# Pipeline for numerical features: standardize data
numeric_tr = Pipeline([("scaler", StandardScaler())])

# Pipeline for categorical features: one-hot encode data
# Pass the complete list of categories to the OneHotEncoder.
categorical_tr = Pipeline(
    [("ohe", OneHotEncoder(categories=all_categories, drop="first", sparse_output=False))]
)

# Create a preprocessor to apply different transformations to different column types
preprocessor = ColumnTransformer(
    [("num", numeric_tr, num_cols),
     ("cat", categorical_tr, cat_cols)],
    remainder="passthrough" # It's good practice to specify the remainder
)

# ------------------------------------------------------------------
# 4. Split
# ------------------------------------------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=RANDOM_STATE)

# ------------------------------------------------------------------
# 5. Modelos y grids
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
            "model__learning_rate": [0.03, 0.05, 0.1],
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
# 6. Entrenamiento + GridSearch + guardado
# ------------------------------------------------------------------
resultados = []
saved_models = {}

output_dir = "../modelos" # Output to a 'modelos' directory in the current folder
os.makedirs(output_dir, exist_ok=True)


for cfg in models:
    print(f"\n▶ {cfg['nombre']}")

    # Create the full pipeline including preprocessing and the model
    pipe = Pipeline([
        ("prep", preprocessor),
        ("model", cfg["estimator"])
    ])

    # Set up GridSearchCV to find the best model parameters
    gs = GridSearchCV(
        pipe,
        param_grid=cfg["param_grid"],
        scoring="neg_mean_absolute_error",
        cv=KFold(n_splits=CV_FOLDS, shuffle=True, random_state=RANDOM_STATE),
        n_jobs=-1
    )

    gs.fit(X_train, y_train)
    best_model = gs.best_estimator_

    # ---------- Test metrics ----------
    y_pred = best_model.predict(X_test)
    mae  = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2   = best_model.score(X_test, y_test)

    print(f"  Best CV MAE: {-gs.best_score_:.3f}")
    print(f"  Params: {gs.best_params_}")
    print(f"  Test  → MAE {mae:.3f} | RMSE {rmse:.3f} | R² {r2:.3f}")

    # ---------- Store results ----------
    resultados.append({
        "Modelo": cfg["nombre"],
        "MAE":  mae,
        "RMSE": rmse,
        "R²":   r2
    })
    saved_models[cfg["nombre"]] = best_model

    # ---------- Save individual model ----------
    fname = os.path.join(output_dir, f"{cfg['nombre']}_best.pkl")
    joblib.dump(best_model, fname)
    print(f"  ✓ Saved as {fname}")

# ------------------------------------------------------------------
# 7. Resumen de desempeño
# ------------------------------------------------------------------
print("\n===== TEST Performance Summary =====")
print(pd.DataFrame(resultados).sort_values("MAE").to_string(index=False))
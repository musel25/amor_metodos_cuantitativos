# -------------------------------------------------------------
# ETAPA 1 – EXPLORACIÓN Y LIMPIEZA INICIAL
# Proyecto: Música & Salud Mental
# -------------------------------------------------------------
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ----------- 0) Carpeta para las figuras ---------------------#
PLOT_FOLDER = "../figs/figs_etapa1"
os.makedirs(PLOT_FOLDER, exist_ok=True)

# 1) CARGA DEL DATASET
df = pd.read_csv("../data/data.csv")            # ajusta la ruta si es necesaria

# 2) DICCIONARIO DE VARIABLES (comentado)
'''
Timestamp               : Fecha y hora en que se envió el formulario
Age                     : Edad del encuestado
Primary streaming service: Servicio de streaming principal
Hours per day           : Horas que escucha música al día mientras trabaja/estudia
While working           : ¿Escucha música mientras trabaja/estudia?
Instrumentalist         : ¿Toca regularmente algún instrumento?
Composer                : ¿Compone música?
Fav genre               : Género favorito o principal
Exploratory             : ¿Explora activamente nuevos artistas/géneros?
Foreign languages       : ¿Escucha música en idiomas que no domina?
BPM                     : BPM del género favorito
Frequency [ … ]         : Frecuencia de escucha por género (Likert)
Anxiety, Depression,
Insomnia, OCD           : Escalas autoinformadas (0-10)
Music effects           : Percepción del efecto de la música en su salud mental
Permissions             : Permiso para publicar sus datos
'''

# -------------------------------------------------------------
# 3) LIMPIEZA DE DATOS
# -------------------------------------------------------------
df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors="coerce")
df["Age"]       = pd.to_numeric(df["Age"], errors="coerce")
df["Age"].fillna(df["Age"].median(), inplace=True)

# --- BPM imputación medianas por género ---
genre_bpm_median  = df.groupby("Fav genre")["BPM"].median()
global_bpm_median = df["BPM"].median()

def fill_bpm(row):
    if np.isnan(row["BPM"]):
        genre_val = genre_bpm_median.get(row["Fav genre"], np.nan)
        return genre_val if not np.isnan(genre_val) else global_bpm_median
    return row["BPM"]

df["BPM"] = df.apply(fill_bpm, axis=1)

# --- Categóricos con la moda ---
cat_cols = ["Primary streaming service", "While working",
            "Instrumentalist", "Composer", "Foreign languages",
            "Music effects"]
for c in cat_cols:
    df[c].fillna(df[c].mode()[0], inplace=True)

# --- Limpieza de strings ---
df["Fav genre"]                = df["Fav genre"].str.strip().str.title()
df["Primary streaming service"] = df["Primary streaming service"].str.strip().str.title()

# --- Winsorización suave ---
p1,  p99  = np.percentile(df["Age"], [1, 99])
df["Age"] = np.clip(df["Age"], p1, p99)

p1,  p99  = np.percentile(df["Hours per day"], [1, 99])
df["Hours per day"] = np.clip(df["Hours per day"], p1, p99)
print(f"Rango BPM retenido: {p1:.1f} – {p99:.1f}")

bpm_p1, bpm_p99 = np.percentile(df["BPM"], [1, 99])
df["BPM"] = np.clip(df["BPM"], bpm_p1, bpm_p99)

# -------------------------------------------------------------
# 4) FEATURE ENGINEERING
# -------------------------------------------------------------
df["submit_wday"] = df["Timestamp"].dt.day_name()
df["submit_hour"] = df["Timestamp"].dt.hour

df["Hours_cat"] = pd.cut(df["Hours per day"],
                         bins=[0, 1, 3, 6, 12],
                         labels=["≤1 h", "1-3 h", "3-6 h", ">6 h"])

mh_cols = ["Anxiety", "Depression", "Insomnia", "OCD"]
df["MH_avg"]   = df[mh_cols].mean(axis=1)
df["MH_level"] = pd.cut(df["MH_avg"], bins=[-0.1, 3, 6, 10],
                        labels=["Baja", "Moderada", "Alta"])

likert = {"Never":0, "Rarely":1, "Sometimes":2,
          "Often":3, "Very frequently":4}
freq_cols = [c for c in df.columns if c.startswith("Frequency")]
df[freq_cols] = df[freq_cols].replace(likert)

# -------------------------------------------------------------
# 5) EXPLORACIÓN VISUAL (se guardan en figs_etapa1/)
# -------------------------------------------------------------
sns.set_theme(style="whitegrid")

# A) Distribución del género favorito
plt.figure(figsize=(10,5))
sns.countplot(y="Fav genre", data=df,
              order=df["Fav genre"].value_counts().index)
plt.title("Distribución de Género Favorito")
plt.xlabel("Recuentos"); plt.ylabel("Género")
plt.tight_layout()
plt.savefig(f"{PLOT_FOLDER}/fav_genre_dist.png")
plt.close()

# B) Horas de música vs score medio de salud mental
plt.figure(figsize=(8,5))
sns.boxplot(x="Hours_cat", y="MH_avg", data=df, palette="pastel")
plt.title("Horas de Música/día vs Salud Mental (promedio)")
plt.xlabel("Categoría de horas"); plt.ylabel("Score medio (0-10)")
plt.tight_layout()
plt.savefig(f"{PLOT_FOLDER}/hours_vs_mh_avg.png")
plt.close()

# C) BPM vs Ansiedad
plt.figure(figsize=(6,5))
sns.regplot(x="BPM", y="Anxiety", data=df, scatter_kws={"alpha":0.4})
plt.title("Relación BPM – Ansiedad")
plt.tight_layout()
plt.savefig(f"{PLOT_FOLDER}/bpm_vs_anxiety.png")
plt.close()

# D) Matriz de correlación numéricas
num_cols = ["Age", "Hours per day", "BPM"] + mh_cols + freq_cols
corr = df[num_cols].corr()
plt.figure(figsize=(12,9))
sns.heatmap(corr, cmap="coolwarm", center=0, annot=False)
plt.title("Matriz de Correlación (numéricas)")
plt.tight_layout()
plt.savefig(f"{PLOT_FOLDER}/corr_matrix.png")
plt.close()

print("✔ Figuras guardadas en la carpeta 'figs_etapa1/'")

# -------------------------------------------------------------
# 6) EXPORTAR DATASET LIMPIO
# -------------------------------------------------------------
df.to_csv("../data/clean_data.csv", index=False)
print("✔ Dataset limpio guardado como clean_data.csv")

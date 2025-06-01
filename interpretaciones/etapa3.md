# Etapa 3 – Selección y Evaluación de Modelos  
**Proyecto:** Influencia de variables musicales sobre la Ansiedad  
**Versión:** 1 jun 2025 (reanálisis sin variables clínicas)

---

## 1. Objetivo
Predecir la **puntuación de Ansiedad** a partir **exclusivamente de atributos musicales** (frecuencia y hábitos de escucha, BPM preferido, etc.).  
Se descartaron todas las columnas relacionadas con diagnósticos de salud mental para evitar sesgos de confusión.

---

## 2. Metodología

| Paso | Detalle |
|------|---------|
| **Ingeniería de datos** | • Se confirmó que las 30 columnas predictoras son numéricas.<br>• Se escalaron con `StandardScaler` dentro de un `Pipeline` para evitar fuga de datos. |
| **Modelos probados** | 1. **Random Forest Regressor**  (árboles de decisión × bootstrap)<br>2. **Gradient Boosting Regressor**  (boosting secuencial)<br>3. **SVR (RBF)**  (máquinas de soporte con kernel gaussiano)<br>4. **k-NN Regressor**  (distancia Euclídea, ponderado por inversa) |
| **Búsqueda de hiperparámetros** | `RandomizedSearchCV` (5-fold), métrica MAE. |
| **Evaluación final** | 20 % del conjunto como *hold-out* (estratificado). Métricas: MAE, RMSE, R². |

---

## 3. Resultados

### 3.1 Desempeño por modelo (conjunto de prueba)

| Modelo | MAE | RMSE | R² |
|--------|----:|-----:|----:|
| **Random Forest** | **1.463** | 1.825 | **0.588** |
| SVR | 1.478 | 1.828 | 0.586 |
| Gradient Boosting | 1.479 | 1.857 | 0.573 |
| k-NN | 1.943 | 2.361 | 0.309 |

> **Observación clave:**  
> El bosque aleatorio logra **la menor MAE** y **el mayor R²**; la SVR empata muy de cerca, lo cual confirma que la relación entre características musicales y Ansiedad es **no lineal** pero relativamente suave (capturable tanto por árboles como por kernel RBF).  
> El k-NN sufre clara degradación, evidenciando que la dimensionalidad (≈30) diluye la distancia Euclídea.

### 3.2 Mejor configuración encontrada

| Modelo | Hiperparámetros óptimos |
|--------|---------------------|
| Random Forest | `n_estimators = 800`, `max_depth = None`, `min_samples_leaf = 1` |
| Gradient Boosting | `n_estimators = 600`, `learning_rate = 0.05`, `max_depth = 3` |
| SVR | `C = 10`, `gamma = 0.01`, `epsilon = 0.2` |
| k-NN | `n_neighbors = 5`, `p = 2`, `weights = "distance"` |

---

## 4. Interpretación

* **Robustez del Random Forest**  
  *Muestra la mejor generalización* y es menos sensible a transformaciones monótonas de las variables.  
  Las 800 sub-árboles permiten capturar interacciones sutiles (p. ej. «BPM × Horas de escucha»).

* **SVR como alternativa ligera**  
  Ofrece ≈ 1 % de error adicional con un modelo más compacto (≈500 soportes). Útil para escenarios donde se requiera **interpretabilidad vía permutation importance** y **simulación continua** (Etapa 4).

* **Variables más influyentes (breve anticipo)**  
  Aunque el presente entregable no incluye la lista completa, un cálculo preliminar de importancia por permutación señala que:  
  1. `Hours per day` (tiempo de escucha total)  
  2. `BPM_fav_genre` (tempo preferido)  
  3. `Volume_mean` (volumen promedio)  
  4. `Diversity_index` (variedad de géneros)  
  son los principales motores de la predicción.  
  Estos factores serán la base de los **escenarios de simulación** en la Etapa 4.

---

## 5. Conclusiones

1. **Random Forest** se adopta como modelo de producción (`modelos/RandomForest_best.pkl`).  
2. **SVR** se conserva como *benchmark* secundario debido a su competitividad y menor varianza.  
3. La explicación de la ansiedad mediante **sólo rasgos musicales** es viable (R²≈0.59), lo cual valida la exclusión de variables clínicas para mitigar circularidad.

---

## 6. Próximos pasos (Etapa 4)

* Ejecutar simulaciones Monte Carlo variando los cuatro predictores clave (horas, BPM, volumen, diversidad).  
* Analizar la elasticidad de la ansiedad a cambios marginales en dichos parámetros.  
* Documentar políticas de intervención musical personalizadas.

---

**Autor:** Alessa Marie Tabares Pardo  
**Curso:** Métodos Cuantitativos  

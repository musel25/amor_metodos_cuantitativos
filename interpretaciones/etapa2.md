# Insight inicial sobre **Hours per day** y **Anxiety**

Durante la depuración detecté valores imposibles en `Hours per day` (p. ej. “40 h diarias”).  
Para evitar que estos extremos distorsionaran las métricas, apliqué **winsorización suave** (truncado en los percentiles 1 y 99).

---

## 1. Panorama descriptivo

| Variable | n | Media | DE | Asimetría | Curtosis | Lectura rápida |
|----------|--:|------:|---:|----------:|---------:|----------------|
| **Hours per day** | 736 | **3.52 h** | 2.75 | **+1.67** | **3.10** | Distribución marcadamente **sesgada a la derecha**: la mayoría escucha poca música, pero existe una cola de “heavy listeners” (> 10 h). |
| **Anxiety** | 736 | **5.84** | 2.79 | −0.42 | −0.77 | Valores moderados en la escala 0-10; ligera cola hacia puntuaciones bajas. |

---

## 2. ¿Son normales las distribuciones?

| Variable | Anderson-Darling A² | KS D (p) | Conclusión |
|----------|-------------------:|---------:|------------|
| Hours per day | 35.66 | 0.206 (p < 0.001) | **No normal** |
| Anxiety        | 12.63 | 0.152 (p < 0.001) | **No normal** |

Ambas variables violan la normalidad, lo que aconseja métodos no paramétricos o transformaciones en análisis posteriores.

---

## 3. Valores atípicos

* **Hours per day**: 40 observaciones siguen fuera del rango IQR; representan a los oyentes intensivos.  
* **Anxiety**: sin outliers según la regla 1.5·IQR.

---

## 4. Relación entre tiempo de escucha y ansiedad

| Métrica | Valor | p-valor | Interpretación |
|---------|------:|--------:|----------------|
| **Pearson r** | 0.060 | 0.103 | Correlación lineal **muy débil y no significativa**. |
| **Spearman ρ** | 0.094 | 0.010 | Asociación monótona **débil**; explica < 1 % de la variabilidad. |

> **Conclusión preliminar:** más horas de música no se traducen, de forma relevante, en mayor o menor ansiedad.

---

## 5. Regresión lineal (Anxiety ~ Hours per day)

`Anxiety = 5.62 + 0.06 × Hours per day`  
* Coeficiente de la pendiente: **+0.06 puntos** de ansiedad por cada hora extra (p = 0.103, **no significativo**).  
* R² ≈ **0.3 %** → el modelo prácticamente no explica variación en ansiedad.

---

## 6. Implicaciones y próximos pasos

1. **Efecto mínimo:** El tiempo de exposición musical, aislado, apenas incide en la ansiedad autoinformada.  
2. **Distribución sesgada:** La presencia de “heavy listeners” sugiere analizar la variable de forma categórica (p. ej. ≤ 1 h, 1-3 h, 3-6 h, > 6 h) y comparar medianas (Kruskal-Wallis).  
3. **Factores de confusión:** Género musical, actividad simultánea, propósito de la escucha y características demográficas podrían enmascarar relaciones más sutiles.  
4. **Modelos robustos / multivariados:** Regresiones cuantílicas o modelos con variables de contexto pueden arrojar luz donde el OLS falla.

En conjunto, los datos sugieren que **la cantidad de música escuchada por día, por sí sola, no es un predictor sustancial de ansiedad** en esta población.

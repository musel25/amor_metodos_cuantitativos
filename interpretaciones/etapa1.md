# Etapa 1 – Interpretación de figuras

A continuación se resumen los hallazgos principales de cada visualización generada durante la exploración inicial. (Las imágenes se guardaron en `figs_etapa1/`; aquí se citan por nombre de archivo).

---

## 1. Distribución de género favorito  
![Distribución del género favorito](figs_etapa1/fav_genre_dist.png)

**Lo que muestra**  
Un conteo horizontal de los géneros preferidos.  

**Hallazgos**  

| Puesto | Género | Observación |
|-------:|--------|-------------|
| 1 | **Rock** | Casi 190 respuestas ≈ 26 % del total. Muestra ser el género dominante en la muestra. |
| 2 | **Pop** | ~115 respuestas; confirma la popularidad transversal de este estilo. |
| 3 | **Metal** | ~90 respuestas; llama la atención la fuerza del metal comparado con otros estudios. |
| 4 | **Classical** | ~55 encuestados; posible sesgo hacia perfiles “instrumentalistas”. |
| 5 | **Video Game Music / EDM / Hip-hop** | Competencia cerrada; refleja gustos eclécticos. |

> **Interpretación general:**  
> - La muestra está fuertemente inclinada hacia géneros de alta energía (Rock, Metal, Pop).  
> - Los géneros minoritarios (Latin, Gospel, Lofi) representan < 5 % cada uno, por lo que cualquier análisis específico de esos subgrupos requerirá muestras mayores.

---

## 2. Horas de música al día vs Salud Mental promedio  
![Horas de música vs salud mental](figs_etapa1/hours_vs_mh_avg.png)

**Lo que muestra**  
Boxplots del puntaje medio de salud mental (`MH_avg`) según cuatro rangos de escucha diaria.

**Lectura rápida**

| Rango (horas) | Mediana `MH_avg` | Tendencia observada |
|---------------|-----------------:|---------------------|
| ≤ 1 h | ~3.5 | Menor puntuación; distribución compacta. |
| 1 – 3 h | ~4.2 | Ligero aumento y mayor dispersión. |
| 3 – 6 h | ~5.0 | Mediana más alta; colas inferiores siguen presentes. |
| > 6 h | ~5.7 | Mediana y cuartiles superiores más altos; rango amplio. |

> **Interpretación:**  
> - Existe una **tendencia ascendente**: quienes escuchan más horas reportan puntajes globales de salud mental más altos (menos síntomas).  
> - No obstante, la **varianza crece** con el tiempo de escucha: oír música muchas horas puede asociarse tanto a bienestar como a problemáticas específicas en ciertos individuos.  
> - El efecto es **moderado**; se requeriría un test no paramétrico (p. ej. Kruskal-Wallis) para confirmar la significación.

---

## 3. Relación BPM – Ansiedad  
![BPM vs ansiedad](figs_etapa1/bpm_vs_anxiety.png)

**Lo que muestra**  
Dispersión de BPM del género favorito frente al puntaje de ansiedad, con línea de regresión (OLS).

**Hallazgos clave**

* **Pendiente positiva leve:** a mayor BPM del género favorito, la ansiedad tiende a ser ligeramente más alta.  
* **Gran dispersión:** R² visualmente muy bajo (la nube de puntos es ancha y densa).  
* **Interpretación prudente:**  
  - La relación es **débil**; la mayoría de la varianza en ansiedad **no** se explica solo por la preferencia de BPM.  
  - Puede existir un subgrupo que prefiera música rápida para regular ansiedad (hipótesis de *coping*), pero la evidencia gráfica no es concluyente.  
  - Recomendación: usar **Spearman ρ** o modelos multivariados que incluyan variables de contexto (horas de escucha, género, actividad mientras escucha).

---

## 4. Matriz de correlación de variables numéricas  
![Matriz de correlación](figs_etapa1/corr_matrix.png)

**Puntos salientes**

1. **Alta colinealidad entre escalas de salud mental**  
   * Anxiety ↔ Depression (~ 0.70 – 0.75)  
   * Anxiety ↔ Insomnia / OCD (0.4 – 0.6)  
   * Depresión también correlaciona con Insomnia y OCD.  
   > Esto sugiere que los cuatro constructos comparten varianza—útil para crear un índice global, pero cuidado con multicolinealidad en modelos.

2. **Edad** presenta correlaciones débiles (≤ |0.15|) con horas de música, BPM y salud mental.  
   * Posible ligero fenómeno de “a mayor edad, menos horas de escucha”.

3. **Horas per day** apenas correlaciona con salud mental (tonos rosados suaves).  
   * Confirma la tendencia moderada vista en la Figura 2.  

4. **Frecuencias de géneros:**  
   * Correlaciones positivas entre casi todos los items `Frequency[...]` (0.2 – 0.4).  
   * Interpretable como “escuchas más de un género cuando en general escuchas mucha música”.

5. **BPM** no muestra correlaciones relevantes (< 0.1) excepto la ligera relación con Anxiety observada en la Figura 3.

> **Conclusión práctica:**  
> - Los **constructos de salud mental pueden modelarse conjuntamente** (p. ej. PCA o un modelo de ecuaciones estructurales).  
> - Las **horas de escucha y BPM** son candidatos a predictores, pero su efecto aislado es pequeño.  
> - Pocas relaciones fuertes con edad, lo cual simplifica el control por covariables demográficas en análisis posteriores.

---

## Conclusión general de la Etapa 1

1. **Muestra predominante de rock/pop y oyentes frecuentes de música** – posible sesgo cultural.  
2. **Tendencia moderada**: más horas de música → mejor autopercepción en salud mental, aunque con gran variabilidad individual.  
3. **BPM** del género favorito tiene **poca capacidad predictiva** de ansiedad de forma aislada.  
4. **Escalas de salud mental** se comportan como dimensiones correlacionadas, recomendando modelos multivariados o índices compuestos.  
5. No se detectaron patrones fuertes con la edad ni outliers que distorsionen las métricas.

Estos hallazgos informan la **Etapa 2 (análisis estadístico profundo)**, donde se aplicarán métodos robustos y se evaluará el efecto conjunto de variables musicales sobre la salud mental.


## Variables clave a profundizar

| Variable | Tipo | Razones para seleccionarla |
|----------|------|----------------------------|
| **Hours per day**<br>(horas que la persona escucha música al día) | Continua · Conductual | - Exhibe un **gradiente positivo** con la salud mental promedio: a mayor tiempo de escucha, mejor puntaje (ver `hours_vs_mh_avg.png`).<br>- Es un **factor modificable**, ideal para diseñar intervenciones sobre la “dosis” musical.<br>- La cuantificación de exposición diaria a la música está poco explorada en la literatura; este dataset permite estimar umbrales de beneficio. |
| **Anxiety**<br>(escala 0-10) | Resultado psicológico | - Presenta la **mayor varianza** entre las escalas de salud mental y fuertes correlaciones con Depression, Insomnia y OCD (ρ ≈ 0.4–0.75), convirtiéndola en un **proxy central** de malestar emocional.<br>- Muestra relaciones (aunque débiles) con BPM y Hours per day, lo que posibilita modelar interacciones entre cantidad/intensidad musical y ansiedad.<br>- Distribución no normal (Anderson-Darling A² = 12.6); motiva aplicar métodos robustos y exploraciones adicionales. |

> **Síntesis:**  
> *Hours per day* actúa como variable de **exposición musical**, mientras que *Anxiety* es un indicador sensible del **estado emocional**. Juntas ofrecen la combinación más directa y accionable para responder:  
> **“¿Cómo influye la cantidad de música que escuchamos en nuestro nivel de ansiedad?”**

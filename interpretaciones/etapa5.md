# Etapa 5 – Conclusiones e Insights
**Proyecto:** Influencia de variables musicales sobre la Ansiedad  
**Autor:** Alessa Marie Tabares Pardo  
**Curso:** Métodos Cuantitativos  
**Fecha:** 1 junio 2025

---

## Objetivo Inicial Revisitado

**Problema declarado:** Determinar cómo los hábitos y preferencias musicales influyen en los niveles de ansiedad autoreportados, con el fin de desarrollar recomendaciones basadas en evidencia para el uso terapéutico de la música en el manejo de la ansiedad.

---

## Insights Relevantes

### 1. **La "Dosis Musical" Tiene Efectos No Lineales Sobre la Ansiedad**
- **Hallazgo:** Existe una relación en forma de "U invertida" entre exposición musical y ansiedad.
- **Evidencia:** Las simulaciones muestran que aumentar a +10h/día reduce la ansiedad en 6.4%, mientras que restringir a ≤0.5h/día la aumenta en 1.4%.
- **Implicación:** No es simplemente "más música = menos ansiedad", sino que existe un rango óptimo de exposición musical que maximiza los beneficios ansiolíticos.

### 2. **El Contexto de Escucha Importa Más Que la Cantidad Pura**
- **Hallazgo:** Escuchar música "mientras se trabaja" tiene efectos ansiolíticos comparables (-0.7%) con menor tiempo de exposición que el escenario de alta intensidad.
- **Evidencia:** El modelo Random Forest captura interacciones complejas entre variables musicales que sugieren efectos contextuales.
- **Implicación:** Las intervenciones musicales deben considerar el **cuándo** y **para qué** se escucha música, no solo el **cuánto**.

### 3. **La Variabilidad Individual Es el Factor Dominante**
- **Hallazgo:** La desviación estándar (~2.0-2.3) representa 35-40% del rango total de ansiedad en todos los escenarios.
- **Evidencia:** R² = 0.588 indica que 41% de la variación en ansiedad NO se explica por variables musicales.
- **Implicación:** Las recomendaciones musicales deben ser **altamente personalizadas**; lo que funciona para una persona puede no funcionar para otra.

### 4. **Los Géneros de Alta Energía Dominan, Pero No Necesariamente Predicen Ansiedad**
- **Hallazgo:** Rock (26%), Pop (16%) y Metal (13%) dominan las preferencias, pero BPM tiene correlaciones débiles con ansiedad (ρ = 0.094).
- **Evidencia:** El modelo prioriza `Hours per day` y `Volume_mean` sobre `BPM_fav_genre` en importancia.
- **Implicación:** La **intensidad de la exposición** (volumen, duración) puede ser más relevante que el **tipo de contenido** (género, tempo) para efectos ansiolíticos.

### 5. **Existe un "Umbral de Deprivación Musical"**
- **Hallazgo:** Restringir severamente la música (<30 min/día) produce los niveles más altos de ansiedad predicha.
- **Evidencia:** El escenario ≤0.5h/día es el único que aumenta la ansiedad respecto al baseline.
- **Implicación:** La música podría ser una **necesidad emocional básica**; su ausencia genera más malestar que su presencia en exceso.

### 6. **Las Variables Musicales Forman Clusters de Comportamiento**
- **Hallazgo:** Alta colinealidad entre frecuencias de géneros (r = 0.2-0.4) sugiere perfiles de "omnívoros musicales".
- **Evidencia:** Matriz de correlación muestra que quienes escuchan un género frecuentemente tienden a escuchar otros también.
- **Implicación:** Las intervenciones deben considerar **diversidad musical** como factor protector, no solo géneros específicos.

---

## Diagnóstico Integral

### ¿Qué le faltó a la base de datos?

#### **Variables Contextuales Críticas**
- **Momento de escucha:** ¿Cuándo durante el día se consume música? (mañana/tarde/noche)
- **Propósito de escucha:** ¿Para relajarse, concentrarse, hacer ejercicio, socializar?
- **Dispositivo/Entorno:** ¿Auriculares vs altavoces? ¿En casa vs transporte público?
- **Acompañamiento:** ¿Solo vs en compañía? ¿Escucha activa vs background?

#### **Variables Longitudinales**
- **Historial temporal:** Cambios en preferencias musicales a lo largo del tiempo
- **Episodios de ansiedad:** Relación entre picos de ansiedad y cambios en hábitos musicales
- **Estacionalidad:** Variaciones según época del año o eventos vitales

#### **Variables Sociodemográficas Enriquecidas**
- **Nivel socioeconómico:** Acceso a servicios de streaming, conciertos, instrumentos
- **Formación musical:** ¿Toca algún instrumento? ¿Educación musical formal?
- **Red social:** Influencia de amigos/familia en preferencias musicales

### ¿Qué más se pudiera hacer con esta información?

#### **Análisis Avanzados Propuestos**
1. **Clustering de Perfiles Musicales**
   - K-means o clustering jerárquico para identificar arquetipos de oyentes
   - Análisis de supervivencia para "tiempo hasta cambio de preferencias"

2. **Modelos de Series Temporales**
   - ARIMA para predecir evolución de ansiedad basada en patrones musicales históricos
   - Análisis de cambio de régimen para detectar "puntos de inflexión" terapéuticos

3. **Análisis de Redes**
   - Grafos de transición entre géneros musicales
   - Centralidad de géneros en la red de preferencias

4. **Modelado Causal**
   - Variables instrumentales para establecer causalidad música → ansiedad
   - Experimentos naturales aprovechando cambios en plataformas de streaming

### ¿Qué otros modelos hubiéramos podido obtener?

#### **Modelos de Machine Learning Alternativos**
1. **XGBoost/LightGBM:** Para capturar interacciones de orden superior
2. **Redes Neuronales (MLP):** Para patrones no lineales complejos
3. **Modelos de Mezcla Gaussiana:** Para identificar subpoblaciones latentes
4. **Isolation Forest:** Para detección de anomalías en perfiles musicales

#### **Modelos Estadísticos Especializados**
1. **Regresión Beta:** Para modelar ansiedad como proporción (0-10 reescalada)
2. **Modelos Multinivel:** Para efectos grupales por género musical favorito
3. **Regresión Cuantílica:** Para entender efectos diferenciales en distintos percentiles de ansiedad
4. **Modelos de Ecuaciones Estructurales:** Para relaciones causales entre constructos latentes

### ¿Qué otros datos podríamos agregar?

#### **Datos Biométricos**
- **Frecuencia cardíaca** durante escucha musical
- **Calidad del sueño** medida objetivamente (actigrafía)
- **Cortisol salival** como marcador de estrés
- **Variabilidad de frecuencia cardíaca** como indicador de activación del sistema nervioso autónomo

#### **Datos Comportamentales Digitales**
- **Metadatos de Spotify/Apple Music:** Skips, repeticiones, volumen por canción
- **Patrones de uso de smartphone:** Correlación entre uso de apps de música y otras apps
- **Actividad en redes sociales:** ¿Comparte música? ¿Comenta sobre artistas?

#### **Datos Ambientales**
- **Clima y estación:** Influencia de factores ambientales en preferencias
- **Eventos sociales:** Conciertos, festivales, eventos musicales asistidos
- **Ruido ambiental:** Niveles de ruido en entorno habitual

### ¿Qué preprocesamiento/transformación se debería hacer sobre los datos?

#### **Transformaciones Estadísticas**
1. **Transformación Box-Cox** para normalizar distribuciones sesgadas (Hours per day)
2. **Escalado robusto** usando mediana y MAD en lugar de media y desviación estándar
3. **Imputación multivariada** usando MICE para valores faltantes
4. **Detección de outliers multivariada** usando elipses de Mahalanobis

#### **Ingeniería de Características Avanzada**
1. **Índices compuestos:**
   - Índice de "Intensidad Musical" = (Hours × Volume × Diversity)
   - Índice de "Coherencia de Género" basado en consistencia de preferencias
2. **Variables de interacción:**
   - Hours per day × BPM_fav_genre
   - Age × Diversity_index
3. **Características temporales:**
   - Tendencias y estacionalidades si hubiera datos longitudinales
4. **Reducción de dimensionalidad:**
   - PCA para frecuencias de géneros
   - Factor analysis para construir dimensiones latentes de preferencias

#### **Validación y Robustez**
1. **Cross-validation estratificada** por género musical favorito
2. **Validación temporal** si hubiera datos secuenciales
3. **Bootstrap paramétrico** para intervalos de confianza robustos
4. **Análisis de sensibilidad** a diferentes esquemas de imputación

---

## Recomendaciones Estratégicas

### Para Aplicaciones Terapéuticas
1. **Desarrollo de una "Escala de Dosis Musical"** personalizada
2. **Protocolos de prescripción musical** basados en perfiles individuales
3. **Apps de monitoreo** que ajusten recomendaciones musicales en tiempo real

### Para Investigación Futura
1. **Estudios longitudinales** con mediciones repetidas
2. **Ensayos clínicos controlados** de intervenciones musicales
3. **Estudios de neuroimagen** para entender mecanismos cerebrales

### Para Industria Musical
1. **Algoritmos de recomendación** que consideren bienestar emocional
2. **Funcionalidades de "modo terapéutico"** en plataformas de streaming
3. **Colaboraciones** con profesionales de salud mental

---

## Conclusión Final

Este análisis demuestra que la relación entre música y ansiedad es **compleja, individualizada y contextualmente dependiente**. Aunque identificamos patrones consistentes (como el efecto protector de la exposición musical moderada-alta), la alta variabilidad individual sugiere que las intervenciones exitosas requerirán **personalización sofisticada** basada en perfiles multidimensionales que vayan más allá de simples preferencias de género.

El **potencial terapéutico de la música** es real pero requiere un enfoque científico riguroso que combine big data, machine learning y comprensión clínica profunda para maximizar sus beneficios en el manejo de la ansiedad.
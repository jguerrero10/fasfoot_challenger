# Análisis y Predicción de Ventas vs Lluvia – FastFood

Este proyecto tiene como objetivo evaluar la relación entre las precipitaciones en diferentes regiones de Bogotá y el volumen de ventas de las tiendas de comida rápida FastFood.

---

## Flujo del proyecto

1. **ETL con Python**:
   - Extracción de datos desde MySQL y MongoDB Atlas.
   - Unificación y transformación de ventas con eventos meteorológicos.
   - Generación de un dataset listo para análisis.

2. **Modelado predictivo**:
   - Modelo `RandomForestRegressor` entrenado con datos de precipitación, región y tienda.
   - R² = 0.78 | MAE = 11.35
   - Se predicen ventas en función de las lluvias y la ubicación.

3. **Análisis exploratorio y clustering**:
   - Tendencias temporales y por región.
   - Relación lluvia vs ventas.
   - Agrupación de patrones con KMeans en 3 clústeres.

---

## Estructura

- `src/`: scripts de conexión, ETL y modelado.
- `notebooks/`: análisis visual (`.ipynb`) y versión exportada en `.pdf`.

---

## Requisitos

Instalar dependencias con:

```bash
pip install -r requirements.txt

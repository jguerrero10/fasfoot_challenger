# Análisis y Predicción de Ventas vs Lluvia – FastFood

Este proyecto tiene como objetivo evaluar la relación entre las precipitaciones en diferentes regiones de Bogotá y el volumen de ventas de las tiendas de comida rápida FastFood.

---

## 🚀 Flujo del proyecto

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

## 📂 Estructura

- `src/`: scripts de conexión, ETL y modelado.
- `notebooks/`: análisis visual (`.ipynb`) y versión exportada en `.pdf`.

---

## 📦 Requisitos

Instalar dependencias con:

```bash
pip install -r requirements.txt
```

## Variables de entorno

Este proyecto utiliza variables de entorno para proteger información sensible como credenciales de conexión. Puedes definirlas de dos formas:

### Opcion 1: Usando un archivo `.env`

Crea un archivo .env en la raíz del proyecto con el siguiente contenido:

```dotenv
MONGO_URI=mongodb+srv://<usuario>:<password>@<cluster>.mongodb.net
DB_USER==<usuario_mysql>
DB_PASSWORD=<contraseña_mysql>
DB_HOST=<host_mysql>
DB_PORT=<puerto_mysql>
DB_NAME=<nombre_base_de_datos>
```

### Opción 2: Definiendo variables de entorno en tu sistema

```bash
export MONGO_URI="mongodb+srv://user:pass@cluster.mongodb.net"
export MYSQL_USER="root"
export MYSQL_PASSWORD="1234"
export MYSQL_HOST="localhost"
export MYSQL_DB="ventas"
```

## Testing
Los tests están ubicados en tests/ y cubren las funciones principales del ETL y el entrenamiento del modelo.

### Cobertura de código (coverage)

Para ejecutar la cobertura de código, asegúrate de tener `pytest` y `pytest-cov` instalados. Luego, ejecuta:

```bash
pytest --cov=src tests/
```
Esto generará un informe de cobertura en la consola y creará un archivo `htmlcov/index.html` que puedes abrir en tu navegador para ver un informe detallado.

Actualmente la cobertura es:

```plaintext
Name              Stmts   Miss  Cover
-------------------------------------
src/etl.py           45      0   100%
src/model.py         26      0   100%
src/config.py         5      0   100%
-------------------------------------
TOTAL                76      0   100%
```

También puedes generar un reporte HTML:

```bash
pytest --cov=src --cov-report=html
```

Esto generará un directorio `htmlcov` con un informe HTML que puedes abrir en tu navegador.

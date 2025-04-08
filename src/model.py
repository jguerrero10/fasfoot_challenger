import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from src.etl import run_etl

def train_model():
    print("Ejecutando ETL...")
    df = run_etl()

    # Convertir variables categóricas
    df['region_id'] = df['region_id'].astype('category')
    df['tienda_id'] = df['tienda_id'].astype('category')

    # One-hot encoding (ubicación y precipitación)
    df_encoded = pd.get_dummies(df[['precipitacion', 'region_id', 'tienda_id']])

    # Variables predictoras y target
    X = df_encoded
    y = df['ventas']

    # División train/test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Entrenar modelo
    print("Entrenando modelo RandomForest con ubicación...")
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Predicción y evaluación
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print(f"📈 MAE: {mae:.2f}")
    print(f"📊 R²: {r2:.2f}")

    # Comparar predicciones
    resultados = pd.DataFrame({
        'Fecha': df.loc[y_test.index, 'fecha_venta'],
        'Ventas reales': y_test.values,
        'Ventas predichas': y_pred
    })

    print("\nPredicciones vs Reales:")
    print(resultados.head())

    return model, resultados

if __name__ == "__main__":
    train_model()

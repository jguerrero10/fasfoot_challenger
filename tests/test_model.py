from unittest.mock import patch
import pandas as pd
from src.model import train_model


@patch("src.model.run_etl")
def test_train_model(mock_run_etl):
    # Datos simulados para cubrir toda la función
    mock_data = pd.DataFrame({
        'tienda_id': [1, 2, 3, 4],
        'region_id': [10, 20, 10, 30],
        'fecha_venta': pd.to_datetime(['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04']),
        'ventas': [100, 150, 130, 120],
        'precipitacion': [5.0, 0.0, 3.0, 2.5]
    })

    mock_run_etl.return_value = mock_data

    model, resultados = train_model()

    # Validaciones
    assert model is not None
    assert not resultados.empty
    assert 'Ventas reales' in resultados.columns
    assert 'Ventas predichas' in resultados.columns

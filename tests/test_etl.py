import pandas as pd
from unittest.mock import patch, MagicMock

from src.etl import transform_data, run_etl


def test_transform_data_basic_case():
    ventas = pd.DataFrame({
        'factura_id': [1],
        'tienda_id': [10],
        'valor_total': [100],
    })

    tickets = pd.DataFrame({
        'factura_id': [1],
        'fecha_venta': ['2023-01-01']
    })

    tiendas = pd.DataFrame({
        'id': [10],
        'region_id': [5],
    })

    sensores = pd.DataFrame({
        'id': [101],
        'region_id': [5],
    })

    eventos = pd.DataFrame({
        'Sensor_id': [101],
        'fecha': ['01/01/2023'],
        'valor': [20.5],
    })

    result = transform_data(ventas, tickets, tiendas, sensores, eventos)

    assert not result.empty
    assert 'precipitacion' in result.columns
    assert result['ventas'].iloc[0] == 100
    assert result['precipitacion'].iloc[0] == 20.5


@patch("src.etl.load_mysql_data")
@patch("src.etl.load_mongodb_data")
def test_run_etl(mock_mongo, mock_mysql):
    # Dummy MySQL Data
    ventas = pd.DataFrame({'factura_id': [1], 'tienda_id': [10], 'valor_total': [100]})
    tickets = pd.DataFrame({'factura_id': [1], 'fecha_venta': ['2023-01-01']})
    productos = pd.DataFrame()
    tiendas = pd.DataFrame({'id': [10], 'region_id': [5]})

    # Dummy Mongo Data
    sensores = pd.DataFrame({'id': [101], 'region_id': [5]})
    eventos = pd.DataFrame({'Sensor_id': [101], 'fecha': ['01/01/2023'], 'valor': [10.0]})

    mock_mysql.return_value = (ventas, tickets, productos, tiendas)
    mock_mongo.return_value = (sensores, eventos)

    df = run_etl()

    assert not df.empty
    assert 'ventas' in df.columns
    assert 'precipitacion' in df.columns


@patch("src.etl.create_engine")
def test_get_mysql_connection(mock_create_engine):
    mock_create_engine.return_value = "mock_engine"
    from src.etl import get_mysql_connection
    engine = get_mysql_connection()
    assert engine == "mock_engine"


@patch("src.etl.get_mysql_connection")
@patch("src.etl.pd.read_sql")
def test_load_mysql_data(mock_read_sql, mock_get_engine):
    mock_engine = MagicMock()
    mock_get_engine.return_value = mock_engine
    mock_read_sql.side_effect = [
        pd.DataFrame({'factura_id': [1]}),  # ventas
        pd.DataFrame({'factura_id': [1]}),  # tickets
        pd.DataFrame({'id': [1]}),          # productos
        pd.DataFrame({'id': [1]})           # tiendas
    ]

    from src.etl import load_mysql_data
    ventas, tickets, productos, tiendas = load_mysql_data()
    assert not ventas.empty and not tickets.empty

@patch("src.etl.MongoClient")
def test_load_mongodb_data(mock_mongo_client):
    mock_db = MagicMock()
    mock_db.__getitem__.side_effect = lambda name: MagicMock(find=MagicMock(return_value=[{'id': 1}]))
    mock_mongo_client.return_value = {'Prueba_Tecnica': mock_db}

    from src.etl import load_mongodb_data
    sensores, eventos = load_mongodb_data()
    assert not sensores.empty and not eventos.empty


def test_transform_data_without_valor_total():
    ventas = pd.DataFrame({
        'factura_id': [1],
        'tienda_id': [10],
        # No 'valor_total' aquí
    })

    tickets = pd.DataFrame({
        'factura_id': [1],
        'fecha_venta': ['2023-01-01'],
    })

    tiendas = pd.DataFrame({
        'id': [10],
        'region_id': [5],
    })

    sensores = pd.DataFrame({
        'id': [101],
        'region_id': [5],
    })

    eventos = pd.DataFrame({
        'Sensor_id': [101],
        'fecha': ['01/01/2023'],
        'valor': [10.0],
    })

    df = transform_data(ventas, tickets, tiendas, sensores, eventos)

    assert not df.empty
    assert 'ventas' in df.columns
    assert df['ventas'].iloc[0] == 1

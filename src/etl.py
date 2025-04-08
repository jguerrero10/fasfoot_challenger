import pandas as pd
from pymongo import MongoClient
from sqlalchemy import create_engine

from src.config import MYSQL_CONFIG, MONGO_URI


def get_mysql_connection():
    url = f"mysql+pymysql://{MYSQL_CONFIG['user']}:{MYSQL_CONFIG['password']}@{MYSQL_CONFIG['host']}:{MYSQL_CONFIG['port']}/{MYSQL_CONFIG['database']}"
    return create_engine(url)


def load_mysql_data():
    engine = get_mysql_connection()

    ventas = pd.read_sql("SELECT * FROM Ventas", con=engine)
    tickets = pd.read_sql("SELECT * FROM ticket", con=engine)
    productos = pd.read_sql("SELECT * FROM Product", con=engine)
    tiendas = pd.read_sql("SELECT * FROM Tiendas", con=engine)

    return ventas, tickets, productos, tiendas


def load_mongodb_data():
    client = MongoClient(MONGO_URI)
    db = client["Prueba_Tecnica"]

    sensores = pd.DataFrame(list(db["Ubicacion_sensores"].find()))
    eventos = pd.DataFrame(list(db["sensor_eventos"].find()))

    return sensores, eventos


def transform_data(ventas, tickets, tiendas, sensores, eventos):
    # Combinar ventas con tickets y tiendas
    ventas_tickets = ventas.merge(tickets, on='factura_id', suffixes=('', '_ticket'))
    ventas_tickets_tiendas = ventas_tickets.merge(tiendas, left_on='tienda_id', right_on='id', suffixes=('', '_tienda'))

    # Usar fecha de tickets y convertir
    ventas_tickets_tiendas['fecha_venta'] = pd.to_datetime(ventas_tickets_tiendas['fecha_venta'])

    # Simular valor_total si no existe
    if 'valor_total' not in ventas_tickets_tiendas.columns:
        ventas_tickets_tiendas['valor_total'] = 1  # placeholder si no hay monto real

    # Agrupar ventas por tienda y día
    ventas_por_dia = ventas_tickets_tiendas.groupby(
        ['tienda_id', 'region_id', ventas_tickets_tiendas['fecha_venta'].dt.date]
    ).agg({'valor_total': 'sum'}).reset_index()
    ventas_por_dia.rename(columns={'fecha_venta': 'fecha_venta', 'valor_total': 'ventas'}, inplace=True)

    # Convertir fechas de eventos de lluvia
    eventos['fecha'] = pd.to_datetime(eventos['fecha'], dayfirst=True)
    eventos['fecha_lluvia'] = eventos['fecha'].dt.date


    # Unir sensores con eventos
    eventos = eventos.merge(sensores, left_on='Sensor_id', right_on='id', suffixes=('', '_sensor'))

    # Agrupar precipitaciones por región y día
    lluvia_por_dia = eventos.groupby(['region_id', 'fecha_lluvia']).agg({'valor': 'mean'}).reset_index()
    lluvia_por_dia.rename(columns={'valor': 'precipitacion'}, inplace=True)

    # Unir con ventas
    data_final = ventas_por_dia.merge(
        lluvia_por_dia,
        left_on=['region_id', 'fecha_venta'],
        right_on=['region_id', 'fecha_lluvia'],
        how='left'
    )

    # Limpiar resultado
    data_final = data_final[['tienda_id', 'region_id', 'fecha_venta', 'ventas', 'precipitacion']]
    data_final['precipitacion'] = data_final['precipitacion'].fillna(0)

    return data_final



def run_etl():
    print("Cargando datos de MySQL y MongoDB...")
    ventas, tickets, productos, tiendas = load_mysql_data()
    sensores, eventos = load_mongodb_data()

    print("Transformando datos...")
    data_final = transform_data(ventas, tickets, tiendas, sensores, eventos)

    print("ETL completado. Dataset listo para modelado.")
    return data_final


if __name__ == "__main__":
    df = run_etl()
    print(df.head())

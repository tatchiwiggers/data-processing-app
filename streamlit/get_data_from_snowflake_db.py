import snowflake.connector
import pandas as pd
from dotenv import load_dotenv
import os
from time import time


def get_data_from_snowflake(**conn_params):
    check_snowflake = False
    start_date = time()
    try:
        # Conectar ao Snowflake
        conn = snowflake.connector.connect(**conn_params)

        # Criar um cursor para executar a consulta
        cur = conn.cursor()

        # Query para importar a tabela FINAL
        query = "SELECT * FROM ECOMMERCE_DB.DBT_TWIGGERS_DE.MART_SCRAPED_PRODUCTS;"

        # Executar a query e carregar os dados em um DataFrame
        cur.execute(query)
        data = cur.fetchall()

        # Obter os nomes das colunas
        columns = [desc[0] for desc in cur.description]

        # Criar o DataFrame
        df = pd.DataFrame(data, columns=columns)

        sf_updated_at = df['UPDATED_AT'].drop_duplicates()
        print(f"Snowflake data updated at: {sf_updated_at}")
        # Exibir os primeiros registros do DataFrame
        print(df.head())
        check_snowflake = True
    finally:
        # Fechar o cursor e a conexão, mesmo em caso de erro
        cur.close()
        conn.close()
        end_date = time()
        execution_time = round(end_date - start_date, 2)

    return check_snowflake, sf_updated_at[0], execution_time, df

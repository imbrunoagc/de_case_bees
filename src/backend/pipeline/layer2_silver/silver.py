import os
import sys
import re
from loguru import logger

from unidecode import unidecode

import duckdb
import pandas as pd
from pydantic import BaseModel
from enum import Enum
from datetime import datetime

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, "..", "..", ".."))
data_dir = os.path.abspath(os.path.join(current_dir, "..", "..", "..", "..", "data"))


sys.path.append(parent_dir)

from resources.duckdb_manager import create_duckdb_connection, execute_query
from resources.s3_manager import PandasBucket
from pipeline.layer2_silver.tdd import validate_and_convert_to_df # import do tdd (contrato de dados)

def metadata(df: pd.DataFrame) -> pd.DataFrame:
    """Info de processamento"""
    df['date'] = datetime.now().strftime('%Y-%m-%d')
    df['hour'] = datetime.now().strftime('%H:%M:%S')
    df['source'] = 'openbrewerydb'
    return df

def clean_partition_value(s):
    s = str(s) if s is not None else "" # converte None ou Nan para string
    s = unidecode(s) # remove os acentos usando o unidecode
    s = re.sub(r'\s+', '_', s.strip()) #remove qualquer espaço por '_'
    s = re.sub(r'[^a-zA-Z0-9_]', '', s) # remove tudo que não for letra (a-zA-Z), número (0-9) ou underline
    s = s.lower() # joga para minusculo o conteudo string
    return s

class BreweryType(str, Enum): # Categorizando a coluna 'brewery_type'
    micro = "micro"
    large = "large"
    closed = "closed"
    brewpub = "brewpub"
    proprietor = "proprietor"
    contract = "contract"
    regional = "regional"
    planning = "planning"
    taproom = "taproom"
    bar = "bar"
    nano = "nano"
    beergarden = "beergarden"
    location = "location"


class Brewery(BaseModel):
    """
    Definição do esquema retornado da API para contrato de dados
    """

    id: str
    name: str
    brewery_type: str #| BreweryType
    address_1: str | None
    address_2: str | None
    address_3: str | None
    city: str
    state: str
    postal_code: str | None
    country: str
    longitude: float | None
    latitude: float | None
    phone: str | None
    website_url: str | None
    state: str
    street: str | None

def run_silver() -> None:
            
    # leitura do conteudo json baixado
    logger.info("Lendo 'breweries.json' do bucket 'bronze'.")
    data = PandasBucket(name="breweries").read_json(name="bronze/breweries.json")

    logger.info("Shape do dataframe derivado do JSON." )
    print(data.shape)
    
    # Chamada da função de vdt
    logger.info("Validando dados e convertendo para DataFrame." )
    df = validate_and_convert_to_df(
        data=data,
        model=Brewery
    )

    # remoção de duplicados
    logger.info("Removendo registros duplicados.")
    df = df.drop_duplicates(subset=['id'])

    # aplicar a transformação das colunas que vão ser usadas no particionamento
    logger.info("Limpando colunas de particionamento ('country' e 'state').")
    df['country'] = df['country'].apply(clean_partition_value)
    df['state'] = df['state'].apply(clean_partition_value)

    # construcao de metadados
    logger.info("Adicionando metadados de processamento.")
    df = metadata(df=df)

    # Create DuckDB connection
    duckdb_conn = None
    try:
        duckdb_conn = create_duckdb_connection()
        
        duckdb_conn.register("df_view", df)
        logger.info("DataFrame registrado como 'df_view' no DuckDB.")

        s3_target_path = 's3://silver/breweries'

        # Query para salvar os dados particionados, agora com ALLOW_OVERWRITE
        query = f"""
            COPY df_view TO '{s3_target_path}' (
                FORMAT PARQUET,
                PARTITION_BY (country, state),
                OVERWRITE_OR_IGNORE
            );
        """
        
        logger.info("Executando a query COPY para salvar dados no MinIO em: %s", s3_target_path)
        execute_query(duckdb_conn, query)
        logger.info("Dados salvos com sucesso no formato Parquet particionado.")

    except Exception as e:
        logger.error("Ocorreu um erro durante a escrita com DuckDB: %s", e)
        # Lançar a exceção novamente para que a tarefa do Airflow falhe
        raise
    finally:
        if duckdb_conn:
            duckdb_conn.close()
            logger.info("Conexão com DuckDB fechada.")

if __name__ == "__main__":
    run_silver()
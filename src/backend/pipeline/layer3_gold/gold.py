import os
import sys

from loguru import logger
import duckdb

current_dir = os.path.abspath(os.path.dirname(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, "..", "..", ".."))
data_dir = os.path.abspath(os.path.join(current_dir, "..", "..", "..", "..", "data"))
sys.path.append(parent_dir)

def run_gold() -> None:
        
    path_silver = os.path.join(data_dir, "silver", "breweries_to_silver")
    path_gold = os.path.join(data_dir, "gold", "quantity_of_breweries_per_type_and_location.parquet")
    
    # Registro no DuckDB
    try:
        logger.info("Estabelcendo conexão com o DuckDB")
        con = duckdb.connect() # conecao local com o duckdb
        logger.success("Conexão com DuckDB realizada com sucesso.")
    except Exception as e:
        logger.error("Falha ao criar a conexão com DuckDB: {error}", error=e)
        # Propagar a exceção
        raise
        
    # Remove o arquivo se já existir (Pois estou usando o COPY)
    if os.path.exists(path_gold):
        os.remove(path_gold)

    logger.info("Realizar leitura da silver + agregação final da gold")
    query = f"""
        COPY (
            SELECT
                brewery_type,
                country,
                state,
                COUNT(id) AS quantidade
            FROM parquet_scan('{path_silver}/**/*.parquet')
            GROUP BY brewery_type, country, state
            HAVING quantidade > 0
            ORDER BY quantidade DESC
        )
        TO '{path_gold}'
        (FORMAT PARQUET)
    """
    try:
        con.execute(query)
    except Exception as e:
        logger.error(f"Erro na execução da gold: {e}")

if __name__ == "__main__":
    run_gold()
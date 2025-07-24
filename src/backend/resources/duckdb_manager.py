import os
import duckdb
from loguru import logger

def create_duckdb_connection() -> duckdb.DuckDBPyConnection:
    """
    Cria e configura uma conexão DuckDB para interagir com o MinIO (S3).

    Carrega as credenciais e configurações das variáveis de ambiente e
    instala as extensões necessárias no DuckDB.

    Returns:
        Uma conexão DuckDB configurada ou None em caso de falha.
    """
    try:
        aws_access_key = os.getenv("MINIO_ACCESS_KEY")
        aws_secret_key = os.getenv("MINIO_SECRET_KEY")
        s3_endpoint_url = os.getenv("MINIO_ENDPOINT") # Ex: "minio:9000"
        aws_region = os.getenv("REGION_NAME", "us-east-1")

        # Log para verificar se as variáveis de ambiente foram carregadas
        logger.info("Configurando conexão DuckDB com o endpoint: {endpoint}", endpoint=s3_endpoint_url)
        if not all([aws_access_key, aws_secret_key, s3_endpoint_url]):
            logger.error("Variáveis de ambiente do MinIO (MINIO_ACCESS_KEY, MINIO_SECRET_KEY, MINIO_ENDPOINT) não foram encontradas.")
            raise ValueError("Credenciais do MinIO não configuradas.")

        conn = duckdb.connect()

        # Instala e carrega a extensão httpfs para acessar S3
        conn.execute("INSTALL httpfs;" )
        conn.execute("LOAD httpfs;" )

        # Configurações essenciais para o MinIO
        conn.execute("SET s3_url_style='path';")
        conn.execute("SET s3_use_ssl=false;")
        conn.execute(f"SET s3_endpoint='{s3_endpoint_url}';")
        conn.execute(f"SET s3_access_key_id='{aws_access_key}';")
        conn.execute(f"SET s3_secret_access_key='{aws_secret_key}';")
        
        # Opcional, mas bom para consistência
        conn.execute(f"SET s3_region='{aws_region}';")

        logger.success("Conexão com DuckDB e S3 configurada com sucesso.")
        return conn

    except Exception as e:
        logger.error("Falha ao criar a conexão com DuckDB: {error}", error=e)
        # Propagar a exceção para que a tarefa do Airflow falhe claramente
        raise

# A função execute_query está boa, não precisa de alterações.
def execute_query(conn: duckdb.DuckDBPyConnection, query: str) -> None:
    try:
        logger.info("Executando a query no DuckDB...")
        logger.debug("Query: {sql}", sql=query) # Use DEBUG para não poluir logs
        conn.execute(query)
        logger.success("Query executada com sucesso.")
    except Exception as e:
        logger.error("Erro ao executar a query: {error}", error=e)
        raise

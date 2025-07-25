import os
import sys

import streamlit as st
import duckdb

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, "..", ".."))
data_dir = os.path.abspath(os.path.join(parent_dir, "data"))
sys.path.append(parent_dir)
print(os.listdir(parent_dir))

def analyze_brewery_data(con, df):
    """Realiza análises dos dados de cervejarias usando DuckDB"""
    
    # Análise 1: Contagem por tipo e localidade
    query1 = """
    SELECT
        *
    FROM df
    """
    result1 = con.execute(query1).fetchdf()
    
    # Análise 2: Contagem por tipo
    query2 = """
    SELECT
        brewery_type,
        SUM(quantidade) AS total
    FROM df
    GROUP BY brewery_type
    ORDER BY total DESC
    """
    result2 = con.execute(query2).fetchdf()
    
    # Análise 3: Contagem por estado
    query3 = """
    SELECT
        state,
        SUM(quantidade) AS total
    FROM df
    GROUP BY state
    ORDER BY total DESC
    """
    result3 = con.execute(query3).fetchdf()
    
    return result1, result2, result3


def main():
    st.set_page_config(
        page_title="Análise de Cervejarias",
        page_icon="🍺",
        layout="wide"
    )
    
    st.title("🍺 Análise de Cervejarias com DuckDB e MinIO")
    st.markdown("---")

    conn_duckdb = duckdb.connect()
    file_path = os.path.join(data_dir, 'gold', 'quantity_of_breweries_per_type_and_location.parquet')

    df = conn_duckdb.query(f"""
        SELECT * FROM read_parquet('{file_path}')
    """).to_df()

    # Mostrar card com números resumidos
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total de Cervejarias", len(df))
    with col2:
        st.metric("Tipos Únicos", df['brewery_type'].nunique())
    with col3:
        st.metric("Estados", df['state'].nunique())
    
    # Mostrar o top 10
    st.subheader("📋 Exibição dos Dados")
    st.dataframe(df.head(10), use_container_width=True)

    with st.spinner("Executando consultas SQL..."):
        result1, result2, result3 = analyze_brewery_data(conn_duckdb, df)
    
    # Mostrar os resultados
    tab1, tab2, tab3 = st.tabs(["📈 Por Tipo e Localidade", "🏷️ Por Tipo", "🗺️ Por Estado"])
    
    with tab1:
        st.dataframe(result1, use_container_width=True)
    
    with tab2:
        st.dataframe(result2, use_container_width=True)
    
    with tab3:
        st.dataframe(result3, use_container_width=True)
    
    
    # Informações adicionais
    st.subheader("ℹ️ Informações Técnicas")
    
    with st.expander("Sobre a Implementação"):
        st.markdown("""
        **Tecnologias Utilizadas:**
        - **DuckDB**: Banco de dados analítico para consultas SQL rápidas | Camada GOLD
        - **MinIO**: Objeto storage S3
        - **Streamlit**: Framework para aplicações web com Python
        
        **Funcionalidades:**
        - Conexão com MinIO para leitura de arquivos Parquet particionados
        - Análise de dados usando SQL no DuckDB
        - Visualizações em tabelas resumidas
        - Interface intuitiva
        """)
    
    conn_duckdb.close() # Fechar conexão DuckDB

if __name__ == "__main__":
    main()
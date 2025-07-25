# 🍻 Data Engineering Case Bees

Este projeto de arquitetura open source tem como foco a coleta de Breweries da `Open Brewery DB`, com armazenamento em um `data lake` e exibição em um dashboard interativo. A construção visa boas práticas e clareza em todos os aspectos, da arquitetura à escrita do código.

## Objetivos

- Implementar um data lake seguindo a arquitetura `medallion`.
- Utilizar frameworks que sejam compreensíveis e simples na resolução do case.
- Armazenar os dados na camada Bronze em formato JSON com Python.
- Realizar transformações nas camadas Silver e Gold com `Pandas e DuckDB` salvando no formato Parquet.
- Utilizar o Airflow para orquestrar as camadas.
- Utilizar o `Loguru` para dar visibilidade em cada etapa do projeto.
- Criar um dashboard com `Streamlit` para visualização gráfica dos dados da camada Gold.
- Subir todos os serviços via `Docker`.

# 🍻 Data Engineering Case Bees
Este projeto de arquitetura open source tem como foco a coleta de Breweries da ``Open Breweriy DB``, com armazenamento em um ``data lake`` e exibição em um dashboard interativo. A construção visa boas práticas e clareza em todos os aspectos, da arquitetura à escrita do código.

### Objetivos:
* Implementar um data lake seguindo a arquitetura ``medallion``.
* Utilizar frameworks que seja compreensivel e simples na resolução do case.
* Armazenar os dados na camada Bronze em formato JSON com Python.
* Realizar transformações nas camadas Silver e Gold com ``Pandas e DuckDB`` salvando no formato Parquet.
* Utilizar o airflow para orquestrar as ``camadas``.
* Utlizar o ```Loguru``` para dar visibilidade em cada etapa do projeto.
* Criar um dashboard com ``Streamlit`` para visualização gráfica dos dados da camada Gold.
* Subir todos os serviços via ``Docker``.

A arquitetura proposta é a seguinte:
<table>
    <td>
    <img src="docs/architecture/architecture-version-3.png"
></img></td></tr>
</table>

**Principais ferramentas utilizadas no projeto:**  
- **Apache Airflow**: Responsável por orquestrar pipelines de dados, automatizando tarefas e seus agendamentos;  
- **MinIO**: Armazenamento de objetos gratuito usado para guardar e organizar os dados;  
- **Pandas e DuckDB**: Bibliotecas utilizadas para processar, transformar e analisar os dados;
- **Docker**: Plataforma para criar e gerenciar containers, garantindo que os serviços rodem de forma consistente;  
- **Streamlit**: Utilizado para criar interfaces simples e rápidas para visualização de dados.

## Descrição da Estrutura do Projeto
* `.git` - Controle de versão.
* `.venv` - Ambiente virtual com dependências do projeto.
* `.gitignore` - Arquivo de exclusões do Git.
* `.python-version` - Versão do python utilizada no projeto.
* `requirements.txt` - Dependências do projeto.
* `pyproject.toml` - Configurações e dependências do projeto com Poetry. 
* `README.md` - Documentação principal do projeto.
* `docs/` - Documentação do projeto.
* `src/backend/` - Arquivo com a construção do backend de dados.
* `src/frontend/` - Arquivo com a construção visual da entrega final.


## Estrutura do Projeto

```bash
|
|── .gitignore
|── .python-version
|── requirements.txt
|── requirements-frontend.txt
|── poetry.lock
|── pyproject.toml
|── README.md
|
|── data/
|   |── bronze/
|   |── silver/
|   └── gold/
|
|── docs/
|   |── architecture/
|   └── assets/
|
|── src/
|   |── backend/
|   |       |── airflow/
|   |       |── api/
|   |       |── dags/
|   |       |── pipeline/
|   |       └── utils/
|   |
|   └── frontend
|           └── app.py
|
|
|── .dockerignore
|── .docker-compose.yml
|── airflow.Dockerfile
└── streamlit.Dockerfile


```



## ✅ Setup do Projeto

### 1. Clone o repositório

**HTTPS**
```bash
#### **1. Clone o repositório em HTTPS
git clone https://github.com/imbrunoagc/de_case_bees.git
cd de_case_bees
```

ou via, **SSH**.

```bash
#### **2. Clone o repositório em SSH**
git clone git@github.com:imbrunoagc/de_case_bees.git
cd de_case_bees
```

#### **3. Execute o projeto**
```bash
> docker-compose up --build
``` 

#### **📦 4. Serviços Disponíveis**
* Mini IO > ````Não implementado nessa branch````
* Airflow > http://localhost:8080/
* Streamlit > http://localhost:8501/
* MkDocs > 

### Visualização dos Containers
<table><td><img src="docs/assets/img1_services_docker_desktop.png"></img></td></tr></table>


### Airflow

Acesse via: http://localhost:8080

**Credenciais de acesso:**

* **Usuário:** ``admin``
* **Senha:** gerada automaticamente em
``src/backend/standalone_admin_password.txt``

```⚠️ A cada rebuild do docker-compose, a senha é regenerada.```

**Recuperação da senha:**
<table>
    <td>
    <img src="docs/assets/img2_service_airflow_get_password.png"
></img></td></tr>
</table>


**Tela de Login**
<table>
    <td>
    <img src="docs/assets/img2_service_airflow_login.png"
></img></td></tr>
</table>

**DAG disponível**
<table>
    <td>
    <img src="docs/assets/img3_service_airflow_dag.png"
></img></td></tr>
</table>


### Streamlit

Acesse via: http://localhost:8501

```A interface só será exibida após a ingestão de dados na camada gold.```
<table>
    <td>
    <img src="docs/assets/img4_service_streamlit.png"
></img></td></tr>
</table>


#### MkDocks

Utilizado para formatação e visualização da documentação técnica do projeto.
<table>
    <td>
    <img src="docs/ssets/.png"
></img></td></tr>
</table>


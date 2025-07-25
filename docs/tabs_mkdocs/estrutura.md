# Estrutura do Projeto

## Arquivos principais

- `.git` – Controle de versão.
- `.venv` – Ambiente virtual com dependências.
- `.gitignore` – Exclusões do Git.
- `.python-version` – Versão do Python.
- `requirements.txt` – Dependências gerais.
- `pyproject.toml` – Configuração com Poetry.
- `README.md` – Documentação principal.
- `docs/` – Documentação técnica.
- `src/backend/` – Backend de dados.
- `src/frontend/` – Interface visual com Streamlit.

## Estrutura de diretórios

```bash
.
├── data/
│   ├── bronze/
│   ├── silver/
│   └── gold/
│
├── docs/
│   ├── architecture/
│   └── assets/
│
├── src/
│   ├── backend/
│   │   ├── airflow/
│   │   ├── api/
│   │   ├── dags/
│   │   ├── pipeline/
│   │   └── utils/
│   └── frontend/
│       └── app.py
│
├── .dockerignore
├── docker-compose.yml
├── airflow.Dockerfile
└── streamlit.Dockerfile

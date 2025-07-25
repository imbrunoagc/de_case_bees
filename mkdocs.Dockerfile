# mkdocs.Dockerfile
FROM python:3.12.2

# Evita prompts interativos
ENV DEBIAN_FRONTEND=noninteractive

# Instala dependências
RUN pip install --no-cache-dir mkdocs mkdocs-material

# Define diretório de trabalho
WORKDIR /docs

# Porta padrão do MkDocs
EXPOSE 8000

# Comando padrão
CMD ["mkdocs", "serve", "--dev-addr=0.0.0.0:8000"]

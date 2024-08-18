FROM python:3.8-slim

# Instalar as dependências de desenvolvimento do PostgreSQL
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Definir o diretório de trabalho
WORKDIR /app

# Copiar os arquivos do projeto para o contêiner
COPY . /app

# Instalar as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Comando para iniciar a aplicação
CMD ["python", "main.py"]

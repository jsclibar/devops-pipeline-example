# Imagem oficial do Python
FROM python:3.13-alpine

# Diretório da aplicação
WORKDIR /app

# Copia o arquivo de dependências
COPY requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia a aplicação
COPY backend_app.py .

# Expõe a porta do Uvicorn
EXPOSE 8000

# Verifica se a API está respondendo
HEALTHCHECK CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/')" || exit 1

# Inicializa o Uvicorn
CMD ["uvicorn", "backend_app:app", "--host", "0.0.0.0", "--port", "8000"]
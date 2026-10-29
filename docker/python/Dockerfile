# Imagem oficial do Python
FROM python:3.13-alpine

# Diretório da aplicação
WORKDIR /app

# Atualiza o SO
RUN apk update && apk upgrade --no-cache

# Copia o arquivo de dependências
COPY requirements.txt .

# Instala as dependências
#RUN pip install --no-cache-dir -r requirements.txt

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt \
    && pip uninstall -y pip

# Copia a aplicação
COPY backend_app.py .

# Cria um usuário sem privilégios administrativos
RUN adduser -D appuser

# Executa a aplicação como usuário não-root
USER appuser

# Expõe a porta do Uvicorn
EXPOSE 8000

# Verifica se a API está respondendo
HEALTHCHECK CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/')" || exit 1

# Inicializa o Uvicorn
CMD ["uvicorn", "backend_app:app", "--host", "0.0.0.0", "--port", "8000"]

# FIM
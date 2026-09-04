# DevOps Pipeline Example

Projeto de exemplo para estudo de **Docker**, **Docker Compose**, **Nginx** e **PHP-FPM**.

---

# Arquitetura

```
Browser
    │
localhost:8080
    │
    ▼
 Nginx
    │
FastCGI
    │
    ▼
PHP-FPM
```

---

# Estrutura

```text
.
├── docker/
│   ├── nginx/
│   └── php/
├── public/
├── compose.dev.yaml
├── compose.prod.yaml
└── README.md
```

---

# Requisitos

- Docker
- Docker Compose
- Git

---

# Desenvolvimento

Subir o ambiente:

```bash
docker compose -f compose.dev.yaml up -d --build
```

Parar:

```bash
docker compose -f compose.dev.yaml down
```

Logs:

```bash
docker compose -f compose.dev.yaml logs
```

---

# Produção

Construir as imagens:

```bash
docker build -t devops-pipeline-example-api:1.0.0 \
    -f docker/php/Dockerfile .
```

```bash
docker build -t devops-pipeline-example-web:1.0.0 \
    -f docker/nginx/Dockerfile .
```

Subir:

```bash
docker compose -f compose.prod.yaml up -d
```

Parar:

```bash
docker compose -f compose.prod.yaml down
```

---

# Executando somente o PHP

Para testar a API sem utilizar Docker ou Nginx:

```bash
php -S localhost:8000 -t public
```

Acesse:

```
http://localhost:8000
```

---

# API

Health Check

```http
GET /health
```

Usuários

```http
GET /users
```

Criar usuário

```http
POST /users
```

---

# Health Checks

## Nginx

```
GET /nginx-health
```

Verifica apenas o container do Nginx.

## PHP-FPM

```
/ping
```

Verifica apenas o PHP-FPM.

## API

```
GET /health
```

Verifica a aplicação.

---

# Comandos Úteis

Containers:

```bash
docker ps
```

Imagens:

```bash
docker images
```

Entrar no container da API:

```bash
docker exec -it devops-pipeline-example-api sh
```

Entrar no container Web:

```bash
docker exec -it devops-pipeline-example-web sh
```

Reconstruir o ambiente:

```bash
docker compose -f compose.dev.yaml up -d --build
```

---

# Próximos Passos

- GitHub Container Registry (GHCR)
- GitHub Actions
- CI/CD
- Deploy em VPS
- AWS
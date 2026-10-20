
# Aula Prática – DevOps: Docker, Redes e Segurança de Contêineres

**Data:** 21/10/2026  
**Projeto:** DevOps Pipeline Example  
**Repositório:** https://github.com/jsclibar/devops-pipeline-example

## Objetivo

Preparar o ambiente de desenvolvimento, executar uma API FastAPI, construir imagens Docker, analisar vulnerabilidades com o Trivy e configurar a comunicação entre contêineres utilizando uma rede Docker e um proxy reverso Nginx.

---

## 1. Clonar o repositório

Clonar o projeto disponibilizado no GitHub:

```bash
git clone https://github.com/jsclibar/devops-pipeline-example.git
```

Acessar o diretório do projeto:

```bash
cd devops-pipeline-example
```

**Importante:** os próximos comandos devem ser executados na raiz do projeto, salvo indicação contrária.

---

## 2. Preparar o ambiente Python

Atualizar a lista de pacotes do Ubuntu:

```bash
sudo apt update
```

Instalar o Python e as ferramentas necessárias:

```bash
sudo apt install -y python3 python3-venv python3-pip
```

Criar o ambiente virtual:

```bash
python3 -m venv .venv --prompt devops-pipeline-example
```

Ativar o ambiente virtual:

```bash
source .venv/bin/activate
```

Instalar as dependências de desenvolvimento:

```bash
python -m pip install -r requirements-dev.txt
```

Listar os pacotes instalados:

```bash
python -m pip list
```

Verificar possíveis conflitos entre as dependências:

```bash
python -m pip check
```

---

## 3. Executar a aplicação localmente

Iniciar a API utilizando o Uvicorn:

```bash
python -m uvicorn backend_app:app --reload
```

O parâmetro `--reload` reinicia automaticamente o servidor quando alterações são identificadas no código.

Verificar o funcionamento pelo navegador:

http://127.0.0.1:8000

Acessar a documentação automática da API:

http://127.0.0.1:8000/docs

Para encerrar o servidor, utilizar `Ctrl + C`.

Desativar o ambiente virtual:

```bash
deactivate
```

---

## 4. Construir a imagem Docker da API

Construir a imagem utilizando o Dockerfile localizado em `docker/python/`:

```bash
docker build -t api_backend:dev -f docker/python/Dockerfile .
```

**Parâmetros:**

- `-t api_backend:dev`: define o nome e a tag da imagem.
- `-f docker/python/Dockerfile`: indica o caminho do Dockerfile.
- `.`: define o diretório atual como contexto de build.

Listar as imagens disponíveis:

```bash
docker image ls
```

Para reconstruir a imagem sem utilizar o cache:

```bash
docker build --no-cache -t api_backend:dev -f docker/python/Dockerfile .
```

---

## 5. Instalar e utilizar o Trivy

O **Trivy** é uma ferramenta de segurança utilizada para identificar vulnerabilidades em imagens Docker e problemas de configuração em arquivos como Dockerfile.

### 5.1. Instalar o Trivy no Debian/Ubuntu

Instalar o Trivy utilizando o repositório oficial.

```bash
sudo apt-get install wget gnupg

wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | gpg --dearmor | sudo tee /usr/share/keyrings/trivy.gpg > /dev/null

echo "deb [signed-by=/usr/share/keyrings/trivy.gpg] https://aquasecurity.github.io/trivy-repo/deb generic main" | sudo tee -a /etc/apt/sources.list.d/trivy.list

sudo apt-get update

sudo apt-get install trivy
```

**Fonte:** [Documentação oficial do Trivy – Instalação](https://trivy.dev/docs/latest/getting-started/installation/)

### 5.2. Analisar a imagem Docker

Verificar vulnerabilidades na imagem da API:

```bash
trivy image api_backend:dev
```

Observar as vulnerabilidades encontradas, os níveis de severidade e as versões corrigidas disponíveis.

### 5.3. Analisar o Dockerfile

Verificar problemas de configuração:

```bash
trivy config docker/python/Dockerfile
```

O Trivy pode identificar problemas como a execução da aplicação com privilégios de root.

Após realizar eventuais correções, reconstruir a imagem Docker e executar novamente as análises.

---

## 6. Criar uma rede Docker

Criar uma rede para permitir a comunicação entre a API e o Nginx:

```bash
docker network create rede-api
```

O Docker utiliza o driver `bridge` por padrão.

Listar as redes existentes:

```bash
docker network ls
```

Inspecionar a rede criada:

```bash
docker network inspect rede-api
```

Essa rede permite a comunicação entre contêineres e oferece resolução DNS interna pelos nomes e aliases configurados.

---

## 7. Criar e executar o contêiner da API

```bash
docker run -d \
  --name backend_api \
  --hostname backend_api \
  --network rede-api \
  --network-alias api \
  -p 8000:8000 \
  api_backend:dev
```

**Parâmetros:**

| Parâmetro | Descrição |
|---|---|
| `-d` | Executa o contêiner em segundo plano |
| `--name backend_api` | Define o nome do contêiner |
| `--hostname backend_api` | Define o hostname interno |
| `--network rede-api` | Conecta à rede Docker |
| `--network-alias api` | Define o nome DNS alternativo `api` |
| `-p 8000:8000` | Publica a porta 8000 no host |
| `api_backend:dev` | Imagem utilizada |

Verificar se o contêiner está em execução:

```bash
docker ps
```

Testar o acesso à API:

```bash
curl http://localhost:8000/
```

Outros contêineres conectados à rede `rede-api` poderão acessar a aplicação pelo endereço:

```text
http://api:8000
```

---

## 8. Verificar e administrar o contêiner

### 8.1. Consultar os logs

Exibir os logs:

```bash
docker logs backend_api
```

Acompanhar os logs em tempo real:

```bash
docker logs -f backend_api
```

Utilizar `Ctrl + C` para encerrar o acompanhamento.

### 8.2. Entrar no contêiner

```bash
docker exec -it backend_api sh
```

Comandos para explorar o ambiente:

```bash
pwd
ls -la
whoami
id
hostname
python --version
cat /etc/os-release
```

Para sair:

```bash
exit
```

### 8.3. Executar comandos sem entrar no contêiner

Listar os arquivos da aplicação:

```bash
docker exec backend_api ls -la /app
```

Verificar a versão do Python:

```bash
docker exec backend_api python --version
```

Verificar o usuário utilizado:

```bash
docker exec backend_api whoami
```

### 8.4. Verificar processos e recursos

Listar os processos:

```bash
docker top backend_api
```

Verificar o consumo de CPU e memória:

```bash
docker stats backend_api
```

Para realizar uma única consulta:

```bash
docker stats --no-stream backend_api
```

### 8.5. Verificar a saúde do contêiner

Consultar o estado do HEALTHCHECK:

```bash
docker inspect --format='{{.State.Health.Status}}' backend_api
```

Estados possíveis:

- `starting`: verificações iniciais.
- `healthy`: verificação realizada com sucesso.
- `unhealthy`: verificações falhando.

### 8.6. Verificar os dados de rede

```bash
docker network inspect rede-api
```

Testar a resolução DNS do alias `api`:

```bash
docker run --rm --network rede-api busybox nslookup api
```

### 8.7. Parar, iniciar e reiniciar

Parar o contêiner:

```bash
docker stop backend_api
```

Iniciar novamente:

```bash
docker start backend_api
```

Reiniciar:

```bash
docker restart backend_api
```

**Antes de continuar para o Nginx, confirmar que a API está em execução.**

---

## 9. Construir a imagem Docker do Nginx

O Nginx será utilizado como proxy reverso, encaminhando requisições HTTP para a API FastAPI.

Construir a imagem:

```bash
docker build -t nginx:dev -f docker/nginx/Dockerfile .
```

Verificar a imagem:

```bash
docker image ls
```

Analisar vulnerabilidades:

```bash
trivy image nginx:dev
```

Analisar o Dockerfile:

```bash
trivy config docker/nginx/Dockerfile
```

---

## 10. Executar o contêiner Nginx

Considerando que a configuração do Nginx utiliza a porta interna `80`:

```bash
docker run -d \
  --name nginx_rproxy \
  --hostname nginx_proxy \
  --network rede-api \
  --network-alias nginx \
  -p 8080:80 \
  nginx:dev
```

**Importante:** se o Dockerfile estiver utilizando a imagem `nginxinc/nginx-unprivileged` e a configuração do Nginx contiver `listen 8080`, utilizar `-p 8080:8080` no lugar de `-p 8080:80`.

Verificar os contêineres:

```bash
docker ps
```

Consultar os logs do Nginx:

```bash
docker logs nginx_rproxy
```

Verificar a configuração do Nginx:

```bash
docker exec nginx_rproxy nginx -t
```

Verificar o usuário utilizado:

```bash
docker exec nginx_rproxy whoami
```

Testar o acesso pelo navegador:

http://localhost:8080

O Nginx deverá encaminhar a requisição para a API utilizando o DNS interno do Docker:

```nginx
proxy_pass http://api:8000;
```

Para isso, ambos os contêineres precisam estar conectados à rede `rede-api`.

---

## 11. Verificações finais

Confirmar os seguintes itens:

- [ ] A imagem da API foi construída corretamente.
- [ ] A análise da imagem e do Dockerfile foi realizada com o Trivy.
- [ ] A rede `rede-api` foi criada.
- [ ] O contêiner da API está em execução.
- [ ] O HEALTHCHECK da API apresenta o estado `healthy`.
- [ ] A API responde diretamente na porta 8000.
- [ ] A imagem do Nginx foi construída corretamente.
- [ ] O contêiner Nginx está em execução.
- [ ] O Nginx consegue encaminhar requisições para a API.
- [ ] A aplicação responde através do endereço `http://localhost:8080`.

---

## 12. Encerrar e limpar o ambiente

### 12.1. Parar os contêineres

```bash
docker stop nginx_rproxy backend_api
```

### 12.2. Remover os contêineres

```bash
docker rm nginx_rproxy backend_api
```

### 12.3. Remover as imagens

```bash
docker image rm nginx:dev
docker image rm api_backend:dev
```

### 12.4. Remover a rede

```bash
docker network rm rede-api
```

### 12.5. Limpeza adicional (opcional)

Para remover recursos Docker não utilizados:

```bash
docker system prune
```

Para uma limpeza mais abrangente, incluindo imagens que não estejam associadas a contêineres:

```bash
docker system prune -a
```

**Atenção:** o `docker system prune` pode remover recursos não utilizados de outros projetos Docker, e não somente os recursos desta atividade.

---

## Resultado esperado

Ao finalizar a atividade, os estudantes deverão compreender o processo básico de preparação de um ambiente Python, construção de imagens Docker, execução e administração de contêineres, análise de segurança com Trivy, comunicação por redes bridge e utilização do Nginx como proxy reverso para uma aplicação FastAPI.
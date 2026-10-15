# DevOps Pipeline Example

Projeto de exemplo para estudo de **Git, Python, FastAPI, testes automatizados, Docker, Docker Compose, Nginx e CI/CD**.

A aplicação consiste em uma API para gerenciamento de livros de uma biblioteca, permitindo realizar operações de cadastro, consulta, atualização e exclusão (CRUD).

Os dados são armazenados temporariamente em uma lista Python, sem utilização de banco de dados.

O objetivo principal deste projeto é servir como base prática para o aprendizado de DevOps, desde a preparação do ambiente de desenvolvimento até a construção de imagens Docker e a futura implementação de pipelines CI/CD.

---

# 1. Arquitetura

A aplicação utiliza dois serviços:

- **Nginx:** atua como proxy reverso, recebendo as requisições HTTP.
- **Python + FastAPI + Uvicorn:** executa a API e processa as requisições.

```text
            Cliente
               |
               | HTTP
               v
         localhost:8080
               |
               v
         Nginx (porta 80)
               |
               | HTTP
               | proxy_pass
               v
        Uvicorn (porta 8000)
               |
               v
             FastAPI
               |
               v
           API de Livros
```

O Nginx e a aplicação Python são executados em contêineres separados, conectados pela rede criada automaticamente pelo Docker Compose.

---

# 2. Estrutura do Projeto

```text
devops-pipeline-example/
│
├── backend_app.py
├── requirements.txt
├── requirements-dev.txt
│
├── tests/
│   └── test_api.py
│
├── docker/
│   ├── nginx/
│   │   ├── Dockerfile
│   │   └── default.conf
│   │
│   └── python/
│       └── Dockerfile
│
├── compose.dev.yaml
├── compose.prod.yaml
├── .dockerignore
├── .gitignore
└── README.md
```

**Principais arquivos:**

| Arquivo | Descrição |
|---|---|
| `backend_app.py` | Código da aplicação FastAPI |
| `requirements.txt` | Dependências necessárias para executar a aplicação |
| `requirements-dev.txt` | Dependências para desenvolvimento e testes |
| `tests/test_api.py` | Testes automatizados da API |
| `docker/python/Dockerfile` | Construção da imagem da aplicação Python |
| `docker/nginx/Dockerfile` | Construção da imagem do Nginx |
| `docker/nginx/default.conf` | Configuração do Nginx como proxy reverso |
| `compose.dev.yaml` | Ambiente Docker de desenvolvimento |
| `compose.prod.yaml` | Ambiente Docker de produção |

---

# 3. Requisitos

Para executar a aplicação localmente:

- Git
- Python 3.11 ou superior
- pip
- venv

Para executar a aplicação em contêineres:

- Docker
- Docker Compose

**Sistemas operacionais utilizados nas aulas:**

- Ubuntu 24.04 LTS
- Debian 13

Essas distribuições disponibilizam versões do Python compatíveis com os requisitos do projeto.

---

# 4. Instalação do Python no Debian e Ubuntu

Antes de executar a aplicação localmente, é necessário instalar o Python.

## 4.1. Atualizar os repositórios

```bash
sudo apt update
```

## 4.2. Instalar Python, pip e venv

```bash
sudo apt install -y python3 python3-venv python3-pip
```

Esse comando instala:

- `python3`: interpretador da linguagem Python.
- `python3-venv`: ferramenta para criação de ambientes virtuais.
- `python3-pip`: gerenciador de pacotes Python.

## 4.3. Verificar a instalação

```bash
python3 --version
```

Versões normalmente encontradas:

| Sistema operacional | Python |
|---|---|
| Ubuntu 24.04 | Python 3.12 |
| Debian 13 | Python 3.13 |

O projeto requer Python 3.11 ou superior.

---

# 5. Clonar o Repositório

Clone o repositório do projeto:

```bash
git clone URL_DO_REPOSITORIO
```

Entre no diretório:

```bash
cd devops-pipeline-example
```

Os próximos comandos devem ser executados na raiz do projeto.

---

# 6. Configuração do Ambiente Virtual Python

O ambiente virtual permite instalar as dependências do projeto sem modificar os pacotes Python do sistema operacional.

Cada desenvolvedor deverá criar seu próprio ambiente virtual.

## 6.1. Criar o ambiente virtual

```bash
python3 -m venv .venv --prompt devops-pipeline-example
```

O comando cria um ambiente virtual na pasta `.venv`.

O parâmetro `--prompt` define o nome exibido no terminal quando o ambiente estiver ativado.

## 6.2. Ativar o ambiente virtual

```bash
source .venv/bin/activate
```

Após a ativação, o terminal apresentará algo semelhante a:

```text
(devops-pipeline-example) usuario@ubuntu:~/devops-pipeline-example$
```

## 6.3. Verificar o interpretador Python

```bash
which python
```

O caminho deverá apontar para o ambiente virtual:

```text
/home/usuario/devops-pipeline-example/.venv/bin/python
```

Verifique também a versão:

```bash
python --version
```

---

# 7. Instalação das Dependências

O projeto utiliza dois arquivos para organizar suas dependências.

## 7.1. Dependências da aplicação

Arquivo:

`requirements.txt`

Contém as bibliotecas necessárias para executar a aplicação:

- FastAPI
- Uvicorn
- Starlette

O Pydantic e outras bibliotecas auxiliares são instalados automaticamente como dependências.

## 7.2. Dependências de desenvolvimento

Arquivo:

`requirements-dev.txt`

Inclui as dependências da aplicação e as ferramentas necessárias para executar os testes automatizados:

- pytest
- httpx2

## 7.3. Instalar as dependências

Com o ambiente virtual ativado, execute:

```bash
python -m pip install -r requirements-dev.txt
```

Esse comando instala tanto as dependências da aplicação quanto as ferramentas de teste.

Não é necessário executar os dois arquivos separadamente, pois o `requirements-dev.txt` já inclui o `requirements.txt`.

## 7.4. Verificar as dependências instaladas

```bash
python -m pip list
```

Para verificar possíveis conflitos entre dependências:

```bash
python -m pip check
```

Resultado esperado:

```text
No broken requirements found.
```

---

# 8. Executando a API Localmente

Com o ambiente virtual ativado, execute:

```bash
python -m uvicorn backend_app:app --reload
```

O Uvicorn iniciará a aplicação na porta 8000.

O parâmetro `--reload` permite reiniciar automaticamente a aplicação quando o código Python for modificado.

Esse recurso deve ser utilizado apenas durante o desenvolvimento.

## 8.1. Acessar a API

Página inicial:

```text
http://localhost:8000
```

Documentação interativa (Swagger UI):

```text
http://localhost:8000/docs
```

Lista de livros:

```text
http://localhost:8000/livros
```

Para encerrar o servidor, pressione:

`Ctrl+C`

---

# 9. Endpoints da API

A aplicação disponibiliza os seguintes endpoints:

| Método HTTP | Endpoint | Funcionalidade |
|---|---|---|
| GET | `/` | Mensagem de boas-vindas |
| GET | `/livros` | Listar todos os livros |
| GET | `/livros/{idlivro}` | Consultar um livro pelo ID |
| GET | `/livros/autor/{nome}` | Consultar livros por autor |
| POST | `/livros` | Cadastrar um livro |
| PUT | `/livros/{idlivro}` | Atualizar um livro |
| DELETE | `/livros/{idlivro}` | Excluir um livro |

## 9.1. Exemplo de cadastro

Requisição:

```http
POST /livros
```

Corpo da requisição:

```json
{
    "titulo": "O Cortiço",
    "autor": "Aluísio Azevedo",
    "ano": 1890
}
```

Resposta esperada:

```json
{
    "message": "Livro cadastrado com sucesso",
    "livro": {
        "titulo": "O Cortiço",
        "autor": "Aluísio Azevedo",
        "ano": 1890,
        "idlivro": 3
    }
}
```

O identificador é gerado automaticamente pela aplicação. No exemplo, o próximo ID disponível é 3.

**Importante:** os dados são armazenados em memória. Ao reiniciar a aplicação, os cadastros, alterações e exclusões realizados durante a execução serão perdidos.

---

# 10. Testes Automatizados

O projeto utiliza **pytest** para executar testes automatizados dos endpoints da API.

Os testes permitem verificar se as funcionalidades continuam funcionando corretamente após alterações no código.

O arquivo de testes está localizado em:

```text
tests/test_api.py
```

## 10.1. Executar os testes

Com o ambiente virtual ativado, execute:

```bash
python -m pytest -v
```

O parâmetro `-v` apresenta informações detalhadas sobre cada teste executado.

Resultado esperado:

```text
13 passed
```

Os testes verificam:

- Funcionamento da página inicial.
- Listagem de livros.
- Cadastro de livros.
- Validação de dados obrigatórios.
- Consulta de livros por ID.
- Consulta de livros por autor.
- Atualização de livros.
- Exclusão de livros.
- Tratamento de erros HTTP 404 e 422.

## 10.2. Independência dos testes

Os testes utilizam dados preparados especificamente para cada cenário.

Antes de cada teste, a lista de livros é reiniciada, evitando que alterações realizadas por um teste interfiram nos demais.

Os testes são executados diretamente pelo FastAPI TestClient.

**Não é necessário iniciar o Uvicorn ou os contêineres Docker para executar os testes automatizados.**

## 10.3. Importância para DevOps

Futuramente, os testes serão executados automaticamente pelo GitHub Actions.

Quando um desenvolvedor enviar alterações ao repositório, a pipeline poderá:

1. Preparar o ambiente Python.
2. Instalar as dependências.
3. Executar os testes automatizados.
4. Interromper a pipeline caso algum teste falhe.
5. Continuar para a construção das imagens Docker quando os testes passarem.

---

# 11. Docker — Ambiente de Desenvolvimento

O ambiente Docker de desenvolvimento utiliza dois contêineres:

- `api`: aplicação FastAPI executada pelo Uvicorn.
- `web`: Nginx configurado como proxy reverso.

O Docker Compose constrói as imagens e cria a rede necessária para a comunicação entre os serviços.

## 11.1. Construir e iniciar os contêineres

Na raiz do projeto:

```bash
docker compose -f compose.dev.yaml up -d --build
```

Esse comando:

- Constrói as imagens Docker.
- Cria os contêineres.
- Configura a rede do projeto.
- Inicia os serviços em segundo plano.

## 11.2. Acessar a aplicação

Swagger UI:

```text
http://localhost:8080/docs
```

Lista de livros:

```text
http://localhost:8080/livros
```

Healthcheck do Nginx:

```text
http://localhost:8080/nginx-health
```

Observe que agora utilizamos a porta **8080**, publicada pelo contêiner Nginx.

O Nginx encaminha as requisições para o Uvicorn, que utiliza a porta 8000 na rede interna do Docker.

## 11.3. Verificar os serviços

```bash
docker compose -f compose.dev.yaml ps
```

## 11.4. Acompanhar os logs

```bash
docker compose -f compose.dev.yaml logs -f
```

## 11.5. Parar e remover os contêineres

```bash
docker compose -f compose.dev.yaml down
```

## 11.6. Desenvolvimento com atualização automática

O ambiente de desenvolvimento utiliza um volume para compartilhar o arquivo Python entre o computador e o contêiner.

O Uvicorn é executado com:

```bash
uvicorn backend_app:app --host 0.0.0.0 --port 8000 --reload
```

Assim, alterações no código Python podem ser aplicadas automaticamente, sem necessidade de reconstruir a imagem Docker.

---

# 12. Docker — Ambiente de Produção

O ambiente de produção utiliza imagens Docker previamente construídas.

Diferentemente do ambiente de desenvolvimento:

- Não utiliza volumes para compartilhar o código-fonte.
- Não utiliza o parâmetro `--reload`.
- Executa os arquivos incorporados às imagens Docker.
- Utiliza imagens identificadas pela versão `1.0.0`.
- Possui política de reinicialização dos contêineres.

## 12.1. Construir a imagem da API

```bash
docker build -t devops-pipeline-example-api:1.0.0 \
    -f docker/python/Dockerfile .
```

## 12.2. Construir a imagem do Nginx

```bash
docker build -t devops-pipeline-example-web:1.0.0 \
    -f docker/nginx/Dockerfile .
```

## 12.3. Iniciar o ambiente de produção

```bash
docker compose -f compose.prod.yaml up -d
```

## 12.4. Verificar os serviços

```bash
docker compose -f compose.prod.yaml ps
```

## 12.5. Acompanhar os logs

```bash
docker compose -f compose.prod.yaml logs -f
```

## 12.6. Parar e remover os contêineres

```bash
docker compose -f compose.prod.yaml down
```

**Observação:** o Compose de produção utiliza as imagens `1.0.0`. Elas devem estar disponíveis localmente ou em um registro de imagens acessível ao Docker.

---

# 13. Health Checks

O projeto utiliza verificações de saúde para acompanhar o funcionamento dos serviços.

## 13.1. Nginx

Endpoint:

```http
GET /nginx-health
```

Retorno:

```text
OK
```

Verifica se o servidor Nginx está respondendo.

Essa verificação é realizada diretamente pelo Nginx, sem consultar a aplicação FastAPI.

## 13.2. Aplicação FastAPI

O Dockerfile Python possui um healthcheck que realiza uma requisição HTTP para:

```http
GET /
```

Se a aplicação responder com sucesso, o contêiner poderá ser considerado saudável.

Essa verificação confirma que a rota inicial está respondendo, mas não garante que todas as funcionalidades do CRUD estejam funcionando.

## 13.3. Verificar a saúde dos contêineres

```bash
docker ps
```

Para verificar diretamente o estado de saúde da API:

```bash
docker inspect --format='{{.State.Health.Status}}' devops-pipeline-example-api
```

Estados possíveis:

| Estado | Significado |
|---|---|
| `starting` | Verificações iniciais em andamento |
| `healthy` | As verificações de saúde estão passando |
| `unhealthy` | As verificações de saúde estão falhando |

**Importante:** um healthcheck com falha não provoca, por si só, a reinicialização automática do contêiner pelo Docker.

---

# 14. Comandos Úteis do Docker

Listar contêineres em execução:

```bash
docker ps
```

Listar todos os contêineres:

```bash
docker ps -a
```

Listar imagens:

```bash
docker images
```

Entrar no contêiner da API:

```bash
docker exec -it devops-pipeline-example-api sh
```

Entrar no contêiner do Nginx:

```bash
docker exec -it devops-pipeline-example-web sh
```

Visualizar os logs da API:

```bash
docker logs devops-pipeline-example-api
```

Visualizar os logs do Nginx:

```bash
docker logs devops-pipeline-example-web
```

Reconstruir o ambiente de desenvolvimento:

```bash
docker compose -f compose.dev.yaml up -d --build
```

---

# 15. Desenvolvimento Local x Docker

O projeto pode ser executado de duas maneiras.

| Característica | Execução local | Execução com Docker |
|---|---|---|
| Python | Instalado no computador | Instalado na imagem |
| Dependências | Instaladas no `.venv` | Instaladas durante o build |
| Ambiente virtual | Necessário para isolamento | Não é necessário no computador |
| Uvicorn | Executado diretamente | Executado no contêiner |
| Nginx | Não utilizado | Atua como proxy reverso |
| Porta de acesso | 8000 | 8080 |
| Testes automatizados | Executados com pytest | Podem ser executados separadamente |

O ambiente virtual criado no computador não é utilizado pelos contêineres Docker.

Cada imagem possui seu próprio ambiente e suas próprias dependências.

---

# 16. Próximos Passos — CI/CD

O projeto será utilizado nas próximas etapas das aulas de DevOps para implementação de uma pipeline CI/CD.

Tecnologias previstas:

- GitHub Actions
- GitHub Container Registry (GHCR)
- Docker
- Docker Compose
- Deploy em VPS
- AWS

## Fluxo previsto

```text
Desenvolvedor
      |
      | Git Push
      v
    GitHub
      |
      v
 GitHub Actions
      |
      | Integração Contínua (CI)
      |
      +--> Preparar ambiente Python
      |
      +--> Instalar dependências
      |
      +--> Executar testes automatizados
      |
      +--> Construir imagens Docker
      |
      v
 GitHub Container Registry
      |
      | Imagens Docker versionadas
      v
 Servidor VPS / AWS
      |
      | Deploy
      v
 Docker Compose
      |
      +--> Nginx
      |
      +--> FastAPI + Uvicorn
      |
      v
 Aplicação disponível
```

O objetivo é automatizar o processo de verificação, construção, publicação e implantação da aplicação.

Os testes automatizados funcionarão como uma etapa de controle de qualidade, permitindo interromper a pipeline caso sejam identificadas falhas nos cenários testados.

---

# 17. Objetivo do Projeto

Este repositório foi desenvolvido para fins educacionais, como material de apoio às aulas de DevOps.

Seu objetivo é demonstrar, de forma prática, como diferentes ferramentas e tecnologias são utilizadas durante o ciclo de desenvolvimento e entrega de software.

A API FastAPI funciona como aplicação de referência, permitindo que os estudantes concentrem seus esforços nos conceitos de versionamento, testes automatizados, conteinerização, integração contínua e implantação de aplicações.

O projeto será ampliado gradualmente conforme a evolução das aulas.
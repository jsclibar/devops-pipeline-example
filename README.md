# DevOps Pipeline Example

Projeto educacional desenvolvido para demonstrar, de forma prática, o ciclo de entrega de software com foco em **DevOps**.

Uma API simples de gerenciamento de livros, desenvolvida com Python e FastAPI, serve de base para explorar **versionamento, testes automatizados, Docker, integração contínua e implantação de aplicações**.

O projeto utiliza Git, GitHub, Docker, Docker Compose, Nginx e GitHub Actions.

A aplicação não utiliza banco de dados. Sua implementação é intencionalmente simples para que o foco das atividades seja o fluxo de entrega, desde a execução local até o deploy em um servidor.

A CI executa os testes e publica as imagens da API e do Nginx no GitHub Container Registry (GHCR). O CD é iniciado manualmente e atualiza o servidor com a versão escolhida.

Uma **instância Amazon EC2** é utilizada como exemplo. O mesmo modelo pode ser adaptado para outras clouds, VPS ou servidores próprios com Docker e acesso SSH.

---

# 1. Arquitetura

A aplicação utiliza dois serviços:

- **Nginx:** recebe as requisições e atua como proxy reverso.
- **Python + FastAPI + Uvicorn:** executa a API.

```text
Cliente
   |
   | HTTP
   v
Host ou servidor:8080
   |
   v
Nginx — porta 80
   |
   | Rede interna do Docker
   v
Uvicorn + FastAPI — porta 8000
   |
   v
API de Livros
```

Os serviços são executados em contêineres separados, conectados pela rede criada pelo Docker Compose.

No computador, o acesso ocorre por `http://localhost:8080`. No servidor, utiliza-se seu IP ou DNS.

---

# 2. Estrutura do Projeto

```text
devops-pipeline-example/
│
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── cd.yml
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
│   └── python/
│       └── Dockerfile
│
├── compose.dev.yaml
├── compose.prod.yaml
├── .dockerignore
├── .gitignore
└── README.md
```

| Arquivo | Finalidade |
|---|---|
| `.github/workflows/ci.yml` | Testar, construir e publicar as imagens |
| `.github/workflows/cd.yml` | Implantar uma versão escolhida por SSH |
| `backend_app.py` | Código da API |
| `requirements.txt` | Dependências da aplicação |
| `requirements-dev.txt` | Dependências de desenvolvimento e testes |
| `tests/test_api.py` | Testes automatizados |
| `docker/python/Dockerfile` | Construção da imagem da API |
| `docker/nginx/Dockerfile` | Construção da imagem do Nginx |
| `docker/nginx/default.conf` | Configuração do proxy reverso |
| `compose.dev.yaml` | Ambiente de desenvolvimento |
| `compose.prod.yaml` | Execução manual com imagens previamente construídas |

**O arquivo `compose.aws.yaml` não faz parte do repositório.** Ele é escrito no servidor pelo workflow de CD durante a implantação.

---

# 3. Requisitos

## Execução local

- Git
- Python 3.11 ou superior
- pip
- venv

## Execução com Docker

- Docker Engine
- Docker Compose

## CI/CD

- Repositório no GitHub com Actions habilitado.
- Permissão para publicar imagens no GHCR.
- Servidor com Docker e Compose com suporte a `--wait`.
- Acesso SSH e usuário autorizado a executar Docker.
- Secrets de conexão cadastrados no GitHub.
- Conectividade entre o executor do Actions, o servidor e o GHCR.

As aulas utilizam Ubuntu 24.04 LTS e Debian 13. A CI utiliza Python 3.13.

As imagens do exemplo são construídas para AMD64/x86_64. O servidor deve utilizar uma arquitetura compatível.

---

# 4. Preparar o Ambiente Local

## 4.1. Instalar Python e ferramentas

No Debian ou Ubuntu:

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip
```

Verifique:

```bash
python3 --version
```

## 4.2. Clonar o projeto

```bash
git clone https://github.com/jsclibar/devops-pipeline-example.git
cd devops-pipeline-example
```

Os próximos comandos devem ser executados na raiz do projeto, salvo indicação contrária.

## 4.3. Criar e ativar o ambiente virtual

```bash
python3 -m venv .venv --prompt devops-pipeline-example
source .venv/bin/activate
```

O ambiente virtual isola as dependências do projeto dos pacotes do sistema.

Confira o interpretador utilizado:

```bash
which python
python --version
```

O caminho deve apontar para a pasta `.venv`.

## 4.4. Instalar as dependências

```bash
python -m pip install -r requirements-dev.txt
```

O arquivo `requirements-dev.txt` inclui as dependências da aplicação e as ferramentas de teste. Não é necessário instalar os dois arquivos separadamente.

Para consultar os pacotes e verificar conflitos:

```bash
python -m pip list
python -m pip check
```

---

# 5. Executar a API Localmente

Com o ambiente virtual ativado:

```bash
python -m uvicorn backend_app:app --reload
```

O parâmetro `--reload` reinicia o servidor quando o código muda e deve ser utilizado apenas durante o desenvolvimento.

| Recurso | Endereço |
|---|---|
| Página inicial | http://localhost:8000 |
| Swagger UI | http://localhost:8000/docs |
| Lista de livros | http://localhost:8000/livros |

Para encerrar o servidor, pressione `Ctrl+C`.

---

# 6. Endpoints da API

| Método | Endpoint | Funcionalidade |
|---|---|---|
| GET | `/` | Mensagem de boas-vindas |
| GET | `/livros` | Listar livros |
| GET | `/livros/{idlivro}` | Consultar livro pelo ID |
| GET | `/livros/autor/{nome}` | Consultar livros por autor |
| POST | `/livros` | Cadastrar livro |
| PUT | `/livros/{idlivro}` | Atualizar livro |
| DELETE | `/livros/{idlivro}` | Excluir livro |

## Exemplo de cadastro

Envie uma requisição `POST /livros` com:

```json
{
    "titulo": "O Cortiço",
    "autor": "Aluísio Azevedo",
    "ano": 1890
}
```

Exemplo de resposta:

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

O ID é gerado automaticamente. No exemplo, o próximo identificador disponível é 3.

**Os dados ficam em memória.** Reiniciar a aplicação ou substituir o contêiner da API elimina as alterações realizadas durante a execução.

---

# 7. Testes Automatizados

Os testes estão em `tests/test_api.py` e utilizam pytest e o TestClient do FastAPI.

Execute com o ambiente virtual ativado:

```bash
python -m pytest -v
```

Resultado esperado para a suíte de referência:

```text
13 passed
```

Os testes verificam o CRUD de livros, a busca por autor e respostas de erro como HTTP 404 e 422.

Antes de cada teste, os dados são reiniciados para evitar interferência entre os cenários.

**Não é necessário iniciar o Uvicorn ou os contêineres para executar os testes.**

A mesma suíte é executada pela CI. Se algum teste falhar, a construção e a publicação das imagens não seguem.

---

# 8. Docker — Desenvolvimento

O ambiente de desenvolvimento utiliza os serviços `api` e `web`.

## Iniciar

```bash
docker compose -f compose.dev.yaml up -d --build
```

O comando constrói as imagens, cria a rede e inicia os contêineres em segundo plano.

## Acessar

| Recurso | Endereço |
|---|---|
| Página inicial | http://localhost:8080 |
| Swagger UI | http://localhost:8080/docs |
| Livros | http://localhost:8080/livros |
| Saúde do Nginx | http://localhost:8080/nginx-health |

A porta 8080 pertence ao acesso externo pelo Nginx. A API utiliza a porta 8000 na rede interna do Docker.

## Verificar serviços

```bash
docker compose -f compose.dev.yaml ps
```

## Acompanhar logs

```bash
docker compose -f compose.dev.yaml logs -f
```

Pressione `Ctrl+C` para sair dos logs sem parar os serviços.

## Encerrar

```bash
docker compose -f compose.dev.yaml down
```

O ambiente utiliza um bind mount para compartilhar o código Python e executa Uvicorn com `--reload`. Alterações no código podem ser aplicadas sem reconstruir a imagem.

Após alterações nas dependências ou nos Dockerfiles, reconstrua:

```bash
docker compose -f compose.dev.yaml up -d --build
```

---

# 9. Docker — Execução Manual com Imagens Versionadas

O arquivo `compose.prod.yaml` demonstra a execução com imagens previamente construídas.

Esse ambiente não compartilha o código por bind mount e não utiliza `--reload`.

## Construir as imagens

```bash
docker build -t devops-pipeline-example-api:1.0.0 \
    -f docker/python/Dockerfile .
```

```bash
docker build -t devops-pipeline-example-web:1.0.0 \
    -f docker/nginx/Dockerfile .
```

## Iniciar

```bash
docker compose -f compose.prod.yaml up -d
```

## Verificar serviços e logs

```bash
docker compose -f compose.prod.yaml ps
docker compose -f compose.prod.yaml logs -f
```

## Encerrar

```bash
docker compose -f compose.prod.yaml down
```

As imagens `1.0.0` precisam estar disponíveis para o Docker.

Esse é o exercício manual. No fluxo CI/CD, as imagens são construídas pelo GitHub Actions, publicadas no GHCR e identificadas pelo commit.

**Encerre o ambiente DEV antes de iniciar o PROD na mesma máquina**, pois eles podem utilizar os mesmos nomes e portas.

---

# 10. Health Checks

Os healthchecks verificam periodicamente se os serviços estão respondendo.

| Serviço | Verificação |
|---|---|
| Nginx | Requisição a `/nginx-health`, que retorna `OK` |
| API | Requisição à rota `/` |

O healthcheck do Nginx não consulta a API. O da API confirma que a rota inicial responde, mas não verifica todas as funcionalidades do CRUD.

Consulte o estado dos contêineres:

```bash
docker ps
```

Para consultar diretamente a API, quando utilizado o nome fixo:

```bash
docker inspect --format='{{.State.Health.Status}}' devops-pipeline-example-api
```

Estados possíveis:

- `starting`: verificações iniciais.
- `healthy`: verificações passando.
- `unhealthy`: verificações falhando.

Caso o contêiner tenha outro nome, consulte `docker ps` e ajuste o comando.

**Um estado `unhealthy` não provoca, por si só, o reinício automático do contêiner.**

No deploy, o Compose utiliza `--wait` para aguardar os serviços ficarem em execução e, quando houver healthcheck, saudáveis. Isso não substitui um teste completo da aplicação.

---

# 11. Comandos Úteis

| Ação | Comando |
|---|---|
| Contêineres em execução | `docker ps` |
| Todos os contêineres | `docker ps -a` |
| Imagens locais | `docker images` |
| Logs da API | `docker logs devops-pipeline-example-api` |
| Logs do Nginx | `docker logs devops-pipeline-example-web` |
| Terminal da API | `docker exec -it devops-pipeline-example-api sh` |
| Terminal do Nginx | `docker exec -it devops-pipeline-example-web sh` |

Os exemplos utilizam nomes fixos definidos com `container_name`. Se utilizar nomes automáticos, confira-os com `docker ps`.

Para baixar uma versão publicada pela CI:

```bash
docker pull ghcr.io/jsclibar/devops-pipeline-example-api:446c0bc
```

A tag `446c0bc` é ilustrativa. Utilize uma tag disponível no GHCR.

---

# 12. Execução Local x Docker

| Característica | Local | Docker |
|---|---|---|
| Python | Instalado no computador | Incluído na imagem |
| Dependências | Instaladas no `.venv` | Instaladas no build |
| Uvicorn | Executado diretamente | Executado no contêiner |
| Nginx | Não utilizado | Proxy reverso |
| Porta de acesso | 8000 | 8080 |

O ambiente virtual do computador não é utilizado pelos contêineres.

No deploy, o servidor não precisa instalar Python ou as bibliotecas da aplicação. Ele executa as imagens utilizando Docker e Docker Compose.

---

# 13. CI/CD com GitHub Actions

O projeto utiliza dois workflows:

| Workflow | Arquivo | Responsabilidade |
|---|---|---|
| CI | `.github/workflows/ci.yml` | Testar, construir e publicar |
| CD | `.github/workflows/cd.yml` | Implantar uma versão escolhida |

```text
Push na main
      |
      v
CI: testes → construção → publicação
      |
      v
GHCR: imagens identificadas pelo commit
      |
      | Escolha manual da tag
      v
CD: conexão SSH → pull → atualização
      |
      v
Aplicação no servidor
```

## 13.1. Integração Contínua — CI

A CI executa a cada push na branch `main` ou manualmente pela aba **Actions**.

Em uma máquina Ubuntu temporária do GitHub, ela:

1. Obtém o código.
2. Prepara Python e instala as dependências.
3. Executa os testes.
4. Constrói as imagens da API e do Nginx.
5. Publica as imagens no GHCR.

Os passos executam em sequência. Uma falha impede a execução dos passos seguintes por padrão.

A autenticação no registry utiliza o `GITHUB_TOKEN`, fornecido automaticamente, com:

```yaml
permissions:
  contents: read
  packages: write
```

Pacotes publicados anteriormente de forma manual podem exigir autorização adicional em:

**Package settings → Manage Actions access → seu repositório → Write**

## 13.2. Tags das imagens

A CI utiliza os primeiros sete caracteres do commit:

```bash
TAG=${GITHUB_SHA:0:7}
```

Exemplo:

```text
ghcr.io/jsclibar/devops-pipeline-example-api:446c0bc
ghcr.io/jsclibar/devops-pipeline-example-web:446c0bc
```

A mesma tag identifica as duas imagens daquela execução.

Antes de implantar, confirme que ela existe nos dois pacotes. A publicação de uma imagem pode funcionar enquanto a outra falha.

## 13.3. Entrega e Implantação — CD

O CD é iniciado manualmente pelo evento `workflow_dispatch`. O usuário informa a tag desejada, e o restante do deploy é automatizado.

A ação `appleboy/ssh-action` conecta ao servidor e executa o conteúdo de `script`.

O script:

1. Cria a pasta da aplicação.
2. Escreve o arquivo `compose.aws.yaml` no servidor.
3. Disponibiliza a variável `TAG`.
4. Baixa as duas imagens.
5. Atualiza os contêineres.

**Não é necessário criar o `compose.aws.yaml` no repositório ou copiá-lo manualmente para a instância.** Sua configuração está no próprio workflow de CD.

Os comandos principais são:

```bash
export TAG

docker compose -f compose.aws.yaml pull

docker compose -f compose.aws.yaml up -d --wait
```

O Compose utiliza `${TAG}` nos nomes das imagens:

```yaml
services:
  api:
    image: ghcr.io/jsclibar/devops-pipeline-example-api:${TAG}

  web:
    image: ghcr.io/jsclibar/devops-pipeline-example-web:${TAG}
```

O `pull` baixa as imagens. O `up` cria ou atualiza os serviços, recriando os contêineres quando necessário, como na mudança de imagem.

O `--wait` aguarda a inicialização e os healthchecks. Ao executar novamente com as mesmas imagens e configurações, o Compose pode manter os contêineres existentes.

## 13.4. Onde os comandos executam

| Trecho do workflow | Local de execução |
|---|---|
| `run` da CI | Executor do GitHub |
| Ação de conexão SSH | Inicia no executor do GitHub |
| `script` da ação SSH | Servidor de destino |

A tag é recebida no GitHub e enviada ao servidor pela ação:

```yaml
env:
  TAG: ${{ inputs.tag }}

with:
  envs: TAG
```

O `env` disponibiliza a variável ao passo. O `envs`, opção da ação SSH, leva essa variável para o ambiente remoto.

---

# 14. Preparar o Servidor

O exemplo utiliza uma instância **Amazon EC2**, com:

- Docker Engine e Docker Compose instalados.
- Acesso SSH funcionando.
- Usuário autorizado a executar Docker sem `sudo`.
- Conectividade para baixar as imagens.
- Arquitetura compatível com as imagens da CI.
- Regras de rede permitindo SSH do executor e acesso à aplicação.

Para adicionar o usuário atual ao grupo Docker:

```bash
sudo usermod -aG docker "$USER"
```

Saia da sessão SSH, conecte-se novamente e teste:

```bash
docker ps
```

O grupo `docker` concede poderes equivalentes aos de administrador sobre o servidor.

No modelo apresentado, as imagens precisam estar públicas no GHCR, pois o CD não realiza login no registry dentro da EC2.

O acesso à aplicação ocorre por:

```text
http://IP_PUBLICO_DO_SERVIDOR:8080/docs
```

A API permanece acessível internamente na porta 8000; o Nginx publica o acesso externo na porta 8080.

**A conexão SSH do Actions vem do executor do GitHub, não do computador do aluno.** Os executores padrão possuem IPs variáveis, que precisam ser considerados nas regras de acesso.

---

# 15. Secrets e Identificação do Servidor

Cadastre as informações em:

**Settings → Secrets and variables → Actions → Secrets → New repository secret**

| Secret | Conteúdo |
|---|---|
| `EC2_HOST` | IP ou DNS do servidor, sem `http://` |
| `EC2_USER` | Usuário SSH, como `ubuntu` |
| `EC2_SSH_KEY` | Conteúdo completo da chave privada `.pem` |
| `EC2_FINGERPRINT` | Fingerprint da chave pública do servidor |

A chave privada deve incluir as linhas de início e fim. Não adicione o `.pem` ao repositório.

Os nomes usam `EC2` por causa do exemplo. Eles podem ser utilizados com outro servidor ou renomeados, desde que o workflow seja atualizado.

## Chave privada e fingerprint

São duas verificações diferentes:

- **Chave privada do usuário:** comprova autorização para acessar.
- **Fingerprint do servidor:** permite conferir quem respondeu à conexão.

O servidor possui suas próprias chaves SSH, separadas das chaves do usuário. O fingerprint é um resumo da chave pública do servidor.

Para consultar os fingerprints, execute dentro do servidor:

```bash
sudo sh -c 'for chave in /etc/ssh/ssh_host_*_key.pub; do ssh-keygen -lf "$chave" -E sha256; done'
```

Cada tipo de chave, como ECDSA, ED25519 ou RSA, possui um fingerprint. Cadastre aquele correspondente à chave apresentada na conexão do Actions.

Copie somente o trecho neste formato:

```text
SHA256:IDENTIFICACAO_DA_CHAVE
```

Se aparecer `host key fingerprint mismatch`, confira o endereço, o Secret e a chave apresentada pelo servidor. Não aceite um fingerprint diferente sem confirmar sua origem.

---

# 16. Executar CI, CD e Rollback

## 16.1. Executar a CI

A CI inicia automaticamente em pushes na `main`.

Para executar manualmente:

1. Abra **Actions**.
2. Selecione o workflow de CI.
3. Clique em **Run workflow**.
4. Selecione `main` e inicie.

Ao terminar, consulte **Packages** e confirme a publicação das duas imagens com a mesma tag.

Os workflows precisam estar na branch padrão para disponibilizar a execução manual pela interface.

## 16.2. Executar o CD

1. Abra **Actions → CD manual**.
2. Clique em **Run workflow**.
3. Selecione `main`.
4. Informe uma tag publicada nas duas imagens.
5. Execute e acompanhe os logs.

Evite deploys simultâneos no mesmo servidor.

Após o sucesso, confira:

```text
http://IP_PUBLICO_DO_SERVIDOR:8080/docs
```

O `--wait` verifica a inicialização dos serviços, mas não testa o acesso externo ou todas as funcionalidades da API.

## 16.3. Fazer rollback

Execute novamente o CD informando uma tag anterior:

```text
Versão atual:     e66081d
Versão anterior:  446c0bc
```

Ao informar `446c0bc`, o servidor passa a executar as imagens dessa versão.

As imagens antigas precisam continuar disponíveis nos dois pacotes do GHCR.

O rollback:

- Altera a versão executada no servidor.
- Não modifica o código da branch `main`.
- Não recupera dados que estavam na memória da aplicação.
- É iniciado manualmente pelo mesmo workflow de CD.

---

# 17. Adaptação para Outras Infraestruturas

A EC2 é apenas o servidor escolhido para demonstrar o deploy.

Como o CD utiliza SSH e Docker Compose, ele pode ser adaptado para outras clouds, VPS, máquinas virtuais ou servidores físicos.

Os principais ajustes são endereço, usuário, chave, fingerprint, caminhos e regras de rede.

O servidor também pode estar em uma **VPC ou rede privada**, desde que o executor consiga alcançá-lo. Isso pode exigir VPN, bastion ou um executor instalado na própria rede.

Uma VPC é a rede onde o servidor está localizado. A conexão depende das rotas e das regras de acesso dessa rede.

O nome `compose.aws.yaml` pode ser alterado em outra infraestrutura, desde que os comandos do workflow sejam atualizados.

---

# 18. Escopo Educacional

O projeto demonstra um fluxo simples, com um único servidor e deploy manualmente iniciado.

O exemplo não inclui alta disponibilidade, HTTPS ou rollback automático. A atualização pode causar uma breve indisponibilidade, e os dados em memória são perdidos quando a API é reiniciada.

Os testes da CI verificam a API, mas não representam uma validação completa do ambiente implantado.

A proposta é permitir que os alunos compreendam o fluxo:

**alterar → testar → construir → publicar → escolher a versão → implantar**

O projeto pode evoluir gradualmente conforme o avanço das aulas.
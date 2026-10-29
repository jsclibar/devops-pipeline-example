# Docker Compose — Fluxo DEV

Comandos básicos para executar o projeto `devops-pipeline-example` em ambiente de desenvolvimento.

## 1. Subir os contêineres

```bash
docker compose -f compose.dev.yaml up -d
```

Inicia os serviços `api` (Python) e `web` (Nginx) em segundo plano.

## 2. Verificar os contêineres

```bash
docker compose -f compose.dev.yaml ps
```

Exibe o estado dos serviços.

## 3. Visualizar os logs

```bash
docker compose -f compose.dev.yaml logs -f
```

Acompanha os logs em tempo real. Pressione `Ctrl + C` para sair sem parar os contêineres.

## 4. Acessar a aplicação

```text
http://localhost:8080
```

## 5. Reconstruir as imagens (quando necessário)

```bash
docker compose -f compose.dev.yaml up --build -d
```

Utilize após alterações nos Dockerfiles ou nas dependências.

## 6. Parar e remover os contêineres

```bash
docker compose -f compose.dev.yaml down
```

Para e remove os contêineres e a rede do Compose.

---

## Resumo rápido

| Ação | Comando |
|---|---|
| Subir | `docker compose -f compose.dev.yaml up -d` |
| Verificar | `docker compose -f compose.dev.yaml ps` |
| Logs | `docker compose -f compose.dev.yaml logs -f` |
| Reconstruir | `docker compose -f compose.dev.yaml up --build -d` |
| Parar e remover | `docker compose -f compose.dev.yaml down` |

# Docker Compose — Ambiente de Produção (PROD)

O arquivo `compose.prod.yaml` define os serviços utilizados no ambiente de produção do projeto `devops-pipeline-example`.

Diferentemente do ambiente de desenvolvimento, a configuração de produção utiliza **imagens Docker previamente construídas e versionadas**, sem realizar o build diretamente pelo Compose.

## 1. Configuração do Compose de produção

```yaml
name: devops-pipeline-example

services:
  api:
    image: devops-pipeline-example-api:1.0.0
    container_name: devops-pipeline-example-api
    restart: unless-stopped

  web:
    image: devops-pipeline-example-web:1.0.0
    container_name: devops-pipeline-example-web

    ports:
      - "8080:80"

    depends_on:
      - api

    restart: unless-stopped
```

### Explicação das configurações

- **`name`**: define o nome do projeto Docker Compose.
- **`services`**: define os serviços que serão executados.
- **`api`**: serviço responsável pela aplicação Python.
- **`web`**: serviço responsável pelo servidor Nginx.
- **`image`**: especifica a imagem Docker e sua versão (`1.0.0`).
- **`container_name`**: define o nome do contêiner.
- **`ports: "8080:80"`**: mapeia a porta 8080 do host para a porta 80 do Nginx.
- **`depends_on`**: inicia o serviço `api` antes do `web`, mas não garante que a API esteja pronta.
- **`restart: unless-stopped`**: reinicia automaticamente o contêiner se ele parar ou após reinício do Docker, exceto quando tiver sido parado manualmente.

## 2. Diferenças entre DEV e PROD

| Desenvolvimento (DEV) | Produção (PROD) |
|---|---|
| Pode construir imagens com `build` | Utiliza imagens previamente construídas |
| Utiliza bind mounts para desenvolvimento | Não monta arquivos do código-fonte |
| Uvicorn utiliza `--reload` | Executa o comando definido na imagem |
| Imagens com tag `dev` | Imagens versionadas, como `1.0.0` |
| Focado em desenvolvimento e testes | Focado em execução estável |

**Por que utilizar imagens versionadas?**

O versionamento permite identificar qual versão da aplicação está sendo executada e facilita a implantação ou reversão para uma versão anterior.

## 3. Preparar as imagens de produção

Como o arquivo `compose.prod.yaml` não possui a configuração `build`, as imagens precisam estar disponíveis antes de iniciar os serviços.

Caso ainda não existam, podem ser construídas utilizando os Dockerfiles do projeto:

**Construir a imagem da API:**

```bash
docker build -f docker/python/Dockerfile -t devops-pipeline-example-api:1.0.0 .
```

**Construir a imagem do Nginx:**

```bash
docker build -f docker/nginx/Dockerfile -t devops-pipeline-example-web:1.0.0 .
```

Esses comandos utilizam os Dockerfiles existentes. É importante verificar se eles estão preparados para produção, especialmente quanto ao comando de inicialização da API.

Em um pipeline CI/CD, normalmente essas imagens são construídas, testadas e publicadas em um registry antes do deploy.

## 4. Subir o ambiente de produção

Com as imagens disponíveis, execute:

```bash
docker compose -f compose.prod.yaml up -d
```

O Docker Compose irá:

1. Ler o arquivo `compose.prod.yaml`.
2. Utilizar as imagens `1.0.0` especificadas.
3. Criar a rede e os contêineres necessários.
4. Iniciar a API e o Nginx.
5. Manter os serviços executando em segundo plano.

**Observação:** se as imagens não estiverem disponíveis localmente, o Docker poderá tentar baixá-las de um registry. Se não conseguir encontrá-las, a inicialização falhará.

## 5. Verificar os serviços

```bash
docker compose -f compose.prod.yaml ps
```

Para acompanhar os logs:

```bash
docker compose -f compose.prod.yaml logs -f
```

## 6. Acessar a aplicação

Com os serviços em execução, acesse:

```text
http://localhost:8080
```

O Nginx recebe as requisições e as encaminha à API Python, conforme sua configuração de proxy reverso.

## 7. Parar e remover os contêineres

```bash
docker compose -f compose.prod.yaml down
```

Remove os contêineres e a rede do Compose, preservando as imagens.

---

## Resumo — Fluxo PROD

| Ação | Comando |
|---|---|
| Construir API | `docker build -f docker/python/Dockerfile -t devops-pipeline-example-api:1.0.0 .` |
| Construir Nginx | `docker build -f docker/nginx/Dockerfile -t devops-pipeline-example-web:1.0.0 .` |
| Subir PROD | `docker compose -f compose.prod.yaml up -d` |
| Verificar | `docker compose -f compose.prod.yaml ps` |
| Logs | `docker compose -f compose.prod.yaml logs -f` |
| Parar e remover | `docker compose -f compose.prod.yaml down` |

> **Importante:** o arquivo de produção não utiliza `build`. Portanto, o comando `docker compose up --build` não construirá essas imagens. A construção deve acontecer separadamente, de preferência em um pipeline CI/CD.

> **Atenção:** os ambientes DEV e PROD utilizam o mesmo nome de projeto e os mesmos nomes de contêineres. Por isso, não devem ser executados simultaneamente nessa configuração. Para alternar entre eles, encerre primeiro o ambiente em execução.

# Docker — Publicando imagens no GitHub Container Registry (GHCR)

Nesta etapa, vamos publicar no GitHub as imagens Docker de produção já construídas anteriormente.

O objetivo é disponibilizar as imagens para que possam ser baixadas e executadas em outros servidores, sem precisar reconstruí-las.

## 1. Verificar as imagens existentes

```bash
docker images
```

As imagens já construídas devem estar disponíveis:

```text
devops-pipeline-example-api:1.0.0
devops-pipeline-example-web:1.0.0
```

## 2. Fazer login no GitHub Container Registry

Crie um Personal Access Token (classic) no GitHub com permissão `write:packages`:

https://github.com/settings/tokens

Depois, execute:

```bash
docker login ghcr.io -u SEU_USUARIO
```

Informe o token quando solicitado.

## 3. Criar as tags para o GitHub

O comando `docker tag` cria uma nova referência para uma imagem existente, sem reconstruí-la.

**API Python:**

```bash
docker tag devops-pipeline-example-api:1.0.0 ghcr.io/SEU_USUARIO/devops-pipeline-example-api:1.0.0
```

**Nginx:**

```bash
docker tag devops-pipeline-example-web:1.0.0 ghcr.io/SEU_USUARIO/devops-pipeline-example-web:1.0.0
```

Substitua `SEU_USUARIO` pelo seu usuário do GitHub, em letras minúsculas.

## 4. Publicar as imagens no GitHub

O comando `docker push` envia as imagens para o GitHub Container Registry.

**API Python:**

```bash
docker push ghcr.io/SEU_USUARIO/devops-pipeline-example-api:1.0.0
```

**Nginx:**

```bash
docker push ghcr.io/SEU_USUARIO/devops-pipeline-example-web:1.0.0
```

## 5. Verificar as imagens publicadas

Acesse seu perfil do GitHub e abra a seção **Packages**.

As imagens publicadas deverão aparecer com a versão `1.0.0`.

---

## Resumo — Publicação no GHCR

| Ação | Comando |
|---|---|
| Verificar imagens | `docker images` |
| Autenticar no GitHub | `docker login ghcr.io -u SEU_USUARIO` |
| Criar tag | `docker tag IMAGEM_LOCAL IMAGEM_GHCR` |
| Publicar imagem | `docker push IMAGEM_GHCR` |

**Importante:**

- Não foi necessário executar `docker build` novamente.
- O `docker tag` não modifica o conteúdo da imagem.
- O `docker push` envia a imagem existente para o GHCR.
- As imagens publicadas mantêm a arquitetura original (AMD64 ou ARM64).
- Para baixar imagens privadas em outro servidor, será necessária autenticação no GHCR.
# GitHub na prática — Clonando e publicando no seu próprio repositório

Nesta atividade, vamos:

1. Clonar o repositório da aula.
2. Remover a ligação com o repositório do professor.
3. Criar um repositório próprio no GitHub.
4. Adicionar o novo repositório como `origin`.
5. Criar um token de acesso.
6. Configurar o Git para salvar a credencial.
7. Fazer o primeiro `push`.
8. Criar uma nova alteração e enviá-la para o GitHub.

---

# 1. Clonar o repositório da aula

Clone o repositório fornecido pelo professor:

```bash
git clone https://github.com/jsclibar/site-empresa.git
```

Entre na pasta do projeto:

```bash
cd site-empresa
```

Confira os arquivos:

```bash
ls
```

Confira o histórico:

```bash
git log --oneline
```

Confira o repositório remoto configurado:

```bash
git remote -v
```

Deve aparecer algo semelhante a:

```text
origin  https://github.com/jsclibar/site-empresa.git (fetch)
origin  https://github.com/jsclibar/site-empresa.git (push)
```

O `git clone` cria automaticamente um remoto chamado `origin` apontando para o repositório que foi clonado.

---

# 2. Remover o repositório remoto do professor

Como cada aluno utilizará seu próprio repositório no GitHub, remova o `origin` atual:

```bash
git remote remove origin
```

Confira:

```bash
git remote -v
```

Agora não deve aparecer nenhum repositório remoto.

> A remoção do `origin` não apaga arquivos nem commits.
>
> Apenas remove a ligação entre o repositório local e o repositório remoto do professor.

---

# 3. Criar um novo repositório no GitHub

Acesse o GitHub e crie um novo repositório.

Clique em:

```text
New repository
```

Utilize, por exemplo:

```text
site-empresa
```

Crie o repositório vazio.

Não selecione:

- README;
- `.gitignore`;
- licença.

Isso é importante porque o projeto e o histórico já existem localmente.

---

# 4. Adicionar seu repositório como `origin`

Depois de criar o repositório, copie a URL HTTPS.

Exemplo:

```text
https://github.com/SEU_USUARIO/site-empresa.git
```

Adicione o repositório remoto:

```bash
git remote add origin https://github.com/SEU_USUARIO/site-empresa.git
```

Confira:

```bash
git remote -v
```

Agora deve aparecer algo semelhante a:

```text
origin  https://github.com/SEU_USUARIO/site-empresa.git (fetch)
origin  https://github.com/SEU_USUARIO/site-empresa.git (push)
```

O nome `origin` representa o repositório remoto principal associado ao projeto.

---

# 5. Criar um Personal Access Token

Para realizar operações Git utilizando HTTPS, utilizaremos um token no lugar da senha da conta.

No GitHub, acesse:

```text
Settings
→ Credentials
→ Personal access tokens
→ Fine-grained tokens
→ Generate new token
```

Defina um nome para o token:

```text
Aula Git
```

Escolha uma data de expiração.

Em:

```text
Repository access
```

selecione:

```text
Only select repositories
```

Escolha:

```text
site-empresa
```

Em:

```text
Repository permissions
```

configure:

```text
Contents → Read and write
```

A permissão `Metadata → Read-only` pode aparecer automaticamente e deve permanecer habilitada.

Depois clique em:

```text
Generate token
```

Copie o token gerado.

> O token será utilizado no lugar da senha da conta durante a autenticação Git via HTTPS.

---

# 6. Configurar o Git para salvar a credencial

Antes de realizar o primeiro `push`, configure o Git para armazenar a credencial:

```bash
git config --global credential.helper store
```

Essa configuração faz com que, depois do primeiro login, o Git armazene o usuário e o token para reutilização.

A credencial normalmente será salva em:

```text
~/.git-credentials
```

> Nesta atividade utilizaremos esse método por simplicidade.
>
> O `credential.helper store` salva a credencial em texto legível no computador.

---

# 7. Fazer o primeiro push

Agora envie a branch `main` para o seu repositório no GitHub:

```bash
git push -u origin main
```

O Git solicitará o usuário:

```text
Username for 'https://github.com':
```

Digite seu usuário do GitHub.

Depois aparecerá:

```text
Password for 'https://SEU_USUARIO@github.com':
```

Nesse campo, cole o **Personal Access Token**.

> Mesmo aparecendo a palavra `Password`, não utilize a senha da sua conta.
>
> Utilize o token criado anteriormente.

---

# 8. Entendendo o primeiro push

O comando utilizado foi:

```bash
git push -u origin main
```

Cada parte possui uma função:

```text
git push
→ envia commits para um repositório remoto

origin
→ nome do repositório remoto

main
→ branch que será enviada

-u
→ salva a relação entre a branch local e a branch remota
```

Depois desse comando, o Git passa a relacionar:

```text
main
   ↕
origin/main
```

Por isso, nos próximos envios normalmente será suficiente executar:

```bash
git push
```

---

# 9. Conferir a credencial salva

Depois da primeira autenticação, é possível verificar se o arquivo foi criado:

```bash
ls -la ~
```

O arquivo pode aparecer como:

```text
.git-credentials
```

Também é possível visualizar seu conteúdo com:

```bash
cat ~/.git-credentials
```

> Atenção: não compartilhe nem mostre publicamente o conteúdo desse arquivo.
>
> Ele pode conter seu token de acesso.

---

# 10. Conferir o projeto no GitHub

Atualize a página do seu repositório no GitHub.

Agora devem aparecer:

- os arquivos do projeto;
- o histórico de commits;
- a branch `main`.

O histórico que existia no repositório clonado também será enviado para o novo repositório.

---

# 11. Fazer uma nova alteração

Agora faça uma alteração no projeto:

```bash
echo "<p>Alteração realizada pelo aluno</p>" >> index.html
```

Confira:

```bash
git status
```

Veja o que mudou:

```bash
git diff
```

Prepare a alteração:

```bash
git add index.html
```

Confira:

```bash
git status
```

Crie um novo commit:

```bash
git commit -m "Adiciona alteração do aluno"
```

Confira o histórico:

```bash
git log --oneline
```

---

# 12. Enviar a nova alteração

Como o remoto já está configurado e o `-u` foi utilizado no primeiro envio, agora basta executar:

```bash
git push
```

Como a credencial foi salva anteriormente, o Git normalmente não solicitará novamente usuário e token.

---

# 13. Conferir a alteração no GitHub

Atualize novamente a página do repositório.

Confira:

- o arquivo `index.html`;
- o novo commit;
- a mensagem do commit;
- o histórico atualizado.

---

# 14. Fluxo completo da atividade

```text
Repositório do professor
          ↓
      git clone
          ↓
Repositório local do aluno
          ↓
git remote remove origin
          ↓
Criar repositório no GitHub
          ↓
git remote add origin ...
          ↓
Criar Personal Access Token
          ↓
Configurar credential.helper
          ↓
git push -u origin main
          ↓
Autenticar com usuário + token
          ↓
Credencial salva
          ↓
Novo desenvolvimento
          ↓
git add
          ↓
git commit
          ↓
git push
```

---

# 15. Principais comandos utilizados

## Clonar um repositório

```bash
git clone URL
```

---

## Ver os repositórios remotos

```bash
git remote -v
```

---

## Remover um remoto

```bash
git remote remove origin
```

---

## Adicionar um remoto

```bash
git remote add origin URL
```

---

## Configurar armazenamento da credencial

```bash
git config --global credential.helper store
```

---

## Primeiro envio da branch

```bash
git push -u origin main
```

---

## Próximos envios

```bash
git push
```

---

# 16. Resumo dos conceitos

## `clone`

```text
Copia um repositório remoto para o computador.
```

Com o clone também são trazidos:

- arquivos;
- commits;
- histórico;
- branches necessárias;
- configuração do `origin`.

---

## `origin`

```text
É apenas um nome utilizado para identificar um repositório remoto.
```

Exemplo:

```text
origin
   ↓
https://github.com/usuario/site-empresa.git
```

---

## `push`

```text
Envia commits do repositório local para o repositório remoto.
```

---

## `-u`

No primeiro:

```bash
git push -u origin main
```

o `-u` registra a relação entre:

```text
main local
     ↕
origin/main
```

Depois disso, normalmente podemos executar apenas:

```bash
git push
```

---

## Token

O Personal Access Token é utilizado para autenticar operações Git via HTTPS.

```text
Username
→ usuário do GitHub

Password
→ Personal Access Token
```

A senha normal da conta não é utilizada para operações Git via HTTPS.

---

# 17. Resultado esperado

Ao final da atividade, cada aluno deverá possuir:

- o projeto clonado em seu computador;
- todo o histórico Git da atividade;
- um repositório próprio no GitHub;
- o `origin` apontando para seu próprio repositório;
- autenticação via Personal Access Token;
- credencial armazenada para os próximos acessos;
- pelo menos um novo commit próprio;
- o novo commit enviado para o GitHub.
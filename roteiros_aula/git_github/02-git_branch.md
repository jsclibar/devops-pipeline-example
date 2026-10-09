# 18. Trabalhando com Branches

Agora que o projeto já está publicado no GitHub, vamos aprender a trabalhar com branches.

A ideia é desenvolver uma nova funcionalidade sem alterar diretamente a branch `main`.

Neste exemplo:

```text
main
→ versão principal do projeto

feature/contato
→ branch usada para desenvolver uma nova página de contato
```

---

# 19. Conferir a branch atual

Veja as branches existentes no repositório local:

```bash
git branch
```

Deve aparecer:

```text
* main
```

O `*` indica a branch em que você está trabalhando naquele momento.

---

# 20. Criar uma nova branch

Crie uma nova branch chamada:

```text
feature/contato
```

Execute:

```bash
git branch feature/contato
```

Esse comando apenas cria a branch.

Ele ainda não troca para ela.

Confira novamente:

```bash
git branch
```

Agora deve aparecer:

```text
  feature/contato
* main
```

Isso significa que:

- a branch `feature/contato` já existe;
- você ainda está trabalhando na `main`.

---

# 21. Trocar para a nova branch

Agora entre na branch criada:

```bash
git switch feature/contato
```

Confira:

```bash
git branch
```

Agora deve aparecer:

```text
* feature/contato
  main
```

O `*` mostra que você está trabalhando na branch `feature/contato`.

---

# 22. Entendendo de onde a branch foi criada

Antes da criação da branch, imagine que a `main` estava assim:

```text
A → B → C
        ↑
       main
```

Quando executamos:

```bash
git branch feature/contato
```

a nova branch foi criada a partir do commit atual da `main`.

Ficou assim:

```text
A → B → C
        ↑
       main
        ↑
feature/contato
```

As duas branches estão apontando para o mesmo commit.

Nesse momento, elas possuem exatamente o mesmo conteúdo.

---

# 23. Criar uma alteração na nova branch

Agora que estamos na `feature/contato`, crie um novo arquivo:

```bash
echo "<h1>Contato</h1>" > contato.html
```

Confira os arquivos:

```bash
ls
```

Deve aparecer:

```text
contato.html
```

Veja o estado do Git:

```bash
git status
```

O arquivo deve aparecer como `untracked`.

---

# 24. Preparar o novo arquivo

Adicione o arquivo ao staging:

```bash
git add contato.html
```

Confira:

```bash
git status
```

Agora o arquivo deve aparecer preparado para o próximo commit.

---

# 25. Criar um commit na branch

Registre a alteração:

```bash
git commit -m "Adiciona página de contato"
```

Confira o histórico:

```bash
git log --oneline --decorate
```

Agora a branch `feature/contato` possui um commit que ainda não existe na `main`.

Exemplo:

```text
A → B → C → D
        ↑     ↑
       main  feature/contato
```

O commit `D` existe apenas na `feature/contato`.

A `main` continua apontando para o commit `C`.

---

# 26. Conferir que a alteração pertence à branch

Volte para a `main`:

```bash
git switch main
```

Confira:

```bash
git branch
```

Deve aparecer:

```text
  feature/contato
* main
```

Veja os arquivos:

```bash
ls
```

O arquivo:

```text
contato.html
```

não deve aparecer.

Isso acontece porque o commit que criou esse arquivo está na branch:

```text
feature/contato
```

---

# 27. Voltar para a branch da funcionalidade

Entre novamente na branch:

```bash
git switch feature/contato
```

Confira:

```bash
git branch
```

Agora:

```text
* feature/contato
  main
```

Veja os arquivos:

```bash
ls
```

O arquivo:

```text
contato.html
```

deve aparecer novamente.

Esse comportamento mostra que cada branch pode representar um estado diferente do projeto.

---

# 28. Enviar a branch para o GitHub

Até agora, a branch existe apenas no computador local.

Envie a branch para o GitHub:

```bash
git push -u origin feature/contato
```

O comando significa:

```text
git push
→ envia commits

origin
→ repositório remoto

feature/contato
→ branch que será enviada

-u
→ salva a relação entre a branch local e a branch remota
```

Depois disso, teremos:

```text
feature/contato local
        ↕
origin/feature/contato
```

---

# 29. Conferir a branch no GitHub

Acesse o repositório no GitHub.

Agora devem existir pelo menos duas branches:

```text
main
feature/contato
```

A branch `main` ainda representa a versão principal.

A branch `feature/contato` contém a nova funcionalidade.

---

# 30. Fazer o merge localmente

Agora vamos integrar a branch `feature/contato` na `main` usando o próprio Git.

Primeiro, volte para a `main`:

```bash
git switch main
```

Confira:

```bash
git branch
```

Deve aparecer:

```text
  feature/contato
* main
```

Agora faça o merge:

```bash
git merge feature/contato
```

Esse comando significa:

```text
pegue as alterações da branch feature/contato
e integre na branch atual
```

Como estamos na `main`, o merge será feito em:

```text
feature/contato
        ↓
       main
```

---

# 31. Entendendo o merge

Antes:

```text
A → B → C
        \
         D
         ↑
feature/contato
```

A `main` ainda estava no commit `C`.

Depois do merge:

```text
A → B → C → D
              ↑
             main
```

Agora a alteração também faz parte da `main`.

---

# 32. Conferir os arquivos depois do merge

Veja os arquivos:

```bash
ls
```

Agora o arquivo:

```text
contato.html
```

deve aparecer na `main`.

Confira o histórico:

```bash
git log --oneline --decorate
```

---

# 33. Enviar a `main` atualizada para o GitHub

O merge foi realizado localmente.

Agora precisamos atualizar o repositório remoto:

```bash
git push
```

Depois disso, a `main` do GitHub também terá a página de contato.

---

# 34. Conferir no GitHub

Atualize a página do repositório.

Confira:

- a branch `main`;
- o arquivo `contato.html`;
- o histórico de commits.

Agora a funcionalidade já faz parte da branch principal.

---

# 35. Excluir a branch local

Depois que a funcionalidade já foi integrada à `main`, a branch local pode ser removida.

Confira primeiro a branch atual:

```bash
git branch
```

Certifique-se de estar na:

```text
main
```

Agora exclua:

```bash
git branch -d feature/contato
```

Confira:

```bash
git branch
```

Deve restar:

```text
* main
```

---

# 36. Excluir a branch remota

A branch `feature/contato` ainda pode continuar existindo no GitHub.

Para removê-la pelo terminal:

```bash
git push origin --delete feature/contato
```

Depois confira no GitHub.

Agora a branch remota também terá sido removida.

---

# 37. Fluxo completo com Branch e Merge

```text
main
  ↓
criar branch
  ↓
feature/contato
  ↓
trocar para a branch
  ↓
desenvolver
  ↓
git add
  ↓
git commit
  ↓
git push
  ↓
voltar para main
  ↓
git merge feature/contato
  ↓
git push
  ↓
main atualizada no GitHub
```

---

# 38. Principais comandos de Branch

## Ver as branches

```bash
git branch
```

---

## Criar uma branch

```bash
git branch feature/contato
```

---

## Trocar para uma branch

```bash
git switch feature/contato
```

---

## Voltar para a `main`

```bash
git switch main
```

---

## Enviar uma nova branch para o GitHub

```bash
git push -u origin feature/contato
```

---

## Fazer o merge

Estando na `main`:

```bash
git merge feature/contato
```

---

## Enviar a `main` atualizada

```bash
git push
```

---

## Excluir uma branch local

```bash
git branch -d feature/contato
```

---

## Excluir uma branch remota

```bash
git push origin --delete feature/contato
```

---

# 39. Conceito principal

Uma branch é uma linha de desenvolvimento separada.

Exemplo inicial:

```text
A → B → C
        ↑
       main
```

Depois da criação:

```text
A → B → C
        ↑
       main
        ↑
feature/contato
```

Depois de um commit na feature:

```text
A → B → C → D
        ↑     ↑
       main  feature/contato
```

A `main` continua em `C`.

A `feature/contato` avançou para `D`.

Depois do merge:

```text
A → B → C → D
              ↑
             main
```

Agora a `main` também contém a funcionalidade.

---

# 40. Branches em projetos reais

Branches normalmente representam tarefas específicas.

Exemplos:

```text
feature/login
feature/contato
feature/cadastro

fix/menu
fix/login
fix/cadastro
```

Fluxo básico:

```text
tarefa
  ↓
criar branch
  ↓
desenvolver
  ↓
commit
  ↓
push
  ↓
merge
  ↓
main
```

---

# 41. E o Pull Request?

Nesta prática, fizemos o merge diretamente pelo terminal:

```bash
git merge feature/contato
```

Isso é importante para entender o funcionamento do Git.

Em equipes, porém, é muito comum não fazer o merge diretamente na `main`.

Nesse caso, o fluxo costuma ser:

```text
feature/contato
        ↓
       push
        ↓
  Pull Request
        ↓
     revisão
        ↓
      merge
        ↓
       main
```

O Pull Request é um recurso da plataforma, como GitHub, usado para revisar e aprovar alterações antes do merge.

O conceito de merge continua sendo o mesmo.

---

# Resultado esperado

Ao final desta prática, você deverá saber:

- visualizar as branches existentes;
- identificar a branch atual;
- criar uma nova branch;
- trocar de branch;
- entender de qual commit uma branch foi criada;
- realizar alterações em uma branch separada;
- criar commits nessa branch;
- enviar a branch para o GitHub;
- voltar para a `main`;
- fazer um merge usando `git merge`;
- enviar a `main` atualizada para o GitHub;
- excluir uma branch local;
- excluir uma branch remota;
- entender a diferença entre `git merge` e Pull Request.
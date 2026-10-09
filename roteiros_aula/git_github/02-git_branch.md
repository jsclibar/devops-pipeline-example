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

Agora teremos algo parecido com:

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

Esse é um dos principais conceitos de branch:

> Cada branch pode representar um estado diferente do projeto.

---

# 28. Conferir os remotos

Antes de enviar a nova branch para o GitHub, confira o remoto:

```bash
git remote -v
```

Deve aparecer o repositório do aluno como `origin`.

Exemplo:

```text
origin  https://github.com/USUARIO/site-empresa.git (fetch)
origin  https://github.com/USUARIO/site-empresa.git (push)
```

---

# 29. Enviar a branch para o GitHub

Envie a branch atual para o repositório remoto:

```bash
git push -u origin feature/contato
```

Esse comando envia:

```text
feature/contato local
        ↓
feature/contato no GitHub
```

O `-u` salva a relação entre:

```text
feature/contato local
        ↕
origin/feature/contato
```

Depois disso, futuros `push` nessa branch podem ser feitos apenas com:

```bash
git push
```

---

# 30. Conferir as branches no GitHub

Acesse o repositório no GitHub.

Agora devem existir duas branches:

```text
main
feature/contato
```

A branch `main` representa a versão principal do projeto.

A branch `feature/contato` contém a nova funcionalidade.

---

# 31. Abrir um Pull Request

No GitHub, crie um Pull Request para enviar as alterações da:

```text
feature/contato
```

para:

```text
main
```

O fluxo será:

```text
feature/contato
        ↓
   Pull Request
        ↓
       main
```

O Pull Request permite revisar as alterações antes de integrá-las à branch principal.

---

# 32. Conferir o Pull Request

Antes do merge, confira:

- os commits;
- os arquivos alterados;
- as linhas adicionadas;
- as linhas removidas;
- a branch de origem;
- a branch de destino.

Neste caso:

```text
origem:
feature/contato

destino:
main
```

---

# 33. Fazer o Merge

Depois de revisar, faça o merge no GitHub.

A alteração da branch:

```text
feature/contato
```

passará a fazer parte da:

```text
main
```

Antes:

```text
A → B → C
        \
         D
         ↑
feature/contato
```

Depois do merge:

```text
A → B → C → D
              ↑
             main
```

---

# 34. Entender o que aconteceu localmente

O merge foi realizado no GitHub.

Mas sua `main` local ainda pode estar desatualizada.

Primeiro, volte para a `main`:

```bash
git switch main
```

Confira:

```bash
git branch
```

Agora:

```text
  feature/contato
* main
```

---

# 35. Atualizar a main local

Busque as alterações que foram integradas no GitHub:

```bash
git pull
```

Agora sua `main` local deve receber o commit da página de contato.

Confira:

```bash
ls
```

O arquivo:

```text
contato.html
```

deve aparecer.

---

# 36. Conferir o histórico

Veja o histórico atualizado:

```bash
git log --oneline --decorate
```

Agora a `main` deve conter a alteração que antes existia apenas na `feature/contato`.

---

# 37. Excluir a branch local

Depois que a funcionalidade já foi integrada à `main`, a branch local pode ser removida.

Primeiro confirme que está na `main`:

```bash
git branch
```

Depois exclua:

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

# 38. Excluir a branch remota

Se a branch ainda existir no GitHub, ela também pode ser removida.

Isso pode ser feito pelo próprio GitHub depois do merge.

Em muitos casos, o GitHub apresenta o botão:

```text
Delete branch
```

Depois da exclusão, a branch deixa de existir no repositório remoto.

---

# 39. Fluxo completo

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
Pull Request
  ↓
revisão
  ↓
merge
  ↓
main no GitHub
  ↓
git pull
  ↓
main local atualizada
```

---

# 40. Principais comandos de Branch

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

## Voltar para a main

```bash
git switch main
```

---

## Enviar a branch para o GitHub

```bash
git push -u origin feature/contato
```

---

## Atualizar a main depois do merge

```bash
git pull
```

---

## Excluir uma branch local

```bash
git branch -d feature/contato
```

---

# 41. Conceito principal

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

Depois de um novo commit na feature:

```text
A → B → C → D
        ↑     ↑
       main  feature/contato
```

A `main` continua em `C`.

A `feature/contato` avançou para `D`.

---

# 42. Branches em projetos reais

Branches normalmente representam trabalhos específicos.

Exemplos:

```text
feature/login
feature/contato
feature/cadastro

fix/menu
fix/login
fix/cadastro
```

A ideia é evitar trabalhar diretamente na branch principal.

Fluxo comum:

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
Pull Request
  ↓
revisão
  ↓
merge
```

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
- abrir um Pull Request;
- revisar as alterações;
- realizar o merge;
- atualizar a `main` local;
- excluir uma branch depois que o trabalho foi concluído.
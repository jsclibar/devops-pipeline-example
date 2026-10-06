# Git na prática

Nesta atividade, vamos criar um pequeno projeto HTML + CSS e acompanhar sua evolução usando Git.

O objetivo é praticar o fluxo básico de versionamento:

**criar → alterar → preparar → registrar → consultar → corrigir → desfazer**

---

# 1. Criando o projeto

Crie a pasta do projeto:

```bash
mkdir site-empresa
cd site-empresa
```

Verifique o estado:

```bash
git status
```

Inicialize o repositório Git:

```bash
git init
```

Confira novamente:

```bash
git status
```

---

# 2. Criando os primeiros arquivos

Crie a página principal:

```bash
echo "<h1>Empresa ABC</h1>" > index.html
```

Crie o arquivo de estilos:

```bash
echo "body { color: black; }" > style.css
```

Confira os arquivos:

```bash
ls
```

Veja o estado do repositório:

```bash
git status
```

Neste momento, os arquivos devem aparecer como **untracked**.

---

# 3. Preparando os arquivos

Adicione apenas o `index.html`:

```bash
git add index.html
```

Confira:

```bash
git status
```

Agora adicione o `style.css`:

```bash
git add style.css
```

Confira novamente:

```bash
git status
```

Os dois arquivos devem estar preparados para o próximo commit.

---

# 4. Primeiro commit

Registre a primeira versão do projeto:

```bash
git commit -m "Adiciona estrutura inicial do site"
```

Confira o estado:

```bash
git status
```

Veja o histórico completo:

```bash
git log
```

Veja o histórico resumido:

```bash
git log --oneline
```

---

# 5. Criando uma nova página

Crie a página institucional:

```bash
echo "<h1>Sobre a Empresa ABC</h1>" > sobre.html
```

Veja o estado:

```bash
git status
```

Adicione o novo arquivo:

```bash
git add sobre.html
```

Crie o commit:

```bash
git commit -m "Adiciona página sobre"
```

Confira:

```bash
git log --oneline
```

---

# 6. Alterando arquivos existentes

Adicione uma mensagem à página inicial:

```bash
echo "<p>Bem-vindo ao nosso site</p>" >> index.html
```

Adicione uma nova regra ao CSS:

```bash
echo "h1 { font-size: 32px; }" >> style.css
```

Veja quais arquivos foram alterados:

```bash
git status
```

Veja exatamente o que mudou:

```bash
git diff
```

Prepare todas as alterações:

```bash
git add .
```

Crie o commit:

```bash
git commit -m "Atualiza página inicial e estilos"
```

Confira:

```bash
git log --oneline
```

---

# 7. Commitando arquivos já rastreados

Adicione uma informação à página `sobre.html`:

```bash
echo "<p>Fundada em 1980</p>" >> sobre.html
```

Veja o estado:

```bash
git status
```

Veja a alteração:

```bash
git diff
```

Faça o commit usando `-a`:

```bash
git commit -a -m "Adiciona data de fundação"
```

Confira:

```bash
git log --oneline
```

Veja o histórico com mais detalhes:

```bash
git log -p
```

> O `-a` inclui automaticamente alterações de arquivos que já são rastreados pelo Git.
>
> Arquivos novos/untracked não são adicionados automaticamente.

---

# 8. Renomeando um arquivo

Renomeie a página:

```bash
git mv sobre.html empresa.html
```

Confira:

```bash
git status
```

Registre a alteração:

```bash
git commit -m "Renomeia página institucional"
```

---

# 9. Removendo um arquivo

Remova o arquivo `empresa.html`:

```bash
git rm empresa.html
```

Confira:

```bash
git status
```

Não faça o commit ainda.

---

# 10. Recuperando um arquivo removido

Retire a remoção do staging:

```bash
git restore --staged empresa.html
```

Confira:

```bash
git status
```

Agora restaure o arquivo:

```bash
git restore empresa.html
```

Confira:

```bash
ls
git status
```

O arquivo deve aparecer novamente.

Fluxo:

```text
git rm empresa.html
        ↓
arquivo removido + staged
        ↓
git restore --staged empresa.html
        ↓
remoção unstaged
        ↓
git restore empresa.html
        ↓
arquivo recuperado
```

---

# 11. Desfazendo uma alteração antes do `git add`

Adicione uma alteração ao CSS:

```bash
echo "body { background: red; }" >> style.css
```

Veja a alteração:

```bash
git diff
```

Desfaça:

```bash
git restore style.css
```

Confira:

```bash
git status
```

---

# 12. Desfazendo uma alteração depois do `git add`

Faça a alteração novamente:

```bash
echo "body { background: red; }" >> style.css
```

Adicione ao staging:

```bash
git add style.css
```

Confira:

```bash
git status
```

Retire do staging:

```bash
git restore --staged style.css
```

Agora descarte a alteração:

```bash
git restore style.css
```

Confira:

```bash
git status
```

Regra:

```text
Ainda não dei git add
→ git restore arquivo

Já dei git add
→ git restore --staged arquivo
→ git restore arquivo
```

---

# 13. Corrigindo o último commit

Adicione um rodapé:

```bash
echo "<footer>Empresa ABC</footer>" >> index.html
```

Prepare:

```bash
git add index.html
```

Faça o commit:

```bash
git commit -m "Adiciona rodapé"
```

Agora adicione outra informação:

```bash
echo "<p>Todos os direitos reservados</p>" >> index.html
```

Prepare novamente:

```bash
git add index.html
```

Corrija o último commit:

```bash
git commit --amend --no-edit
```

Confira:

```bash
git log --oneline
```

Para alterar apenas a mensagem do último commit:

```bash
git commit --amend -m "Nova mensagem"
```

---

# 14. Desfazendo um commit com `revert`

Adicione uma informação incorreta:

```bash
echo "<h2>PROMOÇÃO NÃO APROVADA</h2>" >> index.html
```

Prepare:

```bash
git add index.html
```

Faça o commit:

```bash
git commit -m "Adiciona promoção"
```

Confira:

```bash
git log --oneline
```

Desfaça o último commit preservando o histórico:

```bash
git revert --no-edit HEAD
```

Confira novamente:

```bash
git log --oneline
```

Veja o conteúdo:

```bash
cat index.html
```

O commit incorreto continua no histórico, mas outro commit foi criado para desfazer suas alterações.

---

# 15. Criando um commit experimental

Adicione uma nova versão ao HTML:

```bash
echo "<h2>Nova versão do site</h2>" >> index.html
```

Adicione uma nova regra ao CSS:

```bash
echo "h2 { color: blue; }" >> style.css
```

Prepare tudo:

```bash
git add .
```

Faça o commit:

```bash
git commit -m "Testa novo visual"
```

Confira:

```bash
git log --oneline
```

Antes de continuar:

```text
HEAD
→ commit atual

HEAD~1
→ um commit antes

HEAD~2
→ dois commits antes
```

---

# 16. Reset Soft

Volte um commit mantendo as alterações preparadas:

```bash
git reset --soft HEAD~1
```

Confira:

```bash
git log --oneline
git status
```

As alterações continuam em **staged**.

Resumo:

```text
SOFT
volta o histórico
mantém staged
```

Recrie o commit:

```bash
git commit -m "Testa novo visual"
```

---

# 17. Reset Mixed

Volte um commit mantendo as alterações nos arquivos:

```bash
git reset --mixed HEAD~1
```

Também poderia ser usado:

```bash
git reset HEAD~1
```

Confira:

```bash
git status
```

As alterações continuam nos arquivos, mas agora estão **unstaged**.

Resumo:

```text
MIXED
volta o histórico
mantém alterações
mas unstaged
```

Prepare novamente:

```bash
git add .
```

Recrie o commit:

```bash
git commit -m "Testa novo visual"
```

---

# 18. Reset Hard

Agora volte um commit descartando as alterações:

```bash
git reset --hard HEAD~1
```

Confira:

```bash
git status
git log --oneline
```

Veja o conteúdo dos arquivos:

```bash
cat index.html
cat style.css
```

As alterações do último commit devem ter sido descartadas.

Resumo:

```text
HARD
volta o histórico
descarta alterações
```

> Atenção: `git reset --hard` pode descartar trabalho.

---

# 19. Comparação dos tipos de reset

| Tipo | O que acontece com as alterações? |
|---|---|
| `--soft` | continuam **staged** |
| `--mixed` | continuam **unstaged** |
| `--hard` | são **descartadas** |

```text
git reset HEAD~1
       │
   ┌───┼───┐
   │   │   │
 soft mixed hard
   │   │   │
staged │ descartado
     unstaged
```

---

# 20. `git reset` sem voltar no histórico

Se você executar apenas:

```bash
git reset
```

o comportamento padrão é equivalente a:

```bash
git reset --mixed HEAD
```

Nesse caso, o histórico não volta.

As alterações saem do staging e continuam nos arquivos.

Exemplo:

```text
ANTES

index.html → staged
style.css  → staged


git reset


DEPOIS

index.html → modified / unstaged
style.css  → modified / unstaged
```

Para retirar alterações do staging de forma mais explícita, também pode ser usado:

```bash
git restore --staged .
```

---

# 21. Resumo dos comandos

| Situação | Comando |
|---|---|
| Iniciar um repositório | `git init` |
| Ver o estado | `git status` |
| Ver diferenças | `git diff` |
| Preparar um arquivo | `git add arquivo` |
| Preparar vários arquivos | `git add .` |
| Criar commit | `git commit -m "mensagem"` |
| Commitar arquivos rastreados | `git commit -a -m "mensagem"` |
| Ver histórico | `git log` |
| Ver histórico resumido | `git log --oneline` |
| Ver histórico detalhado | `git log -p` |
| Renomear arquivo | `git mv` |
| Remover arquivo | `git rm` |
| Retirar do staging | `git restore --staged` |
| Descartar alteração | `git restore` |
| Corrigir último commit | `git commit --amend` |
| Desfazer preservando histórico | `git revert` |
| Voltar mantendo staged | `git reset --soft` |
| Voltar mantendo unstaged | `git reset --mixed` |
| Voltar descartando alterações | `git reset --hard` |

---

# 22. Fluxo básico do Git

```text
ALTERAR
   ↓
git status
   ↓
git diff
   ↓
git add
   ↓
git commit
   ↓
git log
   ↓
ALTERAR NOVAMENTE
```

---

# 23. Quando algo der errado

```text
Alteração ainda não staged
→ git restore

Alteração staged
→ git restore --staged
→ git restore

Último commit precisa ser corrigido
→ git commit --amend

Commit precisa ser desfeito mantendo o histórico
→ git revert

Histórico precisa voltar
→ git reset
```

---

# 24. Final da prática

Até aqui, todo o projeto e todo o histórico estão somente no computador local.

Na próxima etapa, vamos aprender como compartilhar esse repositório com outras pessoas usando o GitHub.

```text
Git local
    ↓
GitHub
    ↓
Repositório remoto
    ↓
push / pull / clone
    ↓
Equipe
```
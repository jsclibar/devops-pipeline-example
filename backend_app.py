# Importa o FastAPI, framework usado para criar a API
# HTTPException é usado para retornar erros HTTP
from fastapi import FastAPI, HTTPException

# Importa o BaseModel do Pydantic
# Ele será usado para definir e validar os dados da API
from pydantic import BaseModel

# Importa o Uvicorn, servidor responsável por executar a aplicação
import uvicorn


# Cria a aplicação FastAPI e define as informações da documentação
app = FastAPI(
    title="Backend (API) da Biblioteca Comunitária Saber",
    description="API para gerenciamento do acervo de livros da biblioteca",
    version="1.0.0"
)


# ---------------------------------------------------------
# MODELOS PYDANTIC
# ---------------------------------------------------------

# Define o modelo dos dados recebidos para cadastro e atualização
# O título, autor e ano são obrigatórios
class Livro(BaseModel):
    titulo: str
    autor: str
    ano: int


# Define o modelo dos livros retornados pela API
# Herda os atributos de Livro e acrescenta o identificador
class LivroResposta(Livro):
    idlivro: int


# Define o modelo da resposta da página inicial
class Mensagem(BaseModel):
    message: str


# Define o modelo das respostas de cadastro e atualização
# Contém uma mensagem e os dados completos do livro
class RespostaLivro(BaseModel):
    message: str
    livro: LivroResposta


# Define o modelo da resposta de exclusão
# Contém uma mensagem e o ID do livro excluído
class RespostaExclusao(BaseModel):
    message: str
    idlivro: int


# ---------------------------------------------------------
# ARMAZENAMENTO DOS DADOS
# ---------------------------------------------------------

# Lista de livros armazenada em memória
# Compartilhada entre os endpoints da API
livros = [
    {
        "idlivro": 1,
        "titulo": "Dom Casmurro",
        "autor": "Machado de Assis",
        "ano": 1899
    },
    {
        "idlivro": 2,
        "titulo": "Memórias Póstumas de Brás Cubas",
        "autor": "Machado de Assis",
        "ano": 1881
    }
]

# Controla o ID do próximo livro
proximo_id = 3


# ---------------------------------------------------------
# ENDPOINT GET /
# ---------------------------------------------------------

# Retorna uma mensagem simples para verificar se a API está funcionando
@app.get(
    "/",
    tags=["Geral"],
    summary="Página inicial",
    response_model=Mensagem
)
def home():
    return {
        "message": "Bem-vindo à API da Biblioteca Comunitária Saber"
    }


# ---------------------------------------------------------
# ENDPOINT GET /livros
# ---------------------------------------------------------

# Retorna a lista de todos os livros
@app.get(
    "/livros",
    tags=["Livros"],
    summary="Listar livros",
    response_model=list[LivroResposta]
)
def listar_livros():
    return livros


# ---------------------------------------------------------
# ENDPOINT GET /livros/autor/{nome}
# ---------------------------------------------------------

# Retorna todos os livros de um determinado autor
# Desafio adicional (opcional)
@app.get(
    "/livros/autor/{nome}",
    tags=["Livros"],
    summary="Buscar livros por autor",
    response_model=list[LivroResposta]
)
def buscar_livros_por_autor(nome: str):

    # Cria uma lista para armazenar os livros encontrados
    livros_encontrados = []

    # Percorre a lista procurando livros do autor informado
    for livro in livros:
        if livro["autor"].lower() == nome.lower():
            livros_encontrados.append(livro)

    # Retorna os livros encontrados
    # Caso não encontre nenhum, retorna uma lista vazia
    return livros_encontrados


# ---------------------------------------------------------
# ENDPOINT GET /livros/{idlivro}
# ---------------------------------------------------------

# Retorna um livro específico através do ID
@app.get(
    "/livros/{idlivro}",
    tags=["Livros"],
    summary="Buscar livro por ID",
    response_model=LivroResposta,
    responses={
        404: {"description": "Livro não encontrado"}
    }
)
def buscar_livro(idlivro: int):

    # Percorre a lista procurando o livro pelo ID
    for livro in livros:
        if livro["idlivro"] == idlivro:
            return livro

    # Se o livro não for encontrado, lança uma exceção HTTP
    # O FastAPI transforma essa exceção em uma resposta com status 404
    raise HTTPException(
        status_code=404,
        detail="Livro não encontrado"
    )


# ---------------------------------------------------------
# ENDPOINT POST /livros
# ---------------------------------------------------------

# Recebe os dados de um novo livro através do corpo (body) da requisição
@app.post(
    "/livros",
    tags=["Livros"],
    summary="Cadastrar livro",
    status_code=201,
    response_model=RespostaLivro
)
def cadastrar_livro(livro: Livro):

    global proximo_id

    # Cria um novo livro
    novo_livro = {
        "idlivro": proximo_id,
        "titulo": livro.titulo,
        "autor": livro.autor,
        "ano": livro.ano
    }

    # Adiciona o livro à lista
    livros.append(novo_livro)

    # Incrementa o ID para o próximo cadastro
    proximo_id += 1

    # Retorna a mensagem e os dados do livro cadastrado
    return {
        "message": "Livro cadastrado com sucesso",
        "livro": novo_livro
    }


# ---------------------------------------------------------
# ENDPOINT PUT /livros/{idlivro}
# ---------------------------------------------------------

# Recebe o ID do livro e os novos dados através do corpo (body) da requisição
@app.put(
    "/livros/{idlivro}",
    tags=["Livros"],
    summary="Atualizar livro",
    response_model=RespostaLivro,
    responses={
        404: {"description": "Livro não encontrado"}
    }
)
def atualizar_livro(idlivro: int, dados: Livro):

    # Percorre a lista procurando o livro pelo ID
    for livro in livros:
        if livro["idlivro"] == idlivro:

            # Atualiza os dados do livro
            livro["titulo"] = dados.titulo
            livro["autor"] = dados.autor
            livro["ano"] = dados.ano

            # Retorna a mensagem e os dados atualizados
            return {
                "message": "Livro atualizado com sucesso",
                "livro": livro
            }

    # Se o livro não for encontrado, lança uma exceção HTTP
    raise HTTPException(
        status_code=404,
        detail="Livro não encontrado"
    )


# ---------------------------------------------------------
# ENDPOINT DELETE /livros/{idlivro}
# ---------------------------------------------------------

# Recebe o ID do livro que será excluído
@app.delete(
    "/livros/{idlivro}",
    tags=["Livros"],
    summary="Excluir livro",
    response_model=RespostaExclusao,
    responses={
        404: {"description": "Livro não encontrado"}
    }
)
def excluir_livro(idlivro: int):

    # Percorre a lista procurando o livro pelo ID
    for livro in livros:
        if livro["idlivro"] == idlivro:

            # Remove o livro da lista
            livros.remove(livro)

            # Retorna a mensagem e o ID do livro excluído
            return {
                "message": "Livro excluído com sucesso",
                "idlivro": idlivro
            }

    # Se o livro não for encontrado, lança uma exceção HTTP
    raise HTTPException(
        status_code=404,
        detail="Livro não encontrado"
    )


# ---------------------------------------------------------
# EXECUÇÃO DA APLICAÇÃO
# ---------------------------------------------------------

# Executa o servidor Uvicorn somente quando este arquivo é iniciado diretamente
if __name__ == "__main__":
    uvicorn.run(
        "backend_app:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )

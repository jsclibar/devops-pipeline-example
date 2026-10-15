# Importa o pytest para organizar os testes
import pytest

# Importa o cliente de testes do FastAPI
from fastapi.testclient import TestClient

# Importa a aplicação Python
import backend_app


# Cria o cliente de testes
client = TestClient(backend_app.app)


# Prepara um ambiente limpo antes de cada teste
@pytest.fixture(autouse=True)
def preparar_ambiente():

    # Limpa a lista de livros
    backend_app.livros.clear()

    # Reinicia o contador de identificadores
    backend_app.proximo_id = 1


# ---------------------------------------------------------
# TESTE GET /
# ---------------------------------------------------------

# Verifica se a API está respondendo
def test_home():

    response = client.get("/")

    assert response.status_code == 200

    assert response.json() == {
        "message": "Bem-vindo à API da Biblioteca Comunitária Saber"
    }


# ---------------------------------------------------------
# TESTE GET /livros
# ---------------------------------------------------------

# Verifica se a API retorna uma lista de livros
def test_listar_livros():

    response = client.get("/livros")

    assert response.status_code == 200

    assert response.json() == []


# ---------------------------------------------------------
# TESTE POST /livros
# ---------------------------------------------------------

# Verifica se é possível cadastrar um livro
def test_cadastrar_livro():

    dados = {
        "titulo": "Livro de Teste",
        "autor": "Autor de Teste",
        "ano": 2025
    }

    response = client.post("/livros", json=dados)

    assert response.status_code == 201

    assert response.json()["message"] == "Livro cadastrado com sucesso"

    assert response.json()["livro"] == {
        "idlivro": 1,
        "titulo": "Livro de Teste",
        "autor": "Autor de Teste",
        "ano": 2025
    }


# Verifica se a API rejeita um cadastro com dados incompletos
def test_cadastrar_livro_invalido():

    dados = {
        "titulo": "Livro de Teste",
        "ano": 2025
    }

    response = client.post("/livros", json=dados)

    assert response.status_code == 422


# ---------------------------------------------------------
# TESTE GET /livros/{idlivro}
# ---------------------------------------------------------

# Verifica se é possível consultar um livro pelo ID
def test_buscar_livro():

    # Prepara os dados necessários
    livro = {
        "idlivro": 1,
        "titulo": "Livro de Teste",
        "autor": "Autor de Teste",
        "ano": 2025
    }

    backend_app.livros.append(livro)

    # Executa a consulta
    response = client.get("/livros/1")

    assert response.status_code == 200

    assert response.json() == livro


# Verifica o retorno HTTP 404 para um livro inexistente
def test_buscar_livro_inexistente():

    response = client.get("/livros/999")

    assert response.status_code == 404

    assert response.json()["detail"] == "Livro não encontrado"


# Verifica o retorno HTTP 422 quando o ID é inválido
def test_buscar_livro_id_invalido():

    response = client.get("/livros/abc")

    assert response.status_code == 422


# ---------------------------------------------------------
# TESTE GET /livros/autor/{nome}
# ---------------------------------------------------------

# Verifica se a API encontra livros de um autor
def test_buscar_livros_por_autor():

    # Prepara os dados necessários
    backend_app.livros.extend([
        {
            "idlivro": 1,
            "titulo": "Livro A",
            "autor": "Autor Teste",
            "ano": 2020
        },
        {
            "idlivro": 2,
            "titulo": "Livro B",
            "autor": "Autor Teste",
            "ano": 2021
        },
        {
            "idlivro": 3,
            "titulo": "Livro C",
            "autor": "Outro Autor",
            "ano": 2022
        }
    ])

    # Executa a consulta
    response = client.get("/livros/autor/Autor Teste")

    assert response.status_code == 200

    assert len(response.json()) == 2

    for livro in response.json():
        assert livro["autor"] == "Autor Teste"


# Verifica se a API retorna uma lista vazia quando não encontra o autor
def test_buscar_autor_inexistente():

    response = client.get("/livros/autor/Autor Inexistente")

    assert response.status_code == 200

    assert response.json() == []


# ---------------------------------------------------------
# TESTE PUT /livros/{idlivro}
# ---------------------------------------------------------

# Verifica se é possível atualizar um livro
def test_atualizar_livro():

    # Prepara os dados necessários
    backend_app.livros.append({
        "idlivro": 1,
        "titulo": "Título Original",
        "autor": "Autor Original",
        "ano": 2020
    })

    # Define os novos dados
    dados = {
        "titulo": "Título Atualizado",
        "autor": "Autor Atualizado",
        "ano": 2025
    }

    # Executa a atualização
    response = client.put("/livros/1", json=dados)

    assert response.status_code == 200

    assert response.json()["message"] == "Livro atualizado com sucesso"

    assert response.json()["livro"] == {
        "idlivro": 1,
        "titulo": "Título Atualizado",
        "autor": "Autor Atualizado",
        "ano": 2025
    }

    # Confirma que os dados foram realmente atualizados
    consulta = client.get("/livros/1")

    assert consulta.status_code == 200

    assert consulta.json()["titulo"] == "Título Atualizado"


# Verifica o retorno HTTP 404 ao atualizar um livro inexistente
def test_atualizar_livro_inexistente():

    dados = {
        "titulo": "Livro Atualizado",
        "autor": "Autor Teste",
        "ano": 2025
    }

    response = client.put("/livros/999", json=dados)

    assert response.status_code == 404


# ---------------------------------------------------------
# TESTE DELETE /livros/{idlivro}
# ---------------------------------------------------------

# Verifica se é possível excluir um livro
def test_excluir_livro():

    # Prepara os dados necessários
    backend_app.livros.append({
        "idlivro": 1,
        "titulo": "Livro para Exclusão",
        "autor": "Autor Teste",
        "ano": 2025
    })

    # Executa a exclusão
    response = client.delete("/livros/1")

    assert response.status_code == 200

    assert response.json() == {
        "message": "Livro excluído com sucesso",
        "idlivro": 1
    }

    # Confirma que o livro não existe mais
    consulta = client.get("/livros/1")

    assert consulta.status_code == 404


# Verifica o retorno HTTP 404 ao excluir um livro inexistente
def test_excluir_livro_inexistente():

    response = client.delete("/livros/999")

    assert response.status_code == 404

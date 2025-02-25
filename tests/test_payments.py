import pytest
from app.payment_processor import processar_arquivo, validar_comprovante
from app.utils import salvar_log
import os

# Fixture para criar um arquivo de comprovante de teste
@pytest.fixture
def comprovante_imagem(tmpdir):
    """
    Cria um arquivo de imagem de comprovante de teste.
    """
    file_path = tmpdir.join("comprovante.jpg")
    with open(file_path, "w") as f:
        f.write("Dados fictícios de um comprovante de pagamento.")
    return str(file_path)

@pytest.fixture
def comprovante_pdf(tmpdir):
    """
    Cria um arquivo de PDF de comprovante de teste.
    """
    file_path = tmpdir.join("comprovante.pdf")
    with open(file_path, "w") as f:
        f.write("Dados fictícios de um comprovante de pagamento.")
    return str(file_path)

def test_processar_arquivo_imagem(comprovante_imagem):
    """
    Testa a função processar_arquivo com um arquivo de imagem.
    """
    texto = processar_arquivo(comprovante_imagem)
    assert texto is not None
    assert "Dados fictícios" in texto  # Verifica se o texto esperado foi extraído

def test_processar_arquivo_pdf(comprovante_pdf):
    """
    Testa a função processar_arquivo com um arquivo de PDF.
    """
    texto = processar_arquivo(comprovante_pdf)
    assert texto is not None
    assert "Dados fictícios" in texto  # Verifica se o texto esperado foi extraído

def test_validar_comprovante():
    """
    Testa a função validar_comprovante com um texto de comprovante válido.
    """
    texto = """
    Comprovante de Pagamento
    Nome: João Silva
    Valor: R$ 100,00
    Data: 01/10/2023
    """
    mensagem = validar_comprovante(texto)
    assert "Comprovante validado!" in mensagem
    assert "Valor: R$ 100,00" in mensagem
    assert "Data: 01/10/2023" in mensagem
    assert "Pagador: João Silva" in mensagem

def test_validar_comprovante_sem_valor():
    """
    Testa a função validar_comprovante com um texto sem valor.
    """
    texto = """
    Comprovante de Pagamento
    Nome: João Silva
    Data: 01/10/2023
    """
    mensagem = validar_comprovante(texto)
    assert "Valor não encontrado no comprovante." in mensagem

def test_validar_comprovante_sem_data():
    """
    Testa a função validar_comprovante com um texto sem data.
    """
    texto = """
    Comprovante de Pagamento
    Nome: João Silva
    Valor: R$ 100,00
    """
    mensagem = validar_comprovante(texto)
    assert "Data não encontrada no comprovante." in mensagem

def test_validar_comprovante_erro():
    """
    Testa a função validar_comprovante com um texto inválido.
    """
    texto = "Texto inválido"
    mensagem = validar_comprovante(texto)
    assert "Ocorreu um erro ao validar o comprovante." in mensagem
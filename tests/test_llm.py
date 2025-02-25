import pytest
from app.llm_handler import gerar_resposta
from app.utils import salvar_log
from app.config import LLAMA2_MODEL_PATH

# Fixture para carregar o modelo e o tokenizer
@pytest.fixture(scope="module")
def setup_model():
    """
    Carrega o modelo e o tokenizer para uso nos testes.
    """
    from transformers import AutoTokenizer, AutoModelForCausalLM

    # Verifica se o caminho do modelo foi configurado corretamente
    if not LLAMA2_MODEL_PATH:
        pytest.fail("Caminho do modelo LLaMA 2 não configurado. Verifique o arquivo .env.")

    try:
        salvar_log("Carregando tokenizer e modelo LLaMA 2 para testes...")
        tokenizer = AutoTokenizer.from_pretrained(LLAMA2_MODEL_PATH)
        model = AutoModelForCausalLM.from_pretrained(LLAMA2_MODEL_PATH)
        salvar_log("Tokenizer e modelo LLaMA 2 carregados com sucesso para testes!")
        return tokenizer, model
    except Exception as e:
        pytest.fail(f"Erro ao carregar o modelo LLaMA 2: {e}")

def test_gerar_resposta(setup_model):
    """
    Testa a função gerar_resposta com um prompt simples.
    """
    tokenizer, model = setup_model

    # Prompt de teste
    prompt = "Como posso participar da rifa?"

    # Gera a resposta
    resposta = gerar_resposta(prompt)

    # Verifica se a resposta foi gerada corretamente
    assert resposta is not None
    assert len(resposta) > 0  # Verifica se a resposta não está vazia
    salvar_log(f"Resposta gerada para o prompt '{prompt}': {resposta}")

def test_gerar_resposta_erro(setup_model, mocker):
    """
    Testa a função gerar_resposta com um erro simulado.
    """
    tokenizer, model = setup_model

    # Simula um erro ao gerar a resposta
    mocker.patch("app.llm_handler.model.generate", side_effect=Exception("Erro simulado"))

    # Prompt de teste
    prompt = "Como posso participar da rifa?"

    # Gera a resposta
    resposta = gerar_resposta(prompt)

    # Verifica se a mensagem de erro foi retornada
    assert resposta == "Desculpe, ocorreu um erro ao processar sua mensagem."
    salvar_log(f"Erro simulado ao gerar resposta para o prompt '{prompt}': {resposta}")

def test_gerar_resposta_prompt_vazio(setup_model):
    """
    Testa a função gerar_resposta com um prompt vazio.
    """
    tokenizer, model = setup_model

    # Prompt vazio
    prompt = ""

    # Gera a resposta
    resposta = gerar_resposta(prompt)

    # Verifica se a resposta foi gerada corretamente
    assert resposta is not None
    assert len(resposta) > 0  # Verifica se a resposta não está vazia
    salvar_log(f"Resposta gerada para o prompt vazio: {resposta}")
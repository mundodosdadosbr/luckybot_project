from transformers import AutoTokenizer, AutoModelForCausalLM

from app.config import LLAMA2_MODEL_PATH
from app.utils import salvar_log

# Verifica se o caminho do modelo foi configurado corretamente
if not LLAMA2_MODEL_PATH:
    raise ValueError("Caminho do modelo LLaMA 2 não configurado. Verifique o arquivo .env.")

# Carregar tokenizer e modelo
try:
    salvar_log("Carregando tokenizer e modelo LLaMA 2...")
    tokenizer = AutoTokenizer.from_pretrained(LLAMA2_MODEL_PATH)
    model = AutoModelForCausalLM.from_pretrained(LLAMA2_MODEL_PATH)
    salvar_log("Tokenizer e modelo LLaMA 2 carregados com sucesso!")
except Exception as e:
    salvar_log(f"Erro ao carregar o modelo LLaMA 2: {e}")
    raise

def gerar_resposta(prompt):
    """
    Gera uma resposta para o prompt fornecido usando o modelo LLaMA 2.

    Args:
        prompt (str): Texto de entrada para o modelo.

    Returns:
        str: Resposta gerada pelo modelo.
    """
    try:
        # Tokeniza o prompt
        inputs = tokenizer(prompt, return_tensors="pt")

        # Gera a resposta
        outputs = model.generate(
            **inputs,
            max_length=200,  # Tamanho máximo da resposta
            num_return_sequences=1,  # Número de respostas a serem geradas
            temperature=0.7,  # Controla a criatividade da resposta
            top_p=0.9,  # Controla a diversidade da resposta
            do_sample=True,  # Ativa a amostragem para respostas mais variadas
        )

        # Decodifica a resposta para texto
        resposta = tokenizer.decode(outputs[0], skip_special_tokens=True)
        salvar_log(f"Resposta gerada para o prompt: {prompt}")
        return resposta
    except Exception as e:
        salvar_log(f"Erro ao gerar resposta: {e}")
        return "Desculpe, ocorreu um erro ao processar sua mensagem."
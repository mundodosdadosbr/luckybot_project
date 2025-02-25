import os
import requests
from datetime import datetime
import logging

# Configuração básica de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def download_file(url, file_path):
    """
    Baixa um arquivo de uma URL e salva no caminho especificado.

    Args:
        url (str): URL do arquivo.
        file_path (str): Caminho onde o arquivo será salvo.

    Returns:
        bool: True se o download for bem-sucedido, False caso contrário.
    """
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Verifica se a requisição foi bem-sucedida

        # Cria o diretório se não existir
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Salva o arquivo
        with open(file_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        logger.info(f"Arquivo baixado e salvo em: {file_path}")
        return True
    except Exception as e:
        logger.error(f"Erro ao baixar o arquivo: {e}")
        return False

def salvar_log(mensagem):
    """
    Salva uma mensagem de log em um arquivo de log.

    Args:
        mensagem (str): Mensagem a ser salva no log.
    """
    log_dir = os.path.join("data", "logs")
    os.makedirs(log_dir, exist_ok=True)  # Cria o diretório de logs se não existir

    log_file = os.path.join(log_dir, "luckybot.log")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Adiciona a mensagem ao arquivo de log
    with open(log_file, "a") as f:
        f.write(f"[{timestamp}] {mensagem}\n")

    logger.info(mensagem)  # Também exibe o log no console

def validar_caminho(caminho):
    """
    Verifica se um caminho existe e, se não existir, cria o diretório.

    Args:
        caminho (str): Caminho a ser validado/criado.

    Returns:
        bool: True se o caminho existe ou foi criado, False caso contrário.
    """
    try:
        os.makedirs(caminho, exist_ok=True)
        return True
    except Exception as e:
        logger.error(f"Erro ao validar/criar o caminho {caminho}: {e}")
        return False
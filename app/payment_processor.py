import re

import pytesseract
from PIL import Image
from pdf2image import convert_from_path

from app.utils import salvar_log


def processar_arquivo(file_path):
    """
    Processa um arquivo (imagem ou PDF) e extrai o texto usando OCR.

    Args:
        file_path (str): Caminho do arquivo a ser processado.

    Returns:
        str: Texto extraído do arquivo.
    """
    try:
        salvar_log(f"Processando arquivo: {file_path}")

        # Verifica se o arquivo é um PDF
        if file_path.lower().endswith(".pdf"):
            # Converte o PDF em uma lista de imagens
            imagens = convert_from_path(file_path)
            texto = ""
            for imagem in imagens:
                # Extrai o texto de cada página do PDF
                texto += pytesseract.image_to_string(imagem, lang="por") + "\n"
        else:
            # Se for uma imagem, extrai o texto diretamente
            imagem = Image.open(file_path)
            texto = pytesseract.image_to_string(imagem, lang="por")

        salvar_log(f"Texto extraído: {texto[:100]}...")  # Log dos primeiros 100 caracteres
        return texto
    except Exception as e:
        salvar_log(f"Erro ao processar o arquivo {file_path}: {e}")
        return None

def validar_comprovante(texto):
    """
    Valida as informações extraídas de um comprovante de pagamento.

    Args:
        texto (str): Texto extraído do comprovante.

    Returns:
        str: Mensagem de validação (ex: "Comprovante validado! Valor: R$ 100,00, Data: 01/10/2023").
    """
    try:
        salvar_log("Validando comprovante...")

        # Extrair valor (ex: R$ 100,00)
        valor = re.search(r"R\$\s*(\d+,\d{2})", texto)
        if valor:
            valor = valor.group(1)
        else:
            return "Valor não encontrado no comprovante."

        # Extrair data (ex: 01/10/2023)
        data = re.search(r"(\d{2}/\d{2}/\d{4})", texto)
        if data:
            data = data.group(1)
        else:
            return "Data não encontrada no comprovante."

        # Extrair nome do pagador (ex: João Silva)
        nome = re.search(r"(?:Nome|Pagador):\s*([A-Za-z\s]+)", texto, re.IGNORECASE)
        if nome:
            nome = nome.group(1).strip()
        else:
            nome = "Não identificado"

        # Mensagem de sucesso
        mensagem = f"Comprovante validado! Valor: R$ {valor}, Data: {data}, Pagador: {nome}."
        salvar_log(mensagem)
        return mensagem
    except Exception as e:
        salvar_log(f"Erro ao validar comprovante: {e}")
        return "Ocorreu um erro ao validar o comprovante."
import requests
from bs4 import BeautifulSoup
import re
from unidecode import unidecode
import os

def coletar_texto_lei(url: str) -> str:
    """
    Faz a requisição HTTP ao site do Planalto e extrai o texto bruto da Lei,
    usando um User-Agent de navegador para evitar bloqueios.
    """
    print(f"[*] Iniciando coleta da URL: {url}")
    try:
        print("[*] Fazendo GET request para a URL com User-Agent...")
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/58.0.3029.110 Safari/537.3"
            )
        }
        response = requests.get(url, headers=headers)
        print(f"[*] Requisição concluída. Status code: {response.status_code}")
        response.raise_for_status()  # Levanta exceção se ocorrer erro HTTP

        # Exibe o tamanho do conteúdo em bytes
        print(f"[*] Tamanho do conteúdo retornado: {len(response.content)} bytes")

        print("[*] Iniciando parsing do HTML com BeautifulSoup...")
        soup = BeautifulSoup(response.content, 'html.parser')

        # Captura todo o texto que está no body
        print("[*] Extraindo texto do <body> do HTML...")
        raw_text = soup.body.get_text(separator="\n")
        print("[*] Extração concluída com sucesso!")
        return raw_text

    except requests.exceptions.RequestException as e:
        print("[ERRO] Ocorreu um problema na requisição:", e)
        raise e


def limpar_texto_lei(texto: str) -> str:
    """
    Aplica técnicas simples de limpeza no texto:
      - Remove espaços em branco extras
      - Remove quebras de linha em excesso
      - Remove/acerta caracteres indesejados
      - Converte acentos para formato sem acento (opcional)
    """
    print("[*] Iniciando processo de limpeza do texto...")
    # Remove espaços em branco em excesso
    texto_limpo = re.sub(r'\s+', ' ', texto)

    # Converte acentos (ex.: ç -> c, á -> a, etc.)
    texto_limpo = unidecode(texto_limpo)

    # Remove espaços no início e no fim
    texto_limpo = texto_limpo.strip()

    print("[*] Limpeza concluída.")
    return texto_limpo


if __name__ == "__main__":
    # URL oficial da Lei de Acesso à Informação
    url_lei = "https://www.planalto.gov.br/ccivil_03/_ato2011-2014/2011/lei/l12527.htm"
    
    print("[*] Iniciando coleta e limpeza da Lei de Acesso à Informação...")
    
    # Garantir que o diretório data/raw existe
    os.makedirs("data/raw", exist_ok=True)
    
    # 1. Coleta do texto bruto
    texto_bruto = coletar_texto_lei(url_lei)

    # 2. Limpeza do texto
    texto_processado = limpar_texto_lei(texto_bruto)

    # 3. Salvando o resultado em arquivo local
    arquivo_saida = "data/raw/lei_acesso_informacao_limpa.txt"
    try:
        print(f"[*] Salvando texto limpo no arquivo '{arquivo_saida}'...")
        with open(arquivo_saida, "w", encoding="utf-8") as f:
            f.write(texto_processado)
        print(f"[*] Arquivo '{arquivo_saida}' gerado com sucesso.")
    except Exception as e:
        print("[ERRO] Não foi possível salvar o arquivo:", e)
        raise e

    print("[*] Processo concluído.")

import re
import unicodedata
import os

def remover_cabecalhos_e_rodapes(linhas):
    """
    Remover possíveis cabeçalhos e rodapés indesejados (exemplo genérico).
    Ajuste de acordo com o texto específico.
    """
    linhas_filtradas = []
    for linha in linhas:
        # Exemplo: se houver 'página', 'voltar' etc., remova
        if "página" in linha.lower():
            continue
        if "voltar" in linha.lower():
            continue
        if "publicada no" in linha.lower():
            continue
        
        linhas_filtradas.append(linha)
    return linhas_filtradas

def remover_linhas_vazias_ou_muito_curtas(linhas, tamanho_minimo=4):
    """
    Remove linhas completamente vazias ou muito curtas.
    """
    return [linha for linha in linhas if len(linha.strip()) >= tamanho_minimo]


def normalizar_texto(texto: str) -> str:
    """
    Normaliza o texto removendo acentos, convertendo para minúsculas e
    removendo caracteres especiais.
    """
    # texto = texto.lower()  # Descomente se quiser forçar minúsculas

    # Remove espaços em branco múltiplos
    texto = re.sub(r'\s+', ' ', texto)

    # Remove possíveis caracteres estranhos repetidos (ex.: "-----")
    texto = re.sub(r'[-_=]{2,}', '', texto)

    texto = texto.strip()
    return texto


def segmentar_por_artigo(texto):
    """
    Segmenta o texto considerando o padrão:
      "Art. <número>" (A maiúsculo, seguido de ponto, espaço, número + 'o' ou 'º' ou nada)
    
    Utiliza re.split com lookahead, para não descartar o delimitador.
    """
    # Regex que busca "Art." (A maiúsculo) seguido possivelmente por espaço(s),
    # e depois um número (+ 'o' ou 'º' ou '°'), mas sem ignorar a parte do artigo no split:
    pattern = r'(?=Art\.\s*\d+(?:o|º|°)?)'

    partes = re.split(pattern, texto)

    # Limpa e remove elementos vazios
    partes = [p.strip() for p in partes if p.strip()]

    # Agora, cada posição de 'partes' ou é o preâmbulo (se não começar com 'Art.')
    # ou é algo que começa com "Art. <número>".
    artigos_segmentados = []

    for p in partes:
        # Verifica se o fragmento começa mesmo com "Art. " e extrai o número do artigo
        # Ex.: "Art. 1o Esta lei..." -> pega "1"
        m = re.match(r'Art\.\s*(\d+)', p)
        if m:
            # Extraímos o número do artigo da regex
            numero = m.group(1)
            # Armazena (ex.: "[ARTIGO_1]", texto do fragmento)
            artigos_segmentados.append((numero, p))
        else:
            # Se não começa com "Art.", então é o preâmbulo (ou outro texto)
            artigos_segmentados.append(("PREAMBULO", p))

    return artigos_segmentados


def limpar_e_normalizar_lei(caminho_entrada, caminho_saida):
    """
    Função principal que:
      1. Lê o texto de um arquivo
      2. Remove cabeçalhos, rodapés e linhas vazias
      3. Normaliza e segmenta por artigo
      4. Salva em arquivo com um rótulo coerente
    """
    with open(caminho_entrada, 'r', encoding='utf-8') as f:
        conteudo = f.read()

    # Divide em linhas
    linhas = conteudo.split('\n')

    print("[*] Removendo possíveis cabeçalhos/rodapés...")
    linhas = remover_cabecalhos_e_rodapes(linhas)

    print("[*] Removendo linhas vazias ou muito curtas...")
    linhas = remover_linhas_vazias_ou_muito_curtas(linhas)

    print("[*] Rejuntando em um único texto...")
    texto_unificado = " ".join(linhas)

    print("[*] Normalizando texto...")
    texto_normalizado = normalizar_texto(texto_unificado)

    print("[*] Segmentando texto por artigos (Art. X)...")
    lista_artigos = segmentar_por_artigo(texto_normalizado)

    print(f"[*] Salvando texto segmentado em: {caminho_saida}")
    with open(caminho_saida, 'w', encoding='utf-8') as f_out:
        for idx, (rotulo, texto_artigo) in enumerate(lista_artigos, start=1):
            if rotulo == "PREAMBULO":
                # Marque explicitamente como preâmbulo
                f_out.write("[PREAMBULO]\n")
                f_out.write(texto_artigo + "\n\n")
            else:
                # Use o número do artigo extraído
                f_out.write(f"[ARTIGO_{rotulo}]\n")
                f_out.write(texto_artigo + "\n\n")

    print("[*] Limpeza e normalização concluídas com sucesso!")


if __name__ == "__main__":
    print("[*] Iniciando normalização do texto da Lei de Acesso à Informação...")
    
    # Garantir que o diretório data/raw existe
    os.makedirs("data/raw", exist_ok=True)
    
    # 1. Carregar o texto limpo
    try:
        arquivo_entrada = "data/raw/lei_acesso_informacao_limpa.txt"
        print(f"[*] Carregando texto do arquivo '{arquivo_entrada}'...")
        with open(arquivo_entrada, "r", encoding="utf-8") as f:
            texto = f.read()
    except Exception as e:
        print("[ERRO] Não foi possível ler o arquivo:", e)
        raise e
    
    # 2. Normalizar o texto
    texto_normalizado = normalizar_texto(texto)
    
    # 3. Salvar o texto normalizado
    arquivo_saida = "data/raw/lei_acesso_informacao_normalizada.txt"
    try:
        print(f"[*] Salvando texto normalizado no arquivo '{arquivo_saida}'...")
        with open(arquivo_saida, "w", encoding="utf-8") as f:
            f.write(texto_normalizado)
        print(f"[*] Arquivo '{arquivo_saida}' gerado com sucesso.")
    except Exception as e:
        print("[ERRO] Não foi possível salvar o arquivo:", e)
        raise e
    
    print("[*] Processo concluído.")

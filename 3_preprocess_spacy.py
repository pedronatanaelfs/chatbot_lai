import spacy

def main():
    # 1) Carregar o modelo spaCy
    print("[*] Carregando modelo spaCy pt_core_news_lg...")
    nlp = spacy.load("pt_core_news_lg")
    print("[*] Modelo carregado com sucesso.")

    # 2) Ler o arquivo de texto normalizado da etapa anterior
    arquivo_entrada = "lei_acesso_informacao_normalizada.txt"
    print(f"[*] Lendo arquivo de entrada: {arquivo_entrada}...")
    with open(arquivo_entrada, 'r', encoding='utf-8') as f:
        texto = f.read()
    print("[*] Texto carregado.")
    
    # Exibir alguns caracteres iniciais para checar conteúdo
    print("\n[DEBUG] Primeiros 300 caracteres do texto:")
    print(texto[:300], "...")
    
    # 3) Processar o texto com spaCy
    print("\n[*] Iniciando processamento (tokenização, sentenças, POS, entidades)...")
    doc = nlp(texto)
    print("[*] Pipeline concluído.")

    # 4) Segmentação em sentenças
    sents = list(doc.sents)
    print(f"[*] Foram encontradas {len(sents)} sentenças no texto.")
    print("[DEBUG] Primeiras 2 sentenças:")
    for i, sent in enumerate(sents[:2], 1):
        print(f"   {i}) {sent.text.strip()}\n")

    # 5) Remover pontuação, espaços, stopwords e coletar tokens lematizados
    tokens_filtrados = []
    for token in doc:
        # Ignorar pontuação, espaços em branco e stopwords
        if token.is_punct or token.is_space or token.is_stop:
            continue
        tokens_filtrados.append((token.text, token.lemma_, token.pos_))

    print(f"[*] Total de tokens filtrados (sem pontuação, espaços e stopwords): {len(tokens_filtrados)}")
    print("[DEBUG] Exemplos de tokens filtrados (text, lemma, pos):")
    for t in tokens_filtrados[:10]:  # Mostra só os 10 primeiros
        print("   ", t)
    print()

    # 6) Extração de entidades
    ents = list(doc.ents)
    print(f"[*] Foram encontradas {len(ents)} entidades nomeadas no texto.")
    print("[DEBUG] Primeiras 5 entidades:")
    for i, ent in enumerate(ents[:5], 1):
        print(f"   {i}) Texto: '{ent.text}' | Label: {ent.label_}")
    print()

    # 7) (Opcional) Armazenar resultados em arquivos de texto
    # Se quiser salvar as sentenças, tokens e entidades, descomente abaixo:

    """
    with open("sentencas.txt", "w", encoding="utf-8") as f_sent:
        for sent in sents:
            f_sent.write(sent.text.strip() + "\n")

    with open("tokens_filtrados.txt", "w", encoding="utf-8") as f_tok:
        f_tok.write("TEXT\tLEMMA\tPOS\n")
        for texto_, lemma_, pos_ in tokens_filtrados:
            f_tok.write(f"{texto_}\t{lemma_}\t{pos_}\n")

    with open("entidades_ner.txt", "w", encoding="utf-8") as f_ent:
        f_ent.write("ENTIDADE\tLABEL\n")
        for ent in ents:
            f_ent.write(f"{ent.text}\t{ent.label_}\n")
    """

    print("[*] Fim do script. Todas as etapas foram executadas com sucesso.")

if __name__ == "__main__":
    main()

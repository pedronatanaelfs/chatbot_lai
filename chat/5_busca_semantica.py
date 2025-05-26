import os
import faiss
import pandas as pd
from tqdm import tqdm
from sentence_transformers import SentenceTransformer
from sklearn.preprocessing import normalize

# === 1. Carregar e estruturar os artigos ===

def carregar_artigos(caminho_txt="sentencas.txt"):
    artigos = []
    with open(caminho_txt, "r", encoding="utf-8") as f:
        bloco = ""
        artigo_id = ""
        for linha in f:
            linha = linha.strip()
            if linha.startswith("[ARTIGO_"):
                if artigo_id and bloco:
                    artigos.append({"id": artigo_id, "texto": bloco.strip()})
                artigo_id = linha.strip("[]")
                bloco = ""
            else:
                bloco += " " + linha
        # Adicionar o último artigo
        if artigo_id and bloco:
            artigos.append({"id": artigo_id, "texto": bloco.strip()})
    return artigos

# === 2. Gerar embeddings ===

def gerar_embeddings(textos, modelo_nome="paraphrase-multilingual-MiniLM-L12-v2"):
    print("[*] Carregando modelo de embeddings...")
    model = SentenceTransformer(modelo_nome)
    embeddings = model.encode(textos, show_progress_bar=True)
    embeddings = normalize(embeddings)  # normalização L2
    return embeddings, model

# === 3. Indexar com FAISS ===

def criar_index_faiss(embeddings):
    dim = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)  # IP = inner product (cosine sim. com vetores normalizados)
    index.add(embeddings)
    return index

# === 4. Buscar artigos relevantes ===

def buscar_pergunta(pergunta, model, index, artigos, top_k=3):
    pergunta_embedding = model.encode([pergunta])
    pergunta_embedding = normalize(pergunta_embedding)
    distancias, indices = index.search(pergunta_embedding, top_k)

    resultados = []
    for i, idx in enumerate(indices[0]):
        artigo = artigos[idx]
        resultados.append({
            "rank": i + 1,
            "id": artigo["id"],
            "trecho": artigo["texto"],
            "similaridade": float(distancias[0][i])
        })
    return resultados

# === 5. Simulação interativa ===

def main():
    print("[*] Carregando artigos...")
    artigos = carregar_artigos("sentencas.txt")
    textos = [a["texto"] for a in artigos]

    embeddings, model = gerar_embeddings(textos)
    index = criar_index_faiss(embeddings)

    print("\n[✓] Sistema pronto para busca. Digite uma pergunta ou 'sair' para encerrar.\n")

    while True:
        pergunta = input("🔎 Pergunta: ").strip()
        if pergunta.lower() in {"sair", "exit", "quit"}:
            break
        resultados = buscar_pergunta(pergunta, model, index, artigos)
        print("\n📌 Resultados mais relevantes:\n")
        for r in resultados:
            print(f"[{r['id']}] (simil: {r['similaridade']:.3f})\n{r['trecho']}\n---")
        print("\n")

if __name__ == "__main__":
    main()

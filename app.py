import os
import gc
import requests
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from dotenv import load_dotenv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

app = Flask(__name__)
CORS(app)

# === Configurar API ===
load_dotenv()
GROQ_API_KEY = os.getenv("LLAMA_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
LLM_MODEL = "llama3-8b-8192"  # Modelo menor e mais eficiente

# Variáveis globais para o modelo (otimizado)
artigos = None
vectorizer = None
tfidf_matrix = None

# === Carregar artigos da LAI ===
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
        if artigo_id and bloco:
            artigos.append({"id": artigo_id, "texto": bloco.strip()})
    return artigos

# === Usar TF-IDF como alternativa aos embeddings pesados ===
def criar_index_tfidf(textos):
    print("[*] Criando índice TF-IDF (uso eficiente de memória)...")
    vectorizer = TfidfVectorizer(
        max_features=5000,  # Limitar features
        stop_words=None,
        ngram_range=(1, 2),
        min_df=1,
        max_df=0.8
    )
    tfidf_matrix = vectorizer.fit_transform(textos)
    return vectorizer, tfidf_matrix

# === Buscar trechos relevantes com TF-IDF ===
def buscar_pergunta_tfidf(pergunta, vectorizer, tfidf_matrix, artigos, top_k=3):
    pergunta_vec = vectorizer.transform([pergunta])
    similaridades = cosine_similarity(pergunta_vec, tfidf_matrix).flatten()
    indices_ordenados = np.argsort(similaridades)[::-1][:top_k]
    resultados = [artigos[idx] for idx in indices_ordenados if similaridades[idx] > 0.1]
    return resultados[:top_k]

# === Construir prompt com contexto ===
def construir_prompt(pergunta, trechos):
    contexto = "\n\n".join([f"[{t['id']}]\n{t['texto']}" for t in trechos])
    prompt = f"""
Você é um assistente jurídico especializado na Lei de Acesso à Informação (LAI - Lei nº 12.527/2011).
Responda de forma clara e objetiva, como se estivesse explicando para um cidadão comum.

Contexto da LAI:
{contexto}

Pergunta: {pergunta}
Resposta:"""
    return prompt.strip()

# === Chamada à API da Groq (otimizada) ===
def gerar_resposta_llm(prompt):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "model": LLM_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.1,
        "max_tokens": 500  # Limitar tokens para economizar
    }

    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=body, timeout=10)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Erro ao gerar resposta: {str(e)}"

# === Inicializar o sistema (otimizado) ===
def inicializar_sistema():
    global artigos, vectorizer, tfidf_matrix
    print("[*] Inicializando sistema otimizado...")
    
    # Carregar artigos
    artigos = carregar_artigos("sentencas.txt")
    textos = [a["texto"] for a in artigos]
    
    # Usar TF-IDF em vez de embeddings pesados
    vectorizer, tfidf_matrix = criar_index_tfidf(textos)
    
    # Forçar limpeza de memória
    gc.collect()
    
    print(f"[✓] Sistema inicializado com {len(artigos)} artigos!")

# === Rotas da API ===
@app.route('/')
def index_page():
    return render_template('index.html')

@app.route('/api/pergunta', methods=['POST'])
def processar_pergunta():
    try:
        data = request.get_json()
        pergunta = data.get('pergunta', '').strip()
        
        if not pergunta:
            return jsonify({'erro': 'Pergunta não fornecida'}), 400
        
        # Buscar trechos relevantes
        trechos = buscar_pergunta_tfidf(pergunta, vectorizer, tfidf_matrix, artigos, top_k=3)
        
        if not trechos:
            return jsonify({
                'resposta': 'Não encontrei informações específicas sobre sua pergunta na Lei de Acesso à Informação. Pode reformular a pergunta?',
                'artigos_relacionados': []
            })
        
        # Construir prompt e gerar resposta
        prompt = construir_prompt(pergunta, trechos)
        resposta = gerar_resposta_llm(prompt)
        
        return jsonify({
            'resposta': resposta,
            'artigos_relacionados': [{'id': t['id'], 'texto': t['texto'][:150] + '...'} for t in trechos]
        })
        
    except Exception as e:
        return jsonify({'erro': f'Erro interno: {str(e)}'}), 500

@app.route('/api/status')
def status():
    return jsonify({
        'status': 'Sistema funcionando (versão otimizada)', 
        'artigos_carregados': len(artigos) if artigos else 0,
        'memoria': 'TF-IDF (baixo consumo)'
    })

if __name__ == '__main__':
    inicializar_sistema()
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port) 
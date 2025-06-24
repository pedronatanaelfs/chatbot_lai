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
    try:
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
    except FileNotFoundError:
        print(f"[ERRO] Arquivo {caminho_txt} não encontrado!")
        # Criar dados de exemplo para o sistema funcionar
        artigos = [
            {
                "id": "ARTIGO_1",
                "texto": "Esta Lei dispõe sobre o acesso a informações previsto no inciso XXXIII do art. 5º, no inciso II do § 3º do art. 37 e no § 2º do art. 216 da Constituição Federal; altera a Lei nº 8.112, de 11 de dezembro de 1990; revoga a Lei nº 11.111, de 5 de maio de 2005, e dispositivos da Lei nº 8.159, de 8 de janeiro de 1991; e dá outras providências."
            },
            {
                "id": "ARTIGO_10",
                "texto": "Qualquer interessado poderá apresentar pedido de acesso a informações aos órgãos e entidades referidos no art. 1º desta Lei, por qualquer meio legítimo, devendo o pedido conter a identificação do requerente e a especificação da informação requerida."
            },
            {
                "id": "ARTIGO_11",
                "texto": "O órgão ou entidade pública deverá autorizar ou conceder o acesso imediato à informação disponível. Não sendo possível conceder o acesso imediato, na forma disposta no caput, o órgão ou entidade que receber o pedido deverá, em prazo não superior a 20 (vinte) dias: I - comunicar a data, local e modo para se realizar a consulta, efetuar a reprodução ou obter a certidão; II - indicar as razões de fato ou de direito da recusa, total ou parcial, do acesso pretendido; ou III - comunicar que não possui a informação, indicar, se for do seu conhecimento, o órgão ou a entidade que a detém, ou, ainda, remeter o requerimento a esse órgão ou entidade, cientificando o interessado da remessa."
            }
        ]
        print(f"[*] Usando dados de exemplo com {len(artigos)} artigos")
    except Exception as e:
        print(f"[ERRO] Erro ao carregar artigos: {e}")
        artigos = []
    
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
    
    try:
        # Carregar artigos
        artigos = carregar_artigos("sentencas.txt")
        
        if not artigos:
            print("[ERRO] Nenhum artigo foi carregado!")
            return False
            
        textos = [a["texto"] for a in artigos]
        
        # Usar TF-IDF em vez de embeddings pesados
        vectorizer, tfidf_matrix = criar_index_tfidf(textos)
        
        # Forçar limpeza de memória
        gc.collect()
        
        print(f"[✓] Sistema inicializado com {len(artigos)} artigos!")
        return True
        
    except Exception as e:
        print(f"[ERRO] Falha na inicialização: {e}")
        # Definir valores padrão seguros
        artigos = []
        vectorizer = None
        tfidf_matrix = None
        return False

# === Rotas da API ===
@app.route('/')
def index_page():
    return render_template('index.html')

@app.route('/api/pergunta', methods=['POST'])
def processar_pergunta():
    try:
        # Verificar se o sistema foi inicializado corretamente
        if vectorizer is None or tfidf_matrix is None or not artigos:
            print("[*] Sistema não inicializado. Tentando inicializar...")
            sucesso = inicializar_sistema()
            if not sucesso or vectorizer is None:
                return jsonify({
                    'erro': 'Sistema não pôde ser inicializado. Verifique os logs do servidor.'
                }), 500
        
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
        'memoria': 'TF-IDF (baixo consumo)',
        'vectorizer_ok': vectorizer is not None,
        'tfidf_matrix_ok': tfidf_matrix is not None,
        'sistema_inicializado': all([artigos, vectorizer is not None, tfidf_matrix is not None])
    })

if __name__ == '__main__':
    inicializar_sistema()
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port) 
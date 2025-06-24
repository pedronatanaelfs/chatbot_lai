import os
import faiss
import requests
import pandas as pd
import tempfile
import whisper
from pydub import AudioSegment
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from sklearn.preprocessing import normalize

app = Flask(__name__)
CORS(app)

# === Configurar API ===
load_dotenv()
GROQ_API_KEY = os.getenv("LLAMA_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
LLM_MODEL = "llama3-70b-8192"

# Variáveis globais para o modelo
artigos = None
model = None
index = None
whisper_model = None

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

# === Gerar embeddings ===
def gerar_embeddings(textos, modelo_nome="paraphrase-multilingual-MiniLM-L12-v2"):
    print("[*] Carregando modelo de embeddings...")
    model = SentenceTransformer(modelo_nome)
    embeddings = model.encode(textos, show_progress_bar=True)
    embeddings = normalize(embeddings)
    return embeddings, model

# === Criar índice FAISS ===
def criar_index_faiss(embeddings):
    dim = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)
    index.add(embeddings)
    return index

# === Buscar trechos relevantes ===
def buscar_pergunta(pergunta, model, index, artigos, top_k=3):
    pergunta_embedding = model.encode([pergunta])
    pergunta_embedding = normalize(pergunta_embedding)
    distancias, indices = index.search(pergunta_embedding, top_k)
    resultados = [artigos[idx] for idx in indices[0]]
    return resultados

# === Construir prompt com contexto ===
def construir_prompt(pergunta, trechos):
    contexto = "\n\n".join([f"[{t['id']}]\n{t['texto']}" for t in trechos])
    prompt = f"""
Você é um assistente jurídico treinado na Lei de Acesso à Informação (LAI - Lei nº 12.527/2011).
Responda à pergunta do usuário de forma clara, objetiva e com base legal. Imagine que o usuário é um cidadão que não tem conhecimento jurídico e que está buscando informações sobre a LAI.

Contexto extraído da LAI:
{contexto}

Pergunta: {pergunta}
Resposta:"""
    return prompt.strip()

# === Chamada à API da Groq ===
def gerar_resposta_llm(prompt):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "model": LLM_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2
    }

    response = requests.post(GROQ_API_URL, headers=headers, json=body)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

# === Inicializar Whisper ===
def inicializar_whisper():
    global whisper_model
    try:
        print("[*] Carregando modelo Whisper...")
        # Usar modelo small para balance entre qualidade e velocidade
        whisper_model = whisper.load_model("small")
        print("[✓] Modelo Whisper carregado com sucesso!")
        return True
    except Exception as e:
        print(f"[ERRO] Falha ao carregar Whisper: {e}")
        whisper_model = None
        return False

# === Inicializar o sistema ===
def inicializar_sistema():
    global artigos, model, index
    print("[*] Inicializando sistema...")
    artigos = carregar_artigos("sentencas.txt")
    textos = [a["texto"] for a in artigos]
    embeddings, model = gerar_embeddings(textos)
    index = criar_index_faiss(embeddings)
    
    # Inicializar Whisper
    inicializar_whisper()
    
    print("[✓] Sistema inicializado com sucesso!")

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
        trechos = buscar_pergunta(pergunta, model, index, artigos, top_k=4)
        
        # Construir prompt e gerar resposta
        prompt = construir_prompt(pergunta, trechos)
        resposta = gerar_resposta_llm(prompt)
        
        return jsonify({
            'resposta': resposta,
            'artigos_relacionados': [{'id': t['id'], 'texto': t['texto'][:200] + '...'} for t in trechos]
        })
        
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@app.route('/api/transcrever', methods=['POST'])
def transcrever_audio():
    try:
        if whisper_model is None:
            return jsonify({'erro': 'Modelo Whisper não disponível'}), 500
        
        # Verificar se arquivo de áudio foi enviado
        if 'audio' not in request.files:
            return jsonify({'erro': 'Arquivo de áudio não encontrado'}), 400
        
        audio_file = request.files['audio']
        if audio_file.filename == '':
            return jsonify({'erro': 'Nenhum arquivo selecionado'}), 400
        
        # Salvar arquivo temporário
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
            audio_file.save(temp_file.name)
            temp_path = temp_file.name
        
        try:
            # Converter para formato suportado se necessário
            audio = AudioSegment.from_file(temp_path)
            audio = audio.set_channels(1).set_frame_rate(16000)  # Mono, 16kHz
            
            # Salvar áudio convertido
            converted_path = temp_path.replace('.wav', '_converted.wav')
            audio.export(converted_path, format='wav')
            
            # Transcrever com Whisper
            print("[*] Transcrevendo áudio...")
            result = whisper_model.transcribe(
                converted_path, 
                language='pt',  # Português
                fp16=False  # Para compatibilidade
            )
            
            transcricao = result['text'].strip()
            print(f"[✓] Transcrição: {transcricao}")
            
            return jsonify({
                'transcricao': transcricao,
                'confianca': result.get('confidence', 0.9),
                'idioma': result.get('language', 'pt')
            })
            
        finally:
            # Limpar arquivos temporários
            try:
                os.unlink(temp_path)
                if 'converted_path' in locals():
                    os.unlink(converted_path)
            except:
                pass
                
    except Exception as e:
        print(f"[ERRO] Erro na transcrição: {e}")
        return jsonify({'erro': f'Erro na transcrição: {str(e)}'}), 500

@app.route('/api/status')
def status():
    return jsonify({
        'status': 'Sistema funcionando', 
        'artigos_carregados': len(artigos) if artigos else 0,
        'whisper_disponivel': whisper_model is not None
    })

if __name__ == '__main__':
    inicializar_sistema()
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port) 
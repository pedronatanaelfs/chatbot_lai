# 🌿 Branches do Projeto - Chatbot LAI

Este repositório possui duas versões do chatbot, cada uma em sua própria branch:

## 📋 **Branches Disponíveis**

### 🚀 **Branch `main` - Versão Completa** (Atual)
Esta é a versão original com todos os recursos avançados.

**Características:**
- ✅ **SentenceTransformers**: Embeddings de alta qualidade
- ✅ **FAISS**: Busca vetorial rápida e precisa  
- ✅ **spaCy**: Processamento de linguagem natural completo
- ✅ **LLaMA 70B**: Modelo grande para respostas detalhadas
- ✅ **Performance máxima**: Melhor qualidade de respostas

**Requisitos:**
- 💾 **RAM**: ~1GB+ 
- 🖥️ **Ambiente**: Local ou servidores com mais recursos
- 💰 **Custo**: Planos pagos em hospedagens (Render $7+/mês)

**Como usar:**
```bash
git checkout main
pip install -r requirements.txt
python -m spacy download pt_core_news_lg
python app.py
```

---

### 🪶 **Branch `versao-otimizada` - Versão Leve**
Versão otimizada para hospedagens gratuitas com limitações de memória.

**Características:**
- ✅ **TF-IDF**: Busca textual eficiente
- ✅ **sklearn**: Bibliotecas leves
- ✅ **LLaMA 8B**: Modelo menor mas eficiente  
- ✅ **Gunicorn**: Servidor otimizado
- ✅ **Deploy gratuito**: Funciona no Render free

**Requisitos:**
- 💾 **RAM**: ~150-200MB
- 🖥️ **Ambiente**: Qualquer (incluindo gratuitos)
- 💰 **Custo**: Gratuito (Render, Railway, etc.)

**Como usar:**
```bash
git checkout versao-otimizada
pip install -r requirements.txt
python app.py
```

---

## 🎯 **Qual Versão Escolher?**

### Use a **Branch `main`** se:
- ✅ Tem servidor próprio ou plano pago
- ✅ Quer máxima qualidade nas respostas
- ✅ Performance é prioridade
- ✅ Está rodando localmente

### Use a **Branch `versao-otimizada`** se:
- ✅ Quer deploy gratuito (Render, Railway)
- ✅ Tem limitações de memória
- ✅ Prioriza baixo custo
- ✅ Performance moderada é suficiente

---

## 🔄 **Como Trocar de Branch**

### Para Versão Completa:
```bash
git checkout main
pip install -r requirements.txt
python -m spacy download pt_core_news_lg
python app.py
```

### Para Versão Otimizada:
```bash
git checkout versao-otimizada  
pip install -r requirements.txt
python app.py
```

---

## 🚀 **Deploy Recomendado por Branch**

| Branch | Plataforma Recomendada | Custo | RAM |
|--------|------------------------|-------|-----|
| `main` | Render Starter+ | $7/mês | 1GB |
| `main` | Railway Pro | $5/mês | 1GB |
| `main` | Servidor próprio | Varia | 2GB+ |
| `versao-otimizada` | **Render Free** | **Grátis** | 512MB |
| `versao-otimizada` | **Railway Hobby** | **Grátis** | 512MB |

---

## 📊 **Comparação de Performance**

| Métrica | Branch `main` | Branch `versao-otimizada` |
|---------|---------------|---------------------------|
| **Qualidade das Respostas** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Velocidade de Busca** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Uso de Memória** | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Facilidade de Deploy** | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Custo** | ⭐⭐ | ⭐⭐⭐⭐⭐ |

---

## 🔍 **Diferenças Técnicas**

### Algoritmo de Busca:
- **`main`**: SentenceTransformers + FAISS (embeddings semânticos)
- **`versao-otimizada`**: TF-IDF + Cosine Similarity (busca textual)

### Modelo LLM:
- **`main`**: LLaMA 70B (respostas mais elaboradas)
- **`versao-otimizada`**: LLaMA 8B (respostas concisas)

### Dependências:
- **`main`**: sentence-transformers, faiss-cpu, spacy, pandas
- **`versao-otimizada`**: scikit-learn, numpy (mínimas)

---

## 💡 **Dicas**

1. **Desenvolvimento**: Use `main` localmente para melhor experiência
2. **Produção gratuita**: Use `versao-otimizada` para deploy gratuito  
3. **Produção paga**: Use `main` para máxima qualidade
4. **Testes**: Ambas as versões mantêm a mesma interface

---

**Escolha a branch que melhor se adapta às suas necessidades e orçamento! 🚀** 
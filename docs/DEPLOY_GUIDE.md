# 🚀 Guia de Deploy Gratuito - Chatbot LAI

Este guia mostra como disponibilizar seu chatbot online gratuitamente em diferentes plataformas.

## 🌟 Render (Recomendado)

### Por que Render?
- ✅ **Totalmente gratuito** (750 horas/mês)
- ✅ **Deploy automático** via GitHub
- ✅ **HTTPS incluído**
- ✅ **Fácil configuração**
- ✅ **Suporte completo a Python**

### Passo a Passo

#### 1. Preparar o Repositório
```bash
# Se ainda não tem um repositório Git
git init
git add .
git commit -m "Initial commit"

# Criar repositório no GitHub e fazer push
git remote add origin https://github.com/seu-usuario/chatbot-lai.git
git push -u origin main
```

#### 2. Modificar app.py para Render
Altere a última linha do `app.py`:

```python
if __name__ == '__main__':
    inicializar_sistema()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
```

#### 3. Deploy no Render
1. Acesse: https://render.com
2. Crie uma conta gratuita
3. Clique em **"New +"** → **"Web Service"**
4. Conecte seu repositório GitHub
5. Configure:
   - **Name**: `chatbot-lai`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt && python -m spacy download pt_core_news_lg`
   - **Start Command**: `python app.py`
6. Em **Environment Variables**, adicione:
   - **Key**: `LLAMA_API_KEY`
   - **Value**: sua chave da API Groq
7. Clique em **"Create Web Service"**

#### 4. Resultado
- Seu chatbot estará online em: `https://chatbot-lai.onrender.com`
- Deploy automático a cada push no GitHub

---

## 🚂 Railway (Alternativa)

### Características
- ✅ **$5/mês em créditos gratuitos**
- ✅ **Deploy via GitHub**
- ✅ **Escalabilidade automática**

### Deploy
1. Acesse: https://railway.app
2. Conecte com GitHub
3. Selecione seu repositório
4. Adicione variável `LLAMA_API_KEY`
5. Deploy automático!

---

## ✈️ Fly.io (Para Usuários Avançados)

### Preparação
```bash
# Instalar Fly CLI
curl -L https://fly.io/install.sh | sh

# Login
fly auth login

# Inicializar
fly launch
```

### Configuração (fly.toml)
```toml
app = "chatbot-lai"

[build]
  builder = "paketobuildpacks/builder:base"

[env]
  PORT = "8080"

[[services]]
  http_checks = []
  internal_port = 8080
  processes = ["app"]
  protocol = "tcp"
  script_checks = []

  [[services.ports]]
    force_https = true
    handlers = ["http"]
    port = 80

  [[services.ports]]
    handlers = ["tls", "http"]
    port = 443
```

### Deploy
```bash
fly deploy
fly secrets set LLAMA_API_KEY=sua_chave_aqui
```

---

## 🐍 PythonAnywhere (Limitado)

### Características
- ✅ **Plano gratuito permanente**
- ❌ **Limitações de CPU**
- ❌ **Sem HTTPS no gratuito**
- ❌ **Pode ser lento para ML**

### Deploy
1. Acesse: https://pythonanywhere.com
2. Crie conta gratuita
3. Upload dos arquivos
4. Configure Web App
5. Instale dependências no console

**Nota**: PythonAnywhere gratuito pode ter problemas com modelos de ML pesados.

---

## ☁️ Google Cloud Platform (Créditos)

### Cloud Run (Recomendado para GCP)
```bash
# Criar Dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN python -m spacy download pt_core_news_lg

COPY . .

EXPOSE 8080
CMD ["python", "app.py"]
```

### Deploy
```bash
gcloud run deploy chatbot-lai \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

---

## 📋 Comparação das Plataformas

| Plataforma | Gratuidade | Facilidade | Performance | Recomendação |
|------------|------------|------------|-------------|--------------|
| **Render** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | **MELHOR** |
| Railway | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Boa |
| Fly.io | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Avançados |
| PythonAnywhere | ⭐⭐ | ⭐⭐⭐ | ⭐⭐ | Evitar |
| Google Cloud | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ | Temporário |

---

## 🎯 Recomendação Final

**Use o Render!** É a melhor combinação de:
- Totalmente gratuito
- Fácil de configurar
- Boa performance
- Deploy automático
- HTTPS incluído

### Próximos Passos
1. Modifique o `app.py` conforme mostrado
2. Faça push para o GitHub
3. Configure no Render
4. Compartilhe o link: `https://seu-app.onrender.com`

---

## 🚨 Importante

### Limitações Gratuitas
- **Render**: App "dorme" após 15min sem uso
- **Railway**: $5/mês em créditos (~750h)
- **Todos**: Recursos limitados de CPU/RAM

### Dicas de Otimização
- Use cache para embeddings
- Implemente rate limiting
- Monitore uso de recursos
- Configure logs para debug

### Monitoramento
- Render tem dashboard nativo
- Use logs para debugar problemas
- Configure alertas se necessário

**Seu chatbot estará online 24/7 gratuitamente! 🎉** 
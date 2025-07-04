# Interface Web - Chatbot Lei de Acesso à Informação

Este projeto agora inclui uma interface web moderna para interagir com o chatbot da Lei de Acesso à Informação (LAI).

## 🚀 Como Executar

### 1. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 2. Configurar Variável de Ambiente

Crie um arquivo `.env` na raiz do projeto com:

```
LLAMA_API_KEY=sua_chave_da_api_groq_aqui
```

**Como obter a chave da API:**
- Acesse: https://console.groq.com/
- Crie uma conta gratuita
- Gere uma chave de API
- Cole a chave no arquivo `.env`

### 3. Executar o Servidor

```bash
python app.py
```

### 4. Acessar a Interface

Abra seu navegador e vá para: `http://localhost:5000`

## 🖥️ Funcionalidades da Interface

### Interface Principal
- **Design Moderno**: Interface limpa e responsiva
- **Chat em Tempo Real**: Conversação fluida com o chatbot
- **Perguntas Sugeridas**: Botões com perguntas comuns sobre a LAI
- **Indicador de Carregamento**: Animação enquanto processa a resposta

### Recursos Interativos
- **Auto-resize**: Campo de texto se adapta ao conteúdo
- **Atalhos de Teclado**: Enter para enviar, Shift+Enter para nova linha
- **Artigos Relacionados**: Mostra quais artigos da lei foram consultados
- **Tratamento de Erros**: Mensagens claras em caso de erro

### Responsividade
- **Mobile-First**: Funciona perfeitamente em celulares
- **Desktop**: Interface otimizada para telas grandes
- **Adaptável**: Se ajusta a qualquer tamanho de tela

## 🏗️ Arquitetura

### Backend (Flask)
- **API REST**: Endpoints para processar perguntas
- **Busca Semântica**: Usa FAISS para encontrar artigos relevantes
- **LLM Integration**: Integração com Groq/LLaMA para gerar respostas
- **CORS Habilitado**: Permite requests de diferentes origens

### Frontend (HTML/CSS/JS)
- **Vanilla JavaScript**: Sem dependências externas
- **CSS3 Moderno**: Gradientes, animações e responsividade
- **Fetch API**: Comunicação assíncrona com o backend

## 📱 Exemplo de Uso

1. **Acesse** a interface no navegador
2. **Digite** uma pergunta como "Como solicitar informações públicas?"
3. **Aguarde** o processamento (indicado pela animação)
4. **Receba** a resposta baseada na Lei de Acesso à Informação
5. **Visualize** os artigos relacionados que foram consultados

## 🔧 Estrutura de Arquivos

```
chatbot_lai/
├── app.py                 # Servidor Flask principal
├── templates/
│   └── index.html        # Interface web
├── sentencas.txt         # Artigos da LAI processados
├── requirements.txt      # Dependências Python
└── INTERFACE_README.md   # Esta documentação
```

## 🎨 Personalização

### Cores e Tema
As cores podem ser alteradas no CSS do arquivo `templates/index.html`:
- **Primária**: `#667eea` (azul)
- **Secundária**: `#764ba2` (roxo)
- **Fundo**: Gradiente azul-roxo

### Perguntas Sugeridas
Modifique as sugestões no HTML, seção `suggestions`:
```html
<div class="suggestion" onclick="enviarPerguntaSugerida('Sua pergunta aqui')">
    Texto do botão
</div>
```

## 🔍 Endpoints da API

### `GET /`
Carrega a interface principal

### `POST /api/pergunta`
Processa uma pergunta do usuário

**Request:**
```json
{
  "pergunta": "Como solicitar informações públicas?"
}
```

**Response:**
```json
{
  "resposta": "Para solicitar informações públicas...",
  "artigos_relacionados": [
    {
      "id": "ARTIGO_10",
      "texto": "Qualquer interessado poderá apresentar pedido..."
    }
  ]
}
```

### `GET /api/status`
Verifica o status do sistema

**Response:**
```json
{
  "status": "Sistema funcionando",
  "artigos_carregados": 47
}
```

## 🐛 Solução de Problemas

### Erro de API Key
- Verifique se o arquivo `.env` existe
- Confirme se a chave está correta
- Teste a chave no console Groq

### Erro de Arquivo Não Encontrado
- Certifique-se que `sentencas.txt` existe na raiz
- Execute os scripts de preprocessamento se necessário

### Interface Não Carrega
- Verifique se `templates/index.html` existe
- Confirme se Flask está instalado
- Teste acessar `http://127.0.0.1:5000` em vez de localhost

---

**Desenvolvido com ❤️ para facilitar o acesso à informação pública no Brasil** 
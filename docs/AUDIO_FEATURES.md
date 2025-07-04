# Funcionalidades de Áudio - Chatbot LAI

O projeto implementa duas versões do chatbot com funcionalidades de áudio para entrada por voz.

## **Versões Disponíveis**

### **Versão Econômica** (Branch: `versao-otimizada`)
**Implementada para deploy em serviços como Render**

#### **Tecnologias:**
- Web Speech API (nativa do navegador)
- Transcrição em tempo real
- Sem dependências de servidor para reconhecimento de voz

#### **Funcionalidades:**
- **Botão de microfone** com animação
- **Indicador visual** durante gravação  
- **Interface responsiva** para mobile
- **Tratamento de erros** para falhas de reconhecimento

#### **Compatibilidade:**
- Chrome/Chromium
- Edge  
- Safari (limitado)
- Firefox (não suportado)

---

### **Versão Local Avançada** (Branch: `main`)
**Implementada para uso local ou em servidores com mais recursos**

#### **Tecnologias:**
- OpenAI Whisper (modelo "small")
- Web Speech API (fallback)
- Upload de áudio para processamento no servidor
- Pydub para conversão de formatos

#### **Funcionalidades:**
- **Reconhecimento tempo real** (Web Speech API)
- **Gravação e upload** (Whisper)
- **Dois botões especializados**:
  - Botão vermelho: Reconhecimento instantâneo
  - Botão azul: Gravação para Whisper
- **Indicador de confiança** da transcrição
- **Fallback automático** entre tecnologias
- **Suporte múltiplos formatos** (WAV, MP3, etc.)

---

## **Comparação Técnica**

| Aspecto | Versão Econômica | Versão Local Avançada |
|---------|------------------|----------------------|
| **Dependências** | Nenhuma adicional | whisper, soundfile, pydub |
| **Implementação** | Frontend (JavaScript) | Frontend + Backend |
| **Compatibilidade** | Depende do browser | Universal via upload |
| **Offline** | Requer internet | Funciona offline após baixar modelo |
| **Recursos** | Leve | Requer mais recursos para Whisper |

---

## **Como Usar**

### Versão Econômica:
```bash
git checkout versao-otimizada
python app.py
# Acesse http://localhost:5000
# Clique no microfone vermelho para falar
```

### Versão Local Avançada:
```bash
git checkout main
pip install openai-whisper soundfile pydub
python app.py
# Acesse http://localhost:5000
# Botão vermelho: fala instantânea
# Botão azul: grava e processa com Whisper
```

---

## **Interface de Usuário**

### Versão Econômica:
- 1 botão de microfone (vermelho)
- Status textual simples
- Design minimalista

### Versão Local Avançada:
- Botão Speech (reconhecimento tempo real)
- Botão Record (gravação para Whisper)
- Status avançado com indicadores
- Badge "Versão Avançada"
- Layout responsivo otimizado

---

## **Requisitos Técnicos**

### Versão Econômica:
```
Navegador: Chrome/Edge/Safari
Internet: Necessária para Speech API
```

### Versão Local Avançada:
```
Dependências: whisper, soundfile, pydub
Storage: ~400MB (modelo Whisper)
```

---

## **Exemplos de Uso**

### Perguntas que podem ser feitas por voz:
- "Como apresentar pedido de acesso a informações?"
- "Qual o prazo para resposta do pedido?"
- "Quais informações podem ser negadas?"
- "Quem pode solicitar informações públicas?"

### Dicas para melhor reconhecimento:
- Fale claramente e pausadamente
- Minimize ruído de fundo
- Use microfone de qualidade quando possível
- Teste ambos os botões na versão avançada

---

## **Resultado Final**

Ambas as versões transformam o chatbot em uma interface conversacional, permitindo que os usuários façam perguntas por voz sobre a Lei de Acesso à Informação. 
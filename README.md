# LAI Chatbot - Assistente Virtual da Lei de Acesso à Informação

Um chatbot especializado na Lei de Acesso à Informação (Lei nº 12.527/2011), desenvolvido como projeto de pesquisa para o Mestrado em Ciência da Computação.

## Estrutura do Projeto

```
chatbot_lai/
  - app.py                  # Aplicação principal do chatbot
  - data/                   # Diretório de dados
    - raw/                  # Dados brutos
    - processed/            # Dados processados
    - metrics/              # Métricas de avaliação
  - docs/                   # Documentação
  - notebooks/              # Jupyter notebooks de exploração e avaliação
  - scripts/                # Scripts de processamento
  - templates/              # Templates HTML para a interface web
  - requirements.txt        # Dependências do projeto
```

## Pipeline de Processamento

1. **Coleta e Limpeza**: Extração do texto da Lei de Acesso à Informação do site oficial do Planalto.
2. **Normalização**: Padronização do texto para processamento.
3. **Processamento com SpaCy**: Tokenização, POS tagging e reconhecimento de entidades.
4. **Pós-processamento NER**: Filtragem e correção de entidades nomeadas.
5. **Busca Semântica**: Indexação vetorial do texto para recuperação por similaridade.
6. **Geração de Respostas**: Uso de LLMs para gerar respostas contextualizadas.

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/chatbot_lai.git
cd chatbot_lai
```

2. Crie um ambiente virtual e instale as dependências:
```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Baixe o modelo do SpaCy:
```bash
python -m spacy download pt_core_news_lg
```

4. Configure as variáveis de ambiente:
```bash
# Crie um arquivo .env na raiz do projeto
echo "LLAMA_API_KEY=sua_chave_api" > .env
```

## Uso

### Executando o Pipeline de Processamento

Execute os scripts na ordem numérica:

```bash
python scripts/1_coleta_e_limpeza.py
python scripts/2_limpeza_normalizacao.py
python scripts/3_preprocess_spacy.py
python scripts/4_pos_processamento_ner.py
```

### Iniciando o Chatbot

```bash
python app.py
```

Acesse o chatbot em `http://localhost:5000` no seu navegador.

## Avaliação

Os notebooks de avaliação estão disponíveis no diretório `notebooks/avaliacao/`:

- `avaliacao_completa.ipynb`: Avaliação da versão completa do sistema
- `avaliacao_otimizada.ipynb`: Avaliação da versão otimizada
- `avaliacao_comparativa.ipynb`: Comparação entre versões

## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo LICENSE para detalhes.

---

## Visão Geral

O fluxo completo do projeto envolve:

1. **Coleta e limpeza** do texto original da lei.  
2. **Pré-processamento** (tokenização, remoção de stopwords, lematização etc.) usando spaCy.  
3. **Indexação** do texto (BM25, TF-IDF ou embeddings) para encontrar os trechos relevantes.  
4. **Aplicação do modelo BERTimbau** em uma tarefa de *Question Answering* (QA) para obter a resposta exata.  
5. **Construção de uma API** e/ou interface de chatbot para disponibilizar as respostas ao usuário.

Este repositório contém o primeiro passo: **coleta e limpeza do texto**.

---

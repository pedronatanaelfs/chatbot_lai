# Projeto: Chatbot - Lei de Acesso à Informação

Este projeto tem como objetivo criar um chatbot capaz de interpretar a Lei de Acesso à Informação (Lei nº 12.527/2011) e responder perguntas de forma precisa, utilizando processamento de linguagem natural (NLP) em Python.

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

## Requisitos

Para executar este projeto em um ambiente Anaconda, crie ou ative um *environment* e instale as dependências a partir de `requirements.txt`. Por exemplo:

```bash
conda create -n chatbotLAI python=3.9
conda activate chatbotLAI
pip install -r requirements.txt
python -m spacy download pt_core_news_lg

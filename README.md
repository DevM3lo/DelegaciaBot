# 🇧🇷 Projeto Delegacia 5.0: Chatbot Humanizado para PCPE

## 🎯 Visão Geral do Projeto

Este projeto consiste no desenvolvimento e implementação de um **Assistente Virtual Híbrido** para a Polícia Civil de Pernambuco (PCPE). O objetivo é modernizar o atendimento, fornecendo informações instantâneas sobre serviços, legislação e procedimentos, reduzindo a sobrecarga nas delegacias presenciais.

O sistema atende integralmente ao requisito de **Conformidade com a LGPD** e à preferência por **Tecnologias Open Source** (Ollama/FAISS) em conjunto com uma solução **Cloud-Native** (Gemini API) para garantir estabilidade e alta performance.

## ⚙️ Arquitetura do Sistema (Hybrid RAG)

O projeto utiliza uma arquitetura de Geração Aumentada por Recuperação (RAG) para garantir que as respostas sobre leis e procedimentos sejam factuais e baseadas **apenas** na base de conhecimento oficial (os arquivos `.txt` na pasta `docs`).

| Componente | Função | Tecnologia Específica |
| :--- | :--- | :--- |
| **Orquestração** | Gerencia o fluxo de conversa e a conexão com canais externos (Telegram/WhatsApp). | **n8n** (Docker) |
| **Cérebro (LLM)** | Gera a resposta final, com alta velocidade e inteligência. | **Google Gemini 2.0 Flash** (API Cloud) |
| **Memória (Vector DB)** | Armazena a Lei 7550/77 e os procedimentos em formato vetorial. | **FAISS** (índice) |
| **Embeddings** | Transforma texto em vetores para busca semântica. | **Ollama** (`nomic-embed-text` local) |

## ✅ Requisitos de Execução

Para rodar o projeto em um novo ambiente, é necessário ter instalado e configurado:

1.  **Python 3.11** (com ambiente virtual `venv` ativado).
2.  **Docker Desktop** (para rodar o n8n de forma isolada).
3.  **Ollama CLI** (para gerenciar os modelos de embeddings locais).
4.  **ngrok** (para criar o túnel HTTPS público para o Telegram).
5.  **Chave Gemini API** (Definida como variável de ambiente `GEMINI_API_KEY`).
6.  **Token do Bot do Telegram** (Obtido via @BotFather).

## 🚀 Guia de Setup e Execução (Passo a Passo)

Siga este guia em 4 passos. Certifique-se de estar na pasta raiz do projeto com o `venv` ativado.

### 1. Preparação da Base de Conhecimento e Variáveis

1.  **Defina sua Chave Gemini:**
    ```bash
    $env:GEMINI_API_KEY="SUA_CHAVE_AQUI"
    ```
2.  **Instale as Dependências:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Baixe os Modelos Ollama (Embeddings):**
    ```bash
    ollama pull nomic-embed-text
    ```
4.  **Limpe o Cache:** Garanta que a base vetorial seja recriada com os arquivos `.txt` novos.
    ```bash
    rm -rf faiss_index
    ```

### 2. Inicie a API Python (O Cérebro)

Mantenha esta janela do terminal rodando o tempo todo. Ele irá ler os arquivos `.txt` e criar a memória FAISS:
```bash
uvicorn api:app --reload
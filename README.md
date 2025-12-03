# 👮 Delegacia 5.0 - Assistente Virtual Inteligente (PCPE)

> **Projeto Acadêmico - Categoria B: Sistema de Chatbot e Triagem de Atendimento**

[![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Gemini AI](https://img.shields.io/badge/AI-Google%20Gemini%202.0-orange?style=for-the-badge&logo=google)](https://ai.google.dev/)
[![Status](https://img.shields.io/badge/Status-Online%2024%2F7-brightgreen?style=for-the-badge)]()

---

## 🎯 Visão Geral

O **Delegacia 5.0** é um chatbot de atendimento ao cidadão desenvolvido para a **Polícia Civil de Pernambuco (PCPE)**. O sistema utiliza Inteligência Artificial Generativa (LLM) com a técnica **RAG (Retrieval-Augmented Generation)** para fornecer informações precisas, contextuais e jurídicas sobre serviços policiais, sem alucinações.

O objetivo é reduzir filas presenciais e oferecer triagem imediata para serviços como Registro de B.O., taxas de licenciamento e denúncias anônimas.

### 🔗 Teste Agora (Live Demo)
Acesse o bot diretamente no Telegram:
👉 **[t.me/DelegaciaAdmin_bot](https://t.me/DelegaciaAdmin_bot)**

---

## ⚙️ Arquitetura Técnica

O projeto foi migrado de uma solução local para uma arquitetura **Serverless/Cloud** para garantir disponibilidade 24/7.

| Componente | Tecnologia | Função |
| :--- | :--- | :--- |
| **Backend API** | **Python (FastAPI)** | Gerencia webhooks, lógica de negócios e conexão com IA. |
| **Inteligência** | **Google Gemini 2.0 Flash** | Processamento de Linguagem Natural (NLP) de alta velocidade. |
| **Memória (RAG)** | **FAISS + LangChain** | Banco de dados vetorial local para indexar leis e procedimentos. |
| **Embeddings** | **Google GenAI Embeddings** | Vetorização de alta performance na nuvem. |
| **Interface** | **Telegram Bot API** | Interface de usuário acessível e mobile-first. |
| **Hospedagem** | **Render (Cloud)** | Deploy contínuo via GitHub com monitoramento de uptime. |

---

## 📚 Base de Conhecimento (Escopo de Atendimento)

O robô foi treinado com documentos oficiais (localizados na pasta `/docs`) para responder sobre:

* 📜 **Legislação:** Tabela de taxas e licenciamento (Lei 7550/77).
* 🚨 **Procedimentos:** Diferença legal entre Furto e Roubo; orientações para B.O. Online.
* 📍 **Localização:** Endereços e contatos de delegacias especializadas (Mulher, Turista, DHPP).
* 🛡️ **Prevenção:** Dicas de segurança pública e alertas contra golpes digitais.
* ⭐ **Feedback:** Sistema de avaliação de atendimento integrado.

---

## 🚀 Como Rodar Localmente (Desenvolvimento)

Para clonar e executar este projeto em sua máquina:

### 1. Pré-requisitos
* Python 3.11+
* Conta no Google AI Studio (API Key)
* Token de Bot do Telegram (@BotFather)

### 2. Instalação
```bash
# Clone o repositório
git clone https://github.com/DevM3lo/DelegaciaBot.git
cd DelegaciaBot

# Crie e ative o ambiente virtual
python -m venv venv
.\venv\Scripts\activate  # Windows

# Instale as dependências
pip install -r requirements.txt

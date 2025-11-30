from fastapi import FastAPI, Request, HTTPException
import os
import requests
import json

# --- IMPORTAÇÕES DO CÉREBRO ---
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import DirectoryLoader, TextLoader, PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate

# --- CONFIGURAÇÕES ---
# Pega as chaves do ambiente (Render)
os.environ["GOOGLE_API_KEY"] = os.environ.get("GEMINI_API_KEY")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN") # Nova variável necessária!

app = FastAPI(title="Bot Delegacia 5.0 - Telegram Edition", version="Final")
PASTA_DOCS = "docs"
PASTA_DB = "faiss_index"

vector_store = None
llm = None

# --- INICIALIZAÇÃO (Igual ao anterior) ---
@app.on_event("startup")
def startup_event():
    global vector_store, llm
    print(">>> Inicializando Cérebro 24/7...")
    
    # 1. Configura Gemini (Chat)
    try:
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash", 
            temperature=0.2,
            convert_system_message_to_human=True
        )
    except:
        print("Erro ao conectar Gemini Chat")

    # 2. Configura Embeddings (Google)
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/text-embedding-004", 
        api_key=os.environ.get("GOOGLE_API_KEY")
    )

    # 3. Carrega Memória
    if os.path.exists(PASTA_DOCS):
        print(">>> Indexando documentos...")
        docs = []
        try:
            loader = DirectoryLoader(PASTA_DOCS, glob="*.txt", loader_cls=TextLoader, loader_kwargs={'encoding': 'utf-8'})
            docs.extend(loader.load_and_split())
        except: pass
        
        if docs:
            vector_store = FAISS.from_documents(docs, embeddings)
            print(f">>> Memória carregada com {len(docs)} trechos!")
        else:
            print(">>> AVISO: Nenhum documento lido.")

# --- LÓGICA DE RAG (Função auxiliar) ---
def gerar_resposta_rag(pergunta_usuario):
    if not vector_store:
        return "Desculpe, meu sistema está reiniciando. Tente em 1 minuto."
    
    docs = vector_store.similarity_search(pergunta_usuario, k=4)
    contexto = "\n\n".join([d.page_content for d in docs])
    
    template = """
    Você é o Agente Virtual da Polícia Civil de Pernambuco (Delegacia 5.0).
    Responda com base APENAS no contexto abaixo. Seja formal e cite valores/leis.
    
    CONTEXTO: {contexto}
    PERGUNTA: {pergunta}
    RESPOSTA:"""
    
    prompt = template.format(contexto=contexto, pergunta=pergunta_usuario)
    try:
        res = llm.invoke(prompt)
        return res.content
    except:
        return "Erro temporário na IA. Tente novamente."

# --- ENDPOINT DO TELEGRAM (Onde a mágica acontece) ---
@app.post("/webhook/telegram")
async def telegram_webhook(request: Request):
    # 1. Lê o pacotão do Telegram
    data = await request.json()
    
    try:
        # 2. Extrai quem mandou e o que mandou
        message = data.get("message", {})
        chat_id = message.get("chat", {}).get("id")
        texto_usuario = message.get("text", "")

        if not chat_id or not texto_usuario:
            return {"status": "ignored"} # Não foi mensagem de texto

        print(f"Mensagem recebida de {chat_id}: {texto_usuario}")

        # 3. Lógica de Comandos (/start) vs Pergunta
        if texto_usuario == "/start":
            resposta_final = """Bem-vindo à Delegacia Virtual 5.0 da PCPE.
            
Sou um assistente oficial automatizado. Posso informar sobre:
1. Taxas e Licenciamento (Lei 7550/77)
2. Como registrar Boletim de Ocorrência
3. Endereços de Delegacias
4. Dicas de Segurança

Digite sua dúvida abaixo:"""
        else:
            # Chama a IA
            resposta_final = gerar_resposta_rag(texto_usuario)

        # 4. Envia a resposta de volta para o Telegram
        url_envio = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": resposta_final,
            "parse_mode": "Markdown"
        }
        requests.post(url_envio, json=payload)

    except Exception as e:
        print(f"Erro no processamento: {e}")

    return {"status": "ok"}

@app.get("/")
def health_check():
    return {"status": "Estou vivo e rodando 24/7!", "servico": "Delegacia Bot"}
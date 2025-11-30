from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os

# --- IMPORTAÇÕES CORRETAS ---
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import DirectoryLoader, TextLoader, PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate

# --- SUA CHAVE AQUI ---
# Cole sua chave dentro das aspas abaixo:
os.environ["GOOGLE_API_KEY"] = os.environ.get("GOOGLE_API_KEY")

app = FastAPI(title="API Delegacia 5.0", version="Final")
PASTA_DOCS = "docs"
PASTA_DB = "faiss_index"

class PerguntaRequest(BaseModel):
    texto: str

vector_store = None
llm = None

@app.on_event("startup")
def startup_event():
    global vector_store, llm
    print(">>> Inicializando Cérebro (Modo Nuvem)...")
    
    # --- CONFIGURAÇÃO DO MODELO (O ESCOLHIDO DA LISTA) ---
    # Usando o gemini-2.0-flash que apareceu na sua lista
    try:
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash", 
            temperature=0.2,
            convert_system_message_to_human=True
        )
        print(">>> Modelo Gemini 2.0 Flash conectado!")
    except Exception as e:
        print(f"Erro ao conectar no Google: {e}")

    # --- CONFIGURAÇÃO DA MEMÓRIA (OLLAMA LOCAL) ---
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/text-embedding-004", # Incluindo o prefixo exigido
        api_key=os.environ.get("GOOGLE_API_KEY")
    )
    
    # Carrega banco de dados
    if os.path.exists(PASTA_DB) and os.path.exists(f"{PASTA_DB}/index.faiss"):
        print(">>> Carregando memória do disco...")
        vector_store = FAISS.load_local(PASTA_DB, embeddings, allow_dangerous_deserialization=True)
    
    elif os.path.exists(PASTA_DOCS) and os.listdir(PASTA_DOCS):
        print(">>> Indexando arquivos da pasta 'docs'...")
        docs = []
        # Lê TXT
        try:
            loader_txt = DirectoryLoader(PASTA_DOCS, glob="*.txt", loader_cls=TextLoader, loader_kwargs={'encoding': 'utf-8'})
            docs.extend(loader_txt.load_and_split())
        except: pass
        
        # Lê PDF
        try:
            loader_pdf = DirectoryLoader(PASTA_DOCS, glob="*.pdf", loader_cls=PyPDFLoader)
            docs.extend(loader_pdf.load_and_split())
        except: pass

        if docs:
            vector_store = FAISS.from_documents(docs, embeddings)
            vector_store.save_local(PASTA_DB)
            print(f">>> Indexação concluída com {len(docs)} trechos!")
        else:
            print(">>> AVISO: Pasta 'docs' vazia.")

@app.post("/perguntar")
async def perguntar(request: PerguntaRequest):
    if not vector_store:
        raise HTTPException(status_code=503, detail="Base de dados não carregada.")
    
    # 1. Busca na memória local
    docs = vector_store.similarity_search(request.texto, k=4)
    contexto = "\n\n".join([d.page_content for d in docs])
    
    # 2. Prepara o Prompt
    template = """
    Você é o Agente Virtual da Polícia Civil de Pernambuco (Delegacia 5.0).
    Sua única função é fornecer informações oficiais, sem dar opiniões.

    REGRAS DE RESPOSTA:
    1. Seja extremamente conciso, formal e direto.
    2. Responda apenas com base no CONTEXTO OFICIAL.
    3. Para perguntas sobre valores/taxas, cite o código e o valor.
    4. Para perguntas sobre crime, priorize a orientação de segurança (não reagir) e o procedimento (presencial/online).
    
    CONTEXTO OFICIAL:
    {contexto}
    
    PERGUNTA DO CIDADÃO:
    {pergunta}
    
    RESPOSTA:"""
    
    prompt_final = template.format(contexto=contexto, pergunta=request.texto)
    
    # 3. Pergunta para o Google
    try:
        print(f"Processando: {request.texto}")
        resposta = llm.invoke(prompt_final)
        return {"resposta": resposta.content}
    except Exception as e:
        return {"resposta": "Erro na comunicação com a IA.", "erro_tecnico": str(e)}
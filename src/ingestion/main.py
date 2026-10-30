#libs e imports
print("importando libs")

import os
from pathlib import Path
import sys
from dotenv import load_dotenv
import time

from google import genai #modelo
from google.genai.types import types #configurações system_intructions, temperature.
from google.genai.errors import APIError # para tratar erros
from langchain_community.document_loaders import PyPDFLoader #Loder para ler os PDFs.
from langchain_text_splitters import RecursiveCharacterTextSplitter #Dividir os PDFs em chuncks menores.
from langchain_community.vectorstores import FAISS #Armazenar os embeddings em um banco de dados vetorial.
from langchain_core.prompts import ChatPromptTemplate #Conversar com o documento
from langchain_core.output_parsers import SimpleJsonOutputParser #Output parseado

print("libs importadas")

#Configuração de Paths e modelo
print("Paths e modelo iniciado")

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
CLIENT = genai.Client(api_key=API_KEY)
EMBEDDING_MODEL = "gemini-embedding-001"

project_root = Path("..").resolve()
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

from src.ingestion.candidates import CANDIDATOS_MAP #Importa o mapeamento de candidatos

'''modelo = CLIENT.models.generate_content(
    model="gemini-3.8-flash",
    contents="batch"
)'''
print("Paths e modelo finalizado")

#----------------------Leitura os pdfs no  com Loader ----------------------
#---------------------------------------------------------------------------
def carregar_e_enriquecer_pdf(pdf_path: Path, candidatos_map: dict) -> list:
    file_id = pdf_path.stem # cria id para  arquivo removendo o .pdf

    #map de metadados
    info_candidato = CANDIDATOS_MAP.get(file_id, { 
        "nome_candidato": f"CandidatoNotFound{file_id}",
        "nome_vice": "N/A",
        "nome_partido": "N/A",
        "sigla_partido": "N/A"
    })

    docs = PyPDFLoader(str(pdf_path)).load() #loader instanciado e loaded

    #injetar meta dados
    for doc in docs:
        doc.metadata.update({
            "nome_candidato": info_candidato["nome_candidato"],
            "nome_vice": info_candidato["nome_vice"],
            "nome_partido": info_candidato["nome_partido"],
            "sigla_partido": info_candidato["sigla_partido"],
            "arquivo_origem": pdf_path.name
        })

    return docs

print("inicia leitura de pdf")
data_dir = Path("../data/documentos_2026") 
pdf_files = list(data_dir.glob("*.pdf"))
all_documents = []

for pdf in pdf_files:
    all_documents.extend(carregar_e_enriquecer_pdf(pdf, CANDIDATOS_MAP))

print(f"Total de {len(all_documents)} páginas em {len(pdf_files)} arquivos")

#-----------------------divide em chuncks com o splitter------------------
#-------------------------------------------------------------------------
print("inicia divisão de chunks")
chunks = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=150,
    add_start_index=True
).split_documents(all_documents)
print(f"Total de {len(chunks)} chunks")

#--------------------Tranformar chunks em Embeddings-----------------------
#--------------------------------------------------------------------------
print("inicia transformação em embeddings")
#1. Extrair lista de textos dos chunks
textos = [doc.page_content for doc in chunks] 

#2. Gera vetores com API do Gemini em lotes de 100
batch_size=100
all_embeddings= []

for i in range(0, len(textos), batch_size):
    batch = textos[i:i + batch_size]
    response = CLIENT.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=batch
    )
    # Extrai os vetores retornados no lote
    for e in response.embeddings:
        all_embeddings.append(e.values)
    
    print(f" -> Processados {len(all_embeddings)}/{len(textos)} chunks...")

    if len(all_embeddings) < len(textos): #pausa para não atingir erro 429
        time.sleep(60)

print(f"\nTotal de {len(all_embeddings)} vetores gerados com sucesso!")

#---------------------Criar o FAISS a partir das listas de texto-----------------------
#--------------------------------------------------------------------------------------
print("inicia criação de FAISS")
textos_embeddings = list(zip(textos, all_embeddings))
metadatas = [doc.metadata for doc in chunks]

vectorstore = FAISS.from_embeddings(
    text_embeddings=textos_embeddings,
    embedding=None,  # vetores já gerados, não reprocessa
    metadatas=metadatas
)

#4. Salvar indice no disco para pesistencia fisica e não precisar gastar API novamente
faiss_index_path = Path("../data/02_faiss_index")
vectorstore.save_local(str(faiss_index_path))

print(f"Índice FAISS salvo com sucesso em: {faiss_index_path.resolve()}")

#-----------------------Retriver e Resposta do modelo-------------------
#------------------------------------------------------------------------
#1. Prompt de Input por parte do usuário
print("Prompt de Input por parte do usuário")
pergunta = input("\nDigite a pergunta comparativa (ex: Quais as propostas para saúde e como farão?): ")
'''if not pergunta.strip():
    pergunta = "Quais são as principais propostas dos candidatos para a saúde e como eles abordam que isso será feito?"
    print(f"⚠️ Nenhuma pergunta digitada. Usando padrão: '{pergunta}'")'''

#2. Transformar o prompt em vetor
print("Transformando o prompt em vetor")
query_response = CLIENT.models.embed_content(
    model=EMBEDDING_MODEL,
    contents=pergunta
)
query_vector = query_response.embeddings[0].values

#3. recuperar vetores no nosso banco vetorial FAISS k=8
print("Recuperando vetores no banco vetorial FAISS")
documentos_recuperados = vectorstore.similarity_search_by_vector(query_vector, k=8)

#4. Montar contexto estruturado com retorno de metadados
print("Montando contexto estruturado com retorno de metadados")
contexto_formatado = ""
for i, doc in enumerate(documentos_recuperados):
    candidato = doc.metadata.get("nome_candidato", "N/A")
    partido = doc.metadata.get("sigla_partido", "N/A")
    pagina = doc.metadata.get("page", "N/A")

    contexto_formatado += f"\n--- [TRECHO {i+1}] ---\n"
    contexto_formatado += f"CANDIDATO: {candidato} ({partido}) | PÁGINA: {pagina}\n"
    contexto_formatado += f"CONTEÚDO:\n{doc.page_content}\n"

#5. Prompt especializado PACE em análise comparativa com system_instruction e o prompt_final
print("Montando prompt especializado em análise comparativa com system_instruction e o prompt_final")
system_instruction = """Você é um analista político sênior e imparcial especialista nos Planos de Governo de 2026.
Sua missão é realizar uma ANÁLISE COMPARATIVA estrita sobre as propostas dos candidatos informados no contexto.

REGRAS DE RESPOSTA:
1. Responda APENAS com base no contexto fornecido. Não invente ou adicione informações externas.
2. Para CADA candidato identificado no contexto:
   - **Propostas Principais (O Quê):** Liste os alvos e metas propostas.
   - **Mecanismos de Execução (Como):** Explique exatamente como o candidato afirma que fará isso (ex: orçamentário, PPPs, novas leis, tecnologia, etc.).
   - **Citação das Páginas:** Indique a página de origem de cada ponto [Pág. X].
3. Adicione uma seção final com uma **Tabela Comparativa em Markdown** resumindo as abordagens de cada candidato lado a lado.
4. Caso algum candidato presente no contexto não aborde o tema consultado, mencione expressamente.
5. Se o contexto não trouxer nenhuma informação sobre o tema para nenhum candidato, responda apenas: 'Não foram encontradas propostas sobre este tema nos documentos analisados.'"""

prompt_final = f"""CONTEXTO RECUPERADO DOS PLANOS DE GOVERNO:
{contexto_formatado}

PERGUNTA DO USUÁRIO:
{pergunta}"""

#6. Gerar resposta comparativa como o modelo
print("Gerando resposta comparativa como o modelo")
resposta = CLIENT.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt_final,
    config=types.GenerateContentConfig(
        system_instruction=system_instruction,
        temperature=0.1 #Rigor analítico com baixa alucinação
    )
)

print("\n" + "=" * 60)
print("📊 RESPOSTA ANALÍTICA E COMPARATIVA")
print("=" * 60 + "\n")
print(resposta.text)



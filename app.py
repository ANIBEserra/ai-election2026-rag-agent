import streamlit as st
from pathlib import Path
from dotenv import load_dotenv
from src.rag.engine import RAGEngine

load_dotenv()

st.set_page_config(page_title="RAG Planos de Governo 2026", page_icon="🏛️", layout="wide")

st.title("🏛️ Análise Comparativa de Planos de Governo (2026)")
st.markdown("Faça perguntas e obtenha análises críticas, quantitativas e comparativas baseadas nos documentos oficiais.")

@st.cache_resource
def load_engine():
    faiss_path = Path("data/02_faiss_index")
    return RAGEngine(faiss_path=faiss_path)

try:
    engine = load_engine()
    st.success("Base vetorial FAISS carregada com sucesso!")
except Exception as e:
    st.error(f"Erro ao carregar o índice FAISS: {e}")
    st.stop()

pergunta_usuario = st.text_input(
    "Digite sua pergunta comparativa:",
    placeholder="Ex: Quais as propostas para a saúde e como pretendem financiá-la?"
)

if st.button("Gerar Análise Comparativa", type="primary"):
    if not pergunta_usuario.strip():
        st.warning("Por favor, digite uma pergunta.")
    else:
        with st.spinner("🔍 Consultando vetores e gerando análise crítica com o Gemini..."):
            try:
                resposta = engine.analisar_propostas(pergunta_usuario)
                st.markdown("---")
                st.markdown(resposta)
            except Exception as e:
                st.error(f"Erro ao processar a pergunta: {e}")
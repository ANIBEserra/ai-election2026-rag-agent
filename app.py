from pathlib import Path
import streamlit as st
from dotenv import load_dotenv

from src.rag.engine import RAGEngine
from src.frontend.components import (
    load_css, 
    render_hero_welcome, 
    render_prompt_grid, 
    render_comparison_cards
)

load_dotenv()

st.set_page_config(page_title="Workspace - Eleições 2026", page_icon="🏛️", layout="wide")

# Inicializa a variável do Tema no Session State
if "app_theme" not in st.session_state:
    st.session_state.app_theme = "light-mode"

load_css()

@st.cache_resource
def load_engine():
    return RAGEngine(faiss_path=Path("data/02_faiss_index"))

try:
    engine = load_engine()
except Exception as e:
    st.error(f"Erro ao carregar o motor RAG: {e}")
    st.stop()

    
# --- 2. CABEÇALHO ---
col_head1, col_head2 = st.columns([7,3])
with col_head1:
    st.markdown("<span style='font-weight: 700; font-size: 1.1rem;'>Assistente Eleições 2026</span> <span style='background: #E2E8F0; padding: 2px 8px; border-radius: 6px; font-size: 0.75rem; color: #475569;'>Pro</span>", unsafe_allow_html=True)
with col_head2:
    c1, c2 = st.columns(2)
    with c1:
        # Botão com link para o GitHub
        st.markdown(
            """
            <a href="https://github.com/ANIBEserra/ai-election2026-rag-agent" target="_blank" style="text-decoration: none;">
                <div style="background-color: #0F172A; color: #FFFFFF; border-radius: 8px; padding: 7px 7px; text-align: center; font-size: 0.85rem; font-weight: 600; display: flex; align-items: center; justify-content: center; gap: 6px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <svg height="16" width="16" viewBox="0 0 16 16" fill="white">
                        <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.28.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"></path>
                    </svg>
                    GitHub
                </div>
            </a>
            """,
            unsafe_allow_html=True
        )
    with c2:
        if st.button("Reiniciar", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

st.markdown("<hr style='border: 0; height: 1px; background: #CBD5E1; margin: 15px 0;'>", unsafe_allow_html=True)

# --- 3. ÁREA PRINCIPAL ---
if "messages" not in st.session_state:
    st.session_state.messages = []

pergunta_clicada = None
if not st.session_state.messages:
    render_hero_welcome()
    st.markdown("<p style='text-align: center; font-weight: 600; margin-bottom: 15px;'>Selecione um tema de análise rápida:</p>", unsafe_allow_html=True)
    pergunta_clicada = render_prompt_grid()
else:
    for msg in st.session_state.messages:
        if "structured_data" in msg:
            render_comparison_cards(msg["structured_data"], tema_pergunta=msg.get("pergunta", "Análise"))

# --- 4. BARRA DE DIGITAÇÃO ---
prompt_usuario = st.chat_input("Digite sua pergunta para iniciarmos a análise comparativa...")
final_prompt = pergunta_clicada if pergunta_clicada else prompt_usuario

if final_prompt:
    st.session_state.messages.append({"role": "user", "content": final_prompt})
    with st.spinner("Analisando planos de governo..."):
        try:
            dados_json = engine.analisar_propostas_estruturado(final_prompt)
            st.session_state.messages.append({
                "role": "assistant",
                "structured_data": dados_json,
                "pergunta": final_prompt
            })
            st.rerun()
        except Exception as e:
            st.error(f"Erro ao processar: {e}")
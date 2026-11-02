from pathlib import Path
import streamlit as st

def load_css():
    """Lê e injeta o arquivo CSS customizado no Streamlit."""
    css_path = Path(__file__).parent / "styles.css"
    if css_path.exists():
        with open(css_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def render_hero_welcome():
    load_css()
    st.markdown(
        """
        <div class="hero-container" style="text-align: center; margin: 2rem 0;">
            <div style="width: 56px; height: 56px; background: linear-gradient(135deg, #3B82F6, #1D4ED8); border-radius: 50%; margin: 0 auto 16px auto;"></div>
            <div class="hero-title" style="font-size: 2rem; font-weight: 800; margin-bottom: 8px;">Olá, seja bem-vindo(a)! 👋</div>
            <div class="hero-subtitle" style="font-size: 1rem; max-width: 600px; margin: 0 auto;">
                Sou seu assistente analítico para as Eleições 2026. Selecione uma sugestão abaixo ou digite sua pergunta para iniciarmos a análise comparativa.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

def render_prompt_grid():
    load_css()
    temas = [
        {"titulo": "🏥 Saúde", "pergunta": "Quais as propostas para a saúde e como pretendem financiá-la?"},
        {"titulo": "🛡️ Segurança Pública", "pergunta": "Quais as medidas propostas para segurança pública e combate ao crime?"},
        {"titulo": "💰 Finanças", "pergunta": "Quais as estratégias de financiamento e impacto no orçamento?"},
        {"titulo": "📚 Educação", "pergunta": "Quais são as metas e propostas para a educação básica e ensino superior?"},
        {"titulo": "🤝 Programas Sociais", "pergunta": "Quais as propostas de programas de transferência de renda e assistência social?"},
        {"titulo": "🏗️ Infraestrutura", "pergunta": "Quais os planos de investimento em infraestrutura, transportes e saneamento?"},
        {"titulo": "📊 Economia e Gastos", "pergunta": "Quais as propostas econômicas, controle inflacionário e regras fiscais?"},
        {"titulo": "🎭 Cultura", "pergunta": "Quais as diretrizes para incentivo à cultura, arte e economia criativa?"},
        {"titulo": "🌱 Investimento e Bem estar", "pergunta": "Quais as políticas voltadas para sustentabilidade, meio ambiente e bem-estar?"}
    ]

    pergunta_selecionada = None
    for i in range(0, len(temas), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(temas):
                tema = temas[i + j]
                with cols[j]:
                    if st.button(tema["titulo"], key=f"grid_card_{i+j}", use_container_width=True):
                        pergunta_selecionada = tema["pergunta"]
    return pergunta_selecionada

def render_comparison_cards(dados_json: dict, tema_pergunta: str = "Análise Comparativa"):
    """
    Renderiza o infográfico comparativo em formato de Abas / Carrossel Horizontal:
    - Lula (PT): Vermelho Bordô (#991B1B)
    - Bolsonaro (PL): Azul Escuro (#1E3A8A)
    """
    load_css()
    candidatos = dados_json.get("candidatos", [])
    
    if not candidatos:
        st.warning("Nenhum dado de candidato encontrado para esta consulta.")
        return

    cand_a = candidatos[0] if len(candidatos) > 0 else {}
    cand_b = candidatos[1] if len(candidatos) > 1 else {}

    nome_a = cand_a.get('nome_candidato', 'Candidato A')
    sigla_a = cand_a.get('sigla_partido', '')
    
    nome_b = cand_b.get('nome_candidato', 'Candidato B')
    sigla_b = cand_b.get('sigla_partido', '')

    def get_cand_theme(nome, sigla):
        nome_upper = f"{nome} {sigla}".upper()
        if "LULA" in nome_upper or "PT" in nome_upper:
            return {
                "header_bg": "background: linear-gradient(135deg, #7F1D1D, #991B1B) !important; color: #FFFFFF !important;",
                "card_style": "background-color: #FEF2F2 !important; border-left: 6px solid #991B1B !important; border-top: 1px solid #FCA5A5 !important; border-right: 1px solid #FCA5A5 !important; border-bottom: 1px solid #FCA5A5 !important; border-radius: 12px; padding: 18px; box-shadow: 0 2px 6px rgba(0,0,0,0.03);",
                "tag_style": "color: #7F1D1D !important; font-weight: 800; font-size: 0.9rem; margin-bottom: 8px; border-bottom: 1px solid #FECACA; padding-bottom: 4px; display: flex; align-items: center; gap: 6px;",
                "text_style": "color: #7F1D1D !important; font-size: 0.9rem; line-height: 1.5; margin: 0;",
                "icon": "🔴"
            }
        return {
            "header_bg": "background: linear-gradient(135deg, #1E3A8A, #1E40AF) !important; color: #FFFFFF !important;",
            "card_style": "background-color: #EFF6FF !important; border-left: 6px solid #1E3A8A !important; border-top: 1px solid #93C5FD !important; border-right: 1px solid #93C5FD !important; border-bottom: 1px solid #93C5FD !important; border-radius: 12px; padding: 18px; box-shadow: 0 2px 6px rgba(0,0,0,0.03);",
            "tag_style": "color: #1E3A8A !important; font-weight: 800; font-size: 0.9rem; margin-bottom: 8px; border-bottom: 1px solid #BFDBFE; padding-bottom: 4px; display: flex; align-items: center; gap: 6px;",
            "text_style": "color: #1E3A8A !important; font-size: 0.9rem; line-height: 1.5; margin: 0;",
            "icon": "🔵"
        }

    theme_a = get_cand_theme(nome_a, sigla_a)
    theme_b = get_cand_theme(nome_b, sigla_b)

    # 1. Título do Tema
    st.markdown(f'<div class="vs-theme-title">| {tema_pergunta}</div>', unsafe_allow_html=True)

    # 2. Cabeçalho Convergente
    st.markdown(
        f"""
        <div class="vs-header-container">
            <div class="vs-header-left" style="{theme_a['header_bg']}">{theme_a['icon']} {nome_a} ({sigla_a})</div>
            <div class="vs-circle">VS</div>
            <div class="vs-header-right" style="{theme_b['header_bg']}">{theme_b['icon']} {nome_b} ({sigla_b})</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # 3. Níveis da Análise mapeados em Abas (Carrossel)
    niveis = [
        ("📌 Proposta Principal", "proposta_principal"),
        ("📊 Dados Quantitativos", "dados_quantitativos"),
        ("✅ Impactos Positivos", "impactos_positivos"),
        ("⚠️ Riscos e Desafios", "riscos_desafios")
    ]

    # Criação do carrossel horizontal através de st.tabs
    aba_titulos = [n[0] for n in niveis]
    abas = st.tabs(aba_titulos)

    for aba, (badge_titulo, key_json) in zip(abas, niveis):
        val_a = cand_a.get(key_json, "Informação não especificada no plano de governo.")
        val_b = cand_b.get(key_json, "Informação não especificada no plano de governo.")

        with aba:
            st.markdown("<div style='margin-top: 12px;'></div>", unsafe_allow_html=True)
            col_left, col_right = st.columns(2)

            with col_left:
                st.markdown(
                    f"""
                    <div style="{theme_a['card_style']}">
                        <div style="{theme_a['tag_style']}">
                            {theme_a['icon']} {nome_a} ({sigla_a})
                        </div>
                        <p style="{theme_a['text_style']}">{val_a}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with col_right:
                st.markdown(
                    f"""
                    <div style="{theme_b['card_style']}">
                        <div style="{theme_b['tag_style']}">
                            {theme_b['icon']} {nome_b} ({sigla_b})
                        </div>
                        <p style="{theme_b['text_style']}">{val_b}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
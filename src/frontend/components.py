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
        <div class="hero-container">
            <div class="hero-sphere"></div>
            <div class="hero-title">Olá, seja bem-vindo(a)! 👋</div>
            <div class="hero-subtitle">
                Sou seu assistente analítico para as Eleições 2026. Selecione uma sugestão abaixo ou digite sua pergunta para iniciarmos a análise comparativa.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

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
    Renderiza o infográfico comparativo visual simétrico em Light Mode.
    """
    load_css()
    candidatos = dados_json.get("candidatos", [])
    
    if not candidatos:
        st.warning("Nenhum dado de candidato encontrado para esta consulta.")
        return

    cand_a = candidatos[0] if len(candidatos) > 0 else {}
    cand_b = candidatos[1] if len(candidatos) > 1 else {}

    nome_a = f"{cand_a.get('nome_candidato', 'Candidato A')} ({cand_a.get('sigla_partido', 'N/A')})"
    nome_b = f"{cand_b.get('nome_candidato', 'Candidato B')} ({cand_b.get('sigla_partido', 'N/A')})"

    # 1. Título com a barra vertical azul
    st.markdown(f'<div class="vs-theme-title">| {tema_pergunta}</div>', unsafe_allow_html=True)

    # 2. Cabeçalho Convergente Azul x Verde
    st.markdown(
        f"""
        <div class="vs-header-container">
            <div class="vs-header-left">👤 {nome_a}</div>
            <div class="vs-circle">VS</div>
            <div class="vs-header-right">👤 {nome_b}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # 3. Definição dos 4 Níveis do Eixo Central
    niveis = [
        ("📌 Proposta Principal", "proposta_principal", "vs-text-bold"),
        ("📊 Dados Quantitativos", "dados_quantitativos", "vs-text-green"),
        ("✅ Impactos Positivos", "impactos_positivos", ""),
        ("⚠️ Riscos e Desafios", "riscos_desafios", "vs-text-amber")
    ]

    # 4. Renderização simétrica em 3 colunas [Esquerda (5), Centro (2), Direita (5)]
    for badge_titulo, key_json, custom_class in niveis:
        val_a = cand_a.get(key_json, "Informação não especificada no plano de governo.")
        val_b = cand_b.get(key_json, "Informação não especificada no plano de governo.")

        col_left, col_center, col_right = st.columns([5, 2, 5])

        with col_left:
            st.markdown(
                f"""
                <div class="vs-card-box">
                    <p class="vs-body-text {custom_class}">{val_a}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col_center:
            st.markdown(
                f"""
                <div class="vs-center-badge">
                    {badge_titulo}
                </div>
                """,
                unsafe_allow_html=True
            )

        with col_right:
            st.markdown(
                f"""
                <div class="vs-card-box">
                    <p class="vs-body-text {custom_class}">{val_b}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown("<div style='margin-bottom: 16px;'></div>", unsafe_allow_html=True)
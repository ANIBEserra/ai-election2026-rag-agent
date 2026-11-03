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
    Renderiza os cartões verticais pareados para Mobile/Desktop
    sem risco de vazamento de código HTML.
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
        full = f"{nome} {sigla}".upper()
        if "LULA" in full or "PT" in full:
            return {
                "header_bg": "background: linear-gradient(135deg, #7F1D1D, #991B1B); color: #FFFFFF;",
                "box_style": "background-color: #FEF2F2 !important; border-left: 6px solid #991B1B !important; border-top: 1px solid #FCA5A5 !important; border-right: 1px solid #FCA5A5 !important; border-bottom: 1px solid #FCA5A5 !important;",
                "tag_style": "color: #7F1D1D !important; border-bottom: 1px solid #FECACA;",
                "text_color": "color: #7F1D1D !important;",
                "icon": "🔴"
            }
        return {
            "header_bg": "background: linear-gradient(135deg, #1E3A8A, #1E40AF); color: #FFFFFF;",
            "box_style": "background-color: #EFF6FF !important; border-left: 6px solid #1E3A8A !important; border-top: 1px solid #93C5FD !important; border-right: 1px solid #93C5FD !important; border-bottom: 1px solid #93C5FD !important;",
            "tag_style": "color: #1E3A8A !important; border-bottom: 1px solid #BFDBFE;",
            "text_color": "color: #1E3A8A !important;",
            "icon": "🔵"
        }

    t_a = get_cand_theme(nome_a, sigla_a)
    t_b = get_cand_theme(nome_b, sigla_b)

    niveis = [
        ("📌 Proposta Principal", "proposta_principal"),
        ("📊 Dados Quantitativos", "dados_quantitativos"),
        ("✅ Impactos Positivos", "impactos_positivos"),
        ("⚠️ Riscos e Desafios", "riscos_desafios")
    ]

    # Renderiza o Título e o Cabeçalho VS
    st.markdown(f'<div class="vs-theme-title">| {tema_pergunta}</div>', unsafe_allow_html=True)
    
    header_html = (
        f'<div style="display: flex; align-items: center; position: relative; margin-bottom: 25px;">'
        f'<div style="flex: 1; {t_a["header_bg"]} padding: 12px; border-radius: 10px 0 0 10px; text-align: center; font-weight: 700; font-size: 1rem;">'
        f'{t_a["icon"]} {nome_a} ({sigla_a})'
        f'</div>'
        f'<div style="position: absolute; left: 50%; top: 50%; transform: translate(-50%, -50%); width: 40px; height: 40px; background: #FFF; border: 3px solid #1E3A8A; border-radius: 50%; color: #0F172A; font-weight: 900; display: flex; align-items: center; justify-content: center; z-index: 10; box-shadow: 0 4px 8px rgba(0,0,0,0.15);">'
        f'VS'
        f'</div>'
        f'<div style="flex: 1; {t_b["header_bg"]} padding: 12px; border-radius: 0 10px 10px 0; text-align: center; font-weight: 700; font-size: 1rem;">'
        f'{t_b["icon"]} {nome_b} ({sigla_b})'
        f'</div>'
        f'</div>'
    )
    st.markdown(header_html, unsafe_allow_html=True)

    # Renderiza cada bloco de subtema separadamente para não sobrecarregar o parser do Streamlit
    for badge_titulo, key_json in niveis:
        val_a = cand_a.get(key_json, "Informação não especificada no plano de governo.")
        val_b = cand_b.get(key_json, "Informação não especificada no plano de governo.")

        card_block = (
            f'<div style="margin-bottom: 20px;">'
            f'<div style="background-color: #F1F5F9; color: #334155; border: 1px solid #CBD5E1; padding: 8px 12px; border-radius: 8px; text-align: center; font-weight: 700; font-size: 0.9rem; margin-bottom: 10px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">'
            f'{badge_titulo}'
            f'</div>'
            f'<div style="display: flex; flex-wrap: wrap; gap: 12px;">'
            f'<div style="flex: 1; min-width: 280px; {t_a["box_style"]} border-radius: 12px; padding: 14px; box-shadow: 0 2px 4px rgba(0,0,0,0.03);">'
            f'<div style="{t_a["tag_style"]} font-weight: 800; font-size: 0.85rem; margin-bottom: 6px; padding-bottom: 4px; display: flex; align-items: center; gap: 6px;">'
            f'{t_a["icon"]} {nome_a} ({sigla_a})'
            f'</div>'
            f'<p style="{t_a["text_color"]} font-size: 0.88rem; line-height: 1.5; margin: 0;">{val_a}</p>'
            f'</div>'
            f'<div style="flex: 1; min-width: 280px; {t_b["box_style"]} border-radius: 12px; padding: 14px; box-shadow: 0 2px 4px rgba(0,0,0,0.03);">'
            f'<div style="{t_b["tag_style"]} font-weight: 800; font-size: 0.85rem; margin-bottom: 6px; padding-bottom: 4px; display: flex; align-items: center; gap: 6px;">'
            f'{t_b["icon"]} {nome_b} ({sigla_b})'
            f'</div>'
            f'<p style="{t_b["text_color"]} font-size: 0.88rem; line-height: 1.5; margin: 0;">{val_b}</p>'
            f'</div>'
            f'</div>'
            f'</div>'
        )
        st.markdown(card_block, unsafe_allow_html=True)
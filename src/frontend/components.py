from pathlib import Path
import json
import streamlit as st
import streamlit.components.v1 as components

def load_css():
    """Lê e injeta o arquivo CSS customizado no Streamlit."""
    css_path = Path(__file__).parent / "styles.css"
    if css_path.exists():
        with open(css_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def render_hero_welcome():
    load_css()
    st.markdown(
        '<div class="hero-container" style="text-align: center; margin: 2rem 0;">'
        '<div style="width: 56px; height: 56px; background: linear-gradient(135deg, #3B82F6, #1D4ED8); border-radius: 50%; margin: 0 auto 16px auto;"></div>'
        '<div class="hero-title" style="font-size: 2rem; font-weight: 800; margin-bottom: 8px;">Olá, seja bem-vindo(a)! 👋</div>'
        '<div class="hero-subtitle" style="font-size: 1rem; max-width: 600px; margin: 0 auto;">'
        'Sou seu assistente analítico para as Eleições 2026. Selecione uma sugestão abaixo ou digite sua pergunta para iniciarmos a análise comparativa.'
        '</div>'
        '</div>',
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
    Renderiza um Carrossel no estilo Stack Cards 3D (Swiper.js).
    Possui altura dinâmica e auto-ajuste para evitar cortes de texto no mobile.
    """
    load_css()
    candidatos = dados_json.get("candidatos", [])
    if not candidatos:
        st.warning("Nenhum dado de candidato encontrado para esta consulta.")
        return

    # Título do Tema em Streamlit nativo
    st.markdown(f'<div class="vs-theme-title">| {tema_pergunta}</div>', unsafe_allow_html=True)

    def get_cand_theme(cand: dict):
        nome = cand.get('nome_candidato', 'Candidato')
        sigla = cand.get('sigla_partido', '')
        full = f"{nome} {sigla}".upper()

        if "LULA" in full or "PT" in full:
            return {
                "nome": f"{nome} ({sigla})" if sigla else nome,
                "box": "background-color: #FEF2F2; border: 1px solid #FCA5A5; border-left: 6px solid #991B1B;",
                "tag": "color: #7F1D1D;",
                "icon": "🔴"
            }
        elif "BOLSONARO" in full or "PL" in full:
            return {
                "nome": f"{nome} ({sigla})" if sigla else nome,
                "box": "background-color: #EFF6FF; border: 1px solid #93C5FD; border-left: 6px solid #1E3A8A;",
                "tag": "color: #1E3A8A;",
                "icon": "🔵"
            }
        else:
            return {
                "nome": f"{nome} ({sigla})" if sigla else nome,
                "box": "background-color: #F8FAFC; border: 1px solid #CBD5E1; border-left: 6px solid #475569;",
                "tag": "color: #334155;",
                "icon": "⚪"
            }

    niveis = [
        ("📌 Proposta Principal", "proposta_principal"),
        ("📊 Dados Quantitativos", "dados_quantitativos"),
        ("✅ Impactos Positivos", "impactos_positivos"),
        ("⚠️ Riscos e Desafios", "riscos_desafios")
    ]

    # Monta os slides HTML com scroll interno e adaptação de altura
    swiper_slides_html = ""
    for idx, (badge_titulo, key_json) in enumerate(niveis):
        cand_blocks = ""
        for cand in candidatos:
            t = get_cand_theme(cand)
            val = cand.get(key_json, "Não especificado no plano de governo.")
            cand_blocks += f"""
            <div style="{t['box']} border-radius: 12px; padding: 12px; margin-bottom: 10px; text-align: left;">
                <div style="{t['tag']} font-weight: 800; font-size: 0.85rem; margin-bottom: 4px; padding-bottom: 4px; border-bottom: 1px solid rgba(0,0,0,0.08); display: flex; align-items: center; gap: 6px;">
                    {t['icon']} {t['nome']}
                </div>
                <p style="{t['tag']} font-size: 0.85rem; line-height: 1.45; margin: 0; word-break: break-word;">{val}</p>
            </div>
            """

        swiper_slides_html += f"""
        <div class="swiper-slide">
            <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 20px; padding: 16px; box-shadow: 0 10px 25px rgba(0,0,0,0.08); height: 100%; box-sizing: border-box; display: flex; flex-direction: column; justify-content: space-between; max-height: 520px; overflow-y: auto;">
                <div>
                    <div style="background: #F1F5F9; color: #0F172A; text-align: center; font-weight: 800; padding: 8px 12px; border-radius: 10px; font-size: 0.95rem; margin-bottom: 12px;">
                        {badge_titulo}
                    </div>
                    {cand_blocks}
                </div>
                <div style="display: flex; justify-content: space-between; align-items: center; color: #94A3B8; font-weight: 700; font-size: 0.78rem; border-top: 1px solid #F1F5F9; padding-top: 8px; margin-top: 4px; flex-shrink: 0;">
                    <span>Subtema {idx + 1} de {len(niveis)}</span>
                    <span>Deslize para trocar 👉</span>
                </div>
            </div>
        </div>
        """

    # HTML/CSS/JS completo com Swiper e altura ajustada para Mobile e Desktop
    html_component = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.css" />
        <style>
            body {{
                margin: 0;
                padding: 0;
                background: transparent;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
            }}
            .swiper {{
                width: 100%;
                max-width: 440px;
                height: 540px;
                padding-top: 10px;
                padding-bottom: 30px;
            }}
            .swiper-slide {{
                border-radius: 20px;
            }}
            /* Estilização sutil da barra de rolagem interna */
            ::-webkit-scrollbar {{
                width: 4px;
            }}
            ::-webkit-scrollbar-thumb {{
                background: #CBD5E1;
                border-radius: 4px;
            }}
        </style>
    </head>
    <body>
        <div class="swiper mySwiper">
            <div class="swiper-wrapper">
                {swiper_slides_html}
            </div>
            <div class="swiper-pagination"></div>
        </div>

        <script src="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.js"></script>
        <script>
            var swiper = new Swiper(".mySwiper", {{
                effect: "cards",
                grabCursor: true,
                pagination: {{
                    el: ".swiper-pagination",
                    clickable: true,
                }},
            }});
        </script>
    </body>
    </html>
    """

    components.html(html_component, height=580)
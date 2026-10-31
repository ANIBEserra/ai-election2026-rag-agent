<div align="center">
  <a href="https://ai-election2026-rag-agent.streamlit.app/" target="_blank">
    <img src="https://img.shields.io/badge/_Acessar_App-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit App" />
  </a>
</div>

## Definição do Problema

Planos de governo publicados durante períodos eleitorais são documentos em formato PDF não estruturado, frequentemente longos e com terminologias heterogêneas. Para cidadãos consultar, comparar e extrair propostas específicas sobre eixos como saúde, educação, economia ou infraestrutura consome tempo e dificulta a checagem objetiva.


## Análise de Dores e Hipótese

### Dores Mapeadas

* **Assimetria de Informação:** Dificuldade em localizar propostas concretas em meio a textos extensos de tom institucional.
* **Volume Não Estruturado:** Falta de padronização nas estruturas dos documentos fornecidos pelos partidos.
* **Complexidade na Comparação:** Impossibilidade de realizar buscas por palavras-chave tradicionais sem perder o contexto semântico das propostas.

### Hipótese

A criação de um pipeline local baseado na arquitetura **RAG (Retrieval-Augmented Generation)** utilizando **LangChain** e modelos do **Google Gemini** reduzirá o tempo de consulta a segundos, permitindo extrair respostas fundamentadas exclusivamente nos trechos oficiais extraídos dos planos de governo.


## Proposta de Resolução (Protótipo Local Passo a Passo)

### 1. Onde Encontrar os PDFs das Propostas?

Os planos de governo oficiais das candidaturas à Presidência da República ficam disponíveis publicamente para download nos repositórios mantidos pela Justiça Eleitoral:

* **Portal de Dados Abertos:** Os arquivos zipados contendo todas as propostas consolidadas em PDF podem ser acessados diretamente no [Portal de Dados Abertos do TSE](https://dadosabertos.tse.jus.br/dataset/candidatos-2026).
* **Sistema de Consultas:** Para consultar candidaturas individuais ou baixar arquivos específicos por candidato, utilize o portal [DivulgaCandContas do TSE](https://divulgacandcontas.tse.jus.br/).

Para o teste local, crie uma pasta `data/` na raiz do projeto e salve de 1 a 2 arquivos PDF baixados dessas fontes (por exemplo: `proposta_candidato_A.pdf`).


## Melhoria Contínua

1. **Inclusão de Metadados de Candidatos:** Adicionar atributos nos documentos (`candidato_nome`, `partido`, `eixo_tematico`) durante a fase de *chunking* para permitir filtros antes da busca vetorial.
2. **Avaliação da Qualidade das Respostas:** Testar técnicas de avaliação RAG (usando frameworks como `Ragas`) para medir precisão e relevância das respostas.
3. **Evolução para Nuvem:** Migrar o banco vetorial em memória para o **BigQuery Vector Search** e expor a lógica da cadeia via **FastAPI** no Cloud Run para permitir a integração com o front-end em Google Apps Script ou AppSheet.

## 📁 Estrutura do Projeto (Arquitetura V2)

A arquitetura do projeto foi desenvolvida de forma modularizada, separando o pipeline de ingestão de dados, o motor RAG de consulta e os pontos de entrada:

```text
ai-election2026-rag-agent/
│
├── data/
│   ├── documentos_2026/        # PDFs dos planos de governo baixados do TSE
│   └── 02_faiss_index/         # Banco de dados vetorial FAISS persistido localmente
│
├── docs/
│   └── architecture_diagram.md # Diagrama de arquitetura do pipeline RAG
│
├── notebooks/
│   └── 01_eda_pdf_structure_inspection.ipynb  # Notebook V1 de inspeção, ETL e prototipagem
│
├── src/
│   ├── __init__.py
│   ├── frontend/
│   │   ├── __init__.py
│   │   ├── styles.css           # Estilização CSS das colunas, cards e badges
│   │   └── components.py        # Funções Python que renderizam o HTML comparativo
│   │ 
│   ├── ingestion/
│   │   ├── __init__.py
│   │   ├── candidates.py       # Dicionário de metadados dos candidatos (nome, partido, vice)
│   │   └── ingest.py           # Pipeline de ETL: Leitura de PDF -> Chunking -> Embeddings -> FAISS
│   │
│   └── rag/
│       ├── __init__.py
│       └── engine.py           # Motor RAG: Busca no FAISS + Geração analítica com Gemini
│
├── .env                        # Variáveis de ambiente (GOOGLE_API_KEY)
├── .gitignore                  # Arquivos ignorados pelo versionamento Git
├── app.py                      # Ponto de entrada (CLI/Script) para realizar as consultas
└── requirements.txt            # Dependências do projeto comentadas
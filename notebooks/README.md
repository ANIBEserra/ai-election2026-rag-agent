### Padrão de Nomenclatura para a Pasta `notebooks/`

A estrutura adota o padrão **`XX_categoria_descricao.ipynb`**:

* **`XX_`**: Número sequencial de dois dígitos para ordenação cronológica no sistema de arquivos.
* **`categoria_`**:
* `eda_`: Análise exploratória de dados e inspeção de estrutura.
* `proto_`: Prototipagem de componentes, algoritmos e pipelines.
* `eval_`: Avaliação de qualidade, acurácia e benchmarks do agente.


* **`descricao`**: Descrição sucinta em *snake_case* (sem acentos, espaços ou caracteres especiais).

---

### Sequência Sugerida de Notebooks (`ai-election2026-rag-agent`)

| Arquivo do Notebook | Propósito e Escopo Técnico |
| --- | --- |
| **`01_eda_pdf_structure_inspection.ipynb`** | Leitura exploratória dos PDFs em `data/01_raw/`. Inspeção do layout, extração de texto via `PyPDFLoader`/`pdfplumber`, identificação de ruídos (cabeçalhos, rodapés, tabelas quebradas) e validação da qualidade do texto bruto. |
| **`02_proto_chunking_strategies.ipynb`** | Prototipagem e comparação de estratégias de fragmentação do texto (`RecursiveCharacterTextSplitter`). Testes empíricos variando `chunk_size` (ex: 500 vs 1000) e `chunk_overlap` para otimizar a preservação do contexto semântico. |
| **`03_proto_embeddings_faiss_index.ipynb`** | Vetorização das partes do texto utilizando a API do Gemini (`text-embedding-004`). Armazenamento e indexação no banco vetorial local (**FAISS**), seguidos por testes de busca por similaridade semântica via query vetorial. |
| **`04_proto_rag_chain_gemini.ipynb`** | Construção da cadeia RAG end-to-end com **LangChain** (`create_retrieval_chain` + `gemini-1.5-flash`). Configuração do *system prompt*, integração do *retriever* e geração de respostas com citações de fonte. |
| **`05_eval_rag_responses_quality.ipynb`** | Execução de bateria de testes com perguntas em eixos temáticos reais (Saúde, Economia, Educação, Segurança). Validação de fidelidade do modelo contra alucinações e checagem da rastreabilidade das páginas. |
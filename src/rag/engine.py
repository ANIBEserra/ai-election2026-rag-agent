import json
import os
import re
from pathlib import Path
import streamlit as st
from google import genai
import google.genai.types as types
from langchain_community.vectorstores import FAISS

class RAGEngine:
    def __init__(self, faiss_path: Path):
        # Tenta ler do Streamlit Secrets ou do ambiente (.env)
        api_key = os.getenv("GOOGLE_API_KEY")

        self.CLIENT = genai.Client(api_key=api_key)
        self.EMBEDDING_MODEL = "gemini-embedding-001"
        self.LLM_MODEL = "gemini-3.5-flash-lite"
        
        # Carrega o banco vetorial local
        self.vectorstore = FAISS.load_local(
            folder_path=str(faiss_path),
            embeddings=None,
            allow_dangerous_deserialization=True
        )


    def analisar_propostas_estruturado(self, pergunta: str) -> dict:
        #2. Transformar o prompt em vetor
        query_response = self.CLIENT.models.embed_content(
            model=self.EMBEDDING_MODEL,
            contents=pergunta
        )
        query_vector = query_response.embeddings[0].values
        print("\n2. Prompt transformado em vetor")

        #3. recuperar vetores no nosso banco vetorial FAISS k=50 (similaridade)
        documentos_recuperados = self.vectorstore.similarity_search_by_vector(query_vector, k=50)
        print("\n3. Vetores no banco vetorial FAISS recuperados.")

        #4. Montar contexto estruturado com retorno de metadados
        contexto_formatado = ""
        for i, doc in enumerate(documentos_recuperados):
            candidato = doc.metadata.get("nome_candidato", "N/A")
            partido = doc.metadata.get("sigla_partido", "N/A")
            pagina = doc.metadata.get("page", "N/A")
            contexto_formatado += f"\n--- [TRECHO {i+1}] CANDIDATO: {candidato} ({partido}) | PÁGINA: {pagina} ---\n{doc.page_content}\n"

        print("\n4. Contexto estruturado com retorno de metadados estruturado")

        #5. Prompt especializado PACE em análise comparativa com system_instruction e o prompt_final
        system_instruction = """Você é um economista e analista de políticas públicas sênior, imparcial e altamente crítico, especializado nas Eleições Presidenciais de 2026.

        Sua tarefa é realizar uma ANÁLISE CRÍTICA E QUANTITATIVA sobre as propostas dos candidatos com base EXCLUSIVAMENTE no contexto fornecido.

        INSTRUÇÕES RIGOROSAS PARA CADA CANDIDATO:
        1. Resumo das Propostas & Números Chave:
        - Liste as propostas identificando os mecanismos de execução ("Como fará").
        - Destaque OBRIGATORIAMENTE todos os dados quantitativos explicitados no texto (valores orçamentários, percentuais, prazos, metas ou métricas).
        - Se o documento não trouxer números, declare EXPLICITAMENTE: "O plano não apresenta dados quantitativos ou metas numéricas explícitas para este tema."
        - Cite OBRIGATORIAMENTE a página de origem no formato [Pág. X].

        2. Análise Crítica de Impactos (Cenário Brasil 2026):
        - Impactos Positivos (Oportunidades): Quais avanços sociais, econômicos ou administrativos a medida pode gerar?
        - Riscos e Pontos de Atenção (Desafios): Avalie a viabilidade fiscal, orçamentária e operacional considerando o atual cenário do país (espaço no orçamento, necessidade de aprovação legislativa, complexidade de implementação).

        REGRAS RÍGIDAS:
        - Mantenha tom neutro, técnico e estritamente focado em políticas públicas.
        - Não tome partido; aplique o mesmo rigor crítico a todos os planos analisados.

        A resposta DEVE ser um objeto JSON no formato:
        {
        "candidatos": [
            {
            "nome_candidato": "Nome do Candidato",
            "sigla_partido": "Sigla do Partido",
            "proposta_principal": "Descrição da proposta e como fará executá-la com citação [Pág. X]",
            "dados_quantitativos": "Dados numéricos, %, valores e prazos [Pág. X] OU a declaração 'O plano não apresenta dados quantitativos ou metas numéricas explícitas para este tema.'",
            "impactos_positivos": "Avanços sociais, econômicos ou administrativos esperados",
            "riscos_desafios": "Análise de viabilidade fiscal, orçamentária e complexidade operacional"
            }
        ]
        }"""

        prompt_final = f"CONTEXTO:\n{contexto_formatado}\n\nPERGUNTA:\n{pergunta}"

        print("\n5. Prompt especializado em análise comparativa com system_instruction e o prompt_final montado")

        #6. Gerar resposta comparativa como o modelo
        print("\n6. Gerando resposta comparativa com o modelo...")
        resposta = self.CLIENT.models.generate_content(
            model=self.LLM_MODEL,
            contents=prompt_final,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.1, #Rigor analítico com baixa alucinação
                response_mime_type="application/json" # Assegura o parsing limpo no Python
            )
        )
        texto_resposta = resposta.text.replace("```json", "").replace("```", "").strip()
        return json.loads(texto_resposta)
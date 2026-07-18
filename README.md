# LLM + Python — Estudo aplicado com projetos reais

Repositório de estudo estruturado sobre LLMs aplicados com Python, construído em 6 fases progressivas — da consolidação de fundamentos de Python até um pipeline completo de RAG com avaliação automatizada. Cada fase foi implementada e testada de verdade, não apenas estudada em teoria.

## Sobre este repositório

Diferente da maioria dos materiais de LLM disponíveis, que usam diretamente a API da OpenAI ou Anthropic, este projeto integra com **Azure AI Foundry via Agent Service**, com autenticação interativa (Microsoft Entra ID) — um cenário mais próximo de ambientes corporativos reais, com desafios próprios de autenticação, SDKs e formatos de API que não aparecem em tutoriais "de chave direta".

## Stack

- **Linguagem:** Python 3.14
- **LLM:** Azure AI Foundry (Agent Service) — modelo `gpt-4.1-mini`
- **Embeddings:** `sentence-transformers` (`paraphrase-multilingual-MiniLM-L12-v2`)
- **Validação de dados:** Pydantic
- **Autenticação:** `azure-identity` (InteractiveBrowserCredential)

## Estrutura do projeto

```
LLM--Python/
├── README.md
├── requirements.txt
├── roadmap-llm-python.md
├── fase0_python_para_ia/
│   ├── teste_types.py
│   ├── teste_dataclasses.py
│   └── teste_pydantic.py
├── fase1_fundamentos_llm/
│   ├── teste_embeddings.py
│   └── teste_temperatura.py
├── fase2_prompting/
│   ├── teste_foundry.py
│   ├── teste_fewshot.py
│   └── teste_estruturado.py
├── fase3_tool_calling/
│   ├── teste_tool_clima.py
│   ├── teste_tool_calling.py
│   └── teste_listar_deployments.py
├── fase4_rag/
│   ├── teste_rag_chunking.py
│   ├── teste_rag_embeddings.py
│   ├── teste_rag_busca.py
│   └── teste_rag_completo.py
└── fase5_avaliacao/
    └── teste_avaliacao.py
```

## Estrutura por fase

### Fase 0 — Python para IA
Consolidação de fundamentos essenciais para trabalhar com LLM em produção: type hints, Pydantic vs. dataclasses, ambientes virtuais, e `async/await` (com benchmark real comparando chamadas síncronas vs. assíncronas — resultado: quase metade do tempo total com paralelismo).

### Fase 1 — Fundamentos conceituais
Tokenização, embeddings e mecanismo de atenção testados na prática, não só estudados. Destaque: teste de similaridade semântica revelou que o modelo de embeddings padrão (`all-MiniLM-L6-v2`, focado em inglês) performa mal com palavras soltas em português — decisão documentada de trocar para um modelo multilíngue nas fases seguintes.

### Fase 2 — Prompting como engenharia
Zero-shot vs. few-shot, saídas estruturadas (JSON validado com Pydantic), chain-of-thought e boas práticas de system prompt — todos testados chamando um Agent real do Azure AI Foundry (`TurismoIA`).

### Fase 3 — Tool calling
Implementação manual (sem framework) do loop completo de tool calling: o modelo decide chamar uma função (consulta de previsão do tempo via API Open-Meteo), o código executa de verdade, e o resultado retorna ao modelo para a resposta final. Inclui resolução de incompatibilidade de schema entre Chat Completions API e Responses API.

### Fase 4 — RAG (Retrieval-Augmented Generation)
Pipeline completo: chunking por seção Markdown, embeddings multilíngues, busca por similaridade de cosseno, e geração aumentada com instrução anti-alucinação. Teste real expôs limitação da busca semântica (chunk correto não era o mais similar) — resolvido ajustando `top_k` e delegando o filtro final ao LLM.

### Fase 5 — Avaliação e LLMOps
Pipeline de avaliação automatizado com golden dataset, LLM-as-a-judge (um segundo LLM avalia a qualidade da resposta do primeiro) e métricas de tempo por resposta. O teste revelou uma limitação real do RAG: perguntas que exigem agregação sobre a estrutura do documento (ex: "quantas seções existem") não são bem respondidas por busca semântica local — um problema de arquitetura, não de prompt.

## Principais decisões técnicas e por quê

- **Modelo de embeddings multilíngue em vez do padrão:** testes mostraram similaridade semântica ruim em português com o modelo padrão em inglês.
- **`top_k=3` em vez de `top_k=1` no RAG:** a busca por similaridade nem sempre traz o chunk mais relevante em 1º lugar; um `top_k` maior dá margem para o LLM final filtrar o que é útil.
- **`extra_body` para parâmetros específicos do Azure:** o SDK padrão da OpenAI não conhece nativamente `agent_reference`; parâmetros de extensão precisam ser passados via `extra_body`.
- **Autenticação via `schannel`/`pip-system-certs`:** ambiente Windows exigiu ajuste de backend de certificados SSL tanto no Git quanto no Python para acessar APIs externas (GitHub, Hugging Face) corretamente.

## Problemas reais resolvidos ao longo do projeto

- Erro de certificado SSL no Git (`schannel` vs `openssl`)
- Erro de certificado SSL no Python/Hugging Face Hub (`pip-system-certs`)
- Política de execução do PowerShell bloqueando ativação de `venv`
- Incompatibilidade de schema de `tools` entre Chat Completions API e Responses API
- Limitação de `tools` customizadas ao usar `agent_reference` no Foundry

## Como rodar

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python teste_avaliacao.py
```

---

*Projeto de estudo em andamento — próximos passos: consolidar os scripts soltos em um CLI único e expandir o golden dataset de avaliação.*

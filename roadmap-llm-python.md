# Roadmap: LLM + Python

**Perfil de partida:** base em Python, ambiente PyCharm configurado, já com experiência prática relevante (projeto AI Dashboard e chatbot Telegram + Azure AI Foundry). Isso significa que você não começa do zero — já tem contato real com API de LLM, autenticação e SDKs. O roadmap abaixo aproveita essa base e aprofunda.

**Objetivo:** construir conhecimento sólido em LLM aplicado com Python, gerando projetos de portfólio que reforcem sua candidatura a estágio (front-end/web + suporte de TI, com dados/automação como diferencial).

---

## Fase 0 — Python para IA (consolidação)
Antes de mergulhar em LLM, fechar lacunas comuns que travam quem já sabe Python "básico":
- Type hints (`def resposta(texto: str) -> str`)
- Dataclasses e Pydantic (validar dados estruturados)
- Ambientes virtuais (`venv`, `pip`)
- `async/await` — essencial porque chamadas de API de LLM são de rede (I/O-bound)
- Manipulação de JSON

*Projeto rápido:* script que chama uma API qualquer (ex: clima) usando `async/await` e valida a resposta com Pydantic.

---

## Fase 1 — Fundamentos conceituais de LLM
Entender o que acontece "por dentro", sem precisar treinar um modelo do zero:
- Tokenização (como texto vira números)
- Embeddings (como o modelo representa significado)
- Mecanismo de atenção / Transformers (visão geral, sem matemática pesada)
- Como o modelo gera texto (decodificação: temperatura, top-k, top-p)

*Analogia guia:* um LLM é como um autocomplete extremamente sofisticado, que aprendeu padrões de bilhões de textos.

---

## Fase 2 — Prompting como engenharia
Prompt não é "conversa", é contrato de entrada/saída:
- Zero-shot vs Few-shot (few-shot é padrão de produção)
- Chain-of-thought
- Saídas estruturadas (JSON Schema, Pydantic + LLM)
- Boas práticas de system prompt

*Projeto:* script Python que envia few-shot prompts para a API da Anthropic e valida a saída em JSON.

---

## Fase 3 — Tool calling e Agentes
- Como funciona tool/function calling (o modelo decide qual função chamar, seu código executa)
- Diferença entre um "chat" e um "agente"
- Frameworks: LangChain (fundamentos) e LangGraph (agentes com loops/decisão)

*Projeto:* evoluir seu chatbot do Telegram para ter tool calling real (ex: consultar uma API externa quando o usuário pede).

---

## Fase 4 — RAG (Retrieval-Augmented Generation)
Como fazer o LLM responder sobre dados privados/atualizados:
- Pipeline básico: chunking → embeddings → vector store → retrieval → contexto
- Busca híbrida (keyword + semântica) e reranking (nível avançado)

*Projeto:* um "assistente" que responde perguntas sobre seus próprios documentos (ex: seu material do Senai).

---

## Fase 5 — Avaliação e LLMOps
A habilidade mais subestimada, mas mais pedida em vagas:
- Como montar um dataset de avaliação ("golden dataset")
- LLM-as-a-judge
- Rastreamento de custo/latência por chamada

*Projeto:* pipeline de avaliação simples para um dos projetos anteriores.

---

## Fase 6 — Portfólio final
Consolidar 2-3 projetos que mostrem, na prática:
1. Uso de API de LLM com boas práticas (prompting + validação estruturada)
2. Um agente com tool calling
3. Um sistema de RAG simples

Esses projetos, junto com o chatbot que você já fez, formam uma vitrine forte para vagas de estágio — mesmo que a vaga seja front-end, mostrar que você entende IA aplicada é diferencial competitivo.

---

## Como vamos trabalhar
A cada sessão, escolhemos um tópico da fase atual, eu explico o conceito com analogias, guio passo a passo na implementação, e você pratica no PyCharm. Ajustamos o ritmo conforme sua disponibilidade (considerando horário de aula e trabalho).

*Roadmap gerado em: 07/07/2026 — pode e deve ser ajustado conforme avançamos.*

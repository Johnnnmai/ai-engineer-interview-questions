# AI System Design Interview Questions (2026): 15 LLM Design Prompts with Answer Outlines

**Meta description:** 15 AI and LLM system design interview prompts with answer outlines, a 45-minute round structure and a self-scoring checklist for 2026.

AI system design interviews in 2026 ask you to design a product around a language model: a RAG assistant, an agent, an LLM gateway, an evaluation pipeline or a cost-constrained chatbot. Strong answers follow a clear structure (requirements, architecture, data, model choice, evaluation, safety, cost and scale) and put numbers on latency and cost. Below is a 45-minute structure, 15 common prompts with answer outlines and a checklist to score yourself.

## How to structure a 45-minute AI system design round

| Minutes | Step | What to cover |
| --- | --- | --- |
| 0 to 5 | Requirements | Users, tasks, data sources, quality bar, latency and cost targets, safety constraints |
| 5 to 10 | Estimates | Requests per day, tokens per request, rough monthly model cost, storage |
| 10 to 25 | Architecture | Request path, retrieval or tools, model choice, caching, data pipeline |
| 25 to 35 | Evaluation | Offline test set, metrics, online signals, regression gates |
| 35 to 42 | Risks and scale | Failure modes, safety, privacy, rate limits, fallbacks |
| 42 to 45 | Wrap up | Trade-offs you made and what you would build next |

Label estimates as assumptions. A quick token cost estimate with the free [LLM API cost calculator](https://johnnnmai.github.io/ai-engineer-interview-questions/llm-cost-calculator/) is a strong signal in the estimates step.

## Retrieval and knowledge systems (prompts 1 to 4)

- **1. Design a question-answering assistant over internal documents.** Ingestion with structure-aware chunking and metadata, hybrid retrieval with permission filters, reranking, grounded generation with citations, and a labeled evaluation set for retrieval recall and answer faithfulness. Score yourself with the [RAG design rubric](https://johnnnmai.github.io/ai-engineer-interview-questions/guides/rag-system-design-interview-scoring-rubric/).
- **2. Design a customer support chatbot.** Intent routing, retrieval over help content, read-only account tools, escalation to a human, and metrics such as resolution rate, escalation rate and policy compliance. Deep dive: [Design a customer support chatbot](https://johnnnmai.github.io/ai-engineer-interview-questions/questions/design-a-customer-support-chatbot/)
- **3. Design semantic search for an e-commerce catalog.** Hybrid search so exact attributes and SKUs still match, embeddings refreshed as products change, a reranker tuned on click data and A/B tests on conversion. Deep dive: [What is hybrid search?](https://johnnnmai.github.io/ai-engineer-interview-questions/questions/what-is-hybrid-search/)
- **4. Design a multi-tenant RAG platform.** Tenant isolation in the index and caches, per-tenant quotas, document-level access control at retrieval time and audit logs. Deep dive: [Access control in RAG](https://johnnnmai.github.io/ai-engineer-interview-questions/questions/access-control-in-rag/)

## Agents and tools (prompts 5 to 7)

- **5. Design an agent that books travel or files expense reports.** Tools with typed arguments, approval before payments, step and spend limits, idempotent actions and task-level evaluation. See [AI agent interview questions](https://johnnnmai.github.io/ai-engineer-interview-questions/guides/ai-agent-interview-questions/).
- **6. Design a coding assistant for a large repository.** Code-aware retrieval (symbols, files, recent changes), a sandbox to run tests, diff review by the user and evaluation on real tasks with tests as the pass criterion.
- **7. Design an internal tool platform for LLM apps using MCP.** Shared MCP servers for common systems, authentication per user, permission scopes per tool and central logging. Deep dive: [What is MCP?](https://johnnnmai.github.io/ai-engineer-interview-questions/questions/what-is-model-context-protocol-mcp/)

## Platform and infrastructure (prompts 8 to 11)

- **8. Design an LLM gateway.** A single entry point for all model calls with routing, fallbacks between providers, rate limits, budgets per team, caching, redaction and logging. Deep dive: [Design an LLM gateway](https://johnnnmai.github.io/ai-engineer-interview-questions/questions/design-an-llm-gateway/)
- **9. Cut the cost of an LLM feature by half.** Measure cost per request first, then shorter prompts, caching, smaller models for easy traffic, batching and fewer output tokens. Deep dive: [Reducing LLM inference cost](https://johnnnmai.github.io/ai-engineer-interview-questions/questions/how-to-reduce-llm-inference-cost/)
- **10. Reduce p95 latency of a chat product.** Streaming, prompt caching, a smaller or faster model on the critical path, parallel retrieval and tool calls and a latency budget per stage. Deep dive: [Reducing LLM latency](https://johnnnmai.github.io/ai-engineer-interview-questions/questions/how-to-reduce-llm-latency/)
- **11. Design a self-hosted LLM serving stack.** Continuous batching, KV cache management, quantization trade-offs, autoscaling on queue depth and GPU memory, and a fallback to a hosted API. Deep dive: [What is the KV cache?](https://johnnnmai.github.io/ai-engineer-interview-questions/questions/what-is-kv-cache/)

## Evaluation, safety and product (prompts 12 to 15)

- **12. Design an evaluation pipeline for LLM releases.** Versioned test sets by use case, automatic checks plus calibrated LLM judges, human review samples, regression gates in CI and online monitoring after launch. See [LLM evaluation interview questions](https://johnnnmai.github.io/ai-engineer-interview-questions/guides/llm-evaluation-interview-questions/).
- **13. Design guardrails for a public chatbot.** Input and output moderation, prompt injection defenses, topic limits, rate limits, abuse monitoring and a red-team test set. Deep dive: [LLM guardrails](https://johnnnmai.github.io/ai-engineer-interview-questions/questions/what-are-llm-guardrails/)
- **14. Decide between fine-tuning and RAG for a new feature.** RAG for changing or citable knowledge, fine-tuning for format, style or a narrow task, and a small experiment comparing both on the same test set. Deep dive: [RAG vs fine-tuning](https://johnnnmai.github.io/ai-engineer-interview-questions/questions/rag-vs-fine-tuning/)
- **15. Launch an AI feature and prove it works.** Offline evaluation first, then an A/B test with a primary product metric and guardrail metrics for cost, latency and complaints. Deep dive: [A/B testing an AI feature](https://johnnnmai.github.io/ai-engineer-interview-questions/questions/how-to-ab-test-an-ai-feature/)

## Self-scoring checklist

Use this after each practice round. One point per item, 10 total.

| Check | Done? |
| --- | --- |
| Clarified users, tasks and success criteria before drawing | |
| Stated latency and cost targets with numbers | |
| Drew the full request path end to end | |
| Justified the model choice and a fallback | |
| Explained the data or retrieval pipeline, including freshness | |
| Defined an offline evaluation set and metrics | |
| Named online metrics and a rollout plan | |
| Covered security: permissions, prompt injection, data privacy | |
| Named two failure modes and their mitigations | |
| Summarized trade-offs and next steps at the end | |

## How AI system design differs from classic system design

| | Classic system design | AI system design |
| --- | --- | --- |
| Core question | Can it scale and stay available? | Is the output good enough, safe and affordable? |
| Main cost | Servers and storage | Tokens and GPUs |
| Testing | Deterministic tests | Evaluation sets, judges and online metrics |
| New failure modes | Outages, data loss | Hallucination, injection, quality regressions |
| Shared ground | Caching, queues, rate limits, observability | The same, applied to model calls |

## FAQ

- **What is an AI system design interview?** A round where you design a product or platform built around language models, covering architecture, data, evaluation, safety, cost and scale, usually in 45 to 60 minutes.
- **How is it different from an ML system design interview?** ML system design often centers on training a model (features, labels, offline metrics, serving). AI system design in 2026 more often centers on using foundation models through retrieval, tools, prompts and evaluation, with less training work.
- **How should I practice?** Do one prompt per day out loud with a 45-minute timer, score yourself with the checklist above and review weak areas. The free [mock round](https://johnnnmai.github.io/ai-engineer-interview-questions/mock-interview/) and [study plan](https://johnnnmai.github.io/ai-engineer-interview-questions/study-plan/) help pace this.
- **Do I need to draw diagrams?** Yes, a simple boxes-and-arrows diagram of the request path and the data pipeline. Clear flow matters more than tool names.
- **Which prompts are most common?** RAG assistants, support chatbots, LLM gateways and agents with tools come up most often in public interview reports and prep material, so practice those four first. Start with [RAG interview questions](https://johnnnmai.github.io/ai-engineer-interview-questions/guides/rag-interview-questions/).

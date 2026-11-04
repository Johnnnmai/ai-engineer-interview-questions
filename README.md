# 100 AI Engineer Interview Questions (2026) with Full Model Answers

**Free:** [Check your interview answer](https://johnnnmai.github.io/ai-engineer-interview-questions/answer-check/?utm_source=github&utm_medium=readme&utm_campaign=ai-engineer-interview-questions)  |  **Weekly drill packs:** [Valenx Pass](https://valenx.org/go/pass-y?utm_source=github&utm_campaign=ai-engineer-interview-questions&utm_content=readme), $79/yr, a new drill pack every Monday, cancel anytime.

_Last updated: November 1, 2026_ · Every question answered · Graded **Entry / Mid / Senior** · Free, no sign-up

100 graded questions covering LLMs, RAG, agents, fine-tuning, AI system design, MLOps and coding — with full model answers you can study for free right here.

### Quick start

🆓 **Self-check** — [Paste your answer and get a score in 30 seconds](https://johnnnmai.github.io/ai-engineer-interview-questions/answer-check/?utm_source=github&utm_medium=readme&utm_campaign=line26_20261101&utm_content=ai-engineer-interview-questions)

🆓 **Top 30 questions** — [Free 13-page guide with model answers (PDF)](https://sirjohnnymai.gumroad.com/l/aie-top-30-questions?utm_source=github&utm_medium=readme&utm_campaign=line26_20261101&utm_content=ai-engineer-interview-questions)

📘 **Full interview kit** — [The complete AI Engineer Interview bundle](https://sirjohnnymai.gumroad.com/l/ai-engineer-interview-playbook?utm_source=github&utm_medium=readme&utm_campaign=line26_20261101&utm_content=ai-engineer-interview-questions).

---

**Who this is for:** AI Engineer, LLM Engineer, Applied AI / Applied ML Engineer, GenAI Engineer, Agent Engineer, ML Engineer moving into LLM work, Forward Deployed / Solutions Engineer (AI), AI Product Engineer.

**How to use:** answer each question out loud in under 2 minutes, then read the model answer and score yourself 1-5. Anything below 4 is your study list. Practice the follow-up too.

## Must-know topics

| Topic | Questions |
|---|---|
| Transformer and self-attention | 1-2 |
| KV cache and inference cost | 3 |
| Tokenization and context window | 6-7 |
| RAG end to end | 26 |
| Chunking, hybrid search, re-ranking | 27-29 |
| RAG evaluation | 31 |
| Agents, ReAct and MCP | 41-43 |
| Prompt injection | 21 |
| LoRA / QLoRA and quantization | 10-11 |
| LLM-as-judge | 63 |
| Caching and model routing | 79-80 |
| Cost and latency levers | 84-85 |

## Contents

1. [LLM Fundamentals](#llm-fundamentals) (1-15)
2. [Prompting and Structured Output](#prompting-and-structured-output) (16-25)
3. [RAG and Retrieval](#rag-and-retrieval) (26-40)
4. [Agents, Tool Use and MCP](#agents-tool-use-and-mcp) (41-52)
5. [Fine-Tuning and Model Adaptation](#fine-tuning-and-model-adaptation) (53-60)
6. [Evaluation](#evaluation) (61-70)
7. [AI System Design](#ai-system-design) (71-82)
8. [Production, Cost and Safety](#production-cost-and-safety) (83-92)
9. [Coding](#coding) (93-100)
10. [Sources and further reading](#sources-and-further-reading)

## LLM Fundamentals

### 1. Explain the transformer architecture at a high level. `Entry`

A transformer is a stack of identical blocks. Each block has (1) multi-head self-attention, which lets every token mix information from other tokens, and (2) a position-wise feed-forward network (MLP). Residual connections and layer normalization wrap both sub-layers so deep stacks train stably. Most modern LLMs are decoder-only: causal masking means each token attends only to earlier tokens, and the model is trained to predict the next token. Position information comes from positional encodings, today usually rotary embeddings (RoPE).

> **Likely follow-up:** Why do most LLMs use decoder-only instead of encoder-decoder? (One stack, one objective, scales simply and handles generation natively.)

### 2. What is self-attention and why does it matter? `Entry`

Each token is projected into a query, key and value. Attention weights are softmax(QK^T / sqrt(d_k)), and the output is the weighted sum of values. It lets any token pull information from any other token in one step, so long-range dependencies do not have to pass through a recurrent bottleneck, and the whole sequence is processed in parallel during training. The cost is O(n^2) in sequence length for compute and for the attention matrix.

> **Likely follow-up:** Why divide by sqrt(d_k)? Without it, dot products grow with dimension, the softmax saturates and gradients vanish.

### 3. Explain the KV cache and why it matters for inference. `Mid`

During autoregressive decoding, the keys and values of earlier tokens do not change, so they are stored and reused; each new token computes only its own Q, K, V. This turns per-step attention from recomputing the whole prefix into one pass over cached tensors. The trade-off is memory: per sequence it is roughly 2 x layers x kv_heads x head_dim x tokens x bytes per value, and it often limits batch size and context length more than the weights do. Grouped-query attention, KV quantization and paged allocation (as in vLLM's PagedAttention) exist to shrink or pack it.

> **Likely follow-up:** Estimate KV-cache memory for a 32-layer model, 8 KV heads, head_dim 128, 8k tokens, fp16: 2x32x8x128x8192x2 bytes, about 1 GiB per sequence.

### 4. Compare pre-training, instruction tuning and preference tuning (RLHF/DPO). `Mid`

Pre-training: next-token prediction on trillions of tokens; gives knowledge and fluency but not helpful behavior. Instruction tuning (SFT): supervised training on prompt-response pairs so the model follows instructions and a chat format. Preference tuning: trains on comparisons of better vs worse answers. RLHF fits a reward model and optimizes the policy with RL (e.g. PPO) under a KL penalty to the SFT model; DPO skips the reward model and optimizes directly on preference pairs, which is simpler and more stable. Each stage uses far less data than the one before.

> **Likely follow-up:** When would you pick DPO over PPO-style RLHF? (Smaller team, offline preference data, want stability; PPO when you need online exploration or a reusable reward model.)

### 5. What do scaling laws say, and how do they change decisions? `Senior`

Loss falls as a smooth power law in parameters, data and compute (Kaplan et al., 2020). The Chinchilla work (Hoffmann et al., 2022) showed that for a fixed training budget, parameters and tokens should grow roughly together, around 20 training tokens per parameter, so many earlier models were undertrained. In practice teams now often train smaller models on far more tokens than compute-optimal because inference cost, not training cost, dominates over the model's life.

> **Likely follow-up:** Why would you deliberately train past the compute-optimal point? (Cheaper serving for a model that will answer billions of requests.)

### 6. What is tokenization and why does it matter? `Entry`

Text is split into subword units by algorithms such as BPE or unigram (SentencePiece). It matters because cost, latency and context limits are counted in tokens; token count per word varies by language (many non-English languages need more tokens for the same content); and tokenization explains odd failures such as weak character counting, arithmetic on long numbers and sensitivity to leading spaces.

> **Likely follow-up:** Why can an LLM fail to count the letters in a word? (It sees tokens, not characters.)

### 7. What is the context window and how does it affect system design? `Entry`

It is the maximum number of tokens (prompt plus output) the model can attend to. Larger windows allow whole documents in the prompt but increase cost and latency, and models use information unevenly across long inputs (relevant facts in the middle are used less reliably). Design still needs retrieval, summarization or memory to choose what goes in, plus a token budget per section (system, history, retrieved context, output).

### 8. What do temperature and top-p do, and how do you choose them? `Entry`

Temperature rescales logits before softmax: low values make output near-deterministic, high values flatten the distribution. Top-p (nucleus) sampling keeps only the smallest set of tokens whose cumulative probability reaches p. Use low temperature (0 to 0.3) for extraction, classification and code; moderate (0.7 to 1.0) for brainstorming or creative text. Even at temperature 0, outputs can vary slightly across runs because of batching and floating-point effects, so do not rely on it for strict determinism.

### 9. Fine-tuning vs in-context learning: what is the difference? `Mid`

In-context learning puts instructions and examples in the prompt; the weights do not change, iteration is instant, but every request pays for the extra tokens and behavior is bounded by the window. Fine-tuning changes the weights with training examples; it is good for consistent format, tone, a narrow task or making a smaller model as good as a bigger prompted one, but it needs data, evaluation and redeployment, and it is a poor way to add frequently changing facts (use retrieval for that).

### 10. What is quantization and why is it important for deployment? `Mid`

Storing weights (and sometimes activations or the KV cache) in fewer bits, e.g. 8-bit or 4-bit integers instead of 16-bit floats. It cuts memory roughly 2x to 4x and often raises throughput because decoding is memory-bandwidth bound. Post-training methods such as GPTQ and AWQ keep quality loss small at 4-bit for many models, but you must re-run your task evals because degradation is uneven (math, code and long context tend to suffer first).

### 11. Explain LoRA and QLoRA. `Mid`

LoRA freezes the base weights and learns a low-rank update for selected matrices: W + BA, where A and B have small rank r (often 8 to 64). Trainable parameters drop by orders of magnitude, adapters are small files, and several adapters can share one base model. QLoRA (Dettmers et al., 2023) keeps the frozen base in 4-bit and trains LoRA adapters on top, making fine-tuning of large models feasible on a single GPU.

> **Likely follow-up:** Which layers do you apply LoRA to? (Attention projections at minimum; adding MLP layers usually helps quality at more cost.)

### 12. Explain Mixture of Experts and its trade-offs. `Senior`

An MoE layer replaces one feed-forward block with many experts plus a router that sends each token to the top-k experts (often k = 2). Total parameters are large but active parameters per token are small, so quality per training FLOP improves. Costs: all experts must still sit in memory, routing needs load-balancing losses, expert parallelism adds communication, and batching is less efficient at low traffic.

### 13. How do reasoning models differ from standard chat models? `Mid`

Reasoning models are trained, typically with reinforcement learning on verifiable tasks, to produce a long internal chain of thought before the final answer, and they spend more inference-time compute per query. They are stronger on math, code and multi-step planning but slower and more expensive, and often worse value for simple lookups or style tasks. In a product, route only hard queries to them and set a reasoning budget.

### 14. Why do LLMs hallucinate, and how do you reduce it? `Mid`

The model is trained to produce plausible continuations, not to verify facts, and it has no built-in signal for what it does not know. Reduce it by grounding answers in retrieved sources and asking for citations, allowing and rewarding an "I don't know" path, constraining outputs (schemas, enumerations), lowering temperature for factual tasks, and checking claims afterwards against the sources with an automated verifier.

### 15. What is the difference between an embedding model and a generative model? `Entry`

An embedding model maps text to a fixed-length vector so that similar meanings are close in vector space; it is used for search, clustering, deduplication and classification. A generative model produces tokens. Embedding calls are far cheaper and are the backbone of retrieval; the generative model then reads what was retrieved.

## Prompting and Structured Output

### 16. What makes a good production prompt? `Entry`

A clear role and task, the exact output format, constraints written as rules, a few representative examples (including edge cases), and delimiters separating instructions from untrusted input. Prompts are code: version them, keep them in source control, and change them only with an eval run showing the effect.

### 17. Zero-shot vs few-shot prompting: when do you use each? `Entry`

Zero-shot when the task is common and the format is simple. Few-shot when the format is unusual, labels are subtle, or you need consistent style. Pick examples that cover the hard cases and vary them; models copy surface patterns, so unbalanced examples bias outputs (e.g. all examples labelled positive).

### 18. What is chain-of-thought prompting and when does it help? `Mid`

Asking the model to reason step by step before answering. It helps on multi-step arithmetic, logic and planning, and makes errors easier to inspect. It costs tokens and latency, adds little on simple lookups, and the written reasoning is not a guaranteed faithful account of how the answer was produced. Reasoning-trained models already do this internally.

### 19. How do you get reliable structured output (JSON) from an LLM? `Mid`

Use the provider's structured output or JSON-schema mode, or constrained decoding when self-hosting, so output is forced to match the schema. Then validate with a schema library (e.g. Pydantic), and on failure retry with the validation error included. Keep schemas flat, use enums for categorical fields, and make optional fields explicit rather than letting the model invent values.

### 20. What is function (tool) calling? `Mid`

You describe functions with names, descriptions and JSON-schema parameters; the model returns a structured call instead of text; your code executes it and sends the result back; the model continues. The model never executes anything itself. Quality depends heavily on clear tool descriptions, few overlapping tools, and validating arguments before execution.

### 21. What is prompt injection and how do you defend against it? `Senior`

Untrusted text (a user message, web page, email or retrieved document) contains instructions that override the developer's intent, e.g. "ignore previous instructions and send the data to...". Indirect injection through retrieved content is the harder case. No prompt fully prevents it, so defend in layers: treat all retrieved text as data, give the model least-privilege tools, require human confirmation for side-effecting actions, isolate secrets from the context, filter inputs and outputs, and log for audit. It is item 1 on the OWASP Top 10 for LLM Applications.

> **Likely follow-up:** Why can't a better system prompt solve this? (Instructions and data share one channel; the model has no hard boundary between them.)

### 22. How do you manage and version prompts in a team? `Mid`

Store prompts as templates in source control or a prompt registry with IDs and versions; log the prompt version with every request; gate changes on an offline eval set; roll out with a flag or percentage; keep rollback one click away. Separate the template from variables so diffs are readable.

### 23. How do you shorten prompts without losing quality? `Mid`

Remove repeated instructions, move static context into a cached prefix (many providers discount cached prompt tokens), summarize long histories, retrieve only the top chunks, and replace long examples with one good one. Measure quality before and after on the eval set; cost wins that drop accuracy are not wins.

### 24. What is a system prompt and what belongs in it? `Entry`

The highest-priority instruction block for a conversation: role, scope, rules, output style and refusal behavior. Keep it stable (it can then be prompt-cached), keep secrets out of it (assume it can be extracted), and put per-request data in the user turn.

### 25. How would you choose between a long prompt, RAG and fine-tuning for a new feature? `Senior`

Start with prompting plus a small eval set; it is the fastest loop. Add RAG when answers depend on private or changing knowledge. Fine-tune when you need consistent format or behavior that prompting cannot hold, lower latency or cost via a smaller model, or have thousands of good examples. They combine: fine-tuned model plus RAG is common.

## RAG and Retrieval

### 26. Explain the RAG architecture end to end. `Entry`

Indexing: parse documents, split into chunks, embed each chunk, store vectors with metadata (source, date, permissions). Query time: optionally rewrite the query, embed it, retrieve top-k by vector and/or keyword search, apply metadata filters, re-rank, then put the best chunks in the prompt with instructions to answer only from them and cite sources. Evaluate retrieval and generation separately.

> **Likely follow-up:** Where does RAG usually fail first? (Retrieval: wrong chunk or missing chunk, not the generator.)

### 27. How do you choose a chunking strategy? `Mid`

Follow document structure (headings, paragraphs, code blocks, table rows) rather than fixed character counts; typical chunk sizes are a few hundred tokens with modest overlap. Small chunks give precise matches but lose context; large chunks keep context but dilute similarity and cost more tokens. A common fix is to retrieve small chunks and pass their parent section to the model. Choose by measuring recall on real questions, not by default settings.

### 28. What is hybrid search and when should you use it? `Mid`

Combining lexical search (BM25) with dense vector search, then merging results, often with reciprocal rank fusion. Use it when queries contain exact identifiers, product codes, names, error messages or rare terms that embeddings blur. It is a sensible default for enterprise search.

### 29. How does re-ranking work and why use it? `Mid`

Retrieve a wide candidate set cheaply (e.g. top 50), then score each query-document pair with a cross-encoder or LLM that reads both together, and keep the top 5 to 10. Cross-encoders are more accurate than comparing two independently computed embeddings but too slow to run over the whole corpus, so they are used only on candidates.

### 30. What is the "lost in the middle" problem? `Senior`

Liu et al. (2023) found that models use relevant information placed at the start or end of a long context more reliably than information in the middle. Mitigations: retrieve fewer, better chunks; put the most relevant first; re-rank; and test long-context behavior on your own tasks rather than trusting the advertised window.

### 31. How do you evaluate a RAG system? `Senior`

Separately. Retrieval: recall@k, precision@k, MRR or nDCG against labelled question-to-source pairs. Generation: faithfulness (claims supported by retrieved context), answer relevance, correctness against a reference, and citation accuracy. Build a golden set from real user questions, use an LLM judge calibrated against human labels, and track latency and cost per answer.

### 32. How do you keep a RAG index fresh when documents change? `Mid`

Incremental ingestion keyed by document ID and content hash; re-embed only changed chunks; delete chunks of removed documents (stale chunks are a common source of wrong answers); store timestamps and versions as metadata and filter or boost by recency. Re-embed everything when you change the embedding model, because vectors from different models are not comparable.

### 33. How should a RAG system decide to say "I don't know"? `Mid`

Combine signals: low retrieval scores or re-ranker scores below a calibrated threshold, no chunk that answers the question, and a verifier step that checks the draft answer against sources. Instruct the model explicitly that declining is acceptable and evaluate refusal precision as well as answer accuracy.

### 34. How do you choose an embedding model? `Mid`

Benchmark candidates on your own query-document pairs (public leaderboards such as MTEB are a starting point only). Consider language coverage, domain fit, max input length, dimension (storage and speed), cost or hosting, and whether it supports asymmetric query/document modes. Record the model version with the index.

### 35. Compare common vector store options. `Entry`

Postgres with pgvector: simplest if you already run Postgres, good to millions of vectors. Managed vector databases (e.g. Pinecone): little operations work, pay per usage. Self-hosted engines (e.g. Qdrant, Weaviate, Milvus): more control, filtering and scale. Search engines (Elasticsearch, OpenSearch) suit hybrid lexical plus vector. Pick on filtering needs, scale, latency, operations capacity and cost, not on hype.

### 36. What are HNSW and IVF indexes, and what trade-offs do they make? `Senior`

Both are approximate nearest-neighbor indexes. HNSW builds a layered proximity graph: high recall and low latency but high memory and slower builds. IVF clusters vectors and searches only the nearest clusters: lower memory, tunable via the number of probes, often combined with product quantization. You trade recall for speed and memory; measure recall@k against exact search on a sample.

### 37. What is query transformation and why does it help? `Mid`

Rewriting the user query before retrieval: resolving pronouns from chat history, expanding acronyms, splitting a multi-part question into sub-queries, or generating a hypothetical answer and embedding that (HyDE). It helps when user phrasing differs from document phrasing; it adds a model call, so measure whether recall gain justifies the latency.

### 38. How do you enforce access control in RAG? `Senior`

Store permission metadata (tenant, groups, document ACL) on every chunk at ingestion and filter at query time inside the retrieval call, before anything reaches the model. Never rely on the prompt to hide documents. Keep ACLs in sync with the source system and test with users who should and should not see each document.

### 39. What is agentic RAG? `Mid`

Instead of one retrieve-then-generate pass, the model decides when and what to search, can issue several queries, read results, and search again before answering. It handles multi-hop questions better but costs more and is harder to evaluate; cap the number of steps and log each retrieval.

### 40. How do you debug poor RAG answer quality? `Senior`

Trace a failing question: was the right document ingested and parsed correctly, was it chunked sensibly, did it appear in the top-k, was it ranked high enough, was it included in the prompt, and did the model use it? Fix the earliest failing stage. Most issues are parsing, chunking or retrieval, not the generator.

## Agents, Tool Use and MCP

### 41. What is an AI agent, and how is it different from a chain? `Entry`

A chain is a fixed sequence of steps defined by the developer. An agent is a loop where the model chooses the next action (which tool to call, with what arguments) based on observations, until it decides the task is done. Agents handle open-ended tasks but are less predictable, so use a fixed workflow when the steps are known.

### 42. Explain the ReAct pattern. `Mid`

Reason + Act (Yao et al., 2022): the model alternates between a reasoning step, a tool call, and reading the observation, repeating until it can answer. It grounds reasoning in real tool results. In production you add step limits, structured tool calls instead of parsed text, and error handling for failed tools.

### 43. What is the Model Context Protocol (MCP)? `Mid`

An open protocol, introduced in late 2024, that standardizes how applications expose tools, resources and prompts to LLM clients. A server describes its tools once and any MCP-compatible client can use them, instead of a custom integration per app and per model. Security still matters: servers run with real permissions, so authenticate them, scope their access and review what they expose.

> **Likely follow-up:** How is MCP different from plain function calling? (Function calling is the model-side format; MCP is the client-server protocol for discovering and invoking tools across apps.)

### 44. How do you design good tools for an agent? `Mid`

Few tools with distinct purposes, clear names and descriptions written for the model, strict typed parameters, informative error messages the model can act on, and outputs trimmed to what is needed. Make side-effecting tools idempotent where possible and separate read tools from write tools so permissions can differ.

### 45. How do you make agents reliable in production? `Senior`

Bound them: max steps, timeouts and budget per task; validate every tool argument; retry transient errors with backoff; checkpoint state so long tasks can resume; require human approval for irreversible actions; and log full traces. Evaluate on task-completion suites with realistic tool failures, not only on happy paths.

### 46. How do you handle memory in agents? `Mid`

Short-term: the running conversation and scratchpad, trimmed or summarized to fit the window. Long-term: facts or past episodes stored externally (database or vector store) and retrieved when relevant. Write to long-term memory deliberately (what is worth keeping), and let users see or delete stored memories for privacy.

### 47. Single agent vs multi-agent systems: when is multi-agent worth it? `Senior`

Multi-agent setups (planner plus workers, or specialist agents) help when sub-tasks are separable, need different tools or prompts, or can run in parallel. They add cost, latency and coordination failures. Start with one agent and good tools; split only when evals show a single agent cannot hold the task.

### 48. What guardrails do agents need? `Mid`

Input and output filtering, allow-lists of tools per user role, argument validation, rate and spend limits, sandboxed code execution, human confirmation for actions such as payments, emails or deletes, and treating every tool output as untrusted input (it may contain injected instructions).

### 49. How do you evaluate an agent? `Mid`

Task success rate on a fixed suite of realistic tasks with checkable end states, plus step count, cost, latency and error recovery. Inspect trajectories, not only outcomes: a correct final answer reached through a risky tool call is still a failure. Re-run the suite on every model or prompt change.

### 50. What is planning in an agent and why can it fail? `Entry`

Breaking a goal into steps before or during execution. It fails when the plan is made without enough information, when the agent does not revise the plan after a failed step, or when errors compound over many steps. Re-planning after each observation and short plans with checkpoints reduce this.

### 51. How do you run model-generated code safely? `Senior`

Execute it in an isolated sandbox (container or microVM) with no secrets, restricted network, CPU, memory and time limits, a read-only or scratch filesystem, and resource cleanup after the run. Return only stdout, stderr and declared artifacts to the model.

### 52. Workflows vs agents: how do you decide? `Mid`

If you can draw the flowchart, build a workflow (deterministic steps with model calls inside); it is cheaper, testable and predictable. Use an agent when the path depends on intermediate results you cannot enumerate. Many good systems are workflows with one agentic step.

---

**[Get the full playbook: frameworks, system-design walkthroughs, 8-week plan ($19.99)](https://sirjohnnymai.gumroad.com/l/ai-engineer-interview-playbook?utm_source=github&utm_medium=qbank&utm_campaign=aie_qbank_20261101&utm_content=readme_mid)**

---

## Fine-Tuning and Model Adaptation

### 53. When should you fine-tune instead of prompting or RAG? `Mid`

When you need consistent format or style, a narrow task at lower cost or latency with a smaller model, domain language the base model handles poorly, or behavior that long prompts cannot hold. Not for adding facts that change; use retrieval for those.

### 54. How do you build a fine-tuning dataset? `Mid`

Collect real inputs, write or curate high-quality target outputs, deduplicate, remove PII, balance across task types and edge cases, and hold out a test set before training. Quality beats volume: a few thousand clean examples often outperform a large noisy set. Version the dataset with the model.

### 55. What is catastrophic forgetting and how do you limit it? `Senior`

Fine-tuning on a narrow set can degrade general abilities the base model had. Limit it with parameter-efficient methods (LoRA), lower learning rates and fewer epochs, mixing in general instruction data, and evaluating on general benchmarks as well as the target task.

### 56. What is model distillation and when would you use it? `Mid`

Training a smaller student model to imitate a larger teacher, using the teacher's outputs (or probabilities) on many inputs. Use it to cut latency and cost for a well-defined task after you have proven quality with the large model. Check the provider's terms before training on another model's outputs.

### 57. Explain DPO in one minute. `Senior`

Direct Preference Optimization (Rafailov et al., 2023) trains on pairs of chosen and rejected responses with a classification-style loss that increases the likelihood of the chosen response relative to a frozen reference model. It reaches results similar to RLHF without training a separate reward model or running RL, so it is simpler and more stable.

### 58. How do you evaluate a fine-tuned model before shipping? `Mid`

Compare against the base model and the prompted baseline on a held-out set of the target task, a general-capability set to catch regressions, safety tests, and side-by-side human or LLM-judge review. Ship only if it wins on the target metric without unacceptable regressions, and canary it with monitoring.

### 59. What hyperparameters matter most in LoRA fine-tuning? `Entry`

Learning rate, number of epochs, rank r and alpha (scaling), which modules get adapters, batch size and sequence length. Overfitting usually shows as falling training loss with flat or rising validation loss; stop early and keep the best checkpoint.

### 60. What is synthetic data and what are its risks? `Senior`

Training examples generated by models, used to expand coverage or create preference pairs. Risks: copying the generator's errors and style, low diversity, contamination of your eval set, and degradation when models train repeatedly on model-generated data ("model collapse", Shumailov et al.). Mitigate with filtering, human spot checks, mixing in real data and strict eval separation.

## Evaluation

### 61. Why is evaluating LLM applications hard? `Entry`

Outputs are open-ended, many answers can be correct, quality has several dimensions (correctness, faithfulness, tone, safety), and small prompt or model changes shift behavior unpredictably. That is why teams build task-specific eval sets instead of relying on public benchmarks.

### 62. How do you build an eval set? `Mid`

Start from real or realistic inputs, cover common cases, edge cases and known failures, write expected outputs or grading criteria for each, and keep it versioned. Start with 50 to 200 examples and grow it from production failures. Keep a held-out portion that is never used for prompt tuning.

### 63. How do you make LLM-as-judge reliable? `Senior`

Give the judge a precise rubric and, where possible, a reference answer; ask for a short justification before the score; use pairwise comparison for subjective quality; swap answer order to control position bias; watch for length and self-preference bias; and calibrate against human labels, reporting agreement. Re-check calibration when the judge model changes.

### 64. Offline vs online evaluation: what is the difference? `Mid`

Offline: run a fixed eval set before release to catch regressions. Online: measure live behavior through A/B tests, user feedback, task completion, escalation rates and sampled reviews. Both are needed: offline gates releases, online tells you whether users are actually better off.

### 65. How do you A/B test an AI feature? `Mid`

Randomize users (not requests) to variants, define a primary metric tied to user value (task success, retention, resolution rate) plus guardrail metrics (latency, cost, complaints), size the test for the effect you care about, and watch for novelty effects. Keep model, prompt and retrieval changes separable so you know what caused the result.

### 66. What metrics do you track for a production LLM feature? `Entry`

Quality (eval scores, user ratings, task success), safety (policy violations, refusals), latency (time to first token, total time at p50/p95/p99), cost (tokens and dollars per request), reliability (error, timeout and retry rates) and usage. Slice them by user segment and model version.

### 67. What is benchmark contamination and why does it matter? `Senior`

Test questions from a benchmark leaking into training data, which inflates scores without real capability. It is why public leaderboard results may not predict performance on your task. Use private, recently written eval sets and check for overlap when you fine-tune.

### 68. How do you evaluate hallucination or faithfulness? `Mid`

Break the answer into individual claims and check each against the provided sources (with an NLI model or an LLM judge), then report the share of supported claims. Pair it with citation checks: does the cited passage actually contain the claim?

### 69. What is regression testing for prompts and models? `Mid`

Running the eval suite automatically in CI on every prompt, model or retrieval change and blocking the change if key metrics drop beyond a threshold. It turns prompt changes into reviewed code changes.

### 70. How do you choose between two models for a feature? `Senior`

Run both on your eval set and compare quality, then latency at your expected load, cost per successful task (not per token), context and tooling needs, data and compliance terms, and reliability of the provider. Often a cheaper model plus routing for hard cases wins.

## AI System Design

### 71. Design a customer-support assistant for a SaaS company. `Senior`

Clarify scope (answer questions, take actions, or both), channels, volume and escalation rules. Components: RAG over help docs and past tickets with permission filters; account tools with read-only defaults and confirmation for changes; conversation memory; intent routing to a cheap model for simple questions; human handoff with full context; evals on resolution accuracy; monitoring of escalation and satisfaction. Discuss failure modes: stale docs, prompt injection through tickets, and wrong refunds.

### 72. Design an evaluation pipeline for an LLM product. `Senior`

Versioned eval datasets, a runner that executes prompts/models in parallel with caching, graders (exact match, programmatic checks, calibrated LLM judges, human review queues), result storage per run, dashboards with diffs against the baseline, and CI gates. Feed production failures back into the dataset.

### 73. Design a model-serving platform. `Mid`

API gateway with auth, quotas and routing; model servers with continuous batching and paged KV cache (e.g. vLLM or TGI); autoscaling on queue depth and GPU utilization; streaming responses; per-tenant rate limits; health checks and fallbacks to another model or provider; and metrics for time to first token, tokens per second and cost.

### 74. Design a document-processing (extraction) pipeline. `Mid`

Ingest, then OCR or layout parsing, classify document type, extract fields with schema-constrained output, validate (types, cross-field rules, totals), score confidence, send low-confidence items to human review, and store with lineage back to the page. Measure field-level accuracy per document type.

### 75. Design an LLM gateway for a company. `Senior`

One internal endpoint in front of all providers: authentication, per-team keys and budgets, model routing and fallback, prompt and response logging with PII redaction, caching, rate limiting, usage and cost reporting, and policy enforcement. It gives central control and lets teams switch models without code changes.

### 76. Design a semantic search engine. `Mid`

Ingestion and chunking, embeddings, an ANN index with metadata filters, hybrid lexical plus vector retrieval, re-ranking, snippets and highlighting, query understanding (spelling, synonyms), and click and relevance feedback for tuning. Evaluate with nDCG on labelled queries.

### 77. Design a real-time content moderation system. `Senior`

Layered: fast rules and hashes for known bad content, a small classifier for most traffic, and an LLM or human review for ambiguous cases; policy defined as labeled categories; latency budget per layer; appeals flow; and monitoring of precision and recall per category and language. Bias and over-blocking are as important as misses.

### 78. How do you architect a multi-tenant AI platform? `Senior`

Isolate tenant data at storage and retrieval (tenant ID filters enforced server-side, separate indexes for high-sensitivity tenants), per-tenant keys, quotas and cost tracking, per-tenant prompt or adapter configuration, noisy-neighbor protection, and audit logs. Never let one tenant's data enter another's prompt or cache.

### 79. How do you design caching for LLM applications? `Mid`

Exact-match response cache for repeated identical requests; provider prompt caching for long shared prefixes; semantic cache (embedding similarity above a strict threshold) for near-duplicate questions where answers do not depend on the user; embedding cache during ingestion. Include model and prompt versions in cache keys and set TTLs so answers do not go stale.

### 80. How do you route queries across multiple models? `Senior`

Classify each request by difficulty, task type or required capability (a rules layer or a small classifier), send easy requests to a cheap fast model and hard ones to a stronger model, and escalate when a verifier or confidence check fails. Measure quality and cost per route.

### 81. How do you migrate a product from one model to another? `Mid`

Run both on the eval set, adjust prompts for the new model, shadow-test on live traffic, compare quality, latency and cost, roll out gradually behind a flag with rollback, and keep monitoring. Re-embed if the embedding model changes.

### 82. Design a code-assistant feature for an IDE. `Senior`

Context gathering (current file, related files via retrieval over the repo, recent edits), a low-latency model for inline completion and a stronger one for chat or multi-file edits, streaming, a sandbox for running tests, and acceptance-rate and edit-survival metrics. Respect repository permissions and keep secrets out of prompts.

## Production, Cost and Safety

### 83. How do you monitor an LLM system in production? `Entry`

Log each request with prompt version, model, tokens, latency, cost and outcome; trace multi-step calls; dashboards and alerts on error rate, p95 latency, cost spikes and quality signals; sample conversations for review; and track user feedback. Redact PII in logs.

### 84. How do you reduce LLM inference cost? `Mid`

Route easy requests to smaller models, shorten prompts, use prompt caching for shared prefixes, cache responses, cap output length, batch offline work (batch APIs are usually discounted), and for self-hosting use quantization and continuous batching. Track cost per successful task.

### 85. How do you reduce latency? `Mid`

Stream tokens, choose smaller or faster models for the first response, cut prompt length, parallelize retrieval and tool calls, cache, place servers near users, and use speculative decoding when self-hosting. Measure time to first token and total time separately.

### 86. How do you handle provider rate limits and outages? `Entry`

Retry transient errors with exponential backoff and jitter, respect retry-after headers, queue non-urgent work, spread load across keys or regions where allowed, and fail over to a secondary model or provider with a tested prompt.

### 87. How do you handle PII in AI systems? `Mid`

Minimize what is sent, detect and redact or tokenize PII before prompts and logs, check provider data-retention and training terms, encrypt at rest and in transit, apply retention limits, and support deletion requests. Test redaction recall; missed PII in logs is a common leak.

### 88. What is model or data drift, and how do you detect it? `Mid`

The input distribution, user behavior or the provider model itself changes, and quality shifts. Detect it by monitoring input statistics and topics, eval scores on sampled traffic, user feedback and outcome metrics over time, and by pinning model versions so upgrades are deliberate.

### 89. What does red-teaming an AI system involve? `Senior`

Deliberately attacking the system before release: jailbreaks, prompt injection through every input channel, data exfiltration, harmful content, tool misuse and bias. Use a threat model, both automated attack generation and human testers, record findings with severity, fix, and turn findings into regression tests.

### 90. What are guardrails, and where do they sit? `Mid`

Checks around the model: input checks (policy, injection signals, PII), output checks (policy, schema, groundedness, sensitive data), and action checks (tool permissions, confirmations). Keep them independent of the main prompt so one failure does not disable all protection, and measure their false positive rate.

### 91. How do you measure and reduce bias in an LLM feature? `Senior`

Define the harms relevant to your use case, build test sets that vary protected attributes while holding the task constant, compare outcomes and error rates across groups, and review qualitatively. Reduce with better data, prompt and policy changes, and human review for high-stakes decisions.

### 92. How do you deploy prompt or model changes safely? `Mid`

Treat them like code: review, offline evals in CI, feature flags, canary or percentage rollout with automated rollback on metric drops, and versioned configs so any response can be traced to the exact prompt and model.

## Coding

### 93. Implement retry with exponential backoff for an LLM API call. `Entry`

Retry only transient failures (429, 5xx, timeouts), not 4xx validation errors. Wait base * 2^attempt plus random jitter, honor Retry-After, cap attempts and total time.

```python
import random, time
def call_with_retry(fn, max_attempts=5, base=0.5, cap=20):
    for attempt in range(max_attempts):
        try:
            return fn()
        except TransientError as e:
            if attempt == max_attempts - 1:
                raise
            wait = getattr(e, 'retry_after', None) or min(cap, base * 2 ** attempt)
            time.sleep(wait + random.uniform(0, wait / 2))
```

### 94. Write a structure-aware text chunker. `Entry`

Split on headings and blank lines first, then pack paragraphs into chunks up to a token budget, with a small overlap, and never split inside code blocks.

```python
def chunk(paragraphs, max_tokens=400, overlap=1, count=len):
    chunks, cur = [], []
    for p in paragraphs:
        if cur and sum(map(count, cur)) + count(p) > max_tokens:
            chunks.append('\n\n'.join(cur))
            cur = cur[-overlap:] if overlap else []
        cur.append(p)
    if cur:
        chunks.append('\n\n'.join(cur))
    return chunks
```

Pass a real tokenizer's length function as count; len counts characters.

### 95. Implement hybrid search with reciprocal rank fusion. `Mid`

Run BM25 and vector search separately, then fuse by rank, which avoids normalizing incompatible scores.

```python
def rrf(rankings, k=60):
    scores = {}
    for ranked_ids in rankings:
        for rank, doc_id in enumerate(ranked_ids):
            scores[doc_id] = scores.get(doc_id, 0) + 1 / (k + rank + 1)
    return sorted(scores, key=scores.get, reverse=True)
```

```python
fused = rrf([bm25_ids, vector_ids])[:20]  # then re-rank
```

### 96. Parse and validate structured output from an LLM, with a repair retry. `Mid`

```python
from pydantic import BaseModel, ValidationError
class Invoice(BaseModel):
    vendor: str
    total: float
    currency: str
```

```python
def extract(llm, text, retries=2):
    prompt = f'Return JSON for Invoice from:\n{text}'
    for _ in range(retries + 1):
        raw = llm(prompt)
        try:
            return Invoice.model_validate_json(raw)
        except ValidationError as e:
            prompt += f'\nYour last output was invalid: {e}. Return only valid JSON.'
    raise ValueError('could not parse')
```

Prefer the provider's schema mode when available; keep this as the safety net.

### 97. Implement a token-bucket rate limiter for LLM calls. `Mid`

Limit both requests and tokens per minute, because providers enforce both.

```python
import time, threading
class TokenBucket:
    def __init__(self, rate_per_sec, capacity):
        self.rate, self.cap = rate_per_sec, capacity
        self.tokens, self.t = capacity, time.monotonic()
        self.lock = threading.Lock()
    def acquire(self, n=1):
        while True:
            with self.lock:
                now = time.monotonic()
                self.tokens = min(self.cap, self.tokens + (now - self.t) * self.rate)
                self.t = now
                if self.tokens >= n:
                    self.tokens -= n
                    return
                wait = (n - self.tokens) / self.rate
            time.sleep(wait)
```

### 98. Implement a minimal agent loop with tool calls and a step limit. `Mid`

```python
def run_agent(llm, tools, task, max_steps=8):
    messages = [{'role': 'user', 'content': task}]
    for _ in range(max_steps):
        reply = llm(messages, tools=list(tools))
        messages.append(reply)
        if not reply.get('tool_calls'):
            return reply['content']
        for call in reply['tool_calls']:
            fn = tools.get(call['name'])
            try:
                result = fn(**call['args']) if fn else f'unknown tool {call["name"]}'
            except Exception as e:
                result = f'error: {e}'
            messages.append({'role': 'tool', 'id': call['id'], 'content': str(result)})
    return 'stopped: step limit reached'
```

In production add argument validation, budgets, checkpointing and approval for side-effecting tools.

### 99. Implement a conversation-history manager that fits a token budget. `Senior`

Always keep the system prompt and the latest user turn; add earlier turns newest-first until the budget is reached; summarize what was dropped into one message.

```python
def fit_history(system, turns, budget, count, summarize):
    kept, used = [], count(system) + count(turns[-1])
    for t in reversed(turns[:-1]):
        if used + count(t) > budget * 0.8:
            break
        kept.insert(0, t); used += count(t)
    dropped = turns[:len(turns) - 1 - len(kept)]
    summary = [summarize(dropped)] if dropped else []
    return [system] + summary + kept + [turns[-1]]
```

### 100. Write a small eval harness that compares two prompt versions. `Senior`

```python
def evaluate(cases, run, graders):
    rows = []
    for c in cases:
        out = run(c['input'])
        rows.append({'id': c['id'], **{g.__name__: g(out, c) for g in graders}})
    return rows
```

```python
def compare(cases, run_a, run_b, graders):
    a, b = evaluate(cases, run_a, graders), evaluate(cases, run_b, graders)
    for g in graders:
        n = g.__name__
        print(n, sum(r[n] for r in a) / len(a), sum(r[n] for r in b) / len(b))
    return a, b
```

Graders return 0 or 1 (exact match, schema valid, judge pass). Report per-case diffs so regressions are visible, and fix the random seed or temperature for repeatability.

## Sources and further reading

- [Attention Is All You Need (Vaswani et al., 2017)](https://arxiv.org/abs/1706.03762)
- [Scaling Laws for Neural Language Models (Kaplan et al., 2020)](https://arxiv.org/abs/2001.08361)
- [Training Compute-Optimal LLMs, Chinchilla (Hoffmann et al., 2022)](https://arxiv.org/abs/2203.15556)
- [Retrieval-Augmented Generation (Lewis et al., 2020)](https://arxiv.org/abs/2005.11401)
- [Lost in the Middle (Liu et al., 2023)](https://arxiv.org/abs/2307.03172)
- [LoRA (Hu et al., 2021)](https://arxiv.org/abs/2106.09685)
- [QLoRA (Dettmers et al., 2023)](https://arxiv.org/abs/2305.14314)
- [Direct Preference Optimization (Rafailov et al., 2023)](https://arxiv.org/abs/2305.18290)
- [ReAct (Yao et al., 2022)](https://arxiv.org/abs/2210.03629)
- [PagedAttention / vLLM (Kwon et al., 2023)](https://arxiv.org/abs/2309.06180)
- [Model Context Protocol specification](https://modelcontextprotocol.io)
- [OWASP Top 10 for LLM Applications](https://genai.owasp.org/llm-top-10/)

---

**[The 0 to 1 AI Engineer Interview Playbook ($19.99, instant PDF)](https://sirjohnnymai.gumroad.com/l/ai-engineer-interview-playbook?utm_source=github&utm_medium=qbank&utm_campaign=aie_qbank_20261101&utm_content=readme_bottom)** · [Paperback/Kindle](https://valenx.org/books/aie?utm_source=github&utm_medium=readme&utm_content=ai-engineer-interview-questions_L643)

© 2026 Valenx Press · Last updated November 1, 2026 · Questions reflect common public interview patterns; no company affiliation. Corrections welcome via issues.

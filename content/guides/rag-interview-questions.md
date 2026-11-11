# RAG Interview Questions and Answers (2026): 24 Questions from Basics to Production

**Meta description:** 24 RAG interview questions with model answers: chunking, embeddings, hybrid search, reranking, evaluation, permissions and debugging, plus a 5-step framework.

RAG interview questions in 2026 follow the pipeline: ingestion, chunking, embeddings, retrieval, reranking, grounded generation, evaluation and production safety. Interviewers rarely stop at "what is RAG"; they ask why a system returned the wrong document, how you would measure a chunking change, and how you keep one user from seeing another user's files. Use the framework below, then practice the 24 questions out loud.

## A 5-step framework for any RAG question

Most RAG questions, from a one-line concept check to a 45-minute design round, can be answered with the same five moves.

1. **Name the stage.** Say where the question sits: ingestion, retrieval, generation, evaluation or operations. This shows you think of RAG as a pipeline, not a single prompt.
2. **Give the default.** State what you would build first, for example structure-aware chunks of a few hundred tokens, hybrid search and a cross-encoder reranker.
3. **Name the trade-off.** Precision against recall, latency against quality, freshness against cost.
4. **Say how you would measure it.** Retrieval recall@k on a labeled set, faithfulness of the answer to the retrieved text, citation accuracy, p95 latency.
5. **Name one failure mode and its fix.** Stale index, missing exact-match terms, lost-in-the-middle context, a permission leak.

Score a practiced answer against these five points with the free [answer self-check](https://aie.valenx.org/answer-check/).

## RAG basics (questions 1 to 5)

- **1. What is RAG and why use it?** Retrieval-augmented generation fetches relevant passages from your own data at query time and puts them in the prompt, so the model answers from evidence it was never trained on. It adds private and fresh knowledge, makes citations possible and reduces unsupported answers. Deep dive: [What is RAG?](https://aie.valenx.org/questions/what-is-rag/)
- **2. Walk me through a RAG pipeline.** Offline: load, parse, clean, chunk, embed and index with metadata. Online: rewrite the query if needed, retrieve candidates (vector plus keyword), filter by permissions, rerank, assemble the context, generate with citations, then log the trace for evaluation.
- **3. RAG or fine-tuning?** RAG adds knowledge that changes or must be cited. Fine-tuning changes behavior: format, tone or a narrow task. Many production systems use both. Deep dive: [RAG vs fine-tuning](https://aie.valenx.org/questions/rag-vs-fine-tuning/)
- **4. Does a long context window make RAG unnecessary?** Not for most products. Putting a whole corpus in every request raises cost and latency, models can miss facts placed in the middle of long inputs, and you still need permissions and freshness. Long context does let you retrieve bigger, more coherent chunks.
- **5. When should you not use RAG?** When the answer does not depend on a document collection (pure reasoning or style tasks), when the data fits in a small fixed prompt, or when a database query or API call gives the exact answer more reliably.

## Ingestion and chunking (questions 6 to 10)

- **6. How do you choose a chunk size?** Start from document structure (headings, paragraphs, table rows), pick a few hundred tokens with modest overlap, then tune with an evaluation set. Small chunks match precisely but lose context; large chunks keep context but add noise and tokens. Deep dive: [Choosing a chunking strategy](https://aie.valenx.org/questions/how-to-choose-a-chunking-strategy-for-rag/)
- **7. How do you handle PDFs, tables and code?** Use a layout-aware parser (OCR for scans), keep tables as rows with their headers, and split code by function or class. Flattening everything to plain text is the most common silent quality loss.
- **8. What metadata do you store per chunk?** Document ID and version, source location, section title, date, owner and access-control fields. Metadata powers filters, citations, freshness checks and deletes.
- **9. How do you keep the index fresh?** Re-ingest changed documents incrementally using content hashes or modified dates, delete chunks of removed documents, and alert when an ingestion job lags. Version the embedding model so a model change triggers a planned re-embed.
- **10. What is contextual or parent-document retrieval?** Index small chunks for matching, but return the larger parent section, or prepend a short document-level summary to each chunk before embedding. Both fix chunks that are meaningless on their own.

## Embeddings and retrieval (questions 11 to 16)

- **11. How do you choose an embedding model?** Test candidates on your own labeled queries, not only on public leaderboards. Weigh retrieval quality, languages, dimension size (storage and speed), context length, cost and whether you can host it. Deep dive: [Choosing an embedding model](https://aie.valenx.org/questions/how-to-choose-an-embedding-model/)
- **12. What is hybrid search?** Combining keyword search (such as BM25) with vector search, often merged with reciprocal rank fusion. Vectors handle paraphrase; keywords catch exact strings like error codes, SKUs and names. Deep dive: [What is hybrid search?](https://aie.valenx.org/questions/what-is-hybrid-search/)
- **13. What does a reranker do?** A cross-encoder reads the query and each candidate together and scores relevance. It is slower but more accurate than embedding similarity, so retrieve broadly, then rerank down to the few chunks that fit the context. Deep dive: [Re-ranking in RAG](https://aie.valenx.org/questions/what-is-re-ranking-in-rag/)
- **14. HNSW or IVF?** HNSW gives strong recall at low latency with more memory; IVF variants use less memory and build faster but need tuning of the number of probed lists. Pick by corpus size, update rate and memory budget. Deep dive: [HNSW vs IVF](https://aie.valenx.org/questions/hnsw-vs-ivf/)
- **15. What is query rewriting?** Using a model to turn a conversational question into a better search query: resolving "it" from chat history, expanding acronyms or splitting a compound question into several searches.
- **16. How do you choose top-k?** Retrieve more candidates than you will use (for example a few dozen), rerank, then keep only what the evaluation set shows helps. More context is not free: it costs tokens and can bury the relevant passage.

## Generation, grounding and evaluation (questions 17 to 20)

- **17. How do you reduce hallucinations in RAG?** Instruct the model to answer only from the provided context, require citations per claim, allow an explicit "not found" answer, and verify after generation that each cited passage supports the claim. Deep dive: [Why do LLMs hallucinate?](https://aie.valenx.org/questions/why-do-llms-hallucinate/)
- **18. How do you evaluate a RAG system?** Evaluate retrieval and generation separately. Retrieval: recall@k, MRR or nDCG against labeled supporting passages. Generation: correctness, faithfulness to the context, citation accuracy and abstention when evidence is missing. Then add online signals. Deep dive: [Evaluating a RAG system](https://aie.valenx.org/questions/how-do-you-evaluate-a-rag-system/)
- **19. Can you use an LLM as the judge?** Yes, for faithfulness and helpfulness, with a narrow rubric, examples and a check against human labels. Keep deterministic checks (citation IDs exist, schema valid) as code. Deep dive: [Making LLM-as-a-judge reliable](https://aie.valenx.org/questions/how-to-make-llm-as-a-judge-reliable/)
- **20. What is "lost in the middle"?** Models tend to use information at the start and end of a long context better than information in the middle. Rerank so the best evidence is near the top and keep the context short. Deep dive: [Lost in the middle](https://aie.valenx.org/questions/what-is-lost-in-the-middle/)

## Production, security and debugging (questions 21 to 24)

- **21. How do you enforce document permissions?** Filter by the user's access rights inside the retrieval query (pre-filtering), not after generation. The vector index is not an authorization boundary, and caches must be keyed by permission scope too. Deep dive: [Access control in RAG](https://aie.valenx.org/questions/access-control-in-rag/)
- **22. How do you defend against prompt injection through documents?** Treat retrieved text as untrusted data, keep instructions in the system prompt, never let document text trigger tools on its own, and test with planted malicious passages. The [OWASP prompt injection entry](https://genai.owasp.org/llmrisk/llm01-prompt-injection/) lists indirect injection as a core risk.
- **23. Users say answers got worse. How do you debug?** Pull failing traces, check whether the right passage was retrieved at all, then whether it was ranked high enough, then whether the model used it. Check recent changes: new documents, a re-embed, a prompt or model update. Deep dive: [Debugging poor RAG answers](https://aie.valenx.org/questions/how-to-debug-poor-rag-answers/)
- **24. How do you cut RAG latency and cost?** Cache embeddings and frequent answers (scoped by permissions), shrink the context with reranking, route easy questions to a smaller model, stream tokens and set a latency budget per stage. Estimate token cost per request with the free [LLM API cost calculator](https://aie.valenx.org/llm-cost-calculator/).

## Which RAG questions to expect by level

| Level | Typical focus | What earns a strong answer |
| --- | --- | --- |
| Entry | What RAG is, embeddings, chunking, RAG vs fine-tuning | Clear definitions and one concrete example |
| Mid | Hybrid search, reranking, evaluation, freshness | A metric for every change and a default you can defend |
| Senior | Permissions, multi-tenant isolation, cost, incident debugging, design rounds | Trade-offs, failure modes, rollout and monitoring |

Practice the design version with the [RAG system design scoring rubric](https://aie.valenx.org/guides/rag-system-design-interview-scoring-rubric/), and the broader design round with [AI system design interview questions](https://aie.valenx.org/guides/ai-system-design-interview-questions/).

## FAQ

- **How many RAG questions should I prepare?** Prepare the 24 above well enough to answer each in about a minute, then one full RAG design out loud in 35 to 45 minutes. Depth on a few beats memorizing a long list.
- **Do I need to know a specific vector database?** Usually not. Know the concepts (index types, filtering, hybrid search, updates) and name one tool you have actually used.
- **Are agentic RAG and GraphRAG asked in 2026?** They come up as follow-ups, mostly at senior level. Explain when an agent that decides whether and what to retrieve beats a fixed pipeline, and the latency and evaluation cost it adds. See [AI agent interview questions](https://aie.valenx.org/guides/ai-agent-interview-questions/).
- **What is the most common mistake in RAG interview answers?** Tuning prompts without first checking whether retrieval found the right passage. Always separate retrieval failures from generation failures.
- **How can I practice RAG questions for free?** Use the [timed mock round](https://aie.valenx.org/mock-interview/), score answers with the [self-check](https://aie.valenx.org/answer-check/) and plan the days before your interview with the [study plan](https://aie.valenx.org/study-plan/).

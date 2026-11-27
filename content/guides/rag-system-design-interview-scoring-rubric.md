# RAG System Design Interview: A Scoring Rubric

Score a RAG system design interview out of 100 points. Cover needs, ingestion, retrieval, generation, review, and production safeguards. A strong answer explains the data flow. It uses quality and latency targets. It tells a retrieval failure apart from a generation failure. It also protects document access. This is a practice rubric. It is not an employer standard.

## What should a 100-point RAG design rubric measure?

Use six weighted categories. Reward a complete, testable design rather than a collection of tool names.

- Apply the following suggested scorecard in a consistent way across mock answers. The weights are editorial choices for practice. They are not published interview criteria. No company supplied them.

  | Category | Points | What earns full credit |
  | --- | ---: | --- |
  | Requirements and constraints | 10 | Users, data, targets, assumptions |
  | Ingestion and indexing | 20 | Parsing, chunks, metadata, updates |
  | Retrieval | 20 | Search, ranking, filters, failures |
  | Generation and grounding | 15 | Context, citations, abstention |
  | Evaluation | 20 | Datasets, metrics, regressions |
  | Production and security | 15 | Access, latency, cost, observability |

- Grade each category from zero to its maximum. Award full points for a clear mechanism, a defensible choice, a measurable test, and a known failure mode. Award about half for a plausible but untested outline. Award zero if the category is missing.
- Treat document disclosure that is not allowed as a critical failure, no matter the total. An answer can sound polished yet be unsafe if retrieval ignores tenant permissions. It is also unsafe if untrusted text can authorize tool actions.
- Keep the prompt fixed when comparing candidates. Do the same for practice attempts. Changing corpus size, constraints, or the definition of acceptable answers makes raw scores hard to read.

## How do you score requirements, ingestion, and indexing?

Award up to 30 points for defining the problem in exact terms. Also award points for keeping source content traceable, current, and correctly split.

- **Requirements, 10 points.** Identify target users, question types, data sources, and access rules. Also name document update frequency, rough corpus size, acceptable answer behavior, and service-level constraints. Label every estimated traffic or latency figure as an assumption.
- **Parsing and provenance.** Describe how PDFs, web pages, tables, and metadata become indexed content. Preserve a document ID, version, and source URL or location. Also keep a page or section reference so answers can point to evidence.
- **Chunking choices.** Select a chunking strategy based on document structure and query style. Discuss overlap, table boundaries, truncation, and duplicates. Explain why larger chunks might improve context. Also explain why they can raise irrelevant text and token cost.
- **Index operations.** Explain embedding versioning, document deletion, incremental reindexing, permission metadata, and freshness monitoring. Rebuilding everything for each update is simple. It may cost too much at large scale.
- **Full-credit signal.** A diagram shows the ingestion queue, cleanup, storage, chunk creation, embedding output, and index update path. Include one concrete failure scenario and an alert. Google Cloud's [RAG architecture reference](https://docs.cloud.google.com/architecture/rag-reference-architectures) documents design options.

## How do you score retrieval and grounded generation?

Award up to 35 points for returning useful authorized evidence. Also award points for answers that stay faithful to that evidence.

- **Retrieval, 20 points.** Compare keyword, vector, and hybrid search for the dataset. Explain top-k selection, metadata and tenant filters, query rewriting, and reranking. Explain when the system should find no documents that are good enough.
- **Retrieval diagnostics.** Ask whether the gold supporting document appears in top-k. Ask whether the ranking is useful, and whether retrieved passages are stale or contradictory. Separate a retrieval miss from a generation error. Do not tune prompts at random.
- **Generation, 15 points.** Explain context selection, instruction boundaries, output schema, and answer citations. Also explain explicit abstention for unsupported questions. Citations must resolve to the retrieved document. They should not merely display plausible-looking titles.
- **Trust boundary.** Retrieved material is data, not an instruction source. The response must not grant permissions or run privileged actions. It must not reveal protected info simply because an indexed page asks it to.
- **Full-credit signal.** Walk through a question, retrieved passages, and the final answer. Then show a citation check and a failure case with missing evidence. Google Cloud's [RAG explanation](https://cloud.google.com/use-cases/retrieval-augmented-generation) describes how retrieval and generation form separate stages.

## How do you score evaluation rigor?

Award 20 points for a labeled, repeatable review. It should tell search quality apart from final-answer quality.

- Build a question set with expected supporting documents, answer expectations, and permission contexts. Include cases that should produce abstention. Also include ordinary queries, paraphrases, exact identifiers, stale content, and hostile document text.
- Report retrieval metrics such as recall at k and ranking quality where relevance labels exist. Do not treat retrieval similarity scores as calibrated odds of a correct answer.
- Score groundedness, factual correctness, completeness, citation support, refusal correctness, and task success separately. A response may be relevant yet contain an unsupported claim. It may also be grounded but omit a critical fact.
- Use deterministic checks for machine-verifiable properties and human review for nuanced judgments. If using an LLM judge, write scoring anchors, compare with human annotations, and measure disagreement. Do not treat its number as ground truth.
- Present a baseline, an experimental change, sample sizes, and results segmented by query type. AWS's [RAG evaluation documentation](https://docs.aws.amazon.com/bedrock/latest/userguide/evaluation-kb.html) distinguishes retrieval-only from retrieval-and-generation assessment.

## How do you score operational readiness and explain the result?

Award 15 points for measurable reliability, cost controls, security boundaries, and an actionable incident response plan.

- Break p95 latency into query rewriting, search, reranking, context assembly, model inference, and postprocessing. Show which stages can be cached. Show where caches risk serving stale or unauthorized content.
- Estimate unit economics with input tokens, output tokens, retrieval infrastructure, request volume, retries, and concurrency. State the assumptions. Trade away complexity only when a quality or reliability gain justifies it.
- Enforce authorization at retrieval and tool boundaries. Log without leaking secrets. Redact sensitive data. Restrict model-triggered side effects. OWASP's [prompt injection guidance](https://genai.owasp.org/llmrisk/llm01-prompt-injection/) explains why prompts alone do not establish a security boundary.
- Define dashboards for empty retrievals, unsupported answers, timeouts, cost spikes, stale indexes, and scorer regressions. Pair each alert with a fallback, owner, and rollback decision.
- Interpret the overall practice score as **85-100: strong**, **70-84: workable with gaps**, **50-69: incomplete**, and **below 50: redesign needed**. These ranges are suggested coaching thresholds. They are not validated hiring predictions.

For shorter concept questions before the design round, practice the [24 RAG interview questions](https://aie.valenx.org/guides/rag-interview-questions/). For other design prompts see [AI system design interview questions](https://aie.valenx.org/guides/ai-system-design-interview-questions/).

## FAQ

Use these answers when a mock interviewer challenges the scoring method. They also cover its practical limits.

- **Is this an official RAG interview rubric?** No. It is a transparent practice instrument built around standard engineering concerns. No score can predict a hiring decision across companies or interviewers.
- **Should retrieval and generation be evaluated together?** Score both end to end and separately so the team can locate the failure source. A fluent answer cannot make up for missing evidence. Excellent retrieval cannot make up for made-up claims.
- **Does using a vector database earn points automatically?** No. Selection matters only when supported by the data, constraints, and measurements. A smaller hybrid or keyword baseline may be a better initial design.
- **What is the fastest way to improve a low score?** Identify the lowest weighted category. Add a diagram, a measured test, and a concrete failure response. Rehearse the same scenario again without changing its requirements.

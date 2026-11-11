# RAG System Design Interview: A Scoring Rubric

Score a RAG system design interview out of 100 points across requirements, ingestion, retrieval, generation, evaluation, and production safeguards. A strong answer explains the data flow, uses quality and latency targets, distinguishes retrieval failure from generation failure, and protects document access. This is a practice rubric, not an employer standard.

## What should a 100-point RAG design rubric measure?

Use six weighted categories to reward a complete, testable design rather than a collection of tool names.

- Apply the following suggested scorecard consistently across mock answers; the weights are editorial choices for practice, not published interview criteria from any company.

  | Category | Points | What earns full credit |
  | --- | ---: | --- |
  | Requirements and constraints | 10 | Users, data, targets, assumptions |
  | Ingestion and indexing | 20 | Parsing, chunks, metadata, updates |
  | Retrieval | 20 | Search, ranking, filters, failures |
  | Generation and grounding | 15 | Context, citations, abstention |
  | Evaluation | 20 | Datasets, metrics, regressions |
  | Production and security | 15 | Access, latency, cost, observability |

- Grade each category from zero to its maximum. Award full points for a clear mechanism, defensible choice, measurable validation, and known failure mode; award approximately half for a plausible but untested outline; award zero for omission.
- Treat unauthorized document disclosure as a critical failure regardless of the total. An answer can sound sophisticated yet be unsafe if retrieval ignores tenant permissions or if untrusted text can authorize tool actions.
- Keep the prompt fixed when comparing candidates or practice attempts. Changing corpus size, constraints, or the definition of acceptable answers makes raw scores difficult to interpret.

## How do you score requirements, ingestion, and indexing?

Award up to 30 points for defining the problem precisely and keeping source content traceable, current, and correctly partitioned.

- **Requirements, 10 points:** identify target users, question types, data sources, access rules, document update frequency, approximate corpus size, acceptable answer behavior, and service-level constraints. Label every estimated traffic or latency figure as an assumption.
- **Parsing and provenance:** describe how PDFs, web pages, tables, and metadata become indexed content. Preserve a document ID, version, source URL or location, and page or section reference so answers can point to evidence.
- **Chunking choices:** select a chunking strategy based on document structure and query style. Discuss overlap, table boundaries, truncation, duplicates, and why larger chunks might improve context while increasing irrelevant text and token cost.
- **Index operations:** explain embedding versioning, document deletion, incremental reindexing, permission metadata, and freshness monitoring. Rebuilding everything for each update is simple but may be too costly at large scale.
- **Full-credit signal:** a diagram shows the ingestion queue, normalization, storage, chunk creation, embedding generation, and index update path, with one concrete failure scenario and an alert. Google Cloud's [RAG architecture reference](https://docs.cloud.google.com/architecture/rag-reference-architectures) documents architectural options.

## How do you score retrieval and grounded generation?

Award up to 35 points for returning useful authorized evidence and producing answers that remain faithful to that evidence.

- **Retrieval, 20 points:** compare keyword, vector, and hybrid search for the dataset. Explain top-k selection, metadata and tenant filters, query rewriting, reranking, and when the system should find no acceptable documents.
- **Retrieval diagnostics:** ask whether the gold supporting document appears in top-k, whether the ranking is useful, and whether retrieved passages are stale or contradictory. Separate a retrieval miss from a generation error instead of tuning prompts blindly.
- **Generation, 15 points:** explain context selection, instruction boundaries, output schema, answer citations, and explicit abstention for unsupported questions. Citations must resolve to the retrieved document rather than merely displaying plausible-looking titles.
- **Trust boundary:** retrieved material is data, not an instruction source. The response must not grant permissions, execute privileged actions, or reveal protected information simply because an indexed page asks it to.
- **Full-credit signal:** walk through a question, retrieved passages, final answer, citation check, and a failure case with missing evidence. Google Cloud's [RAG explanation](https://cloud.google.com/use-cases/retrieval-augmented-generation) describes how retrieval and generation form separate stages.

## How do you score evaluation rigor?

Award 20 points for a labeled, reproducible evaluation that distinguishes search quality from final-answer quality.

- Build a question set with expected supporting documents, answer expectations, permission contexts, and cases that should produce abstention. Include ordinary queries, paraphrases, exact identifiers, stale content, and adversarial document text.
- Report retrieval metrics such as recall at k and ranking quality where relevance labels exist. Avoid treating retrieval similarity scores as calibrated probabilities of a correct answer.
- Evaluate groundedness, factual correctness, completeness, citation support, refusal correctness, and task success separately. A response may be relevant yet contain an unsupported claim, or be grounded but omit a critical fact.
- Use deterministic checks for machine-verifiable properties and human review for nuanced judgments. If using an LLM judge, write scoring anchors, compare with human annotations, and measure disagreement rather than treating its number as ground truth.
- Present a baseline, an experimental change, sample sizes, and results segmented by query type. AWS's [RAG evaluation documentation](https://docs.aws.amazon.com/bedrock/latest/userguide/evaluation-kb.html) distinguishes retrieval-only from retrieval-and-generation assessment.

## How do you score operational readiness and explain the result?

Award 15 points for measurable reliability, cost controls, security boundaries, and an actionable incident response plan.

- Break p95 latency into query rewriting, search, reranking, context assembly, model inference, and postprocessing. Show which stages can be cached and where caches risk serving stale or unauthorized content.
- Estimate unit economics with input tokens, output tokens, retrieval infrastructure, request volume, retries, and concurrency. State the assumptions and trade away complexity only when a quality or reliability gain justifies it.
- Enforce authorization at retrieval and tool boundaries, log without leaking secrets, redact sensitive data, and restrict model-triggered side effects. OWASP's [prompt injection guidance](https://genai.owasp.org/llmrisk/llm01-prompt-injection/) explains why prompts alone do not establish a security boundary.
- Define dashboards for empty retrievals, unsupported answers, timeouts, cost spikes, stale indexes, and evaluator regressions. Pair each alert with a fallback, owner, and rollback decision.
- Interpret the overall practice score as **85-100: strong**, **70-84: workable with gaps**, **50-69: incomplete**, and **below 50: redesign needed**. These ranges are suggested coaching thresholds, not validated hiring predictions.

For shorter concept questions before the design round, practice the [24 RAG interview questions](https://aie.valenx.org/guides/rag-interview-questions/), and for other design prompts see [AI system design interview questions](https://aie.valenx.org/guides/ai-system-design-interview-questions/).

## FAQ

Use these answers when a mock interviewer challenges the scoring method or its practical limits.

- **Is this an official RAG interview rubric?** No, it is a transparent practice instrument built around standard engineering concerns. No score can predict a hiring decision across different companies or interviewers.
- **Should retrieval and generation be evaluated together?** Evaluate both end to end and separately so the team can locate the failure source. A fluent answer cannot compensate for missing evidence, and excellent retrieval cannot compensate for fabrication.
- **Does using a vector database earn points automatically?** No, selection matters only when supported by the data, constraints, and measurements. A smaller hybrid or keyword baseline may be a better initial design.
- **What is the fastest way to improve a low score?** Identify the lowest weighted category and add a diagram, a measured test, and a concrete failure response. Rehearse the same scenario again without changing its requirements.


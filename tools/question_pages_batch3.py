# Batch 3 question pages (Nov 8 2026). Drafted by the VM Harness from index.html answers, reviewed by codex, schema-checked. Same schema as question_pages_data.py.
PAGES = [
 {
  "slug": "what-is-self-attention",
  "q": "What is self-attention and why does it matter?",
  "desc": "Learn what self-attention is, how query, key, and value projections work, why it improves long-range context, and where its quadratic cost appears.",
  "level": "Entry",
  "src": [
   2
  ],
  "testing": "Whether you can explain the query-key-value computation, why self-attention improves long-range token interactions, the quadratic cost, and the reason for scaling before softmax.",
  "steps": [
   "Represent each token with three learned projections: a query, a key and a value.",
   "Compute compatibility scores with the query-key dot product, scale them by 1/sqrt(d_k), and apply softmax to obtain attention weights.",
   "Produce each token's output as a weighted sum of the value vectors using those attention weights.",
   "Allow each token to retrieve information from any position permitted by the attention mask in one layer, avoiding a recurrent bottleneck while supporting parallel sequence processing during training.",
   "Recognize the trade-off: full self-attention has O(n^2) compute and an attention matrix that also scales quadratically with sequence length."
  ],
  "sample": [
   "I explain self-attention as a way for the model to decide which other tokens in the sequence matter for the token it is processing. Each token is projected into a query, a key and a value. The query represents what the token is looking for, the key represents what it offers for matching, and the value carries information that can be passed along. We compute scores by taking the query-key dot product, divide by the square root of the key dimension, and apply softmax to get normalized attention weights.",
   "The output for each position is a weighted sum of the value vectors using those weights. The important benefit is direct information flow: each token can pull information from positions permitted by the attention mask through one layer instead of passing it through recurrent steps. Unmasked attention can access the entire sequence; causal attention can access only current and earlier positions. During training, positions can still be processed in parallel.",
   "The trade-off is quadratic computation. For sequence length n and fixed head dimensions, full attention uses O(n^2) compute. Explicitly storing its attention matrix also takes O(n^2) memory, but implementations such as FlashAttention avoid materializing that matrix. Dividing scores by the square root of the key dimension also matters: under standard assumptions, dot-product variance grows with dimension, which can saturate softmax and produce small gradients. Scaling helps keep scores in a useful range."
  ],
  "followups": [
   [
    "Why do we divide the attention scores by sqrt(d_k)?",
    "Without the scaling, dot products grow as the key dimension grows. The softmax can then saturate, producing very small gradients and making optimization harder."
   ],
   [
    "What is the main trade-off in self-attention?",
    "It gives tokens direct access to positions permitted by the attention mask, but full attention requires O(n^2) computation at fixed head dimensions. Materializing the attention matrix also requires O(n^2) memory; memory-efficient implementations avoid storing it."
   ]
  ],
  "mistakes": [
   "Assuming a token can only use nearby context, as in a fixed local window.",
   "Forgetting to scale the QK^T scores by sqrt(d_k) before applying softmax.",
   "Claiming the attention cost is linear in sequence length; the full attention matrix is quadratic.",
   "Describing the output as a plain average of values and ignoring the learned, content-dependent weights."
  ],
  "related": [
   "explain-the-transformer-architecture",
   "what-is-kv-cache",
   "what-is-lost-in-the-middle"
  ]
 },
 {
  "slug": "fine-tuning-vs-in-context-learning",
  "q": "Fine-tuning vs in-context learning: what is the difference?",
  "desc": "Compare fine-tuning and in-context learning, including when to update model weights, prompt examples, data needs, iteration speed, cost, and use cases.",
  "level": "Mid",
  "src": [
   9
  ],
  "testing": "Whether you can distinguish prompt-based learning from weight updates, compare their costs and deployment needs, and choose retrieval for frequently changing facts.",
  "steps": [
   "In-context learning puts instructions and examples into the prompt without changing the model weights.",
   "In-context learning supports immediate iteration, but each request pays for the extra prompt tokens and behavior remains bounded by the context window.",
   "Fine-tuning trains on examples and updates model parameters, potentially making formats, tone or narrow-task behavior more consistent.",
   "Fine-tuning can make a smaller model perform as well as a larger prompted model, but it requires data, training, evaluation and redeployment.",
   "Use retrieval rather than fine-tuning for facts that change frequently, because retrieval lets the source of truth be updated without retraining."
  ],
  "sample": [
   "I would start by separating what changes. With in-context learning, I put the instructions and any examples directly into the prompt. The model parameters do not change, so I can iterate immediately by editing the prompt. The tradeoff is that every request carries and processes the extra prompt tokens, and the behavior I can obtain is constrained by the context window. It is a good fit when the task is quick to prototype, the instructions change often, or I want temporary behavior without a training run.",
   "Fine-tuning is different because I train the model on examples and update model parameters. That can make the desired format, tone or narrow task behavior more consistent and can make a smaller model perform as well as a larger model that only receives examples in its prompt. These benefits require evaluation. Learned behavior can reduce how much instruction I need to supply on every call.",
   "I would also be explicit about the cost. Fine-tuning requires curating data, running training and evaluating whether the result improved. After deployment, a changed model normally means redeployment. I would not use fine-tuning as my default way to teach frequently changing facts; retrieval is better because it lets me update the source of truth without retraining. So I choose based on whether I need durable behavior changes or current information, and whether the per-request prompt cost matters."
  ],
  "followups": [
   [
    "When would I choose in-context learning over fine-tuning?",
    "I would choose it when I need immediate iteration, temporary instructions or examples, or a quick prototype. I would also consider it when the extra prompt tokens and context-window limits are acceptable."
   ],
   [
    "Can fine-tuning be a good way to add frequently changing facts?",
    "Usually not. Fine-tuning is poorly suited to frequently changing information because each update requires training data, evaluation and redeployment. I would use retrieval so the information source can be updated independently."
   ],
   [
    "What operational work does fine-tuning add?",
    "I need to collect and curate training examples, run training, evaluate the result and deploy the updated model. Prompt-only changes also require evaluation and may require curated examples, but they do not require model training."
   ]
  ],
  "mistakes": [
   "Treating in-context learning as a training step that changes model weights.",
   "Claiming prompt examples are permanently learned and no longer consume context tokens on each request.",
   "Using fine-tuning as the default solution for frequently changing facts.",
   "Comparing the approaches only on answer quality while ignoring prompt cost, context limits, training data, evaluation and redeployment."
  ],
  "related": [
   "rag-vs-fine-tuning",
   "what-is-rag",
   "how-to-build-a-fine-tuning-dataset"
  ]
 },
 {
  "slug": "zero-shot-vs-few-shot-prompting",
  "q": "Zero-shot vs few-shot prompting: when do you use each?",
  "desc": "When to use zero-shot versus few-shot prompting, how to select examples, and how to avoid biased outputs from imbalanced labels or style patterns.",
  "level": "Entry",
  "src": [
   17
  ],
  "testing": "Whether you know when zero-shot is enough, can identify cases that need few-shot examples, and can design balanced examples without copying surface patterns into the output.",
  "steps": [
   "Zero-shot prompting: give the instruction and any needed context without demonstrations.",
   "Few-shot prompting: include several labeled input and output examples in the prompt.",
   "Use zero-shot for common tasks with simple formats and little ambiguity.",
   "Use few-shot for unusual formats, subtle labels, or strict style and output consistency.",
   "Choose balanced, varied examples that cover hard cases, since models can copy their surface patterns."
  ],
  "sample": [
   "I start by thinking about how much structure the task needs. For a common task with a simple format, I use zero-shot prompting: I describe the task and give any necessary context, but no demonstrations. That is quicker to maintain and avoids spending context window space on examples. If the model already understands the labels and the expected output is easy to recognize, zero-shot is usually the cleaner choice.",
   "I switch to few-shot prompting when the format is unusual, the labels are subtle, or I need consistent style. I put a few input and output examples directly in the prompt, usually with a clear separation between examples and the final query. I select examples that cover the hard cases, vary the inputs, and make the labels balanced. I also test whether the examples are actually changing behavior, rather than assuming that more examples always help.",
   "I see one failure mode as surface-pattern copying. If every example has a positive label, the model may treat positive as the default, even when the input calls for another label. I would catch that with a small set of edge cases, including examples with the opposite label, and adjust the examples if needed. In short, I use zero-shot for straightforward tasks and few-shot when examples communicate the missing pattern. I also treat examples as data that needs evaluation, not as decoration."
  ],
  "followups": [
   [
    "When is few-shot prompting not worth the extra tokens?",
    "I would use zero-shot when the task is straightforward, the model already understands the format, and added examples would mainly increase cost and latency."
   ],
   [
    "How should I choose few-shot examples?",
    "I would cover hard cases, vary the inputs, balance the labels, and check that surface details in the examples are not driving the outputs."
   ],
   [
    "What if every few-shot example has the same label?",
    "I would rebalance the examples and include the opposite label, then test edge cases because the model may treat the repeated label as the default."
   ]
  ],
  "mistakes": [
   "Using zero-shot for an unusual format or subtle labels without testing the model first.",
   "Using unbalanced labels, which can make one class the default.",
   "Choosing examples only from easy cases instead of covering hard cases.",
   "Assuming more examples always help instead of testing whether they change behavior."
  ],
  "related": [
   "what-is-a-context-window",
   "temperature-vs-top-p",
   "how-to-build-a-fine-tuning-dataset"
  ]
 },
 {
  "slug": "what-is-a-system-prompt",
  "q": "What is a system prompt and what belongs in it?",
  "desc": "What goes in a system prompt, how to structure its role, scope, rules, style and refusals, and what to keep out for security and prompt caching.",
  "level": "Entry",
  "src": [
   24
  ],
  "testing": "Whether you can define a system prompt, separate stable instructions from request data, keep secrets out of it, and explain how caching and refusals affect behavior.",
  "steps": [
   "Put the assistant's role, task scope, and non-negotiable rules in the highest-priority instruction block.",
   "Define output style, required structure, and the desired level of detail.",
   "State refusal behavior for requests that fall outside the allowed scope.",
   "Keep the system prompt stable across requests so the same prefix can be prompt-cached.",
   "Keep secrets and credentials out of it, assume its contents can be extracted, and put per-request data in the user turn."
  ],
  "sample": [
   "I think of a system prompt as the highest-priority instruction block for a conversation. It tells the model who it is, what job it is handling, and which rules it must follow. I put the stable role, scope, behavioral rules, output style, and refusal behavior there. I also define the required output format, such as a schema or concise sections, so the task is explicit before the conversation starts.",
   "One practical rule is to keep that block stable. A stable prefix can be prompt-cached, so the provider may reuse that computation across requests. I separate that shared policy from request-specific information. If a user supplies a document, question, or other request payload, I put it in the user turn rather than rebuilding the system prompt for every call.",
   "I never put secrets in the system prompt. The prompt can be extracted, logged, cached, or shown to someone reviewing the application, so I assume any value there is visible and treat it as unsafe. The same applies to credentials and sensitive data. In an interview, I would explain that the system prompt sets policy, but it is not a security boundary. I would enforce authorization and data protection in the application around the model."
  ],
  "followups": [
   [
    "How do I keep a system prompt from becoming too long?",
    "I keep only stable instructions such as role, scope, rules, style, and refusal behavior, then put request-specific data in the user turn."
   ],
   [
    "Can the system prompt be used to protect sensitive information?",
    "I would not treat it as a security boundary. I assume its contents can be extracted, so secrets stay out and access controls live in the application."
   ],
   [
    "What if a user asks for something the system prompt forbids?",
    "I give the system instructions precedence and apply the refusal behavior defined there."
   ]
  ],
  "mistakes": [
   "Putting API keys, passwords, or other secrets in the system prompt.",
   "Putting changing content before stable instructions, which reduces the shared prefix available for prompt caching.",
   "Putting per-request user data in the system prompt instead of the user turn.",
   "Leaving refusal behavior or output-style rules implicit instead of defining them."
  ],
  "related": [
   "what-are-llm-guardrails",
   "what-is-a-context-window",
   "how-to-get-reliable-json-output-from-an-llm"
  ]
 },
 {
  "slug": "pgvector-vs-pinecone-vs-other-vector-databases",
  "q": "How do you choose a vector database (pgvector, Pinecone, and others)?",
  "desc": "How to choose a vector database, comparing pgvector, managed services, self-hosted engines, and hybrid search options by scale, latency, and operations.",
  "level": "Entry",
  "src": [
   35
  ],
  "testing": "Whether you can compare pgvector, managed services, self-hosted engines, and hybrid-search options using filtering, scale, latency, operations, and cost rather than hype.",
  "steps": [
   "Define filtering needs, scale, latency targets, operations capacity, and cost before choosing a store.",
   "Postgres with pgvector: simplest when you already run Postgres and the expected scale fits the setup.",
   "Managed vector databases such as Pinecone: little operations work, with usage-based pricing.",
   "Self-hosted engines such as Qdrant, Weaviate, and Milvus: more deployment control, with filtering and scaling capabilities to benchmark against the workload.",
   "Search engines such as Elasticsearch and OpenSearch: strong candidates for hybrid lexical plus vector retrieval."
  ],
  "sample": [
   "I start by turning the product requirements into a decision framework: filtering needs, expected scale, latency targets, how much operations work my team can absorb, and cost. I would not pick a database because it is fashionable. I would benchmark representative queries with realistic vector counts, filters, and concurrency, and I would include the index build and update cost in the comparison.",
   "If we already run Postgres and our scale fits what pgvector can handle well, pgvector is often the simplest choice. It keeps our relational data, permissions, and vector search in one system, so there is less infrastructure to operate. For managed vector databases such as Pinecone, the tradeoff is less operations work in exchange for usage-based pricing and less direct control over the stack.",
   "If we need more deployment control, self-hosted engines such as Qdrant, Weaviate, or Milvus are candidates, but their filtering and scaling capabilities need workload-specific testing. If the application needs lexical search, BM25, and vector search together, Elasticsearch or OpenSearch is a natural candidate for hybrid retrieval. My final recommendation would come from the tested requirements, not the category name. I would also plan how the choice changes as the corpus and traffic grow."
  ],
  "followups": [
   [
    "When is pgvector a better fit than a dedicated vector database?",
    "When the team already operates Postgres, the data and filters are relational, and the expected scale and latency fit a validated pgvector setup."
   ],
   [
    "When should I choose a managed vector database?",
    "When minimizing operational work matters more than direct control, and usage-based pricing and the required features fit the workload."
   ],
   [
    "How do I evaluate a hybrid-search engine?",
    "I would test representative lexical and semantic queries, filter behavior, latency, update cost, and ranking quality against the application requirements."
   ]
  ],
  "mistakes": [
   "Choosing a vector database based on popularity rather than filtering, scale, latency, operations, and cost requirements.",
   "Assuming a managed service removes all infrastructure concerns without checking usage-based pricing and limits.",
   "Overlooking hybrid lexical plus vector retrieval when the application needs both exact and semantic matching.",
   "Evaluating only top-k vector speed and ignoring index build time, updates, filters, and operational burden."
  ],
  "related": [
   "hnsw-vs-ivf",
   "what-is-hybrid-search",
   "how-to-choose-an-embedding-model"
  ]
 },
 {
  "slug": "what-is-query-transformation-in-rag",
  "q": "What is query transformation in RAG and why does it help?",
  "desc": "What query transformation does in RAG, why it improves retrieval, and when the added latency and model calls are worth the cost for enterprise search.",
  "level": "Mid",
  "src": [
   37
  ],
  "testing": "Whether you can explain common query transformations, connect them to retrieval recall, and evaluate their latency tradeoff.",
  "steps": [
   "Query transformation rewrites the user's request before retrieval, bridging vocabulary differences between the question and indexed documents.",
   "Common rewrites resolve pronouns from chat history, expand acronyms, and split multi-part questions into separate subqueries.",
   "HyDE generates a hypothetical answer and embeds that answer to retrieve passages related to the expected response.",
   "Transformation helps when relevant documents use different wording than the user, so it can improve retrieval recall.",
   "Because transformation can add model calls and latency, compare retrieval recall and answer quality against a no-rewrite baseline."
  ],
  "sample": [
   "I see query transformation as a query-rewrite step that runs before retrieval. The system takes the user's question and produces one or more search queries that are more likely to match the indexed text. This is useful because people and documents often describe the same concept in different language, so a semantically relevant document may not look close to the original wording.",
   "Depending on the case, the rewrite can resolve pronouns from earlier chat turns, expand an acronym, or split a multi-part question into separate subqueries. For example, if someone asks what it supports after describing a company product, I would substitute the relevant product name before searching. Another technique is HyDE. I generate a hypothetical answer, embed that answer rather than the question, and use the resulting vector to find supporting passages. The important point is that each transformed query still retrieves evidence that I can inspect before answering.",
   "Transformation is not automatically better, though. Model-based transformation can add calls and latency and may introduce errors. I would compare the transformed and original queries on a fixed retrieval set, looking at relevant-document recall and answer quality rather than assuming a gain. I would use it for ambiguous, conversational, or multi-part questions, and keep the original query as a fallback. That lets me pay the extra latency only when the measured recall improvement justifies it."
  ],
  "followups": [
   [
    "When would I prefer HyDE over a normal query rewrite?",
    "I would consider HyDE when the relevant documents use language that differs from the question and generating a plausible answer may lead the retriever closer to that vocabulary."
   ],
   [
    "How do I measure whether query transformation is helping?",
    "I would compare it with the original query on a fixed retrieval set, measuring relevant-document recall and downstream answer quality while also recording latency."
   ],
   [
    "What can go wrong during query transformation?",
    "A rewrite can introduce an incorrect entity, drop part of the request, or produce queries that retrieve plausible but irrelevant passages, so I would inspect the transformed queries."
   ]
  ],
  "mistakes": [
   "Treating query transformation as a guaranteed improvement in retrieval recall.",
   "Using a hypothetical answer as source evidence instead of treating it only as a retrieval proxy.",
   "Rewriting a multi-part question into one query rather than considering separate subqueries.",
   "Ignoring potential added model calls and latency when deciding whether transformation is worthwhile."
  ],
  "related": [
   "what-is-rag",
   "how-to-choose-a-chunking-strategy-for-rag",
   "how-do-you-evaluate-a-rag-system"
  ]
 },
 {
  "slug": "what-is-agentic-rag",
  "q": "What is agentic RAG?",
  "desc": "What agentic RAG means, how iterative retrieval handles multi-hop questions, and how to control cost, latency, and evaluation in production systems.",
  "level": "Mid",
  "src": [
   39
  ],
  "testing": "Whether you can distinguish agentic retrieval from a fixed pipeline and explain its benefits, costs, and production controls.",
  "steps": [
   "Agentic RAG replaces one fixed retrieve-then-generate pass with a model-controlled retrieval loop.",
   "The model decides when and what to search and can issue several queries during that loop.",
   "It reads the returned results and may search again when it still needs evidence.",
   "This supports multi-hop questions, but it can increase cost and make evaluation harder.",
   "Cap the number of steps and log each retrieval so the decision path can be inspected."
  ],
  "sample": [
   "I would define agentic RAG as a retrieval-augmented generation system where the model controls part of the retrieval loop. In a basic RAG pipeline, I rewrite a query once, retrieve documents, and pass them to the model. In an agentic version, the model can decide whether it needs to search, choose what to look for, issue multiple queries, read the results, and decide whether to search again before it writes the answer.",
   "That extra control is useful for questions that cannot be answered from one retrieval pass. For a multi-hop question, I might retrieve evidence about one entity, notice that another fact is missing, and issue a second query that connects the two. I can also ask for a narrower search if the first results look weak. The system therefore treats retrieval as an action the agent can iterate on, while the model uses the retrieved passages as evidence for the final response.",
   "The tradeoff is that this can make the system more expensive, slower, and harder to evaluate than a fixed pipeline. Additional searches add retrieval overhead, and model calls to plan searches or process results can increase token cost. A model may also loop without converging. In production, I would cap the number of steps, log every query and retrieved document, and preserve a trace so I can diagnose both the answer and the path. I would test it on multi-hop tasks against a simpler baseline, measuring success as well as steps, cost, and latency rather than assuming the agentic design wins."
  ],
  "followups": [
   [
    "What distinguishes agentic RAG from a multi-query RAG pipeline?",
    "A multi-query pipeline runs a preset query expansion, while agentic RAG lets the model choose later searches after reading the results of earlier ones."
   ],
   [
    "When is agentic RAG worth the additional cost?",
    "I would favor it when a single retrieval pass cannot connect the evidence needed for a multi-hop task, and when testing shows better task success despite the extra steps."
   ],
   [
    "How do I prevent the retrieval loop from running indefinitely?",
    "I would set a step cap, define stopping conditions, and monitor repeated queries and step counts in production logs."
   ]
  ],
  "mistakes": [
   "Calling any pipeline with several retrievals agentic without a model-controlled retrieval loop.",
   "Assuming more searches will always produce a better answer.",
   "Running the agent without a step cap or stopping condition.",
   "Evaluating only the final answer without retaining retrieval logs and decision traces."
  ],
  "related": [
   "what-is-rag",
   "single-agent-vs-multi-agent",
   "how-do-you-evaluate-a-rag-system"
  ]
 },
 {
  "slug": "how-to-evaluate-an-ai-agent",
  "q": "How do you evaluate an AI agent?",
  "desc": "How to evaluate an AI agent with realistic tasks, measurable end states, trajectory review, error recovery, cost, and latency across model or prompt changes.",
  "level": "Mid",
  "src": [
   49
  ],
  "testing": "Whether you can build a repeatable agent evaluation that measures outcomes, efficiency, recovery, and unsafe trajectory behavior.",
  "steps": [
   "Create a fixed suite of realistic tasks with clearly defined and checkable end states.",
   "Measure task success rate as the primary metric and report results by task type.",
   "Track step count, cost, latency, and error recovery alongside correctness.",
   "Inspect trajectories, including tool calls and intermediate actions, rather than judging only the final response.",
   "Rerun the same suite for every model or prompt change and review regressions."
  ],
  "sample": [
   "I would evaluate an AI agent with a fixed suite of realistic tasks that have checkable end states. For example, a support task succeeds only if the agent opens the right ticket and attaches the correct records, not merely if its final message sounds plausible. I would define the expected state and validation rules before running the suite, then report task success rate as the primary measure. Results should be broken out by task type so a gain on easy tasks does not hide a failure on a critical workflow.",
   "I would also measure step count, cost, latency, and error recovery. These operational metrics show whether the agent reaches the right state efficiently and whether it can recover after a failed tool call or an incorrect intermediate result. A useful test changes one condition, such as making one tool return an error, and checks whether the agent responds appropriately instead of repeating the same call. I would keep the scenario and judge consistent across versions so the comparison is meaningful.",
   "Trajectory review is essential because final-answer scoring can hide unsafe behavior. I would inspect the tool calls, intermediate state changes, and retrieved evidence. If the agent reaches the correct answer after an unauthorized action or a risky tool call, I would count the run as a failure even though the outcome looks right. Finally, I would rerun the same suite for every model or prompt change and review regressions, rather than relying on a few manual demos."
  ],
  "followups": [
   [
    "Can I use an LLM judge to evaluate an agent?",
    "I would use deterministic checks whenever the task has a clear end state. For less structured qualities, an LLM judge can help, but I would calibrate it against human review and keep the rubric consistent."
   ],
   [
    "How do I detect regressions between agent versions?",
    "I would run the same fixed suite, compare success and operational metrics by task type, and investigate every meaningful drop rather than relying on an overall average."
   ],
   [
    "How do I test error recovery?",
    "I would introduce controlled failures, such as a timeout or invalid tool response, and verify that the agent handles the failure appropriately without repeating the same action indefinitely."
   ]
  ],
  "mistakes": [
   "Scoring only the final message and ignoring the path used to reach it.",
   "Treating a correct final answer as success when the trajectory included a risky or unauthorized tool call.",
   "Omitting step count, cost, latency, and error recovery from the evaluation.",
   "Using a few manual demonstrations instead of a fixed suite that can detect regressions."
  ],
  "related": [
   "what-is-an-ai-agent",
   "how-to-make-ai-agents-reliable-in-production",
   "how-to-make-llm-as-a-judge-reliable"
  ]
 },
 {
  "slug": "how-to-monitor-llm-in-production",
  "q": "How do you monitor an LLM system in production?",
  "desc": "How to monitor an LLM system in production with structured logs, traces, dashboards, alerts, quality checks, and feedback while protecting sensitive user data.",
  "level": "Entry",
  "src": [
   83
  ],
  "testing": "Whether you can define request-level logging, multi-step tracing, operational alerts, quality monitoring, and safe handling of production data.",
  "steps": [
   "Log each request with its prompt version, model, token usage, latency, cost, and outcome.",
   "Trace multi-step calls so the order of model, retrieval, and tool operations is visible.",
   "Build dashboards and alerts for error rate, p95 latency, cost spikes, and quality signals.",
   "Sample conversations for review and track user feedback to identify quality problems.",
   "Redact PII before information is written to logs and restrict access to sensitive records."
  ],
  "sample": [
   "I would monitor an LLM system at three levels: individual requests, multi-step traces, and aggregate service health. For every request, I would log a request identifier, the prompt or template version, model name, token counts, latency, cost, and a structured outcome. Those fields let me connect a user report to the exact call that produced it. I would avoid storing unnecessary prompt content, and I would redact personally identifiable information before any text reaches a log or observability tool.",
   "For an agent or multi-step workflow, request logs are not enough. I would add distributed traces that show each model call, tool call, retrieval step, input, output, and error in the order they occurred. Dashboards would track error rate, p95 latency, token usage, and cost, while alerts would fire for sustained error increases, p95 latency regressions, and abnormal cost spikes. I would be careful to make alerts actionable so responders know which service and version are affected.",
   "Operational logs and traces alone do not establish whether an output was useful. I would sample conversations for periodic human review, track thumbs-up, thumbs-down, and other user feedback, and add quality signals such as schema validity, refusal rates, or retrieval hit rates where they apply. I would segment these metrics by prompt version and model so I can detect a quality regression that averages hide. Finally, I would document retention limits, verify that redaction works, and restrict access to sensitive logs."
  ],
  "followups": [
   [
    "Which production signals should trigger alerts?",
    "I would prioritize sustained error-rate increases, p95 latency regressions, abnormal cost spikes, and sharp changes in quality signals. Each alert should identify the affected service and version."
   ],
   [
    "How do I monitor quality when there are too many conversations to review?",
    "I would combine sampled human review with user feedback and targeted automatic checks such as schema validity, refusal rates, or retrieval hit rates, then segment the results by model and prompt version."
   ],
   [
    "How should monitoring handle sensitive user data?",
    "I would redact PII before logging, minimize the content retained, restrict access, and define retention limits. I would also test that the redaction works across prompts, traces, and error messages."
   ]
  ],
  "mistakes": [
   "Logging only final responses without prompt version, model, token usage, latency, cost, or outcome.",
   "Using aggregate dashboards without request-level logs and traces for multi-step workflows.",
   "Sending an alert for every isolated fluctuation instead of sustained changes that need attention.",
   "Storing raw PII in logs because the observability tool is considered internal."
  ],
  "related": [
   "how-do-you-evaluate-an-llm",
   "what-are-llm-guardrails",
   "how-to-make-ai-agents-reliable-in-production"
  ]
 },
 {
  "slug": "how-to-handle-pii-in-ai-systems",
  "q": "How do you handle PII in AI systems?",
  "desc": "How to handle PII in AI systems using minimization, detection, redaction, encryption, retention limits, deletion workflows, and recall testing for logs.",
  "level": "Mid",
  "src": [
   87
  ],
  "testing": "Whether you can apply PII controls across data collection, model prompts, logs, storage, retention, and deletion while testing redaction effectiveness.",
  "steps": [
   "Minimize the data sent to the AI system and include only fields the feature actually needs.",
   "Detect PII and redact or tokenize it before it enters prompts, logs, or other stored artifacts.",
   "Review provider data-retention and training terms before sending user data.",
   "Encrypt sensitive data at rest and in transit, restrict access, and apply retention limits.",
   "Support deletion requests and test redaction recall, since missed PII can expose sensitive data in logs."
  ],
  "sample": [
   "I would treat PII as a data-minimization problem first, not only as a filtering problem. Before sending data to a model, I need to know whether the prompt actually needs each field, so I remove names, contact details, or account identifiers when they are not necessary. I would also review provider retention and training terms to confirm that submitted data is not retained or used in ways the application cannot accept. No model or provider setting makes unnecessary data safe to collect.",
   "Next, I would detect and handle PII before it reaches prompts, vector stores, traces, or application logs. Detection can cover structured identifiers and patterns such as email addresses, phone numbers, and payment information. Redaction replaces sensitive values with placeholders, while tokenization can create reversible references when the application needs to restore a value later. I would prefer a deterministic rule for well-defined fields and a tested model-based detector for more varied text. Whatever I use, I would keep the original mapping outside the prompt and logs.",
   "Security controls must cover the rest of the data lifecycle. I would encrypt data at rest and in transit, restrict access to sensitive mappings, apply retention limits, and build a workflow for deletion requests across the application, logs, and vector indexes. I would test redaction recall with labeled examples, including obfuscated and unusual formats, because missed PII can expose sensitive data in logs. I would also monitor detection failures and review any change to the pipeline with the same tests."
  ],
  "followups": [
   [
    "What is the difference between redaction and tokenization?",
    "Redaction replaces the sensitive value so it cannot be restored directly. Tokenization substitutes a reference that a separate authorized system may map back to the original value when the application needs it."
   ],
   [
    "How do I test whether my PII redaction works?",
    "I would use a labeled set that includes common identifiers, unusual formats, and obfuscated values, then measure how many sensitive values escaped into prompts and logs. I would review false positives as well."
   ],
   [
    "What should a deletion workflow cover?",
    "It should identify the relevant application records, logs, vector indexes, and retained mappings so the deletion request can be handled consistently rather than only removing one database row."
   ]
  ],
  "mistakes": [
   "Sending raw PII to the model and only redacting it from the displayed answer.",
   "Assuming provider retention and training terms remove the application's own privacy obligations.",
   "Keeping the original PII or a redaction mapping in the same logs as the processed content.",
   "Deploying a detector without testing how often it misses PII."
  ],
  "related": [
   "what-are-llm-guardrails",
   "access-control-in-rag",
   "what-is-rag"
  ]
 }
]

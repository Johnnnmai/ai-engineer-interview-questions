# Batch 2 question pages (generated from seo_pages/batch2 drafts by merge_and_check.py). Same schema as question_pages_data.py.
PAGES = [
 {
  "slug": "pre-training-vs-instruction-tuning-vs-rlhf",
  "q": "What is the difference between pre-training, instruction tuning and RLHF?",
  "desc": "Pre-training vs instruction tuning vs RLHF and DPO: what each LLM training stage adds, how much data it uses, and how to explain it in an interview.",
  "level": "Mid",
  "src": [
   4
  ],
  "testing": "Whether you know what each training stage contributes to a chat model, can explain why a pre-trained model alone is not a helpful assistant, and can compare RLHF with DPO without hand-waving.",
  "steps": [
   "Pre-training: next-token prediction on a very large text corpus. It produces knowledge and fluency, not assistant behavior.",
   "Instruction tuning (supervised fine-tuning, SFT): train on prompt-response pairs so the model follows instructions and a chat format.",
   "Preference tuning: train on comparisons where one answer is better than another, to shape helpfulness, tone and refusals.",
   "Compare the two preference methods: RLHF trains a reward model and optimizes against it with RL (for example PPO) under a KL penalty; DPO optimizes directly on the preference pairs.",
   "Point out the data funnel: each stage uses far less data than the one before, but the data gets more curated."
  ],
  "sample": [
   "I think of it as three stages with different jobs. Pre-training is next-token prediction over trillions of tokens. The model picks up facts, grammar and some reasoning, but if you ask it a question it may just continue the text, because nothing has taught it to behave like an assistant.",
   "Instruction tuning fixes that. We fine-tune on curated prompt-response pairs in a chat format, so the model learns to follow instructions, answer in the expected shape and stop when done. Preference tuning then teaches it which of two plausible answers people prefer. In classic RLHF we fit a reward model on human comparisons and optimize the policy with PPO, with a KL penalty that keeps it close to the SFT model so it does not exploit the reward model. DPO reaches a similar goal with a single supervised-style loss on chosen and rejected pairs, so there is no separate reward model and no RL loop.",
   "Moving down the stages, the datasets get smaller and more carefully curated: pre-training is web scale, SFT is often tens of thousands of examples, preference data is comparisons."
  ],
  "followups": [
   [
    "When would you pick DPO over PPO-style RLHF?",
    "With a small team, offline preference data and a need for stable training. PPO-style RLHF is worth it when you want online exploration or a reusable reward model."
   ]
  ],
  "mistakes": [
   "Saying RLHF teaches the model new knowledge; it mostly shapes behavior that pre-training made possible.",
   "Forgetting the KL penalty and why it exists (reward hacking).",
   "Describing DPO as reinforcement learning; it is a classification-style loss on preference pairs.",
   "Treating instruction tuning and preference tuning as the same step."
  ],
  "related": [
   "what-is-dpo",
   "explain-lora-and-qlora",
   "rag-vs-fine-tuning"
  ]
 },
 {
  "slug": "what-are-scaling-laws",
  "q": "What are LLM scaling laws and how do they change decisions?",
  "desc": "LLM scaling laws explained for interviews: power-law loss, compute-optimal training, about 20 tokens per parameter, and why teams overtrain smaller models.",
  "level": "Senior",
  "src": [
   5
  ],
  "testing": "Whether you understand scaling laws as a planning tool rather than trivia: how they relate model size, data and compute, and how inference cost shifts the choice away from the compute-optimal point.",
  "steps": [
   "State the finding: loss falls smoothly, roughly as a power law, as you add parameters, training tokens and compute.",
   "Give the compute-optimal result: for a fixed training budget, grow parameters and tokens together, roughly 20 tokens per parameter (the 2022 Chinchilla paper).",
   "Say what it implied: many earlier large models were undertrained for their size.",
   "Bring in inference: a model served billions of times is cheaper to run if it is smaller, so teams train smaller models on far more tokens than compute-optimal.",
   "Mention the limit: lower loss does not map one-to-one to every downstream task, so you still evaluate on the tasks you care about."
  ],
  "sample": [
   "Scaling laws say that pre-training loss decreases predictably, close to a power law, as you scale parameters, data and compute. That predictability is what makes them useful: you can run small experiments, fit the curve and estimate what a larger run will reach before spending the budget.",
   "The compute-optimal result from the 2022 Chinchilla work is that for a fixed training budget you should scale parameters and training tokens together, at roughly 20 tokens per parameter. So a 10-billion-parameter model would want around 200 billion tokens. Several earlier models had many parameters but too few tokens.",
   "In practice the decision is not only about training cost. If a model will serve a huge number of requests, every parameter costs money on every request, so it often pays to train a smaller model well past the compute-optimal token count. You spend more on training once and less on inference forever."
  ],
  "followups": [
   [
    "Why would you deliberately train past the compute-optimal point?",
    "Because serving cost dominates over a model's life; a smaller model trained on more tokens is cheaper per request at similar quality."
   ]
  ],
  "mistakes": [
   "Quoting the 20-tokens-per-parameter ratio as a law of nature rather than a compute-optimal estimate under specific assumptions.",
   "Ignoring inference cost when choosing model size.",
   "Assuming lower pre-training loss automatically means better results on your product task.",
   "Confusing parameter count with active parameters in mixture-of-experts models."
  ],
  "related": [
   "what-is-mixture-of-experts",
   "pre-training-vs-instruction-tuning-vs-rlhf",
   "how-to-reduce-llm-inference-cost"
  ]
 },
 {
  "slug": "what-is-tokenization-in-llms",
  "q": "What is tokenization in LLMs and why does it matter?",
  "desc": "Tokenization in LLMs for interviews: BPE and subword tokens, why cost and context are counted in tokens, language differences and odd failure modes.",
  "level": "Entry",
  "src": [
   6
  ],
  "testing": "Whether you know that models see tokens, not characters or words, and can connect that to practical consequences: cost, context limits, multilingual products and strange errors.",
  "steps": [
   "Define it: text is split into subword units by an algorithm such as byte-pair encoding (BPE) or a unigram model (SentencePiece), and each unit maps to an ID.",
   "Cost and limits: pricing, latency and the context window are all counted in tokens.",
   "Languages: the same content can take noticeably more tokens in some non-English languages, which raises cost and uses more context.",
   "Failure modes: counting letters, reversing strings and long-number arithmetic are hard because the model never sees individual characters.",
   "Practical habit: measure token counts with the model's own tokenizer when budgeting prompts."
  ],
  "sample": [
   "Tokenization turns text into the integer IDs the model actually reads. Modern LLMs use subword tokenizers such as BPE: frequent words become a single token, rarer words are split into pieces, and anything can still be represented through byte-level fallbacks.",
   "It matters in three practical ways. First, everything is metered in tokens: price, latency and the context window. Second, token efficiency differs by language and by content type, so a product serving several languages, or a lot of code or JSON, can cost more per request than an English-only estimate suggests. Third, it explains failures that look odd from the outside. A model may miscount the letters in a word or slip on arithmetic with long numbers because those characters are bundled into tokens it cannot look inside.",
   "When I budget a prompt I count with the target model's tokenizer rather than estimating from word counts, because tokenizers differ between model families."
  ],
  "followups": [
   [
    "Why can an LLM fail to count the letters in a word?",
    "It sees tokens, not characters, so the letters inside a token are not directly visible to it."
   ]
  ],
  "mistakes": [
   "Assuming one token equals one word for every language and content type.",
   "Estimating prompt size with one model's tokenizer and deploying on another.",
   "Blaming reasoning for errors that come from tokenization, such as character-level tasks.",
   "Forgetting that output tokens count toward cost and context too."
  ],
  "related": [
   "what-is-a-context-window",
   "explain-the-transformer-architecture",
   "how-to-reduce-llm-inference-cost"
  ]
 },
 {
  "slug": "what-is-a-context-window",
  "q": "What is a context window and how does it affect system design?",
  "desc": "Context window interview answer: what counts toward it, why bigger windows still need retrieval, token budgets per section, and cost and latency trade-offs.",
  "level": "Entry",
  "src": [
   7,
   30
  ],
  "testing": "Whether you treat the context window as a design constraint with a budget, not as a reason to skip retrieval or memory, and whether you know models use long inputs unevenly.",
  "steps": [
   "Define it: the maximum number of tokens the model can attend to in one call, prompt plus generated output.",
   "Costs: longer prompts raise price and time to first token on every call.",
   "Quality: models use long inputs unevenly; facts buried in the middle are used less reliably.",
   "Design: decide what goes in with retrieval, summarization or memory, and give each section a token budget (system, history, retrieved context, output).",
   "Verify: test long-context behavior on your own tasks instead of trusting the advertised maximum."
  ],
  "sample": [
   "The context window is the total number of tokens a model can attend to in one request, which includes the system prompt, conversation history, any retrieved documents and the tokens it generates. If the input fills the window, there is no room left for the answer.",
   "A large window makes some things easier, such as reading a whole contract in one pass, but it does not remove design work. Every extra token adds cost and latency on every call, and models do not use all positions equally well; information in the middle of a long prompt is used less reliably than information at the start or end.",
   "So I design with an explicit budget. For a support assistant I might reserve a fixed slice for the system prompt, cap conversation history and summarize older turns, give retrieved passages the largest share and leave enough room for the output. Retrieval decides what deserves to be in the window; the window size only sets the ceiling."
  ],
  "followups": [
   [
    "If a model supports a million tokens, why still use RAG?",
    "Cost and latency per call, uneven use of long context, and the need for fresh, permission-filtered content all still favor retrieving only what is relevant."
   ]
  ],
  "mistakes": [
   "Forgetting that output tokens share the same window as the prompt.",
   "Stuffing everything into a long window instead of retrieving the relevant parts.",
   "Letting chat history grow without trimming or summarizing.",
   "Trusting the advertised window without testing recall at different positions."
  ],
  "related": [
   "what-is-lost-in-the-middle",
   "what-is-tokenization-in-llms",
   "what-is-rag"
  ]
 },
 {
  "slug": "temperature-vs-top-p",
  "q": "What do temperature and top-p do in an LLM?",
  "desc": "Temperature vs top-p for interviews: how each changes sampling, sensible settings for extraction, code and creative tasks, and why temperature 0 still varies.",
  "level": "Entry",
  "src": [
   8
  ],
  "testing": "Whether you understand sampling mechanically and can pick settings for a task, and whether you know the practical caveat that low temperature does not give strict determinism.",
  "steps": [
   "Temperature: divide the logits by T before softmax; low T sharpens the distribution, high T flattens it.",
   "Top-p (nucleus sampling): sample only from the smallest set of tokens whose cumulative probability reaches p.",
   "Choosing: low temperature (0 to 0.3) for extraction, classification and code; moderate (around 0.7 to 1.0) for brainstorming and creative text.",
   "Tune one knob at a time; changing both makes behavior hard to reason about.",
   "Caveat: even at temperature 0 outputs can differ across runs because of batching and floating-point effects."
  ],
  "sample": [
   "Both settings control how the next token is sampled from the model's probability distribution. Temperature rescales the logits before the softmax. With a temperature near zero the most likely token almost always wins, so output is focused and repeatable; with a higher temperature lower-probability tokens get more chance, so output becomes more varied and also more error-prone.",
   "Top-p trims the distribution instead of reshaping it. With top-p of 0.9 the model keeps the smallest group of tokens that together cover 90% of the probability and samples only from those, which cuts off the long tail of unlikely tokens.",
   "In practice I set temperature by task: close to zero for extraction, classification, SQL or code where there is one right answer, and higher for brainstorming or marketing copy. I usually adjust either temperature or top-p, not both. I also do not promise strict determinism at temperature 0, because batching and floating-point differences can still change outputs slightly; if I need exact repeatability I cache results."
  ],
  "followups": [
   [
    "What is the difference between top-p and top-k?",
    "Top-k keeps a fixed number of tokens; top-p keeps a variable number whose probabilities add up to p, so it adapts to how confident the model is."
   ]
  ],
  "mistakes": [
   "Saying temperature changes what the model knows; it only changes how it samples.",
   "Using high temperature for structured output or code.",
   "Assuming temperature 0 means identical outputs every time.",
   "Tuning temperature and top-p together without a reason."
  ],
  "related": [
   "how-to-get-reliable-json-output-from-an-llm",
   "why-do-llms-hallucinate",
   "what-is-tokenization-in-llms"
  ]
 },
 {
  "slug": "what-is-quantization-in-llms",
  "q": "What is LLM quantization and why does it matter for deployment?",
  "desc": "LLM quantization for interviews: 8-bit and 4-bit weights, memory and throughput gains, GPTQ and AWQ, and why you must re-run task evals after quantizing.",
  "level": "Mid",
  "src": [
   10
  ],
  "testing": "Whether you can explain why fewer bits help serving (memory and bandwidth), name the common methods, and show the engineering discipline of checking quality on your own tasks afterwards.",
  "steps": [
   "Define it: store weights, and sometimes activations or the KV cache, in fewer bits, such as 8-bit or 4-bit integers instead of 16-bit floats.",
   "Memory: roughly 2x smaller at 8-bit and 4x smaller at 4-bit for the weights.",
   "Speed: decoding is usually memory-bandwidth bound, so moving fewer bytes per token often raises throughput.",
   "Methods: post-training quantization such as GPTQ and AWQ keeps quality loss small at 4-bit for many models; QLoRA uses 4-bit weights for fine-tuning.",
   "Risk: quality loss is uneven, often showing first in math, code and long-context tasks, so re-run your evals."
  ],
  "sample": [
   "Quantization means representing model weights with fewer bits. A 7-billion-parameter model in 16-bit needs about 14 GB just for weights; at 4-bit that drops to roughly 3.5 GB plus some overhead for scales. That can be the difference between needing a large GPU and fitting on a smaller one, or between one replica and several per GPU.",
   "It often speeds things up too. During decoding each new token requires reading the weights from memory, so the step is usually limited by memory bandwidth rather than arithmetic. Fewer bytes per weight means more tokens per second, especially at small batch sizes.",
   "For post-training quantization I would start with an established method such as AWQ or GPTQ at 4-bit, or 8-bit if quality is critical, and quantize the KV cache if long contexts are the bottleneck. Then I re-run our task evals, not just a general benchmark, because degradation is uneven: arithmetic, code and long-context retrieval tend to suffer first."
  ],
  "followups": [
   [
    "Weight-only vs weight-and-activation quantization?",
    "Weight-only cuts memory and helps bandwidth-bound decoding; quantizing activations too can speed up compute-bound prefill but is harder to do without quality loss."
   ]
  ],
  "mistakes": [
   "Claiming quantization has no quality cost.",
   "Checking only perplexity or a public benchmark instead of task evals.",
   "Forgetting the KV cache, which can dominate memory at long context.",
   "Assuming 4-bit is always faster; it depends on kernels and hardware support."
  ],
  "related": [
   "what-is-kv-cache",
   "explain-lora-and-qlora",
   "how-to-reduce-llm-inference-cost"
  ]
 },
 {
  "slug": "what-is-mixture-of-experts",
  "q": "What is Mixture of Experts (MoE) and what are its trade-offs?",
  "desc": "Mixture of Experts explained for AI engineer interviews: routers, top-k experts, total vs active parameters, and the memory and serving trade-offs.",
  "level": "Senior",
  "src": [
   12
  ],
  "testing": "Whether you understand sparse activation, can separate total from active parameters, and know the systems costs that make MoE harder to train and serve than a dense model.",
  "steps": [
   "Structure: replace a dense feed-forward block with many expert networks plus a router.",
   "Routing: for each token the router picks the top-k experts (often k = 2) and combines their outputs.",
   "Benefit: total parameters are large but active parameters per token are small, so quality per training FLOP improves.",
   "Costs: all experts must still be held in memory; load-balancing losses are needed so the router does not overuse a few experts.",
   "Serving: expert parallelism adds communication, and batching is less efficient at low traffic because tokens spread across experts."
  ],
  "sample": [
   "In a Mixture of Experts layer the single feed-forward block of a transformer layer is replaced by many experts, each its own feed-forward network, and a small router. For every token the router scores the experts and sends the token to the top few, often two, then mixes their outputs by the router weights. Attention layers are usually still dense.",
   "The appeal is that you get the capacity of a very large model while each token only pays for a fraction of it. A model can have several times more total parameters than active parameters, so for the same training compute it usually reaches better quality than a dense model.",
   "The trade-offs are mostly systems problems. Memory is set by total parameters, because every expert has to be loaded somewhere. Training needs auxiliary load-balancing losses or capacity limits, otherwise a few experts get most tokens. In serving, experts are often split across GPUs, so tokens move between devices, and at low traffic each expert sees small batches, which wastes compute. MoE pays off most at high, steady volume."
  ],
  "followups": [
   [
    "Does an MoE model with 8 experts cost 8 times as much to run?",
    "No; compute per token depends on active experts (for example 2), but memory depends on all experts."
   ]
  ],
  "mistakes": [
   "Saying each expert specializes in a human-readable topic; routing is learned and not necessarily interpretable.",
   "Comparing MoE and dense models by total parameters only.",
   "Ignoring memory: sparse compute does not mean small memory.",
   "Leaving out load balancing."
  ],
  "related": [
   "what-are-scaling-laws",
   "what-is-quantization-in-llms",
   "explain-the-transformer-architecture"
  ]
 },
 {
  "slug": "reasoning-models-vs-chat-models",
  "q": "How do reasoning models differ from standard chat models?",
  "desc": "Reasoning models vs chat models for interviews: RL-trained chains of thought, inference-time compute, when they win, and how to route and budget them.",
  "level": "Mid",
  "src": [
   13
  ],
  "testing": "Whether you know how reasoning models are trained and where they help, and whether you can make a cost-aware product decision rather than defaulting to the strongest model.",
  "steps": [
   "Training: reasoning models are trained, typically with reinforcement learning on tasks with verifiable answers, to think through a long chain of thought before answering.",
   "Inference: they spend more compute per query, so they are slower and cost more.",
   "Strengths: math, code, multi-step planning and problems where checking intermediate steps matters.",
   "Weaknesses: poor value for simple lookups, short rewrites and style tasks.",
   "Product design: route only hard queries to them, set a reasoning budget, and evaluate cost per solved task."
  ],
  "sample": [
   "A standard chat model answers more or less directly after reading the prompt. A reasoning model is trained, typically with reinforcement learning on problems where the answer can be checked, such as math and unit-tested code, to produce a long internal chain of thought first. It learns to break problems down, try approaches and check its own work, which is why it does better on multi-step problems.",
   "The cost is inference-time compute. The hidden reasoning can be many times longer than the visible answer, so latency and price per query go up. For a quick factual lookup or rephrasing an email, that extra thinking adds little.",
   "In a product I would not send everything to a reasoning model. I would route by difficulty: a cheap classifier or rules send hard analytical or coding requests to the reasoning model with a capped reasoning budget, and everything else to a fast chat model. Then I would measure accuracy, latency and cost per successful task on both paths."
  ],
  "followups": [
   [
    "Should you still add chain-of-thought prompts to a reasoning model?",
    "Usually not; it already reasons internally. Clear task instructions and output format matter more."
   ]
  ],
  "mistakes": [
   "Using a reasoning model for every request regardless of cost and latency.",
   "Assuming the visible reasoning is a faithful record of how the answer was produced.",
   "Ignoring time to first token in user-facing flows.",
   "Comparing models on accuracy only, not cost per solved task."
  ],
  "related": [
   "what-is-chain-of-thought-prompting",
   "how-to-reduce-llm-latency",
   "how-to-reduce-llm-inference-cost"
  ]
 },
 {
  "slug": "embedding-model-vs-generative-model",
  "q": "What is the difference between an embedding model and a generative model?",
  "desc": "Embedding model vs generative model for interviews: vectors vs tokens, what each is used for, relative cost, and how they work together in RAG systems.",
  "level": "Entry",
  "src": [
   15
  ],
  "testing": "Whether you can explain the different outputs and jobs of the two model types and show how they combine in a retrieval system.",
  "steps": [
   "Embedding model: maps a piece of text to a fixed-length vector so that similar meanings land close together.",
   "Generative model: predicts and outputs tokens to produce text, code or structured data.",
   "Uses of embeddings: semantic search, clustering, deduplication, classification and recommendations.",
   "Cost: embedding calls are far cheaper and faster, so you can embed a whole corpus once.",
   "Together: in RAG the embedding model finds candidate passages and the generative model reads them and writes the answer."
  ],
  "sample": [
   "An embedding model turns text into a single vector of fixed length, for example a few hundred or a few thousand numbers. It is trained so that texts with similar meaning have vectors that are close by a measure such as cosine similarity. It does not write anything; its output is only useful for comparison.",
   "A generative model produces tokens one at a time. It is what writes the answer, the summary or the SQL query.",
   "They solve different problems and have very different costs. Embeddings are cheap enough to compute for millions of documents at ingestion, which is why they back semantic search, deduplication, clustering and simple classifiers. In a RAG system I embed every chunk once, embed each query at request time, find the nearest chunks, and only then pay for the generative model to read those few chunks and answer."
  ],
  "followups": [
   [
    "Can you use a generative model to create embeddings?",
    "You can take hidden states from it, but dedicated embedding models trained with contrastive objectives usually retrieve better and are much cheaper."
   ]
  ],
  "mistakes": [
   "Saying embeddings store the text; they store a lossy representation used for similarity.",
   "Mixing embeddings from two different models in one index.",
   "Using a generative model for tasks a cheap embedding classifier can handle.",
   "Forgetting to re-embed the corpus when the embedding model changes."
  ],
  "related": [
   "how-to-choose-an-embedding-model",
   "what-is-rag",
   "what-is-hybrid-search"
  ]
 },
 {
  "slug": "what-is-chain-of-thought-prompting",
  "q": "What is chain-of-thought prompting and when does it help?",
  "desc": "Chain-of-thought prompting for interviews: how step-by-step reasoning helps multi-step tasks, its cost, faithfulness limits and how reasoning models change it.",
  "level": "Mid",
  "src": [
   18
  ],
  "testing": "Whether you know when chain-of-thought is worth its cost, can describe how to use it in production, and understand that the written reasoning is not necessarily what drove the answer.",
  "steps": [
   "Define it: ask the model to reason step by step before giving a final answer, or show examples that include reasoning.",
   "Where it helps: multi-step arithmetic, logic, planning and problems with several constraints.",
   "Where it does not: simple lookups, classification with clear labels, short rewrites.",
   "Costs: more output tokens, so higher cost and latency.",
   "Production pattern: separate the reasoning from a final structured answer, and do not treat the reasoning as a faithful explanation."
  ],
  "sample": [
   "Chain-of-thought prompting means getting the model to write intermediate reasoning before the answer, either with an instruction such as asking it to work through the problem step by step, or with few-shot examples that show the reasoning. Because each generated token conditions the next, writing out steps gives the model room to compute what it cannot do in a single jump.",
   "It helps most on tasks with several dependent steps: word problems, scheduling with constraints, multi-hop questions. It adds little to a sentiment label or a fact lookup, and it costs output tokens and latency every time.",
   "In production I ask for the reasoning and a final answer in separate fields, parse only the final field, and often hide the reasoning from users. I also treat the reasoning as a useful debugging aid, not proof of how the model reached its answer, because it may not reflect the real computation. With models trained to reason internally, an explicit chain-of-thought prompt usually adds little."
  ],
  "followups": [
   [
    "How would you show that chain-of-thought helps on your task?",
    "Run the same eval set with and without it and compare accuracy, cost and latency."
   ]
  ],
  "mistakes": [
   "Adding chain-of-thought to every prompt by default.",
   "Parsing the answer out of free-form reasoning instead of a separate field.",
   "Treating the written reasoning as a faithful explanation.",
   "Forgetting the token cost at scale."
  ],
  "related": [
   "reasoning-models-vs-chat-models",
   "how-to-get-reliable-json-output-from-an-llm",
   "how-do-you-evaluate-an-llm"
  ]
 },
 {
  "slug": "how-to-get-reliable-json-output-from-an-llm",
  "q": "How do you get reliable structured JSON output from an LLM?",
  "desc": "Reliable JSON output from LLMs: schema modes and constrained decoding, validation with Pydantic, repair retries, and schema design tips for interviews.",
  "level": "Mid",
  "src": [
   19,
   96
  ],
  "testing": "Whether you rely on enforcement and validation rather than prompt wording alone, and whether you design schemas that the model can fill correctly.",
  "steps": [
   "Enforce the format: use the provider's structured output or JSON-schema mode, or constrained decoding (grammar-guided generation) when self-hosting.",
   "Validate every response against the schema in code, for example with Pydantic or a JSON Schema validator.",
   "Repair on failure: retry once or twice with the validation error included in the prompt, then fall back or escalate.",
   "Design the schema: keep it flat, use enums for categories, make optional fields explicit and allow null instead of forcing guesses.",
   "Monitor the parse failure rate and the rate of empty or default values in production."
  ],
  "sample": [
   "I treat structured output as an engineering problem, not a prompting problem. First I enforce the format at generation time: hosted APIs offer a JSON-schema or structured output mode, and with a self-hosted model I use constrained decoding so only tokens that keep the output valid can be sampled. That removes most syntax errors.",
   "Valid JSON can still be wrong, so I validate the parsed object against a Pydantic model: types, enums, ranges and required fields. If validation fails, I send one repair attempt that includes the original output and the exact validation error, and if that also fails I return a clear error or route to a fallback instead of passing bad data downstream.",
   "Schema design matters as much as enforcement. For an invoice extractor I would use a flat object, an enum for currency, explicit nullable fields for values that may be missing, and a short description per field. If a model is forced to fill a required field it cannot find, it will invent one, so allowing null is safer. I then track parse failures and null rates per field as quality signals."
  ],
  "followups": [
   [
    "Why not just ask for JSON in the prompt?",
    "Prompt-only instructions work most of the time, but at scale you get truncated objects, extra prose and wrong types; enforcement plus validation handles those cases."
   ]
  ],
  "mistakes": [
   "Relying on a prompt instruction alone for production parsing.",
   "Skipping semantic validation because the JSON parsed.",
   "Making every field required, which pushes the model to invent values.",
   "Retrying without telling the model what was wrong.",
   "Using a high temperature for extraction tasks."
  ],
  "related": [
   "what-is-function-calling",
   "temperature-vs-top-p",
   "what-are-llm-guardrails"
  ]
 },
 {
  "slug": "what-is-function-calling",
  "q": "What is function calling (tool calling) in LLMs?",
  "desc": "Function calling explained for AI engineer interviews: tool schemas, the call and result loop, writing good tool descriptions and validating arguments safely.",
  "level": "Mid",
  "src": [
   20,
   44
  ],
  "testing": "Whether you understand who executes what in a tool-calling loop, and whether you know what makes tools easy for a model to use correctly and safely.",
  "steps": [
   "Describe tools: give each a name, a description and JSON-schema parameters.",
   "The model decides: instead of text it returns a structured call with a tool name and arguments.",
   "Your code executes: validate the arguments, run the function, and send the result back as a tool message.",
   "The model continues: it uses the result to answer or makes another call.",
   "Quality and safety: clear descriptions, few overlapping tools, strict argument validation and permissions in code."
  ],
  "sample": [
   "Function calling lets a model ask your application to run code. You send the model a list of tools, each with a name, a plain-language description of when to use it and a JSON schema for its parameters. When the model decides a tool is needed, it returns a structured call such as get_order_status with an order ID, rather than a text reply.",
   "The model never executes anything itself. My code receives the call, validates the arguments against the schema and against business rules, checks that this user is allowed to perform the action, runs the function and sends the result back. The model then either answers or calls another tool.",
   "Most quality problems come from the tool design. I keep the tool set small and non-overlapping, write descriptions that say when to use and when not to use each tool, use enums and clear parameter names, and return compact, structured results with useful error messages so the model can recover. For actions with side effects, such as refunds, I require confirmation outside the model."
  ],
  "followups": [
   [
    "How is function calling different from MCP?",
    "Function calling is the model-side format for requesting a call; MCP is a protocol for exposing and discovering tools across applications."
   ]
  ],
  "mistakes": [
   "Saying the model runs the function.",
   "Exposing dozens of similar tools with vague descriptions.",
   "Trusting model-generated arguments without validation or permission checks.",
   "Returning huge raw payloads that waste context."
  ],
  "related": [
   "what-is-model-context-protocol-mcp",
   "how-to-get-reliable-json-output-from-an-llm",
   "what-is-an-ai-agent"
  ]
 },
 {
  "slug": "how-to-choose-a-chunking-strategy-for-rag",
  "q": "How do you choose a chunking strategy for RAG?",
  "desc": "Chunking strategy for RAG interviews: structure-aware splitting, chunk size and overlap trade-offs, small-to-parent retrieval, and measuring recall.",
  "level": "Mid",
  "src": [
   27,
   94
  ],
  "testing": "Whether you choose chunking from the documents and the questions rather than defaults, and whether you can explain the size trade-off and how to measure it.",
  "steps": [
   "Follow structure: split on headings, sections, paragraphs, code blocks and table rows rather than fixed character counts.",
   "Pick a size range: typically a few hundred tokens with modest overlap, then tune.",
   "Know the trade-off: small chunks match precisely but lose context; large chunks keep context but dilute similarity and cost more tokens.",
   "Use parent retrieval when needed: retrieve small chunks, then pass their parent section to the model.",
   "Decide by measurement: compare recall@k on real questions for each strategy."
  ],
  "sample": [
   "I start from the documents. Policies, manuals and wikis have headings and paragraphs, so I split along that structure and keep the heading path as metadata, for example 'Billing > Refunds > Annual plans'. Code is split by function or class, and tables by row with the header repeated, so each chunk still makes sense when read alone.",
   "Then I choose a size, usually a few hundred tokens with a small overlap. Small chunks give sharper matches because the embedding represents one idea, but the model may not get enough context to answer. Large chunks carry more context but blur the embedding and use more of the prompt. A common compromise is small-to-parent retrieval: match on small chunks, then send the enclosing section to the model.",
   "I do not settle this by intuition. I build a set of real questions with the passages that answer them, index the corpus with two or three strategies, and compare recall@k and final answer quality. The winner is often different for different document types."
  ],
  "followups": [
   [
    "What goes wrong with fixed-size chunking?",
    "It cuts sentences, tables and code mid-way and separates headings from their content, so chunks lose meaning and retrieve poorly."
   ]
  ],
  "mistakes": [
   "Using a library's default chunk size without testing.",
   "Splitting tables and code blocks in the middle.",
   "Dropping headings and document titles that give chunks context.",
   "Judging chunking by answer quality alone instead of retrieval recall."
  ],
  "related": [
   "what-is-rag",
   "how-to-debug-poor-rag-answers",
   "what-is-re-ranking-in-rag"
  ]
 },
 {
  "slug": "what-is-hybrid-search",
  "q": "What is hybrid search and when should you use it?",
  "desc": "Hybrid search for RAG interviews: combining BM25 keyword search with vector search, reciprocal rank fusion, and when exact terms make it the right default.",
  "level": "Mid",
  "src": [
   28,
   95
  ],
  "testing": "Whether you know the blind spots of pure vector search, can explain how lexical and dense results are merged, and know when hybrid is worth the extra complexity.",
  "steps": [
   "Define it: run lexical search (usually BM25) and dense vector search on the same query, then merge the results.",
   "Merge: reciprocal rank fusion (RRF) combines ranked lists without needing comparable scores.",
   "When to use it: queries with exact identifiers, product codes, names, error messages or rare domain terms.",
   "Default: it is a sensible default for enterprise and support search.",
   "Follow with a re-ranker, and measure recall against each method alone."
  ],
  "sample": [
   "Hybrid search runs two retrievers over the same corpus. A lexical retriever such as BM25 scores documents by exact term matches, weighted by how rare the terms are. A dense retriever compares embeddings, so it matches meaning even with different wording. Each one fails where the other is strong: embeddings tend to blur an error code like E1047 or a part number into similar-looking strings, while BM25 misses a paraphrase that shares no words with the query.",
   "To combine them I usually use reciprocal rank fusion: each document gets the sum of 1 / (k + rank) across the two lists, with k often around 60. It works on ranks, so I do not have to calibrate BM25 scores against cosine similarities.",
   "I use hybrid search whenever users type identifiers, names, version numbers or jargon, which covers most enterprise, support and developer search. Then I put a re-ranker on the merged candidates and check on an eval set that hybrid actually beats either retriever alone."
  ],
  "followups": [
   [
    "Why use rank fusion instead of adding the scores?",
    "BM25 scores and cosine similarities are on different, query-dependent scales, so summing them is unstable; ranks are comparable."
   ]
  ],
  "mistakes": [
   "Assuming vector search alone handles exact identifiers well.",
   "Adding raw BM25 and cosine scores together without normalization.",
   "Skipping evaluation of each retriever on its own.",
   "Forgetting that BM25 needs the same text preprocessing at index and query time."
  ],
  "related": [
   "what-is-re-ranking-in-rag",
   "what-is-rag",
   "how-to-choose-an-embedding-model"
  ]
 },
 {
  "slug": "what-is-re-ranking-in-rag",
  "q": "How does re-ranking work in RAG and why use it?",
  "desc": "Re-ranking in RAG for interviews: retrieve wide then re-score with a cross-encoder, why it beats embeddings alone, and how to size candidates and latency.",
  "level": "Mid",
  "src": [
   29
  ],
  "testing": "Whether you understand the bi-encoder vs cross-encoder difference and can place a re-ranker in a pipeline with sensible candidate counts and latency.",
  "steps": [
   "Retrieve wide and cheap: get a candidate set, for example the top 50, from vector, keyword or hybrid search.",
   "Re-score each candidate with a model that reads the query and the passage together, usually a cross-encoder or an LLM.",
   "Keep the top 5 to 10 for the prompt.",
   "Explain why: a cross-encoder sees query and passage jointly, so it judges relevance better than comparing two separately computed embeddings.",
   "Manage cost: it is too slow for the whole corpus, so tune the candidate count against latency."
  ],
  "sample": [
   "Retrieval with embeddings uses a bi-encoder: the query and each document are embedded separately and compared with a similarity score. That is fast enough to search millions of chunks, but each vector is a compressed summary, so the ranking is approximate.",
   "Re-ranking adds a second stage. I take a wide candidate set, say the top 50 from hybrid search, and score every query-passage pair with a cross-encoder, which reads both texts together and can notice whether the passage actually answers the question, including negations and specific conditions. Then I keep the best 5 to 10 for the prompt.",
   "The cost is latency, since the cross-encoder runs once per candidate. I tune the candidate count by looking at recall at 50 versus 100 from the first stage and the re-ranker's latency on our hardware. Putting the strongest passages first also helps because models use the start of the context more reliably."
  ],
  "followups": [
   [
    "Can you use an LLM as the re-ranker?",
    "Yes, it can be more accurate on hard queries, but it is slower and more expensive, so it is usually applied to a small candidate set."
   ]
  ],
  "mistakes": [
   "Re-ranking only the top 5, which leaves the re-ranker nothing to fix.",
   "Running a cross-encoder over the whole corpus.",
   "Not measuring first-stage recall, which caps what re-ranking can achieve.",
   "Ignoring the added latency in user-facing flows."
  ],
  "related": [
   "what-is-hybrid-search",
   "what-is-lost-in-the-middle",
   "how-do-you-evaluate-a-rag-system"
  ]
 },
 {
  "slug": "what-is-lost-in-the-middle",
  "q": "What is the lost in the middle problem in LLMs?",
  "desc": "Lost in the middle explained: why LLMs use facts at the start and end of long contexts more reliably, and the retrieval and ordering fixes interviewers expect.",
  "level": "Senior",
  "src": [
   30
  ],
  "testing": "Whether you know that long-context use is uneven, can explain the practical impact on RAG prompts, and can name concrete mitigations and a way to test them.",
  "steps": [
   "State the finding: models use relevant information at the start or end of a long context more reliably than information in the middle (a 2023 study showed a U-shaped curve).",
   "Impact: stuffing many retrieved chunks into the prompt can bury the one that matters.",
   "Mitigate with fewer, better chunks: retrieve and re-rank so only strong passages go in.",
   "Order deliberately: put the most relevant passage first, and the instructions or question near the end.",
   "Test on your own tasks by placing a known fact at different positions and measuring accuracy."
  ],
  "sample": [
   "Lost in the middle describes a position effect in long prompts. In a 2023 study, models answered questions most accurately when the relevant document was at the beginning or end of the context and noticeably worse when it sat in the middle, even though it was well within the context window. Newer models handle long contexts better, but some position sensitivity often remains.",
   "For RAG, the lesson is that more context is not free. If I paste twenty chunks and the answer is in chunk eleven, the model may miss it or blend it with less relevant text. So I retrieve wide, re-rank, and pass only the top few passages. I put the strongest passage first, keep clear source labels, and restate the question after the context.",
   "I verify the effect on our own model and task with a simple needle-style test: insert a known fact at several positions in realistic contexts of different lengths and plot accuracy by position. That tells me how much context I can use before quality drops."
  ],
  "followups": [
   [
    "Does a bigger context window fix this?",
    "Not by itself; the window sets how much fits, not how evenly the model uses it."
   ]
  ],
  "mistakes": [
   "Treating the advertised context length as usable at full quality.",
   "Sending as many chunks as fit instead of the best few.",
   "Putting the key instructions only in the middle of a long prompt.",
   "Not testing position effects on your own model."
  ],
  "related": [
   "what-is-a-context-window",
   "what-is-re-ranking-in-rag",
   "how-to-debug-poor-rag-answers"
  ]
 },
 {
  "slug": "how-to-choose-an-embedding-model",
  "q": "How do you choose an embedding model?",
  "desc": "How to choose an embedding model for RAG or search: benchmark on your own query pairs, weigh language, domain, length, dimension and cost, and version the index.",
  "level": "Mid",
  "src": [
   34
  ],
  "testing": "Whether you pick embedding models with your own evaluation rather than a leaderboard rank, and whether you think about the operational costs of changing models later.",
  "steps": [
   "Build a small eval set of real queries with the documents that should be retrieved.",
   "Shortlist candidates using public leaderboards such as MTEB as a starting point only.",
   "Compare recall@k and MRR on your eval set.",
   "Weigh practical factors: languages, domain fit, max input length, vector dimension (storage and speed), cost or hosting, and query vs document modes.",
   "Record the model and version with the index, since switching models means re-embedding everything."
  ],
  "sample": [
   "I start with our data, not a leaderboard. I collect one to two hundred real or realistic queries and label which chunks should come back for each. Public leaderboards such as MTEB help me shortlist three or four candidates, but their tasks rarely match our domain, language mix or document style.",
   "For each candidate I index the same chunks and measure recall at 10 and mean reciprocal rank. Then I weigh the practical side. Does it support all our languages? Is the max input length long enough for our chunks? A 3072-dimension vector costs more storage and search time than a 768-dimension one, which matters at hundreds of millions of chunks. Hosted models are easy but send data out; open models need serving but give control. Some models expect different prefixes for queries and documents, and getting that wrong hurts results.",
   "Finally I store the model name and version with the index. Embeddings from different models are not comparable, so a model change means re-embedding the whole corpus, and I plan that as a migration."
  ],
  "followups": [
   [
    "Would you fine-tune an embedding model?",
    "When the domain vocabulary is unusual and you have query-document pairs; measure the gain on held-out queries first."
   ]
  ],
  "mistakes": [
   "Choosing purely by leaderboard rank.",
   "Mixing vectors from two models in one index.",
   "Ignoring max input length, which silently truncates chunks.",
   "Forgetting storage and latency costs of high dimensions."
  ],
  "related": [
   "embedding-model-vs-generative-model",
   "hnsw-vs-ivf",
   "how-to-choose-a-chunking-strategy-for-rag"
  ]
 },
 {
  "slug": "hnsw-vs-ivf",
  "q": "HNSW vs IVF: how do vector indexes trade off recall, speed and memory?",
  "desc": "HNSW vs IVF vector indexes for interviews: graph vs cluster search, recall, latency and memory trade-offs, tuning parameters, and measuring recall@k.",
  "level": "Senior",
  "src": [
   36
  ],
  "testing": "Whether you understand approximate nearest-neighbor search well enough to pick an index for a workload and tune it with measurements.",
  "steps": [
   "Both are approximate nearest-neighbor (ANN) indexes: they trade a little recall for much faster search than exact comparison.",
   "HNSW: a layered proximity graph searched greedily from coarse to fine; high recall and low latency, but high memory and slower builds.",
   "IVF: cluster vectors into lists and search only the nearest few clusters; lower memory, tuned by the number of probes, often combined with product quantization (PQ).",
   "Tune: HNSW with M and efSearch, IVF with the number of lists and nprobe.",
   "Measure recall@k against exact search on a sample, plus latency and memory."
  ],
  "sample": [
   "Exact nearest-neighbor search compares the query with every vector, which is too slow at scale, so we use approximate indexes.",
   "HNSW builds a multi-layer graph where each vector links to its near neighbors. A search starts in a sparse top layer and walks greedily toward the query, dropping to denser layers. It gives excellent recall at low latency and handles inserts well, but the graph links add a lot of memory on top of the vectors, and builds are slower. Raising efSearch improves recall at the cost of latency.",
   "IVF first clusters the vectors, for example into a few thousand lists, and at query time searches only the nprobe closest lists. It uses less memory, and with product quantization the vectors themselves are compressed, which lets billions of vectors fit. The cost is lower recall when the answer sits in a cluster you did not probe, and clusters need retraining as data shifts.",
   "I would use HNSW when the index fits in memory and latency matters most, and IVF-PQ when memory or scale is the constraint. Either way I measure recall@10 against exact search on a sample of queries before choosing parameters."
  ],
  "followups": [
   [
    "What happens to recall if you lower nprobe in IVF?",
    "Search gets faster but recall falls, because fewer clusters are searched."
   ]
  ],
  "mistakes": [
   "Treating ANN results as exact.",
   "Choosing an index without measuring recall against exact search.",
   "Ignoring HNSW memory overhead when sizing machines.",
   "Not retraining IVF centroids after large data changes."
  ],
  "related": [
   "how-to-choose-an-embedding-model",
   "what-is-hybrid-search",
   "what-is-rag"
  ]
 },
 {
  "slug": "access-control-in-rag",
  "q": "How do you enforce access control in a RAG system?",
  "desc": "Access control in RAG for interviews: permission metadata on every chunk, filtering inside retrieval, ACL sync with source systems, and how to test it.",
  "level": "Senior",
  "src": [
   38
  ],
  "testing": "Whether you treat permissions as a retrieval-layer control rather than a prompt instruction, and whether you think about sync, caching and testing.",
  "steps": [
   "Attach permission metadata to every chunk at ingestion: tenant, groups, document ACL, sensitivity.",
   "Filter inside the retrieval query, using the caller's identity, before anything reaches the model.",
   "Never rely on the prompt to hide documents the user should not see.",
   "Keep ACLs in sync with source systems, including revocations, and scope caches by permission.",
   "Test with users who should and should not see each document, and log what was retrieved."
  ],
  "sample": [
   "The rule I follow is that the model should only ever see text the user is allowed to read. So access control belongs in retrieval, not in the prompt. At ingestion I copy the source system's permissions onto each chunk: tenant ID, allowed users or groups, and a sensitivity label.",
   "At query time the application resolves the user's identity and groups and passes them as a filter inside the vector or keyword search, so forbidden chunks are never candidates. Post-filtering after retrieval is weaker, because it can return too few results, and asking the model not to reveal certain documents is not a control at all, since prompt injection or a clever question can extract them.",
   "The hard part is keeping permissions current. When someone loses access to a folder in the source system, the index has to reflect that quickly, so I sync ACL changes separately from content changes. Any cache of answers or retrieved chunks must be keyed by user or permission set. Finally I test with pairs of users, one who should see a document and one who should not, and I log retrieved chunk IDs for audits."
  ],
  "followups": [
   [
    "Pre-filtering vs post-filtering?",
    "Pre-filtering applies permissions in the search itself so top-k is all allowed content; post-filtering drops results afterwards and can leave too few or leak through bugs."
   ]
  ],
  "mistakes": [
   "Relying on the system prompt to hide documents.",
   "Ignoring revocations and stale ACLs.",
   "Sharing a response cache across users with different permissions.",
   "Testing only with an admin account."
  ],
  "related": [
   "what-is-prompt-injection",
   "how-to-cache-llm-responses",
   "design-a-customer-support-chatbot"
  ]
 },
 {
  "slug": "how-to-debug-poor-rag-answers",
  "q": "How do you debug poor RAG answer quality?",
  "desc": "How to debug poor RAG answers in an interview: trace ingestion, parsing, chunking, retrieval, ranking and generation, and fix the earliest failing stage.",
  "level": "Senior",
  "src": [
   40
  ],
  "testing": "Whether you debug systematically by stage instead of rewriting the prompt, and whether you know where RAG usually breaks.",
  "steps": [
   "Collect failing questions and, for each, the document that should answer it.",
   "Ingestion and parsing: was the document indexed, and is its text intact (tables, PDFs, scans)?",
   "Chunking: is the answer inside one sensible chunk with its context?",
   "Retrieval and ranking: did the chunk appear in the top-k, and was it ranked high enough to reach the prompt?",
   "Generation: was it in the prompt and did the model use it? Fix the earliest failing stage, then add the case to the eval set."
  ],
  "sample": [
   "I start by turning complaints into concrete cases: a set of questions with bad answers, and for each one the document and passage that should have answered it. Then I trace each case through the pipeline in order.",
   "Was the document ingested at all, and does the parsed text look right? Broken PDF tables and scanned pages are common culprits. Is the answer in one chunk, or was it split from its heading? If I search the index for that chunk directly, does it appear in the top 50, and where does it land after re-ranking? Did it make it into the final prompt, and did the model actually use it or ignore it?",
   "I fix the earliest stage that fails, because later stages cannot recover from it. In my experience most failures are parsing, chunking or retrieval, not the generator, so rewriting the prompt is usually the last step. Every fixed case goes into the regression set so the same failure does not return."
  ],
  "followups": [
   [
    "The right chunk is retrieved but the answer is still wrong. What next?",
    "Check its position and the amount of competing context, tighten instructions to answer from sources, and evaluate faithfulness on that case."
   ]
  ],
  "mistakes": [
   "Starting by changing the model or prompt.",
   "Debugging without labeled failing cases.",
   "Not inspecting parsed text for tables and PDFs.",
   "Fixing a case without adding it to the eval set."
  ],
  "related": [
   "how-do-you-evaluate-a-rag-system",
   "how-to-choose-a-chunking-strategy-for-rag",
   "what-is-re-ranking-in-rag"
  ]
 },
 {
  "slug": "what-is-the-react-pattern",
  "q": "What is the ReAct pattern for LLM agents?",
  "desc": "ReAct pattern for LLM agents explained: the thought, action, observation loop, why grounding in tool results helps, and the stop and budget controls it needs.",
  "level": "Mid",
  "src": [
   42
  ],
  "testing": "Whether you understand the basic agent loop, why interleaving reasoning with tool results beats reasoning alone, and what controls a production loop needs.",
  "steps": [
   "Define it: ReAct (reason plus act) interleaves a short reasoning step, an action such as a tool call, and an observation of the result, repeated until done.",
   "Why it helps: each step is grounded in real tool output instead of the model's memory, which reduces made-up facts.",
   "Relation to tool calling: modern APIs implement the action step as structured function calls.",
   "Controls: a step limit, a token or cost budget, a clear stop condition and error handling for failed tools.",
   "Alternatives: plan-then-execute when the steps are known up front."
  ],
  "sample": [
   "ReAct is the loop most tool-using agents are built on. The model thinks briefly about what it needs, takes an action such as searching documentation or querying a database, reads the observation that comes back, and decides the next step. It repeats until it can answer or hits a limit.",
   "The value is grounding. A model reasoning alone can drift into confident guesses. In ReAct, each step can be checked against real results: if the search shows the API was renamed, the next thought builds on that rather than on stale training data. The loop also makes behavior easier to debug, because the trace shows what the model tried and what it saw.",
   "In production I implement the action step with native tool calling rather than parsing free text, and I wrap the loop with controls: a maximum number of steps, a cost budget, timeouts and retries for tools, detection of repeated identical calls, and a defined way to stop and hand off. For tasks where the steps are known in advance, I would use a plan-then-execute flow or a fixed workflow instead, since it is cheaper and more predictable."
  ],
  "followups": [
   [
    "How do you stop a ReAct agent from looping?",
    "Cap steps and cost, detect repeated calls with the same arguments, and return a partial result or escalate when limits are hit."
   ]
  ],
  "mistakes": [
   "Describing ReAct as a model rather than a prompting and control pattern.",
   "Running the loop without step or cost limits.",
   "Parsing actions from free text when structured tool calls are available.",
   "Using an open-ended loop for a task with fixed steps."
  ],
  "related": [
   "what-is-an-ai-agent",
   "what-is-function-calling",
   "workflows-vs-agents"
  ]
 },
 {
  "slug": "what-is-model-context-protocol-mcp",
  "q": "What is the Model Context Protocol (MCP)?",
  "desc": "Model Context Protocol (MCP) for interviews: clients, servers, tools, resources and prompts, what problem it solves, and the security issues to discuss.",
  "level": "Mid",
  "src": [
   43
  ],
  "testing": "Whether you can explain what MCP standardizes, how it relates to function calling, and the trust and permission questions it raises.",
  "steps": [
   "Define it: an open protocol, introduced in late 2024, for connecting LLM applications to tools and data sources.",
   "Roles: a host application runs MCP clients that connect to MCP servers.",
   "What servers expose: tools (actions), resources (data to read) and prompts (reusable templates).",
   "Benefit: write an integration once and use it from any compatible application, instead of custom glue per app.",
   "Risks: servers are code you trust with data and actions, so review them, scope credentials and watch for prompt injection in returned content."
  ],
  "sample": [
   "MCP is an open protocol for connecting LLM applications to external tools and data. Before it, every application wrote its own integration for each service, so connecting several apps to several systems meant a lot of one-off glue code. With MCP, a service exposes an MCP server once and any compatible host, such as a chat app or an IDE assistant, can connect to it through an MCP client.",
   "A server can expose three things: tools the model can call, resources the application can read as context, and prompt templates. The host discovers what is available at runtime and passes tool definitions to the model. Function calling is still how the model asks for an action; MCP standardizes how those tools are described, discovered and invoked across applications.",
   "The main interview point I would add is security. An MCP server can read data and take actions, so I treat installing one like adding a dependency with credentials: use trusted or reviewed servers, give each the narrowest scopes, require confirmation for destructive actions, and treat text returned by tools as untrusted input that could contain injected instructions."
  ],
  "followups": [
   [
    "Does MCP replace function calling?",
    "No; the model still requests calls in its function-calling format, while MCP standardizes how the host finds and runs the tools."
   ]
  ],
  "mistakes": [
   "Calling MCP a model feature rather than a protocol.",
   "Ignoring the trust and permission model of third-party servers.",
   "Treating tool output as trusted instructions.",
   "Confusing resources (read context) with tools (actions)."
  ],
  "related": [
   "what-is-function-calling",
   "what-is-prompt-injection",
   "what-is-an-ai-agent"
  ]
 },
 {
  "slug": "how-to-make-ai-agents-reliable-in-production",
  "q": "How do you make AI agents reliable in production?",
  "desc": "Making AI agents reliable in production: narrow scope, validated tools, step and cost limits, human approval for risky actions, tracing and trajectory evals.",
  "level": "Senior",
  "src": [
   45
  ],
  "testing": "Whether you design agents as systems with limits, checks and observability, rather than trusting a capable model to behave.",
  "steps": [
   "Narrow the scope: a clear task, a small set of well-designed tools, and workflows where steps are predictable.",
   "Validate at boundaries: schema and business-rule checks on every tool call, idempotent actions and safe retries.",
   "Bound the loop: step limits, cost budgets, timeouts and loop detection.",
   "Gate risky actions: human approval for payments, deletions or external messages, and least-privilege credentials.",
   "Observe and evaluate: trace every step, evaluate full trajectories on a test suite, and review failures in production."
  ],
  "sample": [
   "Reliability comes from the system around the model. I start by narrowing scope: one well-defined job, a handful of tools with clear descriptions, and fixed workflow steps wherever the path is predictable, leaving the open-ended loop only where it is really needed. Small per-step error rates compound over a long chain, so fewer and simpler steps matter.",
   "Every tool call passes through validation: arguments against the schema, values against business rules, and the user's permissions. Actions are idempotent where possible, so a retry does not refund twice. The loop has a step limit, a cost budget and timeouts, and it detects repeated calls. Anything irreversible, such as sending money, deleting data or emailing a customer, needs explicit human approval, and the agent's credentials allow only what the task requires.",
   "Then I make it observable. Every run is traced: prompts, tool calls, arguments, results, cost and latency. I keep a suite of realistic tasks and score whole trajectories, not just final answers, including whether the agent used the right tools and stopped correctly. Production failures are reviewed and added to that suite."
  ],
  "followups": [
   [
    "What do you evaluate besides the final answer?",
    "Tool choice, argument correctness, number of steps, cost, policy violations and whether the agent stopped or escalated appropriately."
   ]
  ],
  "mistakes": [
   "Giving an agent broad tools and credentials for convenience.",
   "No step, cost or time limits.",
   "Letting the model take irreversible actions without approval.",
   "Evaluating only final answers, not trajectories.",
   "Having no tracing, so failures cannot be diagnosed."
  ],
  "related": [
   "workflows-vs-agents",
   "what-is-an-ai-agent",
   "what-are-llm-guardrails"
  ]
 },
 {
  "slug": "how-to-handle-memory-in-ai-agents",
  "q": "How do you handle memory in AI agents?",
  "desc": "Memory in AI agents for interviews: short-term context, summaries, long-term stores with retrieval, structured user facts, and privacy and staleness rules.",
  "level": "Mid",
  "src": [
   46
  ],
  "testing": "Whether you can separate the kinds of memory an agent needs, choose a storage approach for each, and deal with relevance, staleness and privacy.",
  "steps": [
   "Short-term (working) memory: the current conversation and task state inside the context window.",
   "Compression: summarize or trim older turns when the window fills.",
   "Long-term memory: store facts or past episodes outside the model and retrieve the relevant ones per request.",
   "Structured state: keep user preferences and task progress in a database, not just as text.",
   "Governance: decide what to save, let users view and delete it, expire stale facts and keep data scoped per user."
  ],
  "sample": [
   "I split memory into a few layers. Working memory is what sits in the context window right now: recent messages, the current plan and tool results. When it grows too large, I keep the last several turns verbatim and replace older ones with a running summary, so the important decisions survive without the full transcript.",
   "Long-term memory lives outside the model. Some of it is structured, such as a user's timezone, preferred language or the status of an open ticket, and that belongs in a normal database with clear fields. Some of it is unstructured, such as notes from past sessions, which I store as text with embeddings and retrieve by relevance and recency when a new request comes in. Only the few relevant memories go into the prompt.",
   "The design questions are mostly about policy. What is worth saving? I prefer explicit, durable facts over saving everything. How do we handle conflicts and stale facts? Newer facts win and old ones expire. And privacy: memory is scoped per user, users can see and delete it, and sensitive data is not stored without a reason."
  ],
  "followups": [
   [
    "Why not keep the full history in a long context window?",
    "Cost and latency grow every turn, quality drops on long contexts, and old irrelevant turns distract the model."
   ]
  ],
  "mistakes": [
   "Treating memory as one big vector store for everything.",
   "Saving every message without a policy.",
   "Letting stale facts override newer ones.",
   "Ignoring user visibility, deletion and per-user isolation."
  ],
  "related": [
   "what-is-a-context-window",
   "what-is-an-ai-agent",
   "how-to-make-ai-agents-reliable-in-production"
  ]
 },
 {
  "slug": "single-agent-vs-multi-agent",
  "q": "Single agent vs multi-agent systems: when is multi-agent worth it?",
  "desc": "Single agent vs multi-agent systems: why to start with one agent, when parallel or specialized sub-agents help, and the cost and debugging trade-offs.",
  "level": "Senior",
  "src": [
   47
  ],
  "testing": "Whether you resist adding complexity without evidence, and whether you know the specific conditions under which splitting work across agents pays off.",
  "steps": [
   "Default: start with a single agent and a good tool set; it is cheaper, faster and easier to debug.",
   "Multi-agent helps when work splits into independent parallel parts, such as researching several sources at once.",
   "It also helps when sub-tasks need very different tools, permissions or instructions that would crowd one prompt.",
   "Costs: more tokens, more latency from hand-offs, lost context between agents and harder debugging.",
   "Decide by evaluation: compare quality, cost and latency of both designs on the same tasks."
  ],
  "sample": [
   "I start with a single agent unless there is a clear reason not to. One agent with well-designed tools keeps all context in one place, costs less and is much easier to trace when something goes wrong.",
   "Multi-agent setups earn their cost in a few situations. The clearest is parallel work: a research task that needs to read ten sources can fan out to sub-agents, each reading in its own context, while an orchestrator combines their findings. Another is separation of concerns: if one part of the job needs database write access and another only reads public pages, separate agents with separate permissions and focused instructions are safer and simpler than one huge prompt.",
   "The costs are real. Total token use can grow several times, hand-offs lose context, agents can disagree or duplicate work, and failures are harder to locate. So I would prototype both designs on the same evaluation tasks and switch to multi-agent only when it clearly improves quality or speed enough to justify the extra cost."
  ],
  "followups": [
   [
    "How do agents share information in a multi-agent design?",
    "Usually through the orchestrator passing compact summaries or a shared, structured state, not full transcripts."
   ]
  ],
  "mistakes": [
   "Choosing multi-agent because it sounds more advanced.",
   "Ignoring the multiplied token cost.",
   "Passing full transcripts between agents instead of focused summaries.",
   "No tracing across agents, so failures cannot be located."
  ],
  "related": [
   "workflows-vs-agents",
   "what-is-an-ai-agent",
   "how-to-make-ai-agents-reliable-in-production"
  ]
 },
 {
  "slug": "workflows-vs-agents",
  "q": "Workflows vs agents: how do you decide?",
  "desc": "Workflows vs agents for AI engineer interviews: fixed code paths vs model-directed loops, decision criteria, hybrids, and why predictability usually wins.",
  "level": "Mid",
  "src": [
   52
  ],
  "testing": "Whether you can choose the simplest architecture that solves the task, and explain the predictability, cost and testing differences.",
  "steps": [
   "Workflow: code defines the steps (classify, retrieve, draft, check); the LLM fills specific steps.",
   "Agent: the model decides which steps to take and in what order, using tools in a loop.",
   "Choose a workflow when the path is known: it is cheaper, faster, easier to test and to audit.",
   "Choose an agent when the path depends on what is discovered, such as open-ended research or debugging.",
   "Hybrid: a workflow with one bounded agentic step is often the best fit."
  ],
  "sample": [
   "The difference is who controls the path. In a workflow my code decides the sequence: for example, classify the ticket, retrieve the policy, draft a reply, check it against rules, send it for review. The model does specific jobs inside fixed steps. In an agent, the model decides what to do next, which tool to call and when it is finished.",
   "I default to workflows when I can write the steps down, because they are predictable. Each step can be tested on its own, costs and latency are bounded, and it is easy to explain to compliance what happened. Agents make sense when the next step genuinely depends on what was found, such as investigating a production incident, where you cannot know in advance which logs or services matter.",
   "Most real systems end up hybrid: a workflow that handles routing, permissions and final checks, with one bounded agentic step inside it, such as research with a step limit. I would start with the workflow version, measure where it fails, and add autonomy only where that failure is about needing flexible steps."
  ],
  "followups": [
   [
    "Give an example where an agent clearly beats a workflow.",
    "Debugging a failing build across an unfamiliar codebase, where each finding determines the next file or command."
   ]
  ],
  "mistakes": [
   "Building an agent for a task with fixed steps.",
   "Assuming agents are always more capable.",
   "Forgetting testing and audit requirements.",
   "Not bounding the agentic part of a hybrid."
  ],
  "related": [
   "single-agent-vs-multi-agent",
   "what-is-the-react-pattern",
   "how-to-make-ai-agents-reliable-in-production"
  ]
 },
 {
  "slug": "how-to-build-a-fine-tuning-dataset",
  "q": "How do you build a fine-tuning dataset?",
  "desc": "How to build a fine-tuning dataset: define the behavior, collect real inputs, write high-quality outputs, dedupe, balance, hold out an eval set and iterate.",
  "level": "Mid",
  "src": [
   54
  ],
  "testing": "Whether you know that data quality and coverage drive fine-tuning results, and whether you follow a disciplined process including a held-out evaluation.",
  "steps": [
   "Define the target behavior and output format precisely, with a written spec.",
   "Collect real inputs from logs or users, covering common cases, edge cases and refusals.",
   "Produce excellent outputs: expert-written, or model-generated and then reviewed.",
   "Clean: deduplicate, remove personal data, fix inconsistencies and balance categories.",
   "Hold out an eval set before training, start small (hundreds to a few thousand examples), train, and iterate on the failures."
  ],
  "sample": [
   "I begin by writing down exactly what the model should do: the task, the output format, the tone and how it should handle cases it cannot answer. That spec becomes the guide for everyone producing examples.",
   "Inputs come from reality wherever possible, such as anonymized production logs, so the distribution matches what the model will see, and I deliberately add edge cases and examples where the right answer is to decline or ask for more information. For outputs, quality beats quantity: a few hundred carefully reviewed examples often beat thousands of noisy ones. Generating drafts with a stronger model and having experts correct them is a good way to scale.",
   "Then I clean: remove near-duplicates, strip personal data, make formats consistent and check that no single category dominates. Before training I split off an eval set and make sure no near-duplicates leak across the split. After a first training run, I read the eval failures, find what the data is missing and add targeted examples. Each version of the dataset is tracked so results can be reproduced."
  ],
  "followups": [
   [
    "How many examples do you need?",
    "For format or style, often a few hundred good examples; harder behaviors need more, and the eval curve tells you when more data stops helping."
   ]
  ],
  "mistakes": [
   "Collecting lots of data before defining the target behavior.",
   "Using synthetic outputs without review.",
   "Letting near-duplicates leak between train and eval sets.",
   "Leaving out refusal and edge cases."
  ],
  "related": [
   "rag-vs-fine-tuning",
   "explain-lora-and-qlora",
   "what-is-catastrophic-forgetting"
  ]
 },
 {
  "slug": "what-is-catastrophic-forgetting",
  "q": "What is catastrophic forgetting and how do you limit it?",
  "desc": "Catastrophic forgetting in LLM fine-tuning: why narrow training erodes general skills, and limiting it with LoRA, data mixing, low learning rates and evals.",
  "level": "Mid",
  "src": [
   55
  ],
  "testing": "Whether you know fine-tuning can damage existing capabilities and can name practical ways to prevent and detect it.",
  "steps": [
   "Define it: training on a narrow task overwrites weights that supported other skills, so general ability or instruction following drops.",
   "Use parameter-efficient methods such as LoRA, which leave the base weights frozen.",
   "Mix in general or replay data alongside the task data.",
   "Train gently: lower learning rates, fewer epochs, early stopping.",
   "Measure: run general capability and safety evals before and after, not just the target task."
  ],
  "sample": [
   "Catastrophic forgetting is when fine-tuning on a new, narrow task makes the model worse at things it used to do. The gradients from the new data move shared weights without any signal to preserve other skills. A model tuned hard on medical summaries, for example, might become worse at following general instructions, or lose some of its safety behavior.",
   "I limit it in a few ways. Parameter-efficient fine-tuning such as LoRA trains small adapter weights while the base weights stay frozen, which reduces drift. I mix a portion of general instruction data, or examples of the original behaviors, into the training set so the model keeps practicing them. And I train conservatively, with a modest learning rate, a small number of epochs and early stopping based on a validation set.",
   "Most importantly, I measure it. Before and after training, I run the task eval plus a regression suite that covers general instruction following, reasoning and safety refusals. A fine-tune that improves the target task by a few points but breaks refusals is not shippable."
  ],
  "followups": [
   [
    "Does LoRA prevent forgetting completely?",
    "No; it reduces it, but the adapted model can still behave worse on other tasks, so regression evals remain necessary."
   ]
  ],
  "mistakes": [
   "Only evaluating the target task after fine-tuning.",
   "Training many epochs on a small narrow dataset.",
   "Assuming LoRA removes the risk entirely.",
   "Forgetting safety behavior as a capability that can regress."
  ],
  "related": [
   "explain-lora-and-qlora",
   "how-to-build-a-fine-tuning-dataset",
   "rag-vs-fine-tuning"
  ]
 },
 {
  "slug": "what-is-model-distillation",
  "q": "What is model distillation and when would you use it?",
  "desc": "Model distillation for AI engineer interviews: training a small student on a large teacher's outputs, when it cuts cost and latency, and its licensing limits.",
  "level": "Mid",
  "src": [
   56
  ],
  "testing": "Whether you understand how distillation works for LLMs, can name the conditions where it pays off, and know the practical limits including licensing terms.",
  "steps": [
   "Define it: train a smaller student model to imitate a larger teacher model's outputs.",
   "Methods: train on the teacher's generated responses, or match its probability distributions when you have access to logits.",
   "When to use it: a narrow, high-volume task where the large model works well but costs too much or is too slow.",
   "Process: generate teacher outputs on real inputs, filter for quality, fine-tune the student, compare on a held-out eval.",
   "Limits: the student rarely matches the teacher outside the task, and model terms of use may restrict training on outputs."
  ],
  "sample": [
   "Distillation transfers behavior from a large teacher model to a smaller student. For LLMs the most common version is simple: run the teacher on a large set of realistic inputs, keep the good responses, and fine-tune the student on them. If you control the teacher you can also train the student to match its full token probability distributions, which carries more information than a single answer.",
   "I would use it when a strong model handles a well-defined task, such as classifying support tickets or extracting fields from invoices, but serving it at our volume costs too much or adds too much latency. A distilled small model can often get close to the teacher on that one task at a fraction of the cost per request.",
   "I would validate it on a held-out set scored against ground truth, not just against teacher agreement, because the student inherits the teacher's errors. I would also watch the edge cases, which small models handle worse, and check the teacher's license, since some providers restrict using outputs to train competing models."
  ],
  "followups": [
   [
    "Distillation vs quantization?",
    "Quantization shrinks the same model's numeric precision; distillation trains a different, smaller model. They can be combined."
   ]
  ],
  "mistakes": [
   "Expecting the student to match the teacher on general tasks.",
   "Evaluating only agreement with the teacher.",
   "Using unfiltered teacher outputs.",
   "Ignoring the teacher model's terms of use."
  ],
  "related": [
   "how-to-reduce-llm-inference-cost",
   "what-is-quantization-in-llms",
   "how-to-build-a-fine-tuning-dataset"
  ]
 },
 {
  "slug": "what-is-dpo",
  "q": "What is DPO (Direct Preference Optimization)?",
  "desc": "DPO explained for AI engineer interviews: learning from chosen and rejected pairs without a reward model, the beta setting, data needs and comparison with PPO.",
  "level": "Senior",
  "src": [
   57
  ],
  "testing": "Whether you understand what DPO optimizes, how it differs from reward-model RLHF, and what makes preference data good.",
  "steps": [
   "Data: each example has a prompt, a chosen response and a rejected response.",
   "Objective: raise the probability of chosen responses relative to rejected ones, measured against a frozen reference model.",
   "No separate reward model and no RL loop, so training is simpler and more stable.",
   "Beta controls how far the model may move from the reference: higher beta keeps it closer.",
   "Data quality matters most: clear, consistent preferences that reflect the behavior you want."
  ],
  "sample": [
   "DPO is a way to align a model with preferences without the full RLHF machinery. Classic RLHF trains a reward model on human comparisons, then uses reinforcement learning such as PPO to maximize that reward while a KL penalty keeps the policy close to the starting model. DPO shows that the same goal can be written as a simple loss on preference pairs.",
   "Each training example is a prompt with a chosen and a rejected answer. The loss pushes up the log-probability of the chosen answer relative to the rejected one, with both measured against a frozen reference model, usually the SFT model. A beta setting controls the strength of that anchoring: higher beta keeps the model closer to the reference. In practice it trains like supervised fine-tuning, with one model plus a reference, which is cheaper and much easier to tune than PPO.",
   "The quality of the pairs drives the result. I want rejected answers that are plausible but worse in a specific way, consistent labeling guidelines, and coverage of the behaviors I care about. I also watch for side effects such as longer answers, since length often correlates with preference labels."
  ],
  "followups": [
   [
    "When might PPO-style RLHF still be preferred?",
    "When you want online exploration with fresh samples or a reusable reward model across many training runs."
   ]
  ],
  "mistakes": [
   "Calling DPO reinforcement learning with a reward model.",
   "Forgetting the reference model in the loss.",
   "Using rejected answers that are obviously bad, which teaches little.",
   "Ignoring length bias in preference data."
  ],
  "related": [
   "pre-training-vs-instruction-tuning-vs-rlhf",
   "how-to-build-a-fine-tuning-dataset",
   "explain-lora-and-qlora"
  ]
 },
 {
  "slug": "how-to-make-llm-as-a-judge-reliable",
  "q": "How do you make LLM-as-a-judge evaluation reliable?",
  "desc": "Making LLM-as-a-judge reliable: specific rubrics, pairwise comparisons with swapped order, bias checks, and calibrating the judge against human labels.",
  "level": "Senior",
  "src": [
   63
  ],
  "testing": "Whether you treat an LLM judge as a measurement instrument that needs calibration, and know its common biases and how to control them.",
  "steps": [
   "Write a specific rubric with one criterion per score and concrete examples of each score.",
   "Prefer pairwise or binary judgments over vague 1-10 scales.",
   "Control known biases: position (swap the order and average), length and self-preference.",
   "Ask for a short justification before the score, and use a low temperature.",
   "Calibrate against human labels on a sample, report agreement, and re-check when the judge model or prompt changes."
  ],
  "sample": [
   "An LLM judge is useful because it scales, but it is a measurement tool, so I calibrate it like one. First, the rubric: instead of asking whether an answer is good, I ask narrow questions such as whether every claim is supported by the provided sources, yes or no, with examples of passing and failing answers. One criterion per judgment is more reliable than a combined score.",
   "Second, the format. Binary or pairwise judgments are more consistent than a 1-to-10 scale. For pairwise comparisons I run each pair twice with the order swapped, because judges tend to favor one position, and count a win only when both orders agree. I also watch for length bias and for a judge favoring outputs from its own model family.",
   "Third, calibration. A domain expert labels a sample of a few hundred cases, and I measure agreement between the judge and the expert, for example with Cohen's kappa. If agreement is low, I fix the rubric before trusting any numbers. I version the judge prompt and model, and re-run calibration whenever either changes."
  ],
  "followups": [
   [
    "What agreement level is good enough?",
    "Close to the agreement between two human raters on the same task; if humans disagree a lot, the rubric needs work first."
   ]
  ],
  "mistakes": [
   "Using a vague overall quality score.",
   "Not swapping positions in pairwise comparisons.",
   "Trusting the judge without measuring agreement with humans.",
   "Changing the judge model mid-experiment."
  ],
  "related": [
   "how-do-you-evaluate-an-llm",
   "how-to-ab-test-an-ai-feature",
   "how-do-you-evaluate-a-rag-system"
  ]
 },
 {
  "slug": "how-to-ab-test-an-ai-feature",
  "q": "How do you A/B test an AI feature?",
  "desc": "How to A/B test an AI feature: offline evals first, a user-level primary metric, guardrail metrics, enough sample size, and handling noisy model outputs.",
  "level": "Senior",
  "src": [
   65,
   64
  ],
  "testing": "Whether you can connect offline evaluation with online experiments and choose metrics that reflect user value rather than model scores.",
  "steps": [
   "Gate with offline evals first so only candidates that pass reach users.",
   "Pick one primary metric tied to user value, such as task success or resolution without escalation.",
   "Add guardrail metrics: latency, cost per request, complaints, safety flags.",
   "Randomize by user, size the test for the effect you care about, and fix the duration in advance.",
   "Analyze honestly: avoid peeking, check segments, and read sampled conversations alongside the numbers."
  ],
  "sample": [
   "I treat it as two stages. Offline, the new prompt or model has to beat the current one on our eval suite without regressions on safety or format. Only then does it go to an online test, because offline scores do not fully predict what users do.",
   "Online, I pick one primary metric that reflects real value. For a support assistant, that could be the share of conversations resolved without a human agent, or for a writing feature, the share of suggestions users accept and keep. Thumbs-up rates are useful but sparse and biased toward people who bother to click. I add guardrails: p95 latency, cost per request, escalation and complaint rates, and safety flags. A variant that wins on the primary metric but doubles cost or latency needs a separate decision.",
   "For the mechanics, I randomize at the user level so people get a consistent experience, estimate the sample size needed to detect a meaningful lift, and set the duration before starting to avoid stopping on a lucky day. Afterwards I check key segments and read a sample of conversations from each arm, since numbers alone can hide why a variant won."
  ],
  "followups": [
   [
    "Why randomize by user instead of by request?",
    "Per-request switching gives users an inconsistent experience and contaminates behavioral metrics such as retention."
   ]
  ],
  "mistakes": [
   "Skipping offline evaluation and testing everything live.",
   "Using model scores as the primary online metric.",
   "Stopping the test as soon as it looks significant.",
   "Ignoring cost and latency guardrails."
  ],
  "related": [
   "how-do-you-evaluate-an-llm",
   "how-to-make-llm-as-a-judge-reliable",
   "design-a-customer-support-chatbot"
  ]
 },
 {
  "slug": "what-is-benchmark-contamination",
  "q": "What is benchmark contamination and why does it matter?",
  "desc": "Benchmark contamination explained: test data in training sets, why it inflates scores, how to detect it, and why private task evals matter for model choice.",
  "level": "Mid",
  "src": [
   67
  ],
  "testing": "Whether you read public benchmark scores critically and know how to protect your own evaluation from the same problem.",
  "steps": [
   "Define it: benchmark questions or answers appear in a model's training data, so the score measures memory, not ability.",
   "How it happens: benchmarks are published online and web-scale crawls pick them up, directly or through paraphrases.",
   "Effect: inflated scores and misleading model comparisons.",
   "Detection: n-gram overlap checks, testing on rephrased or newly written items, and comparing with performance on fresh data.",
   "Protection: keep a private eval set built from your own tasks and refresh it over time."
  ],
  "sample": [
   "Benchmark contamination means a model has seen the test during training. Popular benchmarks are posted on the web along with discussions of the answers, and large training crawls pick them up. Then a high score may partly reflect memorization rather than the skill the benchmark was designed to measure.",
   "It matters because teams choose models based on those numbers. If one model's score is inflated by contamination, it can look better than another model that would actually perform better on new problems. Signs include a model doing much better on an old benchmark than on a freshly written one of similar difficulty, or getting worse when questions are lightly reworded.",
   "In practice I use public benchmarks only to shortlist models. The decision is made on a private eval set built from our own tasks, ideally from real user inputs, which is not published anywhere. I keep it out of any data used for fine-tuning, add new cases from production regularly, and keep a frozen hold-out portion that is never used while tuning prompts so I am not slowly overfitting to it myself."
  ],
  "followups": [
   [
    "Can your own eval set get contaminated?",
    "Yes, if it leaks into fine-tuning data or you tune prompts against it repeatedly; keep a frozen hold-out portion."
   ]
  ],
  "mistakes": [
   "Choosing a model purely from leaderboard scores.",
   "Publishing or sharing your private eval set.",
   "Tuning prompts on the same set used for the final decision.",
   "Assuming contamination only means exact copies; paraphrases count too."
  ],
  "related": [
   "how-do-you-evaluate-an-llm",
   "how-to-make-llm-as-a-judge-reliable",
   "how-to-ab-test-an-ai-feature"
  ]
 },
 {
  "slug": "design-a-customer-support-chatbot",
  "q": "Design an LLM customer-support assistant for a SaaS company",
  "desc": "System design interview answer for an LLM customer-support assistant: intake, RAG over help docs, account tools, escalation, guardrails, evals and metrics.",
  "level": "Senior",
  "src": [
   71
  ],
  "testing": "Whether you can structure an end-to-end LLM system: requirements, architecture, safe actions, escalation, evaluation and metrics, with sensible trade-offs.",
  "steps": [
   "Clarify requirements: channels, languages, volume, which actions are allowed, latency target and when to hand off to humans.",
   "Architecture: classify intent, retrieve from help docs and past resolved tickets, and call account tools with the user's permissions.",
   "Generate grounded answers with citations; route low-confidence or sensitive cases to a human with a summary.",
   "Guardrails: no unapproved refunds or account changes, PII handling, injection-resistant tool use.",
   "Evaluate offline on real tickets, then track resolution rate, escalation quality, customer satisfaction, cost and latency."
  ],
  "sample": [
   "I would start by asking what it should handle: common how-to questions only, or account-specific requests such as billing status? Which languages and channels, what volume, and which actions can it take without a human? Let us say chat on the web app, English first, with read-only account access and refunds handled by people.",
   "The flow: a fast intent classifier routes greetings, how-to questions, account questions and complaints. For how-to questions, hybrid retrieval over help articles and resolved tickets feeds a model that answers with links to sources. For account questions, the assistant calls tools such as get_subscription with the logged-in user's identity, so it can only see that customer's data. If confidence is low, the customer asks for a person, or the topic is sensitive, like cancellations or legal issues, it hands off to an agent with a short summary so the customer does not repeat themselves.",
   "For safety, actions with side effects go through approval, tool outputs and documents are treated as untrusted, and personal data is masked in logs. Before launch I would evaluate on a few hundred historical tickets for correctness, groundedness and correct escalation, then roll out gradually and track resolution without escalation, reopen rate, satisfaction, cost per conversation and latency."
  ],
  "followups": [
   [
    "How do you keep answers current when docs change?",
    "Re-index on document updates, show source links, and flag answers whose sources were recently changed or removed."
   ]
  ],
  "mistakes": [
   "Jumping to the model choice before clarifying scope and allowed actions.",
   "No escalation path or a hand-off that loses context.",
   "Letting the model take account actions without permission checks.",
   "Measuring only deflection instead of real resolution."
  ],
  "related": [
   "what-is-rag",
   "access-control-in-rag",
   "what-are-llm-guardrails"
  ]
 },
 {
  "slug": "design-an-llm-gateway",
  "q": "How would you design an LLM gateway for a company?",
  "desc": "LLM gateway system design: one API across providers, auth and quotas, routing and fallbacks, caching, logging with redaction, cost tracking and policy controls.",
  "level": "Senior",
  "src": [
   75
  ],
  "testing": "Whether you can design shared platform infrastructure for LLM use: reliability, cost control, security and observability across many teams.",
  "steps": [
   "Unified API: one interface for many providers and self-hosted models, so teams do not integrate each one.",
   "Access control: per-team keys, quotas, rate limits and budgets.",
   "Routing: choose models by policy, with fallbacks on errors and timeouts, and retries with backoff.",
   "Efficiency: response and prompt caching, and streaming passthrough.",
   "Governance and observability: logging with PII redaction, cost attribution per team, data-residency rules and dashboards."
  ],
  "sample": [
   "A gateway sits between internal applications and model providers. Its first job is a single API, often OpenAI-compatible, that can reach several hosted providers and our own models. Teams integrate once, and the platform team can add or swap models without every application changing code.",
   "Second is control. Each team gets its own credentials, quotas, rate limits and monthly budget, and provider keys never leave the gateway. Routing policies decide which models a team may use and where traffic goes: for example, a cheaper model by default, a stronger one for specific use cases, and automatic fallback to another provider when one returns errors or exceeds a latency threshold. Retries use backoff and respect provider rate limits.",
   "Third is efficiency and governance. Exact-match caching and provider prompt caching cut cost on repeated requests. Streaming is passed through without buffering. Every request is logged with team, model, tokens, cost and latency, with personal data redacted, so we can attribute spend and debug. Policy hooks can block sensitive data from going to external providers and keep regulated data in approved regions. The gateway itself must be highly available, since it is now on the critical path for every AI feature."
  ],
  "followups": [
   [
    "What is the biggest risk of a central gateway?",
    "It becomes a single point of failure and a latency hop, so it needs redundancy, low overhead and a careful rollout."
   ]
  ],
  "mistakes": [
   "Forgetting per-team cost attribution and budgets.",
   "Logging full prompts with personal data unredacted.",
   "No fallback when a provider is down.",
   "Adding heavy processing that increases latency on every request."
  ],
  "related": [
   "how-to-cache-llm-responses",
   "how-to-reduce-llm-inference-cost",
   "what-are-llm-guardrails"
  ]
 },
 {
  "slug": "how-to-cache-llm-responses",
  "q": "How do you design caching for LLM applications?",
  "desc": "Caching for LLM applications: exact-match response caches, provider prompt caching, semantic caching risks, cache keys, invalidation and permission scoping.",
  "level": "Mid",
  "src": [
   79
  ],
  "testing": "Whether you know the different cache layers for LLM systems, their risks, and how to key and invalidate them safely.",
  "steps": [
   "Exact-match response cache: key on a hash of model, version, full prompt and parameters.",
   "Prompt (prefix) caching: keep the static part of prompts first so providers or the inference server can reuse computation.",
   "Semantic cache: reuse answers for similar queries, with a high similarity threshold and only for safe, generic content.",
   "Correctness: include permissions and tenant in keys, set expiry, and invalidate when source documents change.",
   "Measure hit rate, savings, and the error rate of cached answers."
  ],
  "sample": [
   "I think of three layers. The simplest is an exact-match cache: hash the model name and version, the full prompt and the sampling parameters, and store the response. It is safe and works well for repeated requests such as the same document summarized by many users or batch jobs that are re-run.",
   "The second is prompt or prefix caching. Many providers and inference servers can reuse the computation for a repeated prompt prefix, which cuts cost and time to first token. To benefit, I order prompts with the stable parts first, such as system instructions, tool definitions and shared documents, and the variable user input last.",
   "The third is semantic caching, where a new query reuses the answer for a sufficiently similar past query. It can save a lot, but it is risky: two questions can be close in embedding space and need different answers, for example plans that differ by one word. I use it only for generic content, with a strict threshold, and never across users when answers depend on their data. Cache keys include tenant and permission scope, entries expire, and they are invalidated when the underlying documents change."
  ],
  "followups": [
   [
    "Why can a semantic cache be dangerous?",
    "Similar-looking questions can need different answers, so it can serve a confidently wrong or another user's answer."
   ]
  ],
  "mistakes": [
   "Leaving the model version or parameters out of the cache key.",
   "Sharing cached answers across users with different permissions.",
   "Putting variable content at the start of the prompt, which defeats prefix caching.",
   "Using a loose similarity threshold for semantic caching."
  ],
  "related": [
   "how-to-reduce-llm-inference-cost",
   "design-an-llm-gateway",
   "access-control-in-rag"
  ]
 },
 {
  "slug": "how-to-reduce-llm-inference-cost",
  "q": "How do you reduce LLM inference cost?",
  "desc": "How to reduce LLM inference cost: measure first, route to smaller models, trim prompts, cache, batch offline work, quantize self-hosted models, and re-check quality.",
  "level": "Mid",
  "src": [
   84
  ],
  "testing": "Whether you approach cost with measurement and a ranked list of levers, while protecting quality with evaluation.",
  "steps": [
   "Measure: cost per request and per successful task, broken down by feature, model, input and output tokens.",
   "Right-size models: route easy requests to smaller models and reserve large ones for hard cases.",
   "Cut tokens: shorter prompts, fewer retrieved chunks, output length limits, and summarized history.",
   "Reuse and batch: response and prefix caching, and batch APIs for offline jobs.",
   "Self-hosted levers: quantization, continuous batching and high GPU utilization; re-run evals after every change."
  ],
  "sample": [
   "I start by measuring where the money goes. I break down spend by feature, model and token type, because output tokens usually cost several times more than input tokens, and I look at cost per successful task rather than per call, since a cheap model that needs three retries is not cheap.",
   "The biggest lever is usually model choice. Many requests, such as classification, extraction or simple rewrites, work well on a small model, so a router sends those there and only escalates hard cases. Next is token volume: trim system prompts, retrieve five good chunks instead of twenty, cap output length and summarize long conversation history.",
   "Then reuse: exact-match caching for repeated requests, prefix caching by putting static content first, and batch APIs, often discounted, for offline jobs such as nightly summarization. If we host our own models, quantization, continuous batching and keeping GPUs busy lower cost per token, and distillation can replace a large model on a narrow, high-volume task. Every change goes through the eval suite, because a cost cut that hurts task success can cost more in user trust."
  ],
  "followups": [
   [
    "Which lever do you try first?",
    "Usually routing to smaller models and trimming tokens, since they need little infrastructure and often give the largest savings."
   ]
  ],
  "mistakes": [
   "Optimizing without a cost breakdown.",
   "Measuring cost per call instead of per successful task.",
   "Ignoring output tokens, which are often priced higher.",
   "Cutting cost without re-running quality evals."
  ],
  "related": [
   "how-to-reduce-llm-latency",
   "how-to-cache-llm-responses",
   "what-is-model-distillation"
  ]
 },
 {
  "slug": "how-to-reduce-llm-latency",
  "q": "How do you reduce LLM latency?",
  "desc": "How to reduce LLM latency: measure time to first token and tokens per second, stream, shorten prompts and outputs, use smaller models, cache and parallelize.",
  "level": "Mid",
  "src": [
   85
  ],
  "testing": "Whether you understand the parts of LLM latency and can pick fixes for each, including the user-perceived side.",
  "steps": [
   "Measure the parts: time to first token (TTFT), tokens per second, and total time including retrieval and tools.",
   "Stream output so users see progress immediately.",
   "Shorten inputs (less prefill) and outputs (fewer decode steps); output length often dominates.",
   "Use smaller or faster models for simple steps, and prefix caching for repeated prompt parts.",
   "Remove serial steps: run retrieval and tool calls in parallel, and cut unnecessary chain steps."
  ],
  "sample": [
   "I split latency into parts before changing anything. Time to first token depends on queueing, network and prefill, which grows with prompt length. Generation time is the number of output tokens divided by decode speed. Around both sit retrieval, re-ranking and tool calls. A trace of a slow request usually shows one dominant part.",
   "For user-facing chat, streaming is the first fix, because perceived latency is mostly time to first token. Then I cut output length, since each output token is a sequential decode step: ask for concise answers, set max tokens, and avoid generating long reasoning the user never sees. Shorter prompts help prefill, and prefix caching makes repeated system prompts and documents nearly free.",
   "Next is architecture. I use small fast models for routing, classification and extraction, and reserve large models for the final answer. Independent steps such as retrieval from two sources or several tool calls run in parallel rather than one after another. On self-hosted models, quantization and speculative decoding can raise tokens per second. I track p50 and p95 separately, because tail latency is what users complain about."
  ],
  "followups": [
   [
    "Why does output length matter more than input length?",
    "Prompt tokens are processed in parallel during prefill, while output tokens are generated one at a time."
   ]
  ],
  "mistakes": [
   "Optimizing without a latency breakdown.",
   "Not streaming in user-facing flows.",
   "Running independent calls sequentially.",
   "Looking only at average latency instead of p95."
  ],
  "related": [
   "how-to-reduce-llm-inference-cost",
   "what-is-kv-cache",
   "what-is-quantization-in-llms"
  ]
 },
 {
  "slug": "what-is-red-teaming-in-ai",
  "q": "What does red-teaming an LLM system involve?",
  "desc": "Red-teaming an LLM system: scoping harms, adversarial and injection testing, automated attack generation, severity triage, fixes and regression tests.",
  "level": "Senior",
  "src": [
   89
  ],
  "testing": "Whether you can run red-teaming as a structured process tied to the actual product risks, not just a collection of jailbreak prompts.",
  "steps": [
   "Scope: list the harms that matter for this product, such as data leaks, unsafe advice, unauthorized actions and policy violations.",
   "Attack manually: jailbreaks, role-play, multi-turn escalation, and direct and indirect prompt injection through documents and tools.",
   "Scale with automation: generate attack variations with models and fuzzing, and score results automatically.",
   "Triage by severity and likelihood, fix with layered defenses, and re-test.",
   "Keep successful attacks as regression tests and repeat before each major release."
  ],
  "sample": [
   "Red-teaming means deliberately trying to make the system fail in harmful ways before real users do. I start by scoping it to the product. For an assistant with access to customer records and an email tool, the top risks are leaking one customer's data to another, sending messages nobody approved, and following instructions hidden in a retrieved document.",
   "Then testers attack. Manual testing covers jailbreak styles, role-play framing, gradual multi-turn escalation and indirect prompt injection, such as a support ticket containing hidden instructions to export data. Because people cannot cover every variation, I add automated generation: a model produces many rephrasings and combinations, and classifiers or rules score which ones succeeded.",
   "Findings are triaged by severity and how easy they are to trigger. Fixes are usually layered: tighter tool permissions and approvals, input and output filters, better system instructions and, where needed, model-level changes. Every successful attack becomes a regression test, and the suite runs before major releases, because new features and model upgrades can reopen old holes."
  ],
  "followups": [
   [
    "Is red-teaming a one-time exercise?",
    "No; models, prompts and tools change, so it is repeated before releases and the regression suite runs continuously."
   ]
  ],
  "mistakes": [
   "Testing only generic jailbreaks unrelated to the product's real risks.",
   "Ignoring indirect injection through documents and tool outputs.",
   "Fixing only by editing the system prompt.",
   "Not turning findings into regression tests."
  ],
  "related": [
   "what-is-prompt-injection",
   "what-are-llm-guardrails",
   "how-to-make-ai-agents-reliable-in-production"
  ]
 },
 {
  "slug": "what-are-llm-guardrails",
  "q": "What are LLM guardrails and where do they sit?",
  "desc": "LLM guardrails explained: input checks, retrieval and tool controls, output validation and action approval, plus latency, false positives and monitoring.",
  "level": "Mid",
  "src": [
   90
  ],
  "testing": "Whether you see guardrails as layered controls around the model at specific points in the pipeline, and understand their trade-offs.",
  "steps": [
   "Input layer: detect prompt injection, off-topic or abusive requests, and redact personal data where needed.",
   "Retrieval and tools layer: permission filtering, least-privilege credentials and argument validation.",
   "Output layer: schema validation, policy and safety classifiers, groundedness checks and PII leak detection.",
   "Action layer: human approval for irreversible or high-value actions.",
   "Operations: measure false positives and latency, log blocks, and tune thresholds."
  ],
  "sample": [
   "Guardrails are checks placed around the model, not inside it, at each point where something can go wrong. On the input side, I screen for prompt injection attempts and requests outside the product's scope, and redact personal data if it should not go to the model provider.",
   "In the middle, the most effective guardrails are boring ones: retrieval only returns documents the user may see, tools run with the narrowest credentials, and every tool argument is validated in code. On the output side, I validate structure against a schema, run policy or safety classifiers, check that factual claims are supported by retrieved sources where that matters, and scan for leaked secrets or personal data. Finally, at the action layer, anything irreversible, such as payments, deletions or external messages, requires explicit approval.",
   "Guardrails have costs. Each check adds latency, and strict classifiers block legitimate requests, which frustrates users. So I measure block rates and false positives on real traffic, review samples of blocked requests, and tune thresholds. No single layer is perfect, which is the reason for layering them."
  ],
  "followups": [
   [
    "Is a strong system prompt a guardrail?",
    "It helps, but it can be overridden by injection, so real controls must live in code outside the model."
   ]
  ],
  "mistakes": [
   "Relying on the system prompt as the only guardrail.",
   "Adding checks without measuring false positives and latency.",
   "Forgetting tool permissions and action approval.",
   "Using one layer and assuming it catches everything."
  ],
  "related": [
   "what-is-prompt-injection",
   "what-is-red-teaming-in-ai",
   "how-to-get-reliable-json-output-from-an-llm"
  ]
 }
]

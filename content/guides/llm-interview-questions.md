# LLM Interview Questions and Answers (2026): 25 Questions from Basics to Production

**Meta description:** 25 LLM interview questions with model answers: transformers, tokens, decoding, LoRA, RLHF, quantization, hallucination and serving, plus a level table and FAQ.

## Quick answer

LLM interview questions check whether you understand how large language models work well enough to build with them. Expect five groups: architecture (transformers, attention, context windows), tokens and decoding (tokenization, temperature, top-p), training and adaptation (pre-training, instruction tuning, RLHF, LoRA), behavior and risk (hallucination, prompt injection, evaluation), and serving (KV cache, quantization, latency and cost). Practice the 25 questions below out loud in about two minutes each, then score yourself with the free answer self-check.

## How to use this page

Questions run from fundamentals to production. Each answer is a short model answer to adapt in your own words, with a link to a deeper explanation on this site. These are original practice questions, not questions reported from a specific company. For application topics, pair this page with the [RAG interview questions](https://johnnnmai.github.io/ai-engineer-interview-questions/guides/rag-interview-questions/), [AI agent interview questions](https://johnnnmai.github.io/ai-engineer-interview-questions/guides/ai-agent-interview-questions/) and [AI system design interview questions](https://johnnnmai.github.io/ai-engineer-interview-questions/guides/ai-system-design-interview-questions/) guides.

| Group | Example question | What a strong answer shows | Typical level |
|---|---|---|---|
| Architecture | Explain self-attention | Queries, keys, values and why it scales with length | Entry |
| Tokens and decoding | Temperature vs top-p? | Knows both change randomness in different ways | Entry |
| Training | What does RLHF add? | Separates pre-training, instruction tuning and preference tuning | Mid |
| Adaptation | When would you use LoRA? | Memory and cost trade-off against full fine-tuning | Mid |
| Behavior | Why do LLMs hallucinate? | Next-token objective, missing knowledge, mitigations | Mid |
| Serving | How do you cut inference cost? | KV cache, batching, quantization, routing | Senior |

## Architecture questions

- **Question: Explain the transformer architecture.** Answer: a stack of layers, each with self-attention and a feed-forward network, plus residual connections and normalization, introduced in [Attention Is All You Need](https://arxiv.org/abs/1706.03762). Decoder-only models predict the next token with a causal mask. Deep dive: [transformer architecture](https://johnnnmai.github.io/ai-engineer-interview-questions/questions/explain-the-transformer-architecture/).
- **Question: What does self-attention compute?** Answer: each token builds a query, key and value; attention weights come from query and key similarity, and the output is a weighted sum of values. Multiple heads let the model attend to different patterns at once.
- **Question: Why does long context cost more?** Answer: standard attention compares every token with every other token, so compute grows roughly with the square of sequence length, and the KV cache grows linearly with it. See [what is a context window](https://johnnnmai.github.io/ai-engineer-interview-questions/questions/what-is-a-context-window/).
- **Question: What is mixture of experts?** Answer: a layer with several expert networks and a router that sends each token to a few of them, so total parameters grow while compute per token stays lower. See [mixture of experts](https://johnnnmai.github.io/ai-engineer-interview-questions/questions/what-is-mixture-of-experts/).
- **Question: What are scaling laws?** Answer: empirical relationships between model size, data and compute and the resulting loss, described in [Kaplan et al., 2020](https://arxiv.org/abs/2001.08361) and revisited for compute-optimal training in [Hoffmann et al., 2022](https://arxiv.org/abs/2203.15556). See [scaling laws](https://johnnnmai.github.io/ai-engineer-interview-questions/questions/what-are-scaling-laws/).

## Tokens and decoding questions

- **Question: What is tokenization and why does it matter?** Answer: text is split into subword tokens from a fixed vocabulary. It affects cost, context limits, multilingual quality and odd failures such as character counting. See [tokenization in LLMs](https://johnnnmai.github.io/ai-engineer-interview-questions/questions/what-is-tokenization-in-llms/).
- **Question: Temperature vs top-p?** Answer: temperature rescales the probability distribution, lower is more deterministic; top-p, or nucleus sampling from [Holtzman et al.](https://arxiv.org/abs/1904.09751), samples only from the smallest set of tokens whose probability adds up to p. Change one at a time. See [temperature vs top-p](https://johnnnmai.github.io/ai-engineer-interview-questions/questions/temperature-vs-top-p/).
- **Question: Why can the same prompt give different answers?** Answer: sampling randomness, and sometimes nondeterminism in serving. Use low temperature, fixed seeds where offered and structured output when you need consistency.
- **Question: How do you get reliable structured output?** Answer: schema-constrained output where the API supports it, validation, and retry with the error message. See [reliable JSON output](https://johnnnmai.github.io/ai-engineer-interview-questions/questions/how-to-get-reliable-json-output-from-an-llm/).
- **Question: What is chain-of-thought prompting?** Answer: asking the model to reason step by step before answering, which improved multi-step reasoning in [Wei et al., 2022](https://arxiv.org/abs/2201.11903). See [chain-of-thought prompting](https://johnnnmai.github.io/ai-engineer-interview-questions/questions/what-is-chain-of-thought-prompting/).

## Training and adaptation questions

- **Question: Pre-training vs instruction tuning vs RLHF?** Answer: pre-training learns language from large text corpora; instruction tuning teaches the model to follow tasks; preference tuning such as RLHF, used in [InstructGPT](https://arxiv.org/abs/2203.02155), aligns outputs with human preferences. See [pre-training vs instruction tuning vs RLHF](https://johnnnmai.github.io/ai-engineer-interview-questions/questions/pre-training-vs-instruction-tuning-vs-rlhf/).
- **Question: What are LoRA and QLoRA?** Answer: [LoRA](https://arxiv.org/abs/2106.09685) freezes base weights and trains small low-rank matrices; QLoRA does this on a quantized base model to save memory. See [LoRA and QLoRA](https://johnnnmai.github.io/ai-engineer-interview-questions/questions/explain-lora-and-qlora/).
- **Question: When would you fine-tune instead of prompting or RAG?** Answer: when you need consistent format, style or a narrow skill that prompting cannot reach, and you have quality examples. For missing knowledge, use retrieval. See [RAG vs fine-tuning](https://johnnnmai.github.io/ai-engineer-interview-questions/questions/rag-vs-fine-tuning/).
- **Question: How do you build a fine-tuning dataset?** Answer: collect real task examples, write consistent target outputs, remove duplicates and sensitive data, hold out an evaluation split and track data versions. See [building a fine-tuning dataset](https://johnnnmai.github.io/ai-engineer-interview-questions/questions/how-to-build-a-fine-tuning-dataset/).
- **Question: Reasoning models vs chat models?** Answer: reasoning models spend more tokens thinking before answering, which helps multi-step problems but adds latency and cost. Route only hard tasks to them. See [reasoning vs chat models](https://johnnnmai.github.io/ai-engineer-interview-questions/questions/reasoning-models-vs-chat-models/).

## Behavior, risk and evaluation questions

- **Question: Why do LLMs hallucinate?** Answer: they are trained to produce likely text, not verified facts, so gaps in knowledge or ambiguous prompts can yield fluent but wrong answers. Mitigate with retrieval, citations, abstention and checks. See [why LLMs hallucinate](https://johnnnmai.github.io/ai-engineer-interview-questions/questions/why-do-llms-hallucinate/).
- **Question: What is prompt injection?** Answer: input that overrides the system's instructions, directly from the user or indirectly through retrieved content. Treat untrusted text as data and limit tool permissions. See [prompt injection](https://johnnnmai.github.io/ai-engineer-interview-questions/questions/what-is-prompt-injection/).
- **Question: How do you evaluate an LLM for your product?** Answer: define the task, build a representative labeled set, pick metrics per failure type, compare against a baseline and combine automated checks with human review. See the [LLM evaluation interview questions guide](https://johnnnmai.github.io/ai-engineer-interview-questions/guides/llm-evaluation-interview-questions/).
- **Question: What is benchmark contamination?** Answer: test data leaking into training data, which inflates scores. Prefer private or fresh evaluation sets. See [benchmark contamination](https://johnnnmai.github.io/ai-engineer-interview-questions/questions/what-is-benchmark-contamination/).
- **Question: What is lost in the middle?** Answer: models tend to use information at the start and end of long inputs better than in the middle, so order and trim context carefully. See [lost in the middle](https://johnnnmai.github.io/ai-engineer-interview-questions/questions/what-is-lost-in-the-middle/).

## Serving and cost questions

- **Question: What is the KV cache?** Answer: stored keys and values from earlier tokens so each new token does not recompute them. It speeds generation but uses memory that grows with context and batch size. See [KV cache](https://johnnnmai.github.io/ai-engineer-interview-questions/questions/what-is-kv-cache/).
- **Question: What is quantization?** Answer: storing weights, and sometimes activations, in fewer bits to cut memory and speed up inference, with some quality risk that you measure on your task. See [quantization in LLMs](https://johnnnmai.github.io/ai-engineer-interview-questions/questions/what-is-quantization-in-llms/).
- **Question: How do you reduce LLM latency?** Answer: stream tokens, shorten prompts, cache, use a smaller model where quality allows, and batch on the server. See [reducing LLM latency](https://johnnnmai.github.io/ai-engineer-interview-questions/questions/how-to-reduce-llm-latency/).
- **Question: How do you reduce inference cost?** Answer: route easy requests to cheaper models, cache, trim context, cap output length and measure cost per successful task. Price scenarios with the free [LLM API cost calculator](https://johnnnmai.github.io/ai-engineer-interview-questions/llm-cost-calculator/).
- **Question: Embedding model vs generative model?** Answer: an embedding model maps text to vectors for search and clustering; a generative model produces text. They are trained and served differently. See [embedding vs generative models](https://johnnnmai.github.io/ai-engineer-interview-questions/questions/embedding-model-vs-generative-model/).

## How to practice

For each question, give a one-sentence definition, the main trade-off, a concrete example and one failure case. Record your answer, paste the transcript into the free [answer self-check](https://johnnnmai.github.io/ai-engineer-interview-questions/answer-check/), and then run a timed [mock interview round](https://johnnnmai.github.io/ai-engineer-interview-questions/mock-interview/). If your interview has a date, the [study plan tool](https://johnnnmai.github.io/ai-engineer-interview-questions/study-plan/) spreads these topics over the days you have. Keep the [free Top 30 AI engineer questions PDF](https://sirjohnnymai.gumroad.com/l/aie-top-30-questions) for quick review.

## FAQ

- **What LLM topics come up most in interviews?** As general guidance, transformers and attention, tokenization and decoding, fine-tuning vs RAG, hallucination, evaluation and serving cost come up often in AI engineer loops.
- **Do I need to derive attention math?** Usually you need to explain it clearly and know why it scales with sequence length. Research roles may ask for more depth.
- **How much should I know about training?** Know the stages, what each changes and when you would fine-tune. Most AI engineer roles focus on adapting and serving models rather than pre-training them.
- **Are LLM interview questions different from AI engineer interview questions?** LLM questions are a subset focused on how models work. AI engineer loops add coding, RAG, agents, system design and behavioral rounds.
- **Are these real questions from a specific company?** No. They are original practice questions that reflect common topics in AI engineer interviews.

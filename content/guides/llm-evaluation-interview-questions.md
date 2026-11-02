# LLM Evaluation Interview Questions and How to Answer Them

Prepare for LLM evaluation interviews by defining the task, building test cases, selecting metrics, and explaining how scores connect to user outcomes. Practice questions about hallucinations, RAG, model judges, tool use, safety, and regression testing. Strong answers distinguish automated checks from human judgment and discuss uncertainty, bias, and deployment decisions.

## How should you answer “How do you evaluate an LLM?”

Begin with a specific product task and define success before choosing any metric or evaluator.

- **Question: How would you evaluate a support assistant?** Answer: “I would list supported intents, build a set of labeled conversations, and measure answer correctness, policy compliance, appropriate escalation, and task completion. I would segment scores by intent and monitor latency and cost.”
- **Question: What belongs in an evaluation dataset?** Answer: include ordinary traffic patterns, difficult failures, ambiguous requests, adversarial input, and relevant language or customer segments. Keep a held-out set so the test does not become a tuning target.
- **Question: What is a good baseline?** Answer: a rule-based system, existing prompt, simpler model, or current production behavior evaluated on the same examples. Improvements are meaningful only with comparable data and stable criteria.
- **Question: Can one number summarize quality?** Answer: use a dashboard of task outcomes and safety gates, because gains in helpfulness can hide regressions in factuality or privacy. OpenAI's [evaluation best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices) emphasize representative cases, iteration, and human feedback.

## How should you answer RAG and hallucination questions?

Separate whether the system found the evidence from whether the model used that evidence correctly.

- **Question: How do you evaluate a RAG application?** Answer: score retrieval recall or ranking against labeled supporting passages, then grade answer correctness, groundedness, citation support, and abstention. Inspect both stages for each failure.
- **Question: What is hallucination?** Answer: in an application setting, it is an output that asserts unsupported or incorrect information. Evaluate unsupported claims against supplied evidence and, separately, factual correctness against trusted references.
- **Question: What if a correct answer cites the wrong document?** Answer: mark citation support as failed even if the answer text is right. Citation integrity matters because users may rely on the linked evidence to verify a claim.
- **Question: How would you test document freshness?** Answer: use time-sensitive queries with known document versions, delete or update a source, and confirm the indexed content and final citations change appropriately.
- Use AWS's [RAG evaluation guide](https://docs.aws.amazon.com/bedrock/latest/userguide/evaluation-kb.html) as a public reference for retrieve-only and retrieve-and-generate evaluation modes.

## How should you choose and explain evaluation metrics?

Map each metric to the failure it detects and specify its denominator, reference data, and decision threshold.

- Use the table as a compact answer aid rather than an exhaustive metric taxonomy:

  | Question | Useful measure | Important caveat |
  | --- | --- | --- |
  | Did search find evidence? | Recall@k | Needs relevance labels |
  | Is the answer supported? | Groundedness review | Depends on evidence quality |
  | Did a tool call work? | Argument and outcome checks | Valid JSON can still be wrong |
  | Is deployment reliable? | p95 latency, error rate | Averages conceal tail failures |

- Define denominators. “Eighty percent correct” is uninterpretable without saying which queries, languages, conditions, and labeled outcomes were included. Where the sample is small, present uncertainty rather than false precision.
- Distinguish offline scorecards from online outcomes. Offline tests make regressions reproducible; live measurements reveal user behavior, changing traffic, and operational issues that curated examples may miss.
- Treat task-specific pass/fail gates as first-class signals. A tiny increase in average helpfulness should not outweigh exposing private data or executing an unauthorized tool request.
- Microsoft's [RAG evaluator overview](https://learn.microsoft.com/en-us/azure/foundry/concepts/evaluation-evaluators/rag-evaluators?view=foundry-classic) documents separate retrieval, groundedness, relevance, and completeness assessments.

## How do you answer “Can an LLM judge another LLM?”

Explain what a model judge can scale, how to calibrate it, and why it cannot replace reliable reference checks.

- **Question: When is an LLM judge useful?** Answer: for nuanced criteria such as response helpfulness or citation faithfulness when exact matching is inadequate. Provide a narrow rubric with anchored score levels and examples.
- **Question: What are judge failure modes?** Answer: position bias in pairwise comparisons, verbosity preferences, inconsistent ratings, shared blind spots with the candidate model, and susceptibility to adversarial instructions in the evaluated output.
- **Question: How do you validate a judge?** Answer: compare scores with blinded human labels, inspect disagreement cases, repeat a subset of judgments, and report agreement by category. Revise ambiguous scoring anchors before using scores as release gates.
- **Question: What should remain deterministic?** Answer: JSON schema validity, expected tool names and arguments, executable code tests, permissions, and exact reference matches where applicable. A model grader adds flexibility, not a substitute for assertions.
- OpenAI's [evaluation guidance](https://developers.openai.com/api/docs/guides/evaluation-best-practices) describes model graders and recommends calibrating automated scoring against human judgments.

## How do you discuss safety, regressions, and release decisions?

Tie evaluation to change management: a deployment should pass quality thresholds without crossing nonnegotiable safety limits.

- **Question: How would you test prompt injection?** Answer: put malicious instructions inside retrieved documents or tool outputs, then verify they cannot override developer instructions, expose secrets, or trigger unauthorized actions. Test the actual tool boundary, not only refusal wording.
- **Question: What should trigger rollback?** Answer: a predefined regression in critical correctness, unauthorized actions, data leakage, severe task failure, or operational service levels. Use canary deployment or an equivalent controlled exposure strategy when available.
- **Question: How do you measure agent performance?** Answer: evaluate full task completion, correct tool choice, argument fidelity, appropriate escalation, and side effects. Analyze traces to locate the step causing failure rather than scoring only final prose.
- **Question: How do you handle new failures?** Answer: reproduce and label the case, add it to a regression set, identify the component, and compare a fix against the unchanged baseline. Prevent overfitting by preserving independent holdouts.
- OWASP's [prompt injection risk page](https://genai.owasp.org/llmrisk/llm01-prompt-injection/) and NIST's [Generative AI Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence) provide public grounding for safety and risk-management discussions.

## FAQ

These answers clarify what interview-ready evaluation reasoning does and does not require.

- **Do I need a proprietary evaluator?** No, many useful checks are simple scripts, curated examples, and structured human review. Choose tooling after defining the measurement problem.
- **What if I have no production traffic?** Create a small labeled dataset from realistic task examples and document its limitations. Do not claim that synthetic examples reproduce actual user distribution.
- **Is benchmark accuracy enough?** No, general benchmarks may miss domain-specific tasks, tool failures, or privacy constraints. Test the application end to end with its real instructions and data boundaries.
- **What makes an answer senior-level?** It connects the metric to release criteria, sampling bias, costs, failure diagnosis, and stakeholder trade-offs. Technical definitions alone do not establish an operational decision process.


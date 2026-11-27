# AI Engineer vs ML Engineer Interview: What Is Different?

An AI engineer interview usually focuses on building apps with existing models. That work covers prompting, retrieval, tools, quality checks, and reliability in production. An ML engineer interview often probes data pipelines, model training, statistical tests, and how learned models are shipped. Both can test Python, systems, experiments, and monitoring. The job post sets the mix.

## What is the practical difference between the roles?

Treat AI engineering and ML engineering as overlapping skill sets. The difference is which part of the modeling system the role owns.

- Applied AI engineering often starts with a ready model or API. The task is to solve a user problem in a reliable way. The hard work includes context construction, tools, model choice, structured outputs, quality checks, and product integration.
- ML engineering more often starts with a dataset, a prediction target, or a training pipeline. The task is to develop and run a model. Label quality, feature leakage, objective choice, experiment repeatability, and model drift are central concerns.
- Neither title guarantees a fixed interview loop. Some AI engineering jobs require fine-tuning and infrastructure. Some ML engineering jobs are mainly serving and platform work. Classify the duties instead of relying on labels.
- Ask what the team ships. It might be a customer-facing assistant, a search experience, an inference service, a recommendation model, or a training platform. That answer predicts later interview topics better than the title alone.

## Which topics are more likely to receive deeper questions?

Prepare shared basics first. Then go deeper based on whether the job mainly adapts existing models or develops learned models.

- Use this as a study heuristic, not a verified company-specific interview blueprint:

  | Topic | AI engineer emphasis | ML engineer emphasis |
  | --- | --- | --- |
  | Core design | RAG, agents, model APIs | Training and serving pipelines |
  | Evaluation | Groundedness, task success, judge calibration | Splits, leakage, precision and recall |
  | Optimization | Tokens, latency, model routing | Features, loss, tuning, inference |
  | Failure modes | Prompt injection, tool errors, citations | Distribution shift, data drift, bias |

- Both tracks need software quality. That means Python fluency, APIs, test cases, monitoring, deployment, versioning, and clear constraints. Coding bar depends on scope and seniority, not a universal label.
- AI engineering questions may test when retrieval is better than fine-tuning. They may also ask how to validate tool calls and how to diagnose hallucinations. Google Cloud's [RAG architecture reference](https://docs.cloud.google.com/architecture/rag-reference-architectures) shows distinct ingestion, serving, and evaluation concerns.
- ML engineering questions may test target leakage, cross-validation, and feature availability at inference. They may also ask why offline metrics can diverge from production. The [scikit-learn common pitfalls guide](https://scikit-learn.org/stable/common_pitfalls) documents leakage and safe preprocessing patterns.

## How does system design change between interviews?

In either track, start with the problem and success metrics. Then set design boundaries around the main sources of uncertainty.

- For an AI app, draw document ingestion, indexing, retriever, reranker, model, tools, user permissions, and output checks. Explain how a stale document gets corrected. Explain how an unsupported answer should be withheld.
- For a predictive ML service, draw events, labels, feature creation, train and validation splits, training, model registry, deployment, online inference, and monitoring. Explain which transforms must be identical online and offline.
- State the quality target separately from the service-level target. A system can meet its latency goal while giving wrong answers. It can also make accurate predictions while missing a throughput need.
- Discuss change management. One design must catch prompt and retrieval regressions. The other must catch data, model, and feature version regressions. In both cases, require a holdout review and a rollback path.
- Estimate constraints with clearly marked assumptions. A concrete plan such as "compare p95 latency before and after reranking" is stronger than a claim that one design is always faster.

## How do coding and statistics expectations differ?

AI engineering coding exercises often stress orchestration correctness. ML engineering exercises often add numerical reasoning and data checks.

- AI practice: write a robust model client, document chunker, reranking scorer, JSON schema validator, or tool dispatcher. Test hostile or unexpected inputs as well as the normal path.
- ML practice: write a test loop, compute class metrics, inspect skewed classes, and prevent train-test leakage. Explain why accuracy alone can hide a model that is not usable.
- Shared practice: solve standard Python problems, reason about cost, transform tabular data, debug tests, and state assumptions. A weak coding base is a liability on either path.
- Know when a metric is undefined or misleading. Precision and recall depend on a positive-class definition. Calibration matters when decisions use probability thresholds. Average accuracy can hide subgroup failures.
- If the role requires deep learning frameworks, practice loading and scoring models, checkpointing, and memory-aware inference. PyTorch's [saving and loading tutorial](https://docs.pytorch.org/tutorials/beginner/saving_loading_models) gives concrete lifecycle cases.

## How should you select a portfolio example and study plan?

Choose one end-to-end project. Then adapt the story to the ownership model implied by each role.

- For AI engineering, show a knowledge-base assistant that answers with citations and can abstain. Show retrieval comparisons, answer-quality cases, user permission controls, and a measured cost and latency budget.
- For ML engineering, show a trained classifier or ranker with a clean data split, a baseline, a repeatable pipeline, a review report, and a monitoring plan. Discuss what happens when incoming data shifts.
- If you have only one project, discuss it through both lenses. Explain the inference API and user failure modes. Then state the dataset, baseline, training choices, and validation design where those parts truly exist.
- Use a 60/40 allocation rule as a planning suggestion. Spend the larger share on the posting's main tasks. Spend the smaller share on overlapping basics. Change that ratio after mock interviews show the real gaps.
- Score yourself on evidence rather than vocabulary. OpenAI's [evaluation guidance](https://developers.openai.com/api/docs/guides/evaluation-best-practices) recommends measurable goals, representative cases, and comparison against baselines for generative systems.

## FAQ

The overlap is large. So these distinctions guide prep. They do not predict a particular interviewer's agenda.

- **Is AI engineering just prompt engineering?** No. Prompting is one part of a system that also needs retrieval, coding, measurement, security, and operations. A good interview answer explains how those parts interact.
- **Which track requires more mathematics?** Model-development roles often need deeper optimization, statistics, and learning theory. Applied AI roles still benefit from probability, review statistics, and a grasp of attention. The posting sets the depth.
- **Can an ML engineer switch to AI engineering?** Yes, mainly with experience in deployment and review. Add hands-on RAG, tool calling, security boundaries, and model API failure handling to close the applied gap.
- **Should I apply to both titles?** Apply when your shown skills match the listed duties, not merely because the names sound close. Tailor project cases and prep to each posting's actual work.

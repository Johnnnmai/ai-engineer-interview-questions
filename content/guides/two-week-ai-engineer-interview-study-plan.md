# A 2-Week AI Engineer Interview Study Plan

A two-week AI engineer interview study plan should combine daily coding, LLM fundamentals, RAG design, evaluation, and timed speaking practice. Spend 90 focused minutes per day, build one small retriever-based application, and keep a mistake log. Use the final days for mock interviews, weak areas, and a measurable project walkthrough.

## How should you structure 14 days of preparation?

Use a consistent daily routine with one concrete deliverable and enough review time to turn mistakes into improved answers.

- Reserve approximately 20 minutes for recalling yesterday's material, 40 minutes for implementation or design, 20 minutes for explaining the result aloud, and 10 minutes for updating a mistake log. Adjust the durations if you have more or less time.
- Define a target role from a current job posting. Highlight its actual requirements so you do not spend two weeks on model training for a role focused on API integration, or only prompting for a role focused on infrastructure.
- Build one small application throughout the plan: a document Q&A system with retrieval, cited answers, and basic tests. Use public or self-created text and a local baseline if model access is unavailable.
- Keep a lightweight evidence sheet: date, exercise, result, missed concept, and next action. Record measured outputs separately from assumptions and avoid inventing quality or latency results.
- Use the following checkpoints as suggested practice targets, not validated thresholds for hiring:

  | Checkpoint | Deliverable |
  | --- | --- |
  | End of week 1 | Search baseline, evaluation questions, first design diagram |
  | End of week 2 | Tested walkthrough, mock interview, prioritized revision list |

## What should you do on days 1 through 3?

Build the conceptual foundation before spending time on frameworks or deployment platforms.

- **Day 1, diagnose:** pick one job description, attempt ten representative questions without notes, and grade definitions, mechanisms, and trade-offs. Set three study priorities from the misses and write a one-page summary of your target role.
- **Day 2, LLM fundamentals:** explain tokens, attention, context windows, sampling, embeddings, and the KV cache. Sketch how autoregressive decoding works, then test yourself on why memory and latency change with context length. Hugging Face's [KV caching guide](https://huggingface.co/docs/transformers/cache_explanation) supplies technical reference material.
- **Day 3, Python and APIs:** implement a typed response parser, retry policy, and a small test suite. Practice dictionaries, sorting, and string algorithms under a clock; narrate edge cases and complexity instead of silently writing code.
- Finish each day with a two-minute recording that begins with a direct answer. Mark any unsupported statement, vague noun, or unexplained trade-off for the next morning's review.

## What should you do on days 4 through 7?

Build a working retrieval prototype and an evaluation baseline that can expose its weaknesses.

- **Day 4, ingest:** collect a small document corpus, normalize text, preserve document identifiers, and implement chunking. Test duplicates, empty documents, long paragraphs, and updates so later citations can be traced back to actual source passages.
- **Day 5, retrieve:** implement a keyword search baseline and, if available, a vector or hybrid comparison. Write queries with exact names, paraphrases, and missing evidence; inspect retrieved passages instead of assuming the most similar result is correct.
- **Day 6, generate:** connect retrieved passages to answer construction or a mocked model output. Add citation identifiers, a structured response schema, and an abstention rule for unsupported questions. Draw both request-time and indexing-time paths.
- **Day 7, evaluate:** label a small set of queries with expected supporting documents and answers. Compare retrieval recall at k, answer support, unsupported claims, and latency where measurable; capture failure examples and prepare a five-minute demo.
- Google Cloud's [RAG overview](https://cloud.google.com/use-cases/retrieval-augmented-generation) explains the two-stage retrieval and generation pattern, while AWS's [RAG evaluation documentation](https://docs.aws.amazon.com/bedrock/latest/userguide/evaluation-kb.html) distinguishes retrieval from end-to-end assessment.

## What should you do on days 8 through 11?

Shift from building features to explaining design decisions, operating limits, and robust evaluation practices.

- **Day 8, system design:** respond to a document assistant prompt with requirements, assumptions, data flow, scaling choices, and a p95 latency budget. Discuss cost per request and what changes when documents must update frequently.
- **Day 9, evaluation depth:** design separate tests for retrieval, groundedness, task success, and abstention. Compare deterministic assertions, expert review, and model judges; explain how to calibrate an evaluator using human-labeled examples.
- **Day 10, safety and operations:** test unauthorized document access, prompt injection in retrieved text, malformed tool arguments, timeouts, and rate limits. Identify enforcement outside the model, then propose alerting, rollback, and appropriate logging.
- **Day 11, coding mock:** complete two timed exercises such as text chunking and an API wrapper. Review correctness, complexity, tests, and communication; refactor only after explaining the simplest working solution.
- Use OpenAI's [evaluation best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices) for quality methodology and OWASP's [prompt injection guidance](https://genai.owasp.org/llmrisk/llm01-prompt-injection/) for system trust boundaries.

## What should you do on days 12 through 14?

Use the last three days to test your readiness under interview conditions rather than expanding the topic list.

- **Day 12, project walkthrough:** present the application in six minutes: user need, baseline, architecture, measurements, failure analysis, and next experiment. Prepare honest answers for choices you did not implement, including what evidence would change your mind.
- **Day 13, full mock:** simulate a coding round, a RAG design round, and questions about LLM evaluation. Review recordings against a rubric for directness, technical correctness, measurable trade-offs, and admitting uncertainty.
- **Day 14, targeted review:** revisit only the weakest five concepts, rerun the tests, redraw the architecture without notes, and practice concise answers. Stop introducing new frameworks and prepare questions about the actual team's data and reliability needs.
- Keep final evidence simple: a runnable project or defensible prototype, a diagram, a compact scorecard, and examples of where the system fails. These artifacts are stronger than an unsupported claim of production-grade quality.
- For additional practice, use the free [AI engineer interview question bank](https://aie.valenx.org/) and compare each spoken answer with a documented model answer.

## FAQ

These adjustments help the same plan fit different backgrounds without promising identical results.

- **Is two weeks enough to become an AI engineer?** No, two weeks is a focused interview review period, not a substitute for practical engineering experience. It can improve recall, clarity, and preparation if the prerequisites already exist.
- **What if I have only 45 minutes daily?** Keep the same sequence but halve implementation scope and prioritize one testable example per day. Retain the spoken recap and error log because they reveal knowledge gaps.
- **What if the role emphasizes ML training?** Replace some RAG sessions with data splits, loss functions, training loops, and model monitoring. Keep evaluation, coding, and system design because those skills still transfer.
- **Should I memorize answers?** Memorize a clear structure and core definitions, not a script. Interview follow-ups usually require adapting assumptions, explaining counterexamples, and defending trade-offs.


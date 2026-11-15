# RAG Interview Prep: One-Week Plan and Key Concepts

This page is your seven-day roadmap for RAG interview preparation. It does not list questions; it tells you what to practice each day, which free reference pages to use, and how to debug retrieval versus generation. Use the links to the existing RAG questions guide, the "what is RAG" page, and the "how do you evaluate a RAG system" page to supplement your drills. The goal is to walk into the interview able to speak about each pipeline stage and name the metric you would check first when results are wrong.


RAG interview prep consists of three parallel tracks: understanding the pipeline architecture, practicing how to explain failure points out loud, and mapping evaluation metrics to specific failure modes. You should be able to diagram the flow from user query to final answer and identify which component (retriever, reranker, or generator) caused a failure. Practice speaking in 60-second outlines, not memorized scripts, and always pair a metric name with the failure you are describing.

## A 7-Day Plan

### Day 1: Pipeline anatomy. Practice drill: Draw the full RAG pipeline from query to answer on a blank sheet. Verbally label each component. Free page to use: the "what is RAG" guide on this site.
### Day 2: Retrieval failures. Practice drill: Take a open-domain question and list three ways the retriever could return useless passages. Free page to use: the RAG questions guide, specifically the retrieval section.
### Day 3: Reranking and context selection. Practice drill: Given a retrieved passage set, decide which two you would keep for the generator and explain why. Free page to use: the evaluation metrics section of the RAG questions guide.
### Day 4: Generation groundedness. Practice drill: Read a generated answer and identify any claim not supported by the provided context. Free page to use: the "how do you evaluate a RAG system" page.
### Day 5: End-to-end failure debugging. Practice drill: Simulate a user complaint that the answer is "wrong" or "hallucinated." Walk through the pipeline stages to locate the likely cause. Free page to use: the failure modes section of the RAG questions guide.
### Day 6: Metric selection. Practice drill: Given a scenario (low user satisfaction but high precision), name the one metric you would check first and why. Free page to use: the "how do you evaluate a RAG system" question page on this site.
### Day 7: Verbal run-through. Practice drill: Set a timer for 12 minutes. Answer three RAG questions from the guide out loud, focusing on pipeline stage and metric pairing. Free page to use: any question from the RAG questions guide.

## A Worked Question: "Walk Me Through a RAG Pipeline and Where It Fails"

Imagine you are asked to walk through a RAG pipeline from query input to final answer output. Outline the stage-by-stage flow, and identify which failure mode you would check first if the user reports that the answer contains facts not present in the source documents.

Stage-by-stage outline:
- Query encoding: The user question is converted into a vector embedding.
- Retrieval: The system searches the vector database for the most similar stored chunks.
- Reranking (optional): A cross-encoder or similar model reorders the top results for relevance.
- Context injection: The top N passages are concatenated with the original query and fed to the language model.
- Generation: The LLM produces the final answer, ideally grounded only in the injected context.
- Failure check: If the answer is wrong or unsupported, first inspect the retrieved passages. If the right passage is missing, you have a retrieval (or chunking, or query) problem. If the right passage is present and the model still invents a claim, you have a generation or context-assembly problem.

Follow-up: which failure do you check first?
Check retrieval first. Look at the retrieved passages before you touch the prompt. If the right passage is not there, no prompt change will fix it. If it is there and the answer still invents a claim, then inspect generation and how the context was assembled.

## How to Talk About Recall@k, Faithfulness, and Why One End-to-End Score Is Not Enough

When discussing evaluation, mention recall@k to describe what fraction of relevant documents the retriever returns in the top k results. Use precision@k to talk about how many of the top k results are actually relevant. For generation quality, faithfulness measures what fraction of the generated answer claims can be verified as true by the source context. No single metric covers all failure modes; if recall@k is low, the retriever is missing relevant documents, but if faithfulness is low, the generator is hallucinating regardless of retrieval quality. Always pair a metric name with the specific failure you are observing.

## Exactly 5 Q/A Pairs

Q: What should I be ready to do first in a RAG interview?
A: Be ready to walk through the pipeline and explain where it can fail. Name each stage and pair a failure mode with a metric you would actually check.

Q: Should I memorize definitions of recall and precision?
A: No. Interviewers want to hear you apply the concepts to a pipeline stage. Saying "recall@k measures the fraction of relevant docs in the top k results" is better than reciting a textbook definition.

Q: How do I handle a question about my specific project?
A: Focus on the pipeline stages you built and the metrics you tracked. If you used a reranker, mention how it changed the top-k results. If you measured faithfulness, explain what the score told you about generation grounding.

Q: What if I don't know a metric the interviewer mentions?
A: It is acceptable to say you are familiar with the concept but would look up the exact formula. Then, connect the metric to a failure mode you have practiced debugging.

Q: Can I practice alone?
A: Yes. Use a timer and speak your outline out loud. Record yourself if possible. The goal is to deliver a 60-second answer that names a stage, a failure, and a metric in under two minutes.

The free RAG questions guide and evaluation pages on this site are enough to start. The 0 to 1 AI Engineer Interview Playbook, $19.99, is the full method as an EPUB plus HTML download, including a RAG systems chapter and a system-design walkthrough.

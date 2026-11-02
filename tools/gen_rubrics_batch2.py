#!/usr/bin/env python3
"""Draft rubrics for the question pages that had no self-check rubric yet.

Concepts come from each page's model-answer steps; synonyms are the most distinctive terms of each step
that also appear in the page's sample answer. Output: tools/answer_check_data_batch2.py (static data, reviewable).
Run from the repo root: python3 tools/gen_rubrics_batch2.py  (needs the IB repo checked out next to this one)
"""
import importlib.util, math, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import answer_check_data as D
try:  # rubrics written by hand are the ones not produced by this script
    import answer_check_data_batch2 as B
    HAND_AIE = {k: v for k, v in D.AIE.items() if k not in B.AIE2}
    HAND_IB = {k: v for k, v in D.IB.items() if k not in B.IB2}
except ImportError:
    HAND_AIE, HAND_IB = D.AIE, D.IB
from question_pages_data import PAGES as AIE_PAGES

def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(spec)
    saved = {k: sys.modules.pop(k) for k in ("question_pages_batch2",) if k in sys.modules}  # same module name in both repos
    sys.path.insert(0, os.path.dirname(path)); spec.loader.exec_module(m); sys.path.pop(0)
    sys.modules.pop("question_pages_batch2", None); sys.modules.update(saved); return m
IB_PAGES = load(os.path.join(HERE, "..", "..", "investment-banking-interview-questions", "_tools", "question_pages_data.py"), "ibq").PAGES

STOP = set("""a an the and or but if then than so as of to in on at by for with from into onto over under about after before
between through during without within is are was were be been being it its it's this that these those there their they them
you your we our i me my he she his her not no nor do does did done can could would should will may might must shall
also just only very more most less least much many some any each every all both either neither one two three four five
first second third next last finally then when where which who whom whose what why how while because since until
say says said use uses used using make makes made get gets got give gives take takes put puts show shows tell tells
way ways thing things point points part parts kind sort lot lots well good better best bad high low same other another such
explain answer answers interview interviewer question questions example examples mention name state define describe walk
step steps case cases like often usually typically mostly rather instead even still yet already here now own new
know want need needs keep keeps look looks start starts close closes end ends line lines one-line sentence
answer model models token tokens change changes roughly large larger earlier call practical product output outputs input inputs problem
simple simply clear clearly real really important key main common great small smaller big bigger useful based level levels""".split())

def stem(w):
    for suf in ("ations", "ation", "ings", "ing", "ies", "ied", "ers", "ed", "es", "er", "ly", "s"):
        if w.endswith(suf) and len(w) - len(suf) >= 4:
            return w[: -len(suf)]
    return w

def toks(s):
    return re.findall(r"[a-z0-9][a-z0-9&/+.'-]*[a-z0-9&+]|[a-z0-9]", s.lower())

def page_text(p):
    return " ".join([p["q"], p["testing"], " ".join(p["steps"]), " ".join(p["sample"])]).lower()

ALL = AIE_PAGES + IB_PAGES
DF = {}
for p in ALL:
    for st in set(stem(t) for t in toks(page_text(p))):
        DF[st] = DF.get(st, 0) + 1

# Hand-written labels where the first clause of a step reads badly on its own.
LABEL_FIX = {
 ("pre-training-vs-instruction-tuning-vs-rlhf", 1): "Instruction tuning trains on prompt-response pairs so the model follows instructions",
 ("temperature-vs-top-p", 2): "Low temperature for extraction and code, moderate for brainstorming",
 ("what-is-quantization-in-llms", 3): "Post-training methods such as GPTQ and AWQ keep quality loss small at 4-bit",
 ("reasoning-models-vs-chat-models", 0): "Reasoning models are trained with reinforcement learning to think before answering",
 ("what-is-chain-of-thought-prompting", 3): "The cost: more output tokens, so higher cost and latency",
 ("what-is-hybrid-search", 0): "Run lexical (BM25) and dense vector search on the same query, then merge",
 ("what-is-hybrid-search", 1): "Merge with reciprocal rank fusion, which needs no comparable scores",
 ("what-is-re-ranking-in-rag", 0): "Retrieve a wide, cheap candidate set first, for example the top 50",
 ("what-is-the-react-pattern", 0): "ReAct interleaves reasoning, an action such as a tool call, and an observation",
 ("what-is-model-context-protocol-mcp", 2): "Servers expose tools, resources and prompts",
 ("workflows-vs-agents", 0): "In a workflow, code defines the steps and the LLM fills specific steps",
 ("how-to-make-llm-as-a-judge-reliable", 2): "Control known biases: position, length and self-preference",
 ("how-to-ab-test-an-ai-feature", 4): "Analyze honestly: avoid peeking, check segments, read sampled conversations",
 ("how-to-reduce-llm-latency", 0): "Measure the parts: time to first token, tokens per second, total time",
 ("how-to-reduce-llm-latency", 2): "Shorten inputs and outputs; output length often dominates",
 ("walk-me-through-the-enterprise-value-bridge", 1): "Add debt, including finance leases, and preferred stock",
 ("walk-me-through-the-enterprise-value-bridge", 2): "Add noncontrolling interest, because 100% of the subsidiary is consolidated",
 ("why-add-minority-interest-to-enterprise-value", 4): "Mirror case: equity-method investments are subtracted",
 ("lifo-vs-fifo", 2): "Under LIFO, lower taxable income means lower taxes and higher cash flow",
 ("unlevered-vs-levered-free-cash-flow", 1): "Unlevered FCF = EBIT x (1 - tax rate) + D&A - capex - increase in NWC",
 ("deferred-tax-asset-vs-deferred-tax-liability", 0): "Book income and taxable income differ in timing",
 ("operating-leases-asc-842", 0): "Balance sheet: a right-of-use asset and a lease liability",
 ("operating-leases-asc-842", 1): "Income statement: a single straight-line lease cost in operating expenses",
 ("how-do-you-calculate-cost-of-equity", 2): "Beta measures sensitivity to the market",
 ("how-to-build-a-comparable-companies-analysis", 3): "Normalize: remove non-recurring items and calendarize",
 ("how-to-build-a-comparable-companies-analysis", 4): "Compute multiples, look at the quartiles and median, apply a justified range",
 ("raise-discount-rate-by-1-percent-dcf", 0): "Value falls, because every future cash flow is discounted more heavily",
 ("ntm-vs-ltm-multiples", 0): "LTM uses actual reported results; NTM uses projected results",
 ("cash-vs-stock-consideration", 0): "Cash gives sellers certain value while the buyer keeps upside and risk",
 ("irr-vs-moic", 0): "MOIC: total value returned divided by equity invested, ignoring time",
 ("irr-vs-moic", 1): "IRR: the annualized return that makes NPV zero, so it reflects timing",
 ("why-our-bank", 3): "Link the firm's structure, such as group size, to how you want to learn",
 ("what-is-terminal-value-and-how-do-you-calculate-it", 1): "Gordon Growth: final-year FCF x (1 + g) / (discount rate - g)",
 ("gordon-growth-vs-exit-multiple", 1): "Gordon Growth: final-year FCF x (1 + g) / (discount rate - g)",
 ("beta-for-a-private-company", 2): "Unlever each peer beta: levered beta / (1 + (1 - t) x D/E)",
 ("beta-for-a-private-company", 4): "Relever at the target's D/E: unlevered beta x (1 + (1 - t) x D/E)",
 ("raise-discount-rate-by-1-percent-dcf", 2): "With g = 2%, the terminal multiple drops from 12.5x to 11.1x",
 ("what-is-accretion-dilution", 1): "Pro forma net income: both companies' net income plus synergies, minus deal financing costs",
 ("what-is-hybrid-search", 3): "A sensible default for enterprise and support search",
 ("irr-vs-moic", 2): "Single entry and exit shortcut: IRR = MOIC^(1 / years) - 1",
 ("multiple-expansion-vs-leverage", 2): "One more turn of leverage with flat EBITDA leaves returns at 1.0x",
 ("operating-leases-asc-842", 3): "Finance leases and IFRS 16: depreciation plus interest expense, so EBITDA excludes the lease cost",
 ("debt-funded-share-buyback-three-statements", 3): "Afterwards: interest expense lowers net income, cash and retained earnings",
}


# Everyday words that show up in vague answers; never enough on their own to count a concept as covered.
GENERIC = set("""year years exit money early total invest investment investor investors time times value values cash debt equity
company companies deal deals return returns price prices rate rates number numbers data user users system systems test tests
quality cost costs latency result results work works team teams business market markets growth risk risks zero
higher lower increase decrease grow grows less more amount amounts example process approach method fast faster slow slower""".split())


def esc(w):
    return re.sub(r"([.+*?^$()\[\]{}|\\/])", r"\\\1", w)

def word_rx(w):
    w = w.strip(".'")
    if re.fullmatch(r"[a-z0-9&/+]{1,4}", w):          # acronym or short token: exact word
        return r"\b" + esc(w) + r"\b"
    return r"\b" + esc(stem(w)) + r"\w*"

VERBS = {"define", "state", "say", "give", "mention", "explain", "compare", "point", "bring", "close", "start", "end", "name",
         "describe", "show", "add", "cover", "walk", "note", "finish", "open", "offer", "flag", "list", "contrast", "tie", "link"}
DANGLING = r"\s+(and|or|with|to|of|the|a|an|for|in|on|by|as|at|plus|but|that|when|where|which|so|than|is|are|x|vs|from|into|its|their|whose|while)$"


def label_of(step):
    s = re.sub(r"\s*\([^)]*\)", "", step.strip())
    m = re.match(r"([^:]{1,40}):\s+(.*)", s)
    if m:
        pre, rest = m.group(1), m.group(2)
        if pre.split()[0].lower() in VERBS or len(s) > 95:
            s = rest if len(rest) >= 12 else s
    s = re.split(r"; |(?<![A-Z]\.[a-z])(?<!e\.g)(?<!i\.e)\. (?=[A-Z])|, because | because |, so |, for example|, e\.g\.,?| such as ", s)[0]
    s = s.strip().rstrip(".:,; ")
    if len(s) > 95:
        k = s.rfind(", ", 0, 95)
        s = s[:k] if k > 30 else s[:95].rsplit(" ", 1)[0]
    for _ in range(3):
        s = re.sub(DANGLING, "", s, flags=re.I).rstrip(",;:= /-")
    return s[0].upper() + s[1:]


def concepts_for(p):
    sample = " ".join(p["sample"]).lower()
    title = set(stem(t) for t in toks(p["q"]))
    used, out = set(), []
    for si, step in enumerate(p["steps"]):
        ws = [t for t in toks(step)]
        cands = []
        for i, w in enumerate(ws):
            if w in STOP or len(w) < 3 or w.isdigit():
                continue
            generic = w in GENERIC or stem(w) in {stem(g) for g in GENERIC}
            st = stem(w)
            if st in title or st in used:
                continue
            r = word_rx(w)
            if not re.search(r, sample):
                continue
            score = DF.get(st, 99) + (30 if generic else 0)
            if len(w) <= 3 and not re.fullmatch(r"[a-z]{2,4}", w):
                score += 5
            cands.append((score, i, st, r))
            # bigram with the next content word, when it appears in the sample as a phrase
            if i + 1 < len(ws) and ws[i + 1] not in STOP and len(ws[i + 1]) >= 3:
                br = r"\b" + esc(stem(w)) + r"\w*[ -]" + esc(stem(ws[i + 1])) + r"\w*"
                if re.search(br, sample):
                    cands.append((score - 1.5, i, st + "+" + stem(ws[i + 1]), br))
        cands.sort()
        pick, seen = [], set()
        for limit in (18, 40, 70):   # prefer terms that appear on few pages; relax only if a step has none
            for sc, i, st, r in cands:
                base = st.split("+")[0]
                if base in seen or sc > limit:
                    continue
                pick.append(r); seen.add(base)
                if len(pick) == 4:
                    break
            if pick:
                break
        if not pick:
            continue
        used |= seen
        # Tighter than one hit: when a step yields two or more terms, an answer must use two of them.
        need = RX_FIX.get((p["slug"], si), (None, None))[1] or (2 if len(pick) >= 2 else 1)
        pick = RX_FIX.get((p["slug"], si), (None, None))[0] or pick
        out.append((LABEL_FIX.get((p["slug"], si)) or label_of(step), pick, need))
    return out[:8]

# Hand-written patterns where the generated terms are too generic: (slug, step index) -> ([regex], min hits).
RX_FIX = {
 ("irr-vs-moic", 0): ([r"divid\w*|\bover\b|\bper\b", r"\binvest\w*|\bequity\b", r"\btotal\w*|returned|proceeds", r"ignor\w*|regardless of time|not (account|consider)\w* (for )?tim\w*"], 3),
 ("irr-vs-moic", 1): ([r"annuali[sz]\w*|per year|compound\w*", r"\bnpv\b|net present value|discount rate", r"timing|time value|how fast|speed"], 2),
 ("irr-vs-moic", 2): ([r"\^|to the power|root", r"1 ?/ ?(years|n|t)\b|\bnth\b", r"single (entry|cash flow)|one (entry|exit)|entry and exit"], 2),
 ("irr-vs-moic", 3): ([r"\b\d(\.\d)?x\b", r"\b\d+ ?(%|percent)", r"\b\d+ years?\b"], 2),
 ("irr-vs-moic", 4): ([r"\bearly\w*|sooner|quick\w*", r"dividend recap\w*|distribution\w*|partial (exit|sale)", r"how much money|absolute|actual\w* (made|earned)|cash on cash"], 2),
}


def emit():
    lines = ["# Generated by tools/gen_rubrics_batch2.py from each page's model-answer steps and sample answer.",
             "# Same format as answer_check_data.py. Edit by hand if a concept reads badly, then rebuild answer-check.", ""]
    for name, pages, have in (("AIE2", AIE_PAGES, HAND_AIE), ("IB2", IB_PAGES, HAND_IB)):
        lines.append(f"{name} = {{")
        for p in pages:
            if p["slug"] in have:
                continue
            cs = concepts_for(p)
            assert len(cs) >= 3, (p["slug"], cs)
            head = f' "{p["slug"]}": {{' + (f'"q": {p["q"]!r}, ' if name == "IB2" else "") + '"concepts": ['
            lines.append(head)
            for lab, rx, need in cs:
                tail = f", {need}" if need > 1 else ""
                lines.append(f"  ({lab!r}, [{', '.join(repr(x) for x in rx)}]{tail}),")
            lines.append(" ]},")
        lines.append("}")
        lines.append("")
    lines.append("IB2_FOLLOWUPS = {")
    for p in IB_PAGES:
        if p["slug"] not in HAND_IB and p["followups"]:
            lines.append(f' "{p["slug"]}": {p["followups"][0][0]!r},')
    lines.append("}")
    open(os.path.join(HERE, "answer_check_data_batch2.py"), "w").write("\n".join(lines) + "\n")
    print("wrote answer_check_data_batch2.py")

if __name__ == "__main__":
    emit()

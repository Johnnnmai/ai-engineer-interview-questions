#!/usr/bin/env python3
"""Generate company interview pages (/companies/<slug>/), preparation guides (/guides/<slug>/), their indexes and /llms.txt.

Sources: content/companies/*.md and content/guides/*.md (reviewed copies; see README of the line 19/21 review).
Run from the repo root:  python3 tools/build_content_pages.py   then  python3 tools/build_question_pages.py  (sitemap picks up the new dirs)
Paid links go through buy_url() from build_question_pages, so EARLYBF stays controlled by the single OFFER_CODE constant there.
"""
import glob, html, json, os, re, sys
import markdown
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_question_pages as B
from build_question_pages import SITE, ROOT, BY_SLUG, head, foot, hero_buy, cta, sticky, buy_url

e = html.escape
FREE_TOP30 = "https://sirjohnnymai.gumroad.com/l/aie-top-30-questions"
DATE = "2026-11-01"
ARROW = '<span class=dot aria-hidden=true>&rarr;</span>'

COMPANY_RELATED = {
    "openai": ["what-is-function-calling", "how-do-you-evaluate-an-llm", "what-is-rag", "how-to-make-ai-agents-reliable-in-production"],
    "anthropic": ["how-do-you-evaluate-an-llm", "what-is-red-teaming-in-ai", "what-is-prompt-injection", "what-are-llm-guardrails"],
    "amazon": ["what-is-rag", "how-to-debug-poor-rag-answers", "how-to-reduce-llm-inference-cost"],
    "databricks": ["access-control-in-rag", "how-to-choose-a-chunking-strategy-for-rag", "how-do-you-evaluate-a-rag-system"],
    "google-deepmind": ["explain-the-transformer-architecture", "what-are-scaling-laws", "what-is-mixture-of-experts"],
    "meta": ["how-to-ab-test-an-ai-feature", "what-is-hybrid-search", "how-to-reduce-llm-latency"],
    "microsoft": ["how-do-you-evaluate-an-llm", "design-an-llm-gateway", "how-to-reduce-llm-latency"],
    "nvidia": ["what-is-kv-cache", "what-is-quantization-in-llms", "how-to-reduce-llm-latency", "what-is-mixture-of-experts"],
    "perplexity": ["what-is-hybrid-search", "what-is-re-ranking-in-rag", "why-do-llms-hallucinate"],
    "scale-ai": ["how-to-build-a-fine-tuning-dataset", "how-to-make-llm-as-a-judge-reliable", "how-do-you-evaluate-an-llm"],
    "google": ["explain-the-transformer-architecture", "what-is-kv-cache", "how-to-ab-test-an-ai-feature", "how-do-you-evaluate-a-rag-system"],
    "apple": ["what-is-quantization-in-llms", "how-to-reduce-llm-latency", "how-do-you-evaluate-an-llm", "what-is-prompt-injection"],
}
GUIDE_META = {
    "how-to-prepare-for-an-ai-engineer-interview-2026": ("Prepare for an AI engineer interview in 2026: Python coding, LLM and RAG fundamentals, evaluation and system design, with a practice checklist and FAQ.",
        ["what-is-rag", "what-is-kv-cache", "how-to-get-reliable-json-output-from-an-llm", "what-is-prompt-injection"]),
    "ai-engineer-vs-ml-engineer-interview": ("AI engineer vs ML engineer interviews: which topics get deeper questions, how system design and coding differ, and how to split your prep.",
        ["rag-vs-fine-tuning", "embedding-model-vs-generative-model", "how-to-build-a-fine-tuning-dataset"]),
    "rag-system-design-interview-scoring-rubric": ("A transparent 100-point practice rubric for RAG system design interviews: requirements, ingestion, retrieval, grounding, evaluation and production.",
        ["how-do-you-evaluate-a-rag-system", "access-control-in-rag", "what-is-re-ranking-in-rag", "how-to-choose-a-chunking-strategy-for-rag"]),
    "llm-evaluation-interview-questions": ("LLM evaluation interview questions with answers: datasets, RAG and hallucination checks, metrics, LLM judges, safety and release decisions.",
        ["how-do-you-evaluate-an-llm", "how-to-make-llm-as-a-judge-reliable", "what-is-benchmark-contamination"]),
    "two-week-ai-engineer-interview-study-plan": ("A 14-day AI engineer interview study plan: daily coding, LLM fundamentals, a small RAG build, evaluation and timed mock practice.",
        ["what-is-rag", "how-do-you-evaluate-a-rag-system", "explain-the-transformer-architecture"]),
    # Nov 3, 2026 SEO batch (seo_20261103): dated and tracked separately, see NEW_PAGES
    "rag-interview-questions": ("24 RAG interview questions with short model answers: chunking, embeddings, hybrid search, reranking, evaluation, permissions and debugging.",
        ["what-is-rag", "how-do-you-evaluate-a-rag-system", "how-to-debug-poor-rag-answers", "access-control-in-rag"]),
    "ai-agent-interview-questions": ("22 AI agent interview questions with answers: agent loops, tool calling, MCP, memory, multi-agent design, evaluation and guardrails.",
        ["what-is-an-ai-agent", "workflows-vs-agents", "what-is-function-calling", "how-to-make-ai-agents-reliable-in-production"]),
    "ai-system-design-interview-questions": ("15 AI and LLM system design interview prompts with answer outlines, a 45-minute structure and a self-scoring checklist.",
        ["design-an-llm-gateway", "design-a-customer-support-chatbot", "how-to-reduce-llm-inference-cost", "how-to-reduce-llm-latency"]),
    # seo5 batch (seo5_20261103): descriptions come from the md files, see SEO5
    "llm-interview-questions": (None, ["explain-the-transformer-architecture", "temperature-vs-top-p", "explain-lora-and-qlora", "what-is-kv-cache"]),
    "prompt-engineering-interview-questions": (None, ["what-is-chain-of-thought-prompting", "how-to-get-reliable-json-output-from-an-llm", "what-is-prompt-injection", "how-to-make-llm-as-a-judge-reliable"]),
}
# competitor alternative pages: content/alternatives/<slug>.md -> /alternatives/<slug>/ (index stays in build_alternatives.py)
ALT_META = {
    "exponent-alternatives": ["design-an-llm-gateway", "what-is-rag", "how-to-make-ai-agents-reliable-in-production"],
    "hello-interview-alternatives": ["design-a-customer-support-chatbot", "how-do-you-evaluate-a-rag-system", "what-is-model-context-protocol-mcp"],
    "interview-query-alternatives": ["rag-vs-fine-tuning", "explain-the-transformer-architecture", "how-to-make-llm-as-a-judge-reliable"],
}
ALT_ORDER = list(ALT_META)
NEW_PAGES = {"rag-interview-questions", "ai-agent-interview-questions", "ai-system-design-interview-questions"} | set(ALT_META)
NEW_DATE = "2026-11-03"

# ---- seo5 pages (campaign seo5_20261103) ----
# Every product link on these pages carries utm_source=qbank&utm_medium=seo&utm_campaign=seo5_20261103&utm_content=<page-slug>,
# with the placement in utm_term. Paid bases are B.CTA_URL and B.TIER9_URL, so OFFER_CODE in build_question_pages still controls
# EARLYBF: clear it and re-run, and the offer code and every promo line leave these pages too. No PM link (not PM or TPM pages).
SEO5 = {"interview-query-alternatives", "google", "apple", "llm-interview-questions", "prompt-engineering-interview-questions"}
NEW_PAGES |= SEO5
GUMROAD = "https://sirjohnnymai.gumroad.com/l/"
SEO5_BASES = {"ai-engineer-interview-playbook": lambda: B.CTA_URL, "aie-50-questions-scoring-rubric": lambda: B.TIER9_URL,
              "aie-top-30-questions": lambda: FREE_TOP30}


def s5(base, slug, term):
    return (base + ("&" if "?" in base else "?") + "utm_source=qbank&utm_medium=seo&utm_campaign=seo5_20261103"
            f"&utm_content={slug}&utm_term={term}")


def s5_tier9(slug, term):
    return f'<p class="alt-buy tier9">{B.TIER9_LEAD}<a href="{e(s5(B.TIER9_URL, slug, term))}">{B.TIER9_LINK_TEXT}</a>{B.TIER9_POST}</p>'


def s5_free(slug, term):
    return f'<p class=free-alt>Not ready to buy? <a href="{e(s5(FREE_TOP30, slug, term))}">Get the free Top 30 AI engineer questions PDF</a>.</p>'


def s5_hero(slug, ghost_href, ghost_text):
    return (f'<div class=acts><a class="btn btn-primary" href="{e(s5(B.CTA_URL, slug, "hero"))}">{B.CTA_BUTTON} {ARROW}</a>'
            f'<a class="btn btn-ghost" href="{ghost_href}">{ghost_text}</a></div>'
            f'<p class=price-line><span><span class=num>{B.PRICE}</span> on Gumroad, instant download</span>{B.promo()}</p>'
            + s5_tier9(slug, "hero_tier9"))


def s5_cta(slug, term):
    return (f'<div class=cta><span class=label>{B.CTA_LABEL}</span><b>{B.CTA_HEADLINE}</b><p>{e(B.CTA_TEXT)}</p>'
            f'<a class="btn btn-primary" href="{e(s5(B.CTA_URL, slug, term))}">{B.CTA_BUTTON} {ARROW}</a>{B.promo()}'
            + s5_tier9(slug, term + "_tier9") + s5_free(slug, term + "_free") + '</div>')


def s5_sticky(slug):
    deal = '<span class="long promo"> &middot; 40% off until Nov 3</span>' if B.PROMO_ON else f'<span class=long> &middot; {B.PRICE}</span>'
    short = '<span class="short promo"> &middot; 40% off</span>' if B.PROMO_ON else f'<span class=short> &middot; {B.PRICE}</span>'
    return (f'<div class=sticky-cta role=complementary aria-label="Buy the playbook" aria-hidden=true>'
            f'<span class=t><b><span class=full>{B.PRODUCT_NAME}</span><span class=short>{B.PRODUCT_SHORT}</span></b>{deal}{short}</span>'
            f'<a class=btn href="{e(s5(B.CTA_URL, slug, "sticky_bar"))}">Get it &rarr;</a></div>')


def s5_body_links(h, slug):
    """Product links written in the markdown get the seo5 utm and, for paid products, the OFFER_CODE base."""
    def sub(m):
        base = SEO5_BASES.get(m.group(1))
        return f'href="{e(s5(base(), slug, "body"))}"' if base else m.group(0)
    return re.sub(r'href="' + re.escape(GUMROAD) + r'([a-z0-9-]+)"', sub, h)



def utm_for(kind, slug):
    if slug in NEW_PAGES:
        return f"utm_source=qbank&utm_medium=seo&utm_campaign=seo_20261103&utm_content={slug}"
    camp = "line19_20261101" if kind == "company" else "line21_20261101"
    return f"utm_source=site&utm_medium=seo&utm_campaign={camp}"

GUIDE_ORDER = list(GUIDE_META)
COMPANY_ORDER = ["openai", "anthropic", "google-deepmind", "google", "apple", "meta", "microsoft", "amazon", "nvidia", "databricks", "scale-ai", "perplexity"]

EXTRA_CSS = """<style>
.body table{width:100%;border-collapse:collapse;font-size:var(--fs-small);margin:var(--s2) 0 var(--s3);display:block;overflow-x:auto}
.body th,.body td{text-align:left;padding:8px 10px;border-bottom:1px solid var(--line);vertical-align:top}
.body h3{margin:var(--s4) 0 var(--s1)}
.practice{background:var(--bg-soft);border:1px solid var(--line);border-radius:var(--r-lg);padding:var(--s3) var(--s4);margin:var(--s6) 0}
.practice ul{margin:var(--s1) 0 0;padding-left:1.2em}.practice li{margin:6px 0}
.free-alt{font-size:var(--fs-small);margin:4px 0 0}
.note{font-size:var(--fs-small);color:var(--ink-2)}
.cards{list-style:none;padding:0;display:grid;gap:var(--s2)}.cards a{display:block;border:1px solid var(--line);border-radius:var(--r-md);padding:var(--s3);text-decoration:none;color:var(--ink);background:var(--surface)}
.cards a b{display:block;font-size:1.1rem;margin:0 0 4px}.cards a span{color:var(--ink-2);font-size:var(--fs-small)}
</style>"""


def ld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False).replace("</", "<\\/") + "</script>"


def plain(md):
    s = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", md)
    s = re.sub(r"\*\*([^*]+)\*\*", r"\1", s)
    return re.sub(r"\s+", " ", s.replace("`", "")).strip()


def parse(path, kind):
    s = open(path).read().strip() + "\n"
    title = re.match(r"# (.+)\n", s).group(1).strip()
    s = s[s.index("\n") + 1:]
    desc = None
    m = re.search(r"\*\*Meta description:\*\* *(.+)\n", s)
    if m:
        desc = m.group(1).strip(); s = s.replace(m.group(0), "")
    # tables nested under list items: lift to top level so the tables extension renders them
    s = re.sub(r"(?m)^  (\|.*)$", r"\1", s)
    # FAQ items
    faq = []
    fm = re.search(r"\n## FAQ\n(.*)$", s, re.S)
    if fm:
        block = fm.group(1)
        if kind == "company":
            for q, a in re.findall(r"### (.+?)\n\n(.+?)(?=\n### |\Z)", block, re.S):
                faq.append((plain(q), plain(a)))
        else:
            for q, a in re.findall(r"^- \*\*(.+?)\*\* (.+)$", block, re.M):
                faq.append((plain(q), plain(a)))
    lead_m = re.search(r"## Quick answer\n\n(.+?)\n\n", s, re.S)
    lead = plain(lead_m.group(1)) if lead_m else plain(s.strip().split("\n\n")[0])
    return title, desc, s, faq, lead


def md_html(s):
    h = markdown.markdown(s, extensions=["tables"])
    h = re.sub(r'<a href="(https?://(?!johnnnmai\.github\.io)[^"]+)"', r'<a href="\1" rel="noopener">', h)
    return h.replace('href="https://johnnnmai.github.io/ai-engineer-interview-questions/', 'href="../../')


def practice_box(related, campaign, rel="../../"):
    q = "".join(f'<li><a href="{rel}questions/{s}/">{e(BY_SLUG[s]["q"])}</a></li>' for s in related)
    return (f'<aside class=practice><span class=label>Practice on this site, free</span>'
            f'<ul><li><a href="{rel}answer-check/">Answer self-check</a>: paste a spoken answer and see which concepts you missed</li>'
            f'<li><a href="{rel}study-plan/">Day-by-day study plan</a> from today to your interview date</li>'
            f'<li><a href="{rel}llm-cost-calculator/">LLM API cost calculator</a> for the cost questions in system design rounds</li></ul>'
            f'<p class=label style="margin-top:var(--s2)">Related question deep dives</p><ul>{q}</ul></aside>')


def free_alt(content, utm):
    u = FREE_TOP30 + "?" + utm + ("&utm_term=" if "utm_content=" in utm else "&utm_content=") + content
    return f'<p class=free-alt>Not ready to buy? <a href="{e(u)}">Get the free Top 30 AI engineer questions PDF</a>.</p>'


def build_page(kind, slug, path):
    title, desc, s, faq, lead = parse(path, kind)
    camp = "line19_20261101" if kind == "company" else "line21_20261101"
    utm = utm_for(kind, slug)
    folder = {"company": "companies", "guide": "guides", "alternative": "alternatives"}[kind]
    related = COMPANY_RELATED[slug] if kind == "company" else ALT_META[slug] if kind == "alternative" else GUIDE_META[slug][1]
    for r in related:
        assert r in BY_SLUG, r
    desc = desc or GUIDE_META[slug][0]
    date = NEW_DATE if slug in NEW_PAGES else DATE
    url = f"{SITE}/{folder}/{slug}/"
    rel = "../../"
    article = {"@context": "https://schema.org", "@type": "Article", "headline": title, "description": desc,
               "datePublished": date, "dateModified": date, "mainEntityOfPage": url, "inLanguage": "en",
               "author": {"@type": "Organization", "name": "Valenx Press"},
               "publisher": {"@type": "Organization", "name": "Valenx Press"}}
    tags = ld(article)
    if faq:
        tags += ld({"@context": "https://schema.org", "@type": "FAQPage",
                    "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]})
    body = md_html(s)
    seo5 = slug in SEO5
    if seo5:
        body = s5_body_links(body, slug)
    # split before FAQ to place a mid-page CTA and the practice box
    parts = body.split("<h2>FAQ</h2>")
    crumb = {"company": "Company interview guides", "guide": "Prep guides", "alternative": "Alternatives"}[kind]
    o = [head(title, desc, url, rel, tags + EXTRA_CSS)]
    o.append(f'<header class=qhero data-hero><div class=wrap><div class="crumb label"><a href="{rel}">{B.SITE_NAME}</a> / <a href="../">{crumb}</a></div>'
             f'<h1>{e(title)}</h1><p class=lead>{e(lead)}</p>' + (s5_hero(slug, f"{rel}answer-check/", "Score my answer free") if seo5 else hero_buy(slug, f"{rel}answer-check/", "Score my answer free", utm)) + '</div></header>')
    o.append('<main id=main class=body><div class=read>')
    if kind == "company":
        o.append('<p class=note>Independent preparation guide by Valenx Press. Not affiliated with or endorsed by the company named. '
                 'Interview stages below are a general industry pattern; the linked public careers pages are the only company sources used.</p>')
    if kind == "alternative":
        o.append('<p class=note>Independent comparison by Valenx Press, publisher of the free question bank and the Playbook listed here. '
                 'Not affiliated with or endorsed by the other products named. Prices and features were read from each seller&rsquo;s public page '
                 'on Nov 2, 2026 unless marked otherwise; sellers change prices, so check before you buy.</p>')
    o.append(parts[0])
    o.append(practice_box(related, camp))
    o.append(s5_cta(slug, "cta_mid") if seo5 else cta(slug, "cta_mid", utm, free_alt(f"{slug}_mid_free", utm)))
    if len(parts) > 1:
        o.append("<h2>FAQ</h2>" + parts[1])
    o.append(s5_cta(slug, "cta_end") if seo5 else cta(slug, "cta_end", utm, free_alt(f"{slug}_end_free", utm)))
    if kind == "alternative":
        o.append(f'<p><a href="../">All alternatives</a> &middot; <a href="{rel}guides/">Prep guides</a> &middot; <a href="{rel}questions/">Question deep dives</a></p>')
    else:
        o.append(f'<p><a href="../">All {crumb.lower()}</a> &middot; <a href="{rel}{"guides" if kind == "company" else "companies"}/">'
               f'{"Prep guides" if kind == "company" else "Company interview guides"}</a> &middot; <a href="{rel}questions/">Question deep dives</a></p>')
    o.append('</div></main>' + (s5_sticky(slug) if seo5 else sticky(slug, utm)) + foot(rel))
    return "".join(o), title, desc


def build_index(kind, items):
    folder = "companies" if kind == "company" else "guides"
    camp = "line19_20261101" if kind == "company" else "line21_20261101"
    utm = f"utm_source=site&utm_medium=seo&utm_campaign={camp}"
    url = f"{SITE}/{folder}/"
    rel = "../"
    if kind == "company":
        title = "AI Engineer Interview Guides by Company (2026): OpenAI, Anthropic, DeepMind and more"
        desc = f"Independent AI engineer interview prep for {len(items)} companies: public careers themes, a general loop, practice questions with scoring points, and FAQs."
        lead = f"{len(items)} independent prep guides. Each one links only the company's own public careers pages and labels interview stages as a general industry pattern."
    else:
        title = "AI Engineer Interview Prep Guides (2026)"
        desc = "Free AI engineer interview prep guides: LLM, prompt engineering, RAG, AI agent and system design questions, LLM evaluation, a RAG rubric and a 2-week plan."
        lead = f"{len(items)} practical guides with public sources, practice rubrics and FAQs."
    cards = "".join(f'<li><a href="{s}/"><b>{e(t)}</b><span>{e(d)}</span></a></li>' for s, t, d in items)
    o = [head(title, desc, url, rel, EXTRA_CSS)]
    o.append(f'<header class="qhero idx" data-hero><div class=wrap><div class="crumb label"><a href="{rel}">{B.SITE_NAME}</a> / {"Companies" if kind == "company" else "Guides"}</div>'
             f'<h1>{e(title)}</h1><p class=lead>{e(lead)}</p>' + hero_buy(f"{folder}-index", f"{rel}answer-check/", "Score my answer free", utm) + '</div></header>')
    o.append(f'<main id=main class=body><div class=read><ul class=cards>{cards}</ul>')
    o.append(practice_box(["what-is-rag", "how-do-you-evaluate-an-llm", "design-an-llm-gateway"], camp, rel))
    o.append(cta(f"{folder}-index", "cta_box", utm, free_alt(f"{folder}_index_free", utm)))
    o.append(f'<p><a href="{rel}{"guides" if kind == "company" else "companies"}/">{"Prep guides" if kind == "company" else "Company interview guides"}</a> &middot; <a href="{rel}questions/">Question deep dives</a></p>')
    o.append('</div></main>' + sticky(f"{folder}-index", utm) + foot(rel))
    return "".join(o)


def llms_txt(comp, guides, alts=None):
    L = ["# AI Engineer Interview Questions (Valenx Press)", "",
         "> A free, answer-first AI engineer interview question bank covering LLM fundamentals, RAG, agents, evaluation, system design and production, "
         "with free browser tools (answer self-check, study plan, LLM API cost calculator, mock round timer) and preparation guides.", "",
         "Content is educational interview preparation, not a record of questions asked by specific employers. Company guides cite only official public careers pages "
         "and describe interview stages as a general industry pattern. Rubrics are practice aids, not hiring standards.", "",
         "## Question bank", "",
         f"- [AI engineer interview questions with answers]({SITE}/): the full question bank on one page",
         f"- [Question deep dives]({SITE}/questions/): one page per question with framework, sample answer and follow-ups",
         f"- [Chinese mirror (first 20 questions)]({SITE}/zh/)" if os.path.isdir(os.path.join(ROOT, "zh")) else None, "",
         "## Free tools", "",
         f"- [Answer self-check]({SITE}/answer-check/): score a practiced answer against a rubric in the browser",
         f"- [Study plan]({SITE}/study-plan/): day-by-day plan from today to the interview date",
         f"- [LLM API cost calculator]({SITE}/llm-cost-calculator/): cost per request, day and month from official list prices",
         f"- [Mock interview round]({SITE}/mock-interview/): timed practice round", "",
         "## Comparisons", "",
         f"- [AI engineer interview prep alternatives]({SITE}/alternatives/): ByteByteGo, Educative, Gumroad guides and free options by price and format",
         *[f"- [{t}]({SITE}/alternatives/{s}/): {d}" for s, t, d in (alts or [])], "",
         "## Preparation guides", ""]
    L += [f"- [{t}]({SITE}/guides/{s}/): {d}" for s, t, d in guides]
    L += ["", "## Company interview guides", ""]
    L += [f"- [{t}]({SITE}/companies/{s}/)" for s, t, d in comp]
    return "\n".join(x for x in L if x is not None) + "\n"


def main():
    comp, guides = [], []
    for kind, order, store in (("company", COMPANY_ORDER, comp), ("guide", GUIDE_ORDER, guides)):
        folder = "companies" if kind == "company" else "guides"
        for slug in order:
            page, t, d = build_page(kind, slug, os.path.join(ROOT, "content", folder, slug + ".md"))
            os.makedirs(os.path.join(ROOT, folder, slug), exist_ok=True)
            open(os.path.join(ROOT, folder, slug, "index.html"), "w").write(page)
            store.append((slug, t, d))
        open(os.path.join(ROOT, folder, "index.html"), "w").write(build_index(kind, store))
    alts = []
    for slug in ALT_ORDER:
        page, t, d = build_page("alternative", slug, os.path.join(ROOT, "content", "alternatives", slug + ".md"))
        os.makedirs(os.path.join(ROOT, "alternatives", slug), exist_ok=True)
        open(os.path.join(ROOT, "alternatives", slug, "index.html"), "w").write(page)
        alts.append((slug, t, d))
    open(os.path.join(ROOT, "llms.txt"), "w").write(llms_txt(comp, guides, alts))
    print(f"built {len(comp)} company pages, {len(guides)} guides, {len(alts)} alternatives, 2 indexes, llms.txt")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Generate /questions/ SEO pages, the questions index, sitemap.xml and robots.txt.

Run from the repo root:  python3 tools/build_question_pages.py
To swap the call-to-action (for example to a free PDF), edit the CTA_* constants below and re-run.
"""
import html, json, os, re, sys
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from question_pages_data import PAGES
try:
    from answer_check_data import AIE as _AC_AIE
except ImportError:
    _AC_AIE = {}

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://johnnnmai.github.io/ai-engineer-interview-questions"
SITE_NAME = "AI Engineer Interview Questions"
LASTMOD = "2026-11-01"

# ---- CTA: the single place to change the offer ----
# Every primary buy link in this repo (question pages, root, questions index, answer-check aie track, mock-interview aie track, alternatives) is built from CTA_URL.
# EARLYBF lives in this one constant. When it ends (Nov 3 2026 11:59 PM PT), set OFFER_CODE = "" and re-run the builders:
# every paid link (question pages, answer-check, mock round, alternatives, LLM cost calculator, study plan) and every promo line drops it.
OFFER_CODE = "EARLYBF"  # 40% off until Nov 3 2026 11:59 PM PT
OFFER_Q = f"?offer_code={OFFER_CODE}" if OFFER_CODE else ""
CTA_URL = "https://sirjohnnymai.gumroad.com/l/ai-engineer-interview-playbook" + OFFER_Q
OFFER_EXPIRES = "2026-11-04T07:59:00Z"  # EARLYBF expiry read from the Gumroad product page; promo lines also hide client-side after it
PROMO_TEXT = "40% off with code EARLYBF until Nov 3, 11:59 PM PT"
PROMO_SHORT = "EARLYBF: 40% off until Nov 3"  # badge text under 560px so the pill stays on one line at 320 to 375
PROMO_HTML = f'<span class=pl>{PROMO_TEXT}</span><span class=ps>{PROMO_SHORT}</span>'
PRICE = "$19.99"  # list price on the Gumroad product page, Nov 1 2026
PRODUCT_NAME = "The 0&rarr;1 AI Engineer Interview Playbook"
PRODUCT_SHORT = "The Playbook"
CTA_LABEL = "The Playbook"
CTA_UTM = "utm_source=seo&utm_medium=qpage&utm_campaign={slug}"
CTA_HEADLINE = "Want the full method?"
CTA_TEXT = "The 0 to 1 AI Engineer Interview Playbook covers the answer frameworks, system-design walkthroughs and an 8-week plan."
CTA_BUTTON = "Get the playbook"
# Secondary text link only: the PM direction bundle (North America Interview Full Package, slug xzptir). PM and TPM content, not AI engineer prep.
# EARLYBF checked on Nov 1 2026: valid on this product, 40% off.
PM_URL = "https://sirjohnnymai.gumroad.com/l/xzptir" + OFFER_Q
PM_NAME = "North America Interview Full Package"
PM_PRICE = "$59"  # list price on the live Gumroad product page, Nov 1 2026
PM_LEAD = "Interviewing for PM or TPM? "
PM_LINK_TEXT = "See the full PM package"
PM_POST = f", {PM_PRICE} on Gumroad: a resume system, a PM, TPM and PGM interview handbook, a 1:1 cheat sheet and a PM playbook. PM and TPM content, not AI engineer prep."
# $9 tier, secondary only (the playbook above stays primary): the 50-question scoring rubric PDFs on Gumroad.
# Both use OFFER_Q, so EARLYBF leaves these links when OFFER_CODE is cleared. EARLYBF checked Nov 1 2026: valid on both, 40% off.
# Placements: question pages, questions index and root (hero_buy + cta), answer-check and mock round (aie track: AIE rubric, ib track: IB rubric).
TIER9_URL = "https://sirjohnnymai.gumroad.com/l/aie-50-questions-scoring-rubric" + OFFER_Q
IB_TIER9_URL = "https://sirjohnnymai.gumroad.com/l/ib-50-questions-scoring-rubric" + OFFER_Q
TIER9_UTM = "utm_source=site&utm_medium=cta&utm_campaign=tripwire9_20261101"
TIER9_PRICE = "$9"  # list price on both Gumroad product pages, Nov 1 2026
TIER9_LEAD = "Smaller start: "
TIER9_LINK_TEXT = f"Score your answers against 50 rubrics, {TIER9_PRICE}"
TIER9_POST = ". 50 AI engineer questions, one rubric each, PDF on Gumroad."
IB_TIER9_LINK_TEXT = f"Score your answers against 50 IB rubrics, {TIER9_PRICE}"
IB_TIER9_POST = ". 50 investment banking questions, one rubric each, PDF on Gumroad."
# ----------------------------------------------------
PROMO_ON = bool(OFFER_CODE)

e = html.escape
try:  # line 20 Chinese mirror: hreflang back-links and /zh/ sitemap entries
    from zh_mirror_data import ZH_URLS, zh_alternates
except ImportError:
    ZH_URLS, zh_alternates = [], (lambda slug=None: "")
UTM_SCRIPT = open(os.path.join(ROOT, "tools", "utm_passthrough.html")).read().strip()  # copies a visitor's utm_source onto Gumroad links
BY_SLUG = {p["slug"]: p for p in PAGES}
LVL = {"Entry": "E", "Mid": "M", "Senior": "S"}
ARROW = '<span class=dot aria-hidden=true>&rarr;</span>'
UI_SCRIPT = ('<script>(function(){var b=document.querySelector(".sticky-cta"),h=document.querySelector("[data-hero]");'
             'if(b&&h){document.body.classList.add("has-sticky");var f=function(){var on=h.getBoundingClientRect().bottom<0;'
             'b.classList.toggle("show",on);b.setAttribute("aria-hidden",on?"false":"true");};addEventListener("scroll",f,{passive:true});f();}'
             'var u=document.documentElement.getAttribute("data-offer-until");if(u&&Date.now()>=Date.parse(u)){'
             'var p=document.querySelectorAll(".promo");for(var i=0;i<p.length;i++)p[i].hidden=true;}})();</script>')


def buy_url(slug, content, utm=None, base=None):
    base = base or CTA_URL
    utm = utm or CTA_UTM.format(slug=slug)
    # page-level utm that already names the page (seo_20261103 batch) carries the link position in utm_term instead
    return base + ("&" if "?" in base else "?") + utm + ("&utm_term=" if "utm_content=" in utm else "&utm_content=") + content


def alt_link(slug, content="pm_link", utm=None):
    """Secondary text link to the PM direction bundle."""
    return f'<p class=alt-buy>{PM_LEAD}<a href="{e(buy_url(slug, content, utm, PM_URL))}">{PM_LINK_TEXT}</a>{PM_POST}</p>'


def tier9_url(content, base=None):
    base = base or TIER9_URL
    return base + ("&" if "?" in base else "?") + TIER9_UTM + "&utm_content=" + content


def tier9_link(content, ib=False):
    """Secondary text link to the $9 scoring rubric, shown next to the primary playbook CTA."""
    href = tier9_url(content, IB_TIER9_URL if ib else TIER9_URL)
    text, post = (IB_TIER9_LINK_TEXT, IB_TIER9_POST) if ib else (TIER9_LINK_TEXT, TIER9_POST)
    return f'<p class="alt-buy tier9">{TIER9_LEAD}<a href="{e(href)}">{text}</a>{post}</p>'


def promo(cls="badge promo"):
    return f'<span class="{cls}">{PROMO_HTML if "badge" in cls else PROMO_TEXT}</span>' if PROMO_ON else ""


def cta(slug, content="cta_box", utm=None, extra=""):
    return (f'<div class=cta><span class=label>{CTA_LABEL}</span><b>{CTA_HEADLINE}</b><p>{e(CTA_TEXT)}</p>'
            f'<a class="btn btn-primary" href="{e(buy_url(slug, content, utm))}">{CTA_BUTTON} {ARROW}</a>{promo()}'
            f'{tier9_link(slug + "_" + content)}'
            f'{alt_link(slug, content.replace("cta", "pm", 1) if content.startswith("cta") else "pm_" + content, utm)}{extra}</div>')


def hero_buy(slug, ghost_href, ghost_text, utm=None):
    return (f'<div class=acts><a class="btn btn-primary" href="{e(buy_url(slug, "hero", utm))}">{CTA_BUTTON} {ARROW}</a>'
            f'<a class="btn btn-ghost" href="{ghost_href}">{ghost_text}</a></div>'
            f'<p class=price-line><span><span class=num>{PRICE}</span> on Gumroad, instant download</span>{promo()}</p>'
            f'{tier9_link(slug + "_hero")}')


def sticky(slug, utm=None):
    deal = f'<span class="long promo"> &middot; 40% off until Nov 3</span>' if PROMO_ON else f'<span class=long> &middot; {PRICE}</span>'
    short = '<span class="short promo"> &middot; 40% off</span>' if PROMO_ON else f'<span class=short> &middot; {PRICE}</span>'
    return (f'<div class=sticky-cta role=complementary aria-label="Buy the playbook" aria-hidden=true>'
            f'<span class=t><b><span class=full>{PRODUCT_NAME}</span><span class=short>{PRODUCT_SHORT}</span></b>{deal}{short}</span>'
            f'<a class=btn href="{e(buy_url(slug, "sticky_bar", utm))}">Get it &rarr;</a></div>')


def preview_card(slug, rel):
    return (f'<li><div class=pcard><img src="{rel}assets/playbook-cover.webp" width=333 height=465 loading=lazy '
            f'alt="Cover of {PRODUCT_NAME.replace("&rarr;", " to ")}, 2026 edition, Valenx Press">'
            f'<div><span class=label>The Playbook &middot; 2026 edition</span><h2>{PRODUCT_NAME}</h2><p>{e(CTA_TEXT)}</p>'
            f'<ul class=spec><li><span>Publisher</span><span>Valenx Press</span></li>'
            f'<li><span>Format</span><span>Digital download on Gumroad</span></li>'
            f'<li><span>Price</span><span>{PRICE}</span></li></ul>'
            f'<div class=acts><a class="btn btn-primary" href="{e(buy_url(slug, "preview_card"))}">{CTA_BUTTON} {ARROW}</a>{promo()}</div>'
            f'{alt_link(slug, "preview_card_pm")}</div></div></li>')


def icons(rel):
    return (f'<link rel=icon href="{rel}favicon.ico" sizes=any><link rel=icon type="image/svg+xml" href="{rel}assets/favicon.svg">'
            f'<link rel=apple-touch-icon href="{rel}assets/apple-touch-icon.png">')


def head(title, desc, url, rel, extra=""):
    until = f' data-offer-until="{OFFER_EXPIRES}"' if PROMO_ON else ""
    return (f'<!doctype html><html lang=en{until}><head><meta charset=utf-8>'
            f'<meta name=viewport content="width=device-width,initial-scale=1">'
            f'<title>{e(title)}</title><meta name=description content="{e(desc)}">'
            f'<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}">'
            f'<meta property="og:type" content="article"><meta property="og:url" content="{url}">'
            f'<meta property="og:image" content="{SITE}/assets/playbook-og.jpg"><meta name="twitter:card" content="summary_large_image">'
            f'<link rel=canonical href="{url}">{icons(rel)}<link rel=preconnect href="https://fonts.googleapis.com">'
            f'<link rel=preconnect href="https://fonts.gstatic.com" crossorigin><link rel=stylesheet href="{rel}assets/valenx.css">{extra}</head>'
            f'<body><a class=skip href="#main">Skip to content</a>'
            f'<nav class=nav aria-label="Site"><a class=brand href="{rel}"><span class=mark>VP</span>Valenx Press<span class=long>&nbsp;&middot; {SITE_NAME}</span></a>'
            f'<div class=nav-group><a href="{rel}questions/">Questions</a><a href="{rel}answer-check/">Self-check</a><a class=hide-sm href="{rel}">All 100</a></div></nav>')


def foot(rel, deep=True):
    dd = f'<a href="{rel}questions/">Question deep dives</a> &middot; ' if deep else ""
    return (f'<footer class=site><div class=wrap>&copy; 2026 Valenx Press &middot; <a href="{rel}">All 100 AI engineer interview questions</a> &middot; '
            f'{dd}Free tools: <a href="{rel}answer-check/">Answer self-check</a> &middot; <a href="{rel}study-plan/">Study plan</a> &middot; '
            f'<a href="{rel}llm-cost-calculator/">LLM cost calculator</a> &middot; <a href="{rel}mock-interview/">Mock round</a> &middot; '
            f'Guides: <a href="{rel}companies/">Company interview guides</a> &middot; <a href="{rel}guides/">Prep guides</a> &middot; '
            f'Questions reflect common public interview patterns; no company affiliation.</div></footer>'
            f'{UTM_SCRIPT}{UI_SCRIPT}</body></html>\n')


def page(p):
    url = f"{SITE}/questions/{p['slug']}/"
    rel = "../../"
    faq = [{"@type": "Question", "name": p["q"],
            "acceptedAnswer": {"@type": "Answer", "text": " ".join(p["sample"])}}]
    faq += [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in p["followups"]]
    ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": faq}
    ld_tag = '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False).replace("</", "<\\/") + "</script>"
    src = ", ".join(f'<a href="../../#q{n}">#{n}</a>' for n in p["src"])
    ac = "../../answer-check/" + (f"?track=aie&amp;q={p['slug']}" if p["slug"] in _AC_AIE else "")
    o = [head(p["q"], p["desc"], url, rel, ld_tag + zh_alternates(p["slug"]))]
    o.append(f'<header class=qhero data-hero><div class=wrap><div class="crumb label"><a href="../../">{SITE_NAME}</a> / <a href="../">Questions</a></div>'
             f'<span class="lvl {LVL[p["level"]]}">{p["level"]}</span><h1>{e(p["q"])}</h1>'
             f'<p class=lead>How to answer it in an AI engineer interview: what is being tested, a step-by-step framework, a sample answer and the mistakes to avoid.</p>'
             + hero_buy(p["slug"], ac, "Score my answer free") + '</div></header>')
    o.append('<main id=main class=body><div class=read>')
    o.append(f'<p class=selfcheck><b>Practiced one out loud?</b> <a href="{ac}">Paste your answer into the free self-check and get a score in 30 seconds</a></p>')
    o.append(f'<h2>What the interviewer is testing</h2><p>{e(p["testing"])}</p>')
    o.append('<h2>Answer framework</h2><ol class=steps>' + "".join(f"<li>{e(s)}</li>" for s in p["steps"]) + "</ol>")
    o.append('<h2>Sample answer</h2><div class=sample>' + "".join(f"<p class=ans>{e(s)}</p>" for s in p["sample"]) + "</div>")
    if p["followups"]:
        o.append('<h2>Likely follow-ups</h2>' + "".join(f'<div class=fu><b>{e(q)}</b> {e(a)}</div>' for q, a in p["followups"]))
    o.append('<h2>Common mistakes</h2><ul class=mist>' + "".join(f"<li>{e(m)}</li>" for m in p["mistakes"]) + "</ul>")
    o.append(cta(p["slug"]))
    o.append('<h2>Related questions</h2><ul class=related>' +
             "".join(f'<li><a href="../{r}/">{e(BY_SLUG[r]["q"])}</a></li>' for r in p["related"]) + topic_links(p["slug"]) +
             f'<li><a href="../../study-plan/">Build a day-by-day study plan to your interview date</a></li><li><a href="../../llm-cost-calculator/">Estimate LLM API cost per day and month</a></li>'
             f'<li><a href="../../mock-interview/">Run a timed mock interview round</a></li><li><a href="../../alternatives/">Compare AI engineer interview prep options</a></li>'
             f'<li><a href="../">All question deep dives</a></li><li><a href="../../">All 100 AI engineer interview questions with answers</a></li></ul>')
    o.append(f'<p class=muted>Based on question {src} in the full question bank.</p>')
    o.append('</div></main>' + sticky(p["slug"]))
    o.append(foot(rel))
    return "".join(o)


# topic hub links from question pages to the Nov 3, 2026 guides (built by tools/build_content_pages.py)
_RAG = ("rag-interview-questions", "RAG interview questions: 24 questions from basics to production")
_AGENT = ("ai-agent-interview-questions", "AI agent interview questions: 22 agentic AI questions with answers")
_SD = ("ai-system-design-interview-questions", "AI system design interview questions: 15 LLM design prompts")
TOPIC_GUIDES = {s: [_RAG] for s in ("what-is-rag", "how-do-you-evaluate-a-rag-system", "how-to-debug-poor-rag-answers", "how-to-choose-a-chunking-strategy-for-rag",
                                     "what-is-re-ranking-in-rag", "what-is-hybrid-search", "access-control-in-rag", "rag-vs-fine-tuning", "how-to-choose-an-embedding-model",
                                     "hnsw-vs-ivf", "what-is-lost-in-the-middle")}
TOPIC_GUIDES.update({s: [_AGENT] for s in ("what-is-an-ai-agent", "what-is-the-react-pattern", "single-agent-vs-multi-agent", "workflows-vs-agents",
                                            "how-to-make-ai-agents-reliable-in-production", "how-to-handle-memory-in-ai-agents", "what-is-function-calling",
                                            "what-is-model-context-protocol-mcp")})
TOPIC_GUIDES.update({s: [_SD] for s in ("design-an-llm-gateway", "design-a-customer-support-chatbot", "how-to-reduce-llm-latency", "how-to-reduce-llm-inference-cost",
                                         "how-to-cache-llm-responses")})
NEW_URL_DATES = {f"{SITE}/guides/{g}/": "2026-11-03" for g in (_RAG[0], _AGENT[0], _SD[0])}
NEW_URL_DATES.update({f"{SITE}/alternatives/{a}/": "2026-11-03" for a in ("exponent-alternatives", "hello-interview-alternatives")})
NEW_URL_DATES.update({f"{SITE}/{p}/": "2026-11-03" for p in ("alternatives/interview-query-alternatives", "companies/google", "companies/apple",
                                                           "guides/llm-interview-questions", "guides/prompt-engineering-interview-questions")})


def topic_links(slug):
    return "".join(f'<li><a href="../../guides/{g}/">{e(t)}</a></li>' for g, t in TOPIC_GUIDES.get(slug, []))


def index():
    url = f"{SITE}/questions/"
    rel = "../"
    title = "AI Engineer Interview Questions: Answer Frameworks and Sample Answers"
    desc = "Deep dives on the most-asked AI engineer interview questions: RAG, transformers, KV cache, LoRA, evals, agents and prompt injection, with sample answers."
    cnt = {k: sum(1 for p in PAGES if p["level"] == k) for k in LVL}
    o = [head(title, desc, url, rel, zh_alternates(None))]
    o.append(f'<header class="qhero idx" data-hero><div class=wrap><div class="crumb label"><a href="../">{SITE_NAME}</a> / Questions</div>'
             f'<span class=bignum aria-hidden=true>{len(PAGES)}<em>deep dives</em></span><h1>{e(title)}</h1>'
             '<p class=lead>One page per question: what the interviewer is testing, an answer framework, a sample answer, follow-ups and common mistakes.</p>'
             + hero_buy("questions-index", "../answer-check/", "Score my answer free") +
             '<div class=chips>' + "".join(f'<span class="lvl {LVL[k]}">{cnt[k]} {k}</span>' for k in LVL) +
             '<span class=chip>Sample answer on every page</span></div></div></header>')
    o.append('<main id=main class=body><div class=read>')
    o.append('<p class=selfcheck><b>Practiced one out loud?</b> <a href="../answer-check/">Paste your answer into the free self-check and get a score in 30 seconds</a></p>')
    o.append('<ol class=qlist>')
    for i, p in enumerate(PAGES, 1):
        o.append(f'<li><a class=qcard href="{p["slug"]}/"><span class=n>{i:02d}</span><span class="lvl {LVL[p["level"]]}">{p["level"]}</span>'
                 f'<b>{e(p["q"])}</b><span class=d>{e(p["desc"])}</span></a></li>')
        if i == 3:
            o.append(preview_card("questions-index", rel))
    o.append('</ol>')
    o.append('<p><b>Practice tool:</b> <a href="../answer-check/">Check your interview answer with the free Answer Self-Check</a> (score, missed concepts and tips).</p>')
    o.append('<p><a href="../">See all 100 AI engineer interview questions with answers</a></p>')
    o.append(cta("questions-index") + '</div></main>' + sticky("questions-index"))
    o.append(foot(rel, deep=False))
    return "".join(o)


def main():
    for p in PAGES:
        d = os.path.join(ROOT, "questions", p["slug"])
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "index.html"), "w").write(page(p))
    open(os.path.join(ROOT, "questions", "index.html"), "w").write(index())
    urls = [f"{SITE}/", f"{SITE}/questions/"] + [f"{SITE}/questions/{p['slug']}/" for p in PAGES] + [f"{SITE}/answer-check/", f"{SITE}/mock-interview/", f"{SITE}/alternatives/", f"{SITE}/llm-cost-calculator/", f"{SITE}/study-plan/"]
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    sm += [f"  <url><loc>{u}</loc><lastmod>{LASTMOD}</lastmod></url>" for u in urls]
    sm += [f"  <url><loc>{u}</loc><lastmod>{LASTMOD}</lastmod></url>" for u in ZH_URLS]
    # line 19/21 company pages and prep guides (built by tools/build_content_pages.py)
    for d in ("companies", "guides", "alternatives"):
        if os.path.isfile(os.path.join(ROOT, d, "index.html")):
            if d != "alternatives":  # /alternatives/ is already in urls above
                sm.append(f"  <url><loc>{SITE}/{d}/</loc><lastmod>{LASTMOD}</lastmod></url>")
            sm += [f"  <url><loc>{SITE}/{d}/{x}/</loc><lastmod>{NEW_URL_DATES.get(f'{SITE}/{d}/{x}/', LASTMOD)}</lastmod></url>"
                   for x in sorted(os.listdir(os.path.join(ROOT, d))) if os.path.isfile(os.path.join(ROOT, d, x, "index.html"))]
    sm.append("</urlset>")
    open(os.path.join(ROOT, "sitemap.xml"), "w").write("\n".join(sm) + "\n")
    rb = os.path.join(ROOT, "robots.txt")
    r = open(rb).read() if os.path.exists(rb) else "User-agent: *\nAllow: /\n"
    line = f"Sitemap: {SITE}/sitemap.xml"
    if line not in r:
        r = r.rstrip("\n") + "\n" + line + "\n"
    open(rb, "w").write(r)
    print(f"built {len(PAGES)} pages + index, sitemap with {len(urls)} urls")


if __name__ == "__main__":
    main()

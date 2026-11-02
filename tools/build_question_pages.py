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
# ----------------------------------------------------
PROMO_ON = bool(OFFER_CODE)

e = html.escape
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
    return base + ("&" if "?" in base else "?") + (utm or CTA_UTM.format(slug=slug)) + "&utm_content=" + content


def alt_link(slug, content="pm_link", utm=None):
    """Secondary text link to the PM direction bundle."""
    return f'<p class=alt-buy>{PM_LEAD}<a href="{e(buy_url(slug, content, utm, PM_URL))}">{PM_LINK_TEXT}</a>{PM_POST}</p>'


def promo(cls="badge promo"):
    return f'<span class="{cls}">{PROMO_TEXT}</span>' if PROMO_ON else ""


def cta(slug, content="cta_box", utm=None, extra=""):
    return (f'<div class=cta><span class=label>{CTA_LABEL}</span><b>{CTA_HEADLINE}</b><p>{e(CTA_TEXT)}</p>'
            f'<a class="btn btn-primary" href="{e(buy_url(slug, content, utm))}">{CTA_BUTTON} {ARROW}</a>{promo()}'
            f'{alt_link(slug, content.replace("cta", "pm", 1) if content.startswith("cta") else "pm_" + content, utm)}{extra}</div>')


def hero_buy(slug, ghost_href, ghost_text, utm=None):
    return (f'<div class=acts><a class="btn btn-primary" href="{e(buy_url(slug, "hero", utm))}">{CTA_BUTTON} {ARROW}</a>'
            f'<a class="btn btn-ghost" href="{ghost_href}">{ghost_text}</a></div>'
            f'<p class=price-line><span><span class=num>{PRICE}</span> on Gumroad, instant download</span>{promo()}</p>')


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
    o = [head(p["q"], p["desc"], url, rel, ld_tag)]
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
             "".join(f'<li><a href="../{r}/">{e(BY_SLUG[r]["q"])}</a></li>' for r in p["related"]) +
             f'<li><a href="../../study-plan/">Build a day-by-day study plan to your interview date</a></li><li><a href="../../llm-cost-calculator/">Estimate LLM API cost per day and month</a></li>'
             f'<li><a href="../../mock-interview/">Run a timed mock interview round</a></li><li><a href="../../alternatives/">Compare AI engineer interview prep options</a></li>'
             f'<li><a href="../">All question deep dives</a></li><li><a href="../../">All 100 AI engineer interview questions with answers</a></li></ul>')
    o.append(f'<p class=muted>Based on question {src} in the full question bank.</p>')
    o.append('</div></main>' + sticky(p["slug"]))
    o.append(foot(rel))
    return "".join(o)


def index():
    url = f"{SITE}/questions/"
    rel = "../"
    title = "AI Engineer Interview Questions: Answer Frameworks and Sample Answers"
    desc = "Deep dives on the most-asked AI engineer interview questions: RAG, transformers, KV cache, LoRA, evals, agents and prompt injection, with sample answers."
    cnt = {k: sum(1 for p in PAGES if p["level"] == k) for k in LVL}
    o = [head(title, desc, url, rel)]
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

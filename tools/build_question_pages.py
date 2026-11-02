#!/usr/bin/env python3
"""Generate /questions/ SEO pages, the questions index, sitemap.xml and robots.txt.

Run from the repo root:  python3 tools/build_question_pages.py
To swap the call-to-action (for example to a free PDF), edit the CTA_* constants below and re-run.
"""
import html, json, os, re, sys
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from question_pages_data import PAGES

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://johnnnmai.github.io/ai-engineer-interview-questions"
SITE_NAME = "AI Engineer Interview Questions"
LASTMOD = "2026-11-01"

# ---- CTA: the single place to change the offer ----
CTA_URL = "https://sirjohnnymai.gumroad.com/l/ai-engineer-interview-playbook"
CTA_UTM = "utm_source=seo&utm_medium=qpage&utm_campaign={slug}"
CTA_HEADLINE = "Want the full method?"
CTA_TEXT = "The 0 to 1 AI Engineer Interview Playbook covers the answer frameworks, system-design walkthroughs and an 8-week plan."
CTA_BUTTON = "Get the playbook &rarr;"
# ----------------------------------------------------

e = html.escape
UTM_SCRIPT = re.search(r"<script>/\* UTM passthrough.*?</script>", open(os.path.join(ROOT, "index.html")).read(), re.S).group(0)
STYLE = re.search(r"<style>.*?</style>", open(os.path.join(ROOT, "index.html")).read(), re.S).group(0)
EXTRA_CSS = "<style>.crumb{font-size:.9rem}.crumb a{color:#cfd6e4}.q h3{margin:.2em 0}.related a,.w p a{color:#175cd3}ol.steps li,ul.mist li{margin:6px 0}</style>"
BY_SLUG = {p["slug"]: p for p in PAGES}
LVL = {"Entry": "E", "Mid": "M", "Senior": "S"}


def cta(slug):
    href = CTA_URL + ("&" if "?" in CTA_URL else "?") + CTA_UTM.format(slug=slug)
    return (f'<div class=cta><b>{CTA_HEADLINE}</b><p>{e(CTA_TEXT)}</p>'
            f'<a class=btn href="{e(href)}">{CTA_BUTTON}</a></div>')


def head(title, desc, url, extra=""):
    return (f'<!doctype html><html lang=en><head><meta charset=utf-8>'
            f'<meta name=viewport content="width=device-width,initial-scale=1">'
            f'<title>{e(title)}</title><meta name=description content="{e(desc)}">'
            f'<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}">'
            f'<meta property="og:type" content="article"><meta property="og:url" content="{url}">'
            f'<link rel=canonical href="{url}">{extra}{STYLE}{EXTRA_CSS}</head><body>')


def foot():
    return (f'<div class=w><footer>&copy; 2026 Valenx Press &middot; <a href="../../">All 100 AI engineer interview questions</a> &middot; '
            f'<a href="../">Question deep dives</a> &middot; Questions reflect common public interview patterns; no company affiliation.</footer></div>'
            f'{UTM_SCRIPT}</body></html>\n')


def page(p):
    url = f"{SITE}/questions/{p['slug']}/"
    faq = [{"@type": "Question", "name": p["q"],
            "acceptedAnswer": {"@type": "Answer", "text": " ".join(p["sample"])}}]
    faq += [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in p["followups"]]
    ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": faq}
    ld_tag = '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False).replace("</", "<\\/") + "</script>"
    src = ", ".join(f'<a href="../../#q{n}">#{n}</a>' for n in p["src"])
    o = [head(p["q"], p["desc"], url, ld_tag)]
    o.append(f'<div class=hero><div class=w><div class=crumb><a href="../../">{SITE_NAME}</a> &rsaquo; <a href="../">Questions</a></div>'
             f'<span class="lvl {LVL[p["level"]]}">{p["level"]}</span><h1>{e(p["q"])}</h1>'
             f'<p>How to answer it in an AI engineer interview: what is being tested, a step-by-step framework, a sample answer and the mistakes to avoid.</p></div></div><div class=w>')
    o.append(cta(p["slug"]))
    o.append(f'<h2>What the interviewer is testing</h2><p>{e(p["testing"])}</p>')
    o.append('<h2>Answer framework</h2><ol class=steps>' + "".join(f"<li>{e(s)}</li>" for s in p["steps"]) + "</ol>")
    o.append('<h2>Sample answer</h2><div class=q>' + "".join(f"<p class=ans>{e(s)}</p>" for s in p["sample"]) + "</div>")
    if p["followups"]:
        o.append('<h2>Likely follow-ups</h2>' + "".join(f'<div class=fu><b>{e(q)}</b> {e(a)}</div>' for q, a in p["followups"]))
    o.append('<h2>Common mistakes</h2><ul class=mist>' + "".join(f"<li>{e(m)}</li>" for m in p["mistakes"]) + "</ul>")
    o.append('<h2>Related questions</h2><ul class=related>' +
             "".join(f'<li><a href="../{r}/">{e(BY_SLUG[r]["q"])}</a></li>' for r in p["related"]) +
             f'<li><a href="../">All question deep dives</a></li><li><a href="../../">All 100 AI engineer interview questions with answers</a></li></ul>')
    o.append(f'<p class=muted>Based on question {src} in the full question bank.</p>')
    o.append(cta(p["slug"]) + "</div>")
    o.append(foot())
    return "".join(o)


def index():
    url = f"{SITE}/questions/"
    title = "AI Engineer Interview Questions: Answer Frameworks and Sample Answers"
    desc = "Deep dives on the most-asked AI engineer interview questions: RAG, transformers, KV cache, LoRA, evals, agents and prompt injection, with sample answers."
    o = [head(title, desc, url)]
    o.append(f'<div class=hero><div class=w><div class=crumb><a href="../">{SITE_NAME}</a> &rsaquo; Questions</div><h1>{e(title)}</h1>'
             '<p>One page per question: what the interviewer is testing, an answer framework, a sample answer, follow-ups and common mistakes.</p></div></div><div class=w>')
    for p in PAGES:
        o.append(f'<div class=q><span class="lvl {LVL[p["level"]]}">{p["level"]}</span><a href="{p["slug"]}/"><b>{e(p["q"])}</b></a><div class=ans>{e(p["desc"])}</div></div>')
    o.append('<p><b>Practice tool:</b> <a href="../answer-check/">Check your interview answer with the free Answer Self-Check</a> (score, missed concepts and tips).</p>')
    o.append('<p><a href="../">See all 100 AI engineer interview questions with answers</a></p>')
    o.append(cta("questions-index") + "</div>")
    o.append(foot().replace('href="../../"', 'href="../"').replace('<a href="../">Question deep dives</a> &middot; ', ''))
    return "".join(o)


def main():
    for p in PAGES:
        d = os.path.join(ROOT, "questions", p["slug"])
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "index.html"), "w").write(page(p))
    open(os.path.join(ROOT, "questions", "index.html"), "w").write(index())
    urls = [f"{SITE}/", f"{SITE}/questions/"] + [f"{SITE}/questions/{p['slug']}/" for p in PAGES] + [f"{SITE}/answer-check/"]
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

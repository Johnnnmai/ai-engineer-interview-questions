"""Build the root page (index.html): the 100-question bank in the Valenx layout.

Body content lives in tools/root_body.html. Every buy link on the page comes from CTA_URL in
build_question_pages.py (offer code included) plus a utm_content tag, so a price or offer change is one edit.
Run: python3 tools/build_root_page.py
"""
import html
import os
import re

import build_question_pages as B

ROOT = B.ROOT
URL = B.SITE + "/"
REL = "./"
SLUG = "root"
UTM = "utm_source=pages&utm_medium=qbank&utm_campaign=aie_qbank_20261101"
TITLE = "100 AI Engineer Interview Questions (2026) with Full Model Answers | Valenx Press"
DESC = ("100 AI engineer interview questions with full model answers: LLMs, prompting, RAG, agents and MCP, "
        "fine-tuning, evals, system design, production and coding. Updated Nov 2026.")
LEAD = ("LLM fundamentals, prompting, RAG, agents and MCP, fine-tuning, evaluation, system design, production and coding. "
        "Every question has a written answer, graded Entry, Mid or Senior, with the follow-ups interviewers tend to ask. Free, no sign-up.")
AMAZON = ('<p class=muted><small>The AI engineer playbook also comes in paperback and Kindle: '
          '<a href="https://valenx.org/books/aie">see it on Amazon</a>.</small></p>')

# Root-only pieces (question accordion, topic cards, contents, code) on the shared design tokens.
STYLE = """<style>
.root .grid{grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px;margin:var(--s3) 0}
.root .card{padding:16px 18px}.root .card b{display:block;margin-bottom:4px}
.root .card:hover{transform:none;box-shadow:none}
.toc{columns:2;column-gap:var(--s4);padding-left:1.2em}.toc li{margin:4px 0}
@media (max-width:560px){.toc{columns:1}}
.tools{margin:var(--s2) 0}
.tools button{font:500 var(--fs-small)/1 var(--font-sans);color:var(--ink);border:1px solid var(--line);background:var(--bg);border-radius:var(--r-pill);padding:10px 16px;cursor:pointer;margin:0 8px 8px 0}
.tools button:hover{border-color:var(--ink)}
details.q{border:1px solid var(--line);border-radius:var(--r-md);margin:10px 0;background:var(--bg)}
details.q summary{cursor:pointer;padding:16px 18px;font-weight:600;line-height:1.4;list-style:none;display:flex;gap:12px;align-items:flex-start}
details.q summary::-webkit-details-marker{display:none}
details.q summary::after{content:"+";margin-left:auto;padding-left:8px;color:var(--ink-3);font-family:var(--font-mono)}
details.q[open] summary::after{content:"\\2212"}
details.q summary .lvl{flex:none;min-width:84px;padding:5px 8px;margin-top:1px}
details.q .qa{padding:0 18px 16px}
details.q .qa p{margin:10px 0}
.root pre{background:#0b0b0c;color:#e7e7e4;padding:14px 16px;border-radius:var(--r-sm);overflow-x:auto;font:400 .82rem/1.55 var(--font-mono)}
.root pre code{background:none;padding:0;color:inherit}
.root .fu{border-top:1px solid var(--line);padding:10px 0 0;font-size:.95rem}
.root h2 small{font:500 var(--fs-label)/1 var(--font-mono);letter-spacing:.1em;text-transform:uppercase;color:var(--ink-3);display:block;margin-top:10px}
.root .cta .muted{margin:0}
@media (max-width:560px){details.q summary{display:block;position:relative;padding:14px 36px 14px 14px}details.q summary .lvl{min-width:0;margin:0 0 8px;display:flex;width:max-content}details.q summary::after{position:absolute;right:14px;top:14px}details.q .qa{padding:0 14px 14px}}
</style>"""


def buy(content, base=None):
    return html.escape(B.buy_url(SLUG, content, UTM, base), quote=True)


def main():
    body = open(os.path.join(ROOT, "tools", "root_body.html")).read()
    body = body.replace("<!--CTA:cta_mid-->", B.cta(SLUG, "cta_mid", UTM, AMAZON))
    body = body.replace("<!--CTA:cta_box-->", B.cta(SLUG, "cta_box", UTM, AMAZON))
    body = body.replace("{{BUY:faq}}", buy("faq_playbook"))
    body = body.replace("{{BUY:faq_pm}}", buy("faq_pm", B.PM_URL))
    assert "<!--CTA" not in body and "{{BUY" not in body
    lv = {k: len(re.findall(rf"class='lvl {v}'", body)) for k, v in B.LVL.items()}
    o = [B.head(TITLE, DESC, URL, REL, STYLE)]
    o.append('<header class="qhero idx" data-hero><div class=wrap>'
             '<div class="crumb label">2026 edition &middot; updated November 1, 2026</div>'
             '<h1>100 AI Engineer Interview Questions with full model answers</h1>'
             f'<p class=lead>{LEAD}</p>'
             + B.hero_buy(SLUG, "questions/", "Question deep dives", UTM) +
             '<div class=chips>' + "".join(f'<span class="lvl {B.LVL[k]}">{lv[k]} {k}</span>' for k in B.LVL) +
             '<span class=chip>Model answer for every question</span></div></div></header>')
    o.append('<main id=main class="body root"><div class=read>' + body + '</div></main>' + B.sticky(SLUG, UTM))
    o.append(B.foot(REL))
    out = "".join(o)
    links = re.findall(r'href="(https://(?:[^"]*gumroad\.com|valenx\.org/(?:kit|get/))[^"]*)"', out)
    assert links and all(l.startswith(("https://valenx.org/get/", "https://valenx.org/kit")) for l in links), links
    assert all(("offer_code=" in l) == bool(B.OFFER_CODE) for l in links), links
    assert any(l.startswith(B.CTA_URL.split("?")[0]) for l in links), links
    open(os.path.join(ROOT, "index.html"), "w").write(out)
    print("wrote index.html,", len(links), "buy links:", ", ".join(re.search(r"utm_content=(\w+)", l).group(1) for l in links))


if __name__ == "__main__":
    main()

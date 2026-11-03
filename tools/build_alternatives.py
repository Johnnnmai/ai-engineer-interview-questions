#!/usr/bin/env python3
"""Generate /alternatives/index.html: honest comparison of AI / ML engineer interview prep options.

Run from the repo root:  python3 tools/build_alternatives.py
Buy links reuse CTA_URL from tools/build_question_pages.py (offer_code lives there only).
Competitor facts come from each product's own page on Nov 1, 2026. Re-check before editing prices.
"""
import html, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_question_pages import (PROMO_HTML, PROMO_SHORT, CTA_URL, PROMO_ON, PROMO_TEXT, PRICE, SITE, ROOT, PRODUCT_NAME, PRODUCT_SHORT, CTA_LABEL, CTA_HEADLINE,
                                  CTA_TEXT, CTA_BUTTON, PM_URL, PM_LEAD, PM_LINK_TEXT, PM_POST, head, foot)

URL = f"{SITE}/alternatives/"
e = html.escape
ARROW = '<span class=dot aria-hidden=true>&rarr;</span>'
TITLE = "AI Engineer Interview Prep Alternatives (2026): ByteByteGo vs Educative vs Gumroad Guides vs Free"
DESC = ("Comparing ML and AI engineer interview prep: ByteByteGo ML System Design Interview, Educative Grokking the ML Interview, "
        "Gumroad guides and free question banks, by price, format and what each covers. Prices checked Nov 1, 2026.")


def buy(content, base=None):
    base = base or CTA_URL
    sep = "&" if "?" in base else "?"
    return base + sep + f"utm_source=compare&utm_medium=compare_page&utm_campaign=aie-alternatives&utm_content={content}"


def alt(content):
    return f'<p class=alt-buy>{PM_LEAD}<a href="{e(buy(content, PM_URL))}">{PM_LINK_TEXT}</a>{e(PM_POST)}</p>'


def cta_box(content):
    return (f'<div class=cta><span class=label>{CTA_LABEL}</span><b>{CTA_HEADLINE}</b><p>{e(CTA_TEXT)}</p>'
            f'<a class="btn btn-primary" href="{e(buy(content))}">{CTA_BUTTON} {ARROW}</a>{PROMO}{alt(content + "_pm")}</div>')


PROMO = f'<span class="badge promo">{PROMO_HTML}</span>' if PROMO_ON else ""
ROWS = [
    ("ByteByteGo, Machine Learning System Design Interview (book)", "About $31 on Amazon on Nov 1, 2026 (list $40)",
     "Book with a 7-step framework, 10 worked ML system design questions and 211 diagrams.", "Classic ML system design (ranking, recommendation, detection)"),
    ("Educative, Grokking the Machine Learning Interview", "Educative subscription",
     "Interactive course: 64 lessons, 66 quizzes and 6 mock interviews, per its course page.", "Structured course if you already pay for Educative"),
    ("ProdRescue, Senior and Staff AI System Design Interview OS", "$59 on Gumroad",
     "Guide focused on RAG, agents and LLM architecture for senior and staff loops. 30-day refund.", "Senior and staff candidates"),
    ("LLMs Research, LLM Flashcards", "$19.99 on Gumroad",
     "376 cards as PDF and Anki, free samples on GitHub.", "Spaced repetition on LLM internals"),
    ("Free: this site's 100 questions", "$0",
     "100 AI engineer questions with answer frameworks, 50 deep dives, a free self-check and a timed mock round.", "Checking your level and practicing out loud"),
    ("The 0&rarr;1 AI Engineer Interview Playbook", PRICE + " on Gumroad",
     "1 PDF, 370+ pages, 20 chapters, 5 frameworks (RAG, agents, LLM system design, evals, behavioral), 8-week plan.", "A full method for RAG, agents and evals loops"),
]
FAQ = [
    ("What is the best alternative to the ByteByteGo ML System Design Interview book?",
     "If your loop is classic ML system design, the book is a strong pick. If your loop is LLM-heavy (RAG, agents, evals), look for material built around those topics, such as the free 100-question bank here or the 0 to 1 AI Engineer Interview Playbook."),
    ("Is Grokking the Machine Learning Interview worth it?",
     "If you already have an Educative subscription, it is a structured course you get as part of it. If you would buy the subscription only for this course, compare the cost with a one-time guide."),
    ("What is the difference between AI engineer and ML engineer interview prep?",
     "ML engineer loops lean on training, features and classic system design. AI engineer loops in 2026 lean on LLM applications: retrieval, agents, tool calling, evals, cost and latency."),
    ("Are free AI engineer interview questions enough?",
     "For screens, often yes, if you answer out loud and get feedback. Use the free bank, the mock round timer and the self-check first, then buy a guide only for the gaps you find."),
    ("Do any of these replace mock interviews with a person?",
     "No. They are reading and self-practice. A mock with a peer or mentor still catches things a page cannot."),
    ("Are these prices current?",
     "Prices were read from each product's own page on Nov 1, 2026. Sellers change prices and run sales, so check before you buy."),
]
CSS = ("<style>.cmp{width:100%;border-collapse:collapse;font-size:15px;min-width:560px}.cmp th,.cmp td{text-align:left;vertical-align:top;"
       "padding:10px 12px;border-bottom:1px solid var(--line,#e5e5e5)}.cmp th{font-weight:600}.tw{overflow-x:auto}</style>")


def build():
    ldf = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}
    h = head(TITLE, DESC, URL, "../", '<script type="application/ld+json">' + json.dumps(ldf) + "</script>" + CSS)
    promo = PROMO
    table = "<div class=tw><table class=cmp><tr><th>Option</th><th>Price</th><th>Format and size</th><th>Best for</th></tr>" + "".join(
        f"<tr><td>{a}</td><td>{e(b)}</td><td>{c.replace(chr(39), '&rsquo;')}</td><td>{e(d)}</td></tr>" for a, b, c, d in ROWS) + "</table></div>"
    o = [h,
         '<header class=qhero data-hero><div class=wrap><div class="crumb label"><a href="../">AI Engineer Interview Questions</a> / Alternatives</div>'
         '<span class=badge>Compared Nov 1, 2026</span><h1>AI engineer interview prep alternatives: ByteByteGo vs Educative vs Gumroad guides vs free</h1>'
         '<p class=lead>Six ways to prep for ML and AI engineer loops, side by side: price, format and what each is best at. Prices are from each seller&rsquo;s own page.</p>'
         f'<div class=acts><a class="btn btn-primary" href="{e(buy("hero"))}">{CTA_BUTTON} {ARROW}</a><a class="btn btn-ghost" href="../">Start with 100 free questions</a></div>'
         f'<p class=price-line><span><span class=num>{PRICE}</span> on Gumroad, instant download</span>{promo}</p></div></header>',
         '<main id=main class=body><div class=read>',
         '<h2>The short version</h2><ul>'
         '<li><b>Classic ML system design:</b> the ByteByteGo book.</li>'
         '<li><b>A guided course:</b> Educative, if you already subscribe.</li>'
         '<li><b>Senior or staff LLM architecture:</b> ProdRescue at $59.</li>'
         '<li><b>Flashcards for LLM internals:</b> LLM Flashcards at $19.99.</li>'
         f'<li><b>RAG, agents and evals on a budget:</b> the free bank here, then the 0 to 1 AI Engineer Interview Playbook at {PRICE}.</li></ul>',
         '<h2>Side by side</h2>', table,
         '<p class=muted>From amazon.com, educative.io and gumroad.com product pages on Nov 1, 2026. Valenx Press is not affiliated with these sellers.</p>',
         '<h2>More comparisons</h2><ul>'
         '<li><a href="exponent-alternatives/">Exponent (now Aced) alternatives for AI engineer interviews</a>: plans, AI Engineering track and cost over a prep window</li>'
         '<li><a href="hello-interview-alternatives/">Hello Interview alternatives for AI engineer interviews</a>: plans, Guided Practice and classic ML vs LLM system design</li></ul>',
         '<h2>What the others do better</h2><p>The ByteByteGo book has 211 diagrams and goes deep on classic ranking and recommendation designs. Educative is interactive, with quizzes. '
         'ProdRescue is written for senior and staff loops. If one of those is your exact gap, buy that one.</p>',
         '<h2>Where the low-cost route wins</h2><ol class=steps>'
         '<li><b>Check your level for free first.</b> Read the <a href="../questions/">50 deep dives</a> and the <a href="../">full 100-question bank</a>.</li>'
         '<li><b>Practice out loud.</b> The free <a href="../mock-interview/">mock round timer</a> draws random questions and the <a href="../answer-check/">self-check</a> scores what you said.</li>'
         f'<li><b>Add the method for {PRICE}.</b> <a href="{e(buy("steps_playbook"))}">{PRODUCT_NAME}</a>: frameworks for RAG, agents, LLM system design and evals, plus an 8-week plan.</li></ol>',
         cta_box("cta_box"),
         '<h2>Which one should you pick?</h2><ul>'
         '<li><b>Loop in a week, LLM-heavy role:</b> free questions, the mock round, then the Playbook.</li>'
         '<li><b>Classic MLE loop at a large company:</b> the ByteByteGo book.</li>'
         '<li><b>Senior or staff:</b> ProdRescue, plus the free bank to warm up.</li>'
         '<li><b>No budget:</b> the free bank, the mock round timer and the self-check.</li></ul>',
         '<h2>FAQ</h2>' + "".join(f'<div class=fu><b>{e(q)}</b> {e(a)}</div>' for q, a in FAQ),
         cta_box("cta_end"),
         '</div></main>',
         f'<div class=sticky-cta role=complementary aria-label="Buy the playbook" aria-hidden=true><span class=t><b><span class=full>{PRODUCT_NAME}</span><span class=short>{PRODUCT_SHORT}</span></b>'
         + ('<span class="long promo"> &middot; 40% off until Nov 3</span><span class="short promo"> &middot; 40% off</span>' if PROMO_ON else '') +
         f'</span><a class=btn href="{e(buy("sticky_bar"))}">Get it &rarr;</a></div>',
         foot("../")]
    os.makedirs(os.path.join(ROOT, "alternatives"), exist_ok=True)
    out = "".join(o)
    open(os.path.join(ROOT, "alternatives", "index.html"), "w").write(out)
    print("wrote alternatives/index.html", len(out))


if __name__ == "__main__":
    build()

#!/usr/bin/env python3
"""Generate two free tool pages:
  /llm-cost-calculator/  LLM API cost per day and month from official list prices (tools/llm_prices.py)
  /study-plan/           day-by-day plan from today to the interview date, linking only pages that exist

Run from the repo root:  python3 tools/build_tools_pages.py
Paid links use OFFER_Q from tools/build_question_pages.py, so any offer code is controlled by the single OFFER_CODE constant there.
Static only: no API calls, no tracking beyond utm parameters on Gumroad links.
"""
import html, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_question_pages import (PROMO_HTML, PROMO_SHORT, SITE, ROOT, OFFER_Q, PROMO_ON, PROMO_TEXT, PROMO_STICKY_LONG, PROMO_STICKY_SHORT, PRICE, PRODUCT_NAME, PRODUCT_SHORT, PM_PRICE,
                                  PAGES, BY_SLUG, head, foot)
import build_answer_check as A
import llm_prices as LP

e = html.escape
ARROW = '<span class=dot aria-hidden=true>&rarr;</span>'
GR = "https://sirjohnnymai.gumroad.com/l/"
IB_FREE = "https://sirjohnnymai.gumroad.com/l/ib-top-30-questions"
DS_PRICE = "$19.99"  # list price on the live Gumroad product page, Nov 1 2026
PMPB_PRICE = "$19.99"  # list price on the live Gumroad product page, Nov 1 2026


def paid(product, campaign, content):
    """Gumroad link with the shared offer query (empty while OFFER_CODE is empty) plus site utm."""
    base = GR + product + OFFER_Q
    return base + ("&" if "?" in base else "?") + f"utm_source=site&utm_medium=tool&utm_campaign={campaign}&utm_content={content}"


def ld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False).replace("</", "<\\/") + "</script>"


def faq_block(items):
    vis = "".join(f'<div class=fu><b>{e(q)}</b> {e(a)}</div>' for q, a in items)
    data = {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items]}
    return vis, ld(data)


def promo():
    return f'<span class="badge promo">{PROMO_HTML}</span>' if PROMO_ON else ""


def sticky(href, label="Buy the playbook"):
    deal = f'<span class="long promo"> &middot; {PROMO_STICKY_LONG}</span>' if PROMO_ON else f'<span class=long> &middot; {PRICE}</span>'
    short = f'<span class="short promo"> &middot; {PROMO_STICKY_SHORT}</span>' if PROMO_ON else f'<span class=short> &middot; {PRICE}</span>'
    return (f'<div class=sticky-cta role=complementary aria-label="{label}" aria-hidden=true>'
            f'<span class=t><b><span class=full>{PRODUCT_NAME}</span><span class=short>{PRODUCT_SHORT}</span></b>{deal}{short}</span>'
            f'<a class=btn href="{e(href)}">Get it &rarr;</a></div>')


def pm_alt(href, label="PM direction bundle"):
    return (f'<p class=alt-buy>Interviewing for PM or TPM instead? <a href="{e(href)}">See the {label}</a>, {PM_PRICE} on Gumroad: '
            f'PM, TPM and PGM interview handbook, resume system and 1:1 cheat sheet. PM content, not AI engineer prep.</p>')


TOOL_CSS = """<style>
.tool{background:var(--bg-soft);border:1px solid var(--line);border-radius:var(--r-lg);padding:var(--s4);margin:0 0 var(--s4)}
.tool .grid2{display:grid;grid-template-columns:1fr 1fr;gap:var(--s3)}@media (max-width:640px){.tool .grid2{grid-template-columns:1fr}.tool{padding:var(--s3)}}
.tool label.f{display:block;font-weight:600;font-size:var(--fs-small);margin:0 0 6px}
.tool input[type=number],.tool input[type=date],.tool select{width:100%;font:500 1rem var(--font-sans);color:var(--ink);background:var(--surface);border:1px solid var(--line);border-radius:var(--r-sm);padding:12px 14px;min-height:48px}
.tool input:focus-visible,.tool select:focus-visible,.tool button:focus-visible{outline:2px solid var(--pop);outline-offset:2px}
.tool .full{grid-column:1/-1}.tool .hint{font-size:var(--fs-small);color:var(--ink-2);margin:6px 0 0}
.tog{display:flex;align-items:center;gap:var(--s1);font-weight:600;cursor:pointer}.tog input{width:20px;height:20px;accent-color:var(--ink)}
.out{background:var(--ink);color:var(--bg);border-radius:var(--r-md);padding:var(--s4);margin:var(--s3) 0 0}
.body .out p,.body .out li{color:var(--bg)}.out .label{opacity:.7}
.out .nums{display:grid;grid-template-columns:repeat(3,1fr);gap:var(--s3);margin:var(--s2) 0}@media (max-width:640px){.out .nums{grid-template-columns:1fr}}
.out .n{font-family:var(--font-serif);font-size:clamp(2.2rem,6vw,3.6rem);line-height:1;font-variant-numeric:tabular-nums;display:block}
.out .k{font:500 var(--fs-label) var(--font-mono);letter-spacing:var(--track-label);text-transform:uppercase;opacity:.7}
.out .brk{font-size:var(--fs-small);opacity:.85;margin:0}
.ctab{width:100%;border-collapse:collapse;font-size:var(--fs-small);font-variant-numeric:tabular-nums}
.ctab th,.ctab td{text-align:left;padding:8px 10px;border-bottom:1px solid var(--line)}.ctab td.r,.ctab th.r{text-align:right}
.ctab tr.cur td{background:#fff6d6;font-weight:600}.tscroll{overflow-x:auto}
.plan{list-style:none;padding:0;margin:var(--s3) 0 0;counter-reset:none}
.plan>li{background:var(--surface);border:1px solid var(--line);border-radius:var(--r-md);padding:var(--s3);margin:0 0 var(--s2);break-inside:avoid}
.plan .dh{display:flex;align-items:baseline;gap:var(--s2);flex-wrap:wrap;margin:0 0 var(--s1)}
.plan .dh b{font-size:1.1rem}.plan .dh .label{color:var(--ink-2)}
.plan ul{margin:var(--s1) 0;padding-left:1.2em}.plan li li{margin:4px 0}
.plan .sc{margin:var(--s1) 0 0;font-weight:600}.plan .done{display:flex;align-items:center;gap:6px;margin-left:auto;font-size:var(--fs-small);color:var(--ink-2)}
.plan .done input{width:18px;height:18px;accent-color:var(--ink)}
.plan .pc{border-top:1px dashed var(--line);margin-top:var(--s2);padding-top:var(--s2);font-size:var(--fs-small)}
.plan .pc a.btn{margin:6px 0}
.plan>li.last{border-color:var(--ink)}
.msg{background:#fff6d6;border:1px solid var(--pop);border-radius:var(--r-md);padding:var(--s2) var(--s3);margin:var(--s3) 0 0}
.tool button.btn{cursor:pointer;font:inherit}
@media print{.qhero::before,.nav,.skip,.sticky-cta,footer.site,.qhero .acts,.qhero .price-line,.noprint,.cta,.tool .grid2,.tool .hint{display:none}
body{background:#fff}.tool{border:0;padding:0;background:#fff}.plan>li{border:1px solid #999}.plan .pc{display:none}
.qhero{padding:0}.qhero h1{font-size:24pt}.plan a{color:#000;text-decoration:none}.plan a[href^="http"]::after{content:""}}
</style>"""


# ---------------------------------------------------------------- calculator
CALC_URL = f"{SITE}/llm-cost-calculator/"
C_CAMP = "line22_20261101"
C_TITLE = "LLM API Cost Calculator (Nov 2026): GPT, Claude, Gemini, DeepSeek, Mistral"
C_DESC = ("Estimate LLM API cost per request, per day and per month for 30 models from OpenAI, Anthropic, Google, DeepSeek and Mistral, "
          "with prompt caching. Official list prices as of Nov 1, 2026, each linked to the provider page.")

COST_LINKS = ["how-to-reduce-llm-inference-cost", "how-to-cache-llm-responses", "design-an-llm-gateway"]

C_FAQ = [
    ("Where do the prices come from?",
     "Each price was read on Nov 1, 2026 from the provider's own pricing page, linked in the sources table on this page. Prices change often, so check the provider page before you commit to a budget."),
    ("How is the monthly cost calculated?",
     "Cost per request is input tokens times the input price plus output tokens times the output price, divided by one million. With caching on, the cached share of input tokens is billed at the cached-input price. Daily cost is cost per request times requests per day, and monthly cost is daily cost times 30."),
    ("What does the cache-hit toggle do?",
     "It bills a share of your input tokens at the provider's published cached-input or cache-hit price. Set the share to how much of each prompt is a repeated prefix, such as a long system prompt or shared documents. Cache-write premiums and cache storage fees are not included."),
    ("Does it include batch discounts or off-peak rates?",
     "No. The calculator uses standard on-demand rates. Batch APIs and DeepSeek off-peak hours are cheaper, and the notes under each source say by how much where the page states it."),
    ("Why are long prompts more expensive on some models?",
     "Some providers charge a higher rate once a single request passes a context threshold, for example 272K input tokens on several OpenAI models and 200K on some Gemini models. The calculator switches to those rates automatically when your input tokens pass the threshold."),
    ("How do I use this in an interview?",
     "Show the unit economics first: tokens per request, price per million tokens, requests per day. Then name the levers that change the number, such as a smaller model for easy requests, prompt caching and shorter outputs, and say what each one risks for quality."),
]


def calc_page():
    rel = "../"
    models = LP.as_json()
    vis_faq, faq_ld = faq_block(C_FAQ)
    app = {"@context": "https://schema.org", "@type": "WebApplication", "name": "LLM API Cost Calculator", "url": CALC_URL,
           "applicationCategory": "BusinessApplication", "operatingSystem": "Any", "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
           "publisher": {"@type": "Organization", "name": "Valenx Press"}}
    o = [head(C_TITLE, C_DESC, CALC_URL, rel, ld(app) + faq_ld + TOOL_CSS).replace('content="article"', 'content="website"', 1)]
    o.append('<header class=qhero data-hero><div class=wrap><div class="crumb label"><a href="../">AI Engineer Interview Questions</a> / Tools / LLM cost calculator</div>'
             '<span class=badge>Free tool</span><h1>LLM API cost calculator</h1>'
             f'<p class=lead>What will this feature cost per day and per month? Pick a model, enter tokens and traffic, turn on prompt caching. '
             f'{len(models)} models from OpenAI, Anthropic, Google, DeepSeek and Mistral, list prices as of Nov 1, 2026, each linked to the provider page.</p>'
             f'<div class=acts><a class="btn btn-primary" href="#calc">Estimate my cost {ARROW}</a>'
             f'<a class="btn btn-ghost" href="{e(paid("ai-engineer-interview-playbook", C_CAMP, "hero"))}">Get the AI engineer playbook</a></div>'
             f'<p class=price-line><span><span class=num>{PRICE}</span> on Gumroad, instant download</span>{promo()}</p></div></header>')
    o.append('<main id=main class=body><div class=read>')
    # tool
    opts, cur = [], None
    for m in models:
        if m["p"] != cur:
            if cur is not None:
                opts.append("</optgroup>")
            opts.append(f'<optgroup label="{e(m["p"])}">')
            cur = m["p"]
        sel = " selected" if m["id"] == "gpt-6.1-terra" else ""
        opts.append(f'<option value="{m["id"]}"{sel}>{e(m["name"])}</option>')
    opts.append("</optgroup>")
    o.append('<section id=calc class=tool aria-labelledby=calc-h><h2 id=calc-h style="margin-top:0">Your workload</h2><div class=grid2>'
             f'<div class=full><label class=f for=m>Model</label><select id=m>{"".join(opts)}</select><p class=hint id=mnote></p></div>'
             '<div><label class=f for=tin>Input tokens per request</label><input id=tin type=number min=0 step=1 value=2000 inputmode=numeric>'
             '<p class=hint>System prompt, history, retrieved context and the user message.</p></div>'
             '<div><label class=f for=tout>Output tokens per request</label><input id=tout type=number min=0 step=1 value=500 inputmode=numeric>'
             '<p class=hint>Reasoning tokens count as output on most providers.</p></div>'
             '<div><label class=f for=rpd>Requests per day</label><input id=rpd type=number min=0 step=1 value=10000 inputmode=numeric></div>'
             '<div><label class=tog for=cache><input id=cache type=checkbox> Cache hits on repeated input</label>'
             '<label class=f for=hit style="margin-top:10px">Share of input tokens served from cache (%)</label>'
             '<input id=hit type=number min=0 max=100 step=1 value=50 disabled inputmode=numeric></div></div>'
             '<div class=out aria-live=polite><span class=label id=oname>Estimate</span><div class=nums>'
             '<div><span class=k>Per request</span><span class=n id=oreq>$0</span></div>'
             '<div><span class=k>Per day</span><span class=n id=oday>$0</span></div>'
             '<div><span class=k>Per month (30 days)</span><span class=n id=omon>$0</span></div></div>'
             '<p class=brk id=obrk></p></div>'
             f'<p class=hint>Prices as of {LP.AS_OF}, check provider page before you budget. Standard on-demand rates in USD. Taxes, batch discounts, cache writes and tool fees are not included.</p></section>')
    o.append('<h2>Same workload on every model</h2><p>Sorted from cheapest to most expensive per month, with your current settings. Caching applies only where the provider publishes a cached-input price.</p>'
             '<div class=tscroll><table class=ctab id=cmp><thead><tr><th>#</th><th>Model</th><th>Provider</th><th class=r>Per day</th><th class=r>Per month</th></tr></thead><tbody></tbody></table></div>')
    o.append('<h2>How the math works</h2><ol class=steps>'
             '<li>Uncached input cost = input tokens &times; (1 &minus; cache share) &times; input price &divide; 1,000,000.</li>'
             '<li>Cached input cost = input tokens &times; cache share &times; cached-input price &divide; 1,000,000.</li>'
             '<li>Output cost = output tokens &times; output price &divide; 1,000,000.</li>'
             '<li>Per day = cost per request &times; requests per day. Per month = per day &times; 30.</li></ol>'
             '<p>Worked example: GPT-6.1 Terra at $1.00 input and $5.00 output per 1M tokens, 2,000 input and 500 output tokens, 10,000 requests a day, no caching. '
             'Per request is 2,000 &times; 1.00 &divide; 1M + 500 &times; 5.00 &divide; 1M = $0.0045. Per day is $45.00 and per month is $1,350.00.</p>')
    o.append(cta_box_aie("cta_mid", C_CAMP))
    # interview section
    lis = "".join(f'<li><a href="../questions/{s}/">{e(BY_SLUG[s]["q"])}</a></li>' for s in COST_LINKS)
    o.append('<h2>How to explain cost trade-offs in an interview</h2>'
             '<p>Cost questions show up in LLM system design rounds as soon as you propose a model. Interviewers want to see that you can turn a design into a number and then defend the levers you would pull.</p>'
             '<ol class=steps><li>State the unit economics. Tokens in, tokens out, price per million, requests per day. Say the monthly number out loud.</li>'
             '<li>Find the biggest term. Long system prompts and retrieved context usually dominate input; long answers or reasoning dominate output.</li>'
             '<li>Pull the cheapest lever first. Prompt caching for repeated prefixes, shorter retrieved context, capped output length.</li>'
             '<li>Route by difficulty. Send easy requests to a small model and escalate hard ones, and say how you would measure that quality holds.</li>'
             '<li>Name the risk. Every saving trades something: freshness for caching, accuracy for a smaller model, latency for batching.</li></ol>'
             f'<p>Practice the three questions where this comes up most:</p><ul class=related>{lis}</ul>'
             '<p>Then <a href="../answer-check/?track=aie&amp;q=how-to-reduce-llm-inference-cost">score your answer to the cost question in the free self-check</a>, '
             'or <a href="../study-plan/">build a day-by-day study plan to your interview date</a>.</p>')
    # sources
    rows = []
    for p, url in LP.SOURCES.items():
        n = sum(1 for m in models if m["p"] == p)
        rows.append(f'<tr><td><b>{e(p)}</b></td><td class=r>{n}</td><td><a href="{url}" rel=nofollow>{e(url.replace("https://", ""))}</a><br><span class=muted>{e(LP.NOTES[p])}</span></td></tr>')
    o.append(f'<h2>Prices and sources</h2><p>Prices as of {LP.AS_OF}, check provider page. Every rate on this page was read from these official pages on that date. '
             'If a page could not be read, its models are left out rather than estimated.</p>'
             f'<div class=tscroll><table class=ctab><thead><tr><th>Provider</th><th class=r>Models</th><th>Official pricing page and notes</th></tr></thead><tbody>{"".join(rows)}</tbody></table></div>')
    o.append('<h2>Questions</h2>' + vis_faq)
    o.append(cta_box_aie("cta_end", C_CAMP))
    o.append('<p class=muted><a href="../answer-check/">Free answer self-check</a> &middot; <a href="../study-plan/">Study plan</a> &middot; '
             '<a href="../mock-interview/">Mock round</a> &middot; <a href="../questions/">Question deep dives</a></p>')
    o.append('</div></main>' + sticky(paid("ai-engineer-interview-playbook", C_CAMP, "sticky_bar")))
    o.append(CALC_JS.replace("__MODELS__", json.dumps(models).replace("</", "<\\/")))
    o.append(foot(rel))
    return "".join(o)


def cta_box_aie(content, camp):
    return (f'<div class=cta><span class=label>The Playbook</span><b>Want the full method?</b>'
            f'<p>The 0 to 1 AI Engineer Interview Playbook covers the answer frameworks, LLM system design walkthroughs including cost and latency, and an 8-week plan. {PRICE} on Gumroad.</p>'
            f'<a class="btn btn-primary" href="{e(paid("ai-engineer-interview-playbook", camp, content))}">Get the AI engineer playbook {ARROW}</a>{promo()}'
            f'{pm_alt(paid("xzptir", camp, content + "_pm"))}</div>')


CALC_JS = r"""<script>
(function(){
var M=__MODELS__,byId={};M.forEach(function(m){byId[m.id]=m});
function $(i){return document.getElementById(i)}
function num(i){var v=parseFloat($(i).value);return isFinite(v)&&v>0?v:0}
function usd(x){if(x===0)return "$0";if(x>=1)return "$"+x.toLocaleString("en-US",{minimumFractionDigits:2,maximumFractionDigits:2});
 if(x>=0.01)return "$"+x.toFixed(4).replace(/0+$/,"").replace(/\.$/,"");return "$"+x.toPrecision(3).replace(/0+$/,"").replace(/\.$/,"")}
function rates(m,tin){if(m.long&&tin>m.long.over)return {i:m.long.in,o:m.long.out,c:m.long.cached,lg:true};return {i:m.in,o:m.out,c:m.cached,lg:false}}
function cost(m,tin,tout,rpd,share){var r=rates(m,tin),sh=(r.c===null||r.c===undefined)?0:share;
 var ui=tin*(1-sh)*r.i/1e6,ci=tin*sh*(r.c||0)/1e6,oc=tout*r.o/1e6,req=ui+ci+oc;
 return {r:r,sh:sh,ui:ui,ci:ci,oc:oc,req:req,day:req*rpd,mon:req*rpd*30}}
window.llmCost=cost;window.llmModels=byId;
function run(){var m=byId[$("m").value],tin=num("tin"),tout=num("tout"),rpd=num("rpd"),on=$("cache").checked;
 $("hit").disabled=on?false:true;var share=on?Math.min(100,num("hit"))/100:0;
 var c=cost(m,tin,tout,rpd,share);
 $("oname").textContent=m.name+" \u00b7 "+m.p;$("oreq").textContent=c.req>0&&c.req<1000?"$"+(c.req<1e-6?"0.000001":c.req.toPrecision(4).replace(/(\.\d*?)0+$/,"$1").replace(/\.$/,"")):usd(c.req);$("oday").textContent=usd(c.day);$("omon").textContent=usd(c.mon);
 var b="Rates per 1M tokens: $"+c.r.i+" input, $"+c.r.o+" output"+(c.r.c===null?"":", $"+c.r.c+" cached input")+(c.r.lg?" (long-context rate, input over "+m.long.over.toLocaleString("en-US")+" tokens)":"")+
  ". Per day: "+usd(c.ui*rpd)+" uncached input, "+usd(c.ci*rpd)+" cached input, "+usd(c.oc*rpd)+" output.";
 if(on&&m.cached===null)b+=" This provider publishes no cached price for this model, so caching is ignored.";
 $("obrk").textContent=b;$("mnote").textContent=m.note||"";
 var rows=M.map(function(x){return {m:x,c:cost(x,tin,tout,rpd,share)}}).sort(function(a,b){return a.c.mon-b.c.mon});
 var tb=document.querySelector("#cmp tbody");tb.textContent="";
 rows.forEach(function(r,i){var tr=document.createElement("tr");if(r.m.id===m.id)tr.className="cur";
  [String(i+1),r.m.name,r.m.p,usd(r.c.day),usd(r.c.mon)].forEach(function(t,j){var td=document.createElement("td");td.textContent=t;if(j>2)td.className="r";tr.appendChild(td)});tb.appendChild(tr)});
 try{var q=new URLSearchParams({m:m.id,in:tin,out:tout,rpd:rpd});if(on)q.set("hit",Math.round(share*100));history.replaceState(null,"","?"+q.toString()+location.hash)}catch(e){}}
function init(){var p=new URLSearchParams(location.search);
 if(p.get("m")&&byId[p.get("m")])$("m").value=p.get("m");
 [["in","tin"],["out","tout"],["rpd","rpd"]].forEach(function(k){var v=p.get(k[0]);if(v&&isFinite(parseFloat(v)))$(k[1]).value=v});
 if(p.get("hit")){$("cache").checked=true;$("hit").value=p.get("hit")}
 ["m","tin","tout","rpd","cache","hit"].forEach(function(i){$(i).addEventListener("input",run);$(i).addEventListener("change",run)});run()}
if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",init);else init();
})();
</script>"""


# ---------------------------------------------------------------- study plan
PLAN_URL = f"{SITE}/study-plan/"
P_CAMP = "line23_20261101"
P_TITLE = "AI Engineer Interview Study Plan: Day-by-Day Prep to Your Interview Date"
P_DESC = ("Enter your interview date and track to get a free day-by-day prep plan: which question to study each day, "
          "a self-check link to score your answer, and a mock round before the day. AI engineer, data science, PM and investment banking.")

DS_SLUGS = ["how-to-ab-test-an-ai-feature", "how-do-you-evaluate-an-llm", "what-is-benchmark-contamination", "embedding-model-vs-generative-model",
            "explain-the-transformer-architecture", "what-is-tokenization-in-llms", "temperature-vs-top-p", "rag-vs-fine-tuning",
            "how-to-build-a-fine-tuning-dataset", "what-is-catastrophic-forgetting", "what-is-model-distillation", "what-are-scaling-laws",
            "how-to-choose-an-embedding-model", "how-to-make-llm-as-a-judge-reliable", "why-do-llms-hallucinate", "what-is-hybrid-search"]
DS_TASKS = ["SQL: solve 3 problems with joins, GROUP BY and window functions, timed at 15 minutes each.",
            "Statistics: explain a p-value, statistical power and a confidence interval out loud, one minute each.",
            "Product metrics: pick one app you use and define a north star metric and two guardrail metrics.",
            "Experiment design: size one A/B test. State the baseline, minimum detectable effect, sample size and duration.",
            "Machine learning: explain bias versus variance and when you would use regularization, with one example.",
            "Metric case: a key metric dropped 10% week over week. Walk through how you would diagnose it.",
            "Behavioral: write two STAR stories, one about influencing a decision with data and one about a mistake."]
PM_SLUGS = ["what-is-rag", "what-is-an-ai-agent", "workflows-vs-agents", "rag-vs-fine-tuning", "how-to-ab-test-an-ai-feature",
            "how-do-you-evaluate-an-llm", "why-do-llms-hallucinate", "what-are-llm-guardrails", "what-is-prompt-injection",
            "how-to-reduce-llm-inference-cost", "how-to-reduce-llm-latency", "design-a-customer-support-chatbot", "what-is-a-context-window",
            "reasoning-models-vs-chat-models", "what-is-red-teaming-in-ai"]
PM_TASKS = ["Product sense: design a product for one user group out loud in 30 minutes. Users, pain points, solutions, prioritization.",
            "Execution: choose success metrics and guardrails for a feature launch, then say what you would do if the main metric fell.",
            "Estimation: size one market out loud in 10 minutes and state your assumptions.",
            "Behavioral: write two STAR stories, one about a conflict and one about a project that failed.",
            "Strategy: structure an answer to whether a company should enter a new market. Structure only, 10 minutes.",
            "AI product: write a one-page spec for an LLM feature, including how you would evaluate quality and handle failures."]

P_FAQ = [
    ("How does the plan decide what to study each day?",
     "It counts the days from today to your interview, keeps the last two days for a mock round and a light warm-up, and spreads the track's questions over the remaining days, Entry level first, then Mid, then Senior. With fewer days it shows fewer questions per day, up to four, starting with the most common ones."),
    ("What happens if my interview is more than 60 days away?",
     "The plan covers the final 60 days and tells you the date to start. Before then, one question every few days and a weekly mock round is enough to keep the material fresh."),
    ("What if my interview is today or the date has passed?",
     "If it is today you get a short warm-up: three core questions to re-read, one timed mock round and a self-check. If the date has passed, the page says so and asks for your next date instead of building a plan."),
    ("Is there a dedicated data science or PM question bank?",
     "Not yet. The data science and PM tracks use the free AI engineer pages that overlap with those interviews, such as A/B testing, evaluation and LLM product design, plus daily practice tasks without links for SQL, statistics, product sense and behavioral rounds."),
    ("What is the self-check link at the end of each day?",
     "It opens the free answer self-check with that day's question loaded. Answer out loud, paste or type what you said, and get a score against the key points in about 30 seconds."),
    ("Can I print the plan?",
     "Yes. Use the print button. The printed version keeps the days, questions and checkboxes and drops the form and buy buttons."),
]


def plan_data():
    lv = {"Entry": 0, "Mid": 1, "Senior": 2}
    aie = sorted(PAGES, key=lambda p: lv[p["level"]])
    item = lambda p: {"s": p["slug"], "q": p["q"], "l": p["level"], "u": f"../questions/{p['slug']}/", "c": f"../answer-check/?track=aie&q={p['slug']}"}
    ib = A.data()["tracks"]["ib"]["questions"]
    for s in DS_SLUGS + PM_SLUGS:
        assert s in BY_SLUG, s
    ctas = {
        "aie": {"head": "Want the full method before the day?", "text": f"The 0 to 1 AI Engineer Interview Playbook: answer frameworks, system design walkthroughs and an 8-week plan. {PRICE} on Gumroad.",
                "btn": "Get the AI engineer playbook", "url": paid("ai-engineer-interview-playbook", P_CAMP, "aie_last3"), "promo": PROMO_ON,
                "alt": {"lead": "Interviewing for PM or TPM instead? ", "text": "See the PM direction bundle", "post": f", {PM_PRICE} on Gumroad. PM content, not AI engineer prep.",
                        "url": paid("xzptir", P_CAMP, "aie_last3_pm")}},
        "ds": {"head": "Want the full data science method?", "text": f"The 0 to 1 Data Science Interview Playbook: SQL, statistics, machine learning, product sense and coding. {DS_PRICE} on Gumroad.",
               "btn": "Get the data science playbook", "url": paid("ds-interview-playbook", P_CAMP, "ds_last3"), "promo": PROMO_ON, "alt": None},
        "pm": {"head": "Want the full PM package?", "text": f"The North America Interview Full Package: PM, TPM and PGM interview handbook, resume system, 1:1 cheat sheet and a PM playbook. {PM_PRICE} on Gumroad.",
               "btn": "Get the PM package", "url": paid("xzptir", P_CAMP, "pm_last3"), "promo": PROMO_ON,
               "alt": {"lead": "Just want the PM playbook? ", "text": "See the 0 to 1 PM Interview Playbook", "post": f", {PMPB_PRICE} on Gumroad.",
                       "url": paid("pm-interview-playbook", P_CAMP, "pm_last3_playbook")}},
        "ib": {"head": "Start with the free IB Top 30", "text": "IB Interview: Top 30 Questions covers the 30 most-asked investment banking interview questions with model answers. Free on Gumroad.",
               "btn": "Get the free Top 30", "url": IB_FREE + f"?utm_source=site&utm_medium=tool&utm_campaign={P_CAMP}&utm_content=ib_last3", "promo": False, "alt": None},
    }
    return {
        "promoText": PROMO_TEXT, "promoShort": PROMO_SHORT,
        "tracks": {
            "aie": {"name": "AI engineer", "items": [item(p) for p in aie], "tasks": [], "mock": "../mock-interview/?track=aie&n=5&min=3",
                    "note": "All 50 AI engineer question pages, Entry level first, each with a self-check rubric."},
            "ds": {"name": "Data science", "items": [item(BY_SLUG[s]) for s in DS_SLUGS], "tasks": DS_TASKS, "mock": "../mock-interview/?track=aie&n=5&min=3",
                   "note": "We do not have a dedicated data science question bank yet. This track uses the free AI engineer pages that overlap with data science loops (experiments, evaluation, model basics) and adds daily SQL, statistics and product tasks without links."},
            "pm": {"name": "Product manager", "items": [item(BY_SLUG[s]) for s in PM_SLUGS], "tasks": PM_TASKS, "mock": "../mock-interview/?track=aie&n=5&min=3",
                   "note": "We do not have a dedicated PM question bank yet. This track uses the free AI engineer pages a PM on an AI product is most likely to be asked about, and adds daily product sense, execution and behavioral tasks without links."},
            "ib": {"name": "Investment banking", "items": [{"s": q["slug"], "q": q["q"], "l": "", "u": q["model"], "c": f"../answer-check/?track=ib&q={q['slug']}"} for q in ib],
                   "tasks": [], "mock": "../mock-interview/?track=ib&n=5&min=3",
                   "note": "All 50 investment banking question pages from the free IB question bank, each with a self-check rubric."},
        },
        "cta": ctas,
    }


def plan_page():
    rel = "../"
    vis_faq, faq_ld = faq_block(P_FAQ)
    app = {"@context": "https://schema.org", "@type": "WebApplication", "name": "Interview Study Plan Generator", "url": PLAN_URL,
           "applicationCategory": "EducationalApplication", "operatingSystem": "Any", "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
           "publisher": {"@type": "Organization", "name": "Valenx Press"}}
    o = [head(P_TITLE, P_DESC, PLAN_URL, rel, ld(app) + faq_ld + TOOL_CSS).replace('content="article"', 'content="website"', 1)]
    o.append('<header class=qhero data-hero><div class=wrap><div class="crumb label"><a href="../">AI Engineer Interview Questions</a> / Tools / Study plan</div>'
             '<span class=badge>Free tool</span><h1>Your interview study plan, day by day</h1>'
             '<p class=lead>Enter your interview date. Get one plan from today to the day: what to study, a self-check link to score yourself each night, '
             'and a mock round before the interview. Free, printable, built on the free question pages.</p>'
             f'<div class=acts><a class="btn btn-primary" href="#plan">Build my plan {ARROW}</a>'
             f'<a class="btn btn-ghost" href="{e(paid("ai-engineer-interview-playbook", P_CAMP, "hero"))}">Get the AI engineer playbook</a></div>'
             f'<p class=price-line><span><span class=num>{PRICE}</span> on Gumroad, instant download</span>{promo()}</p></div></header>')
    o.append('<main id=main class=body><div class=read>')
    o.append('<section id=plan class=tool aria-labelledby=plan-h><h2 id=plan-h style="margin-top:0">Your interview</h2><div class=grid2>'
             '<div><label class=f for=d>Interview date</label><input id=d type=date></div>'
             '<div><label class=f for=t>Track</label><select id=t><option value=aie>AI engineer</option><option value=ds>Data science</option>'
             '<option value=pm>Product manager</option><option value=ib>Investment banking</option></select></div></div>'
             '<p class=hint id=tnote></p><div id=msg class=msg hidden></div><p id=sum style="font-weight:600;margin:var(--s3) 0 0"></p>'
             '<p class=noprint><button type=button class="btn btn-ghost" id=pr>Print this plan</button></p>'
             '<ol class=plan id=days></ol></section>')
    o.append('<h2>How to use the plan</h2><ol class=steps>'
             '<li>Study the day\'s questions: read the framework, then close the page and answer out loud.</li>'
             '<li>End every day with the self-check link. Paste what you said and read the model answer for anything under 70.</li>'
             '<li>Tick the day off. Ticks are saved in this browser only.</li>'
             '<li>Do the mock round the day before under time, and keep the interview day light.</li></ol>')
    o.append(cta_box_aie("cta_mid", P_CAMP))
    o.append('<h2>Questions</h2>' + vis_faq)
    o.append('<p class=muted><a href="../answer-check/">Free answer self-check</a> &middot; <a href="../llm-cost-calculator/">LLM cost calculator</a> &middot; '
             '<a href="../mock-interview/">Mock round</a> &middot; <a href="../questions/">Question deep dives</a></p>')
    o.append('</div></main>' + sticky(paid("ai-engineer-interview-playbook", P_CAMP, "sticky_bar")))
    o.append(PLAN_JS.replace("__DATA__", json.dumps(plan_data()).replace("</", "<\\/")))
    o.append(foot(rel))
    return "".join(o)


PLAN_JS = r"""<script>
(function(){
var D=__DATA__,DAY=864e5,MAXD=60;
function $(i){return document.getElementById(i)}
function d0(x){return new Date(x.getFullYear(),x.getMonth(),x.getDate())}
function parse(v){var m=/^(\d{4})-(\d{2})-(\d{2})$/.exec(v||"");return m?new Date(+m[1],+m[2]-1,+m[3]):null}
function iso(x){return x.getFullYear()+"-"+String(x.getMonth()+1).padStart(2,"0")+"-"+String(x.getDate()).padStart(2,"0")}
function add(x,n){return new Date(x.getFullYear(),x.getMonth(),x.getDate()+n)}
function nice(x){return x.toLocaleDateString("en-US",{weekday:"short",month:"short",day:"numeric"})}
/* build(track, interviewDate, today) -> {status, days[], start, total} ; pure, exported for tests */
function build(tk,iv,today){var T=D.tracks[tk],diff=Math.round((d0(iv)-d0(today))/DAY),out={status:"ok",diff:diff,days:[]};
 if(diff<0){out.status="past";return out}
 var items=T.items,tasks=T.tasks,start=d0(today),L=diff+1;
 if(diff>MAXD){out.status="far";L=MAXD+1;start=add(d0(iv),-MAXD)}
 out.start=start;out.total=L;
 if(L===1){out.status="today";out.days.push({kind:"warm",title:"Interview day: warm-up only",items:items.slice(0,3),task:tasks[0]||null,check:items[0],mock:T.mock});return out}
 var R=L-2,review=[],learnIdx=[],i;
 for(i=0;i<R;i++){if(R>=10&&(i+1)%5===0)review.push(i);else learnIdx.push(i)}
 var nl=learnIdx.length,per=nl?Math.min(4,Math.max(1,Math.ceil(items.length/nl))):0,pos=0,seen=[],plan=[];
 for(i=0;i<R;i++){
  if(review.indexOf(i)>=0){var back=seen.slice(-Math.min(seen.length,8));var pick=back.length?[back[0],back[Math.floor(back.length/2)]].filter(function(v,j,a){return a.indexOf(v)===j}):items.slice(0,2);
   plan.push({kind:"review",title:"Review and a short mock round",items:pick,task:null,check:pick[0],mock:T.mock});continue}
  var day=[];
  if(pos<items.length){day=items.slice(pos,pos+per);pos+=per}
  else{var k=(pos-items.length)%items.length;day=[items[k]];pos++}
  var second=seen.indexOf(day[0])>=0;day.forEach(function(x){if(seen.indexOf(x)<0)seen.push(x)});
  plan.push({kind:second?"second":"learn",title:second?"Second pass":"Learn",items:day,task:tasks.length?tasks[plan.length%tasks.length]:null,check:day[0],mock:null})}
 var top=seen.length?seen:items;
 plan.push({kind:"mock",title:"Full mock round under time",items:top.slice(0,2),task:null,check:top[0],mock:T.mock});
 plan.push({kind:"warm",title:"Interview day: warm-up only",items:items.slice(0,3),task:null,check:items[0],mock:null});
 out.days=plan;out.covered=Math.min(items.length,seen.length);return out}
window.studyPlan=build;
function el(t,c,txt){var x=document.createElement(t);if(c)x.className=c;if(txt!==undefined)x.textContent=txt;return x}
function link(h,txt){var a=el("a",null,txt);a.href=h;return a}
function ctaNode(tk){var c=D.cta[tk],w=el("div","pc");w.appendChild(el("b",null,c.head));w.appendChild(el("p",null,c.text));
 var b=link(c.url,c.btn+" \u2192");b.className="btn btn-primary";w.appendChild(b);
 if(c.promo){var s=el("span","badge promo");s.appendChild(el("span","pl",D.promoText));s.appendChild(el("span","ps",D.promoShort));w.appendChild(s)}
 if(c.alt){var p=el("p","alt-buy",c.alt.lead);p.appendChild(link(c.alt.url,c.alt.text));p.appendChild(document.createTextNode(c.alt.post));w.appendChild(p)}
 return w}
function key(){return "vp-plan-"+$("t").value+"-"+$("d").value}
function render(){var tk=$("t").value,iv=parse($("d").value),T=D.tracks[tk],box=$("days"),msg=$("msg");box.textContent="";msg.hidden=true;$("sum").textContent="";
 $("tnote").textContent=T.note;
 try{history.replaceState(null,"","?track="+tk+($("d").value?"&date="+$("d").value:"")+location.hash)}catch(e){}
 if(iv===null){$("sum").textContent="Pick your interview date to build the plan.";return}
 var P=build(tk,iv,new Date());
 if(P.status==="past"){msg.hidden=false;msg.textContent="That date has passed. If the interview already happened, write down every question you remember tonight while it is fresh, score your answers in the self-check, then enter the date of your next interview.";return}
 if(P.status==="today"){msg.hidden=false;msg.textContent="Your interview is today. Skip new material. Re-read three core answers, do one short timed round, and stop at least an hour before the interview."}
 if(P.status==="far"){msg.hidden=false;msg.textContent="Your interview is "+P.diff+" days away. This plan covers the final "+MAXD+" days and starts on "+nice(P.start)+". Until then, one question every few days and a weekly mock round is enough."}
 $("sum").textContent=T.name+" plan: "+P.total+(P.total===1?" day":" days")+" from "+nice(P.start)+" to "+nice(iv)+(P.covered>0?", covering "+P.covered+" of "+T.items.length+" questions.":".");
 var store={};try{store=JSON.parse(localStorage.getItem(key())||"{}")}catch(e){}
 P.days.forEach(function(d,i){var li=el("li");if(i>=P.days.length-3)li.className="last";var dt=add(P.start,i);
  var h=el("div","dh");h.appendChild(el("span","label","Day "+(i+1)+" \u00b7 "+nice(dt)));h.appendChild(el("b",null,d.title));
  var lab=el("label","done"),cb=el("input");cb.type="checkbox";cb.checked=store[i]===1;cb.addEventListener("change",function(){store[i]=cb.checked?1:0;try{localStorage.setItem(key(),JSON.stringify(store))}catch(e){}});
  lab.appendChild(cb);lab.appendChild(document.createTextNode("Done"));h.appendChild(lab);li.appendChild(h);
  var ul=el("ul");d.items.forEach(function(x){var r=el("li");r.appendChild(link(x.u,x.q));if(x.l)r.appendChild(document.createTextNode(" ("+x.l+")"));ul.appendChild(r)});
  if(d.task){var r=el("li",null,d.task);ul.appendChild(r)}
  if(d.mock){var r2=el("li");r2.appendChild(link(d.mock,"Run a timed mock round: 5 questions, 3 minutes each"));ul.appendChild(r2)}
  li.appendChild(ul);
  var sc=el("p","sc","Self-check: ");sc.appendChild(link(d.check.c,"score your answer to \u201c"+d.check.q+"\u201d"));li.appendChild(sc);
  if(i>=P.days.length-3)li.appendChild(ctaNode(tk));
  box.appendChild(li)})}
function init(){var p=new URLSearchParams(location.search),t=p.get("track");if(t&&D.tracks[t])$("t").value=t;
 var dv=p.get("date");$("d").value=parse(dv)?dv:iso(add(new Date(),14));
 $("d").addEventListener("change",render);$("d").addEventListener("input",render);$("t").addEventListener("change",render);
 $("pr").addEventListener("click",function(){window.print()});render()}
if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",init);else init();
})();
</script>"""


def main():
    for d, fn in (("llm-cost-calculator", calc_page), ("study-plan", plan_page)):
        os.makedirs(os.path.join(ROOT, d), exist_ok=True)
        open(os.path.join(ROOT, d, "index.html"), "w").write(fn())
    print("built llm-cost-calculator and study-plan")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Generate /mock-interview/index.html: free mock interview round generator with a per-question timer (client-side JS).

Run from the repo root:  python3 tools/build_mock_interview.py
Questions and buy links come from tools/build_answer_check.py (data()), which reuses CTA_URL in
tools/build_question_pages.py, so removing EARLYBF there removes it here after a rebuild.
"""
import html, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_answer_check as A
from build_question_pages import PROMO_ON, PROMO_TEXT, PRICE, head, foot

ROOT = A.ROOT
URL = f"{A.SITE}/mock-interview/"
e = html.escape
ARROW = A.ARROW
TITLE = "Mock Interview Question Generator with Timer: AI Engineer and Investment Banking"
DESC = ("Free mock interview round generator: draw 3 to 8 random AI engineer or investment banking interview questions, "
        "answer each out loud against a timer, then score every answer with the free self-check.")


def buy(track, content):
    base = A.AIE_BUY if track == "aie" else A.IB_BUY
    q = "&".join(x for x in (A.OFFER_Q, f"utm_source=tool&utm_medium=mockround&utm_campaign={track}&utm_content={content}") if x)
    return base + "?" + q


CSS = """<style>
.mk fieldset{border:0;margin:0 0 var(--s3);padding:0}.mk legend{display:block;font-weight:600;margin-bottom:var(--s1)}
.seg{display:flex;flex-wrap:wrap;gap:var(--s1)}.seg label{display:flex;align-items:center;gap:var(--s1);background:var(--surface);border:1px solid var(--line);border-radius:var(--r-pill);padding:10px 16px;cursor:pointer;font-weight:600}
.seg input{width:18px;height:18px;accent-color:var(--ink)}.seg label:has(input:checked){border-color:var(--ink);box-shadow:inset 0 0 0 1px var(--ink)}
.mk button.btn{cursor:pointer;font:inherit}.mk button:focus-visible,.seg input:focus-visible{outline:2px solid var(--pop);outline-offset:2px}
#stage[hidden],#done[hidden],#setup[hidden]{display:none}
.mkcard{background:var(--ink);color:var(--bg);border-radius:var(--r-md);padding:var(--s4);margin:0 0 var(--s3)}
.body .mkcard p,.body .mkcard h2{color:var(--bg)}.mkcard .label{opacity:.7}.mkcard h2{font-size:clamp(1.5rem,3.4vw,2.4rem);line-height:1.15;margin:var(--s1) 0 var(--s3)}
.clock{font-family:var(--font-serif);font-size:clamp(3.5rem,10vw,6.5rem);line-height:1;font-variant-numeric:tabular-nums}.clock.over{color:var(--pop)}
.bar{height:8px;background:rgba(255,255,255,.18);border-radius:var(--r-pill);overflow:hidden;margin-top:var(--s2)}.bar span{display:block;height:100%;background:var(--pop);width:100%}
.mkcard .acts a,.mkcard .acts button{margin-top:var(--s2)}.body .mkcard a.btn-ghost{color:var(--bg);border-color:rgba(255,255,255,.4)}
.body .mkcard button.btn-primary{background:var(--bg);color:var(--ink)}
ol.recap li{margin:10px 0}ol.recap .t{font-size:var(--fs-small);color:var(--ink-2)}
.hint{font-size:var(--fs-small);color:var(--ink-2);margin:6px 0 0}
</style>"""

JS = r"""<script>(function(){
var D=__DATA__,st={};
function $(i){return document.getElementById(i)}
function val(n){var x=document.querySelector('input[name='+n+']:checked');return x?x.value:''}
function shuffle(a){a=a.slice();for(var i=a.length-1;i>0;i--){var j=Math.floor(Math.random()*(i+1));var t=a[i];a[i]=a[j];a[j]=t}return a}
function fmt(s){var n=Math.abs(s),m=Math.floor(n/60),r=n%60;return (s<0?'+':'')+m+':'+(r<10?'0':'')+r}
function check(t,q){return '../answer-check/?track='+t+'&q='+encodeURIComponent(q.slug)}
function lvl(){var x=$('lv');return x?x.value:''}
function start(){var t=val('track'),n=+val('n'),m=+val('min'),L=t==='aie'?lvl():'';
 var pool=D[t].qs.filter(function(q){return !L||q.level===L});if(!pool.length)pool=D[t].qs;
 st={t:t,qs:shuffle(pool).slice(0,n),i:0,sec:m*60,used:[]};$('setup').hidden=true;$('done').hidden=true;$('stage').hidden=false;show();
 history.replaceState(null,'','?track='+t+'&n='+n+'&min='+m);}
function show(){var q=st.qs[st.i];$('s-n').textContent='Question '+(st.i+1)+' of '+st.qs.length+' \u00b7 '+D[st.t].name+(q.level?' \u00b7 '+q.level:'');
 $('s-q').textContent=q.q;$('s-check').href=check(st.t,q);$('s-model').href=q.model;$('s-next').textContent=st.i+1<st.qs.length?'Next question':'Finish round';
 st.left=st.sec;st.t0=Date.now();tick();clearInterval(st.h);st.h=setInterval(tick,250);$('s-q').focus();}
function tick(){var s=st.sec-Math.floor((Date.now()-st.t0)/1000);var c=$('s-clock');c.textContent=fmt(s);c.classList.toggle('over',s<0);
 $('s-bar').style.width=Math.max(0,100*s/st.sec)+'%';st.left=s;}
function next(){clearInterval(st.h);st.used.push(Math.floor((Date.now()-st.t0)/1000));st.i++;if(st.i<st.qs.length){show();return}done();}
function done(){$('stage').hidden=true;var o='';st.qs.forEach(function(q,i){o+='<li><b>'+esc(q.q)+'</b><br><span class=t>'+fmt(st.used[i]).replace('+','')+' used</span> \u00b7 <a href="'+check(st.t,q)+'">Score my answer</a> \u00b7 <a href="'+q.model+'">Model answer</a></li>'});
 $('d-list').innerHTML=o;var c=D[st.t].cta;$('d-head').textContent=c.head;$('d-text').textContent=c.text;$('d-buy').href=c.end;$('d-buytxt').textContent=c.btn;
 $('done').hidden=false;$('d-h').focus();}
function esc(s){return s.replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
function syncTrack(){var t=val('track');$('lv-row').hidden=t!=='aie';var b=$('hero-buy');if(b)b.href=D[t].cta.hero;var s=$('sticky-buy');if(s)s.href=D[t].cta.sticky;}
document.addEventListener('DOMContentLoaded',function(){
 var p=new URLSearchParams(location.search);['track','n','min'].forEach(function(k){var v=p.get(k);if(v){var x=document.querySelector('input[name='+k+'][value="'+v+'"]');if(x)x.checked=true}});
 document.querySelectorAll('input[name=track]').forEach(function(x){x.addEventListener('change',syncTrack)});syncTrack();
 $('go').addEventListener('click',start);$('s-next').addEventListener('click',next);$('s-skip').addEventListener('click',next);
 $('d-again').addEventListener('click',start);$('d-setup').addEventListener('click',function(){$('done').hidden=true;$('setup').hidden=false});
});
})();</script>"""


def build():
    d = A.data()["tracks"]
    data = {}
    for t, tr in d.items():
        data[t] = {"name": tr["name"],
                   "qs": [{"slug": q["slug"], "q": q["q"], "level": q.get("level", ""), "model": q["model"]} for q in tr["questions"]],
                   "cta": {"head": tr["cta"]["head"], "text": tr["cta"]["text"], "btn": tr["cta"]["btn"],
                           "hero": buy(t, "hero"), "end": buy(t, "end_card"), "sticky": buy(t, "sticky_bar")}}
    n_aie, n_ib = len(data["aie"]["qs"]), len(data["ib"]["qs"])
    ld = {"@context": "https://schema.org", "@type": "WebApplication", "name": "Mock Interview Round Generator", "url": URL,
          "description": DESC, "applicationCategory": "EducationalApplication", "operatingSystem": "Any",
          "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}}
    faq = [
        ("How does the mock interview generator work?", f"Pick a track, how many questions and how long per question. It draws random questions from {n_aie} AI engineer or {n_ib} investment banking questions and runs a countdown for each one. Answer out loud as if an interviewer were listening."),
        ("How long should each answer take?", "Most single interview answers run one to three minutes. Technical questions with follow-ups can take longer, so the 5 minute setting suits system design and LBO walkthroughs."),
        ("How do I know if my answer was good?", "Every question links to the free Interview Answer Self-Check. Type what you said and it scores coverage of the key concepts, structure and length against a published rubric, and links the model answer."),
        ("Is it free and private?", "Yes. It runs in your browser, nothing is recorded, and there is no sign-up."),
        ("What is the Playbook and do I need it?", f"The free questions and model answers are enough to practice. The Playbook ({PRICE} on Gumroad) adds the answer frameworks, worked walkthroughs and a study plan in one download. Buy it only if the free material shows gaps you want to close faster."),
        ("Is this a replacement for a real mock interview?", "No. A timer and random questions recreate the pressure of not knowing what comes next, but a person can push on follow-ups. Use this daily and a human mock before the real loop."),
    ]
    ldf = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}
    tags = '<script type="application/ld+json">' + json.dumps(ld) + '</script><script type="application/ld+json">' + json.dumps(ldf) + "</script>"
    h = head(TITLE, DESC, URL, "../", tags + CSS).replace('<meta property="og:type" content="article">', '<meta property="og:type" content="website">')
    promo = f'<span class="badge promo">{PROMO_TEXT}</span>' if PROMO_ON else ""
    seg = lambda name, opts, chk: "".join(f'<label for={name}-{v}><input type=radio name={name} id={name}-{v} value={v}{" checked" if v == chk else ""}> {lab}</label>' for v, lab in opts)
    o = [h,
         '<header class=qhero data-hero><div class=wrap><div class="crumb label"><a href="../">AI Engineer Interview Questions</a> / <a href="../answer-check/">Self-check</a> / Mock round</div>'
         '<span class=badge>Free tool</span><h1>Mock interview round generator, with a timer</h1>'
         f'<p class=lead>Random questions, a clock, no notes. Draw 3 to 8 questions from {n_aie} AI engineer or {n_ib} investment banking questions, answer each one out loud before time runs out, then score every answer with the free self-check.</p>'
         f'<div class=acts><a class="btn btn-primary" href="#setup">Start a round {ARROW}</a><a class="btn btn-ghost" id=hero-buy href="{e(data["aie"]["cta"]["hero"])}">Get the playbook</a></div>'
         f'<p class=price-line><span><span class=num>{PRICE}</span> on Gumroad, instant download</span>{promo}</p></div></header>',
         '<main id=main class=body><div class="read mk">',
         '<section id=setup aria-labelledby=setup-h><h2 id=setup-h>Set up your round</h2>'
         f'<fieldset><legend>Track</legend><div class=seg>{seg("track", [("aie", "AI Engineer"), ("ib", "Investment Banking")], "aie")}</div></fieldset>'
         '<fieldset id=lv-row><legend>Level (AI Engineer)</legend><select id=lv style="font:inherit;padding:10px;border:1px solid var(--line);border-radius:var(--r-sm)"><option value="">All levels</option><option>Entry</option><option>Mid</option><option>Senior</option></select></fieldset>'
         f'<fieldset><legend>Questions</legend><div class=seg>{seg("n", [("3", "3 quick"), ("5", "5 standard"), ("8", "8 full loop")], "5")}</div></fieldset>'
         f'<fieldset><legend>Minutes per question</legend><div class=seg>{seg("min", [("2", "2 min"), ("3", "3 min"), ("5", "5 min")], "3")}</div></fieldset>'
         f'<div class=acts><button class="btn btn-primary" type=button id=go>Start the clock {ARROW}</button></div>'
         '<p class=hint>Say each answer out loud. The clock keeps running past zero so you can see how far over you went.</p></section>',
         '<section id=stage hidden aria-live=polite><div class=mkcard><span class=label id=s-n></span><h2 id=s-q tabindex=-1></h2>'
         '<div class=clock id=s-clock aria-label="Time left">3:00</div><div class=bar aria-hidden=true><span id=s-bar></span></div>'
         '<div class=acts><button class="btn btn-primary" type=button id=s-next>Next question</button><a class="btn btn-ghost" id=s-check target=_blank rel=noopener href="../answer-check/">Score this answer</a></div>'
         '<p class=hint style="color:inherit;opacity:.75"><a id=s-model target=_blank rel=noopener href="../questions/" style="color:inherit">Peek at the model answer</a> after you answer, not before. <button type=button id=s-skip style="background:none;border:0;color:inherit;text-decoration:underline;cursor:pointer;font:inherit;padding:0">Skip</button></p></div></section>',
         '<section id=done hidden><h2 id=d-h tabindex=-1>Round complete</h2><p>Now score each answer while you still remember what you said. Scores show which concepts you missed.</p><ol class=recap id=d-list></ol>'
         '<div class=acts><button class="btn btn-ghost" type=button id=d-again>New round, same settings</button><button class="btn btn-ghost" type=button id=d-setup>Change settings</button></div>'
         f'<div class=cta><span class=label>The Playbook</span><b id=d-head></b><p id=d-text></p><a class="btn btn-primary" id=d-buy href="{e(data["aie"]["cta"]["end"])}"><span id=d-buytxt>Get the playbook</span> {ARROW}</a>{promo}</div></section>',
         '<h2>Why practice with a timer</h2><p>In a real loop you do not choose the question and you cannot pause. Practicing the same questions in order trains recall of a script. Random order and a visible clock train the skill that is actually tested: structuring an answer on the spot and stopping on time.</p>'
         '<ol class=steps><li>Pick a track and a round length. 5 questions at 3 minutes is about one interview block.</li><li>Answer out loud. Lead with the direct answer, then how it works, then one example or trade-off.</li><li>When the round ends, paste what you said into the self-check for each question.</li><li>Read the model answer for anything under 70, then run a new round tomorrow.</li></ol>',
         '<h2>Price check</h2><p>Paid interview guides for these loops are listed at $99 to $197 (Wall Street Prep Red Book $99, Breaking Into Wall Street IB Interview Guide $197, prices on their own pages on Nov 1, 2026). This generator and the self-check are free. '
         f'The Playbook is {PRICE} and adds the frameworks behind every model answer.</p>',
         f'<div class=cta><span class=label>The Playbook</span><b>Want the frameworks behind the model answers?</b><p>{e(data["aie"]["cta"]["text"])}</p>'
         f'<a class="btn btn-primary" href="{e(buy("aie", "cta_box"))}">Get the AI Engineer playbook {ARROW}</a> '
         f'<a class="btn btn-ghost" href="{e(buy("ib", "cta_box"))}">Get the IB playbook</a>{promo}</div>',
         '<h2>FAQ</h2>' + "".join(f'<div class=fu><b>{e(q)}</b> {e(a)}</div>' for q, a in faq),
         f'<p class=muted>Also free: <a href="../answer-check/">Interview Answer Self-Check</a> &middot; <a href="../">100 AI engineer interview questions</a> &middot; <a href="{A.IB_SITE}/">100 investment banking interview questions</a></p>',
         '</div></main>',
         '<div class=sticky-cta role=complementary aria-label="Buy the playbook" aria-hidden=true><span class=t><b><span class=full>The 0&rarr;1 Interview Playbooks</span><span class=short>The Playbook</span></b>'
         + ('<span class="long promo"> &middot; 40% off until Nov 3</span><span class="short promo"> &middot; 40% off</span>' if PROMO_ON else '') +
         f'</span><a class=btn id=sticky-buy href="{e(data["aie"]["cta"]["sticky"])}">Get it &rarr;</a></div>',
         JS.replace("__DATA__", json.dumps(data)),
         foot("../")]
    os.makedirs(os.path.join(ROOT, "mock-interview"), exist_ok=True)
    out = "".join(o)
    open(os.path.join(ROOT, "mock-interview", "index.html"), "w").write(out)
    print("wrote mock-interview/index.html", len(out), n_aie, n_ib)


if __name__ == "__main__":
    build()

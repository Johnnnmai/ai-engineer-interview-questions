#!/usr/bin/env python3
"""Generate /answer-check/index.html, the free Interview Answer Self-Check (pure client-side JS).

Run from the repo root:  python3 tools/build_answer_check.py
Rubric data lives in tools/answer_check_data.py; AIE titles come from tools/question_pages_data.py.
"""
import html, json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from question_pages_data import PAGES
import answer_check_data as D

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://johnnnmai.github.io/ai-engineer-interview-questions"
IB_SITE = "https://johnnnmai.github.io/investment-banking-interview-questions"
URL = f"{SITE}/answer-check/"
UTM = "offer_code=EARLYBF&utm_source=tool&utm_medium=answercheck&utm_campaign={track}"
OFFER_EXPIRES = "2026-11-04T07:59:00Z"  # EARLYBF expiry read from the Gumroad product page; the offer line hides after it

TITLE = "Check My Interview Answer: Free Interview Answer Self-Check"
DESC = ("Check my interview answer for free: paste your answer to an AI engineer or investment banking "
        "interview question and get a 0 to 100 rubric score, missed concepts and tips.")
e = html.escape
STYLE = re.search(r"<style>.*?</style>", open(os.path.join(ROOT, "index.html")).read(), re.S).group(0)
CSS = """<style>.crumb{font-size:.9rem}.crumb a{color:#cfd6e4}.w p a,.w li a{color:#175cd3}
fieldset{border:0;margin:0 0 14px;padding:0}legend,label.lb{display:block;font-weight:700;margin-bottom:6px}
.seg{display:flex;flex-wrap:wrap;gap:8px}.seg label{display:flex;align-items:center;gap:8px;background:#fff;border:1px solid #d0d5dd;border-radius:8px;padding:10px 14px;cursor:pointer;font-weight:600}
.seg input{width:18px;height:18px;accent-color:#101828}.seg label:has(input:checked){border:2px solid #101828;background:#fff8e1}
select,textarea{width:100%;font:inherit;font-size:1rem;border:1px solid #98a2b3;border-radius:8px;padding:10px;background:#fff;color:#14161a}
textarea{min-height:220px;resize:vertical;line-height:1.5}select:focus,textarea:focus,button:focus,.seg input:focus,a:focus{outline:3px solid #f5c542;outline-offset:2px}
.row{margin:0 0 16px}.hint{font-size:.9rem;color:#475467;margin:4px 0 0}.acts{display:flex;flex-wrap:wrap;gap:10px;align-items:center}
button.btn{border:0;cursor:pointer}button.sec{background:#fff;border:1px solid #98a2b3;color:#14161a;border-radius:8px;padding:12px 18px;font:inherit;cursor:pointer}
#result{margin-top:24px}#result[hidden]{display:none}.scorebox{display:flex;flex-wrap:wrap;gap:18px;align-items:center;background:#101828;color:#fff;border-radius:10px;padding:18px 20px}
.big{font-size:3rem;font-weight:800;line-height:1}.big small{font-size:1.1rem;color:#cfd6e4}.band{font-weight:700;font-size:1.15rem}.scorebox p{margin:4px 0 0;color:#cfd6e4}
.meter{height:10px;background:#344054;border-radius:5px;overflow:hidden;flex-basis:100%}.meter span{display:block;height:100%;background:#f5c542}
ul.ck{list-style:none;padding:0;margin:8px 0}ul.ck li{padding:6px 0 6px 30px;position:relative;border-bottom:1px solid #f2efe8}
ul.ck li:before{position:absolute;left:0;top:5px;width:22px;height:22px;border-radius:50%;text-align:center;font-weight:800;line-height:22px;font-size:.85rem}
ul.ck li.ok:before{content:'\\2713';background:#d1fadf;color:#05603a}ul.ck li.no:before{content:'\\2717';background:#fee4e2;color:#912018}ul.ck li.mid:before{content:'?';background:#fef0c7;color:#93370d}
.tag{font-size:.75rem;font-weight:700;padding:1px 6px;border-radius:3px;margin-left:6px}.tag.ok{background:#d1fadf;color:#05603a}.tag.no{background:#fee4e2;color:#912018}.tag.mid{background:#fef0c7;color:#93370d}
.vh{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}ol.tips li{margin:8px 0}
.offer{font-size:.95rem;color:#344054}.human{font-size:.9rem;color:#475467;margin-top:10px}@media (max-width:600px){h1{font-size:1.6rem}.big{font-size:2.4rem}.seg label{flex:1 1 100%}}</style>"""


def concepts(lst):
    return [{"label": c[0], "rx": c[1], "min": (c[2] if len(c) > 2 else 1)} for c in lst]


def data():
    aie = []
    for p in PAGES:
        if p["slug"] not in D.AIE:  # rubric covers 10 AIE questions; the question bank has more pages
            continue
        r = D.AIE[p["slug"]]
        aie.append({"slug": p["slug"], "q": p["q"], "level": p["level"], "model": f"../questions/{p['slug']}/",
                    "followup": p["followups"][0][0] if p["followups"] else "", "concepts": concepts(r["concepts"]), "logic": []})
    ib = []
    for slug, r in D.IB.items():
        ib.append({"slug": slug, "q": r["q"], "model": f"{IB_SITE}/questions/{slug}/", "followup": D.IB_FOLLOWUPS.get(slug, ""),
                   "concepts": concepts(r["concepts"]), "logic": r.get("logic", [])})
    assert len(aie) == 10 and len(ib) == 10
    tracks = {
        "aie": {"name": "AI Engineer", "questions": aie,
                "cta": {"url": "https://sirjohnnymai.gumroad.com/l/ai-engineer-interview-playbook?" + UTM.format(track="aie"),
                        "head": "Want model answers for all 100 AI engineer questions?",
                        "text": "The 0 to 1 AI Engineer Interview Playbook covers the answer frameworks, system-design walkthroughs and an 8-week plan.",
                        "btn": "Get the AI Engineer playbook"}},
        "ib": {"name": "Investment Banking", "questions": ib,
               "cta": {"url": "https://sirjohnnymai.gumroad.com/l/ib-interview-playbook?" + UTM.format(track="ib"),
                       "head": "Need the frameworks and full walkthroughs?",
                       "text": "The 0 to 1 Investment Banking Interview Playbook covers fit and behavioral answers, modeling tests and a prep plan.",
                       "btn": "Get the IB playbook"}},
    }
    return {"tracks": tracks, "offerExpires": OFFER_EXPIRES}


JS = r"""
(function(root){
"use strict";
var UP="(up|increas\\w*|ris(e|es|ing)|rose|higher|grow(s|ing)?|gains?|raise[sd]?|raising|boost\\w*|goes up|more)";
var DOWN="(down|decreas\\w*|fall(s|ing)?|fell|drop(s|ped|ping)?|lower(s|ed)?|declin\\w*|reduc\\w*|less|cuts?)";
var reUp=new RegExp("\\b"+UP+"\\b","i"), reDown=new RegExp("\\b"+DOWN+"\\b","i");
var STRUCT={
 def:/\b(is|are|means|refers to|stands for|describes|captures|shows|lets|has two|there are|i would|i'd|i start|start(s)? (with|by)|first|at a high level|in short|assume|two experiences)\b/i,
 how:/\b(because|so that|which means|this means|that means|works by|in order to|the reason|that is why|that's why|therefore|so (the|it|i|each|we|you|they|cash|net)|which (lets|makes|keeps)|then|next|finally|after that|first|second|third|steps?)\b/gi,
 ex:/\b(for example|for instance|e\.g\.|such as|say|imagine|suppose|trade-?offs?|downside|however|but|the cost|at the cost|versus|vs\.?|compared|whereas|on the other hand|limitations?|unless|instead)\b|\$?\d+(\.\d+)?\s*(%|x\b|m\b|gb\b|gib\b|k\b)/i
};
function rx(s){return new RegExp(s,"i");}
function words(t){var m=t.trim().match(/\S+/g);return m?m.length:0;}
function sentences(t){return t.replace(/([.?;:])\s+/g,"$1\n").split(/\n+/).map(function(s){return s.trim();}).filter(function(s){return s.length>0;});}
function clauses(t){var out=[];sentences(t).forEach(function(s){s.split(/,\s+(?=and |but |so |which |while )|;\s*/i).forEach(function(c){if(c.trim())out.push(c.trim());});});return out;}
function dirIn(seg,closestLast){var u=-1,d=-1,m,g;
 g=new RegExp(reUp.source,"gi");while((m=g.exec(seg))){u=closestLast?m.index:(u<0?m.index:u);if(closestLast===false)break;}
 g=new RegExp(reDown.source,"gi");while((m=g.exec(seg))){d=closestLast?m.index:(d<0?m.index:d);if(closestLast===false)break;}
 if(u<0&&d<0)return null;if(u<0)return "down";if(d<0)return "up";
 return closestLast?(u>d?"up":"down"):(u<d?"up":"down");}
function dirNear(text,start,end,preferBefore){
 // nearest direction word after the phrase (45 chars), else just before it (20 chars); conditions look before first
 var after=text.slice(end,end+(preferBefore?18:45)), before=text.slice(Math.max(0,start-20),start);
 var a=dirIn(after,false), b=dirIn(before,true);
 return preferBefore?(b||a):(a||b);
}
function flip(d){return d==="up"?"down":"up";}
function checkLogic(c,text){
 var t=text.toLowerCase();
 if(c.subj){
  var found=null, units=c.cond?sentences(t):clauses(t);
  for(var i=0;i<units.length;i++){
   var u=units[i], want=c.want;
   if(c.cond){var cm=rx(c.cond).exec(u);if(cm===null)continue;var cd=dirNear(u,cm.index,cm.index+cm[0].length,true);if(cd===null)continue;if(cd==="down")want=flip(want);
     var rest=u.slice(cm.index+cm[0].length);
     var sre=new RegExp(c.subj,"gi"),sm,got=null;
     while((sm=sre.exec(rest))){var dd=dirNear(rest,sm.index,sm.index+sm[0].length);
       if(dd){got=dd;break;}if(sm[0].length===0)sre.lastIndex++;}
     if(got){found=(got===want)?"ok":"bad";if(found==="bad")break;}
   } else {
     var sre2=rx(c.subj), m=sre2.exec(u); if(m===null)continue;
     var d2=dirNear(u,m.index,m.index+m[0].length); if(d2===null)continue;
     found=(d2===want)?"ok":"bad"; if(found==="bad")break;
   }
  }
  return found||"missing";
 }
 var bad=(c.bad||[]).some(function(p){return rx(p).test(t);});
 if(bad)return "bad";
 if(c.pass_if_no_bad)return words(t)>=30?"ok":"missing";
 var ok=(c.ok||[]).some(function(p){return rx(p).test(t);});
 return ok?"ok":"missing";
}
function lengthPts(n){
 if(n<30)return [0,"short"]; if(n<60)return [4,"short"]; if(n<80)return [7,"short"];
 if(n<=300)return [10,"ok"]; if(n<=400)return [7,"long"]; if(n<=600)return [4,"long"]; return [0,"long"];
}
var MAX_CHARS=6000;
function normSent(s){return s.toLowerCase().replace(/[^a-z0-9%$]+/g," ").trim();}
function score(q,text){
 var t=(text||"").slice(0,MAX_CHARS), low=t.toLowerCase(), hasLogic=q.logic&&q.logic.length>0;
 var wC=hasLogic?60:70;
 var cs=q.concepts.map(function(c){var hits=c.rx.filter(function(p){return rx(p).test(low);}).length;return {label:c.label,covered:hits>=c.min};});
 var nCov=cs.filter(function(c){return c.covered;}).length;
 var cPts=Math.round(wC*nCov/cs.length);
 // anti keyword stuffing: short answers or few full sentences get half the concept points
 var n=words(t), allS=sentences(t), full=allS.filter(function(s){return words(s)>=6&&/[a-z]/i.test(s);}).length;
 var thin=n<60||full<3; if(thin)cPts=Math.round(cPts/2);
 // anti padding: share of unique sentences
 var norm=allS.map(normSent).filter(function(s){return s.length>0;}), uniq={}, nu=0;
 norm.forEach(function(s){if(uniq[s]!==1){uniq[s]=1;nu++;}});
 var uniqRatio=norm.length?nu/norm.length:1, repeated=norm.length>=4&&uniqRatio<0.7;
 var sents=sentences(t), head=sents.slice(0,2).join(" ");
 var hasDef=STRUCT.def.test(head), howHits=(t.match(STRUCT.how)||[]).length, hasHow=howHits>=2||/\b(because|so that|which means|in order to|the reason|therefore)\b/i.test(t), hasEx=STRUCT.ex.test(t);
 var st=[{part:"Definition or direct answer up front",ok:hasDef,pts:7},{part:"How it works or why (cause, steps)",ok:hasHow,pts:7},{part:"An example, number or trade-off",ok:hasEx,pts:6}];
 var sPts=st.reduce(function(a,s){return a+(s.ok?s.pts:0);},0);
 var L=lengthPts(n);
 var lg=(q.logic||[]).map(function(c){return {label:c.label,status:checkLogic(c,t),tip:c.tip};});
 var lPts=hasLogic?Math.round(10*lg.filter(function(c){return c.status==="ok";}).length/lg.length):0;
 var total=n===0?0:Math.min(100,cPts+sPts+L[0]+lPts);
 var notes=[], wrongDir=lg.some(function(c){return c.status==="bad";});
 if(wrongDir){total=Math.min(total,60);notes.push("Check the direction of the effect. Score capped at 60 because at least one direction looks reversed.");}
 if(repeated){total=Math.min(total,Math.round(60*uniqRatio));notes.push("Much of the answer repeats itself. Score reduced; say each point once.");}
 if(n>600)notes.push("Over 600 words gets no length points. A spoken answer is usually 80 to 300 words.");
 if(thin&&n>0)notes.push("Concept points halved: the answer is short or mostly keywords. Use full sentences, at least about 60 words.");
 // tips: wrong logic first, then missed concepts, structure, length, missing logic, follow-up
 var tips=[];
 lg.forEach(function(c){if(c.status==="bad")tips.push("Check your direction: "+c.tip);});
 cs.filter(function(c){return c.covered===false;}).slice(0,2).forEach(function(c){tips.push("Add this point from the model answer: "+c.label.charAt(0).toLowerCase()+c.label.slice(1)+".");});
 if(hasDef===false)tips.push("Open with a one-sentence definition or direct answer before the details.");
 if(hasHow===false)tips.push("Explain how it works or why, using \"because\" or clear steps (first, then, finally).");
 if(hasEx===false)tips.push("Add one concrete example, number or trade-off to show you have used it.");
 if(L[1]==="short")tips.push("Expand to roughly 80 to 300 words, about one to two minutes spoken.");
 if(L[1]==="long")tips.push("Trim to under about 300 words; interviewers prefer a tight answer they can follow up on.");
 lg.forEach(function(c){if(c.status==="missing")tips.push(c.tip);});
 if(q.followup)tips.push("Prepare the likely follow-up: \""+q.followup+"\"");
 tips.push("Say it out loud with a timer and record it; the written version usually reads better than it sounds.");
 tips=tips.slice(0,3);
 var band=total>=80?"Strong":total>=60?"Solid, with gaps":total>=40?"Needs work":"Thin";
 return {total:total,notes:notes,uniqueRatio:uniqRatio,band:band,words:n,concepts:cs,conceptPts:cPts,conceptMax:wC,structure:st,structurePts:sPts,lengthPts:L[0],lengthNote:L[1],logic:lg,logicPts:lPts,logicMax:hasLogic?10:0,tips:tips};
}
function find(data,track,slug){var tr=data.tracks[track];if(tr==null)return null;for(var i=0;i<tr.questions.length;i++)if(tr.questions[i].slug===slug)return tr.questions[i];return null;}
var api={score:score,checkLogic:checkLogic,find:find,scoreBySlug:function(data,track,slug,text){return score(find(data,track,slug),text);}};
root.AnswerCheck=api; if(typeof module==="object"&&module.exports)module.exports=api;
})(typeof window==="object"?window:this);
"""

UI = r"""
(function(){
"use strict";
var DATA=JSON.parse(document.getElementById("ac-data").textContent), AC=window.AnswerCheck;
var $=function(id){return document.getElementById(id);};
var sel=$("ac-q"), ta=$("ac-answer"), res=$("result");
var params=new URLSearchParams(location.search);
var visitorSrc=(params.get("utm_source")||"").replace(/[^a-z0-9_-]/gi,"-").toLowerCase().slice(0,40);
function track(){var r=document.querySelector("input[name=track]:checked");return r?r.value:"aie";}
function ctaHref(t){var u=new URL(DATA.tracks[t].cta.url);if(visitorSrc)u.searchParams.set("utm_content",visitorSrc);return u.toString();}
function fillCta(t){var c=DATA.tracks[t].cta;document.querySelectorAll(".ac-cta").forEach(function(box){
  box.querySelector(".cta-h").textContent=c.head;box.querySelector(".cta-t").textContent=c.text;
  var a=box.querySelector("a.btn");a.textContent=c.btn+" \u2192";a.href=ctaHref(t);
  var o=box.querySelector(".offer");o.hidden=(Date.now()>=Date.parse(DATA.offerExpires));});}
function fillQuestions(t,slug){sel.innerHTML="";DATA.tracks[t].questions.forEach(function(q){var o=document.createElement("option");o.value=q.slug;o.textContent=q.q;sel.appendChild(o);});
  if(slug&&AC.find(DATA,t,slug))sel.value=slug;}
function syncUrl(){var u=new URL(location.href);u.searchParams.set("track",track());u.searchParams.set("q",sel.value);history.replaceState(null,"",u.toString());}
function li(cls,text,tagText){var l=document.createElement("li");l.className=cls;l.textContent=text;if(tagText){var s=document.createElement("span");s.className="vh";s.textContent=" ("+tagText+")";l.appendChild(s);}return l;}
function render(r,q){
  $("r-score").textContent=String(r.total);$("r-band").textContent=r.band;$("r-meter").style.width=r.total+"%";
  $("r-sum").textContent="Concepts "+r.conceptPts+"/"+r.conceptMax+" \u00b7 Structure "+r.structurePts+"/20 \u00b7 Length "+r.lengthPts+"/10 ("+r.words+" words)"+(r.logicMax?" \u00b7 Logic "+r.logicPts+"/10":"");
  var nt=$("r-notes");if(nt){nt.innerHTML="";(r.notes||[]).forEach(function(x){nt.appendChild(li("no",x));});nt.hidden=!(r.notes&&r.notes.length);}
  var cov=$("r-cov"),mis=$("r-mis");cov.innerHTML="";mis.innerHTML="";
  r.concepts.forEach(function(c){(c.covered?cov:mis).appendChild(li(c.covered?"ok":"no",c.label,c.covered?"covered":"missed"));});
  if(cov.children.length===0)cov.appendChild(li("no","None of the key concepts were detected yet.","none"));
  if(mis.children.length===0)mis.appendChild(li("ok","Nothing missed. Every key concept was detected.","none missed"));
  var st=$("r-struct");st.innerHTML="";r.structure.forEach(function(s){st.appendChild(li(s.ok?"ok":"no",s.part,s.ok?"present":"missing"));});
  var lw=$("r-logic-wrap"),lg=$("r-logic");lg.innerHTML="";lw.hidden=(r.logic.length===0);
  r.logic.forEach(function(c){var lab={ok:"correct",bad:"check the direction",missing:"not stated"}[c.status];lg.appendChild(li(c.status==="ok"?"ok":c.status==="bad"?"no":"mid",c.label+" \u2014 "+lab));});
  var tp=$("r-tips");tp.innerHTML="";r.tips.forEach(function(t){var l=document.createElement("li");l.textContent=t;tp.appendChild(l);});
  var m=$("r-model");m.href=q.model;m.textContent="See the model answer: "+q.q;
  var hl=$("r-human-link");if(hl)hl.href="mailto:54d438ed87c2468592a35e13bbcb86f6@mail.grokbot.com?subject="+encodeURIComponent("Human review waitlist")+"&body="+encodeURIComponent("Track: "+track()+"\nQuestion: "+q.slug+"\n\n");
  res.hidden=false;
}
function run(ev){if(ev)ev.preventDefault();var t=track(),q=AC.find(DATA,t,sel.value);
  if(ta.value.trim().length===0){$("ac-err").textContent="Paste or type your answer first.";ta.focus();return;}
  $("ac-err").textContent="";render(AC.score(q,ta.value),q);fillCta(t);syncUrl();$("r-head").focus();}
document.querySelectorAll("input[name=track]").forEach(function(r){r.addEventListener("change",function(){fillQuestions(track());fillCta(track());res.hidden=true;syncUrl();});});
sel.addEventListener("change",function(){res.hidden=true;syncUrl();});
$("ac-form").addEventListener("submit",run);
$("ac-clear").addEventListener("click",function(){ta.value="";res.hidden=true;ta.focus();});
var t0=params.get("track")==="ib"?"ib":"aie";document.getElementById("t-"+t0).checked=true;
fillQuestions(t0,params.get("q"));fillCta(t0);
})();
"""


HUMAN_TO = "54d438ed87c2468592a35e13bbcb86f6@mail.grokbot.com"
HUMAN = (f'<p class=human id=r-human>\u60f3\u8981\u771f\u4eba\u6279\u6539\uff1f Want a human review of your answer? '
         f'<a id=r-human-link href="mailto:{HUMAN_TO}?subject=Human%20review%20waitlist">Join the waitlist</a></p>')


def cta_box(extra_cls=""):
    c = data()["tracks"]["aie"]["cta"]
    return (f'<div class="cta ac-cta{extra_cls}"><b class=cta-h>{e(c["head"])}</b><p class=cta-t>{e(c["text"])}</p>'
            f'<a class=btn href="{e(c["url"])}">{e(c["btn"])} &rarr;</a>'
            '<p class=offer>Early code EARLYBF (40% off on Gumroad) is included in this link through Nov 3, 2026.</p></div>')


def build():
    d = data()
    ld = {"@context": "https://schema.org", "@type": "WebApplication", "name": "Interview Answer Self-Check", "url": URL,
          "description": DESC, "applicationCategory": "EducationalApplication", "operatingSystem": "Any",
          "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}}
    first_aie = "".join(f'<option value="{q["slug"]}">{e(q["q"])}</option>' for q in d["tracks"]["aie"]["questions"])
    o = [f'<!doctype html><html lang=en><head><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1">'
         f'<title>{e(TITLE)}</title><meta name=description content="{e(DESC)}">'
         f'<meta property="og:title" content="{e(TITLE)}"><meta property="og:description" content="{e(DESC)}">'
         f'<meta property="og:type" content="website"><meta property="og:url" content="{URL}"><link rel=canonical href="{URL}">'
         f'<script type="application/ld+json">{json.dumps(ld)}</script>{STYLE}{CSS}</head><body>',
         '<a class=vh href="#ac-form">Skip to the answer checker</a>',
         '<header class=hero><div class=w><div class=crumb><a href="../">AI Engineer Interview Questions</a> &rsaquo; <a href="../questions/">Questions</a> &rsaquo; Answer Self-Check</div>'
         '<span class=badge>Free tool</span><h1>Check my interview answer: free Interview Answer Self-Check</h1>'
         '<p>Pick an AI engineer or investment banking question, paste your answer, and get a 0 to 100 score from a transparent rubric: '
         'which key concepts you covered and missed, whether the structure works, and two or three concrete fixes. It runs in your browser; your answer is not sent anywhere.</p></div></header>',
         '<main class=w>',
         '<form id=ac-form novalidate aria-describedby=ac-note>'
         '<fieldset class=row><legend>1. Track</legend><div class=seg>'
         '<label for=t-aie><input type=radio name=track id=t-aie value=aie checked> AI Engineer</label>'
         '<label for=t-ib><input type=radio name=track id=t-ib value=ib> Investment Banking</label></div></fieldset>'
         f'<div class=row><label class=lb for=ac-q>2. Question</label><select id=ac-q name=q>{first_aie}</select></div>'
         '<div class=row><label class=lb for=ac-answer>3. Your answer</label>'
         '<textarea id=ac-answer name=answer maxlength=6000 spellcheck=true aria-describedby="ac-hint ac-err" placeholder="Type or paste the answer you would give out loud."></textarea>'
         '<p class=hint id=ac-hint>Aim for what you would say in one to two minutes, roughly 80 to 300 words (6,000 characters max).</p><p class=hint id=ac-err role=alert style="color:#912018"></p></div>'
         '<div class=acts><button class=btn type=submit>Check my answer</button><button class=sec type=button id=ac-clear>Clear</button></div>'
         '<p class=hint id=ac-note>A keyword and structure check against the model answer, not a verdict from an interviewer. Use it to find gaps, then practice out loud.</p></form>',
         '<section id=result hidden aria-live=polite aria-labelledby=r-head>'
         '<h2 id=r-head tabindex=-1>Your result</h2><div class=scorebox><div class=big><span id=r-score>0</span><small> / 100</small></div>'
         '<div><div class=band id=r-band></div><p id=r-sum></p><ul class=ck id=r-notes hidden></ul></div><div class=meter aria-hidden=true><span id=r-meter style="width:0"></span></div></div>'
         '<div class=grid style="margin-top:16px"><div class=card><h3>Covered concepts</h3><ul class=ck id=r-cov></ul></div>'
         '<div class=card><h3>Missed concepts</h3><ul class=ck id=r-mis></ul></div></div>'
         '<div class=grid style="margin-top:12px"><div class=card><h3>Structure</h3><ul class=ck id=r-struct></ul></div>'
         '<div class=card id=r-logic-wrap hidden><h3>Directional logic</h3><ul class=ck id=r-logic></ul></div></div>'
         '<h3>What to improve</h3><ol class=tips id=r-tips></ol><p><a id=r-model href="../questions/">See the model answer</a></p>',
         cta_box(), HUMAN, '</section>',
         '<h2>How the score works</h2><p>The rubric is the same for every answer and is shown in full here.</p><table>'
         '<tr><th>Part</th><th>Points</th><th>What is checked</th></tr>'
         '<tr><td>Key concepts</td><td>60 (70 when a question has no logic checks)</td><td>Each question has 6 to 10 required concepts taken from its model answer, each with synonyms. Points are the share of concepts your answer mentions.</td></tr>'
         '<tr><td>Structure</td><td>20</td><td>A definition or direct answer in the first two sentences (7), how it works or why (7), and an example, number or trade-off (6).</td></tr>'
         '<tr><td>Length</td><td>10</td><td>Full points for 80 to 300 words. Fewer points for shorter or much longer answers.</td></tr>'
         '<tr><td>Directional logic (IB)</td><td>10</td><td>For investment banking questions where it applies, key phrases are checked for the right direction, for example that net income falls and cash rises when depreciation goes up, or that a higher WACC lowers value.</td></tr></table>'
         '<p class=muted>Limits: the check matches words and phrases, so it cannot judge whether an explanation is actually correct in every detail, and an answer can score well and still need work. Read the model answer and practice out loud.</p>',
         '<h2>Questions you can check</h2><div class=grid><div class=card><b>AI Engineer</b><ul>'
         + "".join(f'<li><a href="../questions/{q["slug"]}/">{e(q["q"])}</a></li>' for q in d["tracks"]["aie"]["questions"]) +
         '</ul></div><div class=card><b>Investment Banking</b><ul>'
         + "".join(f'<li><a href="{IB_SITE}/questions/{q["slug"]}/">{e(q["q"])}</a></li>' for q in d["tracks"]["ib"]["questions"]) +
         '</ul></div></div>',
         cta_box(), '</main>',
         '<div class=w><footer>&copy; 2026 Valenx Press &middot; <a href="../">All 100 AI engineer interview questions</a> &middot; '
         f'<a href="{IB_SITE}/">All 100 investment banking interview questions</a> &middot; Questions reflect common public interview patterns; no company affiliation. '
         'Scores are a self-check for practice, not a prediction of any interview outcome.</footer></div>',
         '<script type="application/json" id=ac-data>' + json.dumps(d, ensure_ascii=False).replace("</", "<\\/") + '</script>',
         '<script id=ac-engine>' + JS + '</script><script>' + UI + '</script></body></html>\n']
    out = "".join(o)
    os.makedirs(os.path.join(ROOT, "answer-check"), exist_ok=True)
    open(os.path.join(ROOT, "answer-check", "index.html"), "w").write(out)
    print("wrote answer-check/index.html", len(out), "bytes")


if __name__ == "__main__":
    build()

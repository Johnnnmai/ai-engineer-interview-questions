#!/usr/bin/env python3
"""Generate /answer-check/index.html, the free Interview Answer Self-Check (pure client-side JS).

Run from the repo root:  python3 tools/build_answer_check.py
Rubric data lives in tools/answer_check_data.py; AIE titles come from tools/question_pages_data.py.
"""
import html, json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from question_pages_data import PAGES
import answer_check_data as D

from urllib.parse import urlsplit
from build_question_pages import (PROMO_HTML, PROMO_SHORT, CTA_URL, OFFER_EXPIRES, PROMO_ON, PROMO_TEXT, PRICE, PRODUCT_NAME, CTA_LABEL, CTA_HEADLINE, CTA_TEXT,
                                   CTA_BUTTON, PM_URL, PM_LEAD, PM_LINK_TEXT, PM_POST, head, foot, icons,
                                   TIER9_URL, IB_TIER9_URL, TIER9_UTM, TIER9_LEAD, TIER9_LINK_TEXT, TIER9_POST, IB_TIER9_LINK_TEXT, IB_TIER9_POST)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://johnnnmai.github.io/ai-engineer-interview-questions"
IB_SITE = "https://johnnnmai.github.io/investment-banking-interview-questions"
URL = f"{SITE}/answer-check/"
# Paid links reuse the offer query of CTA_URL (tools/build_question_pages.py), so clearing OFFER_CODE there clears it here.
OFFER_Q = urlsplit(CTA_URL).query
AIE_BUY = CTA_URL.split("?")[0]   # primary for the AI engineer track: the AI engineer playbook
PM_BUY = PM_URL.split("?")[0]      # secondary text link on the AI engineer track only: the PM direction bundle
# Primary for the IB track: the free IB Top 30 product (Gumroad, $0+). No offer code on a free product.
IB_BUY = "https://sirjohnnymai.gumroad.com/l/ib-top-30-questions"
IB_FREE_NAME = "IB Interview: Top 30 Questions"
TOOL_UTM = "utm_source=tool&utm_medium=answercheck&utm_campaign={track}"


def track_url(base, track, offer=True, utm=TOOL_UTM):
    return base + "?" + "&".join(x for x in ((OFFER_Q if offer else ""), utm.format(track=track)) if x)


def tier9(track):
    """$9 scoring rubric for the track: a secondary text link next to the primary CTA. URL and UTM come from build_question_pages."""
    base, name, post = (TIER9_URL, TIER9_LINK_TEXT, TIER9_POST) if track == "aie" else (IB_TIER9_URL, IB_TIER9_LINK_TEXT, IB_TIER9_POST)
    return {"url": base + ("&" if "?" in base else "?") + TIER9_UTM, "pre": TIER9_LEAD, "name": name, "post": post}


def track_ctas(track, utm=TOOL_UTM):
    """Primary CTA plus one secondary text link per track. Shared with the mock-interview page."""
    if track == "aie":
        return {"url": track_url(AIE_BUY, "aie", utm=utm), "label": CTA_LABEL, "head": CTA_HEADLINE, "text": CTA_TEXT,
                "btn": CTA_BUTTON, "promo": PROMO_ON,
                "alt": {"url": track_url(PM_BUY, "aie", utm=utm), "pre": PM_LEAD, "name": PM_LINK_TEXT, "post": PM_POST, "promo": False}, "tier9": tier9("aie")}
    # IB track: free Top 30 only. No paid CTA here (the PM bundle is not IB prep).
    return {"url": track_url(IB_BUY, "ib", offer=False, utm=utm), "label": "Free guide", "head": "Start with the free IB Top 30",
            "text": f"{IB_FREE_NAME} covers the 30 most-asked investment banking interview questions with model answers. 13 pages, free on Gumroad.",
            "btn": "Get the free Top 30", "promo": False, "alt": None, "tier9": tier9("ib")}


TITLE = "Check My Interview Answer: Free Interview Answer Self-Check"
DESC = ("Check my interview answer for free: paste your answer to an AI engineer or investment banking "
        "interview question and get a 0 to 100 rubric score, missed concepts and tips.")
e = html.escape
CSS = """<style>
.ac fieldset{border:0;margin:0 0 var(--s3);padding:0}.ac legend,.ac label.lb{display:block;font-weight:600;margin-bottom:var(--s1)}
.seg{display:flex;flex-wrap:wrap;gap:var(--s1)}.seg label{display:flex;align-items:center;gap:var(--s1);background:var(--surface);border:1px solid var(--line);border-radius:var(--r-pill);padding:10px 16px;cursor:pointer;font-weight:600}
.seg input{width:18px;height:18px;accent-color:var(--ink)}.seg label:has(input:checked){border-color:var(--ink);box-shadow:inset 0 0 0 1px var(--ink)}
.ac select,.ac textarea{width:100%;font:inherit;font-size:1rem;border:1px solid var(--line);border-radius:var(--r-sm);padding:12px;background:var(--surface);color:var(--ink)}
.ac textarea{min-height:220px;resize:vertical;line-height:1.55}.ac select:focus,.ac textarea:focus,.ac button:focus-visible,.seg input:focus-visible{outline:2px solid var(--pop);outline-offset:2px}
.ac .row{margin:0 0 var(--s3)}.hint{font-size:var(--fs-small);color:var(--ink-2);margin:6px 0 0}.err{color:#b42318}
.ac button.btn{cursor:pointer;font:inherit}
#result{margin-top:var(--s6)}#result[hidden]{display:none}
.scorebox{display:flex;flex-wrap:wrap;gap:var(--s3);align-items:center;background:var(--ink);color:var(--bg);border-radius:var(--r-md);padding:var(--s4)}
.big{font-family:var(--font-serif);font-size:4rem;line-height:1}.big small{font-family:var(--font-sans);font-size:1rem;opacity:.7}
.band{font-weight:700;font-size:1.15rem}.scorebox p{margin:4px 0 0;opacity:.85;font-size:var(--fs-small)}.body .scorebox p,.body .scorebox li{color:var(--bg)}.scorebox ul.ck li{border-color:rgba(255,255,255,.18)}#r-head:focus{outline:none}
.meter{height:8px;background:rgba(255,255,255,.18);border-radius:var(--r-pill);overflow:hidden;flex-basis:100%}.meter span{display:block;height:100%;background:var(--pop)}
.gap{display:grid;gap:var(--s3);grid-template-columns:repeat(auto-fit,minmax(260px,1fr));margin-top:var(--s3)}
.gap .card h3{margin:0 0 var(--s1);font-size:1.05rem}.gap .card.miss{border-color:var(--ink)}
ul.ck{list-style:none;padding:0;margin:var(--s1) 0}ul.ck li{padding:8px 0 8px 32px;position:relative;border-bottom:1px solid var(--line)}ul.ck li:last-child{border-bottom:0}
ul.ck li:before{position:absolute;left:0;top:8px;width:22px;height:22px;border-radius:50%;text-align:center;font-weight:700;line-height:22px;font-size:.8rem}
ul.ck li.ok:before{content:'\\2713';background:#d1fadf;color:#05603a}ul.ck li.no:before{content:'\\2717';background:#fee4e2;color:#912018}ul.ck li.mid:before{content:'?';background:#fef0c7;color:#93370d}
ul.ck li .inpb{display:block;font-size:var(--fs-small);color:var(--ink-2)}
.gapbuy{margin-top:var(--s2);padding-top:var(--s2);border-top:1px solid var(--line)}.gapbuy[hidden]{display:none}.gapbuy p{margin:0 0 var(--s2);font-size:var(--fs-small);color:var(--ink-2)}
.body .gapbuy a.btn-primary{color:var(--accent-ink)}
.vh{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}ol.tips li{margin:8px 0}
.human{font-size:var(--fs-small);color:var(--ink-2);margin-top:var(--s2)}
table.rub{width:100%;border-collapse:collapse;font-size:var(--fs-small)}table.rub th,table.rub td{text-align:left;vertical-align:top;padding:10px 8px;border-bottom:1px solid var(--line)}
.qcols{display:grid;gap:var(--s3);grid-template-columns:repeat(auto-fit,minmax(280px,1fr))}.qcols ul{padding-left:1.1em;margin:var(--s1) 0 0}.qcols li{margin:4px 0;font-size:var(--fs-small)}
@media (max-width:560px){.big{font-size:3rem}.seg label{flex:1 1 100%}table.rub{font-size:.85rem}}
</style>"""


def concepts(lst):
    return [{"label": c[0], "rx": c[1], "min": (c[2] if len(c) > 2 else 1)} for c in lst]


def ib_title(q):
    return re.sub(r"\s*\((investment banking|IB) interview\)$", "", q)


def data():
    aie = []
    for p in PAGES:
        if p["slug"] not in D.AIE:
            continue
        r = D.AIE[p["slug"]]
        aie.append({"slug": p["slug"], "q": p["q"], "level": p["level"], "model": f"../questions/{p['slug']}/",
                    "followup": p["followups"][0][0] if p["followups"] else "", "concepts": concepts(r["concepts"]), "logic": []})
    ib = []
    for slug, r in D.IB.items():
        ib.append({"slug": slug, "q": ib_title(r["q"]), "model": f"{IB_SITE}/questions/{slug}/", "followup": D.IB_FOLLOWUPS.get(slug, ""),
                   "concepts": concepts(r["concepts"]), "logic": r.get("logic", [])})
    assert len(aie) == len(PAGES) == 50 and len(ib) == 50, (len(aie), len(ib))
    tracks = {
        "aie": {"name": "AI Engineer", "questions": aie,
                "cta": track_ctas("aie")},
        "ib": {"name": "Investment Banking", "questions": ib,
               "cta": track_ctas("ib")},
    }
    return {"tracks": tracks, "offerExpires": OFFER_EXPIRES if PROMO_ON else "", "promoText": PROMO_TEXT}


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
// lower-case only an ordinary first word; keep acronyms (IRR, EV/EBITDA, QLoRA), numbers and names as written
function lowerFirst(s){var w=s.split(/[\s:,]/)[0];if(/[A-Z0-9$]/.test(w.slice(1))||/^(Gordon)$/.test(w))return s;return s.charAt(0).toLowerCase()+s.slice(1);}
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
 if(wrongDir){total=Math.min(total,59);notes.push("Check the direction of the effect. Score capped at 59 because at least one direction looks reversed.");}
 if(repeated){total=Math.min(total,Math.round(60*uniqRatio));notes.push("Much of the answer repeats itself. Score reduced; say each point once.");}
 if(n>600)notes.push("Over 600 words gets no length points. A spoken answer is usually 80 to 300 words.");
 if(thin&&n>0)notes.push("Concept points halved: the answer is short or mostly keywords. Use full sentences, at least about 60 words.");
 // tips: wrong logic first, then missed concepts, structure, length, missing logic, follow-up
 var tips=[];
 lg.forEach(function(c){if(c.status==="bad")tips.push("Check your direction: "+c.tip);});
 cs.filter(function(c){return c.covered===false;}).slice(0,2).forEach(function(c){tips.push("Add this point from the model answer: "+lowerFirst(c.label)+".");});
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
function ctaHref(t,content,alt){var c=DATA.tracks[t].cta;var u=new URL(alt==="tier9"?c.tier9.url:alt?c.alt.url:c.url);u.searchParams.set("utm_content",content);if(visitorSrc)u.searchParams.set("utm_term",visitorSrc);return u.toString();}
var offerOn=!!DATA.offerExpires&&Date.now()<Date.parse(DATA.offerExpires);
function fillAlt(p,t,content){var c=DATA.tracks[t].cta.alt;if(!p)return;p.innerHTML="";p.hidden=!c;if(!c)return;p.appendChild(document.createTextNode(c.pre));
  var a=document.createElement("a");a.href=ctaHref(t,content,true);a.textContent=c.name;p.appendChild(a);
  p.appendChild(document.createTextNode(c.post+(c.promo&&offerOn?" "+DATA.promoText+".":"")));}
function fillTier9(p,t,content){var c=DATA.tracks[t].cta.tier9;if(!p)return;p.innerHTML="";p.hidden=!c;if(!c)return;p.appendChild(document.createTextNode(c.pre));
  var a=document.createElement("a");a.href=ctaHref(t,content,"tier9");a.textContent=c.name;p.appendChild(a);p.appendChild(document.createTextNode(c.post));}
function fillCta(t){var c=DATA.tracks[t].cta;document.querySelectorAll(".ac-cta").forEach(function(box){
  box.querySelector(".label").textContent=c.label;
  box.querySelector(".cta-h").textContent=c.head;box.querySelector(".cta-t").textContent=c.text;
  var a=box.querySelector("a.btn");a.firstChild.textContent=c.btn+" ";a.href=ctaHref(t,"cta_box");
  var o=box.querySelector(".promo");if(o)o.hidden=!(offerOn&&c.promo);fillTier9(box.querySelector(".tier9"),t,"answercheck_cta_box");fillAlt(box.querySelector(".alt-buy:not(.tier9)"),t,"cta_box_alt");});
  fillTier9($("r-tier9"),t,"answercheck_result");
  var g=$("r-gap-buy");if(g){g.firstChild.textContent=c.btn+" ";g.href=ctaHref(t,"answercheck_gap");}
  var gp=$("r-gap-promo");if(gp)gp.hidden=!(offerOn&&c.promo);}
function fillQuestions(t,slug){sel.innerHTML="";DATA.tracks[t].questions.forEach(function(q){var o=document.createElement("option");o.value=q.slug;o.textContent=q.q;sel.appendChild(o);});
  if(slug&&AC.find(DATA,t,slug))sel.value=slug;}
function syncUrl(){var u=new URL(location.href);u.searchParams.set("track",track());u.searchParams.set("q",sel.value);history.replaceState(null,"",u.toString());}
function li(cls,text,tagText){var l=document.createElement("li");l.className=cls;l.textContent=text;if(tagText){var s=document.createElement("span");s.className="vh";s.textContent=" ("+tagText+")";l.appendChild(s);}return l;}
function render(r,q){
  $("r-score").textContent=String(r.total);$("r-band").textContent=r.band;$("r-meter").style.width=r.total+"%";
  $("r-sum").textContent="Concepts "+r.conceptPts+"/"+r.conceptMax+" \u00b7 Structure "+r.structurePts+"/20 \u00b7 Length "+r.lengthPts+"/10 ("+r.words+" words)"+(r.logicMax?" \u00b7 Logic "+r.logicPts+"/10":"");
  var nt=$("r-notes");if(nt){nt.innerHTML="";(r.notes||[]).forEach(function(x){nt.appendChild(li("no",x));});nt.hidden=!(r.notes&&r.notes.length);}
  var cov=$("r-cov"),mis=$("r-mis");cov.innerHTML="";mis.innerHTML="";
  var nMis=0;r.concepts.forEach(function(c){if(c.covered){cov.appendChild(li("ok",c.label,"covered"));}else{nMis++;var l=li("no",c.label,"missed");
    var s=document.createElement("span");s.className="inpb";s.textContent="In the model answer";l.appendChild(s);mis.appendChild(l);}});
  if(cov.children.length===0)cov.appendChild(li("no","None of the key concepts were detected yet.","none"));
  if(nMis===0)mis.appendChild(li("ok","Nothing missed. Every key concept was detected.","none missed"));
  $("r-ncov").textContent=String(r.concepts.length-nMis);$("r-nmis").textContent=String(nMis);$("r-gap").hidden=(nMis===0);
  var st=$("r-struct");st.innerHTML="";r.structure.forEach(function(s){st.appendChild(li(s.ok?"ok":"no",s.part,s.ok?"present":"missing"));});
  var lw=$("r-logic-wrap"),lg=$("r-logic");lg.innerHTML="";lw.hidden=(r.logic.length===0);
  r.logic.forEach(function(c){var lab={ok:"correct",bad:"check the direction",missing:"not stated"}[c.status];lg.appendChild(li(c.status==="ok"?"ok":c.status==="bad"?"no":"mid",c.label+": "+lab));});
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


ARROW = '<span class=dot aria-hidden=true>&rarr;</span>'


def promo_span(extra=""):
    return f'<span class="badge promo"{extra}>{PROMO_HTML}</span>' if PROMO_ON else ""


def tier9_p(t, content, pid=""):
    return (f'<p class="alt-buy tier9"{pid}>{e(t["pre"])}<a href="{e(t["url"])}&amp;utm_content={content}">{e(t["name"])}</a>{e(t["post"])}</p>')


def cta_box():
    c = data()["tracks"]["aie"]["cta"]
    a = c["alt"]
    return (f'<div class="cta ac-cta"><span class=label>{e(c["label"])}</span><b class=cta-h>{e(c["head"])}</b><p class=cta-t>{e(c["text"])}</p>'
            f'<a class="btn btn-primary" href="{e(c["url"])}&amp;utm_content=cta_box">{e(c["btn"])} {ARROW}</a>{promo_span()}'
            f'{tier9_p(c["tier9"], "answercheck_cta_box")}'
            f'<p class=alt-buy>{e(a["pre"])}<a href="{e(a["url"])}&amp;utm_content=cta_box_alt">{e(a["name"])}</a>{e(a["post"])}</p></div>')


def build():
    d = data()
    aie_cta = d["tracks"]["aie"]["cta"]
    ld = {"@context": "https://schema.org", "@type": "WebApplication", "name": "Interview Answer Self-Check", "url": URL,
          "description": DESC, "applicationCategory": "EducationalApplication", "operatingSystem": "Any",
          "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}}
    ld_tag = '<script type="application/ld+json">' + json.dumps(ld) + "</script>"
    first_aie = "".join(f'<option value="{q["slug"]}">{e(q["q"])}</option>' for q in d["tracks"]["aie"]["questions"])
    h = head(TITLE, DESC, URL, "../", ld_tag + CSS).replace('<meta property="og:type" content="article">', '<meta property="og:type" content="website">')
    o = [h,
         '<header class=qhero data-hero><div class=wrap><div class="crumb label"><a href="../">AI Engineer Interview Questions</a> / <a href="../questions/">Questions</a> / Answer Self-Check</div>'
         '<span class=badge>Free tool</span><h1>Check my interview answer: free Interview Answer Self-Check</h1>'
         '<p class=lead>Pick an AI engineer or investment banking question, paste your answer, and get a 0 to 100 score from a transparent rubric: '
         'which key concepts you covered and missed, whether the structure works, and two or three concrete fixes. It runs in your browser; your answer is not sent anywhere.</p></div></header>',
         '<main id=main class=body><div class="read ac">',
         '<form id=ac-form novalidate aria-describedby=ac-note>'
         '<fieldset class=row><legend>1. Track</legend><div class=seg>'
         '<label for=t-aie><input type=radio name=track id=t-aie value=aie checked> AI Engineer</label>'
         '<label for=t-ib><input type=radio name=track id=t-ib value=ib> Investment Banking</label></div></fieldset>'
         f'<div class=row><label class=lb for=ac-q>2. Question</label><select id=ac-q name=q>{first_aie}</select></div>'
         '<div class=row><label class=lb for=ac-answer>3. Your answer</label>'
         '<textarea id=ac-answer name=answer maxlength=6000 spellcheck=true aria-describedby="ac-hint ac-err" placeholder="Type or paste the answer you would give out loud."></textarea>'
         '<p class=hint id=ac-hint>Aim for what you would say in one to two minutes, roughly 80 to 300 words (6,000 characters max).</p><p class="hint err" id=ac-err role=alert></p></div>'
         f'<div class=acts><button class="btn btn-primary" type=submit>Check my answer {ARROW}</button><button class="btn btn-ghost" type=button id=ac-clear>Clear</button></div>'
         '<p class=hint id=ac-note>A keyword and structure check against the model answer, not a verdict from an interviewer. Use it to find gaps, then practice out loud.</p></form>',
         '<section id=result hidden aria-live=polite aria-labelledby=r-head>'
         '<h2 id=r-head tabindex=-1>Your result</h2><div class=scorebox><div class=big><span id=r-score>0</span><small> / 100</small></div>'
         '<div><div class=band id=r-band></div><p id=r-sum></p><ul class=ck id=r-notes hidden></ul></div><div class=meter aria-hidden=true><span id=r-meter style="width:0"></span></div></div>'
         + tier9_p(aie_cta["tier9"], "answercheck_result", " id=r-tier9") +
         '<div class=gap><div class=card><h3>Covered concepts (<span id=r-ncov>0</span>)</h3><ul class=ck id=r-cov></ul></div>'
         '<div class="card miss"><h3>Missed concepts (<span id=r-nmis>0</span>)</h3><ul class=ck id=r-mis></ul>'
         '<div class=gapbuy id=r-gap hidden><p>Each missed concept is spelled out in the model answer for this question. Read it, then try again out loud.</p>'
         f'<div class=acts><a class="btn btn-primary" id=r-gap-buy href="{e(aie_cta["url"])}&amp;utm_content=answercheck_gap">{e(aie_cta["btn"])} {ARROW}</a>'
         f'{promo_span(" id=r-gap-promo")}</div></div></div></div>'
         '<div class=gap><div class=card><h3>Structure</h3><ul class=ck id=r-struct></ul></div>'
         '<div class=card id=r-logic-wrap hidden><h3>Directional logic</h3><ul class=ck id=r-logic></ul></div></div>'
         '<h3>What to improve</h3><ol class=tips id=r-tips></ol><p><a id=r-model href="../questions/">See the model answer</a></p>',
         cta_box(), HUMAN, '</section>',
         '<h2>How the score works</h2><p>The rubric is the same for every answer and is shown in full here.</p><table class=rub>'
         '<tr><th>Part</th><th>Points</th><th>What is checked</th></tr>'
         '<tr><td>Key concepts</td><td>60 (70 when a question has no logic checks)</td><td>Each question has 3 to 10 required concepts taken from its model answer, each with synonyms. Points are the share of concepts your answer mentions.</td></tr>'
         '<tr><td>Structure</td><td>20</td><td>A definition or direct answer in the first two sentences (7), how it works or why (7), and an example, number or trade-off (6).</td></tr>'
         '<tr><td>Length</td><td>10</td><td>Full points for 80 to 300 words. Fewer points for shorter or much longer answers.</td></tr>'
         '<tr><td>Directional logic (IB)</td><td>10</td><td>For investment banking questions where it applies, key phrases are checked for the right direction, for example that net income falls and cash rises when depreciation goes up, or that a higher WACC lowers value.</td></tr></table>'
         '<p class=muted>Limits: the check matches words and phrases, so it cannot judge whether an explanation is actually correct in every detail, and an answer can score well and still need work. Read the model answer and practice out loud.</p>',
         '<h2>Questions you can check</h2><div class=qcols><div><b>AI Engineer (' + str(len(d["tracks"]["aie"]["questions"])) + ')</b><ul>'
         + "".join(f'<li><a href="../questions/{q["slug"]}/">{e(q["q"])}</a></li>' for q in d["tracks"]["aie"]["questions"]) +
         '</ul></div><div><b>Investment Banking (' + str(len(d["tracks"]["ib"]["questions"])) + ')</b><ul>'
         + "".join(f'<li><a href="{IB_SITE}/questions/{q["slug"]}/">{e(q["q"])}</a></li>' for q in d["tracks"]["ib"]["questions"]) +
         '</ul></div></div>',
         cta_box(),
         f'<p class=muted>Scores are a self-check for practice, not a prediction of any interview outcome. <a href="{IB_SITE}/">All 100 investment banking interview questions</a>.</p>',
         '</div></main>',
         '<script type="application/json" id=ac-data>' + json.dumps(d, ensure_ascii=False).replace("</", "<\\/") + '</script>',
         '<script id=ac-engine>' + JS + '</script><script>' + UI + '</script>',
         foot("../").replace("</body>", '<script defer src="https://static.cloudflareinsights.com/beacon.min.js" data-cf-beacon=\'{"token": "39575a8acd6a48f2836dbd5df6db3c40"}\'></script></body>')]
    out = "".join(o)
    os.makedirs(os.path.join(ROOT, "answer-check"), exist_ok=True)
    open(os.path.join(ROOT, "answer-check", "index.html"), "w").write(out)
    print("wrote answer-check/index.html", len(out), "bytes")


if __name__ == "__main__":
    build()

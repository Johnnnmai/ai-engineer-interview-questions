#!/usr/bin/env python3
"""Generate the Chinese mirror (line 20): /zh/ index plus one page per question for the first 20 questions.

Reuses the site design (assets/valenx.css), the UTM passthrough and the single OFFER_CODE constant
from build_question_pages.py. Run after build_question_pages.py; it also makes sure the /zh/ URLs are
in sitemap.xml (idempotent).
"""
import json
import os
from html import escape as e

import build_question_pages as B
from question_pages_data import PAGES
from zh_mirror_data import LEVEL_ZH, ZH_PAGES, ZH_URLS, zh_alternates

ROOT = B.ROOT
SITE = B.SITE
# Single offer switch lives in build_question_pages.OFFER_CODE; empty string turns the promo off here too.
OFFER_CODE = B.OFFER_CODE
OFFER_Q = f"?offer_code={OFFER_CODE}" if OFFER_CODE else ""
PROMO_ON = bool(OFFER_CODE and PROMO_TEXT)
UTM = "utm_source=site&utm_medium=zh_mirror&utm_campaign=line20_20261101"

ZH_URL = "https://valenx.org/get/ai-engineer-interview-zh" + OFFER_Q
ZH_NAME = "如何从0到1准备AI Engineer面试"
ZH_PRICE = "$9.99"  # list price on the live Gumroad product page, Nov 1 2026
ZH_SPEC = "20 章、5 套答题框架（FLAME、SPARK、FORGE、RISE、EMBER）、100 道题库和 8 周备考计划"  # from the product cover
EN_URL = "https://valenx.org/kit" + OFFER_Q
EN_PRICE = B.PRICE
FREE_URL = "https://valenx.org/get/aie-top-30-questions"
PROMO_TEXT = ""  # zh promo copy; set together with B.OFFER_CODE for a future offer
ZH_STICKY_LONG = ""
ZH_STICKY_SHORT = ""
ARROW = B.ARROW
EN_BY_SLUG = {p["slug"]: p for p in PAGES}

ZH_CSS = ('<style>html[lang="zh-CN"] body{line-height:1.8}'
          'html[lang="zh-CN"] .qhero h1{letter-spacing:0;line-height:1.22;max-width:22ch}'
          'html[lang="zh-CN"] h2,html[lang="zh-CN"] .pcard h2{letter-spacing:0;line-height:1.3}'
          '.zh-en{margin:-8px 0 var(--s3);color:var(--ink-2);font-size:var(--fs-small)}'
          '.zh-en a{color:var(--ink-2)}.zh-deduct{padding:var(--s3);border:1px solid var(--line);border-radius:var(--r-md);background:var(--bg-soft)}'
          '.zh-pn{display:flex;justify-content:space-between;gap:var(--s2);flex-wrap:wrap;margin:var(--s4) 0}'
          'html[lang="zh-CN"] .pcard img{transform:none;max-width:100%;border-radius:10px}'
          'html[lang="zh-CN"] .bignum em{font-family:var(--font-sans);font-style:normal;font-weight:500;letter-spacing:0}'
          'html[lang="zh-CN"] .badge,html[lang="zh-CN"] .label{letter-spacing:.04em}'
          '.qcard b,.qcard span.d{overflow-wrap:anywhere}</style>')


def url_for(base, content, utm=UTM):
    return base + ("&" if "?" in base else "?") + utm + "&utm_content=" + content


def promo(cls="badge promo"):
    return f'<span class="{cls}">{PROMO_TEXT}</span>' if PROMO_ON else ""


def free_link(content):
    return f'<a href="{e(url_for(FREE_URL, content))}">免费领取 Top 30 题 PDF（英文）</a>'


def secondary(content):
    return (f'<p class=alt-buy>更想读英文版？<a href="{e(url_for(EN_URL, content))}">The 0&rarr;1 AI Engineer Interview Playbook</a>'
            f'，{EN_PRICE}，Gumroad 英文版。也可以先{free_link(content + "_free")}。</p>')


def hero_buy(tag, ghost_href, ghost_text):
    return (f'<div class=acts><a class="btn btn-primary" href="{e(url_for(ZH_URL, tag + "_hero"))}">获取中文手册 {ARROW}</a>'
            f'<a class="btn btn-ghost" href="{ghost_href}">{ghost_text}</a></div>'
            f'<p class=price-line><span>中文手册 <span class=num>{ZH_PRICE}</span>，Gumroad 即时下载</span>{promo()}</p>')


def cta(tag, content):
    return (f'<div class=cta><span class=label>中文手册</span><b>想要完整的中文备考方法？</b>'
            f'<p>《{ZH_NAME}》：{ZH_SPEC}。</p>'
            f'<a class="btn btn-primary" href="{e(url_for(ZH_URL, tag + "_" + content))}">获取中文手册 {ARROW}</a>{promo()}'
            f'{secondary(tag + "_" + content + "_en")}</div>')


def sticky(tag):
    deal = f'<span class="long promo"> &middot; {ZH_STICKY_LONG}</span>' if PROMO_ON else f'<span class=long> &middot; {ZH_PRICE}</span>'
    short = f'<span class="short promo"> &middot; {ZH_STICKY_SHORT}</span>' if PROMO_ON else f'<span class=short> &middot; {ZH_PRICE}</span>'
    return (f'<div class=sticky-cta role=complementary aria-label="购买中文手册" aria-hidden=true>'
            f'<span class=t><b><span class=full>{ZH_NAME}</span><span class=short>中文手册</span></b>{deal}{short}</span>'
            f'<a class=btn href="{e(url_for(ZH_URL, tag + "_sticky_bar"))}">获取 &rarr;</a></div>')


def preview_card(tag, rel):
    return (f'<li><div class=pcard><img src="{rel}zh/assets/zh-cover.webp" width=1005 height=566 loading=lazy '
            f'alt="《{ZH_NAME}》中文手册封面，2026 版，Valenx Press">'
            f'<div><span class=label>中文手册 &middot; 2026 版</span><h2>{ZH_NAME}</h2><p>{ZH_SPEC}。</p>'
            f'<ul class=spec><li><span>出版</span><span>Valenx Press</span></li>'
            f'<li><span>格式</span><span>Gumroad 电子版下载</span></li>'
            f'<li><span>价格</span><span>{ZH_PRICE}</span></li></ul>'
            f'<div class=acts><a class="btn btn-primary" href="{e(url_for(ZH_URL, tag + "_preview_card"))}">获取中文手册 {ARROW}</a>{promo()}</div>'
            f'{secondary(tag + "_preview_card_en")}</div></div></li>')


def tools_list(rel, slug=None):
    ac = f"{rel}answer-check/" + (f"?track=aie&amp;q={slug}" if slug else "")
    return (f'<li><a href="{ac}">免费答案自查：粘贴英文回答，30 秒得到分数和遗漏的要点</a></li>'
            f'<li><a href="{rel}mock-interview/">计时模拟面试（英文）</a></li>'
            f'<li><a href="{rel}study-plan/">按面试日期生成逐日学习计划（英文）</a></li>'
            f'<li><a href="{rel}llm-cost-calculator/">LLM API 成本计算器（英文）</a></li>'
            f'<li><a href="{rel}alternatives/">AI 工程师面试备考资料对比（英文）</a></li>'
            f'<li>{free_link("tools_list")}</li>')


def head(title, desc, url, rel, alt, extra=""):
    until = f' data-offer-until="{B.OFFER_EXPIRES}"' if PROMO_ON else ""
    return (f'<!doctype html><html lang=zh-CN{until}><head><meta charset=utf-8>'
            f'<meta name=viewport content="width=device-width,initial-scale=1">'
            f'<title>{e(title)}</title><meta name=description content="{e(desc)}">'
            f'<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}">'
            f'<meta property="og:type" content="article"><meta property="og:url" content="{url}"><meta property="og:locale" content="zh_CN">'
            f'<meta property="og:image" content="{SITE}/zh/assets/zh-cover.jpg"><meta name="twitter:card" content="summary_large_image">'
            f'<link rel=canonical href="{url}">{alt}{B.icons(rel)}<link rel=preconnect href="https://fonts.googleapis.com">'
            f'<link rel=preconnect href="https://fonts.gstatic.com" crossorigin><link rel=stylesheet href="{rel}assets/valenx.css">{ZH_CSS}{extra}</head>'
            f'<body><a class=skip href="#main">跳到正文</a>'
            f'<nav class=nav aria-label="站点"><a class=brand href="{rel}zh/"><span class=mark>VP</span>Valenx Press<span class=long>&nbsp;&middot; AI 工程师面试题中文版</span></a>'
            f'<div class=nav-group><a href="{rel}zh/">中文题目</a><a href="{rel}answer-check/">答案自查</a><a class=hide-sm href="{rel}questions/">English</a></div></nav>')


def foot(rel):
    return (f'<footer class=site><div class=wrap>&copy; 2026 Valenx Press &middot; <a href="{rel}zh/">AI 工程师面试题中文版</a> &middot; '
            f'<a href="{rel}questions/">English question deep dives</a> &middot; <a href="{rel}">All 100 questions</a> &middot; '
            f'免费工具：<a href="{rel}answer-check/">答案自查</a> &middot; <a href="{rel}study-plan/">学习计划</a> &middot; '
            f'<a href="{rel}llm-cost-calculator/">LLM 成本计算器</a> &middot; <a href="{rel}mock-interview/">模拟面试</a> &middot; '
            f'题目整理自公开的常见面试题型，与任何公司无关联。</div></footer>'
            f'{B.UTM_SCRIPT}{B.UI_SCRIPT}</body></html>\n')


def page(i, p):
    slug = p["slug"]
    en = EN_BY_SLUG[slug]
    url = f"{SITE}/zh/{slug}/"
    rel = "../../"
    tag = "zh_" + slug
    fq, fa = p["followup"]
    faq = [{"@type": "Question", "name": p["zh"], "acceptedAnswer": {"@type": "Answer", "text": " ".join(p["answer"])}},
           {"@type": "Question", "name": fq, "acceptedAnswer": {"@type": "Answer", "text": fa}}]
    ld = {"@context": "https://schema.org", "@type": "FAQPage", "inLanguage": "zh-CN", "mainEntity": faq}
    ld_tag = '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False).replace("</", "<\\/") + "</script>"
    ac = f"{rel}answer-check/?track=aie&amp;q={slug}"
    lvl = B.LVL[p["level"]]
    o = [head(f"{p['zh']}{'' if p['zh'].endswith('？') else '：'}评分要点与参考回答 | AI 工程师面试题中文版", p["desc"], url, rel, zh_alternates(slug), ld_tag)]
    o.append(f'<header class=qhero data-hero><div class=wrap><div class="crumb label"><a href="../">AI 工程师面试题中文版</a> / 第 {i} 题</div>'
             f'<span class="lvl {lvl}">{LEVEL_ZH[p["level"]]}</span><h1>{e(p["zh"])}</h1>'
             f'<p class=zh-en>英文原题：<a href="{rel}questions/{slug}/" hreflang=en lang=en>{e(en["q"])}</a></p>'
             f'<p class=lead>先口头作答，再对照评分要点给自己打 1 到 5 分。下面是评分要点、常见扣分点、参考回答和追问。</p>'
             + hero_buy(tag, ac, "免费自查我的回答") + '</div></header>')
    o.append('<main id=main class=body><div class=read>')
    o.append(f'<p class=selfcheck><b>练完一遍了？</b> <a href="{ac}">用英文写下回答，粘贴到免费自查工具打分</a>（工具按英文要点评分）</p>')
    o.append(f'<h2>考察点</h2><p>{e(p["testing"])}</p>')
    o.append('<h2>评分要点</h2><ol class=steps>' + "".join(f"<li>{e(s)}</li>" for s in p["points"]) + "</ol>")
    o.append(f'<h2>常见扣分点</h2><p class=zh-deduct>{e(p["deduct"])}</p>')
    o.append('<h2>参考回答</h2><div class=sample>' + "".join(f"<p class=ans>{e(s)}</p>" for s in p["answer"]) + "</div>")
    o.append(f'<h2>常见追问</h2><div class=fu><b>{e(fq)}</b> {e(fa)}</div>')
    o.append(cta(tag, "cta_box"))
    prev_p = ZH_PAGES[i - 2] if i > 1 else None
    next_p = ZH_PAGES[i] if i < len(ZH_PAGES) else None
    o.append('<div class=zh-pn>' + (f'<a href="../{prev_p["slug"]}/">&larr; 上一题：{e(prev_p["zh"])}</a>' if prev_p else '<span></span>')
             + (f'<a href="../{next_p["slug"]}/">下一题：{e(next_p["zh"])} &rarr;</a>' if next_p else '') + '</div>')
    o.append('<h2>相关链接</h2><ul class=related>'
             f'<li><a href="{rel}questions/{slug}/" hreflang=en>阅读英文原文：{e(en["q"])}</a></li>'
             + tools_list(rel, slug) +
             f'<li><a href="../">全部 20 道中文题目</a></li><li><a href="{rel}">All 100 AI engineer interview questions（英文）</a></li></ul>')
    o.append('</div></main>' + sticky(tag))
    o.append(foot(rel))
    return "".join(o)


def index():
    url = f"{SITE}/zh/"
    rel = "../"
    tag = "zh_index"
    title = "AI 工程师面试题中文版：20 道核心题的评分要点与参考回答"
    desc = ("20 道 AI 工程师面试题的中文版：RAG、Transformer、KV cache、LoRA、LLM 评估、Agent、prompt injection 等，"
            "每题附评分要点、常见扣分点、参考回答和追问。")
    cnt = {k: sum(1 for p in ZH_PAGES if p["level"] == k) for k in LEVEL_ZH}
    o = [head(title + " | Valenx Press", desc, url, rel, zh_alternates(None))]
    o.append(f'<header class="qhero idx" data-hero><div class=wrap><div class="crumb label"><a href="../">AI Engineer Interview Questions</a> / 中文版</div>'
             f'<span class=bignum aria-hidden=true>20<em>道中文题</em></span><h1>{e(title)}</h1>'
             '<p class=lead>先用自己的话把答案说出来，再对照评分要点给自己打 1 到 5 分。低于 3 分的题，读参考回答后隔天重答。</p>'
             + hero_buy(tag, "../answer-check/", "免费自查我的回答") +
             '<div class=chips>' + "".join(f'<span class="lvl {B.LVL[k]}">{LEVEL_ZH[k]} {cnt[k]} 题</span>' for k in LEVEL_ZH) +
             '<span class=chip>每题附英文原题链接</span></div></div></header>')
    o.append('<main id=main class=body><div class=read>')
    o.append('<p class=selfcheck><b>练完一遍了？</b> <a href="../answer-check/">用英文写下回答，粘贴到免费自查工具打分</a>（工具按英文要点评分）</p>')
    o.append('<ol class=qlist>')
    for i, p in enumerate(ZH_PAGES, 1):
        o.append(f'<li><a class=qcard href="{p["slug"]}/"><span class=n>{i:02d}</span><span class="lvl {B.LVL[p["level"]]}">{LEVEL_ZH[p["level"]]}</span>'
                 f'<b>{e(p["zh"])}</b><span class=d lang=en>{e(EN_BY_SLUG[p["slug"]]["q"])}</span></a></li>')
        if i == 3:
            o.append(preview_card(tag, rel))
    o.append('</ol>')
    o.append('<h2>免费工具</h2><ul class=related>' + tools_list(rel) + '</ul>')
    o.append(f'<p><a href="../questions/" hreflang=en>English version: AI engineer interview question deep dives</a></p>')
    o.append(cta(tag, "cta_box") + '</div></main>' + sticky(tag))
    o.append(foot(rel))
    return "".join(o)


def add_to_sitemap():
    """Make sure every /zh/ URL is in sitemap.xml (idempotent, keeps all existing entries)."""
    path = os.path.join(ROOT, "sitemap.xml")
    sm = open(path).read()
    add = "".join(f"  <url><loc>{u}</loc><lastmod>{B.LASTMOD}</lastmod></url>\n" for u in ZH_URLS if f"<loc>{u}</loc>" not in sm)
    if add:
        sm = sm.replace("</urlset>", add + "</urlset>")
        open(path, "w").write(sm)
    return len(ZH_URLS)


def main():
    d = os.path.join(ROOT, "zh")
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "index.html"), "w").write(index())
    for i, p in enumerate(ZH_PAGES, 1):
        pd = os.path.join(d, p["slug"])
        os.makedirs(pd, exist_ok=True)
        open(os.path.join(pd, "index.html"), "w").write(page(i, p))
    n = add_to_sitemap()
    print(f"built zh index + {len(ZH_PAGES)} zh pages, {n} zh urls in sitemap")


if __name__ == "__main__":
    main()

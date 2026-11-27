/* Valenx Press BF30 top bar. CRO 2026-11-27. Self-expires Mon Nov 30 11:59 PM PT (2026-12-01T07:59Z).
   No cookies, no storage, no tracking beyond the UTM on the link. Dismiss hides it for this page view only. */
(function () {
  var END = Date.parse("2026-12-01T07:59:00Z");
  if (Date.now() >= END || document.getElementById("vx-bf30")) return;
  var page = (location.pathname || "/").replace(/[^a-z0-9/_-]/gi, "").slice(0, 60) || "home";
  var href = "https://valenx.org/go/bf-bundle?utm_source=aie.valenx.org&utm_medium=site&utm_campaign=bf30_202611&utm_content=topbar" +
    encodeURIComponent(page.replace(/\//g, "_"));
  var bar = document.createElement("div");
  bar.id = "vx-bf30";
  bar.setAttribute("role", "region");
  bar.setAttribute("aria-label", "Black Friday offer");
  bar.style.cssText = "position:sticky;top:0;z-index:9999;display:flex;gap:12px;align-items:center;justify-content:center;" +
    "flex-wrap:wrap;padding:10px 14px;background:#111827;color:#fff;font:600 14px/1.35 system-ui,-apple-system,Segoe UI,Roboto,sans-serif;text-align:center";
  var t = document.createElement("span");
  t.textContent = "Black Friday: 30% off all interview playbooks with code BF30. Ends Mon Nov 30, 11:59 PM PT.";
  var a = document.createElement("a");
  a.href = href;
  a.textContent = "Get the 3-playbook bundle for $20.30 \u2192";
  a.style.cssText = "background:#facc15;color:#111827;padding:6px 12px;border-radius:6px;text-decoration:none;white-space:nowrap";
  var x = document.createElement("button");
  x.type = "button";
  x.setAttribute("aria-label", "Dismiss");
  x.textContent = "\u00d7";
  x.style.cssText = "background:none;border:0;color:#9ca3af;font-size:18px;cursor:pointer;padding:0 4px";
  x.onclick = function () { bar.remove(); };
  bar.appendChild(t); bar.appendChild(a); bar.appendChild(x);
  document.body.insertBefore(bar, document.body.firstChild);
})();

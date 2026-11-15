// First-party visit counter for aie.valenx.org guide pages.
// Sends path, referrer host and utm_* to https://valenx.org/aie-pv.
// No cookies, no storage, no IP. Skipped when Global Privacy Control or Do Not Track is on.
// Failures are ignored so a down counter never breaks the page.
(function () {
  try {
    var n = navigator;
    if (n.globalPrivacyControl === true || n.doNotTrack === "1" || window.doNotTrack === "1") return;
    var l = window.location, q = new URLSearchParams(l.search), d = { path: l.pathname.slice(0, 300) };
    try { if (document.referrer) d.ref = new URL(document.referrer).hostname.slice(0, 200); } catch (e) {}
    ["utm_source", "utm_medium", "utm_campaign", "utm_content", "utm_term"].forEach(function (k) { var v = q.get(k); if (v) d[k] = v.slice(0, 120); });
    if (q.get("pv_test") === "1") d.t = 1;
    var body = JSON.stringify(d);
    var url = "https://valenx.org/aie-pv";
    if (n.sendBeacon) { n.sendBeacon(url, new Blob([body], { type: "text/plain" })); }
    else if (window.fetch) { fetch(url, { method: "POST", body: body, keepalive: true, credentials: "omit", headers: { "content-type": "text/plain" }, mode: "cors" }).catch(function () {}); }
  } catch (e) {}
})();

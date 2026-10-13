"use strict";
// New Year sale: 60% off the 14-lesson course until Jan 1, 2027 00:00 PT.
// After the end time the page reverts to regular pricing automatically.
(() => {
  const END = Date.parse("2027-01-01T00:00:00-08:00");
  const active = () => Date.now() < END;
  window.COURSE_SALE = Object.freeze({ end: END, isActive: active, salePrice: "400", regularPrice: "1,000" });

  // CSS defaults to regular pricing when JavaScript is absent. Mark JavaScript as
  // active before toggling the dated sale elements.
  document.documentElement.classList.add("sale-js-active");

  function apply() {
    const on = active();
    document.querySelectorAll("[data-sale-on]").forEach((el) => { el.hidden = !on; });
    document.querySelectorAll("[data-sale-off]").forEach((el) => { el.hidden = on; });
    return on;
  }
  function tick() {
    if (!apply()) { clearInterval(timer); document.dispatchEvent(new Event("salechange")); return; }
    let s = Math.floor((END - Date.now()) / 1000);
    const d = Math.floor(s / 86400); s %= 86400;
    const h = Math.floor(s / 3600); s %= 3600;
    const m = Math.floor(s / 60); s %= 60;
    const txt = d + "d " + String(h).padStart(2, "0") + "h " + String(m).padStart(2, "0") + "m " + String(s).padStart(2, "0") + "s left";
    document.querySelectorAll("[data-sale-countdown]").forEach((el) => { el.textContent = txt; });
  }
  let timer = null;
  const start = () => { tick(); if (active()) timer = setInterval(tick, 1000); };
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start); else start();
})();

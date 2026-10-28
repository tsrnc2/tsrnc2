"use strict";
// Single source of truth for contact details. To set the phone number site-wide run:
//   sed -i 's/GOOGLE_VOICE_NUMBER/(503) 555-0100/g; s/GOOGLE_VOICE_TEL/+15035550100/g' *.html site-config.js
// Static HTML copies are marked with data-phone / data-phone-tel so the page works without JS.
window.SITE_CONFIG = Object.freeze({
  phoneDisplay: "GOOGLE_VOICE_NUMBER",
  phoneTel: "GOOGLE_VOICE_TEL",
  email: "Jacob.W.Wood.cs@gmail.com"
});
(() => {
  const c = window.SITE_CONFIG;
  const ready = c.phoneDisplay !== "GOOGLE_VOICE_" + "NUMBER";
  document.querySelectorAll("[data-phone]").forEach((el) => {
    if (!ready) { el.closest("[data-phone-wrap]")?.setAttribute("hidden", ""); return; }
    el.textContent = c.phoneDisplay;
    if (el.tagName === "A") el.href = "tel:" + c.phoneTel;
  });
})();

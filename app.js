"use strict";
// Pages remain functional without JavaScript. This script only enhances small presentation details.
document.querySelectorAll("[data-year]").forEach((element) => {
  element.textContent = String(new Date().getFullYear());
});

// Preserve the current query string and fragment when switching to Basic HTML.
document.querySelectorAll("[data-view-switch]").forEach((link) => {
  try {
    const target = new URL(link.getAttribute("href"), window.location.href);
    target.search = window.location.search;
    target.hash = window.location.hash;
    link.href = target.href;
  } catch {
    // Relative links still work if URL construction is unavailable.
  }
});

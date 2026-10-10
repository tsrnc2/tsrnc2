"use strict";
(() => {
  const products = Object.freeze({
    single: Object.freeze({
      title: "Single C/C++ Lesson",
      price: "100",
      subtitle: "1 × 60-minute one-on-one lesson · USD",
      description: "One private C/C++ lesson tailored to your current level, code, compiler/toolchain, and goals.",
      emailLabel: "Email about this lesson"
    }),
    course: Object.freeze({
      title: "14-Lesson C/C++ Course",
      price: "1,000",
      subtitle: "14 × 60-minute one-on-one lessons · USD",
      description: "A structured 14-session C/C++ systems course with progressive instruction, real-code exercises, debugging, tooling, architecture, and a final capstone review.",
      emailLabel: "Email about the course"
    })
  });
  const button = document.getElementById("checkoutButton");
  const status = document.getElementById("checkoutStatus");
  const radios = [...document.querySelectorAll('input[name="product"]')];
  if (!button || !status || radios.length !== 2) return;

  const owns = (object, key) => Object.prototype.hasOwnProperty.call(object, key);
  let selected = "single";

  // URL validation is a safety boundary, not verification of a Stripe product or price.
  // The payment provider remains authoritative for amount, currency, tax, and payment status.
  function paymentURL(key) {
    const links = window.CHECKOUT_LINKS;
    if (!links || !owns(links, key) || typeof links[key] !== "string") return null;
    const raw = links[key].trim();
    if (!raw || /[\\\u0000-\u0020\u007f]/.test(raw)) return null;
    try {
      const url = new URL(raw);
      if (url.protocol !== "https:" || url.hostname !== "buy.stripe.com" ||
          url.username || url.password || url.port ||
          !/^\/[A-Za-z0-9_]+$/.test(url.pathname)) return null;
      return url;
    } catch {
      return null;
    }
  }

  function refreshCheckoutState() {
    const url = paymentURL(selected);
    button.disabled = !url;
    button.hidden = !url;
    status.classList.toggle("ready", Boolean(url));
    if (!url) {
      status.textContent = "Email Jacob to check availability and order this plan.";
    } else if (url.pathname.startsWith("/test_")) {
      button.textContent = "Open Stripe test checkout";
      status.textContent = "Test mode: this link opens Stripe’s test checkout. It does not accept real payments.";
    } else {
      button.textContent = "Continue to secure online checkout";
      status.textContent = "Secure online checkout is available. You’ll leave this site for Stripe; confirm the plan, amount, and currency before paying.";
    }
  }

  function selectProduct(key, updateURL = false) {
    selected = owns(products, key) ? key : "single";
    const product = products[selected];
    document.getElementById("productTitle").textContent = product.title;
    document.getElementById("productPrice").textContent = product.price;
    document.getElementById("productSubtitle").textContent = product.subtitle;
    document.getElementById("productDescription").textContent = product.description;
    document.getElementById("productSavings").hidden = selected !== "course";
    const email = document.getElementById("bookingEmail");
    email.textContent = product.emailLabel;
    email.href = "mailto:Jacob.w.wood.cs@gmail.com?subject=" + encodeURIComponent(product.title + " inquiry");
    radios.forEach((radio) => { radio.checked = radio.value === selected; });
    refreshCheckoutState();
    if (updateURL) {
      try {
        const url = new URL(window.location.href);
        url.searchParams.set("product", selected);
        // replaceState avoids adding a history entry for every radio-button change.
        window.history.replaceState(null, "", url.href);
      } catch {
        // Local file viewers can deny History API calls; ordering still works.
      }
    }
  }

  function selectFromURL() {
    const key = new URLSearchParams(window.location.search).get("product");
    selectProduct(key);
  }

  radios.forEach((radio) => radio.addEventListener("change", () => {
    if (radio.checked) selectProduct(radio.value, true);
  }));
  window.addEventListener("popstate", selectFromURL);
  button.addEventListener("click", () => {
    const url = paymentURL(selected);
    if (!url) {
      refreshCheckoutState();
      return;
    }
    // User-initiated navigation only. Never mark a purchase as paid in this page.
    window.location.assign(url.href);
  });
  selectFromURL();
})();

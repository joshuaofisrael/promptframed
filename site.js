(function () {
  document.querySelectorAll("[data-copy]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var el = document.getElementById(btn.getAttribute("data-copy"));
      if (!el) return;
      var text = el.innerText.replace(/\u00a0/g, " ").replace(/\n$/, "");
      var previous = btn.textContent;
      btn.textContent = "Copied";
      window.setTimeout(function () { btn.textContent = previous; }, 1600);
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).catch(function () { copyFallback(text); });
      } else {
        copyFallback(text);
      }
    });
  });

  var form = document.querySelector("[data-mailto]");
  if (form) {
    form.addEventListener("submit", function (event) {
      event.preventDefault();
      var name = document.getElementById("name").value.trim();
      var email = document.getElementById("email").value.trim();
      var message = document.getElementById("message").value.trim();
      var subject = encodeURIComponent("Prompt Framed — " + name);
      var body = encodeURIComponent(message + "\n\nFrom: " + name + " <" + email + ">");
      window.location.href = "mailto:" + form.getAttribute("data-mailto") + "?subject=" + subject + "&body=" + body;
    });
  }

  // Deep links such as buy.html#moonlit-alpine-meadow: highlight the piece and
  // bring its buy buttons into view once images have laid out.
  function focusHashTarget() {
    var id = decodeURIComponent((window.location.hash || "").slice(1));
    if (!id) return;
    var el = document.getElementById(id);
    if (!el) return;
    document.querySelectorAll(".is-target").forEach(function (n) { n.classList.remove("is-target"); });
    el.classList.add("is-target");
    el.scrollIntoView({ block: "start" });
  }
  window.addEventListener("hashchange", focusHashTarget);
  window.addEventListener("load", focusHashTarget);

  // Buy buttons are plain <a href> links to Stripe Payment Links, written into
  // the HTML by scripts/apply_stripe_links.py. products.json is only used here
  // to keep them in sync if a link is replaced before the pages are regenerated.
  var src = document.body.getAttribute("data-products");
  if (!src || !window.fetch) return;
  fetch(src)
    .then(function (response) { return response.json(); })
    .then(function (list) {
      var bySlug = {};
      (Array.isArray(list) ? list : []).forEach(function (item) { bySlug[item.slug] = item; });
      document.querySelectorAll("[data-buy]").forEach(function (el) {
        var item = bySlug[el.getAttribute("data-buy")];
        if (!item) return;
        var url = shopUrlFor(item, el.getAttribute("data-sku"));
        if (isShopUrl(url)) el.href = url;
      });
    })
    .catch(function () {});

  function shopUrlFor(item, sku) {
    var stripe = item.stripe || {};
    if (sku === "framed") return stripe.framedUrl || null;
    if (sku === "mural") return stripe.muralUrl || null;
    return stripe.posterUrl || null;
  }

  function isShopUrl(url) {
    return typeof url === "string" && /^https:\/\/buy\.stripe\.com\/[A-Za-z0-9]+$/.test(url.trim());
  }

  function copyFallback(text) {
    var area = document.createElement("textarea");
    area.value = text;
    area.setAttribute("readonly", "");
    area.style.position = "fixed";
    area.style.left = "-9999px";
    document.body.appendChild(area);
    area.select();
    try { document.execCommand("copy"); } catch (err) {}
    area.remove();
  }
})();

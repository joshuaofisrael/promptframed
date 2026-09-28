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

  var src = document.body.getAttribute("data-products");
  if (!src) return;
  fetch(src)
    .then(function (response) { return response.json(); })
    .then(function (list) {
      var bySlug = {};
      (Array.isArray(list) ? list : []).forEach(function (item) { bySlug[item.slug] = item; });
      document.querySelectorAll("[data-buy]").forEach(function (el) {
        var item = bySlug[el.getAttribute("data-buy")];
        if (!item) return;
        var sku = el.getAttribute("data-sku");
        var url = shopUrlFor(item, sku);
        if (!isShopUrl(url)) return;
        el.href = url;
        el.target = "_blank";
        el.rel = "noopener noreferrer";
        var status = document.getElementById("buy-status");
        if (status && sku === "poster") {
          status.textContent = "Buy Poster opens checkout in a new tab. Prompt Framed does not take a card on this page.";
        }
      });
    })
    .catch(function () {});

  function shopUrlFor(item, sku) {
    var stripe = item.stripe || {};
    var printful = item.printful || {};
    if (sku === "framed") {
      return stripe.framedUrl || printful.framedUrl || null;
    }
    return stripe.posterUrl || printful.posterUrl || null;
  }

  function isShopUrl(url) {
    if (typeof url !== "string") return false;
    url = url.trim();
    if (!/^https:\/\//i.test(url)) return false;
    if (/example\.com|placeholder|your-?store|TODO|CHANGEME|printful\.me\/?$/i.test(url)) return false;
    return true;
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

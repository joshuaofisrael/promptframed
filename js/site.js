(function () {
  var toggle = document.querySelector("[data-nav-toggle]");
  var nav = document.querySelector("[data-nav]");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

  document.querySelectorAll("[data-copy]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var el = document.getElementById(btn.getAttribute("data-copy"));
      if (!el) return;
      var text = el.innerText.replace(/\u00a0/g, " ").replace(/\n$/, "");
      var previous = btn.textContent;
      btn.textContent = "Copied";
      window.setTimeout(function () {
        btn.textContent = previous;
      }, 1600);
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).catch(function () {
          copyFallback(text);
        });
      } else {
        copyFallback(text);
      }
    });
  });

  var form = document.querySelector("[data-mailto]");
  if (form) {
    form.addEventListener("submit", function (event) {
      event.preventDefault();
      var to = form.getAttribute("data-mailto");
      var name = document.getElementById("name").value.trim();
      var email = document.getElementById("email").value.trim();
      var message = document.getElementById("message").value.trim();
      var subject = encodeURIComponent("Prompt Framed — " + name);
      var body = encodeURIComponent(message + "\n\nFrom: " + name + " <" + email + ">");
      window.location.href = "mailto:" + to + "?subject=" + subject + "&body=" + body;
    });
  }

  var productsUrl = document.body.getAttribute("data-products");
  if (!productsUrl) return;

  fetch(productsUrl)
    .then(function (response) {
      if (!response.ok) throw new Error("products");
      return response.json();
    })
    .then(function (data) {
      wireInstagram(data.instagram || {});
      wireBuy(data.pieces || {});
    })
    .catch(function () {});

  function wireInstagram(instagram) {
    var handle = instagram.handle || "@placeholder";
    var url = (instagram.url || "").trim();
    document.querySelectorAll("[data-ig-handle]").forEach(function (el) {
      el.textContent = "";
      var live = /^https:\/\/(www\.)?instagram\.com\//i.test(url) && !/placeholder/i.test(handle);
      if (!live) {
        el.textContent = handle;
        return;
      }
      var link = document.createElement("a");
      link.href = url;
      link.target = "_blank";
      link.rel = "noopener noreferrer";
      link.textContent = handle;
      el.appendChild(link);
    });
  }

  function wireBuy(pieces) {
    var posterLive = false;
    document.querySelectorAll("[data-buy]").forEach(function (el) {
      var piece = pieces[el.getAttribute("data-buy")] || {};
      var product = piece[el.getAttribute("data-sku")] || {};
      var url = (product.url || "").trim();
      if (!isShopUrl(url)) return;
      el.href = url;
      el.target = "_blank";
      el.rel = "noopener noreferrer";
      if (product.label) el.textContent = product.label;
      if (el.getAttribute("data-sku") === "poster") posterLive = true;
    });
    var status = document.getElementById("buy-status");
    if (status && posterLive) {
      status.textContent = "Buy Poster opens the print shop in a new tab. Prompt Framed does not take a card on this page. The shop prints the poster and ships it.";
    }
  }

  function isShopUrl(url) {
    if (!/^https:\/\//i.test(url)) return false;
    if (/example\.com|placeholder|your-?store|TODO|CHANGEME/i.test(url)) return false;
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
    document.execCommand("copy");
    area.remove();
  }
})();

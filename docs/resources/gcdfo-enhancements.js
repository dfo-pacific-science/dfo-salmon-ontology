(function () {
  "use strict";

  var STORAGE = {
    tocWidth: "gcdfo.toc.width",
    tocOpen: "gcdfo.toc.open",
    tocScroll: "gcdfo.toc.scroll",
  };

  function onReady(fn) {
    if (document.readyState === "complete") {
      fn();
      return;
    }
    window.addEventListener("load", fn, { once: true });
  }

  function isDesktop() {
    return window.matchMedia && window.matchMedia("(min-width: 901px)").matches;
  }

  function clamp(num, min, max) {
    return Math.max(min, Math.min(max, num));
  }

  function setTocWidth(width) {
    var safe = clamp(Math.round(width), 260, 760);
    document.documentElement.style.setProperty("--gcdfo-toc-width", safe + "px");
    document.documentElement.style.setProperty("--gcdfo-toc-space", safe + 64 + "px");
    try {
      localStorage.setItem(STORAGE.tocWidth, String(safe));
    } catch (_e) {}
  }

  function applyStoredTocWidth() {
    try {
      var raw = localStorage.getItem(STORAGE.tocWidth);
      if (!raw) return;
      var parsed = parseInt(raw, 10);
      if (isNaN(parsed)) return;
      setTocWidth(parsed);
    } catch (_e) {}
  }

  function enhanceTocPersistence() {
    var panel = document.querySelector(".gcdfo-toc-panel");
    var toc = document.getElementById("toc");
    if (!panel || !toc) return;

    applyStoredTocWidth();

    if (window.ResizeObserver) {
      var ro = new ResizeObserver(function (entries) {
        if (!isDesktop() || !entries || !entries[0]) return;
        setTocWidth(entries[0].contentRect.width || panel.getBoundingClientRect().width);
      });
      ro.observe(panel);
    }

    if (!panel.querySelector(".gcdfo-toc-desktop-actions")) {
      var actions = document.createElement("div");
      actions.className = "gcdfo-toc-desktop-actions";

      var hideBtn = document.createElement("button");
      hideBtn.type = "button";
      hideBtn.className = "gcdfo-toc-desktop-hide";
      hideBtn.textContent = "Hide TOC";
      hideBtn.addEventListener("click", function () {
        document.body.classList.add("gcdfo-toc-collapsed");
        try {
          localStorage.setItem(STORAGE.tocOpen, "0");
        } catch (_e) {}
      });

      actions.appendChild(hideBtn);
      panel.insertBefore(actions, panel.firstChild);
    }

    var reopen = document.querySelector(".gcdfo-toc-desktop-reopen");
    if (!reopen) {
      reopen = document.createElement("button");
      reopen.type = "button";
      reopen.className = "gcdfo-toc-desktop-reopen";
      reopen.textContent = "Show TOC";
      reopen.addEventListener("click", function () {
        document.body.classList.remove("gcdfo-toc-collapsed");
        try {
          localStorage.setItem(STORAGE.tocOpen, "1");
        } catch (_e) {}
      });
      document.body.appendChild(reopen);
    }

    try {
      var openState = localStorage.getItem(STORAGE.tocOpen);
      if (openState === "0" && isDesktop()) {
        document.body.classList.add("gcdfo-toc-collapsed");
      }
    } catch (_e) {}

    if (!panel.dataset.gcdfoScrollBound) {
      panel.dataset.gcdfoScrollBound = "1";
      var scTimer = null;
      panel.addEventListener("scroll", function () {
        if (!isDesktop()) return;
        if (scTimer) window.clearTimeout(scTimer);
        scTimer = window.setTimeout(function () {
          try {
            localStorage.setItem(STORAGE.tocScroll, String(panel.scrollTop || 0));
          } catch (_e) {}
        }, 120);
      });
    }

    try {
      var savedScroll = parseInt(localStorage.getItem(STORAGE.tocScroll) || "0", 10);
      if (!isNaN(savedScroll) && savedScroll > 0 && isDesktop()) {
        panel.scrollTop = savedScroll;
      }
    } catch (_e) {}

    window.addEventListener("resize", function () {
      if (!isDesktop()) {
        document.body.classList.remove("gcdfo-toc-collapsed");
      } else {
        try {
          if (localStorage.getItem(STORAGE.tocOpen) === "0") {
            document.body.classList.add("gcdfo-toc-collapsed");
          }
        } catch (_e) {}
      }
    });
  }

  function chooseTargets() {
    var targets = [
      { id: "overv", label: "Overview" },
      { id: "classes-headline", label: "Classes" },
      { id: "objectproperties", label: "Object properties" },
      { id: "skos", label: "SKOS" },
      { id: "WSPBiologicalStatusZone", label: "WSP terms" },
      { id: "changes", label: "Changelog" },
    ];
    return targets.filter(function (t) {
      return !!document.getElementById(t.id);
    });
  }

  function enhanceQuickJumps() {
    var head = document.querySelector(".head");
    if (!head || head.querySelector(".gcdfo-quick-jumps")) return;
    var anchors = chooseTargets();
    if (!anchors.length) return;

    var nav = document.createElement("nav");
    nav.className = "gcdfo-quick-jumps";
    nav.setAttribute("aria-label", "Quick jumps");

    anchors.forEach(function (t) {
      var a = document.createElement("a");
      a.className = "gcdfo-chip";
      a.href = "#" + t.id;
      a.textContent = t.label;
      nav.appendChild(a);
    });

    var h2 = head.querySelector("h2");
    if (h2 && h2.parentNode) {
      h2.insertAdjacentElement("afterend", nav);
    } else {
      head.appendChild(nav);
    }
  }

  function fuzzySubsequenceScore(query, text) {
    var qi = 0;
    var ti = 0;
    var steps = 0;
    while (qi < query.length && ti < text.length) {
      if (query[qi] === text[ti]) qi += 1;
      ti += 1;
      steps += 1;
    }
    if (qi !== query.length) return 0;
    return Math.max(1, 60 - Math.floor((steps - query.length) / 2));
  }

  function makeFuzzySearch() {
    if (typeof window.gcdfoBuildSearchIndex !== "function") return;

    window.gcdfoSearchTerms = function (query) {
      var q = (query || "").trim().toLowerCase();
      if (!q) return [];
      var tokens = q.split(/\s+/).filter(Boolean);
      var items = window.gcdfoBuildSearchIndex();

      var scored = items
        .map(function (item) {
          var hay = (item.label + " " + item.id + " " + (item.iri || "")).toLowerCase();
          var score = 0;

          if (hay.indexOf(q) !== -1) {
            score += 200 - Math.min(150, hay.indexOf(q));
          }

          for (var i = 0; i < tokens.length; i++) {
            var t = tokens[i];
            var idx = hay.indexOf(t);
            if (idx !== -1) {
              score += 140 - Math.min(120, idx);
            } else {
              var fuzzy = fuzzySubsequenceScore(t, hay);
              if (!fuzzy) {
                score = 0;
                break;
              }
              score += fuzzy;
            }
          }

          return { item: item, score: score };
        })
        .filter(function (x) {
          return x.score > 0;
        })
        .sort(function (a, b) {
          if (b.score !== a.score) return b.score - a.score;
          return a.item.label.localeCompare(b.item.label);
        })
        .map(function (x) {
          return x.item;
        });

      return scored;
    };
  }

  function highlightSearchMatches(query) {
    var entities = Array.prototype.slice.call(document.querySelectorAll(".entity"));
    entities.forEach(function (e) {
      e.classList.remove("gcdfo-match");
    });

    var q = (query || "").trim();
    if (q.length < 2 || typeof window.gcdfoSearchTerms !== "function") return;

    var matches = window.gcdfoSearchTerms(q).slice(0, 120);
    matches.forEach(function (m) {
      var el = document.getElementById(m.id);
      if (el) el.classList.add("gcdfo-match");
    });
  }

  function enhanceSearchUX() {
    makeFuzzySearch();

    var input = document.getElementById("gcdfo-search");
    if (!input) return;

    if (!document.body.dataset.gcdfoSlashBound) {
      document.body.dataset.gcdfoSlashBound = "1";
      document.addEventListener("keydown", function (e) {
        if (e.key !== "/") return;
        var tag = (e.target && e.target.tagName) ? e.target.tagName.toLowerCase() : "";
        var editable = e.target && (e.target.isContentEditable || tag === "input" || tag === "textarea" || tag === "select");
        if (editable) return;
        e.preventDefault();
        input.focus();
        input.select();
      });
    }

    if (!input.dataset.gcdfoHighlightBound) {
      input.dataset.gcdfoHighlightBound = "1";
      input.addEventListener("input", function () {
        highlightSearchMatches(input.value);
      });
      input.addEventListener("keydown", function (e) {
        if (e.key === "Enter") {
          var top = document.querySelector("#gcdfo-search-results a[href^='#']");
          if (top) {
            top.click();
          }
        }
      });
    }
  }

  function markLegacyTerms() {
    var legacyTargets = Array.prototype.slice.call(document.querySelectorAll(".scheme h3, .entity h3"));
    legacyTargets.forEach(function (h3) {
      var text = (h3.textContent || "").toLowerCase();
      if (text.indexOf("legacy") === -1) return;
      if (!h3.querySelector(".gcdfo-badge-legacy")) {
        var badge = document.createElement("span");
        badge.className = "gcdfo-badge-legacy";
        badge.textContent = "Legacy";
        h3.appendChild(document.createTextNode(" "));
        h3.appendChild(badge);
      }

      var parent = h3.closest(".scheme, .entity");
      if (!parent || parent.querySelector(".gcdfo-legacy-note")) return;

      var note = document.createElement("p");
      note.className = "gcdfo-legacy-note";
      if ((parent.id || "") === "StockStatusZoneScheme" || text.indexOf("stock status zone scheme") !== -1) {
        note.innerHTML = 'Legacy compatibility term. Prefer <a href="#WSPBiologicalStatusZoneScheme">WSPBiologicalStatusZoneScheme</a> for current WSP Red/Amber/Green zone modeling.';
      } else {
        note.textContent = "Legacy compatibility term retained for backward compatibility.";
      }
      parent.insertBefore(note, parent.children[1] || null);
    });
  }

  function isExternalLink(a) {
    if (!a) return false;
    var href = a.getAttribute("href") || "";
    var title = a.getAttribute("title") || "";
    var iri = title || (href.charAt(0) === "#" ? href.slice(1) : href);

    if (!iri) return false;
    if (/^https?:\/\//i.test(iri)) {
      return iri.indexOf("https://w3id.org/gcdfo/salmon#") !== 0;
    }
    if (href.indexOf("#http") === 0) return true;
    return false;
  }

  function collapseExternalImports() {
    var scopes = [document.getElementById("overview"), document.getElementById("crossref")].filter(Boolean);
    scopes.forEach(function (scope) {
      var lists = Array.prototype.slice.call(scope.querySelectorAll("ul.hlist"));
      lists.forEach(function (list, idx) {
        if (!list || list.classList.contains("gcdfo-external-list")) return;
        if (list.dataset.gcdfoExternalProcessed) return;
        var lis = Array.prototype.slice.call(list.children).filter(function (el) { return el.tagName === "LI"; });
        if (!lis.length) return;

        var local = [];
        var external = [];
        lis.forEach(function (li) {
          var a = li.querySelector("a");
          if (isExternalLink(a)) external.push(li);
          else local.push(li);
        });

        if (!external.length || !local.length) {
          list.dataset.gcdfoExternalProcessed = "1";
          return;
        }

        list.innerHTML = "";
        local.forEach(function (li) { list.appendChild(li); });

        var details = document.createElement("details");
        details.className = "gcdfo-external-imports";
        details.setAttribute("data-gcdfo-external-group", "1");

        var summary = document.createElement("summary");
        summary.textContent = "External imports (" + external.length + ")";
        details.appendChild(summary);

        var extList = document.createElement("ul");
        extList.className = "hlist gcdfo-external-list";
        external.forEach(function (li) { extList.appendChild(li); });
        details.appendChild(extList);

        list.insertAdjacentElement("afterend", details);
        list.dataset.gcdfoExternalProcessed = "1";
      });
    });
  }

  function enhanceWebVowlControls() {
    var panel = document.querySelector("details.gcdfo-webvowl");
    if (!panel || panel.querySelector(".gcdfo-webvowl-controls")) return;

    var iframe = panel.querySelector("iframe");
    if (!iframe) return;

    var controls = document.createElement("div");
    controls.className = "gcdfo-webvowl-controls";

    var reloadBtn = document.createElement("button");
    reloadBtn.type = "button";
    reloadBtn.className = "gcdfo-webvowl-reload";
    reloadBtn.textContent = "Reload diagram";

    var fallback = document.createElement("a");
    fallback.className = "gcdfo-webvowl-fallback";
    fallback.href = "webvowl/data/ontology.json";
    fallback.target = "_blank";
    fallback.rel = "noopener noreferrer";
    fallback.textContent = "Open ontology.json";

    var status = document.createElement("span");
    status.className = "gcdfo-webvowl-status";
    status.textContent = "Checking data...";

    reloadBtn.addEventListener("click", function () {
      var base = (iframe.getAttribute("src") || "webvowl/index.html").split("?")[0];
      iframe.setAttribute("src", base + "?t=" + Date.now());
      status.textContent = "Reloaded";
    });

    fetch("webvowl/data/ontology.json", { cache: "no-store" })
      .then(function (r) {
        status.textContent = r.ok ? "ontology.json: OK" : "ontology.json: " + r.status;
      })
      .catch(function () {
        status.textContent = "ontology.json: unavailable";
      });

    controls.appendChild(reloadBtn);
    controls.appendChild(fallback);
    controls.appendChild(status);

    panel.insertBefore(controls, iframe);
  }

  function collapseChangelog() {
    var wrap = document.querySelector("#changelog > #changelog") || document.getElementById("changelog");
    if (!wrap) return;

    var h2 = wrap.querySelector("h2#changes");
    if (!h2) return;
    if (wrap.querySelector(".gcdfo-changelog-collapsible")) return;

    var details = document.createElement("details");
    details.className = "gcdfo-collapsible gcdfo-changelog-collapsible";

    var summary = document.createElement("summary");
    summary.textContent = "Show changelog details";
    details.appendChild(summary);

    var node = h2.nextSibling;
    while (node) {
      var next = node.nextSibling;
      details.appendChild(node);
      node = next;
    }
    h2.insertAdjacentElement("afterend", details);
  }

  function init() {
    enhanceQuickJumps();
    enhanceTocPersistence();
    enhanceSearchUX();
    markLegacyTerms();
    collapseExternalImports();
    enhanceWebVowlControls();
    collapseChangelog();
  }

  onReady(function () {
    window.setTimeout(init, 50);
  });
})();

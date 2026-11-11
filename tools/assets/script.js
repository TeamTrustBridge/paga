/*
 * Paga Engine SDK documentation — progressive enhancement.
 *
 * Every page is fully readable with JavaScript disabled. This file only adds
 * a theme toggle, the mobile navigation, a live filter over the operation
 * reference, and copy-to-clipboard on code blocks.
 */

(function () {
  "use strict";

  var STORAGE_KEY = "paga-docs-theme";

  // Marks the document as scripted, so the stylesheet can hide controls
  // that would not work without JavaScript.
  document.documentElement.classList.add("has-js");

  /* ---------------------------------------------------------------- */
  /* Theme                                                             */
  /* ---------------------------------------------------------------- */

  function storedTheme() {
    try {
      return window.localStorage.getItem(STORAGE_KEY);
    } catch (error) {
      return null;
    }
  }

  function applyTheme(theme) {
    if (theme === "light" || theme === "dark") {
      document.documentElement.setAttribute("data-theme", theme);
    } else {
      document.documentElement.removeAttribute("data-theme");
    }
    var toggle = document.querySelector("[data-theme-toggle]");
    if (toggle) {
      var dark =
        theme === "dark" ||
        (theme !== "light" &&
          window.matchMedia &&
          window.matchMedia("(prefers-color-scheme: dark)").matches);
      toggle.setAttribute("aria-label", dark ? "Switch to the light theme" : "Switch to the dark theme");
      toggle.textContent = dark ? "☀" : "☾";
    }
  }

  function currentTheme() {
    var explicit = document.documentElement.getAttribute("data-theme");
    if (explicit === "light" || explicit === "dark") return explicit;
    return window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches
      ? "dark"
      : "light";
  }

  applyTheme(storedTheme());

  var toggle = document.querySelector("[data-theme-toggle]");
  if (toggle) {
    toggle.addEventListener("click", function () {
      var next = currentTheme() === "dark" ? "light" : "dark";
      try {
        window.localStorage.setItem(STORAGE_KEY, next);
      } catch (error) {
        /* storage is unavailable; the theme still applies for this page */
      }
      applyTheme(next);
    });
  }

  /* ---------------------------------------------------------------- */
  /* Mobile navigation                                                 */
  /* ---------------------------------------------------------------- */

  var menuToggle = document.querySelector("[data-menu-toggle]");
  if (menuToggle) {
    menuToggle.addEventListener("click", function () {
      var open = document.body.getAttribute("data-nav-open") === "true";
      document.body.setAttribute("data-nav-open", open ? "false" : "true");
      menuToggle.setAttribute("aria-expanded", open ? "false" : "true");
    });

    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape") {
        document.body.setAttribute("data-nav-open", "false");
      }
    });
  }

  /* ---------------------------------------------------------------- */
  /* Copy to clipboard                                                 */
  /* ---------------------------------------------------------------- */

  function copyText(text) {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      return navigator.clipboard.writeText(text);
    }
    var area = document.createElement("textarea");
    area.value = text;
    area.setAttribute("readonly", "");
    area.style.position = "absolute";
    area.style.left = "-9999px";
    document.body.appendChild(area);
    area.select();
    try {
      document.execCommand("copy");
    } finally {
      document.body.removeChild(area);
    }
    return Promise.resolve();
  }

  document.addEventListener("click", function (event) {
    var button = event.target.closest("[data-copy]");
    if (!button) return;
    var target = document.querySelector(button.getAttribute("data-copy"));
    if (!target) return;
    var text = target.textContent || "";
    copyText(text).then(function () {
      var original = button.getAttribute("data-label") || button.textContent;
      button.setAttribute("data-label", original);
      button.textContent = "Copied";
      window.setTimeout(function () {
        button.textContent = original;
      }, 1400);
    });
  });

  /* ---------------------------------------------------------------- */
  /* Reference filter                                                  */
  /* ---------------------------------------------------------------- */

  var filterRoot = document.querySelector("[data-filter-root]");
  if (filterRoot) {
    var search = filterRoot.querySelector("[data-filter-search]");
    var buttons = Array.prototype.slice.call(filterRoot.querySelectorAll("[data-filter-section]"));
    var rows = Array.prototype.slice.call(
      filterRoot.querySelectorAll("[data-filter-item]"),
    );
    var empty = filterRoot.querySelector("[data-filter-empty]");
    var activeSection = "all";

    function matches(row, term) {
      if (activeSection !== "all" && row.getAttribute("data-section") !== activeSection) {
        return false;
      }
      if (!term) return true;
      return (row.getAttribute("data-search") || "").indexOf(term) !== -1;
    }

    function apply() {
      var term = search ? search.value.trim().toLowerCase() : "";
      var visible = 0;
      rows.forEach(function (row) {
        var show = matches(row, term);
        row.hidden = !show;
        if (show) visible += 1;
      });
      if (empty) empty.hidden = visible !== 0;
    }

    if (search) {
      search.addEventListener("input", apply);
      document.addEventListener("keydown", function (event) {
        if (event.key === "/" && document.activeElement !== search) {
          event.preventDefault();
          search.focus();
        }
      });
    }

    buttons.forEach(function (button) {
      button.addEventListener("click", function () {
        activeSection = button.getAttribute("data-filter-section");
        buttons.forEach(function (other) {
          other.setAttribute(
            "aria-pressed",
            other === button ? "true" : "false",
          );
        });
        apply();
      });
    });

    apply();
  }

  /* ---------------------------------------------------------------- */
  /* Contents highlighting                                              */
  /* ---------------------------------------------------------------- */

  var toc = document.querySelector(".toc");
  if (toc) {
    var tocLinks = Array.prototype.slice.call(toc.querySelectorAll("a[href^='#']"));
    var targets = tocLinks
      .map(function (link) {
        var id = link.getAttribute("href").slice(1);
        var element = document.getElementById(id);
        return element ? { link: link, element: element } : null;
      })
      .filter(Boolean);

    if (targets.length) {
      var current = null;

      function highlight() {
        // The last target whose top is above the reading line.
        var line = window.scrollY + 120;
        var next = targets[0];
        for (var index = 0; index < targets.length; index += 1) {
          if (targets[index].element.offsetTop <= line) {
            next = targets[index];
          } else {
            break;
          }
        }
        if (next === current) return;
        if (current) current.link.removeAttribute("data-current");
        next.link.setAttribute("data-current", "true");
        current = next;
      }

      highlight();
      window.addEventListener("scroll", highlight, { passive: true });
      window.addEventListener("resize", highlight);
    }
  }
})();

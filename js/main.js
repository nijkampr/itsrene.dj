/* IT'S RENÉ — all client behavior. Progressive enhancement only:
   every feature here has a designed fallback state in the HTML. */
(function () {
  "use strict";

  var reducedMotion = matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- energy rail: fills with scroll depth ---------- */
  var railFill = document.getElementById("railFill");
  if (railFill && !reducedMotion) {
    var railTicking = false;
    var updateRail = function () {
      var max = document.documentElement.scrollHeight - innerHeight;
      railFill.style.height = (max > 0 ? (scrollY / max) * 100 : 0) + "%";
      railTicking = false;
    };
    addEventListener("scroll", function () {
      if (!railTicking) { requestAnimationFrame(updateRail); railTicking = true; }
    }, { passive: true });
    updateRail();
  }

  var getJSON = function (url) {
    return fetch(url).then(function (r) {
      if (!r.ok) throw new Error(url + " " + r.status);
      return r.json();
    });
  };

  /* ---------- stats: baked numbers refreshed from data/stats.json ---------- */
  getJSON("/data/stats.json").then(function (s) {
    var fmt = {
      twitchFollowers: function (v) { return v.toLocaleString("en-US"); },
      hoursStreamed: function (v) { return v + "+"; },
      peakViewers: function (v) { return v + "+"; },
      sets: function (v) { return String(v); },
      yearsStreaming: function () {
        return String(new Date().getFullYear() - s.streamingSince);
      }
    };
    document.querySelectorAll("[data-stat]").forEach(function (el) {
      var key = el.getAttribute("data-stat");
      if (fmt[key] && (key === "yearsStreaming" || s[key] !== undefined)) {
        el.textContent = fmt[key](s[key]);
      }
    });
  }).catch(function () { /* baked values stay */ });

  /* ---------- listen: tracklist, vibe filter, click-to-load player ---------- */
  var listEl = document.getElementById("setList");
  var filterRow = document.getElementById("filterRow");

  if (listEl && filterRow) {
    getJSON("/data/sets.json").then(function (data) {
      var sets = data.sets;
      var countEl = document.getElementById("set-count");
      if (countEl) countEl.textContent = String(sets.length);

      var frag = document.createDocumentFragment();
      sets.forEach(function (set, i) {
        var row = document.createElement("button");
        row.className = "set-row";
        row.type = "button";
        row.dataset.vibe = set.vibe || "";
        row.dataset.index = String(i);
        row.setAttribute("aria-expanded", "false");
        var hot = set.vibe === "hard" || set.vibe === "chaos";
        row.innerHTML =
          '<span class="mono">' + set.date + "</span>" +
          '<span class="title">' + escapeHtml(set.title) + "</span>" +
          '<span class="tag' + (hot ? " tag-hot" : "") + '">' + (set.vibe || "—") + "</span>" +
          '<span class="play-ico" aria-hidden="true">▶</span>';
        row.addEventListener("click", function () { togglePlayer(row, set); });
        frag.appendChild(row);
      });
      listEl.appendChild(frag);
      filterRow.hidden = false;

      filterRow.addEventListener("click", function (e) {
        var btn = e.target.closest(".filter-btn");
        if (!btn) return;
        filterRow.querySelectorAll(".filter-btn").forEach(function (b) {
          b.setAttribute("aria-pressed", b === btn ? "true" : "false");
        });
        var vibe = btn.dataset.vibe;
        listEl.querySelectorAll(".set-row").forEach(function (row) {
          row.style.display = (vibe === "all" || row.dataset.vibe === vibe) ? "" : "none";
        });
        closePlayer();
      });
    }).catch(function () {
      listEl.innerHTML =
        '<p class="noscript-note">Set list failed to load. Everything is on ' +
        '<a href="https://soundcloud.com/itsrene_nl" rel="noopener">SoundCloud</a>.</p>';
    });
  }

  var openSlot = null;
  var openRow = null;

  function closePlayer() {
    if (openSlot) { openSlot.remove(); openSlot = null; }
    if (openRow) { openRow.setAttribute("aria-expanded", "false"); openRow = null; }
  }

  function togglePlayer(row, set) {
    if (openRow === row) { closePlayer(); return; }
    closePlayer();
    var slot = document.createElement("div");
    slot.className = "player-slot";
    var src = "https://w.soundcloud.com/player/?url=" +
      encodeURIComponent(set.permalink) +
      "&color=%234DD6FF&auto_play=true&hide_related=true&show_comments=false&show_user=true&show_reposts=false&show_teaser=false";
    slot.innerHTML =
      '<iframe title="SoundCloud player: ' + escapeHtml(set.title) + '" allow="autoplay" loading="lazy" src="' + src + '"></iframe>' +
      (set.note ? '<p class="mono player-note">' + escapeHtml(set.note) + "</p>" : "");
    row.after(slot);
    row.setAttribute("aria-expanded", "true");
    openSlot = slot;
    openRow = row;
  }

  function escapeHtml(s) {
    return s.replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  /* ---------- played: gig timeline from data/gigs.json ---------- */
  var gigList = document.getElementById("gigList");
  if (gigList) {
    getJSON("/data/gigs.json").then(function (data) {
      var frag = document.createDocumentFragment();
      data.gigs.forEach(function (gig) {
        var row = document.createElement("div");
        row.className = "gig-row" + (gig.type === "irl" ? " is-irl" : "");
        row.innerHTML =
          '<span class="mono">' + (gig.date || "—") + "</span>" +
          '<span class="name">' + escapeHtml(gig.name) + "</span>" +
          '<span class="tag">' + escapeHtml(gig.label) + "</span>";
        frag.appendChild(row);
      });
      gigList.appendChild(frag);
    }).catch(function () { /* noscript fallback text covers it */ });
  }

  /* ---------- live: one decapi check, offline is the designed default ---------- */
  var badge = document.getElementById("liveBadge");
  var liveText = document.getElementById("liveText");
  var twitchCta = document.getElementById("twitchCta");
  if (badge && liveText) {
    var ctrl = new AbortController();
    var timer = setTimeout(function () { ctrl.abort(); }, 3000);
    fetch("https://decapi.me/twitch/uptime/itsrene_nl", { signal: ctrl.signal })
      .then(function (r) { return r.text(); })
      .then(function (text) {
        clearTimeout(timer);
        text = text.trim();
        if (text && text.indexOf("offline") === -1 && text.length < 40) {
          badge.classList.add("is-live");
          liveText.textContent = "Live now · " + text;
          if (twitchCta) twitchCta.textContent = "Watching now →";
        }
      })
      .catch(function () { /* offline state stays — by design */ });
  }
})();

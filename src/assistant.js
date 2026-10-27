/* ═══════════════════════════════════════════════════════════════════
   ALSTON WEALTH — assistant widget

   Two modes, set by the data-mode attribute on the script tag:
     data-mode="month" data-month="09"   the tool pages
     data-mode="router"                  the home page

   After deploying the Worker, replace ENDPOINT below with its URL.
   ═══════════════════════════════════════════════════════════════════ */
(function () {
  var ENDPOINT = "https://alston-assistant.alston-alex.workers.dev";

  var el   = document.currentScript;
  var MODE  = el.getAttribute("data-mode") || "month";
  var MONTH = el.getAttribute("data-month") || "";
  var TITLE = el.getAttribute("data-title") || "";

  /* one id per browser session, so transcripts group into conversations */
  var SESSION = (function () {
    try {
      var s = sessionStorage.getItem("aw_sid");
      if (!s) { s = Math.random().toString(36).slice(2) + Date.now().toString(36); sessionStorage.setItem("aw_sid", s); }
      return s;
    } catch (e) { return "nostore"; }
  })();

  var CSS = `
.awa{border:1px solid #DCD7CC;background:#fff;margin:34px 0}
.awa-h{padding:15px 20px;border-bottom:1px solid #EDEAE3;background:#FCFBF8}
.awa-h b{font-family:var(--u,"Archivo",Helvetica,sans-serif);font-weight:700;font-size:15px;color:#16233A;display:block}
.awa-h span{font-size:13.5px;color:#5E6878;display:block;margin-top:2px}
.awa-b{padding:20px}
.awa-row{display:flex;gap:9px}
.awa-row input{flex:1;padding:12px 13px;border:1px solid #DCD7CC;background:#fff;
  font-family:var(--u,"Archivo",Helvetica,sans-serif);font-size:15.5px;color:#16233A;border-radius:0}
.awa-row input:focus{outline:2px solid #8A5F24;outline-offset:-1px}
.awa-row button{font-family:var(--u,"Archivo",Helvetica,sans-serif);font-weight:600;font-size:14.5px;
  padding:12px 20px;border:1px solid #16233A;background:#16233A;color:#fff;cursor:pointer;border-radius:0;white-space:nowrap}
.awa-row button:hover{background:#8A5F24;border-color:#8A5F24}
.awa-row button:disabled{opacity:.5;cursor:default}
.awa-sug{display:flex;gap:7px;flex-wrap:wrap;margin-top:12px}
.awa-sug button{font-family:var(--u,"Archivo",Helvetica,sans-serif);font-size:13px;padding:7px 12px;
  border:1px solid #DCD7CC;background:#fff;color:#4C5769;cursor:pointer;border-radius:0}
.awa-sug button:hover{border-color:#8A5F24;color:#8A5F24;background:#F5EEE1}
.awa-out{margin-top:18px}
.awa-q{font-family:var(--u,"Archivo",Helvetica,sans-serif);font-weight:600;font-size:14px;color:#5E6878;
  padding-bottom:9px;margin-bottom:13px;border-bottom:1px solid #EDEAE3}
.awa-a{font-size:15.5px;line-height:1.55;color:#16233A;white-space:pre-wrap}
.awa-a p{margin:0 0 10px}
.awa-cta{margin-top:16px;padding-top:14px;border-top:1px solid #EDEAE3;
  display:flex;gap:9px;flex-wrap:wrap;align-items:center}
.awa-cta a{font-family:var(--u,"Archivo",Helvetica,sans-serif);font-weight:600;font-size:14px;
  padding:10px 16px;border:1px solid #16233A;color:#16233A;text-decoration:none;background:#fff}
.awa-cta a:hover{background:#16233A;color:#fff}
.awa-cta a.p{background:#16233A;color:#fff}
.awa-cta a.p:hover{background:#8A5F24;border-color:#8A5F24}
.awa-route{background:#F5EEE1;border-left:3px solid #8A5F24;padding:16px 18px}
.awa-route b{font-family:var(--u,"Archivo",Helvetica,sans-serif);font-size:15px;display:block;margin-bottom:4px;color:#16233A}
.awa-route span{font-size:14.5px;color:#4C5769;line-height:1.5}
.awa-note{margin-top:14px;font-size:12.5px;color:#5E6878;line-height:1.45}
.awa-load{font-size:14.5px;color:#5E6878;font-style:italic}
@media(max-width:600px){.awa-row{flex-direction:column}.awa-row button{width:100%}}
`;

  /* Starter questions, per month. Each one is answerable from that month's
     knowledge — a suggestion the assistant cannot answer makes it look worse
     than saying nothing. */
  var BY_MONTH = {
    "01": ["What counts as guaranteed income?", "How do I work out what I actually spend?", "What is a coverage ratio?"],
    "02": ["Why does the order of returns matter?", "Is the 4% rule reliable?", "What protects against a bad first decade?"],
    "03": ["What is an income floor?", "How much capital does portfolio income need?", "Which account should I spend from first?"],
    "04": ["How much does waiting until 70 add?", "What happens to the survivor's benefit?", "Does working while claiming hurt me?"],
    "05": ["What is the subsidy cliff?", "What income counts toward it?", "When can I enroll in Medicare?"],
    "06": ["What is the widow's penalty?", "Why does the tax bill go up?", "Do beneficiary forms override a will?"],
    "07": ["What is the safe harbor?", "Why is nothing withheld automatically?", "Can I fix a shortfall in December?"],
    "08": ["What is the tax torpedo?", "Why is my real rate higher than my bracket?", "When do conversions not make sense?"],
    "09": ["What does Medicare actually cover?", "Why is the tail the real risk?", "What is an elimination period?"],
    "10": ["What is the out-of-pocket drug cap?", "Why check the formulary every year?", "Can I switch back to Original Medicare?"],
    "11": ["What order should year-end tasks go in?", "What is the wash sale rule?", "When do required distributions start?"],
    "12": ["What should I review at year end?", "Is underspending really a problem?", "Why track this year over year?"]
  };

  var SUGGEST = {
    month: BY_MONTH[MONTH] || ["Explain that in plain terms", "What should I bring to a meeting?"],
    router: ["When should I take Social Security?", "What if one of us needs care?", "Will my money last?", "What about health insurance before 65?"]
  };

  function build() {
    var s = document.createElement("style"); s.textContent = CSS; document.head.appendChild(s);

    var wrap = document.createElement("div");
    wrap.className = "awa";
    wrap.innerHTML =
      '<div class="awa-h"><b>' +
        (MODE === "router" ? "Not sure where to start?" : "Questions about " + (TITLE || "this month") + "?") +
      '</b><span>' +
        (MODE === "router"
          ? "Ask what's on your mind and I'll point you to the right place."
          : "I can explain how any of this works. I can't advise — that's Alex's job.") +
      '</span></div>' +
      '<div class="awa-b">' +
        '<div class="awa-row">' +
          '<input type="text" id="awaQ" placeholder="' +
            (MODE === "router" ? "e.g. what happens if my husband dies first?" : "Ask a question…") +
          '" maxlength="600">' +
          '<button id="awaGo">Ask</button>' +
        '</div>' +
        '<div class="awa-sug" id="awaSug"></div>' +
        '<div class="awa-out" id="awaOut"></div>' +
        '<div class="awa-note">General information only, not personal advice. Conversations are recorded and reviewed.</div>' +
      '</div>';

    return wrap;
  }

  function esc(t) { var d = document.createElement("div"); d.textContent = t; return d.innerHTML; }

  function mount(wrap) {
    var input = wrap.querySelector("#awaQ"),
        go    = wrap.querySelector("#awaGo"),
        out   = wrap.querySelector("#awaOut"),
        sug   = wrap.querySelector("#awaSug");

    (SUGGEST[MODE] || []).forEach(function (t) {
      var b = document.createElement("button");
      b.textContent = t;
      b.onclick = function () { input.value = t; send(); };
      sug.appendChild(b);
    });

    function send() {
      var q = input.value.trim();
      if (!q) return;
      go.disabled = true;
      out.innerHTML = '<div class="awa-q">' + esc(q) + '</div><div class="awa-load">Thinking…</div>';

      fetch(ENDPOINT, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ mode: MODE, month: MONTH, question: q, session: SESSION })
      })
      .then(function (r) { return r.json(); })
      .then(function (d) { render(q, d); })
      .catch(function () {
        render(q, { kind: "handoff", answer: "I couldn't reach the assistant just now. Worth bringing to the monthly call." });
      })
      .finally(function () { go.disabled = false; input.value = ""; });
    }

    function render(q, d) {
      var html = '<div class="awa-q">' + esc(q) + '</div>';

      if (d.kind === "route") {
        html += '<div class="awa-route"><b>' + esc(d.label || "Start here") + '</b>' +
                '<span>' + esc(d.why || "") + '</span></div>' +
                '<div class="awa-cta"><a class="p" href="' + esc(d.url) + '">Open it &rarr;</a>' +
                (d.call ? '<a href="' + esc(d.call) + '">Join the monthly call</a>' : '') + '</div>';
      } else {
        html += '<div class="awa-a">' + esc(d.answer || "").replace(/\n\n+/g, "</p><p>").replace(/^/, "<p>") + "</p></div>";
        var cta = "";
        if (d.tool)    cta += '<a class="p" href="' + esc(d.tool) + '">Open the tool &rarr;</a>';
        if (d.booking) cta += '<a href="' + esc(d.booking) + '">Talk to Alex</a>';
        if (d.call)    cta += '<a href="' + esc(d.call) + '">Join the monthly call</a>';
        if (cta) html += '<div class="awa-cta">' + cta + "</div>";
      }
      out.innerHTML = html;
    }

    go.onclick = send;
    input.addEventListener("keydown", function (e) { if (e.key === "Enter") send(); });
  }

  function init() {
    var wrap = build();
    var host = document.getElementById("assistant-slot");
    if (host) host.appendChild(wrap);
    else {
      var w = document.querySelector(".wrap") || document.body;
      w.appendChild(wrap);
    }
    mount(wrap);
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();

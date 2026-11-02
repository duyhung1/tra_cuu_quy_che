// CMP-01 Web UI (blueprint §7). All strings come from vi.json; answers are inserted with textContent.
let T = {};
let docsState = { counts: { ready: 0, processing: 0 } };
const MAX_Q = 2000;
const MAX_FILES = 10;
const $ = (id) => document.getElementById(id);
const t = (k, vars = {}) => (T[k] || k).replace(/\{(\w+)\}/g, (_, v) => vars[v]);
const el = (tag, cls, text) => {
  const e = document.createElement(tag);
  if (cls) e.className = cls;
  if (text !== undefined) e.textContent = text;
  return e;
};
const fmtDate = (iso) => (iso ? iso.split("-").reverse().join("/") : "—");

async function api(path, opts) {
  const res = await fetch(path, opts);
  const body = await res.json().catch(() => ({}));
  if (!res.ok) throw Object.assign(new Error(body.message || t("network")), { code: body.code });
  return body;
}

async function loadDocs() {
  try {
    docsState = await api("/api/documents");
  } catch {
    return;
  }
  const { ready, processing } = docsState.counts;
  $("docs-in-use").textContent = t("docsInUse", { n: ready });
  $("processing").hidden = processing === 0;
  $("processing").textContent = t("processing", { n: processing });
  $("locked").hidden = ready > 0;
  $("ask-input").disabled = ready === 0;
  updateCounter();
  const tbody = $("doc-table").querySelector("tbody");
  tbody.replaceChildren();
  if (docsState.items.length === 0) {
    const tr = el("tr");
    const td = el("td", "muted", t("empty"));
    td.colSpan = 5;
    tr.append(td);
    tbody.append(tr);
  }
  for (const d of docsState.items) {
    const tr = el("tr");
    const name = el("td");
    name.append(el("div", "name", d.title || d.filename));
    if (d.title) name.append(el("div", "muted", d.filename));
    if (d.status === "failed") name.append(el("div", "err", d.message));
    tr.append(name, el("td", "", d.doc_number || "—"), el("td", "", fmtDate(d.effective_date)),
      el("td", "num", d.pages ?? "—"), el("td", `badge ${d.status}`, t(`status_${d.status}`)));
    tbody.append(tr);
  }
  if (processing > 0) setTimeout(loadDocs, 3000);
}

function updateCounter() {
  const len = $("ask-input").value.trim().length;
  $("counter").textContent = `${$("ask-input").value.length}/${MAX_Q}`;
  $("counter").className = $("ask-input").value.length > MAX_Q ? "over" : "";
  $("ask-send").disabled = len === 0 || $("ask-input").value.length > MAX_Q || docsState.counts.ready === 0;
}

function renderSources(sources) {
  const box = el("section", "sources");
  box.dataset.testid = "sources";
  box.append(el("h3", "", t("sourcesTitle")));
  const ol = el("ol");
  for (const s of sources) {
    const li = el("li");
    const where = [s.article, s.clause].filter(Boolean).join(", ");
    li.append(el("span", "ref", `[${s.ref}]`));
    const txt = el("div");
    txt.append(el("div", "main", [where, s.doc_title || s.filename].filter(Boolean).join(" — ")));
    const meta = [s.doc_number ? `Số ${s.doc_number}` : null, s.effective_date ? `hiệu lực ${fmtDate(s.effective_date)}` : null,
      `trang ${s.page}`, s.filename].filter(Boolean).join(" · ");
    txt.append(el("div", "muted", meta));
    li.append(txt);
    ol.append(li);
  }
  box.append(ol);
  return box;
}

async function ask(question, turn) {
  const body = turn.querySelector(".ai");
  body.replaceChildren(el("div", "muted", t("thinking")));
  $("ask-send").disabled = true;
  try {
    const res = await api("/api/ask", {
      method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ question }),
    });
    const answer = el("div", "answer", res.answer);
    answer.dataset.testid = "answer";
    body.replaceChildren(answer);
    if (res.sources.length) body.append(renderSources(res.sources));
    body.append(el("div", "muted small", `${t("aiLabel")} · ${t("latency", { s: (res.latency_ms / 1000).toFixed(1) })}`));
  } catch (err) {
    const retry = el("button", "btn small", t("retry"));
    retry.dataset.testid = "retry";
    retry.type = "button";
    retry.onclick = () => ask(question, turn);
    body.replaceChildren(el("div", "err", err.message), retry);
  } finally {
    updateCounter();
  }
}

function submitQuestion(e) {
  e?.preventDefault();
  const question = $("ask-input").value.trim();
  if (!question || question.length > MAX_Q) return;
  const turn = el("article", "turn");
  turn.append(el("div", "user", question), el("div", "ai"));
  $("thread").append(turn);
  $("ask-input").value = "";
  ask(question, turn);
}

async function upload(files) {
  $("upload-errors").replaceChildren();
  if (files.length > MAX_FILES) {
    $("upload-errors").append(el("div", "err", t("tooManyFiles", { n: files.length })));
    $("file-input").value = "";
    return;
  }
  const form = new FormData();
  for (const f of files) form.append("files", f, f.name);
  $("upload-status").textContent = t("uploading");
  try {
    const res = await api("/api/documents", { method: "POST", body: form });
    const bad = res.items.filter((i) => i.status === "failed");
    if (bad.length) {
      $("upload-errors").append(el("div", "", t("rejected")));
      for (const b of bad) $("upload-errors").append(el("div", "err", `${b.filename}: ${b.message}`));
    }
  } catch (err) {
    $("upload-errors").append(el("div", "err", err.message));
  } finally {
    $("upload-status").textContent = "";
    $("file-input").value = "";
    loadDocs();
  }
}

function route() {
  const docs = location.hash === "#documents";
  $("view-ask").hidden = docs;
  $("view-documents").hidden = !docs;
  loadDocs();
}

async function init() {
  T = await (await fetch("vi.json")).json();
  document.querySelectorAll("[data-t]").forEach((n) => (n.textContent = t(n.dataset.t)));
  $("ask-input").placeholder = t("placeholder");
  $("ask-input").addEventListener("input", updateCounter);
  $("ask-input").addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey) submitQuestion(e);
  });
  $("ask-form").addEventListener("submit", submitQuestion);
  $("file-input").addEventListener("change", (e) => upload([...e.target.files]));
  window.addEventListener("hashchange", route);
  route();
}

init();

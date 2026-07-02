// State Variables
let practicals = {};
let selected = new Set();
let fileBObj = null;

// Helpers
const $ = id => document.getElementById(id);

function showMsg(id, message, type) {
  const el = $(id);
  if (!el) return;
  let iconName = 'info';
  if (type === 'ok')  iconName = 'check-circle-2';
  if (type === 'err') iconName = 'alert-triangle';
  el.className = `toast-msg toast-msg-${type} show`;
  el.innerHTML = `
    <div class="toast-msg-icon"><i data-lucide="${iconName}"></i></div>
    <div class="toast-msg-content">${message}</div>
  `;
  if (window.lucide) window.lucide.createIcons();
}

function hideMsg(id) {
  const el = $(id);
  if (el) el.className = 'toast-msg';
}

function updateStepper(step, status) {
  const node = $(`step-node-${step}`);
  if (!node) return;
  if (status === 'active') {
    node.className = 'step-node active';
  } else if (status === 'done') {
    node.className = 'step-node done';
    const circle = node.querySelector('.step-circle');
    if (circle) circle.innerHTML = '<i data-lucide="check" style="width:16px;height:16px;"></i>';
  } else {
    node.className = 'step-node';
    const circle = node.querySelector('.step-circle');
    if (circle) circle.textContent = step;
  }
  let doneCount = 0;
  for (let i = 1; i <= 5; i++) {
    const n = $(`step-node-${i}`);
    if (n && n.classList.contains('done')) doneCount++;
  }
  const fill = $('step-progress-fill');
  if (fill) {
    let pct = 0;
    if (doneCount === 1) pct = 10;
    if (doneCount === 2) pct = 35;
    if (doneCount === 3) pct = 60;
    if (doneCount === 4) pct = 85;
    if (doneCount === 5) pct = 100;
    fill.style.width = `${pct}%`;
  }
  if (window.lucide) window.lucide.createIcons();
}

function formatBytes(bytes, decimals = 2) {
  if (bytes === 0) return '0 Bytes';
  const k = 1024;
  const dm = decimals < 0 ? 0 : decimals;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
}

// ── Cold-start banner (Render.com free tier sleeps after 15 min) ──────────
(function initColdStartBanner() {
  const startTime = Date.now();
  const banner = document.createElement('div');
  banner.id = 'cold-banner';
  banner.innerHTML = `
    <span style="font-size:16px">⏳</span>
    <span>Server is waking up — this takes ~20 seconds on first visit. Almost there!</span>
    <button onclick="document.getElementById('cold-banner').remove()" style="background:none;border:none;cursor:pointer;color:inherit;font-size:16px;line-height:1;padding:0;margin-left:4px">✕</button>
  `;
  banner.style.cssText = [
    'display:none','position:fixed','top:0','left:0','right:0','z-index:9999',
    'background:#FEF3C7','color:#92400E','padding:10px 16px',
    'font-size:13px','font-weight:500','text-align:center',
    'align-items:center','justify-content:center','gap:8px',
    'box-shadow:0 2px 8px rgba(0,0,0,.1)'
  ].join(';');
  document.body.prepend(banner);

  // Show banner only if page takes > 4 seconds to respond (cold start)
  const checkTimer = setTimeout(() => {
    if (!document.body.dataset.serverReady) {
      banner.style.display = 'flex';
      // Auto-remove after 30s
      setTimeout(() => banner.remove(), 30000);
    }
  }, 4000);

  window.addEventListener('load', () => {
    document.body.dataset.serverReady = '1';
    clearTimeout(checkTimer);
    if (Date.now() - startTime < 4000) {
      banner.remove(); // fast load — never show
    }
  });
})();

// ── Drag & Drop Event Listeners ───────────────────────────────────────────
['dz-a', 'dz-b'].forEach(dzId => {
  const dz = $(dzId);
  if (!dz) return;
  dz.addEventListener('dragover', e => { e.preventDefault(); dz.classList.add('over'); });
  dz.addEventListener('dragleave', () => dz.classList.remove('over'));
  dz.addEventListener('drop', e => {
    e.preventDefault();
    dz.classList.remove('over');
    const inp = dz.querySelector('input[type=file]');
    if (e.dataTransfer.files[0]) {
      try { const dt = new DataTransfer(); dt.items.add(e.dataTransfer.files[0]); inp.files = dt.files; } catch (_) {}
      inp.dispatchEvent(new Event('change', { bubbles: true }));
    }
  });
});

// ── File A Handling ───────────────────────────────────────────────────────
$('file-a').addEventListener('change', () => {
  const file = $('file-a').files[0];
  if (!file) return;
  // Validate it's actually a PDF
  if (file.type && file.type !== 'application/pdf' && !file.name.toLowerCase().endsWith('.pdf')) {
    showMsg('msg-parse', 'Please upload a PDF file, not a ' + (file.type || 'unknown') + ' file.', 'err');
    $('file-a').value = '';
    return;
  }
  $('fn-a').textContent = file.name;
  $('fs-a').textContent = formatBytes(file.size);
  $('fp-a').classList.add('show');
  $('dz-a-text').style.display = 'none';
  $('dz-a-icon').style.display = 'none';
  $('btn-parse').disabled = false;
  hideMsg('msg-parse');
});

$('btn-remove-a').addEventListener('click', e => {
  e.stopPropagation();
  $('file-a').value = '';
  $('fp-a').classList.remove('show');
  $('dz-a-text').style.display = 'block';
  $('dz-a-icon').style.display = 'block';
  $('btn-parse').disabled = true;
  hideMsg('msg-parse');
  updateStepper(1, 'active');
  updateStepper(2, 'upcoming');
  $('card1').classList.remove('done');
  $('card2').classList.add('locked');
  practicals = {};
  selected.clear();
  $('prac-grid').innerHTML = '';
  updateSel();
});

// ── File B Handling ───────────────────────────────────────────────────────
$('file-b').addEventListener('change', () => {
  const file = $('file-b').files[0];
  if (!file) return;
  // Validate PDF
  if (file.type && file.type !== 'application/pdf' && !file.name.toLowerCase().endsWith('.pdf')) {
    showMsg('msg-parse', 'Term Work file must be a PDF.', 'err');
    $('file-b').value = '';
    return;
  }
  fileBObj = file;
  $('fn-b').textContent = file.name;
  $('fs-b').textContent = formatBytes(file.size);
  $('fp-b').classList.add('show');
  $('dz-b-text').style.display = 'none';
  $('dz-b-icon').style.display = 'none';
  $('card3').classList.add('done');
  updateStepper(3, 'done');
  updateStepper(4, 'active');
  tryEnableNext();
});

$('btn-remove-b').addEventListener('click', e => {
  e.stopPropagation();
  $('file-b').value = '';
  fileBObj = null;
  $('fp-b').classList.remove('show');
  $('dz-b-text').style.display = 'block';
  $('dz-b-icon').style.display = 'block';
  $('card3').classList.remove('done');
  updateStepper(3, 'active');
  updateStepper(4, 'upcoming');
  tryEnableNext();
});

// ── Parse Index PDF ───────────────────────────────────────────────────────
$('btn-parse').addEventListener('click', async () => {
  const file = $('file-a').files[0];
  if (!file) return;

  $('btn-parse').disabled = true;
  $('sp-parse').style.display = 'inline-block';
  hideMsg('msg-parse');

  // Add a timeout so user gets clear feedback if server is cold-starting
  const controller  = new AbortController();
  const timeoutId   = setTimeout(() => {
    showMsg('msg-parse', '⏳ Server is taking a moment to wake up — still working…', 'info');
  }, 6000);

  const fd = new FormData();
  fd.append('pdf_a', file);

  try {
    const res  = await fetch('/api/parse-index', { method: 'POST', body: fd, signal: controller.signal });
    clearTimeout(timeoutId);
    const data = await res.json();

    if (!res.ok || data.error) {
      showMsg('msg-parse', `Parsing failed: ${data.error || 'Unknown server error'}`, 'err');
      return;
    }

    practicals = data.practicals;
    selected.clear();
    renderGrid();

    $('card2').classList.remove('locked');
    $('card1').classList.add('done');
    updateStepper(1, 'done');
    updateStepper(2, 'active');

    showMsg('msg-parse', `Successfully extracted <b>${Object.keys(practicals).length} practicals</b> from index.`, 'ok');
  } catch (e) {
    clearTimeout(timeoutId);
    if (e.name === 'AbortError') return;
    showMsg('msg-parse', `Network error: ${e.message}. Try refreshing if the server was sleeping.`, 'err');
  } finally {
    $('sp-parse').style.display = 'none';
    $('btn-parse').disabled = false;
  }
});

// ── Render Grid ───────────────────────────────────────────────────────────
function renderGrid() {
  const grid = $('prac-grid');
  grid.innerHTML = '';

  // Show skeleton cards briefly for visual polish
  const count = Object.keys(practicals).length;
  for (let i = 0; i < Math.min(count, 4); i++) {
    const sk = document.createElement('div');
    sk.className = 'prac-card skeleton-card';
    sk.style.cssText = 'animation:pulse 1s ease infinite;background:var(--clr-surface-alt);border:none;min-height:72px;';
    grid.appendChild(sk);
  }

  // Replace with real cards after a brief moment
  setTimeout(() => {
    grid.innerHTML = '';
    Object.keys(practicals).sort((a, b) => +a - +b).forEach(num => {
      const card = document.createElement('div');
      card.className = `prac-card${selected.has(num) ? ' selected' : ''}`;
      card.dataset.num = num;
      card.innerHTML = `
        <div class="prac-card-checkbox">
          <i data-lucide="check" style="width:12px;height:12px;"></i>
        </div>
        <div class="prac-card-num">Practical ${num}</div>
        <div class="prac-card-title">${practicals[num]}</div>
      `;
      card.addEventListener('click', () => togglePractical(num));
      grid.appendChild(card);
    });
    updateSel();
    if (window.lucide) window.lucide.createIcons();
  }, 300);
}

function togglePractical(num) {
  if (selected.has(num)) selected.delete(num);
  else selected.add(num);
  const card = document.querySelector(`.prac-card[data-num="${num}"]`);
  if (card) card.classList.toggle('selected', selected.has(num));
  updateSel();
}

$('btn-all').addEventListener('click', () => {
  Object.keys(practicals).forEach(n => selected.add(n));
  renderGrid();
});

$('btn-none').addEventListener('click', () => {
  selected.clear();
  renderGrid();
});

// ── Selection State ───────────────────────────────────────────────────────
function updateSel() {
  $('sel-count').textContent = selected.size;

  const chips = $('chips');
  chips.innerHTML = '';
  [...selected].sort((a, b) => +a - +b).forEach(num => {
    const chip = document.createElement('div');
    chip.className = 'chip';
    chip.innerHTML = `
      <span>P${num}</span>
      <button class="chip-remove" onclick="removeSel('${num}')">
        <i data-lucide="x" style="width:12px;height:12px;"></i>
      </button>
    `;
    chips.appendChild(chip);
  });

  if (selected.size > 0) {
    $('card2').classList.add('done');
    updateStepper(2, 'done');
    if ($('card3').classList.contains('locked')) {
      $('card3').classList.remove('locked');
      updateStepper(3, 'active');
    }
  } else {
    $('card2').classList.remove('done');
    updateStepper(2, 'active');
    $('card3').classList.add('locked');
    updateStepper(3, 'upcoming');
  }

  tryEnableNext();
  if (window.lucide) window.lucide.createIcons();
}

window.removeSel = function(num) {
  selected.delete(num);
  const card = document.querySelector(`.prac-card[data-num="${num}"]`);
  if (card) card.classList.remove('selected');
  updateSel();
};

// ── Continue Button ───────────────────────────────────────────────────────
function tryEnableNext() {
  const ready = selected.size > 0 && fileBObj !== null;
  $('btn-next').disabled = !ready;
  $('cta-hint').innerHTML = ready
    ? `<b>${selected.size} practical${selected.size > 1 ? 's' : ''}</b> selected — ready to continue.`
    : 'Please complete steps 1, 2, and 3 to proceed.';
}

$('btn-next').addEventListener('click', () => {
  if (selected.size === 0 || !fileBObj) return;

  const srNos  = [...selected].sort((a, b) => +a - +b);
  const titles = srNos.map(n => ({ sr_no: n, title: practicals[n] }));

  sessionStorage.setItem('twf_titles',    JSON.stringify(titles));
  sessionStorage.setItem('twf_sel_count', srNos.length);

  $('btn-next').disabled = true;
  $('btn-next').innerHTML = '<span class="progress-spinner" style="width:14px;height:14px;border-width:2px;margin-right:4px;"></span> Reading Form PDF…';

  const reader   = new FileReader();
  reader.onload  = e => {
    sessionStorage.setItem('twf_pdf_b', e.target.result);
    window.location.href = '/form';
  };
  reader.onerror = () => {
    alert('Failed to read Term Work template PDF. Please try uploading again.');
    $('btn-next').disabled = false;
    $('btn-next').innerHTML = 'Continue to Fill Details <i data-lucide="arrow-right"></i>';
    if (window.lucide) window.lucide.createIcons();
  };
  reader.readAsDataURL(fileBObj);
});

// ── Init ──────────────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  if (window.lucide) window.lucide.createIcons();
  updateStepper(1, 'active');
});

// ═══════════════════════════════════════════════════════════════
// TEMPLATE PICKER MODAL
// ═══════════════════════════════════════════════════════════════

let selectedTemplateKey  = null;
let selectedTemplateLabel = null;

// ── Open / Close ─────────────────────────────────────────────
function openTemplateModal() {
  $('tpl-backdrop').classList.add('open');
  document.body.style.overflow = 'hidden';
}

function closeTemplateModal() {
  $('tpl-backdrop').classList.remove('open');
  document.body.style.overflow = '';
}

window.openTemplateModal  = openTemplateModal;
window.closeTemplateModal = closeTemplateModal;

// ── Trigger button ────────────────────────────────────────────
const openBtn = $('btn-open-templates');
if (openBtn) openBtn.addEventListener('click', openTemplateModal);

// ── Close on backdrop click (not on modal itself) ─────────────
$('tpl-backdrop').addEventListener('click', e => {
  if (e.target === $('tpl-backdrop')) closeTemplateModal();
});

// ── Card selection logic ──────────────────────────────────────
document.querySelectorAll('.tpl-card[data-key]').forEach(card => {
  card.addEventListener('click', () => {
    // Deselect all
    document.querySelectorAll('.tpl-card').forEach(c => c.classList.remove('active'));
    // Select this one
    card.classList.add('active');
    selectedTemplateKey   = card.dataset.key;
    selectedTemplateLabel = card.dataset.label;
    // Update CTA
    const useBtn = $('tpl-use-btn');
    useBtn.disabled = false;
    useBtn.textContent = 'Use this template';
    if (window.lucide) window.lucide.createIcons();
  });
});

// ── "Use this template" button ────────────────────────────────
$('tpl-use-btn').addEventListener('click', async () => {
  if (!selectedTemplateKey) return;

  const useBtn = $('tpl-use-btn');
  useBtn.disabled  = true;
  useBtn.textContent = 'Loading template…';

  try {
    const res = await fetch(`/template/${selectedTemplateKey}`, { cache: 'no-store' });
    if (!res.ok) throw new Error('Template not found on server');

    const blob    = await res.blob();
    const file    = new File([blob], selectedTemplateLabel || 'term_work.pdf', { type: 'application/pdf' });

    // Inject into the file-b input via DataTransfer
    const dt = new DataTransfer();
    dt.items.add(file);
    const fileInput = $('file-b');
    fileInput.files  = dt.files;

    // Fire change event so existing file-b handler picks it up
    fileInput.dispatchEvent(new Event('change', { bubbles: true }));

    closeTemplateModal();
    useBtn.textContent  = 'Use this template';
    useBtn.disabled     = false;
    selectedTemplateKey = null;
    document.querySelectorAll('.tpl-card').forEach(c => c.classList.remove('active'));

  } catch (err) {
    useBtn.disabled     = false;
    useBtn.textContent  = 'Failed — tap to retry';
    console.error('Template load error:', err);
  }
});

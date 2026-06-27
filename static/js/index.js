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
  if (type === 'ok') iconName = 'check-circle-2';
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
  
  // Calculate horizontal progress bar width
  let doneCount = 0;
  for (let i = 1; i <= 5; i++) {
    const n = $(`step-node-${i}`);
    if (n && n.classList.contains('done')) doneCount++;
  }
  
  const fill = $('step-progress-fill');
  if (fill) {
    // 5 nodes mean 4 intervals. Each step represents 25% progress.
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

// ── Drag & Drop Event Listeners ──────────────────────────────────────────
['dz-a', 'dz-b'].forEach(dzId => {
  const dz = $(dzId);
  if (!dz) return;
  
  dz.addEventListener('dragover', e => {
    e.preventDefault();
    dz.classList.add('over');
  });
  
  dz.addEventListener('dragleave', () => {
    dz.classList.remove('over');
  });
  
  dz.addEventListener('drop', e => {
    e.preventDefault();
    dz.classList.remove('over');
    const inp = dz.querySelector('input[type=file]');
    if (e.dataTransfer.files[0]) {
      try {
        const dt = new DataTransfer();
        dt.items.add(e.dataTransfer.files[0]);
        inp.files = dt.files;
      } catch (_) {}
      inp.dispatchEvent(new Event('change', { bubbles: true }));
    }
  });
});

// ── File A Handling (Practical Index) ────────────────────────────────────
$('file-a').addEventListener('change', () => {
  const file = $('file-a').files[0];
  if (!file) return;
  
  $('fn-a').textContent = file.name;
  $('fs-a').textContent = formatBytes(file.size);
  $('fp-a').classList.add('show');
  
  // Hide dropzone label
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
  
  // Revert stepper
  updateStepper(1, 'active');
  updateStepper(2, 'upcoming');
  $('card1').classList.remove('done');
  
  // Lock Card 2
  $('card2').classList.add('locked');
  practicals = {};
  selected.clear();
  $('prac-grid').innerHTML = '';
  updateSel();
});

// ── File B Handling (Blank Term Work PDF) ───────────────────────────────
$('file-b').addEventListener('change', () => {
  const file = $('file-b').files[0];
  if (!file) return;
  
  fileBObj = file;
  $('fn-b').textContent = file.name;
  $('fs-b').textContent = formatBytes(file.size);
  $('fp-b').classList.add('show');
  
  // Hide dropzone labels
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

// ── Parse Index PDF Endpoint ─────────────────────────────────────────────
$('btn-parse').addEventListener('click', async () => {
  const file = $('file-a').files[0];
  if (!file) return;
  
  $('btn-parse').disabled = true;
  $('sp-parse').style.display = 'inline-block';
  hideMsg('msg-parse');
  
  const fd = new FormData();
  fd.append('pdf_a', file);
  
  try {
    const res = await fetch('/api/parse-index', { method: 'POST', body: fd });
    const data = await res.json();
    
    if (!res.ok || data.error) {
      showMsg('msg-parse', `Parsing failed: ${data.error || 'Unknown server error'}`, 'err');
      return;
    }
    
    practicals = data.practicals;
    selected.clear();
    renderGrid();
    
    // Unlock card 2
    $('card2').classList.remove('locked');
    $('card1').classList.add('done');
    updateStepper(1, 'done');
    updateStepper(2, 'active');
    
    showMsg('msg-parse', `Successfully extracted <b>${Object.keys(practicals).length} practicals</b> from index.`, 'ok');
  } catch (e) {
    showMsg('msg-parse', `Network error: ${e.message}`, 'err');
  } finally {
    $('sp-parse').style.display = 'none';
    $('btn-parse').disabled = false;
  }
});

// ── Render Selection Grid ────────────────────────────────────────────────
function renderGrid() {
  const grid = $('prac-grid');
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
}

function togglePractical(num) {
  if (selected.has(num)) {
    selected.delete(num);
  } else {
    selected.add(num);
  }
  
  const card = document.querySelector(`.prac-card[data-num="${num}"]`);
  if (card) {
    card.classList.toggle('selected', selected.has(num));
  }
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

// ── Selected Items State Tracking ────────────────────────────────────────
function updateSel() {
  $('sel-count').textContent = selected.size;
  
  const chips = $('chips');
  chips.innerHTML = '';
  
  const sortedSelected = [...selected].sort((a, b) => +a - +b);
  sortedSelected.forEach(num => {
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
    
    // Unlock card 3 if it was locked
    if ($('card3').classList.contains('locked')) {
      $('card3').classList.remove('locked');
      updateStepper(3, 'active');
    }
  } else {
    $('card2').classList.remove('done');
    updateStepper(2, 'active');
    
    // Lock card 3
    $('card3').classList.add('locked');
    updateStepper(3, 'upcoming');
  }
  
  tryEnableNext();
  if (window.lucide) window.lucide.createIcons();
}

window.removeSel = function(num) {
  selected.delete(num);
  const card = document.querySelector(`.prac-card[data-num="${num}"]`);
  if (card) {
    card.classList.remove('selected');
  }
  updateSel();
};

// ── Enable/Disable Continue Button ───────────────────────────────────────
function tryEnableNext() {
  const ready = selected.size > 0 && fileBObj !== null;
  $('btn-next').disabled = !ready;
  
  $('cta-hint').innerHTML = ready
    ? `<b>${selected.size} practical${selected.size > 1 ? 's' : ''}</b> selected — ready to continue.`
    : 'Please complete steps 1, 2, and 3 to proceed.';
}

// ── Continue Button Navigation ───────────────────────────────────────────
$('btn-next').addEventListener('click', () => {
  if (selected.size === 0 || !fileBObj) return;
  
  const srNos = [...selected].sort((a, b) => +a - +b);
  const titles = srNos.map(n => ({ sr_no: n, title: practicals[n] }));
  
  sessionStorage.setItem('twf_titles', JSON.stringify(titles));
  sessionStorage.setItem('twf_sel_count', srNos.length);
  
  // Show spinner on primary button
  $('btn-next').disabled = true;
  $('btn-next').innerHTML = '<span class="progress-spinner" style="width:14px;height:14px;border-width:2px;margin-right:4px;"></span> Reading Form PDF…';
  
  // Read PDF B as base64 data url for Page 2
  const reader = new FileReader();
  reader.onload = e => {
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

// Initialization
document.addEventListener('DOMContentLoaded', () => {
  if (window.lucide) window.lucide.createIcons();
  updateStepper(1, 'active');
});

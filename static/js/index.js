// ── Retrieve State from sessionStorage ───────────────────────────────────
const titles  = JSON.parse(sessionStorage.getItem('twf_titles')  || '[]');
const pdfBb64 = sessionStorage.getItem('twf_pdf_b') || '';

if (!titles.length || !pdfBb64) {
  window.location.href = '/';
}

const $ = id => document.getElementById(id);

const LS_KEY = 'twf_saved_form';

const FIELD_LABELS = {
  'f-student':  'Student Name',
  'f-pen':      'PEN Number',
  'f-semester': 'Semester',
  'f-class':    'Class',
  'f-batch':    'Batch',
  'f-faculty':  'Faculty Name (Checked By)',
  'f-subject':  'Subject',
  'f-term':     'Term',
  'f-cond':     'Conducted On',
  'f-sub':      'Date of Submission',
  'f-actsub':   'Actual Date of Submission',
  'f-marks':    'Marks',
  'f-signdate': 'Signature Date',
};

function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

function formatDate(val) {
  if (!val) return '';
  const [y, m, d] = val.split('-');
  return `${d}/${m}/${y}`;
}

function formatBytes(bytes, decimals = 2) {
  if (bytes === 0) return '0 Bytes';
  const k = 1024, dm = decimals < 0 ? 0 : decimals;
  const sizes = ['Bytes', 'KB', 'MB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
}

// Mirrors the server-side make_download_name() logic in app.py
function buildDownloadName(srNumbers) {
  const nums = [...new Set(srNumbers.map(Number))].sort((a, b) => a - b);
  if (!nums.length) return 'TermWorkForge_Practicals.pdf';
  const groups = [];
  let start = nums[0], prev = nums[0];
  for (const n of nums.slice(1)) {
    if (n === prev + 1) { prev = n; continue; }
    groups.push([start, prev]);
    start = prev = n;
  }
  groups.push([start, prev]);
  const parts = [];
  for (const [a, b] of groups) {
    if (a === b)         parts.push(String(a));
    else if (b === a+1) { parts.push(String(a)); parts.push(String(b)); }
    else                 parts.push(`${a}-${b}`);
  }
  const label = nums.length === 1 ? 'Practical' : 'Practicals';
  return `TermWorkForge_${label}_${parts.join('_')}.pdf`;
}

function saveFormToLocalStorage() {
  const data = {};
  Object.keys(FIELD_LABELS).forEach(id => {
    const el = $(id);
    if (el) data[id] = el.value;
  });
  try { localStorage.setItem(LS_KEY, JSON.stringify(data)); } catch (_) {}
}

function loadFormFromLocalStorage() {
  try {
    const raw = localStorage.getItem(LS_KEY);
    if (!raw) return;
    const data = JSON.parse(raw);
    let loaded = 0;
    Object.keys(FIELD_LABELS).forEach(id => {
      const el = $(id);
      if (el && data[id]) { el.value = data[id]; loaded++; }
    });
    if (loaded > 0) {
      const toast = $('toast-remembered');
      if (toast) {
        toast.style.display = 'flex';
        setTimeout(() => {
          toast.style.opacity = '0';
          setTimeout(() => toast.remove(), 400);
        }, 3000);
      }
    }
  } catch (_) {}
}

function clearSavedForm() {
  try { localStorage.removeItem(LS_KEY); } catch (_) {}
}

function getFormValues() {
  return {
    student_name: $('f-student').value.trim(),
    pen:          $('f-pen').value.trim(),
    semester:     $('f-semester').value.trim(),
    class_name:   $('f-class').value.trim(),
    batch:        $('f-batch').value.trim(),
    checked_by:   $('f-faculty').value.trim(),
    subject:      $('f-subject').value.trim(),
    term:         $('f-term').value.trim(),
    conducted_on: formatDate($('f-cond').value),
    date_of_sub:  formatDate($('f-sub').value),
    actual_sub:   formatDate($('f-actsub').value),
    marks:        $('f-marks').value.trim(),
    sign_date:    formatDate($('f-signdate').value),
  };
}

function getEmptyFields() {
  const empty = [];
  Object.entries(FIELD_LABELS).forEach(([id, label]) => {
    const el = $(id);
    if (el && !el.value.trim()) empty.push(label);
  });
  return empty;
}

function openModal()  { $('modal-overlay').classList.add('show');    }
function closeModal() { $('modal-overlay').classList.remove('show'); }
window.closeModal = closeModal;

window.confirmGoBack = function () {
  const sure = confirm(
    `Going back will clear your ${titles.length} selected practical${titles.length > 1 ? 's' : ''} and uploaded files. Continue?`
  );
  if (sure) {
    sessionStorage.removeItem('twf_titles');
    sessionStorage.removeItem('twf_pdf_b');
    sessionStorage.removeItem('twf_sel_count');
    window.location.href = '/';
  }
};

// ═══════════════════════════════════════════════════════════════════════════
// LOTTIE — uses lottie-web 5.12.2 (SVG renderer, no WASM, no workers)
// <script> tag in form.html loads it from cdnjs before this file runs
// Animation file: /static/loading-animation.json
// ═══════════════════════════════════════════════════════════════════════════
let _lottieAnim = null;

function initLottie() {
  if (_lottieAnim) return;
  if (typeof lottie === 'undefined') {
    console.warn('lottie-web not available');
    return;
  }
  const container = $('lottie-wrap');
  if (!container) return;

  _lottieAnim = lottie.loadAnimation({
    container,
    renderer:  'svg',
    loop:      true,
    autoplay:  false,
    path:      '/static/loading-animation.json',
  });
}

function startLottie() {
  if (!_lottieAnim) initLottie();
  if (_lottieAnim) _lottieAnim.play();
}

function stopLottie() {
  if (_lottieAnim) _lottieAnim.stop();
}

const MESSAGES = [
  'Reading template PDF\u2026',
  'Mapping your details onto fields\u2026',
  'Server is generating your PDFs\u2026',
  'Merging all pages together\u2026',
  'Preparing your download\u2026',
];

function setProgress(pct, msgIdx) {
  const bar = $('progress-fill');
  const msg = $('progress-message');
  if (bar) bar.style.width = pct + '%';
  if (msg && msgIdx !== undefined)
    msg.textContent = MESSAGES[Math.min(msgIdx, MESSAGES.length - 1)];
}

async function doGenerate() {
  const overlay = $('progress-overlay');
  overlay.classList.add('show');
  startLottie();
  setProgress(8, 0);

  try {
    await sleep(200);
    saveFormToLocalStorage();

    setProgress(20, 1);
    const base64Data   = pdfBb64.split(',')[1];
    const binaryString = atob(base64Data);
    const bytes        = new Uint8Array(binaryString.length);
    for (let i = 0; i < binaryString.length; i++) bytes[i] = binaryString.charCodeAt(i);
    const pdfBlob = new Blob([bytes], { type: 'application/pdf' });

    await sleep(200);
    setProgress(40, 2);

    const formValues = getFormValues();
    const fd = new FormData();
    fd.append('pdf_b',       pdfBlob, 'term_work.pdf');
    fd.append('titles_json', JSON.stringify(titles));
    fd.append('form_json',   JSON.stringify(formValues));

    const response = await fetch('/api/generate', { method: 'POST', body: fd });
    setProgress(75, 3);

    if (!response.ok) {
      let errMsg = 'Server error';
      try { const d = await response.json(); errMsg = d.error || errMsg; } catch (_) {}
      throw new Error(errMsg);
    }

    const outputBlob = await response.blob();
    setProgress(95, 4);
    await sleep(300);

    // Prefer the branded filename the server sends; fall back to a client-side version
    const serverName = response.headers.get('X-Download-Name');
    const downloadName = serverName || buildDownloadName(titles.map(t => t.sr_no));

    const url = URL.createObjectURL(outputBlob);
    const a   = document.createElement('a');
    a.href     = url;
    a.download = downloadName;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    setTimeout(() => URL.revokeObjectURL(url), 1000);

    setProgress(100, 4);
    await sleep(400);

    stopLottie();
    overlay.classList.remove('show');
    $('success-qty').textContent  = `${titles.length} page${titles.length > 1 ? 's' : ''}`;
    $('success-size').textContent = formatBytes(outputBlob.size);
    $('success-screen-overlay').classList.add('show');

  } catch (error) {
    stopLottie();
    overlay.classList.remove('show');
    alert(`\u274C Generation Failed: ${error.message}\n\nPlease check your files and try again.`);
  }
}

document.addEventListener('DOMContentLoaded', () => {
  if (window.lucide) window.lucide.createIcons();

  $('topbar-count').textContent = `${titles.length} practical${titles.length > 1 ? 's' : ''} selected`;
  $('cta-qty-hint').textContent = `Will generate ${titles.length} filled page${titles.length > 1 ? 's' : ''} as one merged PDF.`;

  const summaryBar = $('summary-bar');
  summaryBar.innerHTML = '';
  titles.forEach(item => {
    const pill = document.createElement('div');
    pill.className = 'sum-pill';
    pill.innerHTML = `<i data-lucide="bookmark" style="width:12px;height:12px;color:var(--clr-primary);"></i> P${item.sr_no}`;
    summaryBar.appendChild(pill);
  });
  if (window.lucide) window.lucide.createIcons();

  setTimeout(initLottie, 600);

  loadFormFromLocalStorage();

  // Auto-fill subject from the parsed index.
  // sessionStorage (fresh parse) ALWAYS wins over localStorage (old saved data).
  // If the user's saved subject differs from what was just parsed, the fresh
  // parsed value replaces it — so switching index files always shows the right subject.
  const autoSubject = sessionStorage.getItem('twf_subject') || '';
  const subjectEl   = $('f-subject');
  if (autoSubject && subjectEl) {
    const savedSubject = subjectEl.value.trim(); // already filled by loadFormFromLocalStorage
    if (savedSubject.toLowerCase() !== autoSubject.toLowerCase()) {
      // Different subject detected — override with the freshly parsed one
      subjectEl.value = autoSubject;
      saveFormToLocalStorage(); // update localStorage so future visits also get the right value
    }
    // If they match, leave it — no flicker, no unnecessary write
  }

  Object.keys(FIELD_LABELS).forEach(id => {
    const el = $(id);
    if (el) {
      el.addEventListener('input',  saveFormToLocalStorage);
      el.addEventListener('change', saveFormToLocalStorage);
    }
  });

  $('btn-generate').addEventListener('click', () => {
    const empty = getEmptyFields();
    if (empty.length > 0) {
      $('modal-body-text').textContent =
        `${empty.length} field${empty.length > 1 ? 's are' : ' is'} empty. Blank spaces will appear in those positions on the PDF. Do you want to proceed?`;
      $('modal-empty-list').innerHTML = empty.map(f => `\u2022 ${f}`).join('<br>');
      openModal();
      $('modal-confirm').onclick = () => { closeModal(); doGenerate(); };
    } else {
      doGenerate();
    }
  });

  $('modal-overlay').addEventListener('click', e => {
    if (e.target === $('modal-overlay')) closeModal();
  });

  const clearBtn = $('btn-clear-saved');
  if (clearBtn) {
    clearBtn.addEventListener('click', () => {
      clearSavedForm();
      Object.keys(FIELD_LABELS).forEach(id => {
        const el = $(id);
        if (el) el.value = '';
      });
    });
  }
});

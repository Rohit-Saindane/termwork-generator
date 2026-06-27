// Retrieve State from sessionStorage
const titles  = JSON.parse(sessionStorage.getItem('twf_titles')  || '[]');
const pdfBb64 = sessionStorage.getItem('twf_pdf_b') || '';

if (!titles.length || !pdfBb64) {
  window.location.href = '/';
}

const $ = id => document.getElementById(id);

// ── Field Labels ─────────────────────────────────────────────────────────────
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

// ── Helpers ───────────────────────────────────────────────────────────────────
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

function formatDate(val) {
  if (!val) return '';
  const [y, m, d] = val.split('-');
  return `${d}/${m}/${y}`;
}

function formatBytes(bytes, decimals = 2) {
  if (bytes === 0) return '0 Bytes';
  const k = 1024;
  const dm = decimals < 0 ? 0 : decimals;
  const sizes = ['Bytes', 'KB', 'MB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
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

// ── Modal ─────────────────────────────────────────────────────────────────────
function openModal()  { $('modal-overlay').classList.add('show');    }
function closeModal() { $('modal-overlay').classList.remove('show'); }
window.closeModal = closeModal;

// ── PDF Generation ─────────────────────────────────────────────────────────────
async function doGenerate() {
  const overlay = $('progress-overlay');
  const bar     = $('progress-fill');
  const msg     = $('progress-message');

  overlay.classList.add('show');
  bar.style.width = '10%';
  msg.textContent = 'Reading template PDF…';

  try {
    await sleep(300);

    // Convert base64 → Blob
    const base64Data   = pdfBb64.split(',')[1];
    const binaryString = atob(base64Data);
    const bytes        = new Uint8Array(binaryString.length);
    for (let i = 0; i < binaryString.length; i++) {
      bytes[i] = binaryString.charCodeAt(i);
    }
    const pdfBlob = new Blob([bytes], { type: 'application/pdf' });

    bar.style.width = '35%';
    msg.textContent = 'Mapping form fields…';
    await sleep(300);

    const formValues = getFormValues();
    const fd = new FormData();
    fd.append('pdf_b',       pdfBlob, 'term_work.pdf');
    fd.append('titles_json', JSON.stringify(titles));
    fd.append('form_json',   JSON.stringify(formValues));

    bar.style.width = '60%';
    msg.textContent = 'Generating PDFs on server…';

    const response = await fetch('/api/generate', { method: 'POST', body: fd });

    bar.style.width = '85%';
    msg.textContent = 'Preparing download…';

    if (!response.ok) {
      let errMsg = 'Server error';
      try { const d = await response.json(); errMsg = d.error || errMsg; } catch (_) {}
      throw new Error(errMsg);
    }

    const outputBlob = await response.blob();
    bar.style.width  = '100%';
    msg.textContent  = 'Done!';
    await sleep(400);

    // ── Trigger download ──────────────────────────────────────────────────────
    const downloadUrl = URL.createObjectURL(outputBlob);
    const a           = document.createElement('a');
    a.href            = downloadUrl;
    a.download        = `TermWork_Practicals_${titles.map(t => t.sr_no).join('-')}.pdf`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    setTimeout(() => URL.revokeObjectURL(downloadUrl), 1000);

    // ── Show success screen ───────────────────────────────────────────────────
    overlay.classList.remove('show');
    $('success-qty').textContent  = `${titles.length} page${titles.length > 1 ? 's' : ''}`;
    $('success-size').textContent = formatBytes(outputBlob.size);
    $('success-screen-overlay').classList.add('show');

  } catch (error) {
    overlay.classList.remove('show');
    alert(`❌ Generation Failed: ${error.message}\n\nPlease check your files and try again.`);
  }
}

// ── Initialise everything after DOM is ready ────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  if (window.lucide) window.lucide.createIcons();

  // Populate topbar & summary bar
  $('topbar-count').textContent = `${titles.length} practical${titles.length > 1 ? 's' : ''} selected`;
  $('cta-qty-hint').textContent = `Will generate ${titles.length} filled page${titles.length > 1 ? 's' : ''} as one merged PDF.`;

  const summaryBar = $('summary-bar');
  summaryBar.innerHTML = '';
  titles.forEach(item => {
    const pill = document.createElement('div');
    pill.className = 'sum-pill';
    pill.innerHTML = `<i data-lucide="bookmark" style="width:12px;height:12px;color:var(--primary);"></i> P${item.sr_no}`;
    summaryBar.appendChild(pill);
  });
  if (window.lucide) window.lucide.createIcons();

  // ── Generate button ────────────────────────────────────────────────────────
  $('btn-generate').addEventListener('click', () => {
    const empty = getEmptyFields();
    if (empty.length > 0) {
      $('modal-body-text').textContent =
        `${empty.length} field${empty.length > 1 ? 's are' : ' is'} empty. Blank spaces will appear in those positions. Do you want to proceed?`;
      $('modal-empty-list').innerHTML = empty.map(f => `• ${f}`).join('<br>');
      openModal();
      // Assign confirm action fresh each open
      $('modal-confirm').onclick = () => { closeModal(); doGenerate(); };
    } else {
      doGenerate();
    }
  });

  // Close modal on backdrop click
  $('modal-overlay').addEventListener('click', e => {
    if (e.target === $('modal-overlay')) closeModal();
  });
});

/**
 * TermWorkForge — College Term Work Generator
 * Interactive College Notebook Application
 * Matches preview mockups 100%:
 * - Step 1: Files (Clipped index card with scan line + pinned college form card with VERIFIED stamp)
 * - Step 2: Practicals (Ruled notebook list with tick checkboxes, yellow sweep, floating sidebar with fanned miniature sheets and page chips)
 * - Step 3: Details (Form fields + live R.N.G. Patel miniature sheet with pen & yellow highlighter tracking active field)
 * - Step 4: Print (Yellow FORGE printer with LCD status, animated emerging sheet, filmstrip, rename box, download button)
 * - Step 5: Review (Filmstrip selector, Full/Top/Bottom segmented zoom pill, dashed editable hotspots)
 * - Step 6: Edit Drawer Modal (Scope: Only this page / Pick pages / All pages, editable fields, live "Apply to N pages")
 */

(() => {
  'use strict';

  // ── DOM Helpers ──
  const $ = id => document.getElementById(id);
  const $$ = (sel, root = document) => Array.from(root.querySelectorAll(sel));

  // ── Date Helper (Top-Level Scope) ──
  function splitDate(val) {
    if (!val || !String(val).trim()) return ['', '', ''];
    val = String(val).trim();
    if (val.includes('-')) {
      const parts = val.split('-');
      if (parts[0].length === 4) {
        return [parts[2] || '', parts[1] || '', parts[0] || ''];
      } else {
        return [parts[0] || '', parts[1] || '', parts[2] || ''];
      }
    }
    if (val.includes('/')) {
      const parts = val.split('/');
      if (parts[0].length === 4) {
        return [parts[2] || '', parts[1] || '', parts[0] || ''];
      } else {
        return [parts[0] || '', parts[1] || '', parts[2] || ''];
      }
    }
    return [val, '', ''];
  }

  // ── Clean Initial State (No hardcoded fake index) ──
  const S = {
    currentStep: 1,
    fileA: null,
    fileB: null,
    indexSubject: '',
    practicals: {},
    selected: new Set(),
    overrides: {},
    formData: {
      student_name: 'Aarav Mehta',
      pen: '250843131022',
      class_name: 'CSE-24-C',
      batch: 'C2',
      semester: '5th',
      term: '2026-27',
      subject: '',
      conducted_on: '',
      date_of_sub: '',
      actual_sub: '',
      checked_by: 'Prof. S. Desai',
      marks: '10'
    },
    reviewPage: 1,
    reviewZoom: 'full', // 'full' | 'top' | 'bottom'
    drawerScope: 'this', // 'this' | 'pick' | 'all'
    drawerPickedPages: new Set()
  };

  // ── HTML Escape Helper ──
  function escapeHtml(str) {
    if (!str) return '';
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  }

  // ── Resolve Merged Practical Data (Overrides + Base Form) ──
  function getPracticalData(pno) {
    const overrides = S.overrides[pno] || {};
    return {
      student_name: overrides.student_name !== undefined ? overrides.student_name : (S.formData.student_name || ''),
      pen: overrides.pen !== undefined ? overrides.pen : (S.formData.pen || ''),
      class_name: overrides.class_name !== undefined ? overrides.class_name : (S.formData.class_name || ''),
      batch: overrides.batch !== undefined ? overrides.batch : (S.formData.batch || ''),
      semester: overrides.semester !== undefined ? overrides.semester : (S.formData.semester || ''),
      term: overrides.term !== undefined ? overrides.term : (S.formData.term || ''),
      subject: overrides.subject !== undefined ? overrides.subject : (S.formData.subject || ''),
      checked_by: overrides.checked_by !== undefined ? overrides.checked_by : (S.formData.checked_by || ''),
      marks: overrides.marks !== undefined ? overrides.marks : (S.formData.marks || '10'),
      conducted_on: overrides.conducted_on !== undefined ? overrides.conducted_on : (S.formData.conducted_on || ''),
      date_of_sub: overrides.date_of_sub !== undefined ? overrides.date_of_sub : (S.formData.date_of_sub || ''),
      actual_sub: overrides.actual_sub !== undefined ? overrides.actual_sub : (S.formData.actual_sub || ''),
      title: S.practicals[pno] || (pno ? `Practical ${pno}` : '')
    };
  }

  // ── Unified Sheet Renderer: Keeps all miniatures 100% consistent ──
  function renderTwSheet(container, pno) {
    if (!container) return;
    const d = getPracticalData(pno);

    const setT = (sel, val) => {
      const el = container.querySelector(sel);
      if (el) el.textContent = val || '';
    };

    setT('.tw-student, .print-tw-student, .rev-tw-student, .fs-tw-student, .drw-tw-student', d.student_name);
    setT('.tw-pen, .print-tw-pen, .rev-tw-pen, .fs-tw-pen, .drw-tw-pen', d.pen);
    setT('.tw-class, .print-tw-class, .rev-tw-class, .fs-tw-class, .drw-tw-class', d.class_name);
    setT('.tw-batch, .print-tw-batch, .rev-tw-batch, .fs-tw-batch, .drw-tw-batch', d.batch);
    setT('.tw-semester, .print-tw-sem, .rev-tw-sem, .fs-tw-sem, .drw-tw-sem', d.semester);
    setT('.tw-term, .print-tw-term, .rev-tw-term, .fs-tw-term, .drw-tw-term', d.term);
    setT('.tw-subject, .print-tw-subj, .rev-tw-subj, .fs-tw-subj, .drw-tw-subj', d.subject);
    setT('.tw-faculty, .print-tw-faculty, .rev-tw-faculty, .fs-tw-faculty, .drw-tw-faculty', d.checked_by);
    setT('.tw-pno, .print-tw-pno, .rev-tw-pno, .fs-tw-pno, .drw-tw-pno, #drawer-tw-pno', pno ? String(pno) : '');
    setT('.tw-marks, .print-tw-marks, .rev-tw-marks, .fs-tw-marks, .drw-tw-marks, #drawer-tw-marks', d.marks);

    if (d.title.length > 36) {
      setT('.tw-title, .print-tw-title, .rev-tw-title, .fs-tw-title, .drw-tw-title, #drawer-tw-title', d.title.slice(0, 34));
      setT('.tw-title2, .print-tw-title2, .rev-tw-title2, .fs-tw-title2, .drw-tw-title2', d.title.slice(34));
    } else {
      setT('.tw-title, .print-tw-title, .rev-tw-title, .fs-tw-title, .drw-tw-title, #drawer-tw-title', d.title);
      setT('.tw-title2, .print-tw-title2, .rev-tw-title2, .fs-tw-title2, .drw-tw-title2', '');
    }

    const [cd, cm, cy] = splitDate(d.conducted_on);
    setT('.tw-cond-d, .print-tw-cond-d, .rev-tw-cond-d, .fs-tw-cond-d, .drw-tw-cond-d', cd);
    setT('.tw-cond-m, .print-tw-cond-m, .rev-tw-cond-m, .fs-tw-cond-m, .drw-tw-cond-m', cm);
    setT('.tw-cond-y, .print-tw-cond-y, .rev-tw-cond-y, .fs-tw-cond-y, .drw-tw-cond-y', cy);

    const [sd, sm, sy] = splitDate(d.date_of_sub);
    setT('.tw-sub-d, .print-tw-sub-d, .rev-tw-sub-d, .fs-tw-sub-d, .drw-tw-sub-d', sd);
    setT('.tw-sub-m, .print-tw-sub-m, .rev-tw-sub-m, .fs-tw-sub-m, .drw-tw-sub-m', sm);
    setT('.tw-sub-y, .print-tw-sub-y, .rev-tw-sub-y, .fs-tw-sub-y, .drw-tw-sub-y', sy);

    const [ad, am, ay] = splitDate(d.actual_sub);
    setT('.tw-actsub-d, .print-tw-actsub-d, .rev-tw-actsub-d, .fs-tw-actsub-d, .drw-tw-actsub-d', ad);
    setT('.tw-actsub-m, .print-tw-actsub-m, .rev-tw-actsub-m, .fs-tw-actsub-m, .drw-tw-actsub-m', am);
    setT('.tw-actsub-y, .print-tw-actsub-y, .rev-tw-actsub-y, .fs-tw-actsub-y, .drw-tw-actsub-y', ay);
  }

  // ── Toast Notifications ──
  function showToast(message, type = 'info') {
    const container = $('toast-container');
    if (!container) return;
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.innerHTML = `
      <span class="toast-icon">${type === 'success' ? '✓' : type === 'error' ? '⚠' : 'ℹ'}</span>
      <span class="toast-msg">${message}</span>
    `;
    container.appendChild(toast);
    setTimeout(() => {
      toast.classList.add('fade-out');
      setTimeout(() => toast.remove(), 400);
    }, 3200);
  }

  // ── Theme Switcher (.nb-l cream ruled / .nb-d slate paper) ──
  function applyTheme(theme, save = true) {
    const isDark = theme === 'dark';
    document.body.classList.toggle('nb-d', isDark);
    document.body.classList.toggle('nb-l', !isDark);
    const toggleBtn = $('theme-toggle');
    if (toggleBtn) toggleBtn.setAttribute('aria-checked', String(isDark));
    if (save) {
      try { localStorage.setItem('twf_theme', theme); } catch (_) {}
    }
  }

  const themeToggle = $('theme-toggle');
  if (themeToggle) {
    themeToggle.addEventListener('click', () => {
      const isCurrentlyDark = document.body.classList.contains('nb-d');
      applyTheme(isCurrentlyDark ? 'light' : 'dark', true);
    });
  }

  // Restore saved theme or user preference
  try {
    const savedTheme = localStorage.getItem('twf_theme');
    if (savedTheme) {
      applyTheme(savedTheme, false);
    } else if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
      applyTheme('dark', false);
    }
  } catch (_) {}

  // ── Stepper Navigation ──
  function setStep(stepNumber) {
    // GUARD 1: Block navigating past Step 1 without uploading Practical Index PDF!
    if (stepNumber > 1 && (!S.fileA || Object.keys(S.practicals).length === 0)) {
      showToast('⚠️ Please upload your Practical Index PDF in Step 1 first!', 'error');
      const card = $('card-index-file');
      if (card) {
        card.classList.add('pulse-alert');
        setTimeout(() => card.classList.remove('pulse-alert'), 900);
      }
      const input = $('idx-file-input');
      if (input) input.click();
      return;
    }

    // GUARD 2: Block proceeding to Step 3 or 4 without picking at least 1 practical
    if (stepNumber > 2 && S.selected.size === 0) {
      showToast('⚠️ Please pick at least one practical from the list!', 'error');
      setStep(2);
      return;
    }

    S.currentStep = stepNumber;

    // Switch view visibility
    for (let i = 1; i <= 5; i++) {
      const view = $(`view-step-${i}`);
      if (view) {
        view.classList.toggle('active', i === stepNumber);
        view.style.display = i === stepNumber ? 'block' : 'none';
      }
    }

    // Hide edit drawer when changing main steps
    closeDrawer();

    // Update Header Tabs
    const hasIndex = Boolean(S.fileA && Object.keys(S.practicals).length > 0);
    for (let i = 1; i <= 4; i++) {
      const tab = $(`tab-step-${i}`);
      const icon = $(`tab-icon-${i}`);
      if (!tab) continue;

      const activeTabNum = stepNumber > 4 ? 4 : stepNumber;
      tab.classList.toggle('on', i === activeTabNum);
      const isLocked = i > 1 && !hasIndex;
      tab.classList.toggle('locked', isLocked);

      if (i < activeTabNum) {
        tab.classList.add('done');
        if (icon) {
          icon.innerHTML = `<svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>`;
        }
      } else {
        tab.classList.remove('done');
        if (icon) icon.textContent = String(i);
      }
    }

    // Step-specific initialization
    if (stepNumber === 2) renderPracticalsStep();
    if (stepNumber === 3) syncDetailsStep();
    if (stepNumber === 4) initPrintStep();
    if (stepNumber === 5) initReviewStep();
  }

  // Wire Tab Clicks with Navigation Guarding
  for (let i = 1; i <= 4; i++) {
    const tab = $(`tab-step-${i}`);
    if (tab) {
      tab.addEventListener('click', () => {
        if (i > 1 && (!S.fileA || Object.keys(S.practicals).length === 0)) {
          showToast('⚠️ Please upload your Practical Index PDF in Step 1 first!', 'error');
          const card = $('card-index-file');
          if (card) {
            card.classList.add('pulse-alert');
            setTimeout(() => card.classList.remove('pulse-alert'), 900);
          }
          const input = $('idx-file-input');
          if (input) input.click();
          return;
        }
        setStep(i);
      });
    }
  }

  // ── STEP 1: Files ──
  const cardIndex = $('card-index-file');
  const inputIndex = $('idx-file-input');
  if (cardIndex && inputIndex) {
    cardIndex.addEventListener('click', () => inputIndex.click());

    ['dragover', 'dragenter'].forEach(ev => {
      cardIndex.addEventListener(ev, e => {
        e.preventDefault();
        cardIndex.classList.add('dragover');
      });
    });
    ['dragleave', 'drop'].forEach(ev => {
      cardIndex.addEventListener(ev, e => {
        e.preventDefault();
        cardIndex.classList.remove('dragover');
      });
    });

    cardIndex.addEventListener('drop', e => {
      e.preventDefault();
      if (e.dataTransfer.files && e.dataTransfer.files[0]) {
        handleIndexFile(e.dataTransfer.files[0]);
      }
    });

    inputIndex.addEventListener('change', () => {
      if (inputIndex.files && inputIndex.files[0]) {
        handleIndexFile(inputIndex.files[0]);
      }
    });
  }

  async function handleIndexFile(file) {
    if (!file.name.toLowerCase().endsWith('.pdf')) {
      showToast('Practical index must be a PDF file with selectable text.', 'error');
      return;
    }
    S.fileA = file;
    const nameEl = $('idx-file-name');
    if (nameEl) nameEl.textContent = file.name;

    const countEl = $('idx-practicals-count');
    if (countEl) countEl.textContent = 'Extracting practicals…';

    const scanLine = $('idx-scan-line');
    if (scanLine) scanLine.classList.add('scanning');

    showToast('Analyzing practical index…', 'info');

    const fd = new FormData();
    fd.append('pdf_a', file);

    try {
      const res = await fetch('/api/parse-index', { method: 'POST', body: fd });
      const data = await res.json();
      if (scanLine) scanLine.classList.remove('scanning');

      if (!res.ok || data.error) {
        showToast(`Could not read index: ${data.error || 'No practicals found in this file.'}`, 'error');
        S.fileA = null;
        if (countEl) countEl.textContent = 'Upload failed · Try another PDF';
        return;
      }

      if (data.practicals && Object.keys(data.practicals).length > 0) {
        S.practicals = data.practicals;
        // Select all practicals by default
        S.selected = new Set(Object.keys(data.practicals).map(Number));
        if (countEl) countEl.textContent = `✓ ${Object.keys(data.practicals).length} practicals found`;

        if (data.subject) {
          S.indexSubject = data.subject;
          S.formData.subject = data.subject;
          const subjTape = $('idx-subject-tape');
          if (subjTape) {
            subjTape.textContent = `Subject → ${data.subject}`;
            subjTape.style.display = 'inline-block';
          }
          const fSubj = $('f-subject');
          if (fSubj) fSubj.value = data.subject;
        }

        const card = $('card-index-file');
        if (card) card.classList.add('selected');

        // Unlock Stepper Tabs
        for (let i = 2; i <= 4; i++) {
          const tab = $(`tab-step-${i}`);
          if (tab) tab.classList.remove('locked');
        }

        showToast(`✓ Extracted ${Object.keys(data.practicals).length} practicals from index!`, 'success');

        // Auto-advance to Step 2 so user can review the practicals immediately!
        setTimeout(() => setStep(2), 500);
      } else {
        showToast('No practical experiments table detected in index PDF.', 'error');
        S.fileA = null;
        if (countEl) countEl.textContent = 'No practicals detected';
      }
    } catch (err) {
      if (scanLine) scanLine.classList.remove('scanning');
      showToast(`Error reading PDF: ${err.message}`, 'error');
      S.fileA = null;
      if (countEl) countEl.textContent = 'Upload failed';
    }
  }

  // ── Template Selection & Modal Logic ──
  const cardForm = $('card-form-file');
  const btnChangeTpl = $('btn-change-template-trigger');
  const tplModal = $('template-modal');
  const btnCloseTplModal = $('btn-close-template-modal');
  const tplModalDim = $('template-modal-dim');
  const inputForm = $('form-file-input');
  const formTrigger = $('btn-custom-form-trigger');

  function openTemplateModal() {
    if (tplModal) tplModal.style.display = 'flex';
  }
  function closeTemplateModal() {
    if (tplModal) tplModal.style.display = 'none';
  }

  if (cardForm) {
    cardForm.addEventListener('click', e => {
      if (e.target.closest('#form-file-input') || e.target.closest('#btn-custom-form-trigger')) return;
      openTemplateModal();
    });
  }
  if (btnChangeTpl) {
    btnChangeTpl.addEventListener('click', e => {
      e.stopPropagation();
      openTemplateModal();
    });
  }
  if (btnCloseTplModal) btnCloseTplModal.addEventListener('click', closeTemplateModal);
  if (tplModalDim) tplModalDim.addEventListener('click', closeTemplateModal);

  // Template Choices
  if (tplModal) {
    $$('.tpl-card', tplModal).forEach(card => {
      card.addEventListener('click', () => {
        const tpl = card.getAttribute('data-tpl');
        if (tpl === 'custom') {
          if (inputForm) inputForm.click();
          return;
        }
        selectTemplate(tpl);
        closeTemplateModal();
      });
    });
  }

  const btnTplUploadTrigger = $('btn-tpl-upload-trigger');
  if (btnTplUploadTrigger && inputForm) {
    btnTplUploadTrigger.addEventListener('click', e => {
      e.stopPropagation();
      inputForm.click();
    });
  }

  function selectTemplate(tplKey) {
    if (tplModal) {
      $$('.tpl-card', tplModal).forEach(c => c.classList.toggle('selected', c.getAttribute('data-tpl') === tplKey));
    }
    if (cardForm) cardForm.classList.add('selected');

    const titleEl = $('form-file-title');
    const subtextEl = $('form-file-subtext');

    if (tplKey === 'rngpatel') {
      S.fileB = null;
      if (titleEl) titleEl.textContent = 'R.N.G. Patel Institute of Technology';
      if (subtextEl) subtextEl.textContent = 'Ready-made form · Selected';
      showToast('✓ Selected official R.N.G. Patel Institute of Technology template!', 'success');
    }
  }

  if (formTrigger && inputForm) {
    formTrigger.addEventListener('click', e => {
      e.stopPropagation();
      inputForm.click();
    });
  }
  if (inputForm) {
    inputForm.addEventListener('change', () => {
      if (inputForm.files && inputForm.files[0]) {
        S.fileB = inputForm.files[0];
        const titleEl = $('form-file-title');
        const subtextEl = $('form-file-subtext');
        if (titleEl) titleEl.textContent = inputForm.files[0].name;
        if (subtextEl) subtextEl.textContent = 'Custom template · Uploaded';
        if (tplModal) {
          $$('.tpl-card', tplModal).forEach(c => c.classList.toggle('selected', c.getAttribute('data-tpl') === 'custom'));
        }
        closeTemplateModal();
        showToast('✓ Custom template uploaded successfully!', 'success');
      }
    });
  }

  // Continue to Step 2
  const btnStep1Continue = $('btn-step1-continue');
  if (btnStep1Continue) {
    btnStep1Continue.addEventListener('click', () => setStep(2));
  }

  // ── STEP 2: Practicals ──
  function renderPracticalsStep() {
    const list = $('practicals-list');
    if (!list) return;

    // Subject badge
    const badge = $('s2-subject-badge');
    if (badge) {
      if (S.indexSubject) {
        badge.textContent = `${S.indexSubject} · from index`;
        badge.style.display = 'inline-block';
      } else {
        badge.style.display = 'none';
      }
    }

    list.innerHTML = '';
    const entries = Object.entries(S.practicals).sort((a, b) => +a[0] - +b[0]);

    if (entries.length === 0) {
      list.innerHTML = `
        <div class="empty-practicals-box">
          <div class="ep-icon">📋</div>
          <h3>No Practicals Uploaded Yet</h3>
          <p>Please upload your Practical Index PDF in Step 1 to automatically extract all practical experiments.</p>
          <button type="button" class="go sm" id="btn-back-to-upload">← Upload Index PDF</button>
        </div>
      `;
      const btnBack = $('btn-back-to-upload');
      if (btnBack) btnBack.addEventListener('click', () => setStep(1));
      updatePracticalsSidebar();
      return;
    }

    entries.forEach(([sr, title], idx) => {
      const isSelected = S.selected.has(+sr);
      const li = document.createElement('li');
      li.className = `pr ${isSelected ? 'on' : ''}`;
      li.style.setProperty('--i', idx % 5);
      li.innerHTML = `
        <span class="pno hand">${sr}</span>
        <span class="pt">
          <span class="hl">${title}</span>
        </span>
        <span class="ck">
          <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
            <path class="tick" d="M5 13l4 4 10-11"></path>
          </svg>
        </span>
      `;
      li.addEventListener('click', () => {
        if (S.selected.has(+sr)) {
          S.selected.delete(+sr);
        } else {
          S.selected.add(+sr);
        }
        renderPracticalsStep();
      });
      list.appendChild(li);
    });

    updatePracticalsSidebar();
  }

  function updatePracticalsSidebar() {
    const count = S.selected.size;
    const sorted = Array.from(S.selected).sort((a, b) => a - b);

    // Page counters
    const sideCount = $('sidebar-page-count');
    if (sideCount) sideCount.textContent = String(count);
    const mobCount = $('mobile-selected-count');
    if (mobCount) mobCount.textContent = String(count);

    // Page Chips
    const chipsContainer = $('pchips-container');
    if (chipsContainer) {
      chipsContainer.innerHTML = '';
      sorted.forEach(num => {
        const chip = document.createElement('span');
        chip.textContent = `P${num}`;
        chipsContainer.appendChild(chip);
      });
    }

    // Fanned Miniature Sheets
    for (let i = 0; i < 3; i++) {
      const fanTw = $(`fan-tw-${i}`);
      if (!fanTw) continue;
      const titleEl = fanTw.querySelector('.tw-p-name');
      const pnoEl = fanTw.querySelector('.tw-p-no');
      if (sorted.length > 0 && sorted[i]) {
        const targetPno = sorted[i];
        const targetTitle = S.practicals[targetPno] || `Practical ${targetPno}`;
        if (titleEl) titleEl.textContent = targetTitle.length > 36 ? targetTitle.slice(0, 34) + '…' : targetTitle;
        if (pnoEl) pnoEl.textContent = String(targetPno);
      } else {
        if (titleEl) titleEl.textContent = '';
        if (pnoEl) pnoEl.textContent = '';
      }
    }
  }

  // Select All & Clear
  const btnSelectAll = $('btn-select-all');
  if (btnSelectAll) {
    btnSelectAll.addEventListener('click', () => {
      Object.keys(S.practicals).forEach(k => S.selected.add(+k));
      renderPracticalsStep();
    });
  }
  const btnClearAll = $('btn-clear-all');
  if (btnClearAll) {
    btnClearAll.addEventListener('click', () => {
      S.selected.clear();
      renderPracticalsStep();
    });
  }

  // Continue to Step 3
  const btnStep2Continue = $('btn-step2-continue');
  if (btnStep2Continue) {
    btnStep2Continue.addEventListener('click', () => {
      if (S.selected.size === 0) {
        showToast('Please pick at least one practical to proceed.', 'error');
        return;
      }
      setStep(3);
    });
  }
  const btnMobileStep2Continue = $('btn-mobile-step2-continue');
  if (btnMobileStep2Continue) {
    btnMobileStep2Continue.addEventListener('click', () => {
      if (S.selected.size === 0) {
        showToast('Please pick at least one practical to proceed.', 'error');
        return;
      }
      setStep(3);
    });
  }

  // ── STEP 3: Details & Live Miniature Writing ──
  const FIELD_MAP = [
    { input: 'f-student',   data: 'student_name', sheetText: 'tw-student',  targetSelector: '#tw-student' },
    { input: 'f-pen',       data: 'pen',          sheetText: 'tw-pen',      targetSelector: '#tw-pen' },
    { input: 'f-class',     data: 'class_name',   sheetText: 'tw-class',    targetSelector: '#tw-class' },
    { input: 'f-batch',     data: 'batch',        sheetText: 'tw-batch',    targetSelector: '#tw-batch' },
    { input: 'f-semester',  data: 'semester',     sheetText: 'tw-semester', targetSelector: '#tw-semester' },
    { input: 'f-term',      data: 'term',         sheetText: 'tw-term',     targetSelector: '#tw-term' },
    { input: 'f-subject',   data: 'subject',      sheetText: 'tw-subject',  targetSelector: '#tw-subject' },
    { input: 'f-faculty',   data: 'checked_by',   sheetText: 'tw-faculty',  targetSelector: '#tw-faculty' },
  ];

  function syncDetailsStep() {
    // Populate form inputs
    FIELD_MAP.forEach(({ input, data }) => {
      const el = $(input);
      if (el) el.value = S.formData[data] || '';
    });
    if ($('f-cond')) $('f-cond').value = S.formData.conducted_on || '';
    if ($('f-sub')) $('f-sub').value = S.formData.date_of_sub || '';
    if ($('f-actsub')) $('f-actsub').value = S.formData.actual_sub || '';

    // Update first selected practical header on live sheet
    const sorted = Array.from(S.selected).sort((a, b) => a - b);
    const p1 = sorted[0] || (Object.keys(S.practicals).length > 0 ? Number(Object.keys(S.practicals)[0]) : 1);
    const pHeader = $('live-practical-header');
    if (pHeader) pHeader.textContent = p1 ? `PRACTICAL ${p1}` : 'PREVIEW';

    const pTitle = S.practicals[p1] || "";
    const p1El = $('tw-pname1');
    const p2El = $('tw-pname2');
    const pnoEl = $('tw-pno');
    if (pnoEl) pnoEl.textContent = p1 ? String(p1) : '';

    if (pTitle.length > 38) {
      if (p1El) p1El.textContent = pTitle.slice(0, 36);
      if (p2El) p2El.textContent = pTitle.slice(36);
    } else {
      if (p1El) p1El.textContent = pTitle;
      if (p2El) p2El.textContent = '';
    }

    updateLiveSheet();
  }

  function updateLiveSheet() {
    // Sync text fields to sheet
    FIELD_MAP.forEach(({ data, sheetText }) => {
      const el = $(sheetText);
      if (el) el.textContent = S.formData[data] || '';
    });

    const [cd, cm, cy] = splitDate(S.formData.conducted_on);
    if ($('tw-cond-d')) $('tw-cond-d').textContent = cd;
    if ($('tw-cond-m')) $('tw-cond-m').textContent = cm;
    if ($('tw-cond-y')) $('tw-cond-y').textContent = cy;

    const [sd, sm, sy] = splitDate(S.formData.date_of_sub);
    if ($('tw-sub-d')) $('tw-sub-d').textContent = sd;
    if ($('tw-sub-m')) $('tw-sub-m').textContent = sm;
    if ($('tw-sub-y')) $('tw-sub-y').textContent = sy;

    const [ad, am, ay] = splitDate(S.formData.actual_sub);
    if ($('tw-actsub-d')) $('tw-actsub-d').textContent = ad;
    if ($('tw-actsub-m')) $('tw-actsub-m').textContent = am;
    if ($('tw-actsub-y')) $('tw-actsub-y').textContent = ay;

    // Filled counter
    let filled = 0;
    Object.values(S.formData).forEach(v => { if (v && String(v).trim()) filled++; });
    const counter = $('step3-filled-counter');
    if (counter) counter.textContent = String(filled);
  }

  // ── Moving Pen Follower with Dynamic Typing Tracker ──
  let penScribbleTimer = null;
  function movePenFollower(selector, isTyping = false) {
    const follower = $('tw-follower');
    const target = document.querySelector(selector);
    if (!follower || !target) return;

    follower.style.display = 'block';

    const xVal = parseFloat(target.style.getPropertyValue('--x')) || 200;
    const yVal = parseFloat(target.style.getPropertyValue('--y')) || 381;

    const leftPercent = (xVal / 744) * 100;
    const topPercent = (yVal / 1054) * 100;

    // Dynamically calculate rendered character width so pen moves as user types
    const textLen = (target.textContent || '').length;
    // Times New Roman character scaling on 744 width coordinate space
    const textWidthUnits = Math.max(16, textLen * 7.5 + 10);
    const widthPercent = (textWidthUnits / 744) * 100;

    follower.style.left = `${leftPercent}%`;
    follower.style.top = `calc(${topPercent}% - 2.5%)`;
    follower.style.width = `${Math.min(52, widthPercent)}%`;

    if (isTyping) {
      follower.classList.add('scribbling');
      if (penScribbleTimer) clearTimeout(penScribbleTimer);
      penScribbleTimer = setTimeout(() => {
        follower.classList.remove('scribbling');
      }, 250);
    }
  }

  // Wire live input change & moving pen follower
  FIELD_MAP.forEach(({ input, data, targetSelector }) => {
    const el = $(input);
    if (!el) return;

    el.addEventListener('input', () => {
      S.formData[data] = el.value;
      updateLiveSheet();
      movePenFollower(targetSelector, true);
    });

    el.addEventListener('focus', () => {
      movePenFollower(targetSelector, false);
    });
  });

  ['f-cond', 'f-sub', 'f-actsub'].forEach(id => {
    const el = $(id);
    if (!el) return;
    el.addEventListener('change', () => {
      if (id === 'f-cond') S.formData.conducted_on = el.value;
      if (id === 'f-sub') S.formData.date_of_sub = el.value;
      if (id === 'f-actsub') S.formData.actual_sub = el.value;
      updateLiveSheet();
      const target = id === 'f-cond' ? '#tw-cond-d' : id === 'f-sub' ? '#tw-sub-d' : '#tw-actsub-d';
      movePenFollower(target, true);
    });
    el.addEventListener('focus', () => {
      const target = id === 'f-cond' ? '#tw-cond-d' : id === 'f-sub' ? '#tw-sub-d' : '#tw-actsub-d';
      movePenFollower(target, false);
    });
  });

  // Clear All Form Fields Button
  const btnClearFormFields = $('btn-clear-form-fields');
  if (btnClearFormFields) {
    btnClearFormFields.addEventListener('click', () => {
      // Clear student details in state
      ['student_name', 'pen', 'class_name', 'batch', 'semester', 'term', 'conducted_on', 'date_of_sub', 'actual_sub', 'checked_by'].forEach(k => {
        S.formData[k] = '';
      });
      // Clear input element values
      FIELD_MAP.forEach(({ input }) => {
        const el = $(input);
        if (el && input !== 'f-subject') el.value = '';
      });
      ['f-cond', 'f-sub', 'f-actsub'].forEach(id => {
        const el = $(id);
        if (el) el.value = '';
      });

      // Clear any saved localStorage student profile
      try {
        localStorage.removeItem('twf_student_profile');
      } catch (_) {}

      updateLiveSheet();
      showToast('✓ All fields cleared! Ready for a new student.', 'info');
    });
  }

  // Make My Pages Button
  const btnGenerate = $('btn-step3-generate');
  if (btnGenerate) {
    btnGenerate.addEventListener('click', () => {
      setStep(4);
    });
  }

  // ── STEP 4: Print & Download ──
  let printInterval = null;
  function initPrintStep() {
    const sorted = Array.from(S.selected).sort((a, b) => a - b);
    const total = sorted.length;
    if (total === 0) return;

    // Immediately render printer emerging sheet with the first practical
    const currentEmergingPno = sorted[0];
    const printerSheet = $('printer-miniature-sheet');
    if (printerSheet) {
      renderTwSheet(printerSheet, currentEmergingPno);
    }

    // Animated LCD text & status chip
    const lcd = $('printer-lcd-text');
    const chip = $('printer-status-chip');
    let currentIdx = 0;
    if (printInterval) clearInterval(printInterval);

    if (lcd) lcd.textContent = `PRINTING 1/${total}`;
    if (chip) chip.textContent = `Page 1 of ${total}`;

    // Filmstrip
    const filmstrip = $('printer-filmstrip');
    if (filmstrip) {
      filmstrip.innerHTML = '';
      sorted.forEach((pno, i) => {
        const item = document.createElement('div');
        item.className = `film ${i === 0 ? 'cur' : ''}`;
        const d = getPracticalData(pno);
        item.innerHTML = `
          <div class="tw">
            <span class="t" style="--x:200;--y:381;">${escapeHtml(d.student_name)}</span>
            <span class="t" style="--x:123;--y:351;">${escapeHtml(d.pen)}</span>
            <span class="t" style="--x:142;--y:322;">${escapeHtml(d.subject)}</span>
            <span class="t" style="--x:514;--y:545;">${pno}</span>
            <span class="t" style="--x:604;--y:928;">${escapeHtml(d.marks)}</span>
          </div>
          <span class="flb">P${pno}</span>
        `;
        item.addEventListener('click', () => {
          if (printInterval) clearInterval(printInterval);
          $$('.film', filmstrip).forEach(f => f.classList.remove('cur'));
          item.classList.add('cur');
          currentIdx = i;
          if (chip) chip.textContent = `Page ${i + 1} of ${total}`;
          if (lcd) lcd.textContent = `P${pno} READY`;

          if (printerSheet) {
            renderTwSheet(printerSheet, pno);
          }
        });
        filmstrip.appendChild(item);
      });
    }

    // Loop printing animation
    printInterval = setInterval(() => {
      currentIdx = (currentIdx + 1) % total;
      const pno = sorted[currentIdx];
      if (lcd) {
        lcd.textContent = `PRINTING ${currentIdx + 1}/${total}`;
      }
      if (chip) {
        chip.textContent = `Page ${currentIdx + 1} of ${total}`;
      }
      if (printerSheet) {
        renderTwSheet(printerSheet, pno);
      }
      if (filmstrip) {
        const films = $$('.film', filmstrip);
        films.forEach((f, idx) => {
          f.classList.toggle('cur', idx === currentIdx);
        });
      }
    }, 2200);

    // Default Filename
    const renameInput = $('pdf-rename-input');
    if (renameInput) {
      const minP = sorted[0] || 1;
      const maxP = sorted[sorted.length - 1] || total;
      renameInput.value = `termworkforge_practicals_${minP === maxP ? minP : `${minP}-${maxP}`}`;
    }
  }

  // Rename Button Trigger
  const btnPencilRename = $('btn-pencil-rename');
  if (btnPencilRename) {
    btnPencilRename.addEventListener('click', () => {
      const input = $('pdf-rename-input');
      if (input) {
        input.focus();
        input.select();
      }
    });
  }

  // Download PDF Action
  const btnDownloadPdf = $('btn-download-pdf');
  if (btnDownloadPdf) {
    btnDownloadPdf.addEventListener('click', async () => {
      await executePdfDownload();
    });
  }

  // Review & Edit Button
  const btnOpenReview = $('btn-open-review');
  if (btnOpenReview) {
    btnOpenReview.addEventListener('click', () => setStep(5));
  }

  async function executePdfDownload() {
    const btn = $('btn-download-pdf');
    const btnText = $('dl-btn-text');
    const moreBox = $('generate-more-box');
    const lcd = $('printer-lcd-text');

    // Start download animation
    if (btn) btn.classList.add('downloading');
    if (btnText) btnText.textContent = 'Generating PDF…';
    if (lcd) lcd.textContent = 'STAMPING & BINDING…';
    showToast('Compiling your collegiate PDF…', 'info');

    const sorted = Array.from(S.selected).sort((a, b) => a - b);
    const titlesPayload = sorted.map(pno => ({
      sr_no: String(pno),
      title: S.practicals[pno] || `Practical ${pno}`,
      overrides: S.overrides[pno] || {}
    }));

    const fd = new FormData();
    fd.append('titles_json', JSON.stringify(titlesPayload));
    fd.append('form_json', JSON.stringify(S.formData));

    const renameInput = $('pdf-rename-input');
    const customName = renameInput ? renameInput.value.trim() : 'termworkforge_practicals';
    fd.append('filename', customName);

    // Fetch default R.N.G. Patel form if user didn't upload custom
    try {
      if (S.fileB) {
        fd.append('pdf_b', S.fileB);
      } else {
        const tplRes = await fetch('/static/templates/rngpatel_termwork.pdf');
        if (!tplRes.ok) throw new Error('Template not reachable');
        const tplBlob = await tplRes.blob();
        fd.append('pdf_b', tplBlob, 'rngpatel_termwork.pdf');
      }

      const res = await fetch('/api/generate', { method: 'POST', body: fd });
      if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        showToast(`Generation failed: ${err.error || 'Server error'}`, 'error');
        if (btn) btn.classList.remove('downloading');
        if (btnText) btnText.textContent = 'Download PDF';
        if (lcd) lcd.textContent = 'ERROR · RETRY';
        return;
      }

      const pdfBlob = await res.blob();
      const url = URL.createObjectURL(pdfBlob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `${customName}.pdf`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      URL.revokeObjectURL(url);

      // Download success celebration state
      if (btn) {
        btn.classList.remove('downloading');
        btn.classList.add('download-success');
      }
      if (btnText) btnText.textContent = '✓ Downloaded!';
      if (lcd) lcd.textContent = 'PDF READY ✓';

      // Reveal Generate More Term Works Box
      if (moreBox) {
        moreBox.style.display = 'block';
        moreBox.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
      }

      showToast('✓ Term work PDF downloaded successfully!', 'success');

      setTimeout(() => {
        if (btn) {
          btn.classList.remove('download-success');
          if (btnText) btnText.textContent = 'Download Again';
        }
      }, 3500);

    } catch (e) {
      if (btn) btn.classList.remove('downloading');
      if (btnText) btnText.textContent = 'Download PDF';
      if (lcd) lcd.textContent = 'ERROR';
      showToast(`Error: ${e.message}`, 'error');
    }
  }

  // Wire "Generate More Term Works" Actions
  const btnCreateAnother = $('btn-create-another-tw');
  if (btnCreateAnother) {
    btnCreateAnother.addEventListener('click', () => {
      // Clear student-specific fields for the next student
      ['student_name', 'pen', 'conducted_on', 'date_of_sub', 'actual_sub'].forEach(k => {
        S.formData[k] = '';
      });
      FIELD_MAP.forEach(({ input }) => {
        const el = $(input);
        if (el && (input === 'f-student' || input === 'f-pen')) el.value = '';
      });
      ['f-cond', 'f-sub', 'f-actsub'].forEach(id => {
        const el = $(id);
        if (el) el.value = '';
      });
      setStep(3);
      const sInput = $('f-student');
      if (sInput) sInput.focus();
      showToast('Ready to forge term work for the next student! Practicals preserved.', 'success');
    });
  }

  const btnEditCurrent = $('btn-edit-current-tw');
  if (btnEditCurrent) {
    btnEditCurrent.addEventListener('click', () => {
      setStep(5);
      initReviewStep();
    });
  }

  // ── STEP 5: Review View ──
  function initReviewStep() {
    const sorted = Array.from(S.selected).sort((a, b) => a - b);
    if (!sorted.includes(S.reviewPage)) {
      S.reviewPage = sorted[0] || 1;
    }

    // Populate Left Thumbnail Filmstrip
    const filmstrip = $('review-filmstrip');
    if (filmstrip) {
      filmstrip.innerHTML = '';
      sorted.forEach(pno => {
        const isCurrent = pno === S.reviewPage;
        const th = document.createElement('div');
        th.className = `th ${isCurrent ? 'cur' : ''}`;
        const d = getPracticalData(pno);
        th.innerHTML = `
          <div class="thc">
            <div class="tw">
              <span class="t" style="--x:200;--y:381;">${escapeHtml(d.student_name)}</span>
              <span class="t" style="--x:142;--y:322;">${escapeHtml(d.subject)}</span>
              <span class="t" style="--x:514;--y:545;">${pno}</span>
              <span class="t" style="--x:604;--y:928;">${escapeHtml(d.marks)}</span>
            </div>
          </div>
          <span class="tl">P${pno}</span>
          <span class="tck">
            <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round">
              <path d="M20 6 9 17l-5-5"/>
            </svg>
          </span>
        `;
        th.addEventListener('click', () => {
          S.reviewPage = pno;
          initReviewStep();
        });
        filmstrip.appendChild(th);
      });
    }

    // Update Inspected Sheet
    const sheet = $('review-inspected-sheet');
    if (sheet) {
      renderTwSheet(sheet, S.reviewPage);
    }

    // Metadata
    const total = sorted.length > 0 ? sorted.length : 1;
    const pageIndex = sorted.length > 0 ? (sorted.indexOf(S.reviewPage) >= 0 ? sorted.indexOf(S.reviewPage) + 1 : 1) : 1;
    const metaPage = $('review-meta-page');
    if (metaPage) metaPage.textContent = `Page ${pageIndex} of ${total}`;
    const metaPract = $('review-meta-practical');
    if (metaPract) metaPract.textContent = `Practical ${S.reviewPage || 1} · ${S.practicals[S.reviewPage] || ''}`;

    // Selected count for multi-edit
    const selCountEl = $('review-selected-count');
    if (selCountEl) selCountEl.textContent = String(Math.min(2, total));
  }

  // Segmented Zoom Knob
  const segFull = $('seg-btn-full');
  const segTop = $('seg-btn-top');
  const segBottom = $('seg-btn-bottom');
  const segKnob = $('seg-knob');
  const sheetWrap = $('review-sheet-wrap');

  function setReviewZoom(mode) {
    S.reviewZoom = mode;
    [segFull, segTop, segBottom].forEach(b => { if (b) b.classList.remove('on'); });
    if (sheetWrap) {
      sheetWrap.classList.remove('mode-full', 'mode-top', 'mode-bottom');
      sheetWrap.classList.add(`mode-${mode}`);
    }

    if (mode === 'full') {
      if (segFull) segFull.classList.add('on');
      if (segKnob) segKnob.style.left = '3px';
      if (sheetWrap) sheetWrap.style.transform = 'scale(1) translateY(0)';
    } else if (mode === 'top') {
      if (segTop) segTop.classList.add('on');
      if (segKnob) segKnob.style.left = 'calc((100% - 6px) / 3 + 3px)';
      if (sheetWrap) sheetWrap.style.transform = 'scale(1.5) translateY(14%)';
    } else if (mode === 'bottom') {
      if (segBottom) segBottom.classList.add('on');
      if (segKnob) segKnob.style.left = 'calc((100% - 6px) * 2 / 3 + 3px)';
      if (sheetWrap) sheetWrap.style.transform = 'scale(1.5) translateY(-26%)';
    }
  }

  if (segFull) segFull.addEventListener('click', () => setReviewZoom('full'));
  if (segTop) segTop.addEventListener('click', () => setReviewZoom('top'));
  if (segBottom) segBottom.addEventListener('click', () => setReviewZoom('bottom'));

  // Hotspots: Click hotspot to open Drawer focused on that field
  ['hs-title', 'hs-cond', 'hs-sub', 'hs-marks'].forEach(id => {
    const el = $(id);
    if (el) {
      el.addEventListener('click', () => {
        openDrawer('this');
      });
    }
  });

  // Action Buttons
  const btnEditThis = $('btn-edit-this-page');
  if (btnEditThis) btnEditThis.addEventListener('click', () => openDrawer('this'));

  const btnEditSelected = $('btn-edit-selected-pages');
  if (btnEditSelected) btnEditSelected.addEventListener('click', () => openDrawer('pick'));

  const btnEditAll = $('btn-edit-all-pages');
  if (btnEditAll) btnEditAll.addEventListener('click', () => openDrawer('all'));

  const btnReviewDownload = $('btn-review-download-pdf');
  if (btnReviewDownload) btnReviewDownload.addEventListener('click', executePdfDownload);

  // ── STEP 6: Edit Drawer Modal ──
  const drawerModal = $('edit-drawer-modal');
  const drawerDim = $('drawer-dim');
  const btnCloseDrawer = $('btn-close-drawer');

  function openDrawer(scope = 'this') {
    S.drawerScope = scope;
    if (!drawerModal) return;

    drawerModal.style.display = 'block';

    // Populate scope radio buttons
    ['this', 'pick', 'all'].forEach(s => {
      const opt = $(`scope-opt-${s}`);
      if (opt) opt.classList.toggle('on', s === scope);
    });

    const sorted = Array.from(S.selected).sort((a, b) => a - b);
    const labelThis = $('scope-label-this');
    if (labelThis) labelThis.textContent = `P${S.reviewPage || 1}`;

    const labelPick = $('scope-label-pick');
    if (labelPick) labelPick.textContent = sorted.length > 1 ? `P${sorted[0]}, P${sorted[1]}` : `P${sorted[0] || 1}`;

    const labelAll = $('scope-label-all');
    if (labelAll) labelAll.textContent = sorted.length > 0 ? `P${sorted[0]} – P${sorted[sorted.length - 1]}` : `All pages`;

    // Populate ALL 12 Input Fields for Full Term Work Customization
    const curPno = S.reviewPage;
    const curTitle = S.practicals[curPno] || '';
    const ov = S.overrides[curPno] || {};

    if ($('drawer-input-title')) $('drawer-input-title').value = curTitle;
    if ($('drawer-input-subject')) $('drawer-input-subject').value = ov.subject || S.formData.subject || '';
    if ($('drawer-input-student')) $('drawer-input-student').value = ov.student_name || S.formData.student_name || '';
    if ($('drawer-input-pen')) $('drawer-input-pen').value = ov.pen || S.formData.pen || '';
    if ($('drawer-input-class')) $('drawer-input-class').value = ov.class_name || S.formData.class_name || '';
    if ($('drawer-input-batch')) $('drawer-input-batch').value = ov.batch || S.formData.batch || '';
    if ($('drawer-input-sem')) $('drawer-input-sem').value = ov.semester || S.formData.semester || '';
    if ($('drawer-input-term')) $('drawer-input-term').value = ov.term || S.formData.term || '';
    if ($('drawer-input-cond')) $('drawer-input-cond').value = ov.conducted_on || S.formData.conducted_on || '';
    if ($('drawer-input-sub')) $('drawer-input-sub').value = ov.date_of_sub || S.formData.date_of_sub || '';
    if ($('drawer-input-actsub')) $('drawer-input-actsub').value = ov.actual_sub || S.formData.actual_sub || '';
    if ($('drawer-input-faculty')) $('drawer-input-faculty').value = ov.checked_by || S.formData.checked_by || '';
    if ($('drawer-input-marks')) $('drawer-input-marks').value = ov.marks || S.formData.marks || '10';

    // Update Live Drawer Sheet
    const drawerTw = $('drawer-preview-tw');
    if (drawerTw) {
      renderTwSheet(drawerTw, curPno);
    }

    updateDrawerScopeUi();
  }

  function closeDrawer() {
    if (drawerModal) drawerModal.style.display = 'none';
  }

  if (btnCloseDrawer) btnCloseDrawer.addEventListener('click', closeDrawer);
  if (drawerDim) drawerDim.addEventListener('click', closeDrawer);

  // Scope Option Toggles
  ['this', 'pick', 'all'].forEach(s => {
    const opt = $(`scope-opt-${s}`);
    if (opt) {
      opt.addEventListener('click', () => {
        S.drawerScope = s;
        ['this', 'pick', 'all'].forEach(o => {
          const el = $(`scope-opt-${o}`);
          if (el) el.classList.toggle('on', o === s);
        });
        updateDrawerScopeUi();
      });
    }
  });

  function updateDrawerScopeUi() {
    const chipsBox = $('drawer-pick-chips');
    const btnLabel = $('drawer-btn-label');
    const sorted = Array.from(S.selected).sort((a, b) => a - b);

    if (S.drawerScope === 'pick') {
      if (chipsBox) {
        chipsBox.style.display = 'flex';
        chipsBox.innerHTML = '';
        sorted.forEach(pno => {
          const chip = document.createElement('span');
          chip.className = `pc ${S.drawerPickedPages.has(pno) ? 'cur' : ''}`;
          chip.innerHTML = `<i></i>P${pno}`;
          chip.addEventListener('click', () => {
            if (S.drawerPickedPages.has(pno)) {
              S.drawerPickedPages.delete(pno);
            } else {
              S.drawerPickedPages.add(pno);
            }
            updateDrawerScopeUi();
          });
          chipsBox.appendChild(chip);
        });
      }
      if (btnLabel) btnLabel.textContent = `Apply to ${S.drawerPickedPages.size} pages`;
    } else {
      if (chipsBox) chipsBox.style.display = 'none';
      if (btnLabel) {
        btnLabel.textContent = S.drawerScope === 'this' ? 'Apply to 1 page' : `Apply to all ${sorted.length} pages`;
      }
    }
  }

  // Apply Changes Button
  const btnApplyDrawer = $('btn-apply-drawer-changes');
  if (btnApplyDrawer) {
    btnApplyDrawer.addEventListener('click', () => {
      const newTitle = $('drawer-input-title') ? $('drawer-input-title').value.trim() : '';
      const newSubj = $('drawer-input-subject') ? $('drawer-input-subject').value.trim() : '';
      const newStudent = $('drawer-input-student') ? $('drawer-input-student').value.trim() : '';
      const newPen = $('drawer-input-pen') ? $('drawer-input-pen').value.trim() : '';
      const newClass = $('drawer-input-class') ? $('drawer-input-class').value.trim() : '';
      const newBatch = $('drawer-input-batch') ? $('drawer-input-batch').value.trim() : '';
      const newSem = $('drawer-input-sem') ? $('drawer-input-sem').value.trim() : '';
      const newTerm = $('drawer-input-term') ? $('drawer-input-term').value.trim() : '';
      const newCond = $('drawer-input-cond') ? $('drawer-input-cond').value : '';
      const newSub = $('drawer-input-sub') ? $('drawer-input-sub').value : '';
      const newActSub = $('drawer-input-actsub') ? $('drawer-input-actsub').value : '';
      const newFaculty = $('drawer-input-faculty') ? $('drawer-input-faculty').value.trim() : '';
      const newMarks = $('drawer-input-marks') ? $('drawer-input-marks').value.trim() : '';

      const sorted = Array.from(S.selected).sort((a, b) => a - b);
      let targetPages = [];

      if (S.drawerScope === 'this') {
        targetPages = [S.reviewPage];
      } else if (S.drawerScope === 'pick') {
        targetPages = Array.from(S.drawerPickedPages);
      } else {
        targetPages = sorted;
      }

      targetPages.forEach(pno => {
        if (newTitle) S.practicals[pno] = newTitle;
        if (!S.overrides[pno]) S.overrides[pno] = {};
        if (newSubj) S.overrides[pno].subject = newSubj;
        if (newStudent) S.overrides[pno].student_name = newStudent;
        if (newPen) S.overrides[pno].pen = newPen;
        if (newClass) S.overrides[pno].class_name = newClass;
        if (newBatch) S.overrides[pno].batch = newBatch;
        if (newSem) S.overrides[pno].semester = newSem;
        if (newTerm) S.overrides[pno].term = newTerm;
        if (newCond) S.overrides[pno].conducted_on = newCond;
        if (newSub) S.overrides[pno].date_of_sub = newSub;
        if (newActSub) S.overrides[pno].actual_sub = newActSub;
        if (newFaculty) S.overrides[pno].checked_by = newFaculty;
        if (newMarks) S.overrides[pno].marks = newMarks;
      });

      // Sync shared formData if updating all or current page
      if (S.drawerScope === 'all' || targetPages.includes(S.reviewPage)) {
        if (newSubj) S.formData.subject = newSubj;
        if (newStudent) S.formData.student_name = newStudent;
        if (newPen) S.formData.pen = newPen;
        if (newClass) S.formData.class_name = newClass;
        if (newBatch) S.formData.batch = newBatch;
        if (newSem) S.formData.semester = newSem;
        if (newTerm) S.formData.term = newTerm;
        if (newCond) S.formData.conducted_on = newCond;
        if (newSub) S.formData.date_of_sub = newSub;
        if (newActSub) S.formData.actual_sub = newActSub;
        if (newFaculty) S.formData.checked_by = newFaculty;
        if (newMarks) S.formData.marks = newMarks;
      }

      closeDrawer();
      initReviewStep();
      showToast(`✓ All details successfully updated on ${targetPages.length} page${targetPages.length > 1 ? 's' : ''}!`, 'success');
    });
  }

  // ── Full Screen Preview Controller ──
  const fsModal = $('fullscreen-modal');
  const fsDim = $('fullscreen-modal-dim');
  const btnCloseFsModal = $('btn-close-fs-modal');
  const btnFsPrev = $('btn-fs-prev');
  const btnFsNext = $('btn-fs-next');
  let fsCurrentPage = 1;

  function openFullscreenPreview(pno = null) {
    if (!fsModal) return;
    const sorted = Array.from(S.selected).sort((a, b) => a - b);
    let targetPno = pno;
    if (!targetPno || (sorted.length > 0 && !sorted.includes(targetPno))) {
      targetPno = (sorted.length > 0 ? sorted[0] : null) || S.reviewPage || (Object.keys(S.practicals).length > 0 ? Number(Object.keys(S.practicals)[0]) : 1);
    }
    fsCurrentPage = targetPno || 1;

    renderFullscreenSheet(fsCurrentPage);
    fsModal.style.display = 'flex';
    document.body.style.overflow = 'hidden';
  }

  function closeFullscreenPreview() {
    if (!fsModal) return;
    fsModal.style.display = 'none';
    document.body.style.overflow = '';
  }

  function renderFullscreenSheet(pno) {
    const sorted = Array.from(S.selected).sort((a, b) => a - b);
    const idx = sorted.indexOf(pno);
    const total = sorted.length > 0 ? sorted.length : 1;
    const displayPageNum = idx >= 0 ? idx + 1 : 1;

    // Header updates
    const badge = $('fs-page-badge');
    if (badge) badge.textContent = `Page ${displayPageNum} of ${total}`;

    const titleEl = $('fs-page-title');
    const pTitle = S.practicals[pno] || (pno ? `Practical ${pno}` : 'Term Work Preview');
    if (titleEl) titleEl.textContent = `Practical ${pno || 1} · ${pTitle}`;

    const indicator = $('fs-page-indicator');
    if (indicator) indicator.textContent = `${displayPageNum} / ${total}`;

    // Previous / Next button states
    if (btnFsPrev) btnFsPrev.disabled = sorted.length <= 1 || idx <= 0;
    if (btnFsNext) btnFsNext.disabled = sorted.length <= 1 || idx >= sorted.length - 1;

    // Populate sheet values
    const fsTw = $('fs-inspected-sheet');
    if (fsTw) {
      renderTwSheet(fsTw, pno);
    }
  }

  if (btnCloseFsModal) btnCloseFsModal.addEventListener('click', closeFullscreenPreview);
  if (fsDim) fsDim.addEventListener('click', closeFullscreenPreview);

  if (btnFsPrev) {
    btnFsPrev.addEventListener('click', () => {
      const sorted = Array.from(S.selected).sort((a, b) => a - b);
      if (sorted.length === 0) return;
      const idx = sorted.indexOf(fsCurrentPage);
      if (idx > 0) {
        fsCurrentPage = sorted[idx - 1];
        renderFullscreenSheet(fsCurrentPage);
      }
    });
  }

  if (btnFsNext) {
    btnFsNext.addEventListener('click', () => {
      const sorted = Array.from(S.selected).sort((a, b) => a - b);
      if (sorted.length === 0) return;
      const idx = sorted.indexOf(fsCurrentPage);
      if (idx < sorted.length - 1) {
        fsCurrentPage = sorted[idx + 1];
        renderFullscreenSheet(fsCurrentPage);
      }
    });
  }

  // Keyboard navigation for Fullscreen Modal
  window.addEventListener('keydown', e => {
    if (!fsModal || fsModal.style.display !== 'flex') return;
    if (e.key === 'Escape') {
      closeFullscreenPreview();
    } else if (e.key === 'ArrowLeft' && btnFsPrev) {
      btnFsPrev.click();
    } else if (e.key === 'ArrowRight' && btnFsNext) {
      btnFsNext.click();
    }
  });

  // Connect triggers
  const btnTriggerFs = $('btn-trigger-fullscreen-preview');
  if (btnTriggerFs) {
    btnTriggerFs.addEventListener('click', (e) => {
      e.preventDefault();
      e.stopPropagation();
      openFullscreenPreview(S.reviewPage || 1);
    });
  }
  const btnStep3Fs = $('btn-step3-fs-preview');
  if (btnStep3Fs) {
    btnStep3Fs.addEventListener('click', (e) => {
      e.preventDefault();
      e.stopPropagation();
      const sorted = Array.from(S.selected).sort((a, b) => a - b);
      openFullscreenPreview(sorted[0] || 1);
    });
  }

  // ── Dismiss Cold-Start Banner ──
  const coldBannerClose = $('cold-banner-close');
  if (coldBannerClose) {
    coldBannerClose.addEventListener('click', () => {
      const b = $('cold-banner');
      if (b) b.remove();
    });
  }

  // Initialize App on Step 1
  setStep(1);

})();

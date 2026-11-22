import sys

index_html_clean = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>TermWorkForge — Spiral-Bound College Notebook</title>
  <meta name="description" content="Generate complete, perfectly aligned student term work and practical PDFs in seconds."/>
  
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Caveat:wght@700&family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@600;700&display=swap" rel="stylesheet">
  
  <link rel="icon" type="image/x-icon" href="/static/favicon.ico">
  <link rel="icon" type="image/png" sizes="192x192" href="/static/favicon-192.png">
  <link rel="apple-touch-icon" href="/static/apple-touch-icon.png">
  
  <link rel="stylesheet" href="/static/css/notebook.css?v=2.5"/>
</head>
<body class="nb-l">

  <!-- Cold-Start Wake-up Banner (Render Free Tier) -->
  <div id="cold-banner">
    <span style="font-size:16px;">⏳</span>
    <span>Server is waking up — this takes ~20 seconds on first visit. Almost ready!</span>
    <button id="cold-banner-close" type="button" aria-label="Dismiss banner">✕</button>
  </div>

  <!-- Main College Notebook Container -->
  <div class="notebook-app">
    
    <!-- Top Notebook Spine Header (Brand, Step Tabs, Theme Switch) -->
    <header class="notebook-header">
      <a href="/" class="brand" aria-label="TermWorkForge Home">
        <span class="lg">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
            <path d="M4 19.5V5a2 2 0 0 1 2-2h13v16H6a2 2 0 0 0-2 2Z"></path>
            <path d="M8 7h7M8 11h5"></path>
          </svg>
        </span>
        <b>TermWorkForge</b>
      </a>

      <!-- Color Index Tabs (Wizard Stepper) -->
      <nav class="tabs" role="tablist" aria-label="Notebook Steps">
        <div class="tab t1 on" id="tab-step-1" role="tab" tabindex="0">
          <b>1</b>Files
        </div>
        <div class="tab t2" id="tab-step-2" role="tab" tabindex="0">
          <b>2</b>Practicals
        </div>
        <div class="tab t3" id="tab-step-3" role="tab" tabindex="0">
          <b>3</b>Details
        </div>
        <div class="tab t4" id="tab-step-4" role="tab" tabindex="0">
          <b>4</b>Print
        </div>
      </nav>

      <!-- Sun / Moon Theme Toggle -->
      <button type="button" class="tg" id="theme-toggle" aria-label="Switch between light and dark theme">
        <i></i>
        <span class="s">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
            <circle cx="12" cy="12" r="4"></circle>
            <path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"></path>
          </svg>
        </span>
        <span class="m">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
            <path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8Z"></path>
          </svg>
        </span>
      </button>
    </header>

    <!-- Physical Ruled Notebook Body -->
    <main class="notebook-body">
      
      <!-- Desktop Spiral Binder Rings (Left Spine) -->
      <div class="rings" aria-hidden="true">
        <i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i>
      </div>

      <!-- Mobile Punched Binder Holes -->
      <div class="holes" aria-hidden="true">
        <i></i><i></i><i></i>
      </div>

      <!-- ====================================================================
           STEP 1: FILES
           ==================================================================== -->
      <div class="step-view active" id="view-step-1">
        <div class="s1-grid">
          <div class="s1-l">
            <span class="note">today\'s to-do ✓</span>
            <h1 class="hand h1">Get term work <span class="mk">off your list</span></h1>
            <svg class="squig" viewBox="0 0 160 10" width="150" height="9" aria-hidden="true">
              <path d="M2 6c14-7 26 5 40 0s26-6 40 0 26 5 40 0 20-3 36 0" fill="none" stroke="var(--pen)" stroke-width="3" stroke-linecap="round"></path>
            </svg>
            <p class="sub">Drop in the two files. We fill every page, you take the credit.</p>
            <ol class="how">
              <li><b>1</b>We read your index</li>
              <li><b>2</b>Pick the practicals</li>
              <li><b>3</b>Preview, edit, print</li>
            </ol>
          </div>

          <div class="s1-r">
            <!-- Clipped Index PDF Card -->
            <div class="att idx" id="card-index-file" title="Click or drop your Practical Index PDF here">
              <span class="clip">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                  <path d="m21.4 11.1-9.2 9.2a6 6 0 0 1-8.5-8.5l9.2-9.2a4 4 0 0 1 5.7 5.7l-9.2 9.2a2 2 0 0 1-2.8-2.8l8.5-8.5"></path>
                </svg>
              </span>
              <div class="pdfm">
                <i></i><i></i><i></i><i></i><i></i><i></i>
                <u class="scan" id="idx-scan-line"></u>
              </div>
              <div class="att-t">
                <b id="idx-file-name">Upload Practical Index PDF</b>
                <em class="found" id="idx-status-badge">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                    <path d="M20 6 9 17l-5-5"></path>
                  </svg>
                  <span id="idx-practicals-count">0 practicals found</span>
                </em>
                <span class="tape" id="idx-subject-tape">Subject → Auto-detect from index</span>
              </div>
              <input type="file" id="idx-file-input" accept=".pdf" style="display:none;"/>
            </div>

            <!-- Pinned Form Template Card -->
            <div class="att frm" id="card-form-file" title="Click to view or upload custom college form template">
              <span class="pin"></span>
              <div class="ftw">
                <!-- Exact R.N.G. Patel College Sheet Miniature -->
                <div class="tw">
                  <span class="t" style="--x:200;--y:381;">Student Name</span>
                  <span class="t" style="--x:123;--y:351;">250843131022</span>
                  <span class="t" style="--x:131;--y:405;">CSE-24-C</span>
                  <span class="t" style="--x:586;--y:405;">C2</span>
                  <span class="t" style="--x:601;--y:351;">5th</span>
                  <span class="t" style="--x:627;--y:289;">2026-27</span>
                  <span class="t" style="--x:142;--y:322;">Operating Systems</span>
                  <span class="t" style="--x:176;--y:725;">Prof. Faculty</span>
                  <span class="t" style="--x:356;--y:435;">Experiment Title</span>
                  <span class="t" style="--x:514;--y:545;">1</span>
                </div>
              </div>
              <div class="att-t">
                <b id="form-file-title">R.N.G. Patel Institute of Technology</b>
                <em>Ready-made form · selected</em>
                <span class="stamp">VERIFIED</span>
                <span class="own" id="btn-custom-form-trigger">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                    <path d="M12 16V4"></path>
                    <path d="m7 9 5-5 5 5"></path>
                    <path d="M5 20h14"></path>
                  </svg>
                  upload your own instead
                </span>
              </div>
              <input type="file" id="form-file-input" accept=".pdf,image/*,.docx" style="display:none;"/>
            </div>

            <!-- Continue Button -->
            <div style="margin-top: 6px;">
              <button type="button" class="go" id="btn-step1-continue" style="width: 100%;">
                Continue 
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                  <path d="M5 12h14"></path>
                  <path d="m13 6 6 6-6 6"></path>
                </svg>
              </button>
            </div>
            <span class="tip">tip: subject &amp; practicals come from your index ✎</span>
          </div>
        </div>
      </div>

      <!-- ====================================================================
           STEP 2: PRACTICALS
           ==================================================================== -->
      <div class="step-view" id="view-step-2">
        <div class="s2-grid">
          <div class="s2-m">
            <div class="s2-h">
              <h2 class="hand h2">Pick your practicals</h2>
              <span class="tape" id="s2-subject-badge">Operating Systems · from index</span>
            </div>

            <div class="tools">
              <button type="button" class="ghost" id="btn-select-all">Select all</button>
              <button type="button" class="ghost" id="btn-clear-all">Clear</button>
            </div>

            <!-- Ruled Practicals List -->
            <ul class="plist" id="practicals-list">
              <!-- Dynamically populated via JS -->
            </ul>
          </div>

          <!-- Practicals Sidebar -->
          <aside class="s2-sidebar">
            <span style="font-size: 11px; font-weight: 800; letter-spacing: .12em; color: var(--mut);">YOUR PAGES</span>
            <div class="big hand">
              <span id="sidebar-page-count">0</span>
              <small>pages</small>
            </div>
            
            <div class="fan">
              <div class="sk sk2">
                <div class="tw" id="fan-tw-2">
                  <span class="t tw-p-name" style="--x:356;--y:435;">Practical 3</span>
                  <span class="t tw-p-no" style="--x:514;--y:545;">3</span>
                </div>
              </div>
              <div class="sk sk1">
                <div class="tw" id="fan-tw-1">
                  <span class="t tw-p-name" style="--x:356;--y:435;">Practical 2</span>
                  <span class="t tw-p-no" style="--x:514;--y:545;">2</span>
                </div>
              </div>
              <div class="sk sk0">
                <div class="tw" id="fan-tw-0">
                  <span class="t tw-p-name" style="--x:356;--y:435;">Practical 1</span>
                  <span class="t tw-p-no" style="--x:514;--y:545;">1</span>
                </div>
              </div>
            </div>

            <div class="pchips" id="pchips-container">
              <!-- Populated via JS -->
            </div>

            <button type="button" class="go" id="btn-step2-continue" style="width: 100%; margin-top: 6px;">
              Continue 
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                <path d="M5 12h14"></path>
                <path d="m13 6 6 6-6 6"></path>
              </svg>
            </button>
          </aside>
        </div>
      </div>

      <!-- ====================================================================
           STEP 3: DETAILS (LIVE WRITING)
           ==================================================================== -->
      <div class="step-view" id="view-step-3">
        <div class="s3-grid">
          <!-- Form Inputs Column -->
          <div class="s3-f">
            <h2 class="hand h2" style="margin-bottom: 8px;">Fill the sheet</h2>
            
            <div class="fields-grid">
              <label class="fl sp-6 w-full">
                <span class="fn">Student name</span>
                <input type="text" class="in" id="f-student" placeholder="e.g. Aarav Mehta" autocomplete="name"/>
              </label>

              <label class="fl sp-3 w-half">
                <span class="fn">PEN / Roll No</span>
                <input type="text" class="in" id="f-pen" placeholder="e.g. 250843131022"/>
              </label>

              <label class="fl sp-3 w-half">
                <span class="fn">Class</span>
                <input type="text" class="in" id="f-class" placeholder="e.g. CSE-24-C"/>
              </label>

              <label class="fl sp-2 w-half">
                <span class="fn">Batch</span>
                <input type="text" class="in" id="f-batch" placeholder="e.g. C2"/>
              </label>

              <label class="fl sp-2 w-half">
                <span class="fn">Semester</span>
                <input type="text" class="in" id="f-semester" placeholder="e.g. 5th"/>
              </label>

              <label class="fl sp-2 w-half">
                <span class="fn">Term</span>
                <input type="text" class="in" id="f-term" placeholder="e.g. 2026-27"/>
              </label>

              <label class="fl sp-6 w-full">
                <span class="fn">Subject <b class="auto">auto from index</b></span>
                <input type="text" class="in" id="f-subject" placeholder="e.g. Operating Systems (1CS)"/>
              </label>

              <label class="fl sp-2 w-half">
                <span class="fn">Conducted on</span>
                <input type="date" class="in" id="f-cond"/>
              </label>

              <label class="fl sp-2 w-half">
                <span class="fn">Date of submission</span>
                <input type="date" class="in" id="f-sub"/>
              </label>

              <label class="fl sp-2 w-half">
                <span class="fn">Actual submission</span>
                <input type="date" class="in" id="f-actsub"/>
              </label>

              <label class="fl sp-4 w-half">
                <span class="fn">Checked by (Faculty)</span>
                <input type="text" class="in" id="f-faculty" placeholder="e.g. Prof. S. Desai"/>
              </label>

              <label class="fl sp-2 w-half">
                <span class="fn">Default Marks</span>
                <input type="text" class="in" id="f-marks" placeholder="10" value="10"/>
              </label>
            </div>

            <div style="margin-top: 14px;">
              <button type="button" class="go" id="btn-step3-generate" style="width: 100%;">
                Make my pages 
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                  <path d="M5 12h14"></path>
                  <path d="m13 6 6 6-6 6"></path>
                </svg>
              </button>
            </div>
          </div>

          <!-- Live Miniature Sheet View -->
          <div class="s3-p">
            <div class="lv">
              <span style="font-size: 11px; font-weight: 800; letter-spacing: .12em; color: var(--mut);" id="live-practical-header">LIVE · PRACTICAL 1</span>
              <span class="rec">writing</span>
            </div>
            
            <div class="cam">
              <div class="tw" id="live-writing-sheet">
                <span class="t" id="tw-student" style="--x:200;--y:381;">Aarav Mehta</span>
                <span class="t" id="tw-pen" style="--x:123;--y:351;">250843131022</span>
                <span class="t" id="tw-class" style="--x:131;--y:405;">CSE-24-C</span>
                <span class="t" id="tw-batch" style="--x:586;--y:405;">C2</span>
                <span class="t" id="tw-semester" style="--x:601;--y:351;">5th</span>
                <span class="t" id="tw-term" style="--x:627;--y:289;">2026-27</span>
                <span class="t" id="tw-subject" style="--x:142;--y:322;">Operating Systems (1CS)</span>
                
                <span class="t" id="tw-cond-d" style="--x:523;--y:576;">12</span>
                <span class="t" id="tw-cond-m" style="--x:570;--y:576;">08</span>
                <span class="t" id="tw-cond-y" style="--x:613;--y:576;">2026</span>
                
                <span class="t" id="tw-sub-d" style="--x:523;--y:604;">19</span>
                <span class="t" id="tw-sub-m" style="--x:570;--y:604;">08</span>
                <span class="t" id="tw-sub-y" style="--x:613;--y:604;">2026</span>
                
                <span class="t" id="tw-actsub-d" style="--x:523;--y:632;">19</span>
                <span class="t" id="tw-actsub-m" style="--x:570;--y:632;">08</span>
                <span class="t" id="tw-actsub-y" style="--x:613;--y:632;">2026</span>
                
                <span class="t" id="tw-faculty" style="--x:176;--y:725;">Prof. S. Desai</span>
                <span class="t" id="tw-pname1" style="--x:356;--y:435;">Demonstrate Basic and Advanced Linux</span>
                <span class="t" id="tw-pname2" style="--x:92;--y:467;">Command.</span>
                <span class="t" id="tw-pno" style="--x:514;--y:545;">1</span>
                <span class="t" id="tw-marks" style="--x:604;--y:928;">10</span>

                <!-- Live Pen & Highlighter Box Tracking Focused Field -->
                <i class="hb" id="tw-follower" aria-hidden="true" style="display:none;">
                  <svg class="hpen" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M17 3a2.85 2.83 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5Z"></path>
                  </svg>
                </i>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- ====================================================================
           STEP 4: PRINTING & DOWNLOAD
           ==================================================================== -->
      <div class="step-view" id="view-step-4">
        <div class="s4-grid">
          <!-- Printer Slot Mechanism -->
          <div class="s4-st">
            <div class="prt">
              <div class="prt-top">
                <div class="lcd" id="printer-lcd-text">READY</div>
                <div class="leds">
                  <i class="g"></i><i></i>
                </div>
              </div>
              <div class="prt-slot"></div>
            </div>

            <div class="pwin">
              <div class="sw animating" id="printer-animated-sheet">
                <div class="tw" id="printer-miniature-sheet">
                  <span class="t print-tw-student" style="--x:200;--y:381;">Aarav Mehta</span>
                  <span class="t print-tw-pen" style="--x:123;--y:351;">250843131022</span>
                  <span class="t print-tw-class" style="--x:131;--y:405;">CSE-24-C</span>
                  <span class="t print-tw-batch" style="--x:586;--y:405;">C2</span>
                  <span class="t print-tw-sem" style="--x:601;--y:351;">5th</span>
                  <span class="t print-tw-term" style="--x:627;--y:289;">2026-27</span>
                  <span class="t print-tw-subj" style="--x:142;--y:322;">Operating Systems</span>
                  <span class="t print-tw-faculty" style="--x:176;--y:725;">Prof. S. Desai</span>
                  <span class="t print-tw-title" style="--x:356;--y:435;">Linux Commands Demo</span>
                  <span class="t print-tw-pno" style="--x:514;--y:545;">1</span>
                  <span class="t print-tw-marks" style="--x:604;--y:928;">10</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Download & Review Details -->
          <div class="s4-sd">
            <div class="s4-h">
              <h2 class="hand h2">Fresh from the printer</h2>
              <span class="chip" id="printer-status-chip">Page 1 of 4</span>
            </div>

            <!-- Filmstrip -->
            <div class="films" id="printer-filmstrip">
              <!-- Populated dynamically via JS -->
            </div>

            <!-- Rename Box -->
            <div class="namebox">
              <input type="text" id="pdf-rename-input" aria-label="File name" value="termworkforge_practicals"/>
              <span>.pdf</span>
              <button type="button" id="btn-pencil-rename" aria-label="Rename file">
                <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                  <path d="M17 3a2.85 2.83 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5Z"></path>
                </svg>
              </button>
            </div>

            <!-- Actions -->
            <div class="act2">
              <button type="button" class="go dl" id="btn-download-pdf">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                  <path d="M12 15V3"></path>
                  <path d="m7 10 5 5 5-5"></path>
                  <path d="M5 21h14"></path>
                </svg>
                Download PDF
              </button>
              <button type="button" class="ghost" id="btn-open-review">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                  <path d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7-10-7-10-7Z"></path>
                  <circle cx="12" cy="12" r="3"></circle>
                </svg>
                Review &amp; edit
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- ====================================================================
           STEP 5: REVIEW VIEW
           ==================================================================== -->
      <div class="step-view" id="view-step-5">
        <div class="s5-grid">
          <!-- Thumbnail Filmstrip (Left Column) -->
          <div class="s5-l" id="review-filmstrip">
            <!-- Populated via JS -->
          </div>

          <!-- Center Viewer with Segmented Zoom -->
          <div class="s5-c">
            <div class="seg" id="view-mode-seg">
              <i class="knob" id="seg-knob"></i>
              <span class="on" id="seg-btn-full">Full page</span>
              <span id="seg-btn-top">Top half</span>
              <span id="seg-btn-bottom">Bottom half</span>
            </div>

            <div class="pv">
              <div class="pvi mode-full" id="review-sheet-wrap">
                <div class="tw" id="review-inspected-sheet">
                  <span class="t rev-tw-student" style="--x:200;--y:381;">Aarav Mehta</span>
                  <span class="t rev-tw-pen" style="--x:123;--y:351;">250843131022</span>
                  <span class="t rev-tw-class" style="--x:131;--y:405;">CSE-24-C</span>
                  <span class="t rev-tw-batch" style="--x:586;--y:405;">C2</span>
                  <span class="t rev-tw-sem" style="--x:601;--y:351;">5th</span>
                  <span class="t rev-tw-term" style="--x:627;--y:289;">2026-27</span>
                  <span class="t rev-tw-subj" style="--x:142;--y:322;">Operating Systems</span>
                  <span class="t rev-tw-faculty" style="--x:176;--y:725;">Prof. S. Desai</span>
                  <span class="t rev-tw-title" style="--x:356;--y:435;">Linux Commands Demo</span>
                  <span class="t rev-tw-pno" style="--x:514;--y:545;">1</span>
                  <span class="t rev-tw-marks" style="--x:604;--y:928;">10</span>

                  <!-- Hotspots -->
                  <i class="hs" style="left:47.04%;top:39.66%;width:41.67%;height:2.09%" title="Click to edit Title" id="hs-title"></i>
                  <i class="hs" style="left:67.88%;top:50.09%;width:21.51%;height:2.09%" title="Click to edit Conducted Date" id="hs-cond"></i>
                  <i class="hs" style="left:69.62%;top:53.04%;width:18.15%;height:2.09%" title="Click to edit Submission Date" id="hs-sub"></i>
                  <i class="hs" style="left:80.38%;top:86.43%;width:8.33%;height:2.09%" title="Click to edit Marks" id="hs-marks"></i>
                </div>
              </div>
            </div>
          </div>

          <!-- Right Sidebar Actions -->
          <div class="s5-r">
            <div class="meta">
              <b class="hand" id="review-meta-page">Page 1 of 4</b>
              <span id="review-meta-practical">Practical 1</span>
            </div>

            <button type="button" class="go" id="btn-edit-this-page">
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                <path d="M17 3a2.85 2.83 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5Z"></path>
              </svg>
              Edit this page
            </button>

            <button type="button" class="ghost" id="btn-edit-selected-pages">
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                <path d="m12 2 10 5-10 5L2 7l10-5Z"></path>
                <path d="m2 17 10 5 10-5"></path>
                <path d="m2 12 10 5 10-5"></path>
              </svg>
              Edit selected pages
            </button>

            <button type="button" class="ghost" id="btn-edit-all-pages">
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                <path d="m12 2 10 5-10 5L2 7l10-5Z"></path>
                <path d="m2 17 10 5 10-5"></path>
                <path d="m2 12 10 5 10-5"></path>
              </svg>
              Edit all pages
            </button>

            <button type="button" class="ghost" id="btn-review-download-pdf">
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                <path d="M12 15V3"></path>
                <path d="m7 10 5 5 5-5"></path>
                <path d="M5 21h14"></path>
              </svg>
              Download PDF
            </button>

            <button type="button" class="ghost" id="btn-review-back" style="margin-top: 6px;">
              Back to Print
            </button>
          </div>
        </div>
      </div>

      <!-- ====================================================================
           EDIT DRAWER MODAL (.s6)
           ==================================================================== -->
      <div class="s6" id="edit-drawer-modal" style="display:none;">
        <div class="dim" id="drawer-dim"></div>
        <div class="drw">
          <div class="dh">
            <h2 class="hand h2">Edit pages</h2>
            <span class="x" id="btn-close-drawer">✕</span>
          </div>

          <!-- Scope Choice -->
          <div class="scope">
            <div class="sc on" id="scope-opt-this">
              <i class="rd"></i>
              <b>Only this page</b>
              <em id="scope-label-this">P1</em>
            </div>
            <div class="sc" id="scope-opt-pick">
              <i class="rd"></i>
              <b>Pick pages</b>
              <em id="scope-label-pick">Selected</em>
            </div>
            <div class="sc" id="scope-opt-all">
              <i class="rd"></i>
              <b>All pages</b>
              <em id="scope-label-all">All</em>
            </div>
          </div>

          <!-- Pick Chips Container -->
          <div class="pcs" id="drawer-pick-chips" style="display:none;">
            <!-- Populated dynamically via JS -->
          </div>

          <!-- Fields -->
          <div class="ef">
            <label>
              <span>Experiment title</span>
              <input type="text" class="ei" id="drawer-input-title" placeholder="Practical title..."/>
            </label>
            <div class="er">
              <label style="flex: 1;">
                <span>Marks</span>
                <input type="text" class="ei" id="drawer-input-marks" placeholder="10"/>
              </label>
              <label style="flex: 1.5;">
                <span>Checked by</span>
                <input type="text" class="ei" id="drawer-input-faculty" placeholder="Faculty name"/>
              </label>
            </div>
          </div>

          <button type="button" class="go ap" id="btn-apply-drawer-changes">
            <span id="drawer-btn-label">Apply to 1 page</span>
          </button>
        </div>
      </div>

    </main>
  </div>

  <!-- Toast Notification Stack -->
  <div id="toast-container" role="status" aria-live="polite"></div>

  <!-- Main Application Script -->
  <script src="/static/js/app.js?v=2.5"></script>
</body>
</html>
'''

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(index_html_clean)

print("Successfully written clean templates/index.html!")

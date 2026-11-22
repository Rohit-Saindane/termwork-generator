import sys

notebook_css_content = """/* ==========================================================================
   TermWorkForge — Spiral-Bound College Notebook Theme (notebook.css)
   Clean, responsive, full-page design system
   ========================================================================== */

@import url('https://fonts.googleapis.com/css2?family=Caveat:wght@700&family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@600;700&display=swap');

/* Theme Tokens */
:root, body.nb-l {
  --desk: #e8dfcb;
  --paper: #fffdf6;
  --rule: #d4e3f5;
  --margin: #f0a9a9;
  --ink: #1d2640;
  --mut: #5a6480;
  --pen: #2547c9;
  --penink: #ffffff;
  --hl: #ffe45e;
  --hlbg: #ffe45e;
  --hls: #fff0a3;
  --hlink: #1d2640;
  --card: #ffffff;
  --line: #e0d9c4;
  --edge: #cfc5aa;
  --ok: #2b7a47;
  --oks: #e4f3e8;
  --ring: #a9afbb;
  --t1: #ffd966;
  --t2: #8ec5ff;
  --t3: #ffa8c5;
  --t4: #8fe0b0;
  --fl: #d6cdb5;
  --shadow: rgba(70,55,20,0.18);
  --tape: #ffb3cf;
  --note: #fff1a1;
}

body.nb-d {
  --desk: #12131a;
  --paper: #1e2130;
  --rule: #2b3250;
  --margin: #8f4d62;
  --ink: #e9ecf7;
  --mut: #a3abc5;
  --pen: #8fb0ff;
  --penink: #0f1530;
  --hl: #f2d24a;
  --hlbg: #6b5a14;
  --hls: #4a4222;
  --hlink: #1d2640;
  --card: #272b3f;
  --line: #363c59;
  --edge: #3a4160;
  --ok: #6ee7a0;
  --oks: #173326;
  --ring: #6d748a;
  --t1: #e0b94a;
  --t2: #6aa6e6;
  --t3: #e0799b;
  --t4: #58c088;
  --fl: #2a2e44;
  --shadow: rgba(0,0,0,0.45);
  --tape: #d9779c;
  --note: #e9cf63;
}

* { box-sizing: border-box; }
html, body {
  margin: 0;
  padding: 0;
  min-height: 100vh;
  background-color: var(--desk);
  color: var(--ink);
  font-family: 'Inter', system-ui, -apple-system, sans-serif;
  transition: background-color .25s ease, color .25s ease;
  overflow-x: hidden;
}

button, input { font-family: inherit; }
button { cursor: pointer; }
.hand { font-family: 'Caveat', 'Segoe Print', cursive; font-weight: 700; letter-spacing: 0; }

/* Cold-Start Wakeup Banner */
#cold-banner {
  display: none;
  background: var(--hl);
  color: #1d2640;
  font-size: 13px;
  font-weight: 700;
  padding: 8px 16px;
  text-align: center;
  align-items: center;
  justify-content: center;
  gap: 10px;
  width: 100%;
  border-bottom: 2px solid var(--ink);
  z-index: 9999;
}
#cold-banner.visible { display: flex; }
#cold-banner-close {
  background: transparent;
  border: none;
  font-size: 14px;
  font-weight: 800;
  cursor: pointer;
  color: #1d2640;
}

/* Notebook App Shell Wrapper */
.notebook-app {
  width: 100%;
  max-width: 1040px;
  margin: 0 auto;
  padding: 16px 12px 32px;
  display: flex;
  flex-direction: column;
}
@media (min-width: 880px) {
  .notebook-app {
    padding: 24px 20px 48px;
  }
}

/* Top Notebook Spine Header (Brand, Stepper Tabs, Sun/Moon) */
.notebook-header {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 12px;
  padding: 0 8px;
  margin-bottom: -1px;
  position: relative;
  z-index: 20;
}

.brand {
  display: flex;
  align-items: center;
  gap: 8px;
  text-decoration: none;
  color: inherit;
  padding-bottom: 8px;
  flex-shrink: 0;
}
.brand .lg {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  background: var(--pen);
  color: var(--penink);
  display: flex;
  align-items: center;
  justify-content: center;
}
.brand b {
  font-family: 'Caveat', cursive;
  font-size: 28px;
  font-weight: 700;
  line-height: 1;
}

/* Color Index Stepper Tabs */
.tabs {
  display: flex;
  gap: 6px;
  align-items: flex-end;
  flex: 1;
  max-width: 480px;
  margin: 0 12px;
}
.tab {
  flex: 1;
  height: 32px;
  border-radius: 10px 10px 0 0;
  background: var(--tc);
  color: #1d2640;
  font-size: 12px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  border: 1.5px solid var(--edge);
  border-bottom: 0;
  box-sizing: border-box;
  opacity: .85;
  cursor: pointer;
  transition: height .15s ease, opacity .15s ease, transform .15s ease;
  user-select: none;
  padding: 0 6px;
  white-space: nowrap;
}
.tab:hover { opacity: 1; }
.tab.on {
  height: 40px;
  opacity: 1;
  font-size: 13px;
  border-color: var(--ink);
  box-shadow: 0 -2px 8px rgba(0,0,0,0.06);
}
.tab b {
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background: #1d2640;
  color: #fff;
  font-size: 10.5px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
.tab.done b {
  background: var(--ok);
}
.t1 { --tc: var(--t1); }
.t2 { --tc: var(--t2); }
.t3 { --tc: var(--t3); }
.t4 { --tc: var(--t4); }

/* Sun/Moon Toggle */
.tg {
  width: 66px;
  height: 32px;
  border-radius: 99px;
  background: var(--paper);
  border: 2px solid var(--ink);
  padding: 0;
  box-sizing: border-box;
  position: relative;
  color: var(--ink);
  cursor: pointer;
  margin-bottom: 8px;
  flex-shrink: 0;
}
.tg i {
  position: absolute;
  top: 3px;
  left: 3px;
  width: 22px;
  height: 22px;
  border-radius: 50%;
  background: var(--hl);
  border: 2px solid var(--ink);
  box-sizing: border-box;
  transition: left .2s cubic-bezier(.4, 0, .2, 1);
}
.nb-d .tg i { left: 37px; }
.tg span {
  position: absolute;
  top: 50%;
  margin-top: -7.5px;
  z-index: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}
.tg .s { left: 7px; }
.tg .m { right: 7px; }
.nb-l .tg .s { color: #1d2640; }
.nb-d .tg .m { color: #1d2640; }

/* The Physical College Notebook Binder (.paper) */
.notebook-body {
  position: relative;
  background-color: var(--paper);
  border: 1.5px solid var(--edge);
  border-radius: 14px;
  box-shadow: 0 16px 40px var(--shadow);
  background-image: linear-gradient(var(--rule) 1px, transparent 1px);
  background-size: 100% 28px;
  background-position: 0 24px;
  min-height: 600px;
  padding: 24px 20px 32px 54px;
  z-index: 10;
}
@media (min-width: 880px) {
  .notebook-body {
    padding: 32px 36px 40px 84px;
    border-radius: 16px;
    min-height: 640px;
  }
}

/* Red Margin Line */
.notebook-body::before {
  content: "";
  position: absolute;
  top: 0;
  bottom: 0;
  width: 2px;
  background: var(--margin);
  opacity: .8;
  left: 42px;
  pointer-events: none;
}
@media (min-width: 880px) {
  .notebook-body::before {
    left: 66px;
  }
}

/* Left Spiral Rings & Holes */
.rings {
  display: none;
  pointer-events: none;
}
@media (min-width: 880px) {
  .rings {
    display: flex;
    flex-direction: column;
    justify-content: space-around;
    position: absolute;
    left: -12px;
    top: 24px;
    bottom: 24px;
    z-index: 30;
  }
  .rings i {
    display: block;
    width: 32px;
    height: 10px;
    border-radius: 5px;
    background: linear-gradient(90deg, #888, #ddd 40%, #fff 60%, #999);
    border: 1px solid #777;
    box-shadow: 2px 2px 4px rgba(0,0,0,0.22);
    margin: 8px 0;
  }
}
.holes {
  position: absolute;
  left: 12px;
  top: 40px;
  bottom: 40px;
  display: flex;
  flex-direction: column;
  justify-content: space-around;
  pointer-events: none;
}
@media (min-width: 880px) {
  .holes { display: none; }
}
.holes i {
  width: 14px;
  height: 14px;
  border-radius: 50%;
  background: var(--desk);
  box-shadow: inset 0 2px 4px rgba(0,0,0,.35);
}

/* Step Views */
.step-view {
  display: none;
  animation: fadeIn .2s ease-out;
}
.step-view.active {
  display: block;
}
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(4px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Primary Action Buttons */
.go {
  height: 46px;
  border: 0;
  border-radius: 12px;
  background: var(--pen);
  color: var(--penink);
  font-size: 15px;
  font-weight: 700;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 0 24px;
  box-shadow: 0 3px 0 rgba(0,0,0,.25);
  transition: transform .12s, box-shadow .12s;
  cursor: pointer;
  text-decoration: none;
}
.go:hover { transform: translateY(-2px); box-shadow: 0 5px 0 rgba(0,0,0,.25); }
.go:active { transform: translateY(2px); box-shadow: 0 1px 0 rgba(0,0,0,.25); }
.go.sm { height: 38px; font-size: 13px; padding: 0 16px; }

.ghost {
  height: 38px;
  border-radius: 10px;
  border: 1.5px solid var(--ink);
  background: var(--card);
  color: var(--ink);
  font-size: 13px;
  font-weight: 700;
  padding: 0 14px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  cursor: pointer;
  transition: background .12s, transform .12s;
}
.ghost:hover { background: var(--hls); transform: translateY(-1px); }

/* Accent Decorations */
.note {
  display: inline-block;
  background: var(--note);
  color: #4a3d00;
  font-family: 'Caveat', cursive;
  font-weight: 700;
  font-size: 20px;
  padding: 2px 14px;
  transform: rotate(-2deg);
  box-shadow: 0 2px 0 rgba(0,0,0,.15);
  border-radius: 2px;
}
.mk {
  background: linear-gradient(transparent 52%, var(--hlbg) 52%);
  color: var(--ink);
  padding: 0 4px;
}
.tape {
  display: inline-block;
  background: var(--tape);
  color: #1d2640;
  font-size: 12px;
  font-weight: 700;
  padding: 4px 12px;
  transform: rotate(-1.5deg);
  clip-path: polygon(0 0, 100% 0, 98% 50%, 100% 100%, 0 100%, 2% 50%);
}
.stamp {
  display: inline-block;
  font-family: 'Caveat', cursive;
  font-weight: 700;
  font-size: 17px;
  color: var(--ok);
  border: 2px solid var(--ok);
  padding: 0 8px;
  border-radius: 6px;
  transform: rotate(-8deg);
  line-height: 1.2;
}

/* ==========================================================================
   Exact Miniature of the College Term Work Sheet (.tw)
   ========================================================================== */
.tw {
  position: relative;
  width: 100%;
  aspect-ratio: 744/1054;
  background: #fff url("data:image/png;base64,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") center/100% 100% no-repeat;
  container-type: inline-size;
  box-shadow: 0 1px 0 rgba(0,0,0,.08), 0 4px 14px var(--shadow);
  border-radius: 2px;
}
.tw .t {
  position: absolute;
  left: calc(var(--x)/744*100%);
  top: calc(var(--y)/1054*100%);
  transform: translateY(-100%);
  font-family: 'Times New Roman', Times, serif;
  font-size: 1.95cqw;
  line-height: 1;
  color: #1a1f6b;
  white-space: nowrap;
  pointer-events: none;
}
.tw .hs {
  position: absolute;
  border: 1.5px dashed #d6a400;
  background: rgba(255,228,94,.28);
  border-radius: 2px;
  animation: hsp 2.4s ease-in-out infinite;
  cursor: pointer;
}
.tw .hb {
  position: absolute;
  height: 2.2%;
  background: rgba(255,228,94,.55);
  border-radius: 2px;
  pointer-events: none;
  color: #1a1f6b;
  transition: all .2s cubic-bezier(.4, 0, .2, 1);
}
.tw .hb svg {
  position: absolute;
  right: -9px;
  top: -13px;
  animation: pnb .5s ease-in-out infinite;
}

/* ==========================================================================
   Step 1: Files (.s1)
   ========================================================================== */
.s1-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 24px;
}
@media (min-width: 820px) {
  .s1-grid {
    grid-template-columns: 1.15fr 1fr;
    gap: 36px;
    align-items: start;
  }
}
.s1-l {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}
.h1 {
  margin: 12px 0 0;
  font-size: clamp(34px, 4vw, 48px);
  line-height: 1.12;
  word-break: normal;
}
.squig { display: block; margin: 8px 0 12px; }
.sub {
  margin: 0 0 16px;
  font-size: 14.5px;
  line-height: 1.55;
  color: var(--mut);
}
.how {
  list-style: none;
  margin: 12px 0 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.how li {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 14px;
  font-weight: 600;
}
.how b {
  font-family: 'Caveat', cursive;
  font-size: 20px;
  width: 30px;
  height: 30px;
  border: 2px solid var(--ink);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--card);
  flex-shrink: 0;
}

.s1-r {
  display: flex;
  flex-direction: column;
  gap: 16px;
}
.att {
  position: relative;
  background: var(--card);
  border: 1.5px solid var(--edge);
  border-radius: 8px;
  padding: 14px;
  display: flex;
  gap: 14px;
  box-shadow: 0 4px 14px var(--shadow);
  cursor: pointer;
  transition: transform .15s ease, border-color .15s ease;
}
.att:hover {
  border-color: var(--pen);
}
.att.dragover {
  border-color: var(--pen);
  background: var(--hls);
}
.att.idx { transform: rotate(-.6deg); }
.att.frm { transform: rotate(.5deg); }
.att.idx:hover { transform: rotate(-.6deg) translateY(-2px); }
.att.frm:hover { transform: rotate(.5deg) translateY(-2px); }

.clip {
  position: absolute;
  left: -8px;
  top: -12px;
  color: var(--mut);
  transform: rotate(-20deg);
  pointer-events: none;
}
.pin {
  position: absolute;
  left: 20px;
  top: -6px;
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: #e0524f;
  border: 1.5px solid #8f2523;
  z-index: 2;
  box-shadow: 1px 2px 0 rgba(0,0,0,.25);
  pointer-events: none;
}
.pdfm {
  position: relative;
  width: 54px;
  height: 72px;
  flex-shrink: 0;
  background: #fff;
  border: 1px solid #cfc7b0;
  padding: 8px 6px;
  box-sizing: border-box;
  overflow: hidden;
  border-radius: 3px;
}
.pdfm i {
  display: block;
  height: 3px;
  background: #c9c3b0;
  margin-bottom: 5px;
  border-radius: 2px;
}
.pdfm i:nth-child(odd) { width: 80%; }
.scan {
  position: absolute;
  left: 0;
  right: 0;
  height: 12px;
  background: rgba(255,228,94,.7);
  top: 0;
  display: none;
}
.att.scanning .scan {
  display: block;
  animation: scn 2.6s ease-in-out infinite;
}
.ftw {
  width: 64px;
  flex-shrink: 0;
  position: relative;
  transform: rotate(-2deg);
}

.att-t {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 6px;
  align-items: flex-start;
}
.att-t b {
  font-size: 13.5px;
  font-weight: 700;
  line-height: 1.3;
  word-break: break-word;
}
.att-t em {
  font-style: normal;
  font-size: 12px;
  color: var(--mut);
}
.found {
  color: var(--ok) !important;
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: 5px;
}
.own {
  font-size: 12px;
  color: var(--pen);
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: 5px;
  cursor: pointer;
}
.own:hover { text-decoration: underline; }
.own svg { animation: bnc 1.2s ease-in-out infinite; }

.tip {
  align-self: flex-start;
  background: var(--note);
  color: #4a3d00;
  font-family: 'Caveat', cursive;
  font-weight: 700;
  font-size: 18px;
  padding: 4px 14px;
  transform: rotate(1deg);
  box-shadow: 0 2px 0 rgba(0,0,0,.15);
  margin-top: 4px;
  border-radius: 2px;
}

/* ==========================================================================
   Step 2: Practicals (.s2)
   ========================================================================== */
.s2-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 24px;
}
@media (min-width: 820px) {
  .s2-grid {
    grid-template-columns: 1fr 240px;
    gap: 28px;
    align-items: start;
  }
}
.s2-h {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
}
.h2 {
  margin: 0;
  font-size: 32px;
  line-height: 1;
}
.tools {
  display: flex;
  gap: 8px;
  margin-bottom: 14px;
}
.plist {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 4px;
}
@media (min-width: 820px) {
  .plist {
    display: grid;
    grid-template-columns: 1fr 1fr;
    column-gap: 20px;
    max-height: 480px;
    overflow-y: auto;
    padding-right: 8px;
  }
}
.pr {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 10px;
  border-bottom: 1px dashed var(--line);
  cursor: pointer;
  border-radius: 6px;
  transition: background .12s;
}
.pr:hover {
  background: rgba(255,228,94,.12);
}
.pno {
  width: 32px;
  text-align: right;
  font-size: 26px;
  line-height: 1;
  color: var(--mut);
  flex-shrink: 0;
}
.pt {
  flex: 1;
  min-width: 0;
  font-size: 13px;
  font-weight: 600;
  line-height: 1.4;
}
.hl {
  background-repeat: no-repeat;
  background-image: linear-gradient(transparent 40%, var(--hlbg) 40%);
  background-size: 0 100%;
  -webkit-box-decoration-break: clone;
  box-decoration-break: clone;
  transition: background-size .25s ease;
}
.pr.on .hl {
  background-size: 100% 100%;
  color: var(--ink);
}
.ck {
  flex-shrink: 0;
  width: 26px;
  height: 26px;
  border: 2px solid var(--ink);
  border-radius: 7px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--pen);
  background: var(--card);
}
.tick {
  stroke-dasharray: 26;
  stroke-dashoffset: 26;
  transition: stroke-dashoffset .2s ease;
}
.pr.on .tick {
  stroke-dashoffset: 0;
}
.pr.on .ck {
  border-color: var(--pen);
}

.s2-sidebar {
  display: flex;
  flex-direction: column;
  gap: 14px;
  background: var(--card);
  border: 1.5px solid var(--edge);
  border-radius: 10px;
  padding: 16px;
  box-shadow: 0 6px 16px var(--shadow);
  transform: rotate(.8deg);
}
.big {
  font-size: 52px;
  line-height: .9;
  display: flex;
  align-items: baseline;
  gap: 6px;
}
.big small {
  font-family: 'Inter';
  font-size: 14px;
  font-weight: 700;
  color: var(--mut);
}
.fan {
  position: relative;
  height: 120px;
  margin: 6px 0;
}
.sk {
  position: absolute;
  width: 76px;
}
.sk0 { left: 4px; top: 12px; transform: rotate(-8deg); }
.sk1 { left: 52px; top: 6px; transform: rotate(-1deg); }
.sk2 { left: 100px; top: 12px; transform: rotate(7deg); }
.pchips {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  max-height: 60px;
  overflow-y: auto;
}
.pchips span {
  font-size: 11.5px;
  font-weight: 800;
  background: var(--hls);
  color: var(--ink);
  border-radius: 6px;
  padding: 3px 8px;
}

/* ==========================================================================
   Step 3: Details & Live Writing (.s3)
   ========================================================================== */
.s3-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 28px;
}
@media (min-width: 820px) {
  .s3-grid {
    grid-template-columns: 1fr 310px;
    gap: 36px;
    align-items: start;
  }
}
.s3-f {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.fields-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px 14px;
}
@media (min-width: 820px) {
  .fields-grid {
    grid-template-columns: repeat(6, 1fr);
  }
}
.fl {
  display: flex;
  flex-direction: column;
  gap: 3px;
  min-width: 0;
}
.fl.w-full { grid-column: 1 / -1; }
.fl.w-half { grid-column: span 1; }
@media (min-width: 820px) {
  .fl.sp-6 { grid-column: span 6; }
  .fl.sp-4 { grid-column: span 4; }
  .fl.sp-3 { grid-column: span 3; }
  .fl.sp-2 { grid-column: span 2; }
}
.fn {
  font-size: 11px;
  font-weight: 800;
  letter-spacing: .05em;
  color: var(--mut);
  text-transform: uppercase;
}
.auto {
  margin-left: 6px;
  font-size: 9.5px;
  font-weight: 800;
  background: var(--tape);
  color: #1d2640;
  border-radius: 99px;
  padding: 1px 8px;
  letter-spacing: 0;
  text-transform: none;
}
input.in {
  height: 34px;
  border: 1.5px solid var(--line);
  border-radius: 8px;
  background: var(--card);
  padding: 0 10px;
  font-size: 13px;
  font-weight: 600;
  color: var(--ink);
  outline: none;
  width: 100%;
  box-sizing: border-box;
  transition: border-color .15s, box-shadow .15s;
}
input.in:focus {
  border-color: var(--pen);
  box-shadow: 0 0 0 3px var(--hls);
}

.s3-p {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.lv {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.rec {
  font-size: 11px;
  font-weight: 800;
  color: #b3261e;
  display: flex;
  align-items: center;
  gap: 6px;
}
.nb-d .rec { color: #ff8a80; }
.rec::before {
  content: "";
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #e0524f;
  animation: blink 1s step-end infinite;
}
.cam {
  position: relative;
  background: var(--desk);
  border: 1.5px solid var(--edge);
  border-radius: 8px;
  padding: 6px;
  box-shadow: 0 4px 16px var(--shadow);
}

/* ==========================================================================
   Step 4: Print (.s4)
   ========================================================================== */
.s4-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 28px;
  align-items: center;
  justify-content: center;
}
@media (min-width: 820px) {
  .s4-grid {
    grid-template-columns: 260px 1fr;
    gap: 48px;
  }
}
.s4-st {
  width: 100%;
  max-width: 260px;
  margin: 0 auto;
}
.prt {
  position: relative;
  z-index: 3;
  background: var(--t1);
  border: 2px solid var(--ink);
  border-radius: 16px;
  padding: 12px 14px 20px;
  box-shadow: 0 8px 0 rgba(0,0,0,.18);
}
.prt-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
}
.lcd {
  background: #cfe8d6;
  color: #17331f;
  border: 2px solid var(--ink);
  border-radius: 6px;
  padding: 4px 10px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px;
  font-weight: 700;
}
.leds { display: flex; gap: 4px; }
.leds i {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #1d2640;
  opacity: .3;
  display: block;
}
.leds i.g {
  background: #17a34a;
  opacity: 1;
  animation: blink 1s step-end infinite;
}
.prt-slot {
  position: absolute;
  left: 14px;
  right: 14px;
  bottom: 8px;
  height: 8px;
  border-radius: 99px;
  background: #1d2640;
}
.pwin {
  position: relative;
  z-index: 1;
  margin: -8px 12px 0;
  height: 320px;
  overflow: hidden;
}
.sw {
  position: absolute;
  left: 0;
  right: 0;
  top: 0;
}
.sw.animating {
  animation: sheetcyc 10s cubic-bezier(.4, 0, .2, 1) infinite;
}

.s4-sd {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.s4-h {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
}
.chip {
  font-size: 12px;
  font-weight: 800;
  background: var(--hls);
  color: var(--ink);
  border-radius: 99px;
  padding: 4px 12px;
}
.films {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(70px, 1fr));
  gap: 10px;
  padding: 8px 0;
}
.film {
  position: relative;
  border-radius: 4px;
  cursor: pointer;
  transition: transform .15s ease, box-shadow .15s ease;
}
.film:hover { transform: translateY(-2px); }
.film.active {
  transform: translateY(-4px) scale(1.05);
  box-shadow: 0 0 0 2px var(--pen), 0 8px 16px var(--shadow);
}
.film .flb {
  position: absolute;
  left: 0;
  right: 0;
  bottom: -16px;
  text-align: center;
  font-size: 11px;
  font-weight: 800;
  color: var(--mut);
}
.namebox {
  display: flex;
  align-items: center;
  border: 1.5px solid var(--ink);
  border-radius: 10px;
  background: var(--card);
  overflow: hidden;
  margin-top: 14px;
}
.namebox input {
  flex: 1;
  min-width: 0;
  border: 0;
  outline: 0;
  background: transparent;
  padding: 11px 12px;
  font-size: 13px;
  font-weight: 600;
  color: var(--ink);
}
.namebox span {
  padding: 0 8px 0 2px;
  font-size: 13px;
  color: var(--mut);
}
.namebox button {
  align-self: stretch;
  width: 42px;
  border: 0;
  border-left: 1.5px solid var(--ink);
  background: var(--hl);
  color: #1d2640;
  display: flex;
  align-items: center;
  justify-content: center;
}
.act2 {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}
.act2 .go, .act2 .ghost { height: 44px; }
.dl svg { animation: bnc .9s ease-in-out infinite; }

/* ==========================================================================
   Step 5: Review (.s5)
   ========================================================================== */
.s5-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 20px;
}
@media (min-width: 820px) {
  .s5-grid {
    grid-template-columns: 70px 1fr 210px;
    gap: 28px;
    align-items: start;
  }
}
.s5-l {
  display: flex;
  gap: 10px;
  overflow-x: auto;
  padding-bottom: 8px;
}
@media (min-width: 820px) {
  .s5-l {
    flex-direction: column;
    overflow-y: auto;
    max-height: 480px;
    gap: 16px;
  }
}
.th {
  position: relative;
  width: 60px;
  flex-shrink: 0;
  cursor: pointer;
}
.thc {
  border: 2px solid transparent;
  border-radius: 4px;
  transition: all .15s;
}
.th.cur .thc {
  border-color: var(--pen);
  box-shadow: 0 0 0 2px var(--hls);
}
.th .tl {
  position: absolute;
  left: 0;
  right: 0;
  bottom: -15px;
  text-align: center;
  font-size: 11px;
  font-weight: 800;
  color: var(--mut);
}
.tck {
  position: absolute;
  right: -4px;
  top: -4px;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background: var(--card);
  border: 1.5px solid var(--ink);
  color: var(--penink);
  display: flex;
  align-items: center;
  justify-content: center;
}
.th.cur .tck {
  background: var(--pen);
  border-color: var(--pen);
}

.s5-c {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.seg {
  position: relative;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  background: var(--card);
  border: 1.5px solid var(--ink);
  border-radius: 10px;
  padding: 3px;
  font-size: 12px;
  font-weight: 700;
  text-align: center;
}
.seg span {
  position: relative;
  z-index: 1;
  padding: 7px 0;
  color: var(--mut);
  cursor: pointer;
  transition: color .2s;
}
.seg span.on { color: #1d2640; }
.knob {
  position: absolute;
  left: 3px;
  top: 3px;
  bottom: 3px;
  width: calc((100% - 6px)/3);
  background: var(--hl);
  border-radius: 7px;
  transition: left .25s cubic-bezier(.4, 0, .2, 1);
}
.pv {
  position: relative;
  overflow: hidden;
  border-radius: 8px;
  display: flex;
  justify-content: center;
  background: var(--desk);
  border: 1.5px solid var(--edge);
  height: 380px;
}
.pvi {
  flex-shrink: 0;
  transform-origin: top center;
  width: 250px;
  transition: transform .3s ease;
}
.pvi.mode-full { transform: none; }
.pvi.mode-top { transform: scale(1.6) translateY(0); }
.pvi.mode-bottom { transform: scale(1.6) translateY(-90px); }

.s5-r {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.meta b { font-size: 30px; line-height: 1; }
.meta span { font-size: 12.5px; color: var(--mut); }

/* ==========================================================================
   Edit Drawer Modal (.s6)
   ========================================================================== */
.s6 {
  position: fixed;
  inset: 0;
  z-index: 999;
}
.dim {
  position: absolute;
  inset: 0;
  background: rgba(10, 12, 24, .5);
  cursor: pointer;
}
.drw {
  position: absolute;
  background: var(--paper);
  border: 1.5px solid var(--edge);
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 14px;
  box-shadow: 0 -8px 30px rgba(0,0,0,.25);
  left: 0;
  right: 0;
  bottom: 0;
  border-radius: 24px 24px 0 0;
  max-height: 85vh;
  overflow-y: auto;
}
@media (min-width: 820px) {
  .drw {
    left: auto;
    right: 0;
    top: 0;
    bottom: 0;
    width: 360px;
    border-radius: 0;
    box-shadow: -8px 0 30px rgba(0,0,0,.25);
    max-height: none;
  }
}
.dh {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.dh .x {
  cursor: pointer;
  font-size: 18px;
  font-weight: 700;
  color: var(--mut);
  padding: 4px 8px;
  border-radius: 6px;
}
.dh .x:hover { background: var(--card); color: var(--ink); }
.scope {
  display: grid;
  gap: 8px;
}
.sc {
  display: flex;
  align-items: center;
  gap: 10px;
  border: 1.5px solid var(--line);
  border-radius: 10px;
  padding: 10px 12px;
  background: var(--card);
  cursor: pointer;
  transition: all .15s;
}
.sc.on {
  border-color: var(--pen);
  background: var(--hls);
}
.sc b { font-size: 13px; flex: 1; }
.sc em { font-style: normal; font-size: 12px; color: var(--mut); font-weight: 700; }
.rd {
  width: 18px;
  height: 18px;
  border-radius: 50%;
  border: 2px solid var(--ink);
  box-sizing: border-box;
  position: relative;
  flex-shrink: 0;
}
.sc.on .rd::after {
  content: "";
  position: absolute;
  inset: 3px;
  border-radius: 50%;
  background: var(--pen);
}
.pcs {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}
.pc {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  font-weight: 800;
  border: 1.5px solid var(--line);
  border-radius: 8px;
  padding: 5px 10px;
  background: var(--card);
  cursor: pointer;
}
.pc.on {
  border-color: var(--pen);
  background: var(--hls);
}
.pc i {
  width: 14px;
  height: 14px;
  border-radius: 4px;
  border: 1.5px solid var(--ink);
}
.pc.on i {
  background: var(--pen);
  border-color: var(--pen);
}
.ef {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.ef label {
  display: flex;
  flex-direction: column;
  gap: 3px;
}
.ef label span {
  font-size: 10.5px;
  font-weight: 800;
  letter-spacing: .05em;
  color: var(--mut);
  text-transform: uppercase;
}
.er { display: flex; gap: 10px; }
.ei {
  height: 36px;
  border: 1.5px solid var(--line);
  border-radius: 8px;
  background: var(--card);
  padding: 0 10px;
  font-size: 13px;
  font-weight: 600;
  color: var(--ink);
  outline: none;
  width: 100%;
}
.ei:focus {
  border-color: var(--pen);
  background: var(--hls);
}
.ap { width: 100%; height: 46px; }

/* Keyframe Animations */
@keyframes wob { 0%, 100% { transform: rotate(-2deg); } 50% { transform: rotate(2deg); } }
@keyframes bnc { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-3px); } }
@keyframes blink { 0%, 49% { opacity: 1; } 50%, 100% { opacity: .25; } }
@keyframes scn { 0% { top: -2px; } 100% { top: 60px; } }
@keyframes pnb { 0%, 100% { transform: translate(0, 0) rotate(0); } 50% { transform: translate(-2px, 2px) rotate(-8deg); } }
@keyframes hsp { 0%, 100% { opacity: .55; } 50% { opacity: 1; } }
@keyframes sheetcyc {
  0% { transform: translateY(-104%); opacity: 1; }
  8%, 22% { transform: translateY(0); opacity: 1; }
  30% { transform: translateY(106%); opacity: 1; }
  30.1%, 100% { transform: translateY(-104%); opacity: 0; }
}

/* Toast Container */
#toast-container {
  position: fixed;
  bottom: 24px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  flex-direction: column;
  gap: 8px;
  z-index: 10000;
  pointer-events: none;
}
.toast {
  pointer-events: auto;
  padding: 10px 20px;
  border-radius: 10px;
  background: var(--ink);
  color: var(--paper);
  border: 1.5px solid var(--hl);
  font-size: 13.5px;
  font-weight: 700;
  box-shadow: 0 6px 18px var(--shadow);
  display: flex;
  align-items: center;
  gap: 10px;
  animation: bnc .25s ease-out;
}
.toast.success { border-color: var(--ok); }
.toast.error { border-color: #e0524f; }
"""

with open('static/css/notebook.css', 'w', encoding='utf-8') as f:
    f.write(notebook_css_content)

print("Successfully written clean static/css/notebook.css!")

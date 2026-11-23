"""
TermWorkForge — v6  (Notebook UI)
- Index parsing: cell-level extraction with width-aware word splitting, so titles
  never come out fused ("WriteaprogramtoimplementBFS") no matter how the index
  PDF was produced.
- Subject auto-extract from the index.
- Per-page overrides (the Review / Edit flow edits individual pages).
- Real-page preview: /api/template-preview renders the blank form as PNG and
  /api/config exposes the exact overlay coordinates, so the browser draws the
  very same miniature that ends up in the PDF.
- Branded filename: termworkforge_practicals_2-5.pdf
"""
import io, json, os, re
import pdfplumber
from flask import Flask, jsonify, redirect, render_template, request, send_file, Response
from pypdf import PdfReader, PdfWriter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from PIL import Image
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
app.config["MAX_CONTENT_LENGTH"] = 32 * 1024 * 1024  # 32 MB

# ── Page geometry ──────────────────────────────────────────────────────────────
PAGE_W, PAGE_H = 594.96, 842.52
FONT, SIZE = "Times-Roman", 12

# ── Supported file types ───────────────────────────────────────────────────────
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".webp", ".tiff", ".tif"}
DOCX_EXTS = {".docx", ".doc"}
PDF_EXT = {".pdf"}
ALL_TERM_WORK_EXTS = PDF_EXT | IMAGE_EXTS | DOCX_EXTS
ALL_INDEX_EXTS = PDF_EXT  # index must be PDF — OCR isn't possible on Render free tier

BRAND = "termworkforge"

# ── Field injection coordinates (x, y_reportlab, max_x) ───────────────────────
FIELDS = {
    "term":           (502,  609.2, 527),
    "subject":        (111,  585.4, 527),
    "pen":            (97,   562.0, 385),
    "semester":       (479,  562.0, 527),
    "student_name":   (157,  536.9, 526),
    "class_name":     (101,  516.6, 386),
    "batch":          (463,  516.6, 525),
    "exp_z1":         (283,  494.9, 523),
    "exp_z2":         (73,   469.9, 526),
    "checked_by":     (136,  263.2, 524),
    "practical_no":   (407,  406.6, 531),
    "cond_dd":        (415,  383.7, 445),
    "cond_mm":        (450,  383.7, 480),
    "cond_yyyy":      (485,  383.7, 517),
    "sub_dd":         (413,  361.2, 444),
    "sub_mm":         (448,  360.2, 480),
    "sub_yyyy":       (484,  360.2, 515),
    "act_dd":         (414,  337.7, 447),
    "act_mm":         (451,  337.7, 484),
    "act_yyyy":       (488,  337.7, 518),
    "sign_date_dd":   (290,   97.5, 322),
    "sign_date_mm":   (327,   97.5, 357),
    "sign_date_yyyy": (363,   97.9, 392),
    "marks":          (478,  102.1, 525),
}

# ─────────────────────────────────────────────────────────────────────────────
# FILE CONVERSION HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def _ext(filename: str) -> str:
    return os.path.splitext(filename.lower())[1] if filename else ""


def image_bytes_to_pdf(img_bytes: bytes) -> bytes:
    """Any PIL-readable image → single-page A4 PDF (scaled to fit, centred)."""
    img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
    iw, ih = img.size
    W, H = A4
    margin = 28
    avail_w, avail_h = W - 2 * margin, H - 2 * margin
    scale = min(avail_w / iw, avail_h / ih)
    dw, dh = iw * scale, ih * scale
    x = margin + (avail_w - dw) / 2
    y = margin + (avail_h - dh) / 2

    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    c.setFillColorRGB(1, 1, 1)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    img_buf = io.BytesIO()
    img.save(img_buf, "PNG")
    img_buf.seek(0)
    c.drawImage(ImageReader(img_buf), x, y, dw, dh)
    c.save()
    return buf.getvalue()


def docx_to_pdf(docx_bytes: bytes) -> bytes:
    """DOCX → plain PDF (text extraction; no LibreOffice on Render free tier)."""
    import docx as python_docx
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib import colors

    doc = python_docx.Document(io.BytesIO(docx_bytes))
    buf = io.BytesIO()
    pdf = SimpleDocTemplate(buf, pagesize=A4, leftMargin=50, rightMargin=50,
                            topMargin=50, bottomMargin=50)
    styles = getSampleStyleSheet()
    story = []
    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            story.append(Spacer(1, 6))
            continue
        name = para.style.name or ""
        style = styles["Heading1"] if "Heading 1" in name else styles["Heading2"] if "Heading 2" in name else styles["Normal"]
        story.append(Paragraph(text, style))
        story.append(Spacer(1, 4))
    for table in doc.tables:
        data = [[cell.text for cell in row.cells] for row in table.rows]
        if data:
            t = Table(data)
            t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                                   ("FONTSIZE", (0, 0), (-1, -1), 9),
                                   ("PADDING", (0, 0), (-1, -1), 4)]))
            story.append(t)
            story.append(Spacer(1, 8))
    if not story:
        story.append(Paragraph("(Empty document)", styles["Normal"]))
    pdf.build(story)
    return buf.getvalue()


def to_pdf_bytes(file_bytes: bytes, filename: str) -> bytes:
    ext = _ext(filename)
    if ext in PDF_EXT:
        return file_bytes
    if ext in IMAGE_EXTS:
        return image_bytes_to_pdf(file_bytes)
    if ext in DOCX_EXTS:
        return docx_to_pdf(file_bytes)
    raise ValueError(f"Unsupported file type: {ext}")


def validate_ext(filename: str, allowed: set, field_name: str):
    ext = _ext(filename)
    if ext not in allowed:
        return False, f"{field_name} must be one of: {', '.join(sorted(allowed))}. Got '{ext}'."
    return True, ""

# ─────────────────────────────────────────────────────────────────────────────
# INDEX PARSING
# ─────────────────────────────────────────────────────────────────────────────

# A real word gap is ≥ ~0.25 em; kerning inside a word is ≈ 0. Splitting at
# 0.2 em separates words even when the PDF has no space glyph at all.
GAP_RATIO = 0.2


def _clean(text: str) -> str:
    """Collapse whitespace; glue words that were hard-wrapped on a hyphen."""
    lines = [" ".join(l.split()) for l in (text or "").split("\n")]
    out = ""
    for l in lines:
        if not l:
            continue
        if out and out.endswith("-"):
            out += l          # "Tic-tac-" + "toe"  →  "Tic-tac-toe"
        else:
            out = (out + " " + l) if out else l
    return out


def _cell_text(page, bbox) -> str:
    x0, top, x1, bottom = bbox
    bx0, bt, bx1, bb = page.bbox
    box = (max(x0, bx0), max(top, bt), min(x1, bx1), min(bottom, bb))
    if box[2] - box[0] < 1 or box[3] - box[1] < 1:
        return ""
    try:
        return _clean(page.crop(box).extract_text(x_tolerance_ratio=GAP_RATIO) or "")
    except Exception:
        return ""


def _extract_via_cells(pdf) -> dict:
    practicals = {}
    for page in pdf.pages:
        tables = page.find_tables()
        if not tables:
            continue
        best = max(tables, key=lambda t: len(t.rows))
        for row in best.rows:
            cells = [c for c in row.cells if c]
            if len(cells) < 3:
                continue
            texts = [_cell_text(page, c) for c in row.cells if c]
            sr = next((t for t in texts[:2] if re.fullmatch(r"\d+", t)), None)
            if sr is None:
                continue
            # title = the longest non-numeric, non-date cell in the row
            cand = [t for t in texts if t and not re.fullmatch(r"[\d\s/.\-]+", t)]
            if not cand:
                continue
            title = max(cand, key=len)
            if len(title) >= 3:
                practicals[int(sr)] = title
    return practicals


def _extract_via_tables(pdf) -> dict:
    """Legacy fallback (pdfplumber extract_tables) — only used if cell mode finds nothing."""
    practicals = {}
    for page in pdf.pages:
        tables = page.extract_tables()
        if not tables:
            continue
        best = max(tables, key=len)
        for row in best:
            if not row or not row[0]:
                continue
            sr = str(row[0]).strip()
            if not re.fullmatch(r"\d+", sr):
                continue
            title = row[2] if len(row) > 2 else ""
            if title:
                practicals[int(sr)] = " ".join(title.split())
    return practicals


def extract_practicals(file_bytes: bytes, filename: str = "index.pdf") -> dict:
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        data = _extract_via_cells(pdf)
        if not data:
            data = _extract_via_tables(pdf)
    return data


def extract_subject_from_index(file_bytes: bytes) -> str:
    """Pull the 'SUBJECT : …' value from the index header. '' when blank/not found."""
    try:
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            for page in pdf.pages[:2]:
                text = re.sub(r"\s+", " ", page.extract_text(x_tolerance_ratio=GAP_RATIO) or "")
                m = re.search(
                    r"S\s*U\s*B\s*J\s*E\s*C\s*T\s*:\s*(?!(?:RUBRICS|SR\.?\s*NO|DATE|PEN\b|NAME\b|TOTAL))(.+?)"
                    r"(?=\s*(?:RUBRICS|SR\.?\s*NO|DATE|PEN\s*:|NAME\s*:|TOTAL|$))",
                    text, re.IGNORECASE)
                if m:
                    subject = m.group(1).strip()
                    subject = re.sub(r"(?<=\b[A-Z])\s(?=[a-z])", "", subject)   # "O perating" → "Operating"
                    subject = re.sub(r"\s{2,}", " ", subject).strip(" :-")
                    if 2 <= len(subject) <= 80:
                        return subject
    except Exception:
        pass
    return ""

# ─────────────────────────────────────────────────────────────────────────────
# PDF BUILDING
# ─────────────────────────────────────────────────────────────────────────────

def _w(text): return pdfmetrics.stringWidth(text, FONT, SIZE)


def _fit(text, max_width):
    while text and _w(text) > max_width:
        text = text[:-1]
    return text


def wrap_experiment(title):
    """Zone 1 = inline after the label, zone 2 = full line below. Never overflows."""
    z1_avail = FIELDS["exp_z1"][2] - FIELDS["exp_z1"][0]
    z2_avail = FIELDS["exp_z2"][2] - FIELDS["exp_z2"][0]
    title = " ".join((title or "").split())
    words, buf = title.split(), []
    for i, word in enumerate(words):
        if _w(" ".join(buf + [word])) <= z1_avail:
            buf.append(word)
        else:
            l1 = " ".join(buf)
            rest = " ".join(words[i:])
            if not l1:  # first word alone is too long
                l1 = _fit(word, z1_avail)
                rest = " ".join(words[i + 1:])
            if _w(rest) > z2_avail:
                rest = _fit(rest, z2_avail - _w("…")) + "…"
            return l1, rest
    return " ".join(buf), ""


def _date_parts(s):
    if not s:
        return None
    parts = re.split(r"[/\-\.]", s.strip())
    if len(parts) != 3:
        return None
    return parts[0].zfill(2), parts[1].zfill(2), parts[2]


def build_pdf(pdf_b_bytes: bytes, title: str, form: dict) -> bytes:
    l1, l2 = wrap_experiment(title)
    packet = io.BytesIO()
    c = canvas.Canvas(packet, pagesize=(PAGE_W, PAGE_H))
    c.setFont(FONT, SIZE)

    def put(key, text):
        if not text:
            return
        x, y, mx = FIELDS[key]
        c.drawString(x, y, _fit(str(text), mx - x))

    for k_form, k_field in [("term", "term"), ("subject", "subject"), ("pen", "pen"),
                            ("semester", "semester"), ("student_name", "student_name"),
                            ("class_name", "class_name"), ("batch", "batch"),
                            ("checked_by", "checked_by"), ("practical_no", "practical_no"),
                            ("marks", "marks")]:
        put(k_field, form.get(k_form, ""))

    for prefix, key in [("cond", "conducted_on"), ("sub", "date_of_sub"),
                        ("act", "actual_sub"), ("sign_date", "sign_date")]:
        p = _date_parts(form.get(key, ""))
        if p:
            put(f"{prefix}_dd", p[0]); put(f"{prefix}_mm", p[1]); put(f"{prefix}_yyyy", p[2])

    if l1: c.drawString(FIELDS["exp_z1"][0], FIELDS["exp_z1"][1], l1)
    if l2: c.drawString(FIELDS["exp_z2"][0], FIELDS["exp_z2"][1], l2)
    c.save()
    packet.seek(0)

    overlay = PdfReader(packet).pages[0]
    try:
        writer = PdfWriter(clone_from=io.BytesIO(pdf_b_bytes))
        writer.pages[0].merge_page(overlay)
    except Exception:
        reader_b = PdfReader(io.BytesIO(pdf_b_bytes))
        writer = PdfWriter()
        for p in reader_b.pages:
            writer.add_page(p)
        writer.pages[0].merge_page(overlay)
    out = io.BytesIO()
    writer.write(out)
    return out.getvalue()


def sr_label(nums):
    """[2,3,4,5] → '2-5' ; [1,3,5] → '1_3_5'."""
    nums = sorted({int(n) for n in nums})
    if not nums:
        return "all"
    if len(nums) == 1:
        return str(nums[0])
    if nums[-1] - nums[0] == len(nums) - 1:
        return f"{nums[0]}-{nums[-1]}"
    return "_".join(str(n) for n in nums)


def safe_filename(name: str, fallback: str) -> str:
    name = re.sub(r"\.pdf$", "", (name or "").strip(), flags=re.I)
    name = re.sub(r"[^A-Za-z0-9 _\-\.()]", "", name).strip(" .")
    return (name[:80] or fallback) + ".pdf"

# ─────────────────────────────────────────────────────────────────────────────
# ROUTES
# ─────────────────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/form")
def form_page():
    # the details form now lives inside the single-page app
    return redirect("/", code=302)


@app.route("/health")
def health():
    resp = jsonify({"status": "ok", "service": BRAND})
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Access-Control-Allow-Methods"] = "GET, HEAD, OPTIONS"
    resp.headers["Cache-Control"] = "no-store"
    return resp


@app.route("/template/<name>")
def get_template(name):
    safe = re.sub(r"[^a-zA-Z0-9_\-]", "", name)
    path = os.path.join(app.root_path, "static", "templates", safe + ".pdf")
    if not os.path.exists(path):
        return jsonify({"error": "Template not found"}), 404
    return send_file(path, mimetype="application/pdf")


@app.route("/api/config")
def config():
    """Overlay geometry for the live preview — one source of truth."""
    return jsonify({"page": [PAGE_W, PAGE_H], "font_size": SIZE,
                    "fields": {k: list(v) for k, v in FIELDS.items()}})


@app.route("/api/template-preview", methods=["POST"])
def template_preview():
    """Render page 1 of the blank form to a PNG so the browser can draw on the real thing."""
    f = request.files.get("pdf_b")
    if not f:
        return jsonify({"error": "No file"}), 400
    ok, err = validate_ext(f.filename or "", ALL_TERM_WORK_EXTS, "Term Work template")
    if not ok:
        return jsonify({"error": err}), 400
    try:
        import pypdfium2 as pdfium
        pdf_bytes = to_pdf_bytes(f.read(), f.filename or "")
        doc = pdfium.PdfDocument(pdf_bytes)
        page = doc[0]
        img = page.render(scale=1.4).to_pil().convert("RGB")
        img = img.quantize(colors=48, method=Image.Quantize.MEDIANCUT).convert("P")
        buf = io.BytesIO()
        img.save(buf, "PNG", optimize=True)
        return Response(buf.getvalue(), mimetype="image/png", headers={"Cache-Control": "no-store"})
    except Exception as e:
        return jsonify({"error": f"Preview unavailable: {e}"}), 501


@app.route("/api/parse-index", methods=["POST"])
def parse_index():
    if "pdf_a" not in request.files:
        return jsonify({"error": "No index file uploaded"}), 400
    f = request.files["pdf_a"]
    filename = f.filename or "index.pdf"
    ok, err = validate_ext(filename, ALL_INDEX_EXTS, "Practical Index")
    if not ok:
        return jsonify({"error": err}), 400
    try:
        file_bytes = f.read()
        data = extract_practicals(file_bytes, filename)
        if not data:
            return jsonify({"error": "No practicals found. Make sure the index has a table with SR. No. and Title columns."}), 422
        return jsonify({"practicals": data, "subject": extract_subject_from_index(file_bytes)})
    except Exception as e:
        msg = str(e)
        if "Root object" in msg or "EOF" in msg:
            msg = "This file doesn't look like a valid PDF. Please check and try again."
        return jsonify({"error": msg}), 500


@app.route("/api/generate", methods=["POST"])
def generate():
    """
    multipart:
      pdf_b        – blank Term Work file
      titles_json  – [{"sr_no":"2","title":"…","overrides":{"student_name":"…"}}, …]
      form_json    – shared field values
      filename     – (optional) user-chosen download name
    """
    if "pdf_b" not in request.files:
        return jsonify({"error": "No Term Work file uploaded"}), 400
    f = request.files["pdf_b"]
    filename = f.filename or "term_work.pdf"
    ok, err = validate_ext(filename, ALL_TERM_WORK_EXTS, "Term Work template")
    if not ok:
        return jsonify({"error": err}), 400

    try:
        pdf_b_bytes = to_pdf_bytes(f.read(), filename)
        titles = json.loads(request.form.get("titles_json", "[]"))
        form = json.loads(request.form.get("form_json", "{}"))
    except Exception as e:
        return jsonify({"error": "Bad payload: " + str(e)}), 400
    if not titles:
        return jsonify({"error": "No practicals selected"}), 400

    try:
        merged = PdfWriter()
        for item in titles:
            fc = dict(form)
            fc.update({k: v for k, v in (item.get("overrides") or {}).items() if isinstance(v, str)})
            fc["practical_no"] = str(item["sr_no"])
            page_bytes = build_pdf(pdf_b_bytes, item.get("title", ""), fc)
            for pg in PdfReader(io.BytesIO(page_bytes)).pages:
                merged.add_page(pg)
        out = io.BytesIO()
        merged.write(out)
        out.seek(0)

        default = f"{BRAND}_practicals_{sr_label([t['sr_no'] for t in titles])}"
        return send_file(out, mimetype="application/pdf", as_attachment=True,
                         download_name=safe_filename(request.form.get("filename"), default))
    except Exception as e:
        msg = str(e)
        if "Root object" in msg or "EOF" in msg:
            msg = "Your Term Work file appears corrupted. Please re-upload it."
        return jsonify({"error": msg}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)

"""
OS Practical Term-Work Filler  — v5
- Accepts PDF, JPG, JPEG, PNG, BMP, WEBP, DOCX for Term Work template
- Accepts PDF, JPG, JPEG, PNG for Practical Index
- Predefined template picker
- Health endpoint for splash page
"""
import io, json, os, re
import pdfplumber
from flask import Flask, jsonify, render_template, request, send_file
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
FONT,   SIZE   = "Times-Roman", 12

# ── Supported file types ───────────────────────────────────────────────────────
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".webp", ".tiff", ".tif"}
DOCX_EXTS  = {".docx", ".doc"}
PDF_EXT    = {".pdf"}
ALL_TERM_WORK_EXTS = PDF_EXT | IMAGE_EXTS | DOCX_EXTS
ALL_INDEX_EXTS     = PDF_EXT | IMAGE_EXTS   # index must be parseable

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
    """
    Convert any PIL-readable image (JPG/PNG/BMP/WEBP/TIFF) to a single-page PDF.
    The image is scaled to fit A4 with margins, centred, white background.
    """
    img   = Image.open(io.BytesIO(img_bytes)).convert("RGB")
    iw, ih = img.size

    W, H  = A4        # 595.27 × 841.89 pt
    margin = 28       # pt padding on all sides
    avail_w = W - 2 * margin
    avail_h = H - 2 * margin

    scale = min(avail_w / iw, avail_h / ih)
    dw, dh = iw * scale, ih * scale
    x = margin + (avail_w - dw) / 2
    y = margin + (avail_h - dh) / 2

    buf = io.BytesIO()
    c   = canvas.Canvas(buf, pagesize=A4)
    c.setFillColorRGB(1, 1, 1)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    img_buf = io.BytesIO()
    img.save(img_buf, "PNG")
    img_buf.seek(0)
    c.drawImage(ImageReader(img_buf), x, y, dw, dh)
    c.save()
    buf.seek(0)
    return buf.read()

def docx_to_pdf(docx_bytes: bytes) -> bytes:
    """
    Convert a DOCX file to PDF by extracting all text and reflowing into
    a plain-text PDF. Preserves structure (headings, paragraphs, tables).
    Note: this is a text extraction approach — full layout fidelity isn't
    possible without LibreOffice, which isn't available on Render free tier.
    """
    import docx as python_docx
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.units import pt
    from reportlab.lib import colors

    doc  = python_docx.Document(io.BytesIO(docx_bytes))
    buf  = io.BytesIO()
    pdf  = SimpleDocTemplate(buf, pagesize=A4,
                              leftMargin=50, rightMargin=50,
                              topMargin=50, bottomMargin=50)

    styles = getSampleStyleSheet()
    story  = []

    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            story.append(Spacer(1, 6))
            continue
        style_name = para.style.name or ""
        if "Heading 1" in style_name:
            story.append(Paragraph(text, styles["Heading1"]))
        elif "Heading 2" in style_name:
            story.append(Paragraph(text, styles["Heading2"]))
        else:
            story.append(Paragraph(text, styles["Normal"]))
        story.append(Spacer(1, 4))

    for table in doc.tables:
        data = [[cell.text for cell in row.cells] for row in table.rows]
        if data:
            t = Table(data)
            t.setStyle(TableStyle([
                ("GRID",      (0, 0), (-1, -1), 0.5, colors.grey),
                ("FONTSIZE",  (0, 0), (-1, -1), 9),
                ("PADDING",   (0, 0), (-1, -1), 4),
            ]))
            story.append(t)
            story.append(Spacer(1, 8))

    if not story:
        story.append(Paragraph("(Empty document)", styles["Normal"]))

    pdf.build(story)
    buf.seek(0)
    return buf.read()

def to_pdf_bytes(file_bytes: bytes, filename: str) -> bytes:
    """Route any supported file format to PDF bytes."""
    ext = _ext(filename)
    if ext in PDF_EXT:
        return file_bytes
    if ext in IMAGE_EXTS:
        return image_bytes_to_pdf(file_bytes)
    if ext in DOCX_EXTS:
        return docx_to_pdf(file_bytes)
    raise ValueError(f"Unsupported file type: {ext}")

def validate_ext(filename: str, allowed: set, field_name: str):
    """Return (ok, error_message)."""
    ext = _ext(filename)
    if ext not in allowed:
        nice = ", ".join(sorted(allowed))
        return False, f"{field_name} must be one of: {nice}. Got '{ext}'."
    return True, ""

# ─────────────────────────────────────────────────────────────────────────────
# PDF BUILDING
# ─────────────────────────────────────────────────────────────────────────────

def _w(text): return pdfmetrics.stringWidth(text, FONT, SIZE)

def _fit(text, max_width):
    while text and _w(text) > max_width:
        text = text[:-1]
    return text

def _wrap_experiment(title):
    z1_avail = FIELDS["exp_z1"][2] - FIELDS["exp_z1"][0]
    z2_avail = FIELDS["exp_z2"][2] - FIELDS["exp_z2"][0]
    words, buf = title.split(), []
    for i, word in enumerate(words):
        if _w(" ".join(buf + [word])) <= z1_avail:
            buf.append(word)
        else:
            l1   = " ".join(buf)
            rest = " ".join(words[i:])
            if _w(rest) > z2_avail:
                rest = _fit(rest, z2_avail - _w("…")) + "…"
            return l1, rest
    return " ".join(buf), ""

def extract_practicals_from_ocr(img_bytes: bytes) -> dict:
    """
    Use pytesseract OCR to extract practical titles from an image of the index.
    Handles cases where OCR merges multiple practicals into one block by
    splitting on sentence-ending punctuation mid-block.
    """
    try:
        import pytesseract
        from PIL import ImageEnhance
    except ImportError:
        raise RuntimeError("pytesseract is required for image index parsing.")

    img  = Image.open(io.BytesIO(img_bytes)).convert("L")
    img  = ImageEnhance.Sharpness(img).enhance(2.5)
    img  = ImageEnhance.Contrast(img).enhance(1.8)
    text = pytesseract.image_to_string(img, config="--oem 3 --psm 4")

    # Noise patterns to discard
    NOISE = re.compile(
        r"^(INDEX|PEN|NAME|SUBJECT|RUBRICS|TITLE|DATE|SR\.?|NO\.?|SIGN|MARKS|TOTAL"
        r"|PG\.?|R\s*[\(\[]|M\s*[\(\[]|V\s*[\(\[]|\(?G?\)\.?|TR\]|@|®|\|)",
        re.IGNORECASE
    )

    # Split into paragraph blocks on blank lines
    raw_blocks, current = [], []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            if current:
                raw_blocks.append(current)
                current = []
        else:
            current.append(stripped)
    if current:
        raw_blocks.append(current)

    # New practical starters — these words reliably begin a new practical title
    STARTERS = re.compile(
        r"^(Write|Demonstrate|Study|Implement|Design|Develop|Create|Build|Perform|Explore)\b",
        re.IGNORECASE
    )

    def split_block_on_sentences(lines):
        """
        Split a merged block into sub-blocks wherever a new practical begins.
        A new practical begins when a line starts with a known starter word
        AND the previous lines already form a complete sentence (end with . or )).
        """
        if len(lines) <= 1:
            return [lines]
        sub_blocks, current = [], [lines[0]]
        for line in lines[1:]:
            prev_complete = current[-1].rstrip().endswith(('.', ')'))
            starts_new    = bool(STARTERS.match(line.strip()))
            if prev_complete and starts_new:
                sub_blocks.append(current)
                current = [line]
            else:
                current.append(line)
        if current:
            sub_blocks.append(current)
        return sub_blocks

    # Flatten all blocks, re-splitting on sentence boundaries
    all_blocks = []
    for block in raw_blocks:
        clean = [l for l in block if not NOISE.match(l) and len(l.strip()) > 2]
        if not clean:
            continue
        sub = split_block_on_sentences(clean)
        all_blocks.extend(sub)

    # Convert blocks to practical titles
    practicals = {}
    sr = 0
    for block in all_blocks:
        title = re.sub(r"\s+", " ", " ".join(block)).strip()
        # Clean up common OCR artifacts
        title = re.sub(r"Write\.a\b", "Write a", title)
        title = re.sub(r"\s*\|\s*", " ", title)
        # Must look like a practical: has lowercase words, reasonable length
        if re.search(r"[a-z]{3,}", title) and 8 < len(title) < 300:
            sr += 1
            practicals[sr] = title

    return practicals


def extract_practicals(file_bytes: bytes, filename: str = "index.pdf") -> dict:
    """
    Extract practicals from PDF (via pdfplumber table extraction)
    or from an image (via pytesseract OCR).
    These are two completely different pipelines — images cannot use
    pdfplumber because converting an image→PDF via reportlab produces
    a raster-only PDF with no extractable text objects.
    """
    ext = _ext(filename)

    if ext in IMAGE_EXTS:
        # Image path: OCR directly on the image bytes
        return extract_practicals_from_ocr(file_bytes)

    # PDF path: pdfplumber table extraction
    practicals = {}
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            if not tables:
                continue
            best = max(tables, key=len)
            for row in best:
                if not row or not row[0]:
                    continue
                sr = str(row[0]).strip()
                if not re.match(r"^\d+$", sr):
                    continue
                title = row[2] if len(row) > 2 else ""
                if title:
                    practicals[int(sr)] = " ".join(title.split())
    return practicals

def build_pdf(pdf_b_bytes: bytes, title: str, form: dict) -> bytes:
    l1, l2 = _wrap_experiment(title)
    packet  = io.BytesIO()
    c       = canvas.Canvas(packet, pagesize=(PAGE_W, PAGE_H))
    c.setFont(FONT, SIZE)

    def put(key, text):
        if not text: return
        x, y, mx = FIELDS[key]
        c.drawString(x, y, _fit(str(text), mx - x))

    put("term",         form.get("term", ""))
    put("subject",      form.get("subject", ""))
    put("pen",          form.get("pen", ""))
    put("semester",     form.get("semester", ""))
    put("student_name", form.get("student_name", ""))
    put("class_name",   form.get("class_name", ""))
    put("batch",        form.get("batch", ""))
    put("checked_by",   form.get("checked_by", ""))
    put("practical_no", form.get("practical_no", ""))

    def put_date(prefix, date_str):
        if not date_str: return
        parts = re.split(r"[/\-\.]", date_str.strip())
        if len(parts) == 3:
            put(f"{prefix}_dd",   parts[0].zfill(2))
            put(f"{prefix}_mm",   parts[1].zfill(2))
            put(f"{prefix}_yyyy", parts[2])

    put_date("cond", form.get("conducted_on", ""))
    put_date("sub",  form.get("date_of_sub", ""))
    put_date("act",  form.get("actual_sub", ""))

    sign_raw = form.get("sign_date", "")
    if sign_raw:
        parts = re.split(r"[/\-\.]", sign_raw.strip())
        if len(parts) == 3:
            put("sign_date_dd",   parts[0].zfill(2))
            put("sign_date_mm",   parts[1].zfill(2))
            put("sign_date_yyyy", parts[2])

    put("marks", form.get("marks", ""))
    if l1: c.drawString(FIELDS["exp_z1"][0], FIELDS["exp_z1"][1], l1)
    if l2: c.drawString(FIELDS["exp_z2"][0], FIELDS["exp_z2"][1], l2)

    c.save(); packet.seek(0)

    overlay  = PdfReader(packet).pages[0]
    reader_b = PdfReader(io.BytesIO(pdf_b_bytes))
    writer   = PdfWriter()
    page     = reader_b.pages[0]
    page.merge_page(overlay)
    writer.add_page(page)
    for i in range(1, len(reader_b.pages)):
        writer.add_page(reader_b.pages[i])

    out = io.BytesIO()
    writer.write(out)
    return out.getvalue()

# ─────────────────────────────────────────────────────────────────────────────
# ROUTES
# ─────────────────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/form")
def form_page():
    return render_template("form.html")

@app.route("/health")
def health():
    resp = jsonify({"status": "ok", "service": "termworkforge"})
    resp.headers["Access-Control-Allow-Origin"]  = "*"
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

@app.route("/api/parse-index", methods=["POST"])
def parse_index():
    if "pdf_a" not in request.files:
        return jsonify({"error": "No index file uploaded"}), 400

    f        = request.files["pdf_a"]
    filename = f.filename or "index.pdf"
    ok, err  = validate_ext(filename, ALL_INDEX_EXTS, "Practical Index")
    if not ok:
        return jsonify({"error": err}), 400

    try:
        data = extract_practicals(f.read(), filename)
        if not data:
            return jsonify({"error": "No practicals found. Make sure the index has a table with SR. No. and Title columns."}), 422
        return jsonify({"practicals": data})
    except Exception as e:
        msg = str(e)
        if "Root object" in msg or "EOF" in msg:
            msg = "This file doesn't look like a valid PDF. Please check and try again."
        return jsonify({"error": msg}), 500

@app.route("/api/generate", methods=["POST"])
def generate():
    if "pdf_b" not in request.files:
        return jsonify({"error": "No Term Work file uploaded"}), 400

    f        = request.files["pdf_b"]
    filename = f.filename or "term_work.pdf"
    ok, err  = validate_ext(filename, ALL_TERM_WORK_EXTS, "Term Work template")
    if not ok:
        return jsonify({"error": err}), 400

    try:
        raw_bytes    = f.read()
        pdf_b_bytes  = to_pdf_bytes(raw_bytes, filename)
        titles       = json.loads(request.form.get("titles_json", "[]"))
        form         = json.loads(request.form.get("form_json",   "{}"))
    except Exception as e:
        return jsonify({"error": "Bad payload: " + str(e)}), 400

    if not titles:
        return jsonify({"error": "No practicals selected"}), 400

    try:
        merged = PdfWriter()
        for item in titles:
            fc = dict(form)
            fc["practical_no"] = str(item["sr_no"])
            page_bytes = build_pdf(pdf_b_bytes, item["title"], fc)
            for pg in PdfReader(io.BytesIO(page_bytes)).pages:
                merged.add_page(pg)

        out     = io.BytesIO()
        merged.write(out); out.seek(0)
        sr_list = "_".join(str(t["sr_no"]) for t in titles)
        return send_file(out, mimetype="application/pdf",
                         as_attachment=True,
                         download_name=f"TermWork_{sr_list}.pdf")
    except Exception as e:
        msg = str(e)
        if "Root object" in msg or "EOF" in msg:
            msg = "Your Term Work file appears corrupted. Please re-upload it."
        return jsonify({"error": msg}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)

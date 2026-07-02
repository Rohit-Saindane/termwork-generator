"""
OS Practical Term-Work Filler  — v4
White theme · Mobile-first · Full form fill
"""
import io, json, re
import pdfplumber
from flask import Flask, jsonify, render_template, request, send_file, session
from pypdf import PdfReader, PdfWriter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
app.config["MAX_CONTENT_LENGTH"] = 32 * 1024 * 1024

# ── Page geometry ──────────────────────────────────────────────────────────────
PAGE_W, PAGE_H = 594.96, 842.52
FONT,   SIZE   = "Times-Roman", 12

# ── All field injection coordinates (x, y_reportlab, max_x) ───────────────────
# y_reportlab = PAGE_H − pdfplumber_underline_top + 2
FIELDS = {
    "term":         (502,  609.2, 527),   # TERM: top-right
    "subject":      (111,  585.4, 527),   # Subject:
    "pen":          (97,   562.0, 385),   # PEN:
    "semester":     (479,  562.0, 527),   # Semester:
    "student_name": (157,  536.9, 526),   # Name of Student:
    "class_name":   (101,  516.6, 386),   # Class:
    "batch":        (463,  516.6, 525),   # Batch:
    # Name of Experiment — two zones
    "exp_z1":       (283,  494.9, 523),   # inline after label
    "exp_z2":       (73,   469.9, 526),   # full-width below
    # Checked By (faculty name) — underline x0=136.2 top=582.3 x1=524.4
    "checked_by":   (136,  263.2, 524),
    # Practical No.
    "practical_no": (407,  406.6, 531),
    # Conducted On (DD / MM / YYYY)
    "cond_dd":      (415,  383.7, 445),
    "cond_mm":      (450,  383.7, 480),
    "cond_yyyy":    (485,  383.7, 517),
    # Date of Submission
    "sub_dd":       (413,  361.2, 444),
    "sub_mm":       (448,  360.2, 480),
    "sub_yyyy":     (484,  360.2, 515),
    # Actual Date of Submission
    "act_dd":       (414,  337.7, 447),
    "act_mm":       (451,  337.7, 484),
    "act_yyyy":     (488,  337.7, 518),
    # Bottom row — Date: DD/MM/YYYY slots + Marks
    "sign_date_dd":   (290,   97.5, 322),   # DD  slot (before first /)
    "sign_date_mm":   (327,   97.5, 357),   # MM  slot (between / and /)
    "sign_date_yyyy": (363,   97.9, 392),   # YYYY slot (after second /)
    "marks":          (478,  102.1, 525),   # Marks value
}

# ── Helpers ────────────────────────────────────────────────────────────────────
def _w(text): return pdfmetrics.stringWidth(text, FONT, SIZE)

def _fit(text, max_width):
    """Truncate text to fit within max_width points."""
    while text and _w(text) > max_width:
        text = text[:-1]
    return text

def _wrap_experiment(title):
    """Split title across Zone1 (inline) then Zone2 (full-width below)."""
    z1_avail = FIELDS["exp_z1"][2] - FIELDS["exp_z1"][0]  # ~240pt
    z2_avail = FIELDS["exp_z2"][2] - FIELDS["exp_z2"][0]  # ~453pt
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

def extract_practicals(pdf_bytes):
    practicals = {}
    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            if not tables: continue
            best = max(tables, key=len)
            for row in best:
                if not row or not row[0]: continue
                sr = str(row[0]).strip()
                if not re.match(r"^\d+$", sr): continue
                title = row[2] if len(row) > 2 else ""
                if title:
                    practicals[int(sr)] = " ".join(title.split())
    return practicals

def build_pdf(pdf_b_bytes, title, form):
    """Overlay all form fields + experiment title onto one Term Work page."""
    l1, l2 = _wrap_experiment(title)

    packet = io.BytesIO()
    c = canvas.Canvas(packet, pagesize=(PAGE_W, PAGE_H))
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

    # Date fields — split DD/MM/YYYY from a single date string
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

    # Bottom row — signature date split into DD / MM / YYYY slots
    sign_raw = form.get("sign_date", "")
    if sign_raw:
        parts = re.split(r"[/\-\.]", sign_raw.strip())
        if len(parts) == 3:
            put("sign_date_dd",   parts[0].zfill(2))
            put("sign_date_mm",   parts[1].zfill(2))
            put("sign_date_yyyy", parts[2])

    put("marks", form.get("marks", ""))

    # Experiment title (two zones)
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

# ── Routes ─────────────────────────────────────────────────────────────────────
@app.route("/template/<name>")
def get_template(name):
    """Serve a predefined Term Work template PDF from static/templates/."""
    import os
    safe = re.sub(r"[^a-zA-Z0-9_\-]", "", name)   # sanitise filename
    path = os.path.join(app.root_path, "static", "templates", safe + ".pdf")
    if not os.path.exists(path):
        return jsonify({"error": "Template not found"}), 404
    return send_file(path, mimetype="application/pdf")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/form")
def form_page():
    return render_template("form.html")

@app.route("/health")
def health():
    """
    Lightweight readiness probe used by the standalone splash page to detect
    when the Flask app (not just Render's proxy) is actually responding.
    Returns a small JSON payload with CORS enabled so the splash page —
    hosted on a different origin — can read the response, not just an
    opaque no-cors signal that would false-positive on Render's own
    wake-up placeholder.
    """
    resp = jsonify({"status": "ok", "service": "termworkforge"})
    resp.headers["Access-Control-Allow-Origin"]  = "*"
    resp.headers["Access-Control-Allow-Methods"] = "GET, HEAD, OPTIONS"
    resp.headers["Cache-Control"] = "no-store"
    return resp

@app.route("/api/parse-index", methods=["POST"])
def parse_index():
    if "pdf_a" not in request.files:
        return jsonify({"error": "No index PDF"}), 400
    try:
        data = extract_practicals(request.files["pdf_a"].read())
        if not data:
            return jsonify({"error": "No practicals found"}), 422
        return jsonify({"practicals": data})
    except Exception as e:
        msg = str(e)
        if "Root object" in msg or "PDF" in msg or "EOF" in msg:
            msg = "This file doesn't look like a valid PDF. Please check the file and try again."
        return jsonify({"error": msg}), 500

@app.route("/api/generate", methods=["POST"])
def generate():
    """
    Body (multipart):
      pdf_b        – blank Term Work PDF
      titles_json  – JSON: [{"sr_no":"1","title":"Study of…"}, …]
      form_json    – JSON: { subject, pen, semester, … }
    """
    if "pdf_b" not in request.files:
        return jsonify({"error": "No Term Work PDF"}), 400

    try:
        pdf_b_bytes  = request.files["pdf_b"].read()
        titles       = json.loads(request.form.get("titles_json", "[]"))
        form         = json.loads(request.form.get("form_json",   "{}"))
    except Exception as e:
        return jsonify({"error": "Bad payload: " + str(e)}), 400

    if not titles:
        return jsonify({"error": "No practicals selected"}), 400

    try:
        merged = PdfWriter()
        for item in titles:
            form_copy = dict(form)
            form_copy["practical_no"] = str(item["sr_no"])
            page_bytes = build_pdf(pdf_b_bytes, item["title"], form_copy)
            for pg in PdfReader(io.BytesIO(page_bytes)).pages:
                merged.add_page(pg)

        out = io.BytesIO()
        merged.write(out); out.seek(0)

        sr_list = "_".join(str(t["sr_no"]) for t in titles)
        return send_file(out, mimetype="application/pdf",
                         as_attachment=True,
                         download_name=f"TermWork_{sr_list}.pdf")
    except Exception as e:
        msg = str(e)
        if "Root object" in msg or "EOF" in msg:
            msg = "Your Term Work PDF appears to be corrupted or invalid. Please re-upload it."
        return jsonify({"error": msg}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)

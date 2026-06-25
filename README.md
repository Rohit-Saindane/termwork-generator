# Term Work Filler — Setup Guide

## Project Structure
```
termwork/
├── app.py
├── requirements.txt
├── README.md
└── templates/
    ├── index.html   ← Page 1: upload + select practicals
    └── form.html    ← Page 2: fill details + download
```

---

## Setup in VS Code (Step by Step)

### 1. Open the folder
```
File → Open Folder → select the `termwork` folder
```

### 2. Create virtual environment
Open terminal with  Ctrl+`
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the app
```bash
python app.py
```

### 5. Open in browser
Visit → **http://localhost:5000**

On mobile: make sure your phone is on the same Wi-Fi,
then visit → **http://YOUR_PC_IP:5000**
(find your PC IP with `ipconfig` on Windows or `ifconfig` on Mac/Linux)

---

## How to Use

**Page 1 — Upload & Select**
1. Upload your OS Practical Index PDF
2. Tap "Parse Practicals" — all 10 appear as cards
3. Select the ones you need (tap individual cards, or "Select All")
4. Upload the blank Term Work form PDF
5. Tap "Continue to Fill Details →"

**Page 2 — Fill Details**
- Fill in any or all fields (Name, PEN, Class, Dates, etc.)
- All fields are optional — skip freely
- Tap "Generate Term Work PDFs"
- If any fields are empty, you'll see a confirmation before proceeding
- One merged PDF downloads with one page per practical

---

## Field Coordinate Reference (app.py)
All coordinates are calibrated for the specific Term Work PDF used.
If you use a different form, update the `FIELDS` dict in `app.py`.

Font: Times-Roman, 12pt (matches the original PDF exactly)

Zone 1 (inline, after "Name of Experiment:" label): x=283, y=494.9
Zone 2 (full-width below): x=73, y=469.9

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` in venv |
| Port 5000 in use | Change `port=5000` to `port=5001` in `app.py` |
| Text in wrong position | Adjust FIELDS coords in `app.py` |
| Phone can't connect | Check firewall, run `app.run(host='0.0.0.0', port=5000)` |

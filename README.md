# PM_Project

A small Flask-based reference site comparing major project management standards (ISO 21502, PMI/PMBOK, and PRINCE2). The app provides curated similarities, differences, and unique elements across the standards and links to local PDF references stored in the `Books/` directory.

## Features

- Static, easy-to-read comparison tables (similarities, differences, unique elements).
- Quick links to local PDF copies of standards in `Books/` and inferred page anchors where possible.
- Minimal Flask app intended for local use or lightweight demos.

## Project layout

```
app.py                # Flask application (entrypoint)
Books/                # Place PDFs here (ISO, PMBOK, PRINCE2 PDFs included)
static/               # CSS and other static assets
templates/            # Jinja2 templates: index, section, reference
README.md             # This file
```

Included sample PDFs (already present in this repo):

- `ISO 21502.pdf`
- `ISO21500.pdf`
- `PMBOK7.pdf`
- `PRINCE2.pdf`

## Requirements

- Python 3.8+ (3.11 recommended)
- Flask

There is no pinned requirements file in this repository. For a minimal environment, install Flask directly:

```fish
# create and activate a venv (fish shell)
python3 -m venv .venv
source .venv/bin/activate.fish

# install Flask
pip install flask
```

## Run (development)

The app can be launched directly with Python:

```fish
python app.py
```

Open http://localhost:5000 in your browser. The app runs on port 5000 by default (see `app.py`).

## Routes / Usage

- `/` — Home page showing an overview and navigation.
- `/section/<name>` — Show a comparison section. Supported `name` values in code: `similarities`, `differences`, `unique`.
- `/reference?id=<id>&label=<label>&theme=<theme>&summary=<summary>` — Reference view. The `label` parameter is parsed to infer which PDF (from `Books/`) and a page number when possible.
- `/books/<filename>` — Serves files from the `Books/` directory (used for the PDF links).

Notes:

- The app attempts to infer which PDF to open from human labels (for example, labels mentioning "ISO" or "PMBOK"). If a PDF exists in `Books/`, the app will generate a link to it and include an optional `#page=` anchor when a page number can be parsed.
- For security, `serve_book` performs a safe path check before returning files.

## Development notes & TODOs

- The Flask `SECRET_KEY` is hard-coded in `app.py` for convenience. Rotate this and use environment variables in production.
- Consider adding a `requirements.txt` (pin Flask version) and a small test harness.
- If you add more PDF references, place them in the `Books/` folder and use the existing label patterns so the app can discover them.

## Contributing

Feel free to open issues or pull requests. Small, focused contributions like adding a `requirements.txt`, improving templates, or making the PDF parsing more robust are welcome.

## License & Credits

This project is provided as-is for educational/demonstration use. No license file is included; add one if you need an explicit license.

---

If you want, I can also add a `requirements.txt`, a small test, or tweak templates to improve the UI. Tell me which next.
# PM_Project

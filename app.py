from flask import Flask, render_template, request, send_from_directory, abort, url_for
import os
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = 'pm-standards-secret-key-2025'

# --- DATA STRUCTURE ---
PM_STANDARDS = {
    "similarities": {
        "title": "7 Key Similarities",
        "rows": [
            {"theme": "Lifecycle orientation", "summary": "All three standards describe a project lifecycle and emphasise staged progression through phases.", "refs": [{"label": "ISO 21502 §3.1 p.9", "id": "iso_3_1_p9"}, {"label": "PMI §1.2 p.12", "id": "pmi_1_2_p12"}, {"label": "PRINCE2 Ch 5 p.60", "id": "prince2_ch5_p60"}]},
            {"theme": "Tailoring to context", "summary": "Each encourages tailoring the approach to the organisation and project's context.", "refs": [{"label": "ISO §2.5 p.6", "id": "iso_2_5_p6"}, {"label": "PMI §2.1 p.20", "id": "pmi_2_1_p20"}, {"label": "PRINCE2 Principle 7 p.29", "id": "prince2_principle7_p29"}]},
            {"theme": "Stakeholder engagement", "summary": "All emphasise stakeholder identification, engagement and communications.", "refs": [{"label": "ISO §4.2 p.13", "id": "iso_4_2_p13"}, {"label": "PMI §10.1 p.180", "id": "pmi_10_1_p180"}, {"label": "PRINCE2 'Organising' pp.74-93", "id": "prince2_organising_p74_93"}]},
            {"theme": "Governance and roles", "summary": "Clear governance, roles and responsibilities are required in each standard.", "refs": [{"label": "ISO §4.5 p.14", "id": "iso_4_5_p14"}, {"label": "PMI §3.4 p.45", "id": "pmi_3_4_p45"}, {"label": "PRINCE2 Principle 3 p.24", "id": "prince2_principle3_p24"}]},
            {"theme": "Integration and coordination", "summary": "Integration across disciplines and coordination of work streams is common to all.", "refs": [{"label": "ISO §5.1 p.22", "id": "iso_5_1_p22"}, {"label": "PMI Integration Management Ch p.78", "id": "pmi_integration_p78"}, {"label": "PRINCE2 'Practices' Ch 5–11 pp.55–211", "id": "prince2_ch5_11_p55_211"}]},
            {"theme": "Business justification & benefits", "summary": "All require a business justification or benefits focus for running projects.", "refs": [{"label": "ISO Ch 5 'Business Case' p.55", "id": "iso_businesscase_p55"}, {"label": "PMI Benefits Realization p.27", "id": "pmi_benefits_p27"}, {"label": "PRINCE2 Business Case p.61", "id": "prince2_businesscase_p61"}]},
            {"theme": "Continuous improvement", "summary": "Lessons learned, continual improvement and knowledge capture are encouraged.", "refs": [{"label": "ISO §7 'Improvement' p.88", "id": "iso_improvement_p88"}, {"label": "PMI 'Lessons Learned' p.210", "id": "pmi_lessons_p210"}, {"label": "PRINCE2 'Learn from Experience' p.22", "id": "prince2_learn_p22"}]}
        ]
    },
    "differences": {
        "title": "7 Major Differences",
        "rows": [
            {"theme": "Nature of guidance", "summary": "ISO standards provide concise, international normative guidance; PRINCE2 is a prescriptive method; PMI provides a broad body of practice and guidance.", "refs": [{"label": "ISO Preface", "id": "iso_preface"}, {"label": "PRINCE2 Preface xii", "id": "prince2_preface_xii"}, {"label": "PMI Preface v", "id": "pmi_preface_v"}]},
            {"theme": "Terminology", "summary": "Each uses different core terminology (e.g., 'practice' vs 'process' vs 'principle').", "refs": [{"label": "ISO Glossary", "id": "iso_glossary"}, {"label": "PMI Glossary", "id": "pmi_glossary"}, {"label": "PRINCE2 Glossary", "id": "prince2_glossary"}]},
            {"theme": "Governance depth", "summary": "PRINCE2 provides detailed governance and document templates; ISO is higher-level; PMI focuses on processes and inputs/outputs.", "refs": [{"label": "PRINCE2 Ch 14 p.229", "id": "prince2_ch14_p229"}, {"label": "ISO §4 p.12", "id": "iso_4_p12"}, {"label": "PMI §2.3 p.42", "id": "pmi_2_3_p42"}]},
            {"theme": "Structure granularity", "summary": "PMI's PMBOK (ITTOs) is more prescriptive in inputs/outputs and tools; PRINCE2 structures stages and products; ISO gives principles and practices.", "refs": [{"label": "PMI Ch 5–7 pp.78–195", "id": "pmi_ch5_7_p78_195"}, {"label": "PRINCE2 Ch 2–19 pp.19–284", "id": "prince2_ch2_19_p19_284"}, {"label": "ISO Overview", "id": "iso_overview"}]},
            {"theme": "People & cultural focus", "summary": "PRINCE2 emphasizes roles, responsibilities and people aspects more explicitly than ISO; PMI includes people management within knowledge areas.", "refs": [{"label": "PRINCE2 Ch 3 pp.31–45", "id": "prince2_ch3_p31_45"}, {"label": "PMI §6.5–6.7 pp.143–150", "id": "pmi_6_5_6_7_p143_150"}, {"label": "ISO §4.6 p.15", "id": "iso_4_6_p15"}]},
            {"theme": "Benefits realization position", "summary": "ISO and PMI place benefits realization as central; PRINCE2 treats benefits through the Business Case and project board oversight.", "refs": [{"label": "ISO §5 'Benefits' p.60", "id": "iso_benefits_p60"}, {"label": "PMI §1.10 p.27", "id": "pmi_1_10_p27"}, {"label": "PRINCE2 Ch 5 p.61", "id": "prince2_ch5_p61"}]},
            {"theme": "Philosophy & adoption", "summary": "PMI is widely used in industry practices and certifications; PRINCE2 is often used in UK/Europe with strong method adoption; ISO is used for aligning standards internationally.", "refs": [{"label": "PMI Adoption notes", "id": "pmi_adoption"}, {"label": "PRINCE2 Adoption notes", "id": "prince2_adoption"}, {"label": "ISO Adoption notes", "id": "iso_adoption"}]}
        ]
    },
    "unique": {
        "title": "7 Unique Elements",
        "rows": [
            {"theme": "ISO - standardised terminology & international alignment", "summary": "ISO 21502 provides internationally recognised standard terminology and alignment with other ISO management standards.", "refs": [{"label": "ISO 21502 §1 p.3", "id": "iso_1_p3"}]},
            {"theme": "ISO - explicit change management linkage", "summary": "ISO ties project change control explicitly to organisational change management and governance.", "refs": [{"label": "ISO §7.14 pp.40–41", "id": "iso_7_14_p40_41"}]},
            {"theme": "PMI - ITTO model and knowledge areas", "summary": "PMBOK maintains the Inputs-Tools-Techniques-Outputs model and organized knowledge areas and process groups.", "refs": [{"label": "PMI Ch 5–7 pp.78–195", "id": "pmi_5_7_p78_195"}]},
            {"theme": "PMI - integration across versions and toolkits", "summary": "PMI publishes toolkits, practice guides and ties to certification, offering pragmatic toolsets for practitioners.", "refs": [{"label": "PMI Preface v and §1.7 p.19", "id": "pmi_preface_v_1_7_p19"}]},
            {"theme": "PRINCE2 - product-based planning & people element", "summary": "PRINCE2 emphasises product-based planning and clear role definitions (e.g., project board).", "refs": [{"label": "PRINCE2 Ch 3 pp.31–45", "id": "prince2_ch3_p31_45"}]},
            {"theme": "PRINCE2 - focus on tailoring, digital & sustainability guidance", "summary": "Newer PRINCE2 materials explicitly mention digital delivery and sustainability considerations in guidance and tailoring.", "refs": [{"label": "PRINCE2 Preface xii", "id": "prince2_preface_xii"}]},
            {"theme": "PMI - toolkits & automation guidance", "summary": "PMI provides guidance on tool-supported practices, automation and modern delivery toolkits.", "refs": [{"label": "PMI Ch 9–10 pp.201–315", "id": "pmi_ch9_10_p201_315"}]}
        ]
    }
}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/section/<name>')
def section(name):
    section = PM_STANDARDS.get(name)
    if not section:
        return "Not found", 404
    return render_template('section.html', section=section, name=name)


@app.route('/reference')
def reference():
    ref_id = request.args.get('id', 'unknown')
    label = request.args.get('label', 'Reference')
    theme = request.args.get('theme', '')
    summary = request.args.get('summary', '')

    pdf_filename, page_number = _parse_label_to_pdf_and_page(label)
    open_url = None
    if pdf_filename:
        open_url = url_for('serve_book', filename=pdf_filename)
        if page_number:
            open_url += f"#page={page_number}"

    return render_template('reference.html', ref_id=ref_id, label=label, theme=theme, summary=summary, open_url=open_url)


@app.route('/books/<path:filename>')
def serve_book(filename: str):
    books_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Books')
    safe_path = os.path.normpath(os.path.join(books_dir, filename))
    if not safe_path.startswith(books_dir):
        abort(404)
    if not os.path.exists(safe_path):
        abort(404)
    return send_from_directory(books_dir, filename)


def _parse_label_to_pdf_and_page(label: str):
    """Infer the PDF filename in Books/ and the first page number from a human label."""
    normalized = label or ""
    lower = normalized.lower()

    filename = None
    # ✅ FIX: Match any 'ISO' reference, not just 'ISO 21502'
    if 'iso' in lower:
        filename = 'ISO 21502.pdf'
    elif 'iso 21500' in lower or 'iso21500' in lower or 'iso-21500' in lower:
        filename = 'ISO21500.pdf'
    elif 'prince2' in lower or 'prince 2' in lower:
        filename = 'PRINCE2.pdf'
    elif 'pmbok' in lower or 'pmi' in lower or 'pmi guide' in lower:
        filename = 'PMBOK7.pdf'

    # Extract page number
    page = None
    cleaned = normalized.replace('–', '-').replace('—', '-')
    match = re.search(r"\bpp?\.?\s*(\d+)", cleaned, flags=re.IGNORECASE)
    if not match:
        match = re.search(r"\bp\.?\s*(\d+)", cleaned, flags=re.IGNORECASE)
    if not match:
        match = re.search(r"\b(\d{1,4})\b", cleaned)
    if match:
        try:
            page = int(match.group(1))
        except ValueError:
            page = None

    return filename, page


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

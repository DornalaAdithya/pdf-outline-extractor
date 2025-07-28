import fitz  # PyMuPDF
import json
import os

# ----------- Helper: Classify Span Using Multiple Features -------------
def classify_span(span):
    text = span.get("text", "").strip()
    size = span.get("size", 0)
    font = span.get("font", "").lower()
    flags = span.get("flags", 0)
    bbox = span.get("bbox", [0, 0, 0, 0])

    if not text or len(text) < 3:
        return None

    is_bold = "bold" in font or (flags & 2 != 0)
    is_upper = text.isupper()
    is_centered = abs((bbox[0] + bbox[2]) / 2 - 300) < 70
    is_top = bbox[1] < 150

    # Flexible Title rule — but not too loose
    if size >= 20 and is_bold and is_top:
        return "Title"
    elif is_bold and size >= 17:
        return "H1"
    elif is_bold or size >= 14:
        return "H2"
    elif is_upper or is_bold:
        return "H3"
    return None

# ----------- Extract Headings From One Page -------------
def extract_headings_from_page(page, page_number):
    headings = []
    blocks = page.get_text("dict")["blocks"]

    for b in blocks:
        for l in b.get("lines", []):
            for s in l.get("spans", []):
                level = classify_span(s)
                if level:
                    headings.append({
                        "level": level,
                        "text": s["text"].strip(),
                        "page": page_number,
                        "size": s.get("size", 0),
                        "flags": s.get("flags", 0),
                        "font": s.get("font", "")
                    })
    return headings

# ----------- Main PDF Processing Logic -------------
def extract_outline_from_pdf(pdf_path):
    outline = []
    title = None
    doc = fitz.open(pdf_path)

    for i, page in enumerate(doc):
        page_number = i + 1
        headings = extract_headings_from_page(page, page_number)

        for h in headings:
            # STRONGER TITLE DETECTION
            if title is None:
                text = h["text"].lower()

                if "report" in text or "summary" in text or "overview" in text:
                    title = h["text"]
                    continue

                # fallback: biggest heading on page 1
                if page_number == 1 and h["level"] in ("Title", "H1", "H2"):
                    title = h["text"]
                    continue

            outline.append({
                "level": h["level"],
                "text": h["text"],
                "page": h["page"]
            })

    doc.close()
    return {
        "title": title or "Untitled Document",
        "outline": outline
    }

# ----------- Batch Process PDFs -------------
def process_all_pdfs(input_dir="/app/input", output_dir="/app/output"):
    print(f"📂 Scanning input folder: {input_dir}")
    for file in os.listdir(input_dir):
        if file.lower().endswith(".pdf"):
            print(f"📄 Processing: {file}")
            pdf_path = os.path.join(input_dir, file)
            result = extract_outline_from_pdf(pdf_path)
            out_file = os.path.join(output_dir, file.replace(".pdf", ".json"))
            with open(out_file, "w", encoding="utf-8") as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            print(f"✅ Saved: {out_file}")

if __name__ == "__main__":
    process_all_pdfs()
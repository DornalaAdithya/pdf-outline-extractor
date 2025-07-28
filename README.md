# Adobe Hackathon 2025 - Round 1A: Structured PDF Outline Extractor

## 🧠 Challenge Overview

Extract a structured outline from raw PDFs, including:
- Title
- Headings: H1, H2, H3
- Page number for each heading

Output format must follow Adobe's required JSON structure, and the solution must run **offline**, within a **Docker container**, using **≤200MB CPU-only logic**.

---

## 🧰 Technologies Used

- Python 3.10
- [PyMuPDF (fitz)](https://github.com/pymupdf/PyMuPDF)
- Docker (Linux/amd64)
- No machine learning model (fully rule-based)

---

## ✅ Features

- Extracts `Title`, `H1`, `H2`, and `H3` based on font size, position, and styling
- Applies intelligent fallback logic to detect the most likely title
- Outputs to JSON per Adobe’s required format
- Works entirely offline with zero internet dependency
- Processes multiple PDFs in `/app/input`, outputs to `/app/output`

---

## 📂 Sample Output Format

```json
{
  "title": "Annual Financial Report 2024",
  "outline": [
    { "level": "H2", "text": "Revenue Overview", "page": 1 },
    { "level": "H2", "text": "R&D Expenses", "page": 1 }
  ]
}
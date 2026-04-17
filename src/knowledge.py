import os
import re

import fitz  # PyMuPDF


def _clean_title(filename):
    """Derive a clean display title from a PDF filename."""
    name = os.path.splitext(filename)[0]
    # Remove Zone.Identifier suffix if present
    name = re.sub(r":Zone\.Identifier$", "", name)
    return name


def extract_modules(pdf_directory):
    """Extract text from all PDF files in the given directory.

    Returns a list of CourseModule dicts per data-model.md:
      [{"filename": str, "title": str, "content": str, "page_count": int}, ...]
    """
    modules = []
    for entry in sorted(os.listdir(pdf_directory)):
        if not entry.lower().endswith(".pdf"):
            continue
        filepath = os.path.join(pdf_directory, entry)
        if not os.path.isfile(filepath):
            continue
        try:
            doc = fitz.open(filepath)
            text_parts = []
            for page in doc:
                text_parts.append(page.get_text())
            content = "\n".join(text_parts).strip()
            if not content:
                continue
            modules.append({
                "filename": entry,
                "title": _clean_title(entry),
                "content": content,
                "page_count": len(doc),
            })
            doc.close()
        except Exception:
            # Skip files that can't be parsed
            continue
    return modules


def build_knowledge_text(modules):
    """Build a single text string from all modules for use in LLM context."""
    parts = []
    for mod in modules:
        parts.append(f"=== {mod['title']} ===\n{mod['content']}")
    return "\n\n".join(parts)

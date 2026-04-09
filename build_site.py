from html import escape
import re

BIB_FILE = "publications.bib"
INDEX_FILE = "index.html"
TARGET_AUTHOR = "Yuhang Bai"


def split_entries(text):
    entries = []
    i = 0
    n = len(text)
    while i < n:
        at = text.find("@", i)
        if at == -1:
            break

        brace = text.find("{", at)
        if brace == -1:
            break

        entry_type = text[at + 1:brace].strip()
        depth = 1
        j = brace + 1
        while j < n and depth > 0:
            if text[j] == "{":
                depth += 1
            elif text[j] == "}":
                depth -= 1
            j += 1

        raw_body = text[brace + 1:j - 1].strip()
        if raw_body:
            entries.append((entry_type, raw_body))
        i = j
    return entries


def parse_value(body, pos):
    while pos < len(body) and body[pos].isspace():
        pos += 1

    if pos >= len(body):
        return "", pos

    if body[pos] == "{":
        depth = 1
        pos += 1
        start = pos
        while pos < len(body) and depth > 0:
            if body[pos] == "{":
                depth += 1
            elif body[pos] == "}":
                depth -= 1
            pos += 1
        value = body[start:pos - 1]
    elif body[pos] == '"':
        pos += 1
        start = pos
        while pos < len(body):
            if body[pos] == '"' and body[pos - 1] != "\\":
                break
            pos += 1
        value = body[start:pos]
        pos += 1
    else:
        start = pos
        while pos < len(body) and body[pos] not in ",\n":
            pos += 1
        value = body[start:pos].strip()

    while pos < len(body) and body[pos].isspace():
        pos += 1
    if pos < len(body) and body[pos] == ",":
        pos += 1

    return value.strip(), pos


def parse_entry(entry_type, raw_body):
    if "," not in raw_body:
        return None

    entry_id, body = raw_body.split(",", 1)
    entry = {"ENTRYTYPE": entry_type.strip(), "ID": entry_id.strip()}
    pos = 0

    while pos < len(body):
        while pos < len(body) and body[pos] in " \t\r\n,":
            pos += 1
        if pos >= len(body):
            break

        eq = body.find("=", pos)
        if eq == -1:
            break

        field = body[pos:eq].strip().lower()
        pos = eq + 1
        value, pos = parse_value(body, pos)
        if field:
            entry[field] = value

    return entry


def load_bib_entries(path):
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    entries = []
    for entry_type, raw_body in split_entries(text):
        entry = parse_entry(entry_type, raw_body)
        if entry:
            entries.append(entry)
    return entries


def normalize_spaces(text):
    return re.sub(r"\s+", " ", text).strip()


def strip_braces(text):
    return text.replace("{", "").replace("}", "")


def normalize_name(name):
    return normalize_spaces(strip_braces(name)).lower()


def format_authors(authors_str):
    if not authors_str:
        return ""

    authors = [a.strip() for a in authors_str.replace("\n", " ").split(" and ") if a.strip()]
    formatted = []
    for author in authors:
        if "," in author:
            parts = author.split(",", 1)
            author = f"{parts[1].strip()} {parts[0].strip()}"
        author = normalize_spaces(strip_braces(author))
        if normalize_name(author) == TARGET_AUTHOR.lower():
            formatted.append(f"<strong>{escape(TARGET_AUTHOR)}</strong>")
        else:
            formatted.append(escape(author))
    return ", ".join(formatted)


def determine_category(entry):
    entry_type = entry.get("ENTRYTYPE", "").lower()
    journal = entry.get("journal", "").lower()
    note = entry.get("note", "").lower()

    if entry_type == "unpublished" or "arxiv" in journal or "arxiv" in note:
        return "Preprint"
    if entry_type == "article":
        return "Journal"
    if entry_type in ["inproceedings", "conference"]:
        return "Conference"
    return "Preprint"


def get_year(entry):
    if "year" in entry:
        return str(entry["year"])
    match = re.search(r"\d{4}", entry.get("ID", ""))
    if match:
        return match.group(0)
    return "0"


def build_venue(entry, category):
    parts = []
    if category == "Conference" and entry.get("booktitle"):
        parts.append(f"In {strip_braces(entry.get('booktitle', ''))}")
    elif entry.get("journal"):
        parts.append(strip_braces(entry.get("journal", "")))
    elif "arxiv" in entry.get("note", "").lower():
        parts.append(strip_braces(entry.get("note", "")))

    vol_info = ""
    if entry.get("volume"):
        vol_info += strip_braces(entry.get("volume", ""))
        if entry.get("number"):
            vol_info += f" ({strip_braces(entry.get('number', ''))})"
    if entry.get("pages"):
        pages = strip_braces(entry.get("pages", ""))
        vol_info = f"{vol_info}, {pages}" if vol_info else pages

    if vol_info:
        parts.append(vol_info)

    return ", ".join(part for part in parts if part)


def build_title(entry):
    title = escape(normalize_spaces(strip_braces(entry.get("title", ""))))
    url = entry.get("url", "").strip()
    if url:
        return f'<a class="pub-title" href="{escape(url, quote=True)}">{title}</a>'
    return f'<span class="pub-title">{title}</span>'


def build_publication_html(entry, idx, category):
    authors = format_authors(entry.get("author", ""))
    title_html = build_title(entry)
    venue = build_venue(entry, category)
    venue_html = f'<span class="pub-venue">{escape(venue)}</span>' if venue else ""
    is_submitted = entry.get("note", "").lower().strip() == "submitted"
    status_html = '<span class="pub-status">Submitted</span>' if is_submitted else ""

    summary_bits = [bit for bit in [authors, title_html, venue_html, status_html] if bit]
    summary_html = ". ".join(summary_bits).replace("..", ".")

    lines = [
        '    <article class="pub-item">',
        f'      <div class="pub-index">[{idx}]</div>',
        '      <div class="pub-main">',
        f'        <p class="pub-text">{summary_html}.</p>',
    ]

    abstract = normalize_spaces(entry.get("abstract", ""))
    if abstract:
        lines.extend([
            '        <details class="pub-abstract">',
            "          <summary>Abstract</summary>",
            f"          <blockquote>{escape(abstract)}</blockquote>",
            "        </details>",
        ])

    lines.extend([
        "      </div>",
        "    </article>",
    ])
    return "\n".join(lines)


def generate_html(entries):
    categories = {"Preprint": [], "Journal": [], "Conference": []}

    for i, entry in enumerate(entries):
        entry["_original_index"] = i

    for entry in entries:
        cat = determine_category(entry)
        if cat in categories:
            categories[cat].append(entry)

    for cat in categories:
        if cat == "Journal":
            categories[cat].sort(
                key=lambda x: (
                    1 if x.get("note", "").lower().strip() == "submitted" else 0,
                    get_year(x),
                    x["_original_index"],
                ),
                reverse=True,
            )
        else:
            categories[cat].sort(
                key=lambda x: (
                    get_year(x),
                    x["_original_index"],
                ),
                reverse=True,
            )

    lines = []
    for cat_name, cat_entries in categories.items():
        if not cat_entries:
            continue

        lines.extend([
            '<section class="pub-group">',
            f"  <h3>{escape(cat_name)}</h3>",
            '  <div class="pub-list">',
        ])

        total_entries = len(cat_entries)
        for i, entry in enumerate(cat_entries):
            idx = total_entries - i
            lines.append(build_publication_html(entry, idx, cat_name))

        lines.extend([
            "  </div>",
            "</section>",
        ])

    return "\n".join(lines)


def main():
    try:
        entries = load_bib_entries(BIB_FILE)
    except FileNotFoundError:
        print(f"Error: {BIB_FILE} not found.")
        return

    new_html = generate_html(entries)

    try:
        with open(INDEX_FILE, "r", encoding="utf-8") as f:
            content = f.read()

        pattern = re.compile(r"(<!-- PUBS_START -->).*?(<!-- PUBS_END -->)", re.DOTALL)
        if pattern.search(content):
            new_content = pattern.sub(r"\g<1>\n" + new_html + r"\n\g<2>", content)
            with open(INDEX_FILE, "w", encoding="utf-8") as f:
                f.write(new_content)
            print("Successfully updated index.html")
        else:
            print("Markers <!-- PUBS_START --> and <!-- PUBS_END --> not found in index.html")
    except FileNotFoundError:
        print(f"Error: {INDEX_FILE} not found.")


if __name__ == "__main__":
    main()

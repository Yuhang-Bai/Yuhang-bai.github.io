# scripts/bib2md.py
import re
from pathlib import Path
import bibtexparser

SELF_NAMES = ["Yuhang Bai"]  # 自定义：需要高亮的作者名

MONTHS = {m:i for i,m in enumerate(
    ["jan","feb","mar","apr","may","jun","jul","aug","sep","oct","nov","dec"], start=1)}

def normalize(name):
    return re.sub(r"\s+", " ", name).strip().lower()

def highlight_author(name):
    base = name.strip()
    for s in SELF_NAMES:
        if normalize(base) == normalize(s):
            return f"**{base}**"
    return base

def fmt_authors(s):
    if not s:
        return ""
    names = [n.strip() for n in s.split(" and ") if n.strip()]
    names = [highlight_author(n) for n in names]
    if len(names) <= 2:
        return " and ".join(names)
    return ", ".join(names[:-1]) + " and " + names[-1]

def venue_of(e):
    parts = []
    if e.get("journal"):
        parts.append(e["journal"])
    elif e.get("booktitle"):
        parts.append(e["booktitle"])

    # 期刊/会议的补充信息
    if e.get("series"):
        parts.append(e["series"])
    tail = []
    if e.get("volume"): tail.append(e["volume"])
    if e.get("number"): tail.append(f"({e['number']})")
    vol = " ".join(tail).strip()
    if vol:
        parts[-1] = parts[-1] + " " + vol
    if e.get("pages"):
        parts.append(e["pages"])
    return ", ".join(parts)

def month_num(e):
    m = (e.get("month") or "").strip().lower()
    try:
        return int(m)
    except:
        return MONTHS.get(m[:3], 0)

def link_of(e):
    doi = e.get("doi")
    url = e.get("url")
    eprint = e.get("eprint")
    if doi:
        return f"https://doi.org/{doi}"
    if url:
        return url
    if eprint and ("arxiv" in (e.get("archivePrefix","") + e.get("note","")).lower() or re.fullmatch(r"\d{4}\.\d{5}(v\d+)?|\d{2}\d{2}\.\d{5}(v\d+)?", eprint)):
        return f"https://arxiv.org/abs/{eprint}"
    return None

def stage_score(e):
    note = (e.get("note") or "").lower()
    # 让 "to appear" > "submitted" > 具体年份
    if "to appear" in note or "in press" in note:
        return 9998
    if "submitted" in note:
        return 9997
    y = e.get("year")
    try:
        return int(y)
    except:
        return 0

def classify(e):
    t = (e.get("ENTRYTYPE") or "").lower()
    if t == "inproceedings":
        return "Conference"
    if t == "article" or e.get("journal"):
        return "Journal"
    # 有 arXiv 或标记 preprint 的
    if e.get("eprint") or "arxiv" in (e.get("note","").lower()):
        return "Preprint"
    # 未发表的一般按 Journal 区显示（与你现在页面一致）
    if t == "unpublished":
        return "Journal"
    return "Preprint"

def one_line(e):
    authors = fmt_authors(e.get("author","")).rstrip(".")
    title = (e.get("title","")).strip().rstrip(".")
    venue = venue_of(e)
    link = link_of(e)
    note  = e.get("note","").strip()
    year  = e.get("year","")

    title_md = f"**{title}**"
    if link:
        title_md = f"[{title_md}]({link})"

    bits = [authors + ".", title_md + "."]
    if venue: bits.append(f"*{venue}*")
    if year: bits.append(str(year))
    if note and note.lower() not in {"arxiv preprint"}:
        bits.append(note)  # 显示 submitted / to appear 等

    text = " ".join(b for b in bits if b).strip()
    return f"- 📄 {text}"

def main():
    bib_path = Path("publications.bib")
    out_path = Path("_includes/publications.md")
    db = bibtexparser.loads(bib_path.read_text(encoding="utf-8"))

    groups = {"Preprint": [], "Journal": [], "Conference": []}
    for e in db.entries:
        groups[classify(e)].append(e)

    for k in groups:
        groups[k].sort(key=lambda e: (stage_score(e), month_num(e)), reverse=True)

    lines = []
    for title in ["Preprint", "Journal", "Conference"]:
        if groups[title]:
            lines.append(f"### {title}\n")
            lines += [one_line(e) for e in groups[title]]
            lines.append("\n---\n")

    out = "\n".join(lines).rstrip() + "\n"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(out, encoding="utf-8")

if __name__ == "__main__":
    main()

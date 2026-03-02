import bibtexparser
import re

BIB_FILE = 'publications.bib'
INDEX_FILE = 'index.md'
TARGET_AUTHOR = "Yuhang Bai"

def format_authors(authors_str):
    if not authors_str: return ""
    authors = [a.strip() for a in authors_str.replace('\n', ' ').split(' and ')]
    formatted = []
    for author in authors:
        if ',' in author:
            parts = author.split(',')
            author = f"{parts[1].strip()} {parts[0].strip()}"
        author = author.replace('{', '').replace('}', '')
        if TARGET_AUTHOR.lower() in author.lower():
            formatted.append(f"**{TARGET_AUTHOR}**")
        else:
            formatted.append(author)
    return ", ".join(formatted)

def determine_category(entry):
    entry_type = entry.get('ENTRYTYPE', '').lower()
    journal = entry.get('journal', '').lower()
    if 'arxiv' in journal or entry_type == 'unpublished': return 'Preprint'
    elif entry_type == 'article': return 'Journal'
    elif entry_type in ['inproceedings', 'conference']: return 'Conference'
    return 'Preprint'

def generate_markdown(entries):
    categories = {'Preprint': [], 'Journal': [], 'Conference': []}
    for entry in entries:
        cat = determine_category(entry)
        if cat in categories:
            categories[cat].append(entry)
    
    # 按年份降序排序
    for cat in categories:
        categories[cat].sort(key=lambda x: x.get('year', '0'), reverse=True)

    md_lines = ["\n## List of papers\n"]
    for cat_name, cat_entries in categories.items():
        if not cat_entries: continue
        md_lines.append(f"### {cat_name}\n")
        for idx, entry in enumerate(cat_entries, 1):
            authors = format_authors(entry.get('author', ''))
            title = entry.get('title', '').replace('{', '').replace('}', '')
            url = entry.get('url', '')
            
            if cat_name == 'Conference':
                venue = f"In *{entry.get('booktitle', 'Conference')}*"
            else:
                venue = f"*{entry.get('journal', 'Journal')}*"
                
            vol, pages = entry.get('volume', ''), entry.get('pages', '')
            if vol and pages: venue += f", {vol}, {pages}"

            if url:
                line = f"{idx}. {authors}. [{title}]({url}). {venue}."
            else:
                line = f"{idx}. {authors}. {title}. {venue}. *Submitted*."
            md_lines.append(line)
            
            abstract = entry.get('abstract', '')
            if abstract:
                md_lines.extend(["   <details>", "       <summary>Abstract</summary>", "       <blockquote>", f"       {abstract}", "       </blockquote>", "       </details>"])
        md_lines.append("\n")
    return "\n".join(md_lines)

def main():
    try:
        with open(BIB_FILE, 'r', encoding='utf-8') as f:
            bib_db = bibtexparser.load(f)
    except FileNotFoundError:
        print(f"File {BIB_FILE} not found.")
        return
        
    new_pubs_md = generate_markdown(bib_db.entries)
    
    with open(INDEX_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # 替换标志位之间的内容
    pattern = re.compile(r'(<!-- PUBS_START -->).*?(<!-- PUBS_END -->)', re.DOTALL)
    if pattern.search(content):
        # 转义反斜杠，确保正确注入
        new_content = pattern.sub(r'\g<1>\n' + new_pubs_md.replace('\\', '\\\\') + r'\n\g<2>', content)
        with open(INDEX_FILE, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("Successfully updated index.md")
    else:
        print("Markers <!-- PUBS_START --> and <!-- PUBS_END --> not found in index.md")

if __name__ == "__main__":
    main()

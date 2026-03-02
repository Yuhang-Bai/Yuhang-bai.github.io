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
    note = entry.get('note', '').lower()
    
    if entry_type == 'unpublished' or 'arxiv' in journal or 'arxiv' in note:
        return 'Preprint'
    elif entry_type == 'article':
        return 'Journal'
    elif entry_type in ['inproceedings', 'conference']:
        return 'Conference'
    return 'Preprint'

def get_year(entry):
    if 'year' in entry:
        return str(entry['year'])
    match = re.search(r'\d{4}', entry.get('ID', ''))
    if match:
        return match.group(0)
    return '0'

def generate_markdown(entries):
    categories = {'Preprint': [], 'Journal': [], 'Conference': []}
    for entry in entries:
        cat = determine_category(entry)
        if cat in categories:
            categories[cat].append(entry)

    for cat in categories:
        categories[cat].sort(key=get_year, reverse=True)

    md_lines = ["\n## List of papers\n"]
    for cat_name, cat_entries in categories.items():
        if not cat_entries: continue
        md_lines.append(f"### {cat_name}\n")
        
        for idx, entry in enumerate(cat_entries, 1):
            authors = format_authors(entry.get('author', ''))
            title = entry.get('title', '').replace('{', '').replace('}', '')
            url = entry.get('url', '')
            
            title_md = f"[{title}]({url})" if url else title
            
            venue_parts = []
            if cat_name == 'Conference' and 'booktitle' in entry:
                venue_parts.append(f"In *{entry.get('booktitle')}*")
            elif 'journal' in entry:
                venue_parts.append(f"*{entry.get('journal')}*")
            elif 'note' in entry and 'arXiv' in entry.get('note', ''):
                venue_parts.append(f"*{entry.get('note')}*")
                
            vol_info = ""
            if 'volume' in entry:
                vol_info += entry.get('volume')
                if 'number' in entry:
                    vol_info += f" ({entry.get('number')})"
            if 'pages' in entry:
                if vol_info:
                    vol_info += f", {entry.get('pages')}"
                else:
                    vol_info = entry.get('pages')
                    
            if vol_info:
                venue_parts.append(vol_info)
                
            venue_str = ", ".join(venue_parts)
            if entry.get('note', '').lower() == 'submitted':
                if venue_str:
                    line = f"{idx}. {authors}. {title_md}. {venue_str}. *Submitted*."
                else:
                    line = f"{idx}. {authors}. {title_md}. *Submitted*."
            else:
                line = f"{idx}. {authors}. {title_md}. {venue_str}."
                
            line = line.replace('..', '.')
            md_lines.append(line)
            
            abstract = entry.get('abstract', '')
            if abstract:
                md_lines.extend([
                    "   <details>",
                    "       <summary>Abstract</summary>",
                    "       <blockquote>",
                    f"       {abstract}",
                    "       </blockquote>",
                    "       </details>"
                ])
                
    return "\n".join(md_lines)

def main():
    try:
        with open(BIB_FILE, 'r', encoding='utf-8') as f:
            bib_db = bibtexparser.load(f)
    except FileNotFoundError:
        print(f"Error: {BIB_FILE} not found.")
        return
        
    new_md = generate_markdown(bib_db.entries)
    
    try:
        with open(INDEX_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
            
        pattern = re.compile(r'(<!-- PUBS_START -->).*?(<!-- PUBS_END -->)', re.DOTALL)
        if pattern.search(content):
            new_content = pattern.sub(r'\g<1>\n' + new_md.replace('\\', '\\\\') + r'\n\g<2>', content)
            with open(INDEX_FILE, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print("Successfully updated index.md")
        else:
            print("Markers <!-- PUBS_START --> and <!-- PUBS_END --> not found in index.md")
    except FileNotFoundError:
        print(f"Error: {INDEX_FILE} not found.")

if __name__ == "__main__":
    main()

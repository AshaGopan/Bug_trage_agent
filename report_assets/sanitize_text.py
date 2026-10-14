import os

path = os.path.join(os.path.dirname(__file__), 'generate_exact_65.py')
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

replacements = {
    '–': '-',
    '—': ' - ',
    '“': '"',
    '”': '"',
    '‘': "'",
    '’': "'",
    '≥': '>=',
    '≤': '<=',
    '→': '->',
    '×': 'x'
}

count = 0
for k, v in replacements.items():
    c = content.count(k)
    if c > 0:
        print(f"'{k}' -> '{v}': {c} occurrences")
        content = content.replace(k, v)
        count += c

if count > 0:
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Replaced {count} non-ASCII symbols with standard ASCII equivalents.')
else:
    print('No replacements needed.')

import csv
import json
import os

# Ensure directories exist
os.makedirs('content/books', exist_ok=True)
os.makedirs('data', exist_ok=True)

# Read CSV
all_books = []
catalog = []
with open('books.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        all_books.append(row)
        if row['Build_Status'] != 'delete':
            catalog.append(row)

# Delete .md files for 'delete' rows
for book in all_books:
    if book['Build_Status'] == 'delete':
        filename = f"content/books/{book['Book_ID']}.md"
        if os.path.exists(filename):
            os.remove(filename)

# First 5 books to bestsellers.json
bestsellers = []
for book in catalog[:5]:
    bestsellers.append({
        'Book_ID': book['Book_ID'],
        'Title': book['Title'],
        'Image_URL': book['Image_URL'],
        'Amazon_Link': book['Amazon_Link']
    })

with open('data/bestsellers.json', 'w') as f:
    json.dump(bestsellers, f, indent=2)

# Process each book
L = len(catalog)
for i, book in enumerate(catalog):
    # Calculate next 4 with wrap-around
    related = []
    for j in range(1, 5):
        idx = (i + j) % L
        related.append({
            'Book_ID': catalog[idx]['Book_ID'],
            'Title': catalog[idx]['Title'],
            'Image_URL': catalog[idx]['Image_URL'],
            'Amazon_Link': catalog[idx]['Amazon_Link']
        })
    
    if book['Build_Status'] == 'on':
        # Prepare front-matter
        front_matter = {
            'title': book['Title'],
            'subtitle': book['Subtitle'],
            'category': book['Category'],
            'image_url': book['Image_URL'],
            'amazon_link': book['Amazon_Link'],
            'ku_eligible': book['KU_Eligible'].upper() == 'TRUE',
            'review_count': int(book['Review_Count']),
            'description_bullets': book['Description_Bullets'].split(';'),
            'related_books': related
        }
        
        # Write Markdown file
        filename = f"content/books/{book['Book_ID']}.md"
        with open(filename, 'w') as f:
            f.write('---\n')
            f.write(json.dumps(front_matter, indent=2))
            f.write('\n---\n\n')
            # Content can be empty or placeholder
            f.write('# ' + book['Title'] + '\n\n')
            f.write('Content here.\n')

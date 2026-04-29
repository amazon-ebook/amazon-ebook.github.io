import csv
import json
import os

# Ensure directories exist
os.makedirs('content/books', exist_ok=True)
os.makedirs('data', exist_ok=True)

# Read books.csv
catalog = []
with open('books.csv', 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        # Filter out rows where Build_Status == "delete" and delete their corresponding .md file
        if row['Build_Status'] == 'delete':
            md_file = f"content/books/{row['Book_ID']}.md"
            if os.path.exists(md_file):
                os.remove(md_file)
            continue
        
        # Keep rows with "on" or "off" in catalog list
        if row['Build_Status'] in ['on', 'off']:
            catalog.append(row)

# Take the first 5 books from catalog and save to bestsellers.json
bestsellers = []
for book in catalog[:5]:
    bestsellers.append({
        'Book_ID': book['Book_ID'],
        'Title': book['Title'],
        'Image_URL': book['Image_URL'],
        'Amazon_Link': book['Amazon_Link']
    })

with open('data/bestsellers.json', 'w', encoding='utf-8') as f:
    json.dump(bestsellers, f, indent=2, ensure_ascii=False)

# Loop through catalog with index i
L = len(catalog)
for i, book in enumerate(catalog):
    # Calculate the next 4 books using modulo wrap-around
    related_books = []
    for j in range(1, 5):
        related_index = (i + j) % L
        related_book = catalog[related_index]
        related_books.append({
            'Book_ID': related_book['Book_ID'],
            'Title': related_book['Title'],
            'Image_URL': related_book['Image_URL'],
            'Amazon_Link': related_book['Amazon_Link']
        })
    
    # If Build_Status == "on", create/overwrite markdown file
    if book['Build_Status'] == 'on':
        # Split Description_Bullets by ';' into array
        description_bullets = [bullet.strip() for bullet in book['Description_Bullets'].split(';')]
        
        # Create YAML front-matter
        frontmatter = f"""---
title: "{book['Title']}"
subtitle: "{book['Subtitle']}"
category: "{book['Category']}"
image_url: "{book['Image_URL']}"
amazon_link: "{book['Amazon_Link']}"
ku_eligible: "{book['KU_Eligible']}"
review_count: {book['Review_Count']}
description_bullets:
{chr(10).join(f'  - "{bullet}"' for bullet in description_bullets)}
related_books:
{chr(10).join(f'  - Book_ID: "{rb["Book_ID"]}"' + chr(10) + f'    Title: "{rb["Title"]}"' + chr(10) + f'    Image_URL: "{rb["Image_URL"]}"' + chr(10) + f'    Amazon_Link: "{rb["Amazon_Link"]}"' for rb in related_books)}
date: 2024-01-01T00:00:00Z
draft: false
---

# {book['Title']}

{book['Subtitle']}

## Description

"""
        
        # Add description bullets as unordered list
        for bullet in description_bullets:
            frontmatter += f"- {bullet}\n"
        
        # Write the markdown file
        filename = f"content/books/{book['Book_ID']}.md"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(frontmatter)

print("Build complete!")

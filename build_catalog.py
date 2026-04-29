#!/usr/bin/env python3
"""
Amazon KDP Book Catalog Builder
Reads books.csv and generates Hugo markdown files with cross-selling logic
"""

import csv
import json
import os
import sys
from pathlib import Path

def sanitize_string(text):
    """Sanitize text for YAML frontmatter"""
    if not text:
        return ""
    return text.replace('"', '\\"').replace("'", "\\'")

def read_books_csv():
    """Read and filter books from CSV"""
    books = []
    csv_path = Path("books.csv")
    
    if not csv_path.exists():
        print(f"ERROR: books.csv not found at {csv_path}")
        sys.exit(1)
    
    with open(csv_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Skip rows marked for deletion
            if row.get('Build_Status', '').lower() == 'delete':
                # Delete existing markdown file if it exists
                book_id = row.get('Book_ID', '').strip()
                if book_id:
                    md_file = Path(f"content/books/{book_id}.md")
                    if md_file.exists():
                        md_file.unlink()
                        print(f"Deleted: {md_file}")
                continue
            
            # Keep rows with 'on' or 'off' status
            if row.get('Build_Status', '').lower() in ['on', 'off']:
                books.append(row)
    
    return books

def create_bestsellers_json(books):
    """Create bestsellers.json with first 5 books"""
    bestsellers = []
    for book in books[:5]:  # Take first 5 books
        bestsellers.append({
            'title': book.get('Title', '').strip(),
            'image_url': book.get('Image_URL', '').strip(),
            'amazon_link': book.get('Amazon_Link', '').strip(),
            'book_id': book.get('Book_ID', '').strip()
        })
    
    # Ensure data directory exists
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    # Write bestsellers.json
    bestsellers_file = data_dir / "bestsellers.json"
    with open(bestsellers_file, 'w', encoding='utf-8') as f:
        json.dump(bestsellers, f, indent=2, ensure_ascii=False)
    
    print(f"Created: {bestsellers_file} with {len(bestsellers)} bestsellers")

def get_related_books(books, current_index):
    """Get 4 related books using N+4 modulo wrap-around logic"""
    related = []
    n = len(books)
    
    for i in range(1, 5):  # Get next 4 books
        related_index = (current_index + i) % n  # Modulo wrap-around
        book = books[related_index]
        related.append({
            'title': book.get('Title', '').strip(),
            'image_url': book.get('Image_URL', '').strip(),
            'amazon_link': book.get('Amazon_Link', '').strip(),
            'book_id': book.get('Book_ID', '').strip()
        })
    
    return related

def generate_hugo_file(book, related_books):
    """Generate Hugo markdown file for a book"""
    # Validate required fields
    required_fields = ['Book_ID', 'Title', 'Image_URL', 'Amazon_Link']
    for field in required_fields:
        if not book.get(field, '').strip():
            print(f"WARNING: Skipping {book.get('Book_ID', 'unknown')} - missing {field}")
            return None
    
    # Parse description bullets
    description_bullets = []
    if book.get('Description_Bullets', '').strip():
        description_bullets = [bullet.strip() for bullet in book.get('Description_Bullets', '').split(';') if bullet.strip()]
    
    # Create frontmatter
    frontmatter = f"""---
title: "{sanitize_string(book.get('Title', ''))}"
subtitle: "{sanitize_string(book.get('Subtitle', ''))}"
category: "{sanitize_string(book.get('Category', ''))}"
image_url: "{sanitize_string(book.get('Image_URL', ''))}"
amazon_link: "{sanitize_string(book.get('Amazon_Link', ''))}"
ku_eligible: "{book.get('KU_Eligible', 'FALSE').upper()}"
review_count: {int(book.get('Review_Count', '0') or '0')}
description_bullets:
{chr(10).join(f'  - "{sanitize_string(bullet)}"' for bullet in description_bullets)}
related_books:
{chr(10).join(f'  - title: "{sanitize_string(rb["title"])}"' + chr(10) + f'    image_url: "{sanitize_string(rb["image_url"])}"' + chr(10) + f'    amazon_link: "{sanitize_string(rb["amazon_link"])}"' + chr(10) + f'    book_id: "{sanitize_string(rb["book_id"])}"' for rb in related_books)}
date: 2024-01-01T00:00:00Z
draft: false
---

# {sanitize_string(book.get('Title', ''))}

{sanitize_string(book.get('Subtitle', ''))}

## Description

"""
    
    # Add description bullets as content
    if description_bullets:
        frontmatter += "\n".join(f"- {bullet}" for bullet in description_bullets)
    
    return frontmatter

def build_catalog():
    """Main build function"""
    print("Building Amazon KDP Book Catalog...")
    
    # Ensure content/books directory exists
    content_dir = Path("content/books")
    content_dir.mkdir(parents=True, exist_ok=True)
    
    # Read and filter books
    books = read_books_csv()
    print(f"Found {len(books)} active books")
    
    if not books:
        print("No active books found in CSV")
        return
    
    # Create bestsellers JSON
    create_bestsellers_json(books)
    
    # Generate Hugo files for books with Build_Status = "on"
    generated_count = 0
    for index, book in enumerate(books):
        if book.get('Build_Status', '').lower() == 'on':
            # Get related books using modulo wrap-around
            related_books = get_related_books(books, index)
            
            # Generate Hugo file
            content = generate_hugo_file(book, related_books)
            if content:
                book_id = book.get('Book_ID', '').strip()
                file_path = content_dir / f"{book_id}.md"
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print(f"Generated: {file_path}")
                generated_count += 1
        else:
            print(f"Skipped: {book.get('Book_ID', '')} (Build_Status: {book.get('Build_Status', '')})")
    
    print(f"Build complete! Generated {generated_count} book files.")

if __name__ == "__main__":
    build_catalog()

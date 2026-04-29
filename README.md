# Amazon KDP Book Catalog System

A fully automated Hugo-based static site for showcasing Amazon KDP books, driven entirely by a CSV file and Python automation.

## Features

- **CSV-Driven**: All book data managed through a single `books.csv` file
- **Automated Build**: Python script generates Hugo files with cross-selling logic
- **Amazon Branding**: Custom UI with Amazon's color scheme and high-conversion design
- **Sticky Buy Buttons**: Mobile-friendly sticky purchase buttons
- **Cross-Selling**: Intelligent N+4 modulo wrap-around for related books
- **Responsive Design**: Works perfectly on desktop and mobile
- **Kindle Unlimited Support**: Conditional KU badges and buttons

## Quick Start

1. **Install Dependencies**:
   ```bash
   # Install Python (if not already installed)
   # Install Hugo (https://gohugo.io/getting-started/installing/)
   ```

2. **Run the Build Script**:
   ```bash
   python build_catalog.py
   ```

3. **Start Hugo Server**:
   ```bash
   hugo server
   ```

4. **Visit Your Site**:
   Open `http://localhost:1313` in your browser

## File Structure

```
amazon-ebook/
├── books.csv              # Master book data file
├── build_catalog.py       # Python automation script
├── config.toml           # Hugo configuration
├── content/
│   └── books/            # Generated book pages
├── data/
│   └── bestsellers.json  # Generated bestsellers data
├── layouts/
│   ├── index.html        # Homepage layout
│   └── books/
│       └── single.html   # Individual book page layout
├── static/
│   ├── css/
│   │   └── style.css     # Custom styling
│   └── js/
│       └── main.js       # JavaScript functionality
└── README.md
```

## CSV Format

The `books.csv` file must contain these exact headers:

| Header | Description | Example |
|--------|-------------|---------|
| Book_ID | Unique identifier | `book001` |
| Title | Book title | `Python Mastery` |
| Subtitle | Book subtitle | `Become a Python Expert` |
| Category | Book category | `Programming` |
| Image_URL | Cover image URL | `https://picsum.photos/seed/python101/400/600.jpg` |
| Amazon_Link | Amazon purchase URL | `https://amazon.com/dp/B001` |
| KU_Eligible | Kindle Unlimited eligible | `TRUE` or `FALSE` |
| Review_Count | Number of reviews | `245` |
| Description_Bullets | Semicolon-separated features | `Learn fast; No stress; Save money` |
| Build_Status | Build status | `on`, `off`, or `delete` |

## Build Status Values

- **`on`**: Generate/update the Hugo page for this book
- **`off`**: Keep in memory for cross-selling but don't generate a page
- **`delete`**: Remove from memory and delete existing Hugo page

## Cross-Selling Logic

The system uses N+4 modulo wrap-around logic:
- Each book shows the next 4 books as "Readers also bought"
- When reaching the end of the list, it wraps around to the beginning
- Example: Book 10 shows Books 1, 2, 3, 4 as related

## Customization

### Colors
Edit `static/css/style.css` to modify:
- `--amazon-orange`: Amazon buy button color (`#FF9900`)
- `--ku-dark`: Kindle Unlimited button color (`#232F3E`)
- `--bg-color`: Background color (`#FFFFFF`)
- `--section-bg`: Section background (`#F8F9FA`)

### Typography
The site uses Google Fonts 'Inter'. You can modify this in the HTML layouts.

### Layouts
- Homepage: `layouts/index.html`
- Book pages: `layouts/books/single.html`

## Deployment

### Build for Production
```bash
hugo --minify
```

The static site will be generated in the `public/` directory, ready for deployment to any static hosting service.

## Automation Features

### Python Script (`build_catalog.py`)
- Reads and filters `books.csv`
- Generates `data/bestsellers.json` (first 5 books)
- Creates individual book pages with cross-selling data
- Handles file deletions when `Build_Status` = `delete`
- Validates required fields before generating pages

### JavaScript Features
- Sticky buy button that appears on scroll
- Smooth scrolling for anchor links
- Dynamic bestsellers loading
- Image loading states
- Keyboard navigation support

## Browser Support

- Chrome/Chromium 80+
- Firefox 75+
- Safari 13+
- Edge 80+

## Performance

- Optimized CSS with custom properties
- Debounced scroll events
- Lazy image loading
- Minimal JavaScript footprint
- Static site generation for maximum speed

## License

This project is open source and available under the [MIT License](LICENSE).

## Support

For issues and questions, please check the documentation or create an issue in the project repository.

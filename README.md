# Python Static Site Generator

This project is a simple static site generator written in Python. It converts Markdown content into HTML pages using customizable templates and supports static assets like images and CSS.

## Features
- Converts Markdown files to HTML
- Supports nested directories for content (e.g., blog posts, contact pages)
- Uses HTML templates for consistent page structure
- Copies static assets (CSS, images) to the output directory
- Easily extensible for new content types or templates

## Project Structure
```
content/         # Markdown source files (site content)
docs/            # Output directory for generated HTML and assets
src/             # Python source code for the generator
static/          # Static assets (CSS, images)
template.html    # HTML template for all pages
build.sh         # Script to build the site
main.sh          # Main entry point script
```

## Getting Started

### Prerequisites
- Python 3.7+

### Installation
1. Clone the repository:
   ```bash
   git clone <repo-url>
   cd Python-Static-Site-Generator
   ```
2. (Optional) Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

### Usage
To build the static site, run:
```bash
./build.sh
```
Or, to run the main script directly:
```bash
./main.sh
```
The generated site will be in the `docs/` directory.

## Testing
To run the tests:
```bash
cd src
python3 -m unittest discover
```

## Customization
- Edit `template.html` to change the site layout.
- Add Markdown files to `content/` to create new pages or blog posts.
- Place images and CSS in `static/` to include them in the site.

## License
MIT License

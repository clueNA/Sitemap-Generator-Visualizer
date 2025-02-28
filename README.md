![Sitemap-Generator-Visualizer](https://socialify.git.ci/clueNA/Sitemap-Generator-Visualizer/image?font=Raleway&language=1&name=1&owner=1&pattern=Transparent&stargazers=1&theme=Dark)
# Sitemap Generator & Visualizer

A Python-based tool that generates XML sitemaps by crawling websites and provides interactive visualization of sitemap structures using Streamlit and Plotly.

## 🌐 Live Demo
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://xmlsgv.streamlit.app/)

## Overview

This tool combines sitemap generation and visualization capabilities to help webmasters and SEO professionals analyze and maintain their website structure.

### Features

- **Sitemap Generation**
  - Automatic website crawling
  - Configurable crawl depth and URL limits
  - Exclusion patterns support
  - Polite crawling with delays
  - XML sitemap generation with priority and change frequency

- **Sitemap Visualization**
  - Interactive network graph visualization
  - Hierarchical structure display
  - URL metadata table
  - Support for both URL input and file upload

## Installation

1. Clone the repository:
```bash
git clone https://github.com/clueNA/Sitemap-Generator-Visualizer
cd sitemap-generator-visualizer
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the application using Streamlit:
```bash
streamlit run app.py
```

### Generate a Sitemap

1. Navigate to the "Generate Sitemap" tab
2. Enter your website URL
3. Configure settings:
   - Maximum URLs to crawl
   - Excluded paths
4. Click "Generate Sitemap"
5. Download the generated XML file

### Visualize a Sitemap

1. Navigate to the "Visualize Sitemap" tab
2. Choose input method:
   - Enter sitemap URL
   - Upload XML file
3. View the interactive visualization and data table

## Project Structure

```
sitemap-generator-visualizer/
├── sitemap_generator.py   # Core sitemap generation logic
├── app.py        # Streamlit web interface
└── requirements.txt      # Project dependencies
```

## Dependencies

- streamlit
- requests
- networkx
- plotly
- pandas
- beautifulsoup4

## Features in Detail

### Sitemap Generator
- Respects robots.txt
- Adds appropriate delays between requests
- Handles both relative and absolute URLs
- Generates standard XML sitemap format
- Configurable crawling parameters

### Visualization Features
- Interactive network graph
- Node connection visualization
- URL hierarchy display
- Sortable data tables
- Multiple input methods

## Best Practices

1. **Respectful Crawling**
   - Use appropriate delays between requests
   - Honor robots.txt directives
   - Set proper user agent string

2. **Resource Management**
   - Set reasonable URL limits
   - Configure excluded paths
   - Monitor server response times

## Contributing

Contributions are welcome! Please feel free to submit pull requests, create issues, or suggest improvements.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Streamlit for the web interface framework
- Plotly for interactive visualizations
- NetworkX for graph generation
- BeautifulSoup4 for HTML parsing

import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from xml.dom import minidom
from datetime import datetime
import time
import hashlib

class SitemapGenerator:
    def __init__(self, base_url, excluded_paths=None, max_urls=5000):
        self.base_url = base_url.rstrip('/')
        self.domain = urlparse(base_url).netloc
        self.urls = set()
        self.crawled = set()
        self.excluded_paths = excluded_paths or []
        self.max_urls = max_urls
        self.session = requests.Session()
        # Set a user agent to be polite
        self.session.headers.update({
            'User-Agent': 'SitemapGenerator/1.0 (https://github.com/yourname/sitemapgenerator)'
        })

    def should_crawl(self, url):
        parsed = urlparse(url)
        if parsed.netloc != self.domain:
            return False
        
        path = parsed.path.lower()
        
        # Skip excluded paths
        for excluded in self.excluded_paths:
            if excluded in path:
                return False
                
        # Skip common non-content files
        if any(path.endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.gif', '.pdf', '.zip']):
            return False
            
        return True

    def crawl_page(self, url):
        if url in self.crawled or len(self.urls) >= self.max_urls:
            return

        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            self.crawled.add(url)
            
            # Add the current URL to our collection
            self.urls.add(url)
            
            # Parse the HTML content
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find all links
            for link in soup.find_all('a', href=True):
                href = link['href']
                absolute_url = urljoin(url, href)
                
                if self.should_crawl(absolute_url):
                    # Remove fragments and query parameters
                    clean_url = absolute_url.split('#')[0].split('?')[0]
                    if clean_url not in self.crawled:
                        self.crawl_page(clean_url)
                        
            # Add a small delay to be polite to the server
            time.sleep(0.1)
            
        except Exception as e:
            print(f"Error crawling {url}: {str(e)}")

    def generate_sitemap(self):
        # Create the root element
        urlset = ET.Element('urlset', xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
        
        # Add each URL to the sitemap
        for page_url in sorted(self.urls):
            url_element = ET.SubElement(urlset, 'url')
            
            # Add loc element (required)
            loc = ET.SubElement(url_element, 'loc')
            loc.text = page_url
            
            # Add lastmod element (optional)
            lastmod = ET.SubElement(url_element, 'lastmod')
            lastmod.text = datetime.utcnow().strftime('%Y-%m-%d')
            
            # Add changefreq element (optional)
            changefreq = ET.SubElement(url_element, 'changefreq')
            if page_url == self.base_url:
                changefreq.text = 'daily'
            else:
                changefreq.text = 'weekly'
            
            # Add priority element (optional)
            priority = ET.SubElement(url_element, 'priority')
            if page_url == self.base_url:
                priority.text = '1.0'
            else:
                # Calculate priority based on URL depth
                depth = len(urlparse(page_url).path.split('/')) - 1
                priority.text = str(max(0.1, 1.0 - (depth * 0.2)))
        
        # Convert to string with pretty printing
        xml_str = minidom.parseString(ET.tostring(urlset)).toprettyxml(indent="  ")
        return xml_str

    def generate(self):
        print(f"Starting crawl of {self.base_url}")
        self.crawl_page(self.base_url)
        return self.generate_sitemap()
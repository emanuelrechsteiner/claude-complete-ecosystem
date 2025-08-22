#!/usr/bin/env python3
"""
Simple Documentation Website Scraper
Crawls documentation websites and converts pages to markdown files.
"""

import asyncio
import os
import re
import json
from datetime import datetime
from urllib.parse import urljoin, urlparse
from typing import Set, List, Dict, Optional
import logging
from pathlib import Path

from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode
from bs4 import BeautifulSoup

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DocumentationScraper:
    """Scrapes documentation websites and saves content as markdown files."""
    
    def __init__(self, output_dir: str = "scraped_docs"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.visited_urls: Set[str] = set()
        self.failed_urls: Set[str] = set()
        self.domain = None
        
    def _is_valid_doc_url(self, url: str) -> bool:
        """Check if URL is a valid documentation page."""
        if not url or not self.domain:
            return False
            
        parsed = urlparse(url)
        
        # Must be same domain
        if parsed.netloc != self.domain:
            return False
            
        # Skip non-documentation URLs
        skip_patterns = [
            r'/api/', r'/login', r'/signup', r'/auth/', 
            r'\.pdf$', r'\.zip$', r'\.tar\.gz$',
            r'#', r'mailto:', r'javascript:', 
            r'/download/', r'/releases/download/'
        ]
        
        for pattern in skip_patterns:
            if re.search(pattern, url.lower()):
                return False
                
        return True
    
    def _clean_filename(self, url: str) -> str:
        """Convert URL to a safe filename."""
        parsed = urlparse(url)
        path = parsed.path.strip('/')
        
        if not path:
            path = "index"
            
        # Replace special characters
        filename = re.sub(r'[^\w\-_\.]', '_', path)
        filename = re.sub(r'_+', '_', filename)
        
        if not filename.endswith('.md'):
            filename += '.md'
            
        return filename
    
    def _extract_internal_links(self, html: str, base_url: str) -> List[str]:
        """Extract all internal documentation links from HTML."""
        soup = BeautifulSoup(html, 'html.parser')
        links = set()
        
        for tag in soup.find_all(['a', 'link']):
            href = tag.get('href')
            if href:
                absolute_url = urljoin(base_url, href)
                if self._is_valid_doc_url(absolute_url):
                    # Remove fragments and normalize
                    parsed = urlparse(absolute_url)
                    clean_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
                    if parsed.query:
                        clean_url += f"?{parsed.query}"
                    links.add(clean_url)
                    
        return list(links)
    
    def _save_content(self, url: str, content: str, metadata: Dict) -> str:
        """Save content to markdown file."""
        filename = self._clean_filename(url)
        filepath = self.output_dir / filename
        
        # Create subdirectories if needed
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        # Add metadata header
        markdown_content = f"""---
url: {url}
scraped_at: {metadata.get('scraped_at', datetime.now().isoformat())}
title: {metadata.get('title', 'Untitled')}
---

{content}
"""
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
            
        return str(filepath)
    
    async def scrape_page(self, crawler, url: str) -> Optional[Dict]:
        """Scrape a single page and extract links."""
        try:
            # Add delay to avoid rate limiting
            await asyncio.sleep(2)
            
            config = CrawlerRunConfig(
                cache_mode=CacheMode.BYPASS,
                wait_for="article, main, .content, .documentation, body",
                delay_before_return_html=1.0,
            )
            
            result = await crawler.arun(url, config=config)
            
            if not result.success:
                logger.error(f"Failed to crawl {url}: {result.error_message if hasattr(result, 'error_message') else 'Unknown error'}")
                self.failed_urls.add(url)
                return None
                
            # Extract internal links for further crawling
            html_content = result.html if hasattr(result, 'html') else ""
            internal_links = self._extract_internal_links(html_content, url) if html_content else []
            
            # Get page title
            soup = BeautifulSoup(html_content, 'html.parser') if html_content else None
            title = soup.find('title') if soup else None
            title_text = title.text.strip() if title else "Untitled"
            
            # Use markdown content if available
            content = result.markdown if hasattr(result, 'markdown') else result.text if hasattr(result, 'text') else ""
            
            if not content:
                logger.warning(f"No content extracted from {url}")
                return None
            
            # Save the content
            metadata = {
                'scraped_at': datetime.now().isoformat(),
                'title': title_text,
                'links_found': len(internal_links)
            }
            
            filepath = self._save_content(url, content, metadata)
            
            logger.info(f"Saved {url} -> {filepath} (found {len(internal_links)} links)")
            
            return {
                'url': url,
                'links': internal_links,
                'filepath': filepath
            }
            
        except Exception as e:
            logger.error(f"Error scraping {url}: {str(e)}")
            self.failed_urls.add(url)
            return None
    
    async def scrape_documentation(self, start_url: str, max_pages: int = 1000):
        """Scrape entire documentation website starting from a URL."""
        # Parse domain
        parsed = urlparse(start_url)
        self.domain = parsed.netloc
        
        logger.info(f"Starting documentation scrape for domain: {self.domain}")
        logger.info(f"Output directory: {self.output_dir}")
        
        # URLs to process
        urls_to_crawl = {start_url}
        self.visited_urls = set()
        
        async with AsyncWebCrawler(verbose=False) as crawler:
            while urls_to_crawl and len(self.visited_urls) < max_pages:
                # Get next batch of URLs (process one at a time for simplicity)
                url = urls_to_crawl.pop()
                
                if url in self.visited_urls:
                    continue
                    
                logger.info(f"Scraping page {len(self.visited_urls) + 1}/{max_pages}: {url}")
                
                # Scrape the page
                result = await self.scrape_page(crawler, url)
                
                if result:
                    self.visited_urls.add(result['url'])
                    
                    # Add new links to queue
                    for link in result['links']:
                        if link not in self.visited_urls and link not in self.failed_urls:
                            urls_to_crawl.add(link)
                
                # Progress update
                if len(self.visited_urls) % 10 == 0:
                    logger.info(f"Progress: {len(self.visited_urls)} pages scraped, "
                              f"{len(urls_to_crawl)} in queue, "
                              f"{len(self.failed_urls)} failed")
        
        # Save crawl summary
        summary = {
            'start_url': start_url,
            'domain': self.domain,
            'total_pages_scraped': len(self.visited_urls),
            'failed_urls': list(self.failed_urls),
            'visited_urls': list(self.visited_urls),
            'scrape_completed_at': datetime.now().isoformat()
        }
        
        summary_path = self.output_dir / '_scrape_summary.json'
        with open(summary_path, 'w') as f:
            json.dump(summary, f, indent=2)
            
        logger.info(f"\nScraping completed!")
        logger.info(f"Total pages scraped: {len(self.visited_urls)}")
        logger.info(f"Failed URLs: {len(self.failed_urls)}")
        logger.info(f"Summary saved to: {summary_path}")


async def main():
    """Main entry point."""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python SimpleDocScraper.py <documentation_url> [output_dir] [max_pages]")
        print("\nExample:")
        print("  python SimpleDocScraper.py https://docs.anthropic.com")
        print("  python SimpleDocScraper.py https://docs.anthropic.com anthropic_docs 500")
        sys.exit(1)
    
    start_url = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "scraped_docs"
    max_pages = int(sys.argv[3]) if len(sys.argv) > 3 else 1000
    
    scraper = DocumentationScraper(output_dir)
    await scraper.scrape_documentation(start_url, max_pages)


if __name__ == "__main__":
    asyncio.run(main())
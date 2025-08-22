#!/usr/bin/env python3
"""
Documentation Website Scraper
Crawls entire documentation websites and converts pages to markdown files.
"""

import asyncio
import os
import re
import json
from datetime import datetime
from urllib.parse import urljoin, urlparse, unquote
from typing import Set, List, Dict, Optional
import logging
from pathlib import Path

from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode
from crawl4ai import MemoryAdaptiveDispatcher, RateLimiter
from crawl4ai import CrawlerMonitor, DisplayMode
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
        self.should_stop = False
        
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
            config = CrawlerRunConfig(
                cache_mode=CacheMode.BYPASS,
                wait_for="article, main, .content, .documentation, body",
                delay_before_return_html=2.0,
            )
            
            result = await crawler.arun(url, config=config)
            
            if not result.success:
                logger.error(f"Failed to crawl {url}: {result.error}")
                self.failed_urls.add(url)
                return None
                
            # Extract internal links for further crawling
            internal_links = self._extract_internal_links(result.cleaned_html or result.html, url)
            
            # Get page title
            soup = BeautifulSoup(result.html, 'html.parser')
            title = soup.find('title')
            title_text = title.text.strip() if title else "Untitled"
            
            # Save the content
            metadata = {
                'scraped_at': datetime.now().isoformat(),
                'title': title_text,
                'links_found': len(internal_links)
            }
            
            filepath = self._save_content(url, result.markdown, metadata)
            
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
        
        # Initialize crawler with rate limiting
        rate_limiter = RateLimiter(
            base_delay=(1.0, 2.0),
            max_delay=30.0,
            max_retries=3
        )
        
        # Try to create monitor with fallback
        try:
            monitor = CrawlerMonitor(
                display_mode=DisplayMode.DETAILED
            )
            
            dispatcher = MemoryAdaptiveDispatcher(
                rate_limiter=rate_limiter,
                monitor=monitor,
                max_session_permit=5,  # Concurrent crawls
                memory_threshold_percent=80.0
            )
        except TypeError:
            # Fallback: Create monitor without parameters or no monitor
            try:
                monitor = CrawlerMonitor()
                dispatcher = MemoryAdaptiveDispatcher(
                    rate_limiter=rate_limiter,
                    monitor=monitor,
                    max_session_permit=5,
                    memory_threshold_percent=80.0
                )
            except:
                # No monitor fallback
                dispatcher = MemoryAdaptiveDispatcher(
                    rate_limiter=rate_limiter,
                    max_session_permit=5,
                    memory_threshold_percent=80.0
                )
        
        # URLs to process
        urls_to_crawl = {start_url}
        self.visited_urls = set()
        
        async with AsyncWebCrawler() as crawler:
            while urls_to_crawl and len(self.visited_urls) < max_pages and not self.should_stop:
                # Check for stop condition
                if self.should_stop:
                    logger.info("Scraping stopped by user")
                    break
                    
                # Get next batch of URLs
                batch_size = min(10, len(urls_to_crawl))
                current_batch = set(list(urls_to_crawl)[:batch_size])
                urls_to_crawl -= current_batch
                
                # Filter out already visited
                current_batch = {url for url in current_batch if url not in self.visited_urls}
                
                if not current_batch:
                    continue
                    
                logger.info(f"Processing batch of {len(current_batch)} URLs...")
                
                # Scrape pages in parallel
                tasks = [self.scrape_page(crawler, url) for url in current_batch]
                
                # Process tasks with early termination support
                try:
                    results = await asyncio.gather(*tasks)
                except asyncio.CancelledError:
                    logger.info("Batch processing cancelled")
                    break
                
                # Process results
                for result in results:
                    if result and not self.should_stop:
                        self.visited_urls.add(result['url'])
                        
                        # Add new links to queue only if not stopping
                        if not self.should_stop:
                            for link in result['links']:
                                if link not in self.visited_urls and link not in self.failed_urls:
                                    urls_to_crawl.add(link)
                
                # Check stop condition again
                if self.should_stop:
                    logger.info("Scraping stopped by user during result processing")
                    break
                
                # Progress update
                logger.info(f"Progress: {len(self.visited_urls)} pages scraped, "
                          f"{len(urls_to_crawl)} in queue, "
                          f"{len(self.failed_urls)} failed")
                
                # Small delay between batches (with stop check)
                for _ in range(10):  # Check stop every 100ms for 1 second
                    if self.should_stop:
                        break
                    await asyncio.sleep(0.1)
        
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
        print("Usage: python DocScraper.py <documentation_url> [output_dir] [max_pages]")
        print("\nExample:")
        print("  python DocScraper.py https://docs.anthropic.com")
        print("  python DocScraper.py https://docs.anthropic.com anthropic_docs 500")
        sys.exit(1)
    
    start_url = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "scraped_docs"
    max_pages = int(sys.argv[3]) if len(sys.argv) > 3 else 1000
    
    scraper = DocumentationScraper(output_dir)
    await scraper.scrape_documentation(start_url, max_pages)


if __name__ == "__main__":
    asyncio.run(main())
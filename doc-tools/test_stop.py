#!/usr/bin/env python3
"""
Test script to verify the stop functionality works correctly.
"""

import asyncio
from DocScraper import DocumentationScraper

async def test_stop():
    """Test that the scraper can be stopped properly."""
    scraper = DocumentationScraper("test_output")
    
    # Start scraping in a task
    scrape_task = asyncio.create_task(
        scraper.scrape_documentation("https://docs.anthropic.com", max_pages=100)
    )
    
    # Wait a bit, then stop
    await asyncio.sleep(3)
    print("Setting stop flag...")
    scraper.should_stop = True
    
    # Wait for scraping to complete
    try:
        await scrape_task
        print("Scraping completed")
    except Exception as e:
        print(f"Scraping error: {e}")
    
    print(f"Pages scraped: {len(scraper.visited_urls)}")
    print("Stop test completed")

if __name__ == "__main__":
    asyncio.run(test_stop())
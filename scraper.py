import asyncio
from playwright.async_api import async_playwright

class HTMLScraper:
    async def setup_browser(self):
        """Create and configure a browser instance."""
        self.playwright = await async_playwright().start()
        return await self.playwright.chromium.launch(
            headless=True,
            args=['--no-sandbox']
        )

    async def get_page_html(self, url: str) -> str:
        """Fetch and return the HTML content from a URL."""
        browser = await self.setup_browser()
        
        try:
            context = await browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            )
            
            page = await context.new_page()
            await page.goto(url, wait_until='domcontentloaded', timeout=20000)
            
            # Quick scroll to trigger any lazy loading
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await page.wait_for_timeout(1000)
            
            # Get the full HTML content
            html_content = await page.content()
            return html_content
            
        except Exception as e:
            return f"<html><body><p>Error fetching {url}: {str(e)}</p></body></html>"
        finally:
            await browser.close()
            await self.playwright.stop()

async def get_url_html(url: str) -> str:
    """Helper function to get HTML content from a URL."""
    scraper = HTMLScraper()
    return await scraper.get_page_html(url)

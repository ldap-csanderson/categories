from flask import Flask, render_template, request
import asyncio
import os
from scraper import get_url_html
from vertex_client import VertexAIClient

app = Flask(__name__)

def run_async(coro):
    """Helper function to run async code in Flask route."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()

async def process_url(url: str) -> str:
    """Process a URL through scraping and LLM analysis."""
    # First get the HTML content
    html_content = await get_url_html(url)
    
    # Initialize Vertex AI client
    vertex_client = VertexAIClient()
    
    # Get taxonomy CSV
    csv_content = await vertex_client.get_taxonomy(url, html_content)
    return csv_content

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Check for required environment variables
        if not os.getenv("GOOGLE_CLOUD_PROJECT"):
            return "Error: GOOGLE_CLOUD_PROJECT environment variable not set", 500
            
        url = request.form.get('url')
        if url:
            # Set response headers for CSV
            csv_content = run_async(process_url(url))
            response = app.make_response(csv_content)
            response.headers["Content-Type"] = "text/csv"
            response.headers["Content-Disposition"] = f"attachment; filename=taxonomy_{url.replace('/', '_')}.csv"
            return response
            
    return render_template('index.html')

if __name__ == '__main__':
    # Get port from environment variable or default to 8080
    port = int(os.getenv('PORT', '8080'))
    # Run on all interfaces (0.0.0.0) using the specified port
    app.run(host='0.0.0.0', port=port)

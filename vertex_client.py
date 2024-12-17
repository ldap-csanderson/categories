import os
from datetime import datetime
import vertexai
from vertexai.preview.generative_models import GenerativeModel
from google.cloud import aiplatform

class VertexAIClient:
    def __init__(self):
        self.project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
        self.location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
        vertexai.init(project=self.project_id, location=self.location)
        
        # Load the LLM prompt template
        with open("llm_prompt.md", "r") as f:
            self.prompt_template = f.read()
        
    def format_prompt(self, url: str, content: str) -> str:
        """Format the prompt with the webpage content."""
        # The prompt already contains the structure and rules
        # We just need to provide the URL and content as context
        context = f"\nAnalyzing URL: {url}\n\nWebpage Content:\n{content}\n"
        return self.prompt_template + context
        
    async def get_taxonomy(self, url: str, content: str) -> str:
        """Send content to Vertex AI and get taxonomy CSV."""
        try:
            # Format the prompt with webpage content
            formatted_prompt = self.format_prompt(url, content)
            
            # Initialize the model
            model = GenerativeModel("gemini-1.5-pro")
            
            # Generate response
            response = model.generate_content(
                formatted_prompt,
                generation_config={
                    "temperature": 0.2,  # Lower temperature for more consistent output
                    "max_output_tokens": 8192,  # Allow for longer response
                }
            )
            
            # Remove any code fence markdown indicators from the response
            response_text = response.text.strip()
            if response_text.startswith("```csv") and response_text.endswith("```"):
                response_text = response_text[6:-3].strip()
            elif response_text.startswith("```") and response_text.endswith("```"):
                response_text = response_text[3:-3].strip()
            
            return response_text
            
        except Exception as e:
            # Return a CSV with error information
            error_csv = f'"taxonomy","seasonal","confidence","source_url","date_scraped","reasoning"\n'
            error_csv += f'"<error>",FALSE,weak,"{url}","{datetime.now().strftime("%Y-%m-%d")}","Error processing content: {str(e)}"'
            return error_csv

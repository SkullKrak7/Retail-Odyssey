import os

from google import genai
from typing import Optional
import argparse

class VirtualTryOnAPI:
    """Integration with Google AI Studio (Gemini/Imagen)"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Google AI client
        
        Args:
            api_key: Google API key (optional, defaults to env var)
        """
        self.client = genai.Client()

    def try_on_inference_api(self, description: str, output_path: str = "model.png") -> Optional[str]:
        """
        Generate image using Google Imagen model
        
        Args:
            description: Prompt for virtual try-on
            output_path: Path to save the generated image
            
        Returns:
            Path to output image or None if failed
        """
        try:
            prompt = description

            response = self.client.models.generate_content(
                model="gemini-2.5-flash-image",
                contents=[prompt],
            )

            for part in response.parts:
                if part.text is not None:
                    print(part.text)
                elif part.inline_data is not None:
                    image = part.as_image()
                    image.save("generated_image.png")
                
        except Exception as e:
            print(f"Error in virtual try-on: {e}")
            # Fallback or detailed error message
            print("Ensure you have access to Imagen models in Google AI Studio.")
            return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Virtual Try-On using FLUX")
    parser.add_argument("--description", type=str, required=True, help="Description of the clothes/scene")
    parser.add_argument("--output", type=str, default="model.png", help="Path to save the generated image")
    
    args = parser.parse_args()
    
    api = VirtualTryOnAPI()
    api.try_on_inference_api(args.description, args.output)
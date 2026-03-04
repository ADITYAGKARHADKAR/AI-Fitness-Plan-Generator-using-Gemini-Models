import google.generativeai as genai
from dotenv import load_dotenv
import os
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

def test_gemini_connection():
    """Test if Gemini API key and model are working correctly."""
    
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        logger.error("❌ GEMINI_API_KEY not found in .env file!")
        return False
    
    try:
        # Configure Gemini
        genai.configure(api_key=api_key)
        
        # Load gemini-1.5-flash model
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        logger.info("🔄 Sending test request to Gemini...")
        
        response = model.generate_content(
            "Give me one short fitness tip for weight loss in one sentence."
        )
        
        print("\n✅ Gemini API connected successfully!")
        print(f"📌 Model used: gemini-1.5-flash")
        print(f"💡 Test Response: {response.text}\n")
        return True
        
    except Exception as e:
        logger.error(f"❌ Connection failed: {str(e)}")
        return False

if __name__ == "__main__":
    test_gemini_connection()
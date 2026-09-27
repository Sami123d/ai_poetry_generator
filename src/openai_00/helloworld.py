import google.generativeai as genai
from dotenv import load_dotenv
import os

print("🚀 Starting helloworld.py with Gemini API...")

# Load environment variables
load_dotenv()
print("✅ Environment variables loaded")

# Get Gemini API key from environment
gemini_api_key = os.environ.get("GEMINI_API_KEY")
print(f"🔑 Gemini API Key found: {'Yes' if gemini_api_key else 'No'}")

if not gemini_api_key:
    print("🚨 GEMINI_API_KEY not found!")
    print("\nTo use this script, you need to:")
    print("1. Get an API key from https://makersuite.google.com/app/apikey")
    print("2. Set it as an environment variable:")
    print("   - Windows (PowerShell): $env:GEMINI_API_KEY='your-api-key-here'")
    print("   - Windows (CMD): set GEMINI_API_KEY=your-api-key-here")
    print("   - Linux/Mac: export GEMINI_API_KEY='your-api-key-here'")
    print("3. Or create a .env file in the project root with:")
    print("   GEMINI_API_KEY=your-api-key-here")
    print("\nDemo mode - showing what the script would do:")
    print("🤖 AI Response:")
    print("Code calls itself,\nFunctions within functions,\nEndless loops of thought.")
    print("✅ Demo completed successfully!")
else:
    print("✅ Gemini API key found!")
    print("🤖 Making API call to Google Gemini...")

    # Configure Gemini API
    genai.configure(api_key=gemini_api_key)

    try:
        # Create a Gemini model instance
        model = genai.GenerativeModel(os.environ.get('GEMINI_MODEL', 'gemini-2.5-flash'))
        
        # Generate content
        prompt = "Write a pakitani poetry roman urdu about recursion in artificial intelligence."
        response = model.generate_content(prompt)
        
        # Print the response
        print("🤖 Gemini AI Response:")
        print(response.text)
        
    except Exception as e:
        print(f"❌ Error occurred: {e}")
        print("Make sure your Gemini API key is valid and you have sufficient credits.")

print("🏁 Script execution completed!")
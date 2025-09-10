from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os
from dotenv import load_dotenv

app = Flask(__name__)

# Load environment variables
load_dotenv()

def generate_poetry(api_key, poetry_type, custom_topic, language):
    """Generate poetry using Gemini AI"""
    try:
        # Configure Gemini API
        genai.configure(api_key=api_key)
        
        # Create model
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Create prompt based on type and language
        prompts = {
            'recursion': "Write a Pakistani poetry in Roman Urdu about recursion in programming. Make it creative and educational.",
            'ai': "Write a beautiful Pakistani poetry in Roman Urdu about artificial intelligence and its impact on society.",
            'love': "Write a romantic Pakistani poetry in Roman Urdu about love and relationships.",
            'nature': "Write a nature poetry in Roman Urdu about Pakistan's beautiful landscapes and seasons.",
            'custom': f"Write a creative Pakistani poetry in Roman Urdu about: {custom_topic}"
        }
        
        base_prompt = prompts.get(poetry_type, prompts['custom'])
        
        # Add language instructions
        if language == 'urdu':
            base_prompt += " Include both Urdu text and Roman Urdu translation."
        elif language == 'english':
            base_prompt = base_prompt.replace("Roman Urdu", "English")
        
        # Generate content
        response = model.generate_content(base_prompt)
        
        return {
            'success': True,
            'poetry': response.text
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')

@app.route('/generate-poetry', methods=['POST'])
def generate_poetry_api():
    """API endpoint to generate poetry"""
    try:
        data = request.get_json()
        
        api_key = data.get('apiKey')
        poetry_type = data.get('poetryType', 'recursion')
        custom_topic = data.get('customTopic', '')
        language = data.get('language', 'roman_urdu')
        
        if not api_key:
            return jsonify({
                'success': False,
                'error': 'API key is required'
            })
        
        result = generate_poetry(api_key, poetry_type, custom_topic, language)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        })

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    print("🚀 Starting AI Poetry Generator...")
    print("📱 Open your browser and go to: http://localhost:5000")
    print("🔑 Make sure to set your GEMINI_API_KEY environment variable")
    app.run(debug=True, host='0.0.0.0', port=5000)


import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import time
from streamlit_option_menu import option_menu

# Page configuration
st.set_page_config(
    page_title="🤖 AI Poetry Generator",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load environment variables
load_dotenv()

# Custom CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    
    .poetry-container {
        background: #f8f9fa;
        padding: 2rem;
        border-radius: 15px;
        border-left: 5px solid #667eea;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .poetry-text {
        font-size: 1.1rem;
        line-height: 1.8;
        color: #333;
        white-space: pre-line;
        font-family: 'Georgia', serif;
    }
    
    .success-message {
        background: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #c3e6cb;
        margin: 1rem 0;
    }
    
    .error-message {
        background: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #f5c6cb;
        margin: 1rem 0;
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
</style>
""", unsafe_allow_html=True)

def generate_poetry(api_key, poetry_type, custom_topic, language, style):
    """Generate poetry using Google Gemini"""
    try:
        # Configure Gemini API
        genai.configure(api_key=api_key)
        
        # Create model
        model = genai.GenerativeModel(os.environ.get('GEMINI_MODEL', 'gemini-2.5-flash'))
        
        # Create prompt based on type and language
        prompts = {
            'recursion': f"Write a {style} Pakistani poetry in {language} about recursion in programming. Make it creative, educational, and engaging.",
            'ai': f"Write a {style} Pakistani poetry in {language} about artificial intelligence and its impact on society. Make it thoughtful and inspiring.",
            'love': f"Write a {style} romantic Pakistani poetry in {language} about love and relationships. Make it emotional and beautiful.",
            'nature': f"Write a {style} nature poetry in {language} about Pakistan's beautiful landscapes, seasons, and natural beauty.",
            'philosophy': f"Write a {style} philosophical Pakistani poetry in {language} about life, wisdom, and human nature.",
            'technology': f"Write a {style} Pakistani poetry in {language} about technology, digital life, and how it affects our daily lives. Make it relatable and modern.",
            'education': f"Write a {style} Pakistani poetry in {language} about education, learning, and the importance of knowledge. Make it inspiring and motivational.",
            'social_media': f"Write a {style} Pakistani poetry in {language} about social media, its impact on society, and human connections. Make it thought-provoking and relevant.",
            'climate': f"Write a {style} Pakistani poetry in {language} about climate change, environmental protection, and our responsibility to nature. Make it urgent and meaningful.",
            'family': f"Write a {style} Pakistani poetry in {language} about family bonds, relationships, and the importance of family in Pakistani culture. Make it heartwarming and touching.",
            'custom': f"Write a {style} creative Pakistani poetry in {language} about: {custom_topic}. Make it engaging and meaningful."
        }
        
        base_prompt = prompts.get(poetry_type, prompts['custom'])
        
        # Add specific instructions based on language
        if language == 'English':
            base_prompt += " Use Roman Urdu script (English letters) for Urdu words."
        elif language == 'Arabic':
            base_prompt += " Use Arabic script for Urdu words."
        elif language == 'Urdu':
            base_prompt = base_prompt.replace("Pakistani poetry", "poetry")
        
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

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🤖 AI Poetry Generator</h1>
        <p>Create beautiful Pakistani poetry using Google Gemini</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Auto-load API key from .env file (hidden from UI)
    api_key = os.environ.get('GEMINI_API_KEY')
    
    # Sidebar for settings
    with st.sidebar:
        st.header("⚙️ Settings")
        
        # Poetry type selection
        poetry_type = st.selectbox(
            "📝 Poetry Type",
            ["recursion", "ai", "love", "nature", "philosophy", "technology", "education", "social_media", "climate", "family", "custom"],
            format_func=lambda x: {
                "recursion": "🔄 Recursion in Programming",
                "ai": "🤖 Artificial Intelligence", 
                "love": "💕 Love & Relationships",
                "nature": "🌿 Nature & Landscapes",
                "philosophy": "🧠 Philosophy & Wisdom",
                "technology": "💻 Technology & Digital Life",
                "education": "📚 Education & Learning",
                "social_media": "📱 Social Media Impact",
                "climate": "🌍 Climate Change & Environment",
                "family": "👨‍👩‍👧‍👦 Family & Relationships",
                "custom": "✨ Custom Topic"
            }[x]
        )
        
        # Quick topic selection for common themes
        if poetry_type == "custom":
            st.markdown("**🎯 Quick Topic Selection:**")
            quick_topics = [
                "Technology and humanity",
                "Childhood memories", 
                "Pakistani culture",
                "Dreams and aspirations",
                "Friendship and loyalty",
                "Education and learning",
                "Social media impact",
                "Climate change",
                "Family bonds",
                "Future of AI"
            ]
            
            selected_quick_topic = st.selectbox(
                "Choose a quick topic:",
                ["Type manually..."] + quick_topics,
                help="Select from popular topics or type your own"
            )
            
            if selected_quick_topic != "Type manually...":
                custom_topic = selected_quick_topic
                st.success(f"✅ Selected: {custom_topic}")
            else:
                custom_topic = st.text_input(
                    "🎯 Custom Topic",
                    placeholder="Enter your custom topic...",
                    help="What would you like the poetry to be about?"
                )
        else:
            custom_topic = ""
        
        # Language selection
        language = st.selectbox(
            "🌐 Language",
            ["English", "Arabic", "Urdu"],
            help="Choose the language for your poetry"
        )
        
        # Style selection
        style = st.selectbox(
            "🎨 Style",
            ["traditional", "modern", "romantic", "philosophical", "humorous"],
            help="Choose the style of poetry"
        )
        
       
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("🎨 Generate Poetry")
        
        # Generate button
        if st.button("🚀 Generate Poetry", type="primary", use_container_width=True):
            if not api_key:
                st.error("❌ API key not found! Please check your .env file.")
                st.info("""
                **To fix this:**
                1. Create a `.env` file in project root
                2. Add: `GEMINI_API_KEY=your-api-key-here`
                3. Restart the app
                """)
            elif poetry_type == "custom" and not custom_topic:
                st.error("❌ Please enter a custom topic!")
            else:
                # Show loading
                with st.spinner("🤖 AI is creating beautiful poetry for you..."):
                    result = generate_poetry(api_key, poetry_type, custom_topic, language, style)
                
                if result['success']:
                    st.markdown("""
                    <div class="success-message">
                        ✅ Poetry generated successfully!
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Display poetry
                    st.markdown(f"""
                    <div class="poetry-container">
                        <h3>✨ Generated Poetry:</h3>
                        <div class="poetry-text">{result['poetry']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Add download button
                    st.download_button(
                        label="📥 Download Poetry",
                        data=result['poetry'],
                        file_name=f"ai_poetry_{poetry_type}_{int(time.time())}.txt",
                        mime="text/plain"
                    )
                    
                else:
                    st.markdown(f"""
                    <div class="error-message">
                        ❌ Error: {result['error']}
                    </div>
                    """, unsafe_allow_html=True)
    
    with col2:
        st.header("📚 Examples")
        
        # Example poetry types
        examples = {
            "🔄 Recursion": "Functions calling themselves, creating beautiful patterns in code",
            "🤖 AI": "Artificial intelligence changing the world, one algorithm at a time",
            "💕 Love": "Romantic poetry about relationships and emotions",
            "🌿 Nature": "Beautiful descriptions of Pakistan's landscapes and seasons",
            "🧠 Philosophy": "Deep thoughts about life, wisdom, and human nature"
        }
        
        for title, description in examples.items():
            with st.expander(title):
                st.write(description)
        
        st.markdown("---")
        
        # Quick stats
        st.metric("🎯 Poetry Types", "6")
        st.metric("🌐 Languages", "3")
        st.metric("🎨 Styles", "5")
        
        # Tips
        st.info("💡 **Tip:** Try different combinations of poetry types and styles for unique results!")

if __name__ == "__main__":
    main()

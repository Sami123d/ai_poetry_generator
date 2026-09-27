import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import time
import json
from datetime import datetime
from streamlit_option_menu import option_menu

# Page configuration
st.set_page_config(
    page_title="🤖 AI Poetry Generator Pro",
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
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .poetry-container {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 2rem;
        border-radius: 20px;
        border-left: 5px solid #667eea;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        position: relative;
        overflow: hidden;
    }
    
    .poetry-container::before {
        content: '';
        position: absolute;
        top: 0;
        right: 0;
        width: 100px;
        height: 100px;
        background: linear-gradient(45deg, #667eea20, #764ba220);
        border-radius: 50%;
        transform: translate(30px, -30px);
    }
    
    .poetry-text {
        font-size: 1.2rem;
        line-height: 2;
        color: #2c3e50;
        white-space: pre-line;
        font-family: 'Georgia', serif;
        position: relative;
        z-index: 1;
    }
    
    .success-message {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        color: #155724;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #c3e6cb;
        margin: 1rem 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    .error-message {
        background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
        color: #721c24;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #f5c6cb;
        margin: 1rem 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        text-align: center;
        margin: 0.5rem 0;
    }
    
    .history-item {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
    }
</style>
""", unsafe_allow_html=True)

def generate_poetry(api_key, poetry_type, custom_topic, language, style, mood):
    """Generate poetry using Gemini AI"""
    try:
        # Configure Gemini API
        genai.configure(api_key=api_key)
        
        # Create model
        model = genai.GenerativeModel(os.environ.get('GEMINI_MODEL', 'gemini-2.5-flash'))
        
        # Create detailed prompt
        mood_descriptions = {
            'happy': 'joyful, uplifting, and positive',
            'melancholic': 'sad, reflective, and emotional',
            'inspiring': 'motivational, encouraging, and empowering',
            'romantic': 'passionate, loving, and tender',
            'mystical': 'mysterious, spiritual, and enchanting'
        }
        
        prompts = {
            'recursion': f"Write a {mood_descriptions[mood]} Pakistani poetry in {language} about recursion in programming. Make it {style}, creative, and educational. Include metaphors and analogies.",
            'ai': f"Write a {mood_descriptions[mood]} Pakistani poetry in {language} about artificial intelligence and its impact on society. Make it {style}, thoughtful, and inspiring.",
            'love': f"Write a {mood_descriptions[mood]} romantic Pakistani poetry in {language} about love and relationships. Make it {style}, emotional, and beautiful.",
            'nature': f"Write a {mood_descriptions[mood]} nature poetry in {language} about Pakistan's beautiful landscapes, seasons, and natural beauty. Make it {style} and vivid.",
            'philosophy': f"Write a {mood_descriptions[mood]} philosophical Pakistani poetry in {language} about life, wisdom, and human nature. Make it {style} and profound.",
            'technology': f"Write a {mood_descriptions[mood]} Pakistani poetry in {language} about technology, digital life, and how it affects our daily lives. Make it {style}, relatable, and modern.",
            'education': f"Write a {mood_descriptions[mood]} Pakistani poetry in {language} about education, learning, and the importance of knowledge. Make it {style}, inspiring, and motivational.",
            'social_media': f"Write a {mood_descriptions[mood]} Pakistani poetry in {language} about social media, its impact on society, and human connections. Make it {style}, thought-provoking, and relevant.",
            'climate': f"Write a {mood_descriptions[mood]} Pakistani poetry in {language} about climate change, environmental protection, and our responsibility to nature. Make it {style}, urgent, and meaningful.",
            'family': f"Write a {mood_descriptions[mood]} Pakistani poetry in {language} about family bonds, relationships, and the importance of family in Pakistani culture. Make it {style}, heartwarming, and touching.",
            'custom': f"Write a {mood_descriptions[mood]} creative Pakistani poetry in {language} about: {custom_topic}. Make it {style}, engaging, and meaningful."
        }
        
        base_prompt = prompts.get(poetry_type, prompts['custom'])
        
        # Add specific instructions based on language
        if language == 'Roman Urdu':
            base_prompt += " Use Roman Urdu script (English letters) for Urdu words. Make it authentic and culturally rich."
        elif language == 'Urdu + Roman':
            base_prompt += " Include both Urdu script and Roman Urdu translation. Make it beautiful and poetic."
        elif language == 'English':
            base_prompt = base_prompt.replace("Pakistani poetry", "poetry").replace("Pakistani", "")
        
        # Add style-specific instructions
        style_instructions = {
            'traditional': "Use traditional poetic forms and classical language.",
            'modern': "Use contemporary language and modern poetic techniques.",
            'romantic': "Focus on emotions, feelings, and romantic imagery.",
            'philosophical': "Include deep thoughts, wisdom, and philosophical concepts.",
            'humorous': "Add wit, humor, and playful elements while maintaining poetic beauty."
        }
        
        base_prompt += f" {style_instructions.get(style, '')}"
        
        # Generate content
        response = model.generate_content(base_prompt)
        
        return {
            'success': True,
            'poetry': response.text,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'settings': {
                'type': poetry_type,
                'language': language,
                'style': style,
                'mood': mood,
                'custom_topic': custom_topic if poetry_type == 'custom' else None
            }
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def save_to_history(poetry_data):
    """Save poetry to session state history"""
    if 'poetry_history' not in st.session_state:
        st.session_state.poetry_history = []
    
    st.session_state.poetry_history.insert(0, poetry_data)
    
    # Keep only last 10 items
    if len(st.session_state.poetry_history) > 10:
        st.session_state.poetry_history = st.session_state.poetry_history[:10]

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🤖 AI Poetry Generator Pro</h1>
        <p>Create beautiful Pakistani poetry using Google Gemini AI</p>
        <p>✨ Advanced features • Multiple styles • History tracking</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation
    selected = option_menu(
        menu_title=None,
        options=["🎨 Generate", "📚 History", "⚙️ Settings", "📊 Analytics"],
        icons=["pencil", "clock-history", "gear", "graph-up"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
        styles={
            "container": {"padding": "0!important", "background-color": "#fafafa"},
            "icon": {"color": "#667eea", "font-size": "20px"},
            "nav-link": {
                "font-size": "16px",
                "text-align": "center",
                "margin": "0px",
                "--hover-color": "#eee",
            },
            "nav-link-selected": {"background-color": "#667eea"},
        }
    )
    
    # Auto-load API key from .env file (hidden from UI)
    api_key = os.environ.get('GEMINI_API_KEY')
    
    # Sidebar for settings
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Poetry settings
        st.subheader("🎨 Poetry Settings")
        
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
                "Future of AI",
                "Urban life vs rural life",
                "Digital age challenges",
                "Cultural traditions",
                "Mental health awareness",
                "Environmental conservation"
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
            ["Roman Urdu", "Urdu + Roman", "English"],
            help="Choose the language for your poetry"
        )
        
        # Style selection
        style = st.selectbox(
            "🎨 Style",
            ["traditional", "modern", "romantic", "philosophical", "humorous"],
            help="Choose the style of poetry"
        )
        
        # Mood selection
        mood = st.selectbox(
            "😊 Mood",
            ["happy", "melancholic", "inspiring", "romantic", "mystical"],
            help="Choose the mood of the poetry"
        )
        
        st.markdown("---")
        
        # Quick stats
        st.subheader("📊 Quick Stats")
        if 'poetry_history' in st.session_state:
            st.metric("📝 Poems Generated", len(st.session_state.poetry_history))
        else:
            st.metric("📝 Poems Generated", "0")
        
        st.metric("🎯 Poetry Types", "6")
        st.metric("🌐 Languages", "3")
        st.metric("🎨 Styles", "5")
        st.metric("😊 Moods", "5")
    
    # Main content based on selected page
    if selected == "🎨 Generate":
        generate_page(api_key, poetry_type, custom_topic, language, style, mood)
    elif selected == "📚 History":
        history_page()
    elif selected == "⚙️ Settings":
        settings_page()
    elif selected == "📊 Analytics":
        analytics_page()

def generate_page(api_key, poetry_type, custom_topic, language, style, mood):
    """Generate poetry page"""
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("🎨 Generate Poetry")
        
        # Current settings display
        st.info(f"""
        **Current Settings:**
        - Type: {poetry_type.title()}
        - Language: {language}
        - Style: {style.title()}
        - Mood: {mood.title()}
        """)
        
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
                    result = generate_poetry(api_key, poetry_type, custom_topic, language, style, mood)
                
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
                    
                    # Save to history
                    save_to_history(result)
                    
                    # Action buttons
                    col_a, col_b, col_c = st.columns(3)
                    
                    with col_a:
                        st.download_button(
                            label="📥 Download",
                            data=result['poetry'],
                            file_name=f"ai_poetry_{poetry_type}_{int(time.time())}.txt",
                            mime="text/plain"
                        )
                    
                    with col_b:
                        if st.button("🔄 Generate Again"):
                            st.rerun()
                    
                    with col_c:
                        if st.button("📚 View History"):
                            st.session_state.selected_page = "📚 History"
                            st.rerun()
                    
                else:
                    st.markdown(f"""
                    <div class="error-message">
                        ❌ Error: {result['error']}
                    </div>
                    """, unsafe_allow_html=True)
    
    with col2:
        st.header("💡 Tips & Examples")
        
        # Tips
        st.markdown("""
        ### 💡 Pro Tips:
        - Try different mood combinations
        - Mix traditional style with modern topics
        - Use custom topics for unique results
        - Experiment with different languages
        """)
        
        # Example topics
        st.markdown("### 🎯 Example Topics:")
        example_topics = [
            "Technology and humanity",
            "Childhood memories",
            "Pakistani culture",
            "Dreams and aspirations",
            "Friendship and loyalty"
        ]
        
        for topic in example_topics:
            if st.button(f"✨ {topic}", key=f"example_{topic}"):
                st.session_state.custom_topic = topic
                st.rerun()

def history_page():
    """History page"""
    st.header("📚 Poetry History")
    
    if 'poetry_history' not in st.session_state or not st.session_state.poetry_history:
        st.info("📝 No poetry generated yet. Go to the Generate page to create some!")
        return
    
    # Search and filter
    col1, col2 = st.columns([2, 1])
    
    with col1:
        search_term = st.text_input("🔍 Search in history", placeholder="Search by type, style, or content...")
    
    with col2:
        filter_type = st.selectbox("Filter by type", ["All"] + list(set([item['settings']['type'] for item in st.session_state.poetry_history])))
    
    # Display history
    filtered_history = st.session_state.poetry_history
    
    if search_term:
        filtered_history = [item for item in filtered_history if search_term.lower() in item['poetry'].lower() or search_term.lower() in item['settings']['type'].lower()]
    
    if filter_type != "All":
        filtered_history = [item for item in filtered_history if item['settings']['type'] == filter_type]
    
    for i, item in enumerate(filtered_history):
        with st.expander(f"📝 {item['settings']['type'].title()} - {item['timestamp']}", expanded=False):
            st.markdown(f"""
            <div class="history-item">
                <div class="poetry-text">{item['poetry']}</div>
                <br>
                <small><strong>Settings:</strong> {item['settings']['language']} • {item['settings']['style']} • {item['settings']['mood']}</small>
            </div>
            """, unsafe_allow_html=True)
            
            col_a, col_b, col_c = st.columns(3)
            
            with col_a:
                st.download_button(
                    label="📥 Download",
                    data=item['poetry'],
                    file_name=f"poetry_{i+1}_{int(time.time())}.txt",
                    mime="text/plain",
                    key=f"download_{i}"
                )
            
            with col_b:
                if st.button("🔄 Regenerate", key=f"regenerate_{i}"):
                    # Set settings and go to generate page
                    st.session_state.regenerate_settings = item['settings']
                    st.rerun()
            
            with col_c:
                if st.button("🗑️ Delete", key=f"delete_{i}"):
                    st.session_state.poetry_history.pop(i)
                    st.rerun()

def settings_page():
    """Settings page"""
    st.header("⚙️ Settings & Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔑 API Configuration")
        st.info("""
        **API key is automatically loaded from .env file.**
        
        **To set up your API key:**
        1. Create a `.env` file in project root
        2. Add: `GEMINI_API_KEY=your-api-key-here`
        3. Restart the app
        """)
        
        st.subheader("🎨 Default Settings")
        st.selectbox("Default Language", ["Roman Urdu", "Urdu + Roman", "English"])
        st.selectbox("Default Style", ["modern", "traditional", "romantic", "philosophical", "humorous"])
        st.selectbox("Default Mood", ["happy", "melancholic", "inspiring", "romantic", "mystical"])
    
    with col2:
        st.subheader("📊 App Information")
        st.markdown("""
        **Version:** 2.0.0  
        **Powered by:** Google Gemini AI  
        **Framework:** Streamlit  
        **Last Updated:** {date}
        """.format(date=datetime.now().strftime("%Y-%m-%d")))
        
        st.subheader("🔄 Actions")
        if st.button("🗑️ Clear History"):
            if 'poetry_history' in st.session_state:
                st.session_state.poetry_history = []
                st.success("History cleared!")
        
        if st.button("🔄 Reset Settings"):
            st.success("Settings reset to defaults!")

def analytics_page():
    """Analytics page"""
    st.header("📊 Analytics & Insights")
    
    if 'poetry_history' not in st.session_state or not st.session_state.poetry_history:
        st.info("📝 No data available yet. Generate some poetry first!")
        return
    
    history = st.session_state.poetry_history
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>📝 Total Poems</h3>
            <h2>{count}</h2>
        </div>
        """.format(count=len(history)), unsafe_allow_html=True)
    
    with col2:
        types_count = len(set([item['settings']['type'] for item in history]))
        st.markdown("""
        <div class="metric-card">
            <h3>🎯 Types Used</h3>
            <h2>{count}</h2>
        </div>
        """.format(count=types_count), unsafe_allow_html=True)
    
    with col3:
        languages_count = len(set([item['settings']['language'] for item in history]))
        st.markdown("""
        <div class="metric-card">
            <h3>🌐 Languages</h3>
            <h2>{count}</h2>
        </div>
        """.format(count=languages_count), unsafe_allow_html=True)
    
    with col4:
        styles_count = len(set([item['settings']['style'] for item in history]))
        st.markdown("""
        <div class="metric-card">
            <h3>🎨 Styles</h3>
            <h2>{count}</h2>
        </div>
        """.format(count=styles_count), unsafe_allow_html=True)
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Poetry Types Distribution")
        type_counts = {}
        for item in history:
            type_name = item['settings']['type']
            type_counts[type_name] = type_counts.get(type_name, 0) + 1
        
        st.bar_chart(type_counts)
    
    with col2:
        st.subheader("📊 Language Usage")
        lang_counts = {}
        for item in history:
            lang = item['settings']['language']
            lang_counts[lang] = lang_counts.get(lang, 0) + 1
        
        st.bar_chart(lang_counts)
    
    # Recent activity
    st.subheader("🕒 Recent Activity")
    recent_items = history[:5]  # Last 5 items
    
    for item in recent_items:
        st.markdown(f"""
        <div class="history-item">
            <strong>{item['settings']['type'].title()}</strong> • {item['timestamp']} • {item['settings']['language']}
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

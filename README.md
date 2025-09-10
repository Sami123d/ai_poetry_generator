# OpenAI-00

A Python project using Google Gemini AI for AI-powered assistance.

## Installation

This project uses `uv` for dependency management. To install:

```bash
# Clone the repository
git clone <your-repo-url>
cd openai_00

# Install dependencies
uv sync
```

## Usage

### As a command-line tool

```bash
# Run the main application
openai-00
```

### As a Python module

```python
from openai_00 import main

# Run the main function
main()
```

### Run helloworld.py with Gemini AI

```bash
# Method 1: Set environment variable
$env:GEMINI_API_KEY='your-api-key-here'
uv run python -u src/openai_00/helloworld.py

# Method 2: Use .env file (Recommended)
# Create .env file in project root with:
# GEMINI_API_KEY=your-api-key-here
uv run python -u src/openai_00/helloworld.py
```

### Run Streamlit UI

```bash
# Basic UI
uv run streamlit run streamlit_app.py

# Advanced UI with multiple pages
uv run streamlit run advanced_streamlit_app.py

# Or use batch files
run_streamlit.bat
run_advanced.bat
```

## Development

To set up the development environment:

```bash
# Install dependencies
uv sync

# Run in development mode
uv run python -m openai_00
```

## Requirements

- Python 3.12+
- Google Gemini API key (set as environment variable `GEMINI_API_KEY`)

## Getting a Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Create a new API key
4. Set it as an environment variable: `GEMINI_API_KEY=your-key-here`

## License

[Add your license here]

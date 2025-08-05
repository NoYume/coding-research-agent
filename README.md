# 🤖 Coding Research AI Agent

<div align="center">

<p align="center">
  <img src=https://github.com/NoYume/coding-research-agent/blob/1ca2f8dc1cbded9bfaf859d26ee072bdde2a529a/media/banner.png />
</p>

*Discover, Compare, and Analyze Developer Tools with AI*

</div>

## 📋 Overview

The Coding Research AI Agent is an intelligent CLI tool that helps developers discover and compare alternative tools, libraries, and platforms. Using advanced AI workflows, it automatically researches tools, scrapes documentation, and provides personalized recommendations based on your specific needs.

### ✨ Key Features

- **Smart Tool Discovery** - Automatically finds alternatives to any developer tool
- **Dynamic Categorization** - Uses AI to understand query context and tool categories
- **Comprehensive Analysis** - Extracts pricing, tech stack, language support, and integrations
- **Intelligent Fallbacks** - Multiple search strategies ensure reliable results
- **Real-time Progress** - Custom CLI with spinners and progress indicators
- **Dynamic Error Handling** - Automatic retries and failure recovery
- **Local Processing** - All analysis runs on your machine

<p align="center">
  <img src=https://github.com/NoYume/coding-research-agent/blob/748c7db4302ba0310e5a4d25ec9abd70794a4692/media/loading_messages.gif />
</p>

## 🚀 Quick Start

### Prerequisites

- Python 3.13+
- [uv](https://github.com/astral-sh/uv) package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/coding-research-agent.git
   cd coding-research-agent
   ```

2. **Install dependencies with uv**
   ```bash
   uv sync
   ```

3. **Run the application**
   ```bash
   uv run main.py
   ```

## ⚙️ Configuration

Create a `.env` file in the project root:

```env
# Required API Keys
ANTHROPIC_API_KEY=your_anthropic_api_key_here
FIRECRAWL_API_KEY=your_firecrawl_api_key_here
```

### Getting API Keys

- **Anthropic API Key**: Sign up at [console.anthropic.com](https://console.anthropic.com/)
- **Firecrawl API Key**: Get yours at [firecrawl.dev](https://firecrawl.dev/)

## 💡 Usage Examples

### Basic Queries
```bash
❔ Developer Tools Question: React alternatives
❔ Developer Tools Question: databases better than MySQL
❔ Developer Tools Question: hosting platforms like AWS
```

### Specific Use Cases
```bash
❔ Developer Tools Question: vector databases for AI applications
❔ Developer Tools Question: free alternatives to GitHub Copilot
❔ Developer Tools Question: Python web frameworks faster than Django
```

### Sample Output

<p align="center">
  <img src=https://github.com/NoYume/coding-research-agent/blob/748c7db4302ba0310e5a4d25ec9abd70794a4692/media/output_example.gif />
</p>

## 🏗️ Project Structure

```
coding-research-agent/
├── app/
│   ├── __init__.py
│   ├── workflow.py          # Main LangGraph workflow orchestration
│   ├── models.py            # Pydantic data models
│   ├── prompts.py           # AI prompts and dynamic categorization
│   ├── logger.py            # Progress logging and CLI interface
│   └── firecrawl.py         # Web scraping service with retry logic
├── media/                   # README media files
├── main.py                  # CLI entry point
├── pyproject.toml          # uv project configuration
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

## 🔧 Development

### Running with uv

```bash
# Activate virtual environment
uv venv

# Install new dependencies
uv sync

# Run the application
uv run main.py

```

### Available Commands

- `help` - Show help menu with examples
- `clear` - Clear the terminal screen
- `exit`/`quit` - Exit the application

<p align="center">
  <img src=https://github.com/NoYume/coding-research-agent/blob/c36edc252299d62144f0291b4b43e5fb9e228f3c/media/command_example.gif />
</p>

## 🛠️ Technical Architecture

### Core Components

1. **LangGraph Workflow** - Orchestrates the research pipeline with three main nodes:
   - `extract_tools` - Finds and extracts tool names from articles
   - `research` - Gathers detailed information about each tool
   - `analyze` - Generates personalized recommendations

2. **Dynamic AI Categorization** - Uses Claude to automatically:
   - Detect query categories (databases, frameworks, hosting, etc.)
   - Generate relevant examples for better extraction
   - Exclude generic terms to improve accuracy

3. **Intelligent Fallback System** - Multiple strategies ensure reliable results:
   - Article-based extraction (primary)
   - Direct search results (secondary)
   - AI-generated suggestions (tertiary)

4. **Robust Error Handling** - Handles API failures:
   - Automatic retries with exponential backoff
   - 502 error detection and recovery
   - JSON parsing error handling

## 🤝 Contributing

Contributions are welcome! Here are some ways you can help:

- Report bugs and issues
- Suggest new features or improvements
- Submit pull requests
- Improve documentation


<div align="center">

**[⭐ Star this repository](https://github.com/yourusername/coding-research-agent)** if you find it useful!


</div>

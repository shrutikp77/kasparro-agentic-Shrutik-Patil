# Kasparro AI - Agentic Content Generation System

An intelligent, multi-agent system for automated content generation using AI.

## 🚀 Overview

This project implements an agentic architecture where multiple specialized AI agents collaborate to generate, refine, and output high-quality content.

## 📁 Project Structure

```
kasparro-ai-agentic-content-generation-system/
├── src/
│   ├── agents/           # Individual agent implementations
│   ├── content_blocks/   # Reusable logic components  
│   ├── templates/        # Template definitions
│   ├── models/           # Data models and schemas
│   ├── orchestrator.py   # Agent coordination logic
│   └── utils.py          # Utility functions
├── output/               # Generated JSON outputs
├── docs/                 # Project documentation
│   └── projectdocumentation.md
├── main.py               # Application entry point
├── requirements.txt      # Python dependencies
└── README.md             # This file
```

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd kasparro-ai-agentic-content-generation-system
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

## 🚀 Usage

Run the main application:

```bash
python main.py
```

## 🏗️ Architecture

### Agents

The system uses specialized agents for different tasks:
- **Content Planning Agent**: Plans content structure
- **Content Generation Agent**: Generates content
- **Review Agent**: Reviews and refines output
- **Output Agent**: Formats and saves final content

### Orchestrator

The orchestrator (`src/orchestrator.py`) coordinates agent execution:
- Registers and manages agents
- Defines execution pipelines
- Handles inter-agent communication

### Templates

Templates in `src/templates/` define content structures and formats.

### Models

Data models in `src/models/` ensure type safety and validation.

## 📤 Output

Generated content is saved as JSON files in the `output/` directory.

## 📚 Documentation

See [docs/projectdocumentation.md](docs/projectdocumentation.md) for detailed documentation.

## 🧪 Testing

```bash
pytest
```

## 📝 License

[Add license information]

## 🤝 Contributing

[Add contribution guidelines]

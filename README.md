# Kasparro AI — Multi-Agent Content Generation System

A DAG-based multi-agent system that generates structured content pages from product data using LLM-powered autonomous agents.

## Overview

This system demonstrates how multiple specialized AI agents can collaborate to produce rich content. Given product information, the pipeline generates:

- **FAQ Pages** — 15 categorized Q&As addressing common customer concerns
- **Product Pages** — Compelling descriptions with benefits, usage, and safety information
- **Comparison Pages** — Competitive analysis with auto-generated competitor benchmarking

The architecture emphasizes **agent autonomy**, **modular design**, and **clean dependency management** through DAG-based orchestration.

---

## Key Features

| Feature | Description |
|---------|-------------|
| Autonomous Agents | Each agent independently determines when to execute based on dependency satisfaction |
| DAG Orchestration | Clean, predictable execution order with parallel processing where possible |
| LLM Integration | Powered by Groq's Llama 3.3 70B for fast, high-quality content generation |
| Modular Architecture | Easily swap agents, templates, or LLM providers without system-wide changes |
| Production-Ready | Built-in rate limiting, retry logic, and graceful error handling |

---

## Project Structure

```
├── main.py                     # Application entry point
├── src/
│   ├── orchestrator.py         # DAG-based agent coordination
│   ├── llm_client.py           # Groq API integration
│   ├── utils.py                # Utility functions
│   ├── agents/                 # Agent implementations
│   │   ├── base_agent.py       # Abstract base class
│   │   ├── parser_agent.py     # Data validation agent
│   │   ├── question_agent.py   # Question generation agent
│   │   ├── faq_agent.py        # FAQ generation agent
│   │   ├── product_agent.py    # Product page agent
│   │   └── comparison_agent.py # Comparison agent
│   ├── models/                 # Pydantic data schemas
│   ├── templates/              # Output structure templates
│   └── content_blocks/         # Utility generators
├── output/                     # Generated JSON files
└── docs/                       # Documentation
```

---

## Getting Started

### Prerequisites
- Python 3.8+
- Groq API key ([Get one free](https://console.groq.com/))

### Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Configure environment
echo "GROQ_API_KEY=your_api_key_here" > .env

# Run the pipeline
python main.py
```

### Output

After execution, check the `output/` directory for:

| File | Contents |
|------|----------|
| `faq.json` | 15 Q&As across 5 categories (Informational, Safety, Usage, Purchase, Comparison) |
| `product_page.json` | Complete product page with all content sections |
| `comparison_page.json` | Side-by-side comparison with generated competitor analysis |

---

## Architecture

### Agent Dependency Graph (DAG)

```
         ┌─────────┐
         │ Parser  │  ← Runs first (no dependencies)
         └────┬────┘
              │
    ┌─────────┼─────────┐
    │         │         │
    ▼         ▼         ▼
┌─────────┐ ┌─────────┐ ┌────────────┐
│Questions│ │ Product │ │ Comparison │  ← Depend on Parser
└────┬────┘ └─────────┘ └────────────┘
     │
     ▼
 ┌───────┐
 │  FAQ  │  ← Depends on Parser + Questions
 └───────┘
```

### Agent Summary

| Agent | Dependencies | Purpose | Uses LLM |
|-------|--------------|---------|----------|
| DataParserAgent | None | Validates product data into Pydantic model | No |
| QuestionGenerationAgent | Parser | Generates 15 diverse user questions | Yes |
| ProductPageAgent | Parser | Creates marketing copy and product descriptions | Yes |
| ComparisonAgent | Parser | Generates competitor product and analysis | Yes |
| FAQGenerationAgent | Parser, Questions | Produces answers for generated questions | Yes |

---

## Documentation

For detailed architecture documentation, design decisions, and implementation details, see:

**[docs/projectdocumentation.md](docs/projectdocumentation.md)**

---

## Technology Stack

| Component | Technology |
|-----------|------------|
| Language | Python 3.8+ |
| LLM Provider | Groq Cloud |
| Model | Llama 3.3 70B Versatile |
| Data Validation | Pydantic |
| Environment Management | python-dotenv |

---

## Notes

- **Rate Limits**: The system includes automatic retry with exponential backoff for API rate limits
- **Customization**: Modify product data in `main.py` to generate content for different products
- **Extensibility**: The modular design supports adding new agents with minimal changes to existing code

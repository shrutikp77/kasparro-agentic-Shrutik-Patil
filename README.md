# Kasparro AI — Multi-Agent Content Generation System

A LangGraph-powered multi-agent system that generates structured content pages from product data using LLM-powered autonomous agents.

## Overview

This system demonstrates how multiple specialized AI agents can collaborate to produce rich content. Given product information, the pipeline generates:

- **FAQ Pages** — 15 categorized Q&As addressing common customer concerns
- **Product Pages** — Compelling descriptions with benefits, usage, and safety information
- **Comparison Pages** — Competitive analysis with auto-generated competitor benchmarking

The architecture emphasizes **agent autonomy**, **modular design**, and **clean dependency management** through LangGraph-based orchestration.

---

## Key Features

| Feature | Description |
|---------|-------------|
| LangGraph Orchestration | StateGraph-based workflow with typed state management and declarative edges |
| Autonomous Agents | Each agent independently determines when to execute based on dependency satisfaction |
| LLM Integration | Lazy-initialized Groq Llama 3.3 70B for fast, high-quality content generation |
| Comprehensive Tests | 50+ pytest tests covering agents, generators, and integration workflows |
| **Hardcode-Free** | No requirement strings in code; all data loaded from external JSON files |
| **Clean-Env Compatible** | Tests run without API key; imports don't crash in fresh environments |
| **Strict Validation** | FAQ count ≥15 enforced; all outputs schema-validated at boundaries |
| **CLI Support** | Command-line arguments for dataset, output dir, and product selection |
| Modular Architecture | Easily swap agents, templates, or LLM providers without system-wide changes |
| Production-Ready | Built-in rate limiting, retry logic, and graceful error handling |

---

## Project Structure

```
├── main.py                     # Application entry point
├── src/
│   ├── orchestrator.py         # LangGraph workflow wrapper
│   ├── llm_client.py           # Groq API integration
│   ├── utils.py                # Utility functions
│   ├── graph/                  # LangGraph workflow
│   │   ├── state.py            # TypedDict state schema
│   │   └── workflow.py         # StateGraph definition
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
├── tests/                      # Test suite
│   ├── test_agents.py          # Agent unit tests
│   ├── test_content_blocks.py  # Generator function tests
│   └── test_integration.py     # End-to-end workflow tests
├── output/                     # Generated JSON files
└── docs/                       # Documentation
```

---

## Getting Started

### Prerequisites
- Python 3.10+
- Groq API key ([Get one free](https://console.groq.com/))

### Installation

```bash
# Clone the repository (or extract from zip)
cd kasparro-ai-agentic-content-generation-system-Shrutik_Patil

# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Configure environment (copy example and edit)
copy .env.example .env  # Windows
cp .env.example .env    # Linux/Mac

# Edit .env and add your Groq API key
# GROQ_API_KEY=your_actual_api_key_here
```

### Running the Pipeline

```bash
# Use default dataset (data/products.json)
python main.py

# Use custom dataset file
python main.py --dataset path/to/your_products.json

# Select different product from dataset (by index)
python main.py --product-index 0

# Use custom output directory
python main.py --output-dir custom_output/

# See all options
python main.py --help
```

### Running Tests

```bash
# Run all tests (works WITHOUT Groq API key)
pytest tests/ -v

# Run specific test module
pytest tests/test_agents.py -v

# Run with coverage
pytest tests/ --cov=src
```

### Output

After execution, check your output directory (default: `output/`) for:

| File | Contents | Validation |
|------|----------|------------|
| `faq.json` | **≥15 Q&As** across 5 categories (Informational, Safety, Usage, Purchase, Comparison) | Enforced: Must have at least 15 FAQs |
| `product_page.json` | Complete product page with all content sections | Schema validated |
| `comparison_page.json` | Side-by-side comparison with generated competitor analysis | Schema validated |

> **Note**: All outputs are validated against strict schemas. FAQ count < 15 will raise an error.

---

## Architecture

### LangGraph Workflow

The system uses LangGraph's StateGraph to orchestrate agent execution. Each node in the graph represents an agent, and edges define the dependency structure.

```
         ┌─────────┐
         │ Parser  │  ← START node (no dependencies)
         └────┬────┘
              │
    ┌─────────┼─────────┐
    │         │         │
    ▼         ▼         ▼
┌─────────┐ ┌─────────┐ ┌────────────┐
│Questions│ │ Product │ │ Comparison │  ← Depend on Parser
└────┬────┘ └────┬────┘ └─────┬──────┘
     │           │            │
     ▼           └──────┬─────┘
 ┌───────┐              │
 │  FAQ  │              │
 └───┬───┘              │
     └────────┬─────────┘
              ▼
            [END]
```

### State Management

The workflow uses a `ContentGenerationState` TypedDict to share data between nodes:

```python
class ContentGenerationState(TypedDict, total=False):
    raw_input: Dict[str, Any]
    parsed_product: Optional[Product]
    questions: Optional[List[Question]]
    faq_output: Optional[Dict[str, Any]]
    product_output: Optional[Dict[str, Any]]
    comparison_output: Optional[Dict[str, Any]]
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

## Test Coverage

The project includes a comprehensive test suite:

| Test Module | Tests | Coverage |
|-------------|-------|----------|
| `test_agents.py` | 18 | Agent initialization, dependencies, can_execute logic |
| `test_content_blocks.py` | 15 | Generator functions, price calculations |
| `test_integration.py` | 17 | Templates, orchestrator, LangGraph workflow |

---

## Documentation

For detailed architecture documentation, design decisions, and implementation details, see:

**[docs/projectdocumentation.md](docs/projectdocumentation.md)**

---

## Technology Stack

| Component | Technology |
|-----------|------------|
| Language | Python 3.10+ |
| Orchestration | LangGraph |
| LLM Provider | Groq Cloud |
| Model | Llama 3.3 70B Versatile |
| Data Validation | Pydantic |
| Testing | pytest |
| Environment Management | python-dotenv |

---

## Configuration

All configuration is managed via environment variables (`.env` file):

| Variable | Default | Description |
|----------|---------|-------------|
| `GROQ_API_KEY` | *(required)* | Your Groq API key from console.groq.com |
| `AGENT_DELAY` | `5` | Delay between LLM calls (seconds) for rate limiting |
| `DEFAULT_DATASET_PATH` | `data/products.json` | Default path to product dataset |
| `OUTPUT_DIR` | `output` | Directory for generated JSON files |
| `DEFAULT_MAX_RETRIES` | `3` | Max retries for failed LLM calls |
| `DEFAULT_MAX_TOKENS` | `2000` | Default max tokens for LLM responses |

---

## Notes & Features

### Clean Environment Support
- **No hardcoded data**: All product data loaded from external `data/products.json`
- **No import-time crashes**: System uses lazy LLM client initialization
- **Tests work offline**: Full test suite runs without Groq API key set

### Validation & Quality
- **FAQ Count Enforced**: System validates ≥15 FAQs (assignment requirement)
- **Schema Validation**: All outputs validated at boundaries before writing
- **Error Handling**: Graceful failures with clear error messages

### Extensibility
- **CLI Support**: Use `--dataset`, `--product-index`, `--output-dir` arguments
- **Rate Limiting**: Configurable delay via `AGENT_DELAY` environment variable
- **Modular Design**: Easily add new agents or swap LLM providers
- **Dataset Flexibility**: Support for multiple products in single dataset file

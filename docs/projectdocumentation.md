# Multi-Agent Content Generation System — Technical Documentation

This document provides a comprehensive overview of the system architecture, design decisions, and implementation details.

---

## Problem Statement

Traditional content generation approaches often suffer from:

- **Monolithic design** — Data processing, content logic, and formatting tightly coupled in single scripts
- **Poor maintainability** — Changes in one area cascade unpredictably to others
- **Limited reusability** — Adding new content types requires significant rework

Our goal was to build a system where specialized agents work autonomously, coordinated through a clean dependency graph, producing structured content that's easy to extend and maintain.

---

## Solution Approach

We implemented a **DAG-based multi-agent system** with the following characteristics:

| Principle | Implementation |
|-----------|----------------|
| Agent Autonomy | Each agent determines its own readiness based on dependency satisfaction |
| Single Responsibility | One agent, one job — no overlap in responsibilities |
| Shared State Communication | Agents exchange data through a common dictionary, not direct calls |
| Template-Based Output | Standardized output structures with validation |
| LLM-Powered Generation | Groq API for intelligent, context-aware content creation |

---

## System Architecture

### High-Level Overview

```
┌─────────────────────────────────────────────────────────────┐
│                      ORCHESTRATOR                           │
│   Coordinates agent execution based on dependency graph     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   ┌─────────────────────────────────────────────────────┐   │
│   │                 SHARED DATA STATE                   │   │
│   │   Central storage for agent inputs and outputs      │   │
│   └─────────────────────────────────────────────────────┘   │
│                            │                                │
│          ┌─────────────────┼─────────────────┐              │
│          ▼                 ▼                 ▼              │
│     ┌─────────┐      ┌──────────┐      ┌──────────┐        │
│     │ Agents  │      │   LLM    │      │Templates │        │
│     │  (5x)   │      │  Client  │      │   (3x)   │        │
│     └─────────┘      └──────────┘      └──────────┘        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Component Responsibilities

| Component | Purpose |
|-----------|---------|
| **Orchestrator** | Manages execution loop, tracks completion, enforces dependencies |
| **Agents** | Execute specific content generation tasks autonomously |
| **LLM Client** | Handles API communication, retries, and JSON parsing |
| **Templates** | Validate and structure final outputs |
| **Models** | Pydantic schemas for data validation |

---

## Agent Specifications

### 1. Data Parser Agent

| Property | Value |
|----------|-------|
| Agent ID | `parser` |
| Dependencies | None |
| Input | Raw product JSON from `shared_data["raw_input"]` |
| Output | Validated `Product` Pydantic model |
| LLM Usage | None — performs validation only |

**Purpose**: Serves as the entry point, ensuring all downstream agents receive clean, validated data. Runs first since it has no dependencies.

---

### 2. Question Generation Agent

| Property | Value |
|----------|-------|
| Agent ID | `questions` |
| Dependencies | `["parser"]` |
| Input | `Product` model from parser output |
| Output | List of 15 `Question` objects across 5 categories |
| LLM Usage | Generates diverse, natural user questions |

**Purpose**: Creates realistic questions a user might ask about the product. Categories include Informational, Safety, Usage, Purchase, and Comparison.

---

### 3. Product Page Agent

| Property | Value |
|----------|-------|
| Agent ID | `product` |
| Dependencies | `["parser"]` |
| Input | `Product` model from parser output |
| Output | Structured product page dictionary |
| LLM Usage | Generates marketing copy and descriptions |

**Purpose**: Transforms raw product data into compelling marketing content including descriptions, benefits explanations, usage guidance, and safety information.

---

### 4. Comparison Agent

| Property | Value |
|----------|-------|
| Agent ID | `comparison` |
| Dependencies | `["parser"]` |
| Input | `Product` model from parser output |
| Output | Comparison page with two products and analysis |
| LLM Usage | Two calls — generates competitor, then comparative analysis |

**Purpose**: Creates a realistic competitive comparison by first generating a fictional competitor product, then analyzing differences in ingredients, pricing, and effectiveness.

---

### 5. FAQ Generation Agent

| Property | Value |
|----------|-------|
| Agent ID | `faq` |
| Dependencies | `["parser", "questions"]` |
| Input | `Product` model + list of `Question` objects |
| Output | FAQ page with Q&A pairs |
| LLM Usage | Generates helpful, accurate answers |

**Purpose**: Takes the generated questions and produces informative answers based on product data. Runs last due to its dependency on both parser and question agent outputs.

---

## Execution Flow

### DAG Structure

```
         ┌─────────┐
         │ Parser  │
         └────┬────┘
              │
    ┌─────────┼─────────┐
    │         │         │
    ▼         ▼         ▼
┌─────────┐ ┌─────────┐ ┌────────────┐
│Questions│ │ Product │ │ Comparison │
└────┬────┘ └─────────┘ └────────────┘
     │
     ▼
 ┌───────┐
 │  FAQ  │
 └───────┘
```

### Execution Sequence

1. **Initialization**
   - Create all 5 agent instances
   - Initialize shared data dictionary
   - Configure rate limit delays (5 seconds between LLM-using agents)

2. **Data Loading**
   - Product data placed in `shared_data["raw_input"]`

3. **DAG Execution Loop**
   - Identify agents with satisfied dependencies
   - Execute ready agents
   - Store outputs in `shared_data[agent_id]`
   - Apply rate limiting between LLM calls
   - Repeat until all agents complete

4. **Output Collection**
   - Gather FAQ, product, and comparison outputs
   - Write to JSON files in `output/` directory

---

## LLM Integration

### Configuration

| Setting | Value |
|---------|-------|
| Provider | Groq Cloud |
| Model | `llama-3.3-70b-versatile` |
| Output Mode | Structured JSON prompts |
| Max Retries | 3 |
| Backoff Strategy | Exponential (10s, 20s, 30s) |
| Inter-Agent Delay | 5 seconds |

### Error Handling

The LLM client implements several robustness features:

- **Rate limit detection** — Identifies 429 errors and rate-related messages
- **Automatic retry** — Exponential backoff with configurable max attempts
- **JSON extraction** — Regex-based parsing to handle markdown-wrapped responses
- **Response validation** — Ensures valid JSON before returning to agents

---

## Template System

Templates provide structure and validation for agent outputs:

| Template | Required Fields | Output Structure |
|----------|-----------------|------------------|
| FAQTemplate | question, answer for each item | `{page_type, faqs: [{question, answer}]}` |
| ProductTemplate | name, benefits, how_to_use, key_ingredients, price | `{page_type, sections: {...}}` |
| ComparisonTemplate | product_a, product_b, comparison_metrics | `{page_type, products: [], comparison_metrics: []}` |

Templates validate inputs and raise `ValueError` if required fields are missing, preventing malformed outputs.

---

## Utility Functions

The `content_blocks/generators.py` module provides deterministic helper functions:

| Function | Purpose |
|----------|---------|
| `extract_product_summary` | Generate one-line product summary |
| `calculate_price_difference` | Compute price delta and percentage |
| `extract_common_ingredients` | Find shared ingredients between products |
| `extract_unique_ingredients` | Identify ingredients unique to one product |
| `generate_content_block` | Create structured content block wrapper |
| `merge_content_blocks` | Combine multiple blocks into single output |

These functions are pure (no LLM calls) and deterministic, suitable for operations where exact reproducibility is needed.

---

## Output Files

| File | Description |
|------|-------------|
| `output/faq.json` | 15 Q&A pairs organized by category |
| `output/product_page.json` | Complete product page with all sections |
| `output/comparison_page.json` | Two-product comparison with detailed metrics |

All outputs are machine-readable JSON, suitable for direct integration with CMS platforms, APIs, or frontend applications.

---

## Running the System

### Prerequisites

- Python 3.8 or higher
- Groq API key

### Setup and Execution

```bash
# Install dependencies
pip install -r requirements.txt

# Configure API key
echo "GROQ_API_KEY=your_key_here" > .env

# Execute pipeline
python main.py
```

### Expected Output

```
============================================================
Kasparro AI - Agentic Content Generation System
============================================================
Starting multi-agent content generation pipeline...

Product: GlowBoost Vitamin C Serum
Price: ₹699

Agent execution order based on DAG dependencies...
  parser (no deps) → runs first
  questions, product, comparison (dep: parser) → run after parser
  faq (deps: parser, questions) → runs after questions

----------------------------------------
Executing agents...
----------------------------------------
Using model: llama-3.3-70b-versatile
Executing agent: parser...
Agent parser completed.
Executing agent: questions...
Agent questions completed.
Waiting 5s to respect rate limits...
...

  [parser] completed
  [questions] completed
  [faq] completed
  [product] completed
  [comparison] completed

----------------------------------------
Saving outputs to JSON files...
----------------------------------------
  ✓ faq.json
  ✓ product_page.json
  ✓ comparison_page.json

============================================================
All pages generated successfully!
Outputs saved to: output/
============================================================
```

---

## Design Principles

### Agent Autonomy

Each agent implements two key methods from `BaseAgent`:

- `can_execute(completed_agents)` — Returns `True` when all dependencies are satisfied
- `execute(shared_data)` — Performs the agent's work and returns output

The orchestrator never dictates agent behavior — it only queries readiness and triggers execution.

### Modularity

The system is organized into independent modules:

| Module | Responsibility |
|--------|----------------|
| `src/agents/` | Individual agent implementations |
| `src/models/` | Data validation schemas |
| `src/templates/` | Output structure definitions |
| `src/content_blocks/` | Pure utility functions |
| `src/llm_client.py` | External API abstraction |
| `src/orchestrator.py` | Workflow coordination |

This separation allows changes to one component without affecting others.

### Graceful Degradation

The system handles failures without crashing:

- Rate limits trigger automatic retry with backoff
- Missing LLM response fields fall back to defaults
- Template validation catches malformed outputs early

---

## Technology Stack

| Layer | Technology |
|-------|------------|
| Language | Python 3.8+ |
| LLM Provider | Groq Cloud |
| Model | Llama 3.3 70B Versatile |
| Data Validation | Pydantic |
| Environment | python-dotenv |
| Output Format | JSON |

---

## Summary

This multi-agent system demonstrates how autonomous, specialized agents can collaborate through a well-defined dependency graph to produce structured content. The modular design supports extensibility, the DAG structure ensures predictable execution, and the LLM integration enables high-quality content generation.

The architecture prioritizes:
- **Clarity** — Each component has a single, well-defined purpose
- **Reliability** — Error handling and validation at every layer
- **Extensibility** — New agents can be added with minimal changes

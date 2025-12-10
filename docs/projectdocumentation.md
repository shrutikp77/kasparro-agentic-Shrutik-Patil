# 📖 Multi-Agent Content Generation System — Full Documentation

> *A deep dive into how 5 AI agents work together to generate content.*

---

## 🎯 The Problem We're Solving

Traditional content generation is a mess. You've probably seen it:

- **Monolithic scripts** that mix data processing, business logic, and output formatting into one giant file
- **Spaghetti dependencies** where changing one thing breaks everything else
- **Zero reusability** — need a new content type? Write everything from scratch

We wanted something better. Something that feels more like a **team of specialists** than a one-size-fits-all script.

---

## 💡 Our Solution: A Team of Autonomous Agents

Imagine you're running a content agency. You wouldn't have one person do everything. You'd have:

1. **A data person** who cleans and validates incoming data
2. **A researcher** who comes up with the right questions to ask
3. **A product writer** who crafts compelling descriptions
4. **A comparison analyst** who benchmarks against competitors
5. **An FAQ specialist** who answers customer questions

That's exactly what we built — but with AI agents.

### How They Work Together

Each agent is **autonomous**:
- It knows what it needs before it can start (its *dependencies*)
- It decides on its own when those dependencies are satisfied
- It does its job and publishes results for others to use

The **orchestrator** simply keeps track of who's done and kicks off whoever's ready next. It doesn't micromanage — just coordinates.

---

## 🏗️ Architecture Overview

Here's the big picture:

```
┌─────────────────────────────────────────────────────────────┐
│                     ORCHESTRATOR                            │
│  "I keep track of who's done and start whoever's ready"     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   ┌─────────────────────────────────────────────────────┐   │
│   │              📦 SHARED DATA STATE                   │   │
│   │   "This is where agents drop off their work for     │   │
│   │    other agents to pick up"                         │   │
│   └─────────────────────────────────────────────────────┘   │
│                            │                                │
│          ┌─────────────────┼─────────────────┐              │
│          ▼                 ▼                 ▼              │
│     ┌─────────┐      ┌──────────┐      ┌──────────┐        │
│     │ 🤖 5    │      │ 🧠 LLM   │      │ 📝 3     │        │
│     │ Agents  │      │ Client   │      │Templates │        │
│     └─────────┘      └──────────┘      └──────────┘        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 👥 Meet the Agents

### 1. 🔍 Data Parser Agent

**The Gatekeeper**

| | |
|---|---|
| **Job** | Take raw product data and turn it into a clean, validated model |
| **Waits for** | Nothing — it goes first |
| **Uses LLM?** | No — pure validation |
| **Output** | A Pydantic `Product` model that everyone else can trust |

This agent is simple but crucial. Garbage in, garbage out — so it makes sure the data is solid before anyone else touches it.

---

### 2. ❓ Question Generation Agent

**The Curious One**

| | |
|---|---|
| **Job** | Generate 15 diverse questions a real user might ask |
| **Waits for** | Parser |
| **Uses LLM?** | Yes — crafts natural, varied questions |
| **Output** | Questions across 5 categories: Informational, Safety, Usage, Purchase, Comparison |

Why not hardcode questions? Because real users ask things in unexpected ways. The LLM generates questions that feel human.

---

### 3. 📦 Product Page Agent

**The Copywriter**

| | |
|---|---|
| **Job** | Create compelling product page content |
| **Waits for** | Parser |
| **Uses LLM?** | Yes — writes marketing copy |
| **Output** | Description, benefits, usage instructions, ingredient explanations, safety info |

This is your product storyteller. It takes dry data and turns it into content that sells.

---

### 4. ⚖️ Comparison Agent

**The Analyst**

| | |
|---|---|
| **Job** | Generate a competitor product and analyze differences |
| **Waits for** | Parser |
| **Uses LLM?** | Yes (twice!) — first to create a competitor, then to compare |
| **Output** | Two products side-by-side with ingredient, price, and effectiveness comparisons |

The clever part: it *invents* a realistic competitor. No external data needed — just smart LLM prompting.

---

### 5. 💬 FAQ Generation Agent

**The Helper**

| | |
|---|---|
| **Job** | Answer all the questions from the Question Agent |
| **Waits for** | Parser AND Questions |
| **Uses LLM?** | Yes — generates helpful, accurate answers |
| **Output** | 15 Q&A pairs ready for a FAQ page |

This agent has the most dependencies because it needs both the product data AND the questions before it can work.

---

## 🔄 The Execution Flow

Let's walk through what happens when you run `python main.py`:

```
1️⃣  INITIALIZE
    └── Create all 5 agent instances
    └── Set up the shared data dictionary
    └── Configure rate limiting (5 sec between LLM agents)

2️⃣  LOAD DATA
    └── Product data goes into shared_data["raw_input"]

3️⃣  RUN THE DAG
    └── Loop until everyone's done:
        ├── "Who can run?" (check dependencies)
        ├── Run those agents
        ├── Store their outputs
        ├── Wait for rate limits if needed
        └── Repeat

4️⃣  COLLECT RESULTS
    └── Grab FAQ, Product, and Comparison outputs

5️⃣  SAVE FILES
    └── Write everything to output/ as JSON
```

---

## 🔀 The DAG (Who Waits for Whom)

This is the dependency graph:

```
                    ┌─────────┐
        START ────▶ │ Parser  │
                    └────┬────┘
                         │
         ┌───────────────┼───────────────┐
         │               │               │
         ▼               ▼               ▼
    ┌─────────┐    ┌─────────┐    ┌────────────┐
    │Questions│    │ Product │    │ Comparison │
    └────┬────┘    └─────────┘    └────────────┘
         │              │               │
         │              └───────┬───────┘
         │                      │
         ▼                      ▼
     ┌───────┐              COMPLETE
     │  FAQ  │                  ▲
     └───┬───┘                  │
         └──────────────────────┘
```

**Translation:**
1. Parser runs first (no dependencies)
2. Questions, Product, and Comparison can run next (all just need Parser)
3. FAQ runs last (needs both Parser AND Questions)

---

## 🧠 The LLM Integration

We use **Groq** because it's *fast*. Like, really fast.

| Setting | Value |
|---------|-------|
| **Provider** | Groq Cloud |
| **Model** | `llama-3.3-70b-versatile` |
| **Output format** | Structured JSON |
| **Rate limit handling** | Exponential backoff (10s → 20s → 30s) |
| **Max retries** | 3 |
| **Delay between agents** | 5 seconds |

The `llm_client.py` handles all the messy stuff:
- Cleaning up markdown from responses
- Extracting JSON from freeform text
- Retrying on rate limits
- Validating responses

---

## 📐 The Template System

Templates aren't just formatting — they're **validation**. Each template checks that the agent output is complete before structuring it.

| Template | Validates | Output Shape |
|----------|-----------|--------------|
| **FAQTemplate** | Every Q&A has both question AND answer | `{page_type, faqs: [{question, answer}]}` |
| **ProductTemplate** | Has name, benefits, usage, ingredients, price | `{page_type, sections: {...}}` |
| **ComparisonTemplate** | Has both products and metrics | `{page_type, products: [], comparison_metrics: []}` |

If something's missing, the template throws an error. No silent failures.

---

## 🛠️ Utility Functions

The `content_blocks/generators.py` has pure utility functions for deterministic operations:

| Function | What It Does |
|----------|--------------|
| `extract_product_summary` | Quick one-liner summary of a product |
| `calculate_price_difference` | Math for price comparisons |
| `extract_common_ingredients` | Find what two products share |
| `extract_unique_ingredients` | Find what's unique to one product |

These don't use the LLM — they're just reliable helper functions.

---

## 📂 Output Files

After a successful run, you'll find these in `output/`:

| File | What's Inside |
|------|---------------|
| `faq.json` | 15 Q&As across 5 categories |
| `product_page.json` | Complete product page sections |
| `comparison_page.json` | Two products + detailed comparison metrics |

All files are **machine-readable JSON** — plug them into your CMS, API, or frontend.

---

## 🚀 Running the System

### Prerequisites
- Python 3.8 or higher
- A Groq API key (free tier works!)

### Steps

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set up your API key
echo "GROQ_API_KEY=your_key_here" > .env

# 3. Run it
python main.py
```

### What You'll See

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
Executing agent: product...
Agent product completed.
...

✓ faq.json
✓ product_page.json
✓ comparison_page.json

============================================================
All pages generated successfully!
Outputs saved to: output/
============================================================
```

---

## 🔑 Key Design Principles

### 1. Autonomy
Each agent makes its own decisions. The orchestrator doesn't tell agents *how* to do their job — just *when* they can start.

### 2. Modularity
Every piece is a separate module:
- Swap the LLM? Just edit `llm_client.py`
- Add a new agent? Create a file in `agents/` and register it
- Change output format? Modify the template

### 3. Separation of Concerns
- **Agents** = business logic
- **Templates** = output structure
- **LLM Client** = external API
- **Orchestrator** = workflow coordination
- **Models** = data validation

### 4. Fail Gracefully
Rate limits? Retry with backoff. Invalid JSON? Parse what we can. Missing field? Use sensible defaults.

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| Language | Python 3.8+ |
| LLM | Groq Cloud (Llama 3.3 70B) |
| Validation | Pydantic |
| Config | python-dotenv |
| Output | JSON |

---

## 🎉 That's It!

You now understand how 5 specialized agents collaborate to turn simple product data into rich, structured content.

The key insight: **let each agent be an expert at one thing**, and **let the orchestrator handle coordination**. It's simpler, more maintainable, and more powerful than a monolithic script.

Happy generating! 🚀

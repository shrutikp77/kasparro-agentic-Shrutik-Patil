"""
Main Entry Point

Kasparro AI - Agentic Content Generation System

This is the main entry point for the content generation application.
Executes the multi-agent LangGraph pipeline for content generation.
"""

from src.orchestrator import AgentOrchestrator
from src.utils import write_json_output
from src.config import SAMPLE_PRODUCT_DATA


def main():
    """
    Main function to run the agentic content generation system.
    """
    print("=" * 60)
    print("Kasparro AI - Agentic Content Generation System")
    print("=" * 60)
    
    print("\nStarting multi-agent content generation pipeline...")
    
    # Use product data from centralized config
    product_data = SAMPLE_PRODUCT_DATA
    
    print(f"\nProduct: {product_data['name']}")
    print(f"Price: {product_data['price']}")
    
    # Initialize AgentOrchestrator
    orchestrator = AgentOrchestrator()
    
    print("\nAgent execution order based on DAG dependencies...")
    print("  parser (no deps) → runs first")
    print("  questions, product, comparison (dep: parser) → run after parser")
    print("  faq (deps: parser, questions) → runs after questions")
    
    # Run the DAG execution
    print("\n" + "-" * 40)
    print("Executing agents...")
    print("-" * 40)
    
    results = orchestrator.execute_dag(product_data)
    
    # Print status of each agent
    agent_statuses = orchestrator.get_agent_status()
    for agent_id, status in agent_statuses.items():
        print(f"  [{agent_id}] {status}")
    
    # Write outputs to JSON files
    print("\n" + "-" * 40)
    print("Saving outputs to JSON files...")
    print("-" * 40)
    
    write_json_output(results["faq"], "faq.json")
    print("  ✓ faq.json")
    
    write_json_output(results["product"], "product_page.json")
    print("  ✓ product_page.json")
    
    write_json_output(results["comparison"], "comparison_page.json")
    print("  ✓ comparison_page.json")
    
    print("\n" + "=" * 60)
    print("All pages generated successfully!")
    print("Outputs saved to: output/")
    print("=" * 60)
    
    return results


if __name__ == "__main__":
    main()

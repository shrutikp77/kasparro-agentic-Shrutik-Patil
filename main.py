"""
Main Entry Point

Kasparro AI - Agentic Content Generation System

This is the main entry point for the content generation application.
Executes the multi-agent LangGraph pipeline for content generation.
"""

import argparse
import sys
from pathlib import Path

from src.orchestrator import AgentOrchestrator
from src.utils import write_json_output, load_product_from_dataset
from src.config import DEFAULT_DATASET_PATH, OUTPUT_DIR
from src.validators import validate_output_schema


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Kasparro AI - Multi-Agent Content Generation System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Use default dataset
  python main.py
  
  # Use custom dataset
  python main.py --dataset data/my_products.json
  
  # Select different product from dataset
  python main.py --dataset data/products.json --product-index 1
  
  # Use custom output directory
  python main.py --output-dir custom_output/
        """
    )
    
    parser.add_argument(
        '--dataset',
        type=str,
        default=DEFAULT_DATASET_PATH,
        help=f'Path to product dataset JSON file (default: {DEFAULT_DATASET_PATH})'
    )
    
    parser.add_argument(
        '--product-index',
        type=int,
        default=0,
        help='Index of product to use from dataset (default: 0)'
    )
    
    parser.add_argument(
        '--output-dir',
        type=str,
        default=OUTPUT_DIR,
        help=f'Output directory for generated files (default: {OUTPUT_DIR})'
    )
    
    return parser.parse_args()


def main():
    """
    Main function to run the agentic content generation system.
    """
    # Parse CLI arguments
    args = parse_arguments()
    
    print("=" * 60)
    print("Kasparro AI - Agentic Content Generation System")
    print("=" * 60)
    
    # Load product data from dataset
    print(f"\nLoading dataset: {args.dataset}")
    try:
        product_data = load_product_from_dataset(args.dataset, args.product_index)
    except (FileNotFoundError, IndexError, KeyError, ValueError) as e:
        print(f"❌ Error loading dataset: {e}")
        sys.exit(1)
    
    print(f"\n✓ Loaded product: {product_data['name']}")
    print(f"  Price: {product_data.get('price', 'N/A')}")
    print(f"  Product index: {args.product_index}")
    
    print("\n" + "=" * 60)
    print("Starting multi-agent content generation pipeline...")
    print("=" * 60)
    
    # Initialize AgentOrchestrator
    orchestrator = AgentOrchestrator()
    
    print("\nAgent execution order based on DAG dependencies:")
    print("  parser (no deps) → runs first")
    print("  questions, product, comparison (dep: parser) → run after parser")
    print("  faq (deps: parser, questions) → runs after questions")
    
    # Run the DAG execution
    print("\n" + "-" * 60)
    print("Executing agents...")
    print("-" * 60)
    
    try:
        results = orchestrator.execute_dag(product_data)
    except Exception as e:
        print(f"\n❌ Pipeline execution failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    # Print status of each agent
    agent_statuses = orchestrator.get_agent_status()
    print("\nAgent Execution Status:")
    for agent_id, status in agent_statuses.items():
        status_symbol = "✓" if status == "completed" else "✗"
        print(f"  {status_symbol} [{agent_id}] {status}")
    
    # Validate outputs
    print("\n" + "-" * 60)
    print("Validating outputs...")
    print("-" * 60)
    
    try:
        validate_output_schema(results["faq"], "faq")
        print("  ✓ FAQ validation passed (count >= 15)")
        
        validate_output_schema(results["product"], "product")
        print("  ✓ Product page validation passed")
        
        validate_output_schema(results["comparison"], "comparison")
        print("  ✓ Comparison page validation passed")
        
    except ValueError as e:
        print(f"\n❌ Validation failed: {e}")
        sys.exit(1)
    
    # Write outputs to JSON files
    print("\n" + "-" * 60)
    print(f"Saving outputs to: {args.output_dir}")
    print("-" * 60)
    
    try:
        write_json_output(results["faq"], "faq.json", args.output_dir)
        print("  ✓ faq.json")
        
        write_json_output(results["product"], "product_page.json", args.output_dir)
        print("  ✓ product_page.json")
        
        write_json_output(results["comparison"], "comparison_page.json", args.output_dir)
        print("  ✓ comparison_page.json")
        
    except Exception as e:
        print(f"\n❌ Error writing outputs: {e}")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("✓ All pages generated successfully!")
    print(f"✓ Outputs saved to: {Path(args.output_dir).absolute()}")
    print(f"✓ FAQ count: {len(results['faq']['faqs'])}")
    print("=" * 60)
    
    return results


if __name__ == "__main__":
    main()

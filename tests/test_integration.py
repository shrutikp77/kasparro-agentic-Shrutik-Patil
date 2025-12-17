"""
Integration Tests for Content Generation System

Tests the end-to-end workflow and LangGraph integration.
Uses mocked LLM to avoid actual API calls during testing.
"""

import pytest
from typing import Dict, Any
from unittest.mock import patch, MagicMock

from src.orchestrator import AgentOrchestrator
from src.templates.template_definitions import FAQTemplate, ProductTemplate, ComparisonTemplate
from src.models.schemas import Product, Question


class TestTemplates:
    """Tests for template classes."""
    
    def test_faq_template_build(self):
        """Test FAQTemplate builds valid output."""
        questions = [
            {"question": "What is this product?", "answer": "A Vitamin C serum."},
            {"question": "How to use it?", "answer": "Apply 2-3 drops daily."}
        ]
        
        result = FAQTemplate.build(questions)
        
        assert result["page_type"] == "faq"
        assert "faqs" in result
        assert len(result["faqs"]) == 2
    
    def test_faq_template_validates_fields(self):
        """Test FAQTemplate raises error for missing fields."""
        invalid_questions = [
            {"question": "What?"}  # Missing 'answer'
        ]
        
        with pytest.raises(ValueError) as excinfo:
            FAQTemplate.build(invalid_questions)
        
        assert "missing 'answer' field" in str(excinfo.value)
    
    def test_product_template_build(self):
        """Test ProductTemplate builds valid output."""
        product_data = {
            "name": "Test Product",
            "description": "A test product",
            "concentration": "10%",
            "benefits": ["Benefit 1", "Benefit 2"],
            "how_to_use": "Use daily",
            "key_ingredients": ["Ingredient 1"],
            "price": "₹500",
            "side_effects": "None"
        }
        
        result = ProductTemplate.build(product_data)
        
        assert result["page_type"] == "product"
        assert "sections" in result
        assert result["sections"]["name"] == "Test Product"
    
    def test_product_template_validates_required_fields(self):
        """Test ProductTemplate raises error for missing required fields."""
        incomplete_data = {
            "name": "Test"
            # Missing: benefits, how_to_use, key_ingredients, price
        }
        
        with pytest.raises(ValueError) as excinfo:
            ProductTemplate.build(incomplete_data)
        
        assert "Missing required field" in str(excinfo.value)
    
    def test_comparison_template_build(self):
        """Test ComparisonTemplate builds valid output."""
        product_a = {"name": "Product A", "price": "₹500"}
        product_b = {"name": "Product B", "price": "₹600"}
        metrics = [{"difference": "₹100"}]
        
        result = ComparisonTemplate.build(product_a, product_b, metrics)
        
        assert result["page_type"] == "comparison"
        assert "products" in result
        assert len(result["products"]) == 2
        assert "comparison_metrics" in result


class TestOrchestratorInitialization:
    """Tests for AgentOrchestrator initialization."""
    
    def test_orchestrator_creates_workflow(self):
        """Test that orchestrator initializes with LangGraph workflow."""
        orchestrator = AgentOrchestrator()
        
        assert orchestrator.workflow is not None
        assert orchestrator._last_state == {}
    
    def test_orchestrator_reset(self):
        """Test that reset clears last state."""
        orchestrator = AgentOrchestrator()
        orchestrator._last_state = {"test": "data"}
        
        orchestrator.reset()
        
        assert orchestrator._last_state == {}
    
    def test_get_agent_status_initial(self):
        """Test initial agent status before execution."""
        orchestrator = AgentOrchestrator()
        
        status = orchestrator.get_agent_status()
        
        assert status["parser"] == "pending"
        assert status["questions"] == "pending"
        assert status["faq"] == "pending"
        assert status["product"] == "pending"
        assert status["comparison"] == "pending"


class TestLangGraphWorkflow:
    """Tests for LangGraph workflow structure."""
    
    def test_workflow_imports(self):
        """Test that LangGraph workflow can be imported."""
        from src.graph.workflow import content_workflow, create_workflow
        
        assert content_workflow is not None
        assert create_workflow is not None
    
    def test_state_type_imports(self):
        """Test that state types can be imported."""
        from src.graph.state import ContentGenerationState
        
        assert ContentGenerationState is not None
    
    def test_workflow_has_nodes(self):
        """Test that workflow has expected nodes."""
        from src.graph.workflow import create_workflow
        
        workflow = create_workflow()
        
        # LangGraph compiled graph should exist
        assert workflow is not None


class TestSchemaValidation:
    """Tests for Pydantic schema validation."""
    
    def test_product_schema_valid(self, sample_product_data):
        """Test Product schema with valid data."""
        product = Product(**sample_product_data)
        
        assert product.name == "Test Vitamin C Serum"
        assert product.concentration == "10% Vitamin C"
        assert len(product.skin_type) == 2
    
    def test_product_schema_model_dump(self, sample_product_data):
        """Test Product schema model_dump method."""
        product = Product(**sample_product_data)
        
        data = product.model_dump()
        
        assert isinstance(data, dict)
        assert data["name"] == "Test Vitamin C Serum"
    
    def test_question_schema_valid(self):
        """Test Question schema with valid data."""
        question = Question(
            id="q1",
            text="What does this product do?",
            category="INFORMATIONAL"
        )
        
        assert question.id == "q1"
        assert question.text == "What does this product do?"
        assert question.answer is None  # Optional field


class TestMockedWorkflowExecution:
    """Tests for workflow execution with mocked LLM."""
    
    @patch('src.graph.workflow.get_llm_client')
    def test_parse_product_node(self, mock_get_llm, sample_product_data):
        """Test parse_product node function."""
        from src.graph.workflow import parse_product
        
        state = {"raw_input": sample_product_data}
        result = parse_product(state)
        
        assert "parsed_product" in result
        assert isinstance(result["parsed_product"], Product)
        assert result["parsed_product"].name == "Test Vitamin C Serum"
    
    @patch('src.graph.workflow.get_llm_client')
    @patch('src.graph.workflow._delay_for_rate_limit')
    def test_generate_questions_node(self, mock_delay, mock_get_llm, sample_product_data, mock_llm_client):
        """Test generate_questions node with mocked LLM."""
        from src.graph.workflow import generate_questions
        
        # Setup mock
        mock_get_llm.return_value = mock_llm_client
        mock_llm_client.generate_json.return_value = [
            {"id": "q1", "text": "What is this?", "category": "INFORMATIONAL"},
            {"id": "q2", "text": "Is it safe?", "category": "SAFETY"}
        ]
        
        product = Product(**sample_product_data)
        state = {"parsed_product": product}
        
        result = generate_questions(state)
        
        assert "questions" in result
        assert len(result["questions"]) == 2
        mock_llm_client.generate_json.assert_called_once()
    
    @patch('src.graph.workflow.get_llm_client')
    @patch('src.graph.workflow._delay_for_rate_limit')
    def test_generate_faq_node(self, mock_delay, mock_get_llm, sample_product_data, mock_faq_response):
        """Test generate_faq_page node with mocked LLM."""
        from src.graph.workflow import generate_faq_page
        from unittest.mock import MagicMock
        
        # Setup mock
        mock_llm = MagicMock()
        mock_get_llm.return_value = mock_llm
        mock_llm.generate_json.return_value = mock_faq_response
        
        product = Product(**sample_product_data)
        questions = [
            Question(id="q1", text="What is this?", category="INFORMATIONAL"),
            Question(id="q2", text="How to use?", category="USAGE")
        ]
        state = {"parsed_product": product, "questions": questions}
        
        result = generate_faq_page(state)
        
        assert "faq_output" in result
        assert result["faq_output"]["page_type"] == "faq"


class TestOutputStructure:
    """Tests for output structure validation."""
    
    def test_faq_output_structure(self):
        """Test that FAQ output has expected structure."""
        faq_items = [
            {"question": "Q1?", "answer": "A1."},
            {"question": "Q2?", "answer": "A2."}
        ]
        
        output = FAQTemplate.build(faq_items)
        
        assert "page_type" in output
        assert output["page_type"] == "faq"
        assert "faqs" in output
        for faq in output["faqs"]:
            assert "question" in faq
            assert "answer" in faq
    
    def test_product_output_structure(self, sample_product_data):
        """Test that product output has expected structure."""
        product_data = sample_product_data.copy()
        product_data["description"] = "A great product"
        
        output = ProductTemplate.build(product_data)
        
        assert output["page_type"] == "product"
        assert "sections" in output
        sections = output["sections"]
        assert "name" in sections
        assert "benefits" in sections
        assert "usage" in sections
        assert "ingredients" in sections
        assert "price" in sections


class TestOutputValidation:
    """Tests for output validation."""
    
    def test_faq_count_validation(self, mock_faq_response):
        """Test that FAQ count validation enforces minimum 15 FAQs."""
        from src.validators import validate_faq_count
        
        # Valid FAQ (15 questions)
        valid_faq = FAQTemplate.build(mock_faq_response)
        validate_faq_count(valid_faq)  # Should not raise
        
        # Invalid FAQ (less than 15 questions)
        invalid_faq = FAQTemplate.build(mock_faq_response[:10])
        
        import pytest
        with pytest.raises(ValueError) as excinfo:
            validate_faq_count(invalid_faq)
        
        assert "less than required minimum" in str(excinfo.value)
        assert "15" in str(excinfo.value)
    
    def test_output_schema_validation(self):
        """Test output schema validation."""
        from src.validators import validate_output_schema
        
        # Valid FAQ output
        valid_faq = {
            "page_type": "faq",
            "faqs": [{"question": f"Q{i}?", "answer": f"A{i}."} for i in range(15)]
        }
        validate_output_schema(valid_faq, "faq")  # Should not raise
        
        # Invalid FAQ output (wrong page_type)
        import pytest
        with pytest.raises(ValueError) as excinfo:
            validate_output_schema({"page_type": "product"}, "faq")
        
        assert "Expected page_type 'faq'" in str(excinfo.value)

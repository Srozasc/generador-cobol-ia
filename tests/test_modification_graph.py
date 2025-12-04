"""
Tests para la integración del Modo Modificación en el Grafo.

Verifica que el grafo pueda ejecutar el flujo completo de modificación:
Planner -> Coder -> Validator (mock) para código COBOL existente.
"""

import pytest
from unittest.mock import MagicMock, patch
from core.graph import GraphState, get_compiled_graph, run_documentation_process

class TestModificationGraphIntegration:
    """
    Tests para la integración del modo modificación en el grafo.
    """

    @pytest.fixture
    def sample_cobol_code(self):
        """Código COBOL de ejemplo para modificar."""
        return """       IDENTIFICATION DIVISION.
       PROGRAM-ID. COBPROG01.
       DATA DIVISION.
       WORKING-STORAGE SECTION.
       01  WS-MONTO-PAGO     PIC 9(07)V99.
       PROCEDURE DIVISION.
       PAR-VALIDACION.
           IF WS-MONTO-PAGO > 5000
               DISPLAY 'PAGO ALTO'
           END-IF.
           STOP RUN.
        """

    def test_graph_state_supports_modification_mode(self):
        """
        Test que verifica que GraphState soporta los campos necesarios para modificación.
        """
        # Arrange & Act
        state = GraphState(
            request="Cambiar límite a 10000",
            code="",
            plan={},
            error_message="",
            mode="modification",
            original_code="COBOL CODE HERE"
        )
        
        # Assert
        assert state["mode"] == "modification"
        assert "original_code" in state
        assert state["original_code"] == "COBOL CODE HERE"

    @patch("agents.planner.ChatGoogleGenerativeAI")
    @patch("agents.coder.ChatGoogleGenerativeAI")
    def test_modification_flow_executes_planner_coder_validator(
        self, mock_coder_llm, mock_planner_llm, sample_cobol_code
    ):
        """
        Test que verifica que el flujo de modificación ejecuta Planner -> Coder -> Validator.
        """
        # Arrange
        from types import SimpleNamespace
        
        # Mock Planner
        mock_plan = SimpleNamespace(content="""
        {
            "plan": "Modificar validación",
            "mode": "modification",
            "analysis": "Cambiar límite",
            "steps": ["Modificar IF"]
        }
        """)
        mock_planner = mock_planner_llm.return_value
        mock_planner.invoke.return_value = mock_plan
        mock_planner.return_value = mock_plan
        
        # Mock Coder
        modified_code = sample_cobol_code.replace("5000", "10000")
        mock_code_response = SimpleNamespace(content=modified_code)
        mock_coder = mock_coder_llm.return_value
        mock_coder.invoke.return_value = mock_code_response
        mock_coder.return_value = mock_code_response
        
        # Validator es un mock, no necesita patch
        
        # Act
        graph = get_compiled_graph()
        initial_state = GraphState(
            request="Cambiar límite de pago a 10000",
            code=sample_cobol_code,  # Código original
            plan={},
            error_message="",
            mode="modification"
        )
        
        result = graph.invoke(initial_state)
        
        # Assert
        assert result is not None
        assert result["mode"] == "modification"
        assert "10000" in result["code"]  # Verificar que se modificó
        assert "IDENTIFICATION DIVISION" in result["code"]  # Preservó estructura

    def test_modification_mode_preserves_original_code_in_state(self, sample_cobol_code):
        """
        Test que verifica que el código original se preserva en el estado durante el flujo.
        """
        # Arrange
        initial_state = GraphState(
            request="Cambiar algo",
            code=sample_cobol_code,
            plan={},
            error_message="",
            mode="modification"
        )
        
        # Act & Assert
        # El estado inicial debe tener el código
        assert initial_state["code"] == sample_cobol_code
        assert initial_state["mode"] == "modification"

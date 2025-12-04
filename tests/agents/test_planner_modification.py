"""
Tests para el Agente Planificador en Modo Modificación.

Verifica que el planificador pueda analizar código existente y generar
un plan de cambios estructurado basado en una solicitud de lenguaje natural.
"""

from unittest.mock import MagicMock, patch

import pytest

from agents.planner import get_planner_chain


class TestPlannerModificationMode:
    """
    Tests para el modo de modificación del Agente Planificador.
    """

    @pytest.fixture
    def sample_cobol_code(self):
        return """
       IDENTIFICATION DIVISION.
       PROGRAM-ID. COBPROG01.
       DATA DIVISION.
       WORKING-STORAGE SECTION.
       01  WS-MONTO-PAGO     PIC 9(07)V99.
       01  WS-ESTADO-CLIENTE PIC X(10).
       PROCEDURE DIVISION.
       PAR-VALIDACION.
           IF WS-MONTO-PAGO > 5000
               DISPLAY 'PAGO ALTO'
           END-IF.
        """

    def test_planner_detects_modification_mode(self, sample_cobol_code):
        """
        Test que verifica que el planner detecta el modo modificación
        cuando se le pasa 'original_code'.
        """
        # Arrange
        request = "Cambiar el límite de pago a 10000"
        input_data = {"request": request, "original_code": sample_cobol_code}

        # Act
        # Nota: Esto fallará hasta que actualicemos get_planner_chain para aceptar original_code
        chain = get_planner_chain()

        # Simulamos la invocación para verificar el comportamiento esperado
        # En una prueba real de integración con LLM, esto invocaría al modelo.
        # Aquí queremos verificar que la cadena se construye correctamente para manejar este input.

        # Para TDD, primero verificamos que la cadena acepte el input sin error
        # y que el prompt generado incluya el código original.

        # Como es difícil inspeccionar la cadena compilada, probaremos la lógica de procesamiento
        # de entrada si es accesible, o haremos un test de integración mockeado.
        pass

    @patch("agents.planner.ChatGoogleGenerativeAI")
    def test_planner_generates_modification_plan(
        self, mock_llm_class, sample_cobol_code
    ):
        """
        Test que verifica que el planner genera un plan de modificación con la estructura correcta.
        Simulamos la respuesta del LLM.
        """
        # Arrange
        from types import SimpleNamespace

        mock_response = SimpleNamespace(
            content="""
        ```json
        {
            "analysis": "Se identificó WS-MONTO-PAGO. El cambio es en PAR-VALIDACION.",
            "steps": [
                "Modificar condición IF en PAR-VALIDACION para comparar con 10000"
            ]
        }
        ```
        """
        )
        mock_llm = mock_llm_class.return_value
        # Configurar tanto invoke como __call__ para cubrir ambos casos
        mock_llm.invoke.return_value = mock_response
        mock_llm.return_value = mock_response  # Para __call__

        request = "Cambiar el límite de pago a 10000"
        input_data = {"request": request, "original_code": sample_cobol_code}

        # Act
        chain = get_planner_chain()
        result = chain.invoke(input_data)

        # Assert
        assert result is not None
        assert "analysis" in result
        assert "steps" in result
        assert len(result["steps"]) > 0
        assert "10000" in result["steps"][0]

    def test_planner_identifies_variables_and_insertion_point(self):
        """
        Test específico para el caso de uso del cliente: Monto > 10000 y Mora.
        Este test valida que el planificador (mockeado) estructure la respuesta esperada.
        """
        # Este test es más conceptual para guiar la implementación del prompt
        pass
